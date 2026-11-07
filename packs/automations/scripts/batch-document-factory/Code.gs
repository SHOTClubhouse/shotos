/**
 * Batch Document Factory (Google Apps Script, V8 runtime)
 *
 * Makes one Google Doc (or Slides deck) per row of a sheet, from one master
 * template, by replacing {{placeholders}} with the values in the row.
 *
 * What it will never do: send, share or delete anything. It creates copies of
 * your template and fills them. A copy that fails is renamed with a "FAILED - "
 * prefix and kept, never trashed; a retry fills that same copy.
 *
 * Safety design:
 *   - One atomic update per document: all placeholders are replaced in a single
 *     Docs or Slides batchUpdate call, which applies fully or not at all.
 *   - A done marker column. Rows marked DONE are never touched on a rerun.
 *   - A copy_state column tells a retry of a failed new copy (copy_state "retry":
 *     the same copy is reused) from a redo of a finished row (copy_state
 *     "complete", done cleared: a fresh copy is made and the old id is kept in
 *     previous_doc_ids). A filled document is never reused as a fresh fill.
 *   - Sample mode processes three rows only. Dry-run mode creates nothing.
 *   - Time-boxed batches: when time runs short the script schedules its own
 *     continuation trigger, and deletes it when no rows are left.
 *   - A banned-term check blocks a row before any document is made.
 *   - A Report tab records every decision, with attempt counts for retry.
 *
 * Sheet layout (tab "Rows"): row 1 is headers. Each header that is not a
 * control column is a placeholder name: the header "client" fills {{client}}.
 * Control columns (added by setupFactory): doc_name, done, status, doc_id,
 * doc_url, attempts, previous_doc_ids, last_message, done_at, copy_state.
 *
 * Setup in short (full steps in README.md):
 *   1. Paste Code.gs and appsscript.json into a project bound to your sheet.
 *   2. Set TEMPLATE_ID and OUTPUT_FOLDER_ID (both required for live runs) in
 *      Script Properties.
 *   3. Run setupFactory(), fill the Rows tab, run dryRun(), then runSample(),
 *      read the documents, and only then runBatch().
 */

// ---------------------------------------------------------------------------
// CONFIGURATION
// ---------------------------------------------------------------------------

var CONFIG = {
  // Prefer Script Properties TEMPLATE_ID and OUTPUT_FOLDER_ID; these are fallbacks.
  TEMPLATE_ID: '',
  OUTPUT_FOLDER_ID: '',            // required for live runs. Copies inherit this folder's sharing, so use a private one.

  PLACEHOLDER_OPEN: '{{',
  PLACEHOLDER_CLOSE: '}}',

  // Name for each new document. {{column}} tokens and {{row}} are filled in.
  NAME_PATTERN: 'Document {{row}}',

  SAMPLE_ROWS: 3,                  // rows processed by runSample()
  BATCH_BUDGET_MS: 4 * 60 * 1000 + 30 * 1000, // stop starting rows after 4.5 minutes
  CONTINUE_AFTER_MS: 60 * 1000,    // when the continuation trigger fires after a stop
  MAX_ATTEMPTS: 3,                 // a row with this many failed attempts waits for retryFailed()
  REQUIRE_ALL_VALUES: true,        // block a row if a placeholder column is empty
  OPTIONAL_COLUMNS: [],            // placeholder columns allowed to be empty, lower case

  // Terms that block a row. The BannedTerms tab adds to this list.
  BANNED_TERMS: [],

  DONE_VALUE: 'DONE',
  LOCK_WAIT_MS: 30 * 1000,

  TAB_ROWS: 'Rows',
  TAB_BANNED: 'BannedTerms',
  TAB_REPORT: 'Report'
};

var CONTROL_COLUMNS = ['doc_name', 'done', 'status', 'doc_id', 'doc_url', 'attempts',
  'previous_doc_ids', 'last_message', 'done_at', 'copy_state'];
var REPORT_HEADERS = ['Timestamp', 'RunId', 'Row', 'DocName', 'Action', 'DocId', 'DocUrl', 'Detail', 'Attempt'];

