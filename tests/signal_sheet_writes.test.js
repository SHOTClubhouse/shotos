const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { resolve } = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const script = readFileSync(resolve(__dirname,
  '../packs/automations/scripts/signal-engine/Code.gs'), 'utf8');

function recordingSheet(existing) {
  const writes = [];
  const sheet = {
    getLastRow: () => existing.length + 1,
    getRange: (...range) => ({
      getValues: () => existing,
      setValues: (values) => writes.push({ range, values }),
      clearContent: () => assert.fail('Retention must not clear rows in a separate call'),
    }),
  };
  return { sheet, writes };
}

test('queue and log appends pass formula-shaped data as text', () => {
  const context = vm.createContext({});
  vm.runInContext(script, context);
  const { sheet, writes } = recordingSheet([]);
  context.appendRows_(sheet, [['=1+2', "'quoted", 'ordinary', 7]]);
  assert.deepEqual(writes[0].range, [2, 1, 1, 4]);
  assert.deepEqual(Array.from(writes[0].values[0]), ["'=1+2", "''quoted", 'ordinary', 7]);
});

test('retention keeps literal data and blanks the tail in one write', () => {
  const context = vm.createContext({});
  vm.runInContext(script, context);
  const recent = new Date().toISOString();
  const { sheet, writes } = recordingSheet([[recent, '=1+2'], ['2000-01-01', 'expired']]);
  assert.equal(context.pruneOldRows_(sheet, 2, 0, 30), 1);
  assert.equal(writes.length, 1);
  assert.deepEqual(writes[0].range, [2, 1, 2, 2]);
  assert.deepEqual(Array.from(writes[0].values, (row) => Array.from(row)), [[recent, "'=1+2"], ['', '']]);
});
