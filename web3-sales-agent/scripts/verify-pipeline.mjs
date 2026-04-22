#!/usr/bin/env node
/**
 * web3-sales-agent - Three-Agent Pipeline Verifier
 *
 * Checks that:
 * - stage-1 inbox files exist
 * - stage-2 handoff files are present and well-formed
 * - linked stage-2 report paths resolve
 * - stage-3 tracker state is sane
 *
 * Usage: node scripts/verify-pipeline.mjs
 */

import { readFileSync, readdirSync, existsSync, statSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const HANDOFF_DIR = resolve(ROOT, 'data/research-handoffs');

const CANONICAL_STATUSES = new Set([
  'Research Pending',
  'Research Complete',
  'Evaluated',
  'Pitched',
  'Responded',
  'Call Scheduled',
  'Proposal Sent',
  'Negotiating',
  'Closed Won',
  'Closed Lost',
  'Not a Fit',
  'Watch',
]);

const REQUIRED_HANDOFF_FIELDS = [
  'Protocol',
  'Slug',
  'Chain',
  'Bucket',
  'Lead Source',
  'Report Type',
  'Report Path',
  'Status',
  'Recommended Service',
  'Primary Pain',
  'Pitch Hook',
  'Proof Points To Use',
  'Cautions',
];

let errors = 0;
let warnings = 0;

function err(msg) {
  console.log(`  ERROR: ${msg}`);
  errors++;
}

function warn(msg) {
  console.log(`  WARN: ${msg}`);
  warnings++;
}

function ok(msg) {
  console.log(`  OK: ${msg}`);
}

function parseHandoff(content) {
  const fields = {};
  for (const key of REQUIRED_HANDOFF_FIELDS) {
    const match = content.match(new RegExp(`\\*\\*${key}:\\*\\*\\s*(.+)`));
    if (match) fields[key] = match[1].trim();
  }
  return fields;
}

function main() {
  console.log('\nThree-Agent Pipeline Check');
  console.log('='.repeat(50));

  console.log('\n[1] Required files');
  const required = [
    'data/leads.md',
    'data/pipeline.md',
    'templates/research-handoff-template.md',
  ];

  for (const relPath of required) {
    const fullPath = resolve(ROOT, relPath);
    if (existsSync(fullPath)) ok(relPath);
    else warn(`${relPath} missing`);
  }

  const stageOneConfig = resolve(ROOT, '../career-ops-source/portals.yml');
  if (existsSync(stageOneConfig)) ok('../career-ops-source/portals.yml');
  else warn('../career-ops-source/portals.yml missing');

  console.log('\n[2] Tracker integrity');
  const leadsPath = resolve(ROOT, 'data/leads.md');
  if (!existsSync(leadsPath)) {
    warn('data/leads.md missing - skipping tracker checks');
  } else {
    const content = readFileSync(leadsPath, 'utf8');
    const rows = [];
    const protocols = new Set();

    content.split('\n').forEach(line => {
      if (!line.startsWith('|') || line.startsWith('| #') || line.startsWith('|---')) return;
      const cols = line.split('|').filter((_, i) => i > 0 && i < 12).map(c => c.trim());
      if (!cols[0] || !/^\d+$/.test(cols[0])) return;
      rows.push({ protocol: cols[2], status: cols[7] });
    });

    if (rows.length === 0) {
      ok('leads.md exists (empty)');
    } else {
      ok(`${rows.length} tracked leads`);
      for (const row of rows) {
        const key = row.protocol.toLowerCase();
        if (protocols.has(key)) err(`duplicate protocol in leads.md: ${row.protocol}`);
        protocols.add(key);
        if (row.status && !CANONICAL_STATUSES.has(row.status)) {
          warn(`non-canonical status "${row.status}" for "${row.protocol}"`);
        }
      }
    }
  }

  console.log('\n[3] Research handoffs');
  if (!existsSync(HANDOFF_DIR)) {
    warn('data/research-handoffs/ missing');
  } else if (!statSync(HANDOFF_DIR).isDirectory()) {
    err('data/research-handoffs exists but is not a directory');
  } else {
    const handoffFiles = readdirSync(HANDOFF_DIR)
      .filter(name => name.endsWith('.md'))
      .filter(name => name !== '.gitkeep');

    ok(`${handoffFiles.length} handoff file(s) found`);

    for (const file of handoffFiles) {
      const fullPath = resolve(HANDOFF_DIR, file);
      const content = readFileSync(fullPath, 'utf8');
      const fields = parseHandoff(content);

      for (const key of REQUIRED_HANDOFF_FIELDS) {
        if (!fields[key]) err(`${file} missing field: ${key}`);
      }

      if (fields.Status && fields.Status !== 'Research Complete') {
        warn(`${file} has non-ready status: ${fields.Status}`);
      }

      if (fields['Report Path']) {
        const reportPath = resolve(ROOT, fields['Report Path']);
        if (!existsSync(reportPath)) err(`${file} points to missing report: ${fields['Report Path']}`);
      }
    }
  }

  console.log('\n[4] Reports vs tracker');
  const reportsDir = resolve(ROOT, 'reports');
  if (!existsSync(reportsDir)) {
    ok('No stage-3 reports yet');
  } else {
    const reportFiles = readdirSync(reportsDir).filter(name => name.endsWith('.md') && /^\d+/.test(name));
    ok(`${reportFiles.length} stage-3 report(s) found`);

    const leadsContent = existsSync(leadsPath) ? readFileSync(leadsPath, 'utf8') : '';
    for (const file of reportFiles) {
      const match = file.match(/^(\d+)-/);
      if (match && !leadsContent.includes(`[${match[1]}]`)) {
        warn(`report ${file} has no matching leads.md entry - merge tracker additions`);
      }
    }
  }

  console.log('\n[5] Pending tracker additions');
  const additionsDir = resolve(ROOT, 'batch/tracker-additions');
  if (!existsSync(additionsDir)) {
    ok('No batch/tracker-additions/ directory yet');
  } else {
    const tsvFiles = readdirSync(additionsDir).filter(name => name.endsWith('.tsv'));
    if (tsvFiles.length === 0) ok('No pending TSV additions');
    else warn(`${tsvFiles.length} unmerged TSV addition(s) - run node scripts/merge-tracker.mjs`);
  }

  console.log('\n[6] Shared inbox');
  const pipelinePath = resolve(ROOT, 'data/pipeline.md');
  if (!existsSync(pipelinePath)) {
    warn('data/pipeline.md missing');
  } else {
    const pending = [...readFileSync(pipelinePath, 'utf8').matchAll(/^- \[ \] /gm)].length;
    ok(`${pending} pending raw lead(s) in inbox`);
  }

  console.log('\n' + '='.repeat(50));
  if (errors === 0 && warnings === 0) {
    console.log('Pipeline is clean. Three-agent flow is wired correctly.');
  } else {
    console.log(`Result: ${errors} error(s), ${warnings} warning(s)`);
  }
  console.log('='.repeat(50) + '\n');

  process.exit(errors > 0 ? 1 : 0);
}

main();