var CONTINUE_HANDLER = 'continueBatch';
var DOC_MIME = 'application/vnd.google-apps.document';
var SLIDES_MIME = 'application/vnd.google-apps.presentation';
var FAILED_PREFIX = 'FAILED - ';

var REPORT_BUFFER_ = [];
var RUN_ID_ = '';

// ---------------------------------------------------------------------------
// ENTRY POINTS
// ---------------------------------------------------------------------------

/** Creates the Rows, BannedTerms and Report tabs and adds missing control columns. Safe to rerun. */
function setupFactory() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var rows = ss.getSheetByName(CONFIG.TAB_ROWS) || ss.insertSheet(CONFIG.TAB_ROWS);
  var banned = ss.getSheetByName(CONFIG.TAB_BANNED);
  if (!banned) {
    banned = ss.insertSheet(CONFIG.TAB_BANNED);
    banned.getRange(1, 1).setValue('Banned term (one per row)').setFontWeight('bold');
  }
  var report = ss.getSheetByName(CONFIG.TAB_REPORT);
  if (!report) {
    report = ss.insertSheet(CONFIG.TAB_REPORT);
    report.getRange(1, 1, 1, REPORT_HEADERS.length).setValues([REPORT_HEADERS]).setFontWeight('bold');
    report.setFrozenRows(1);
  }
  var width = Math.max(rows.getLastColumn(), 1);
  var headers = rows.getRange(1, 1, 1, width).getValues()[0].map(function (h) { return String(h).trim(); });
  if (headers.length === 1 && headers[0] === '') { headers = []; }
  var lower = headers.map(function (h) { return h.toLowerCase(); });
  CONTROL_COLUMNS.forEach(function (name) {
    if (lower.indexOf(name) === -1) {
      headers.push(name);
      lower.push(name);
    }
  });
  rows.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight('bold');
  rows.setFrozenRows(1);
  Logger.log('Setup done. Add placeholder columns to the left of doc_name, one per {{placeholder}} in the template.');
}

/** Checks everything and reports what would happen. Creates no documents and changes no rows. */
function dryRun() {
  runWithLock_('dryRun', function () { processRows_({ mode: 'dry', limit: Infinity }); });
}

/** Processes the first three pending rows for real, so you can read the results. */
function runSample() {
  runWithLock_('runSample', function () { processRows_({ mode: 'live', limit: CONFIG.SAMPLE_ROWS }); });
}

/** Processes all pending rows, in time-boxed batches that continue themselves. */
function runBatch() {
  runWithLock_('runBatch', function () { processRows_({ mode: 'live', limit: Infinity }); });
}

/** Trigger entry point for the continuation. Takes no arguments on purpose. */
function continueBatch() {
  runWithLock_('continueBatch', function () { processRows_({ mode: 'live', limit: Infinity }); });
}

/** Clears the attempt count on rows in error, then processes them again. */
function retryFailed() {
  runWithLock_('retryFailed', function () {
    var table = readRows_();
    var changed = 0;
    table.data.forEach(function (row) {
      if (row.get('status') === 'error' && row.get('done') !== CONFIG.DONE_VALUE) {
        table.sheet.getRange(row.rowNumber, table.col.attempts + 1).setValue(0);
        changed++;
      }
    });
    report_('-', '', 'retry-reset', '', '', 'Reset attempts on ' + changed + ' row(s) in error.', '');
    processRows_({ mode: 'live', limit: Infinity });
  });
}

/** Read-only check that every DONE row still has an openable document. */
function auditDocuments() {
  runWithLock_('auditDocuments', function () {
    var table = readRows_();
    var checked = 0;
    var problems = 0;
    table.data.forEach(function (row) {
      if (row.get('done') !== CONFIG.DONE_VALUE) { return; }
      checked++;
      var id = row.get('doc_id');
      try {
        var file = DriveApp.getFileById(id);
        if (file.isTrashed()) { throw new Error('document is in the bin'); }
      } catch (err) {
        problems++;
        report_(row.rowNumber, row.get('doc_name'), 'audit-problem', id, '', String(err.message || err), '');
      }
    });
    report_('-', '', 'audit', '', '', 'Checked ' + checked + ' done row(s); ' + problems + ' problem(s).', '');
  });
}

