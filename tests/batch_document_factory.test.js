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
