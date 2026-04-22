#!/usr/bin/env node
/**
 * web3-sales-agent — Tracker Merge Script
 * 
 * Merges TSV additions from batch/tracker-additions/ into data/leads.md.
 * This is the same pattern as career-ops' merge-tracker.mjs — write individual
 * TSV files per evaluation, then merge them all at once to avoid edit conflicts.
 * 
 * Usage: node scripts/merge-tracker.mjs
 */

import { readFileSync, writeFileSync, readdirSync, existsSync, unlinkSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const ADDITIONS_DIR = resolve(ROOT, 'batch/tracker-additions');
const LEADS_PATH = resolve(ROOT, 'data/leads.md');

const HEADER = '| # | Date | Protocol | Chain | TVL | Bucket | Score | Status | Pitch | Report | Notes |';
const DIVIDER = '|---|------|----------|-------|-----|--------|-------|--------|-------|--------|-------|';

function readLeads() {
  if (!existsSync(LEADS_PATH)) {
    return `# Lead Pipeline\n\n${HEADER}\n${DIVIDER}\n`;
  }
  return readFileSync(LEADS_PATH, 'utf8');
}

function parseLeadsTable(content) {
  const lines = content.split('\n');
  const rows = [];
  let inTable = false;
  
  for (const line of lines) {
    if (line.startsWith('| #')) { inTable = true; continue; }
    if (line.startsWith('|---')) continue;
    if (inTable && line.startsWith('|')) {
      const cols = line.split('|').filter((_, i) => i > 0 && i < 12).map(c => c.trim());
      if (cols[0] && /^\d+$/.test(cols[0])) {
        rows.push({
          num: parseInt(cols[0]),
          date: cols[1],
          protocol: cols[2],
          chain: cols[3],
          tvl: cols[4],
          bucket: cols[5],
          score: cols[6],
          status: cols[7],
          pitch: cols[8],
          report: cols[9],
          notes: cols[10] || ''
        });
      }
    } else if (inTable && !line.startsWith('|')) {
      inTable = false;
    }
  }
  return rows;
}

function parseTsv(content) {
  const line = content.trim().split('\n')[0];
  if (!line) return null;
  const cols = line.split('\t');
  if (cols.length < 10) return null;
  return {
    num: parseInt(cols[0]),
    date: cols[1],
    protocol: cols[2],
    chain: cols[3],
    tvl: cols[4],
    bucket: cols[5],
    score: cols[6],
    status: cols[7],
    pitch: cols[8],
    report: cols[9],
    notes: cols[10] || ''
  };
}

function rowToMarkdown(row) {
  return `| ${row.num} | ${row.date} | ${row.protocol} | ${row.chain} | ${row.tvl} | ${row.bucket} | ${row.score} | ${row.status} | ${row.pitch} | ${row.report} | ${row.notes} |`;
}

function main() {
  console.log('\n🔄 web3-sales-agent — Merge Tracker');
  console.log('═'.repeat(45));

  if (!existsSync(ADDITIONS_DIR)) {
    console.log('  No batch/tracker-additions/ directory found. Nothing to merge.');
    return;
  }

  const files = readdirSync(ADDITIONS_DIR).filter(f => f.endsWith('.tsv'));
  
  if (files.length === 0) {
    console.log('  ✅ No pending TSV additions. leads.md is up to date.');
    return;
  }

  console.log(`  Found ${files.length} TSV addition(s) to merge.`);

  // Parse existing leads
  const leadsContent = readLeads();
  const existingRows = parseLeadsTable(leadsContent);
  const existingProtocols = new Set(existingRows.map(r => r.protocol.toLowerCase()));

  let added = 0, skipped = 0, updated = 0;
  const newRows = [];
  const processedFiles = [];

  for (const file of files) {
    const filePath = resolve(ADDITIONS_DIR, file);
    const content = readFileSync(filePath, 'utf8');
    const row = parseTsv(content);

    if (!row) {
      console.log(`  ⚠️  Skipping malformed TSV: ${file}`);
      continue;
    }

    const protocolKey = row.protocol.toLowerCase();
    
    if (existingProtocols.has(protocolKey)) {
      // Update existing entry instead of duplicating
      const idx = existingRows.findIndex(r => r.protocol.toLowerCase() === protocolKey);
      if (idx !== -1) {
        existingRows[idx] = { ...existingRows[idx], ...row, num: existingRows[idx].num };
        updated++;
        console.log(`  🔄 Updated: ${row.protocol}`);
      } else {
        skipped++;
      }
    } else {
      // Re-number: use the max existing number + newRows already added
      row.num = (existingRows.length > 0 
        ? Math.max(...existingRows.map(r => r.num)) 
        : 0) + newRows.length + 1;
      newRows.push(row);
      existingProtocols.add(protocolKey);
      added++;
      console.log(`  ✅ Added: ${row.protocol} (score: ${row.score})`);
    }

    processedFiles.push(filePath);
  }

  // Rebuild leads.md
  const allRows = [...existingRows, ...newRows].sort((a, b) => b.num - a.num);
  
  const tableLines = allRows.map(rowToMarkdown);
  const newContent = `# Lead Pipeline\n\n${HEADER}\n${DIVIDER}\n${tableLines.join('\n')}\n`;
  
  writeFileSync(LEADS_PATH, newContent);

  // Delete processed TSV files
  processedFiles.forEach(f => unlinkSync(f));

  console.log('\n  Summary:');
  console.log(`    Added: ${added} new leads`);
  console.log(`    Updated: ${updated} existing leads`);
  console.log(`    Skipped: ${skipped}`);
  console.log(`    Total in pipeline: ${allRows.length}`);
  console.log('\n  ✅ data/leads.md updated. TSV additions cleared.');
  console.log('═'.repeat(45));
}

main();