/** Deletes this script's continuation triggers (the only triggers it ever makes). */
function removeContinuation() {
  deleteContinuationTriggers_();
}

// ---------------------------------------------------------------------------
// CORE LOOP
// ---------------------------------------------------------------------------

/**
 * Walks the pending rows. options.mode is 'dry' or 'live'; options.limit caps
 * how many rows are attempted in this run (blocked rows do not count).
 */
function processRows_(options) {
  var started = Date.now();
  var live = options.mode === 'live';
  if (live && options.limit === Infinity) {
    deleteContinuationTriggers_(); // a fresh one is made below only if work remains
  }

  var templateId = getSetting_('TEMPLATE_ID');
  if (!templateId) { throw new Error('Set TEMPLATE_ID in Script Properties (or CONFIG).'); }
  var template = inspectTemplate_(templateId);

  var outputFolderId = getSetting_('OUTPUT_FOLDER_ID');
  if (live) {
    if (!outputFolderId) {
      throw new Error('Set OUTPUT_FOLDER_ID in Script Properties (or CONFIG) before a live run. ' +
        'Use a private folder: copies inherit the sharing of the folder they are made in.');
    }
    DriveApp.getFolderById(outputFolderId); // fails early, with Drive's own message, if the folder is wrong
  } else {
    report_('-', '', 'folder-warning', outputFolderId, '', outputFolderId
      ? 'Copies would be made in the output folder and inherit its sharing. Check who can see it.'
      : 'OUTPUT_FOLDER_ID is blank: a live run will refuse to start. Copies inherit the sharing of the folder they are made in.', '');
  }

  var table = readRows_();
  var missing = template.keys.filter(function (k) { return table.col[k] === undefined; });
  if (missing.length) {
    report_('-', '', 'config-error', templateId, '', 'Template placeholders with no column in Rows: ' + missing.join(', '), '');
    throw new Error('Add columns for: ' + missing.join(', '));
  }

  var banned = readBannedTerms_();
  var created = 0, blocked = 0, failed = 0, skipped = 0, stoppedEarly = false;

  for (var i = 0; i < table.data.length; i++) {
    var row = table.data[i];
    if (row.get('done') === CONFIG.DONE_VALUE) { skipped++; continue; }
    var attempts = Number(row.get('attempts')) || 0;
    if (attempts >= CONFIG.MAX_ATTEMPTS) { skipped++; continue; }
    if (created + failed >= options.limit) { stoppedEarly = true; break; }
    if (live && Date.now() - started > CONFIG.BATCH_BUDGET_MS) { stoppedEarly = true; break; }

    var values = placeholderValues_(row, template.keys);
    var name = buildName_(row, table, template.keys);

    // 1. Checks that need no document.
    var problem = checkRow_(row, values, name, banned);
    if (problem) {
      blocked++;
      if (row.get('last_message') !== 'blocked: ' + problem) {
        report_(row.rowNumber, name, 'blocked', '', '', problem, attempts);
      }
      if (live) { setControl_(table, row, { status: 'blocked', last_message: 'blocked: ' + problem }); }
      continue;
    }

    // 2. Dry run stops here.
    if (!live) {
      created++;
      report_(row.rowNumber, name, 'would-create', '', '', 'Passes all checks. ' + template.keys.length + ' placeholder(s).', attempts);
      continue;
    }

    // 3. Make or reuse the document and fill it in.
    var existingId = String(row.get('doc_id') || '');
    var copyState = String(row.get('copy_state') || '');
    // Reuse only a copy that a failed attempt left unfinished. A completed row that was cleared
    // for regeneration (or a row from before copy_state existed) always gets a fresh copy.
    var reuse = existingId !== '' && copyState === 'retry' && isUsableFile_(existingId);
    // Placeholders are replaced in place, so a copy that was already filled (perhaps with older
    // sheet values) cannot be filled again. Reuse it only if every placeholder is still there;
    // otherwise make a fresh copy and fill it from the current sheet values.
    if (reuse && !hasAllPlaceholders_(existingId, template)) { reuse = false; }
    var docId = reuse ? existingId : '';
    try {
      if (!reuse) {
        docId = copyTemplate_(templateId, name);
        var fresh = { doc_id: docId, doc_url: '', copy_state: 'retry' };
        if (existingId) {
          fresh.previous_doc_ids = (row.get('previous_doc_ids') ? row.get('previous_doc_ids') + ', ' : '') + existingId;
        }
        // Recorded before filling, so a failure or a timeout leaves a copy the next attempt can find.
        setControl_(table, row, fresh);
      }
      fillDocument_(docId, template.type, template.tokens, values);
      var readBack = verifyDocument_(docId, template.type);
      if (readBack.length) { throw new Error('Placeholders still present after update: ' + readBack.join(', ')); }

      var file = DriveApp.getFileById(docId);
      if (reuse) { file.setName(name); } // undo the FAILED prefix
      setControl_(table, row, {
        done: CONFIG.DONE_VALUE, status: 'ok', doc_id: docId, doc_url: file.getUrl(),
        attempts: attempts + 1, last_message: 'created', done_at: new Date(), copy_state: 'complete'
      });
      created++;
      report_(row.rowNumber, name, reuse ? 'retried' : (existingId ? 'regenerated' : 'created'), docId, file.getUrl(),
        'Filled ' + template.tokens.length + ' placeholder(s) in one update and read back clean.', attempts + 1);
    } catch (err) {
      failed++;
      var message = String(err && err.message ? err.message : err);
      if (docId) { markCopyFailed_(docId, name); }
      var failure = { status: 'error', attempts: attempts + 1, last_message: truncate_(message, 200) };
      if (docId) { failure.doc_id = docId; failure.copy_state = 'retry'; }
      setControl_(table, row, failure);
      report_(row.rowNumber, name, 'error', docId || existingId, '', message +
        (docId ? ' The copy was kept as "' + FAILED_PREFIX + name + '" and the next attempt reuses it.' : ''), attempts + 1);
    }
  }

  var summary = (live ? '' : 'DRY RUN. ') + 'Created or would create ' + created + ', blocked ' + blocked +
    ', failed ' + failed + ', skipped ' + skipped + (stoppedEarly ? ', stopped early.' : '.');
  report_('-', '', 'summary', '', '', summary, '');

  // Continuation: only for a live full batch that stopped for time, not for a sample.
  var more = live && stoppedEarly && options.limit === Infinity;
  if (more) {
    var trigger = ScriptApp.newTrigger(CONTINUE_HANDLER).timeBased().after(CONFIG.CONTINUE_AFTER_MS).create();
    PropertiesService.getScriptProperties().setProperty('CONTINUATION_TRIGGER_ID', trigger.getUniqueId());
    report_('-', '', 'continuation-scheduled', '', '', 'More rows remain. Continuing in about a minute.', '');
  } else if (live && options.limit === Infinity) {
    report_('-', '', 'finished', '', '', 'No pending rows left. Continuation trigger removed.', '');
  }
}

