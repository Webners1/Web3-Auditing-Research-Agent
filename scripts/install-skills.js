#!/usr/bin/env node
/**
 * Auto-installs companion Claude Code skills required by the Web3 Auditing Agent.
 * Runs automatically on `npm install` via the postinstall hook.
 *
 * Skills installed:
 *   - pashov/skills       — x-ray protocol mapper + solidity-auditor (primary audit engine)
 *   - trailofbits/skills  — advanced static analysis and security workflows
 *   - auditmos/skills     — DeFi-specific audit heuristics
 */

const { execSync, spawnSync } = require('child_process');
const path = require('path');

const SKILLS = [
  {
    name: 'pashov/skills',
    url: 'https://github.com/pashov/skills',
    description: 'x-ray protocol mapper + solidity-auditor (primary audit engine)',
    required: true,
  },
  {
    name: 'trailofbits/skills',
    url: 'https://github.com/trailofbits/skills',
    description: 'Advanced static analysis and security workflows',
    required: false,
  },
  {
    name: 'auditmos/skills',
    url: 'https://github.com/auditmos/skills',
    description: 'DeFi-specific audit heuristics',
    required: false,
  },
];

function claudeAvailable() {
  const result = spawnSync('claude', ['--version'], { encoding: 'utf8', shell: true });
  return result.status === 0;
}

function installSkill(skill) {
  console.log(`  Installing ${skill.name} — ${skill.description}`);
  try {
    execSync(`claude install ${skill.url}`, {
      stdio: 'inherit',
      shell: true,
      timeout: 60000,
    });
    console.log(`  ✓ ${skill.name} installed\n`);
    return true;
  } catch (err) {
    const level = skill.required ? 'WARNING' : 'OPTIONAL';
    console.warn(`  [${level}] Could not install ${skill.name}: ${err.message}`);
    console.warn(`  Install manually: claude install ${skill.url}\n`);
    return false;
  }
}

function main() {
  console.log('\n──────────────────────────────────────────');
  console.log('  Web3 Auditing Agent — Skill Installer');
  console.log('──────────────────────────────────────────\n');

  if (!claudeAvailable()) {
    console.log('  Claude Code CLI not found in PATH.');
    console.log('  Install it from: https://claude.ai/code\n');
    console.log('  Then run companion skills manually:\n');
    SKILLS.forEach(s => console.log(`    claude install ${s.url}`));
    console.log('\n  The agent works without companion skills.');
    console.log('  They extend the audit engine with additional analysis layers.\n');
    return;
  }

  console.log('  Claude Code CLI found. Installing companion skills...\n');

  let installed = 0;
  for (const skill of SKILLS) {
    if (installSkill(skill)) installed++;
  }

  console.log('──────────────────────────────────────────');
  console.log(`  Done. ${installed}/${SKILLS.length} skills installed.`);
  console.log('\n  Start auditing:');
  console.log('    Open Claude Code in this directory');
  console.log('    Type: /start https://yourprotocol.xyz/');
  console.log('──────────────────────────────────────────\n');
}

main();
