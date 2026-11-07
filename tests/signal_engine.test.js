const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const script = readFileSync(resolve(__dirname,
  '../packs/automations/scripts/signal-engine/Code.gs'), 'utf8');

function digestHarness({ dry = false, failSend = false, failFlush = false } = {}) {
  const properties = new Map();
  const sent = [];
  const messages = [];
  const context = vm.createContext({});
  vm.runInContext(script, context);

  const cols = context.indexMap_(context.QUEUE_HEADERS);
  const row = Array(context.QUEUE_HEADERS.length).fill('');
  row[cols.ItemKey] = 'fixture-item';
  row[cols.Status] = 'queued';
  row[cols.FinalScore] = 999;
  Object.assign(context, {
    withLock_: (_name, run) => run(),
    ensureSheets_: () => {},
    getSheet_: () => ({}),
    readTable_: () => ({ rows: [row.slice()] }),
    isDryRun_: () => dry,
    buildDigest_: () => ({ text: 'Fixture', html: '<p>Fixture</p>' }),
    resolveDigestTo_: () => 'operator@example.invalid',
    log_: (_level, message) => messages.push(message),
    PropertiesService: { getScriptProperties: () => ({
      getProperty: (key) => properties.get(key),
      setProperty: (key, value) => properties.set(key, value),
      deleteProperty: (key) => properties.delete(key),
    }) },
    Utilities: { formatDate: () => '2026-11-07', getUuid: () => 'fixture-attempt' },
    Session: { getScriptTimeZone: () => 'UTC' },
    MailApp: { sendEmail: (message) => {
      assert.ok(properties.has('PENDING_DIGEST'));
      sent.push(message);
      if (failSend) throw new Error('delivery outcome unknown');
    } },
    SpreadsheetApp: { flush: () => {
      assert.ok(properties.has('PENDING_DIGEST'));
      if (failFlush) throw new Error('queue readback failed');
    } },
    writeColumns_: (_sheet, rows) => {
      assert.equal(rows[0][cols.Status], 'digested');
    },
  });
  return { context, properties, sent, messages };
}

test('a send with an uncertain outcome holds subsequent and forced sends', () => {
  const { context, properties, sent, messages } = digestHarness({ failSend: true });
  assert.throws(() => context.sendDigest(), /delivery outcome unknown/);
  assert.deepEqual(JSON.parse(properties.get('PENDING_DIGEST')).itemKeys, ['fixture-item']);
  assert.match(sent[0].body, /Digest reference: fixture-attempt/);
  context.sendDigest();
  context.sendDigestAgain();
  assert.equal(sent.length, 1);
  assert.ok(messages.some((message) => message.includes('needs reconciliation')));
});

test('a failed queue flush leaves the send reserved', () => {
  const { context, properties, sent } = digestHarness({ failFlush: true });
  assert.throws(() => context.sendDigest(), /queue readback failed/);
  assert.equal(properties.get('LAST_DIGEST_DATE'), '2026-11-07');
  assert.ok(properties.has('PENDING_DIGEST'));
  context.sendDigestAgain();
  assert.equal(sent.length, 1);
});

test('success clears the reservation after recording the digest', () => {
  const { context, properties, sent } = digestHarness();
  context.sendDigest();
  assert.equal(properties.get('LAST_DIGEST_DATE'), '2026-11-07');
  assert.equal(properties.has('PENDING_DIGEST'), false);
  context.sendDigest();
  assert.equal(sent.length, 1);
});

test('dry run leaves the queue and mail alone', () => {
  const { context, properties, sent } = digestHarness({ dry: true });
  context.sendDigest();
  assert.equal(properties.size, 0);
  assert.equal(sent.length, 0);
});
