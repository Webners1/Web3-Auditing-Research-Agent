#!/usr/bin/env node
/**
 * web3-sales-agent - Stage-1 Scanner Wrapper
 *
 * The canonical lead finder lives in ../career-ops-source/scan.mjs.
 * This wrapper exists so any legacy `node scripts/scan.mjs` usage still
 * flows through the required three-agent order.
 */

import { spawnSync } from 'child_process';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const scannerPath = resolve(__dirname, '../../career-ops-source/scan.mjs');

console.log('\nweb3-sales-agent scan wrapper');
console.log('Forwarding to stage 1: ../career-ops-source/scan.mjs');
console.log('Stage 2 must run next before stage 3 can pitch.\n');

const result = spawnSync(process.execPath, [scannerPath, ...process.argv.slice(2)], {
  stdio: 'inherit',
});

if (typeof result.status === 'number') {
  process.exit(result.status);
}

process.exit(1);
