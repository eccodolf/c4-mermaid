// Optional maintainer test; the offline viewer itself does not require Node.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const context = vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(root, 'assets/offline/airgap-guard.js'), 'utf8'), context);
const guard = context.assertAirGapSource;
for (const legend of ['', '   ', '\n\t', null]) assert.throws(() => context.assertLegend(legend));
assert.doesNotThrow(() => context.assertLegend('Blue = system. Arrow = directed call.'));
for (const name of fs.readdirSync(path.join(root, 'assets/templates')).filter(name => name.endsWith('.mmd'))) {
  assert.doesNotThrow(() => guard(fs.readFileSync(path.join(root, 'assets/templates', name), 'utf8')), name);
}
for (const input of [
  'flowchart LR\nA@{ img: "https://invalid.example/icon.png" }',
  'flowchart LR\nclick A "https://invalid.example"',
  'flowchart LR\nA@{ img: "local.png" }',
  'flowchart LR\nA["<img src=\"remote.png\">"]',
  'flowchart LR\nA["//invalid.example/icon"]',
  '!include local-file',
  'flowchart LR\nclassDef A fill:url(remote.svg)',
  'flowchart LR\nA["data:image/svg+xml,resource"]',
]) assert.throws(() => guard(input), /Air-gap policy/);
console.log('Air-gap source guard passed: nine examples and eight rejected resource inputs.');