/** Reasons a row cannot proceed: empty values, placeholder-shaped data, banned terms. Returns '' when clean. */
function checkRow_(row, values, name, banned) {
  if (CONFIG.REQUIRE_ALL_VALUES) {
    var empty = Object.keys(values).filter(function (k) {
      return values[k] === '' && CONFIG.OPTIONAL_COLUMNS.indexOf(k) === -1;
    });
    if (empty.length) { return 'empty value for: ' + empty.join(', '); }
  }
  // Ordered replacements can otherwise rewrite a token inserted as row data.
  var tokenColumns = Object.keys(values).filter(function (key) {
    return findTokens_(values[key]).length > 0;
  });
  if (tokenColumns.length) {
    return 'placeholder text in values for: ' + tokenColumns.join(', ');
  }
  var texts = [name].concat(Object.keys(values).map(function (k) { return values[k]; }));
  for (var t = 0; t < banned.length; t++) {
    var re = termRegex_(banned[t]);
    for (var v = 0; v < texts.length; v++) {
      if (re.test(texts[v])) { return 'banned term "' + banned[t] + '" found in this row'; }
    }
  }
  return '';
}

// ---------------------------------------------------------------------------
// DOCUMENT OPERATIONS
// ---------------------------------------------------------------------------

/** Copies the template into the output folder (required) and returns the new file ID. */
function copyTemplate_(templateId, name) {
  var folderId = getSetting_('OUTPUT_FOLDER_ID');
  if (!folderId) { throw new Error('OUTPUT_FOLDER_ID is not set.'); }
  var copy = DriveApp.getFileById(templateId).makeCopy(name, DriveApp.getFolderById(folderId));
  return copy.getId();
}

