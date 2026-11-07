const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const script = readFileSync(resolve(__dirname,
  '../packs/automations/scripts/batch-document-factory/Code.gs'), 'utf8');

function batchWithClient(client, mode) {
  const updates = [];
  const reports = [];
  const row = { rowNumber: 2, get: (key) => ({ client, city: 'York' })[key] || '' };
  const context = vm.createContext({});
  vm.runInContext(script, context);
  Object.assign(context, {
    getSetting_: () => 'fixture-id',
    inspectTemplate_: () => ({
      keys: ['client', 'city'],
      tokens: [{ key: 'client', token: '{{client}}' }, { key: 'city', token: '{{city}}' }],
    }),
    readRows_: () => ({ data: [row], col: { client: 0, city: 1 } }),
    readBannedTerms_: () => [],
    DriveApp: { getFolderById: () => ({}) },
    report_: (_row, _name, action, _id, _url, detail) => reports.push({ action, detail }),
    setControl_: (_table, _row, change) => updates.push(change),
    copyTemplate_: () => assert.fail('This fixture should not create a document'),
  });
  context.processRows_({ mode, limit: 3 });
  return { reports, updates };
}

test('dry run reports token-shaped data without writing control cells', () => {
  const { reports, updates } = batchWithClient('Example {{city}}', 'dry');
  assert.deepEqual(updates, []);
  assert.ok(reports.some(({ action, detail }) =>
    action === 'blocked' && detail === 'placeholder text in values for: client'));
  assert.ok(!reports.some(({ action }) => action === 'would-create'));
});

test('live preflight blocks token-shaped data before making a copy', () => {
  const { updates } = batchWithClient('Example {{city}}', 'live');
  assert.equal(updates.length, 1);
  assert.equal(updates[0].status, 'blocked');
  assert.equal(updates[0].last_message, 'blocked: placeholder text in values for: client');
});

test('plain data can pass dry run', () => {
  const { reports } = batchWithClient('Example {Community Centre}', 'dry');
  assert.ok(reports.some(({ action }) => action === 'would-create'));
});

test('DONE is written only after the document receipt flushes', () => {
  const events = [];
  const context = vm.createContext({
    SpreadsheetApp: { flush: () => events.push('flush') },
  });
  vm.runInContext(script, context);
  const table = {
    col: { done: 0, doc_url: 1, copy_state: 2 },
    sheet: { getRange: (_row, col) => ({ setValue: (value) => events.push([col, value]) }) },
  };
  context.setControl_(table, { rowNumber: 2, values: [] },
    { done: 'DONE', doc_url: 'fixture-link', copy_state: 'complete' });
  assert.deepEqual(events, [[2, 'fixture-link'], [3, 'complete'], 'flush', [1, 'DONE'], 'flush']);
});

test('a receipt write failure leaves a verified copy intact and stops the batch', () => {
  const context = vm.createContext({});
  vm.runInContext(script, context);
  const row = { rowNumber: 2, get: (key) => (key === 'client' ? 'Workshop' : '') };
  const reports = [];
  let writes = 0;
  Object.assign(context, {
    getSetting_: () => 'fixture-id',
    inspectTemplate_: () => ({ keys: ['client'], tokens: [{ key: 'client', token: '{{client}}' }] }),
    readRows_: () => ({ data: [row], col: { client: 0 } }),
    readBannedTerms_: () => [],
    copyTemplate_: () => 'verified-fixture',
    fillDocument_: () => {},
    verifyDocument_: () => [],
    markCopyFailed_: () => assert.fail('A verified document must be left intact'),
    DriveApp: {
      getFolderById: () => ({}),
      getFileById: () => ({ getUrl: () => 'fixture-link' }),
    },
    report_: (_row, _name, action, id) => reports.push({ action, id }),
    setControl_: (_table, _row, updates) => {
      writes++;
      if (updates.done) throw new Error('receipt write interrupted');
    },
  });
  assert.throws(() => context.processRows_({ mode: 'live', limit: 3 }), /receipt write interrupted/);
  assert.equal(writes, 2);
  assert.deepEqual(reports, [{ action: 'receipt-error', id: 'verified-fixture' }]);
});

test('the report writes formula-shaped document names and details as text', () => {
  const context = vm.createContext({});
  vm.runInContext(script, context);
  const rows = [];
  Object.assign(context, {
    Logger: { log: () => {} },
    SpreadsheetApp: { getActiveSpreadsheet: () => ({
      getSheetByName: () => ({
        getLastRow: () => 1,
        getRange: () => ({ setValues: (values) => rows.push(...values) }),
      }),
    }) },
  });
  context.report_(2, '=1+2', 'blocked', '', '', '=3+4', 0);
  context.flushReport_();
  assert.equal(rows[0][3], "'=1+2");
  assert.equal(rows[0][4], 'blocked');
  assert.equal(rows[0][7], "'=3+4");
  assert.equal(rows[0][8], 0);
});

test('retryFailed processes only unfinished errors', () => {
  const context = vm.createContext({});
  vm.runInContext(script, context);
  const pending = { client: 'Pending' };
  const failed = { client: 'Failed', status: 'error', attempts: 3 };
  const done = { client: 'Done', status: 'error', done: 'DONE' };
  const rows = [pending, failed, done].map((fields, index) => ({
    rowNumber: index + 2,
    get: (key) => fields[key] ?? '',
  }));
  const reset = [];
  const rendered = [];
  Object.assign(context, {
    runWithLock_: (_name, run) => run(),
    getSetting_: () => 'fixture-id',
    inspectTemplate_: () => ({ keys: ['client'], tokens: [{ key: 'client', token: '{{client}}' }] }),
    readRows_: () => ({
      data: rows,
      col: { client: 0, attempts: 1 },
      sheet: { getRange: (row, col) => ({ setValue: (value) => {
        reset.push([row, col, value]);
        failed.attempts = value;
      } }) },
    }),
    SpreadsheetApp: { flush: () => {} },
    readBannedTerms_: () => [],
    deleteContinuationTriggers_: () => assert.fail('A retry must not alter the batch continuation'),
    copyTemplate_: () => 'verified-fixture',
    fillDocument_: (_id, _type, _tokens, values) => rendered.push(values.client),
    verifyDocument_: () => [],
    DriveApp: {
      getFolderById: () => ({}),
      getFileById: () => ({ getUrl: () => 'fixture-link' }),
    },
    report_: () => {},
    setControl_: () => {},
  });
  context.retryFailed();
  assert.deepEqual(reset, [[3, 2, 0]]);
  assert.deepEqual(rendered, ['Failed']);
});