/** True if the file can be opened and is not in the bin. */
function isUsableFile_(id) {
  try {
    return !DriveApp.getFileById(id).isTrashed();
  } catch (err) {
    return false;
  }
}

/** Renames a failed copy so it is easy to find. Never trashes it. Best effort. */
function markCopyFailed_(docId, name) {
  try {
    DriveApp.getFileById(docId).setName(FAILED_PREFIX + name);
  } catch (err) {
    Logger.log('Could not rename the failed copy ' + docId + ': ' + err);
  }
}

/**
 * One atomic batchUpdate: every placeholder replaced, or none. Documents: all
 * tabs. Slides: the slides only (not layouts, masters or speaker notes), which
 * matches what verifyDocument_ checks.
 */
function fillDocument_(docId, type, tokens, values) {
  if (!tokens.length) { return; }
  var scope = type === 'slides' ? slideIds_(docId) : docTabIds_(docId);
  var requests = tokens.map(function (t) {
    var request = {
      containsText: { text: t.token, matchCase: true },
      replaceText: values[t.key]
    };
    if (type === 'slides') { request.pageObjectIds = scope; }
    else if (scope.length) { request.tabsCriteria = { tabIds: scope }; }
    return { replaceAllText: request };
  });
  if (type === 'slides') {
    Slides.Presentations.batchUpdate({ requests: requests }, docId);
  } else {
    Docs.Documents.batchUpdate({ requests: requests }, docId);
  }
}

/** IDs of every tab in a document, including nested tabs. */
function docTabIds_(docId) {
  var doc = Docs.Documents.get(docId, { includeTabsContent: true });
  var ids = [];
  (function walk(tabs) {
    (tabs || []).forEach(function (tab) {
      if (tab.tabProperties && tab.tabProperties.tabId) { ids.push(tab.tabProperties.tabId); }
      walk(tab.childTabs);
    });
  })(doc.tabs);
  return ids;
}

/** Object IDs of the slides in a presentation (not layouts or masters). */
function slideIds_(docId) {
  var pres = Slides.Presentations.get(docId);
  return (pres.slides || []).map(function (sl) { return sl.objectId; });
}

/** Reads the template and returns its type and the placeholders it contains. */
function inspectTemplate_(templateId) {
  var file = DriveApp.getFileById(templateId);
  var mime = file.getMimeType();
  var type = mime === SLIDES_MIME ? 'slides' : (mime === DOC_MIME ? 'doc' : '');
  if (!type) { throw new Error('The template must be a Google Doc or Google Slides file.'); }
  var text = documentText_(templateId, type);
  var tokens = findTokens_(text);
  if (!tokens.length) { throw new Error('The template contains no ' + CONFIG.PLACEHOLDER_OPEN + 'placeholder' + CONFIG.PLACEHOLDER_CLOSE + ' tokens.'); }
  return { type: type, tokens: tokens, keys: tokens.map(function (t) { return t.key; }) };
}

/** True when a copy still contains every placeholder of the template, i.e. it has not been filled. */
function hasAllPlaceholders_(docId, template) {
  try {
    var present = verifyDocument_(docId, template.type);
    return template.tokens.every(function (t) { return present.indexOf(t.token) !== -1; });
  } catch (err) {
    return false;
  }
}

/** After filling, returns any placeholder tokens that remain (empty array = clean). */
function verifyDocument_(docId, type) {
  return findTokens_(documentText_(docId, type)).map(function (t) { return t.token; });
}

/**
 * Whole-document text via the REST representation, with text runs joined so split
 * tokens are found. Documents: every tab (and child tab), with headers, footers and
 * footnotes. Slides: the page elements of the slides only, not layouts, masters or notes.
 */
function documentText_(docId, type) {
  var blocks = [];
  if (type === 'slides') {
    (Slides.Presentations.get(docId).slides || []).forEach(function (slide) {
      collectText_({ pageElements: slide.pageElements || [] }, blocks);
    });
  } else {
    collectText_(Docs.Documents.get(docId, { includeTabsContent: true }), blocks);
  }
  return blocks.join('\n');
}

/** Walks the API JSON. Each paragraph or text body is joined into one string. */
function collectText_(node, blocks) {
  if (!node || typeof node !== 'object') { return; }
  var runs = node.elements || node.textElements;
  if (Array.isArray(runs) && runs.some(function (e) { return e && e.textRun; })) {
    blocks.push(runs.map(function (e) { return e && e.textRun ? e.textRun.content : ''; }).join(''));
  }
  Object.keys(node).forEach(function (k) {
    var child = node[k];
    if (Array.isArray(child)) { child.forEach(function (c) { collectText_(c, blocks); }); }
    else if (child && typeof child === 'object') { collectText_(child, blocks); }
  });
}

/** Finds unique tokens such as {{client}}. key is the trimmed lower-case name. */
function findTokens_(text) {
  var open = escapeRegex_(CONFIG.PLACEHOLDER_OPEN);
  var close = escapeRegex_(CONFIG.PLACEHOLDER_CLOSE);
  var re = new RegExp(open + '([^{}\\n]+?)' + close, 'g');
  var seen = {};
  var out = [];
  var m;
  while ((m = re.exec(text)) !== null) {
    if (!seen[m[0]]) {
      seen[m[0]] = true;
      out.push({ token: m[0], key: m[1].trim().toLowerCase() });
    }
  }
  return out;
}

// ---------------------------------------------------------------------------
// SHEET HELPERS
// ---------------------------------------------------------------------------

/**
 * Reads the Rows tab. Returns { sheet, col, data } where col maps lower-case
 * header to zero-based index and each data row has get(name) and rowNumber.
 */
function readRows_() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.TAB_ROWS);
  if (!sheet) { throw new Error('Missing tab "Rows". Run setupFactory().'); }
  var lastRow = sheet.getLastRow();
  var lastCol = sheet.getLastColumn();
  if (lastRow < 1 || lastCol < 1) { throw new Error('The Rows tab is empty. Run setupFactory().'); }
  var headers = sheet.getRange(1, 1, 1, lastCol).getValues()[0].map(function (h) { return String(h).trim().toLowerCase(); });
  CONTROL_COLUMNS.forEach(function (c) {
    if (headers.indexOf(c) === -1) { throw new Error('Missing control column "' + c + '". Run setupFactory().'); }
  });
  var col = {};
  headers.forEach(function (h, i) { if (h) { col[h] = i; } });
  var data = [];
  if (lastRow >= 2) {
    var display = sheet.getRange(2, 1, lastRow - 1, lastCol).getDisplayValues(); // what the owner sees is what is inserted
    display.forEach(function (values, i) {
      if (values.every(function (v) { return v === ''; })) { return; } // fully blank row
      data.push({
        rowNumber: i + 2,
        values: values,
        get: function (name) { return values[col[name]]; }
      });
    });
  }
  return { sheet: sheet, col: col, data: data };
}

/** The value for each placeholder key from this row, trimmed. */
function placeholderValues_(row, keys) {
  var out = {};
  keys.forEach(function (k) { out[k] = String(row.get(k) === undefined ? '' : row.get(k)).trim(); });
  return out;
}

/** Document name from doc_name, else NAME_PATTERN. Characters Drive dislikes are removed. */
function buildName_(row, table, keys) {
  var explicit = String(row.get('doc_name') || '').trim();
  var name = explicit;
  if (!name) {
    name = CONFIG.NAME_PATTERN.replace(/\{\{\s*([^{}]+?)\s*\}\}/g, function (all, key) {
      key = key.toLowerCase();
      if (key === 'row') { return String(row.rowNumber); }
      return table.col[key] !== undefined ? String(row.get(key) || '').trim() : '';
    });
  }
  name = name.replace(/[\\\/:*?"<>|]+/g, ' ').replace(/\s+/g, ' ').trim();
  return name || ('Document row ' + row.rowNumber);
}

/** Writes control cells for one row, then flushes so a crash loses at most this row. */
function setControl_(table, row, updates) {
  Object.keys(updates).forEach(function (name) {
    table.sheet.getRange(row.rowNumber, table.col[name] + 1).setValue(updates[name]);
    row.values[table.col[name]] = String(updates[name]);
  });
  SpreadsheetApp.flush();
}

function readBannedTerms_() {
  var terms = CONFIG.BANNED_TERMS.slice();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.TAB_BANNED);
  if (sheet && sheet.getLastRow() >= 2) {
    sheet.getRange(2, 1, sheet.getLastRow() - 1, 1).getValues().forEach(function (r) {
      var t = String(r[0]).trim();
      if (t) { terms.push(t); }
    });
  }
  return terms;
}

/** Appends a report line to the buffer and writes the buffer to the Report tab. */
function report_(rowNumber, name, action, docId, docUrl, detail, attempt) {
  REPORT_BUFFER_.push([new Date(), RUN_ID_, rowNumber, name, action, docId, docUrl, detail, attempt]);
  Logger.log(action + ' row ' + rowNumber + ': ' + detail);
}

function flushReport_() {
  if (!REPORT_BUFFER_.length) { return; }
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.TAB_REPORT);
    if (!sheet) { return; }
    sheet.getRange(sheet.getLastRow() + 1, 1, REPORT_BUFFER_.length, REPORT_HEADERS.length).setValues(REPORT_BUFFER_);
  } catch (err) {
    Logger.log('Could not write the Report tab: ' + err);
  }
  REPORT_BUFFER_ = [];
}

// ---------------------------------------------------------------------------
// LOCK, TRIGGERS, SETTINGS
// ---------------------------------------------------------------------------

/** Holds the script lock for the run, always writes the report, never lets two runs overlap. */
function runWithLock_(name, fn) {
  RUN_ID_ = name + ' ' + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd HH:mm:ss');
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(CONFIG.LOCK_WAIT_MS)) {
    Logger.log(name + ': another run holds the lock. Nothing done.');
    return;
  }
  try {
    fn();
  } catch (err) {
    report_('-', '', 'run-error', '', '', String(err && err.message ? err.message : err), '');
    Logger.log(name + ' failed: ' + String(err && err.message ? err.message : err));
    throw err; // rethrown so a failed trigger run shows as failed; the report is still flushed below
  } finally {
    flushReport_();
    lock.releaseLock();
  }
}

function deleteContinuationTriggers_() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === CONTINUE_HANDLER) { ScriptApp.deleteTrigger(t); }
  });
  PropertiesService.getScriptProperties().deleteProperty('CONTINUATION_TRIGGER_ID');
}

/** Script Property first, CONFIG fallback. */
function getSetting_(name) {
  var value = PropertiesService.getScriptProperties().getProperty(name);
  return value ? value.trim() : String(CONFIG[name] || '').trim();
}

// ---------------------------------------------------------------------------
// SMALL UTILITIES
// ---------------------------------------------------------------------------

function termRegex_(term) {
  return new RegExp('(^|[^a-z0-9])' + escapeRegex_(term.toLowerCase()) + '([^a-z0-9]|$)', 'i');
}

function escapeRegex_(s) { return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
function truncate_(s, n) { s = String(s || ''); return s.length > n ? s.slice(0, n - 1) + '…' : s; }
