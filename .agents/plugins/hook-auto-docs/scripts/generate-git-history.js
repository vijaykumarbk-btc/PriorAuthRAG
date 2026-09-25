#!/usr/bin/env node

/**
 * Git History & Project Evolution Documentation Generator
 * Generates comprehensive historical documentation from the first commit to HEAD,
 * with dedicated per-commit folders for enhanced readability and navigation.
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function getProjectRoot() {
  if (process.env.CLAUDE_PROJECT_ROOT) {
    return process.env.CLAUDE_PROJECT_ROOT;
  }
  let dir = process.cwd();
  while (dir !== path.dirname(dir)) {
    if (fs.existsSync(path.join(dir, '.git')) || fs.existsSync(path.join(dir, '.agents'))) {
      return dir;
    }
    dir = path.dirname(dir);
  }
  return process.cwd();
}

const projectRoot = getProjectRoot();

// Determine output directory: default 'documentation'
const configPath = path.join(projectRoot, '.plugin-config', 'hook-auto-docs.json');
let outputDirName = 'documentation';
try {
  if (fs.existsSync(configPath)) {
    const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    if (config.outputDirectory) {
      outputDirName = config.outputDirectory;
    }
  }
} catch (e) {}

const outputDir = path.isAbsolute(outputDirName) ? outputDirName : path.join(projectRoot, outputDirName);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const commitsBaseDir = path.join(outputDir, 'commits');
if (!fs.existsSync(commitsBaseDir)) {
  fs.mkdirSync(commitsBaseDir, { recursive: true });
}

function runGit(cmd) {
  try {
    return execSync(cmd, { cwd: projectRoot, encoding: 'utf8', maxBuffer: 15 * 1024 * 1024 });
  } catch (error) {
    return '';
  }
}

function slugify(text) {
  const clean = (text || 'commit')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 45);
  return clean || 'commit';
}

function parseCommits() {
  const raw = runGit('git log --reverse --pretty=format:%H%x1f%h%x1f%an%x1f%ae%x1f%ad%x1f%s%x1f%b%x1e --date=iso');
  if (!raw.trim()) {
    return [];
  }

  const entries = raw.split('\x1e').filter(Boolean);
  const commits = [];

  for (let i = 0; i < entries.length; i++) {
    const [fullHash, hash, author, email, date, subject, body] = entries[i].split('\x1f');
    if (!hash) continue;

    const commitHash = hash.trim();
    const commitFullHash = fullHash.trim();
    const commitSubject = subject.trim();
    const slug = slugify(commitSubject);
    const folderName = `${String(i + 1).padStart(2, '0')}_${commitHash}_${slug}`;

    // Fetch changes for this commit
    const nameStatusRaw = runGit(`git diff-tree --root --no-commit-id --name-status -r ${commitFullHash}`).trim();
    const numstatRaw = runGit(`git diff-tree --root --no-commit-id --numstat -r ${commitFullHash}`).trim();

    const numstatMap = {};
    if (numstatRaw) {
      for (const line of numstatRaw.split('\n')) {
        if (!line.trim()) continue;
        const [added, deleted, filePath] = line.split('\t');
        if (filePath) {
          numstatMap[filePath.trim()] = { added: added.trim(), deleted: deleted.trim() };
        }
      }
    }

    const fileChanges = [];
    let addedCount = 0;
    let modifiedCount = 0;
    let deletedCount = 0;
    let renamedCount = 0;
    let totalLinesAdded = 0;
    let totalLinesDeleted = 0;

    if (nameStatusRaw) {
      for (const line of nameStatusRaw.split('\n')) {
        if (!line.trim()) continue;
        const parts = line.split('\t');
        const code = parts[0][0]; // A, M, D, R
        if (code === 'R') {
          renamedCount++;
          fileChanges.push({
            status: 'Renamed',
            oldPath: parts[1],
            path: parts[2],
            added: '-',
            deleted: '-'
          });
        } else {
          const filePath = parts[1];
          if (!filePath) continue;
          const status = code === 'A' ? 'Added' : code === 'D' ? 'Deleted' : 'Modified';
          if (code === 'A') addedCount++;
          else if (code === 'D') deletedCount++;
          else modifiedCount++;

          const stats = numstatMap[filePath] || { added: '-', deleted: '-' };
          if (stats.added !== '-' && !isNaN(parseInt(stats.added))) {
            totalLinesAdded += parseInt(stats.added);
          }
          if (stats.deleted !== '-' && !isNaN(parseInt(stats.deleted))) {
            totalLinesDeleted += parseInt(stats.deleted);
          }

          fileChanges.push({
            status,
            path: filePath,
            added: stats.added,
            deleted: stats.deleted
          });
        }
      }
    }

    commits.push({
      index: i + 1,
      folderName,
      fullHash: commitFullHash,
      hash: commitHash,
      author: author.trim(),
      email: email.trim(),
      date: date.trim(),
      subject: commitSubject,
      body: body ? body.trim() : '',
      fileChanges,
      stats: {
        totalFiles: fileChanges.length,
        addedCount,
        modifiedCount,
        deletedCount,
        renamedCount,
        totalLinesAdded,
        totalLinesDeleted
      }
    });
  }

  return commits;
}

function writeIndividualCommitDoc(commit, prevCommit, nextCommit) {
  const commitFolder = path.join(commitsBaseDir, commit.folderName);
  if (!fs.existsSync(commitFolder)) {
    fs.mkdirSync(commitFolder, { recursive: true });
  }

  let md = `# Commit ${commit.index}: ${commit.subject}\n\n`;

  // Navigation header
  md += `<nav>\n`;
  if (prevCommit) {
    md += `  <a href="../${prevCommit.folderName}/README.md">&larr; Previous Commit (${prevCommit.hash})</a> | \n`;
  }
  md += `  <a href="../README.md">All Commits Index</a>\n`;
  if (nextCommit) {
    md += ` | <a href="../${nextCommit.folderName}/README.md">Next Commit (${nextCommit.hash}) &rarr;</a>\n`;
  }
  md += `</nav>\n\n`;
  md += `---\n\n`;

  // Commit Metadata Table
  md += `## Metadata\n\n`;
  md += `| Attribute | Value |\n`;
  md += `| :--- | :--- |\n`;
  md += `| **Commit Index** | \`#${commit.index}\` |\n`;
  md += `| **Short Hash** | \`${commit.hash}\` |\n`;
  md += `| **Full Hash** | \`${commit.fullHash}\` |\n`;
  md += `| **Author** | ${commit.author} &lt;${commit.email}&gt; |\n`;
  md += `| **Date** | ${commit.date} |\n`;
  md += `| **Files Affected** | **${commit.stats.totalFiles}** |\n`;
  md += `| **Lines Added** | **+${commit.stats.totalLinesAdded}** |\n`;
  md += `| **Lines Deleted** | **-${commit.stats.totalLinesDeleted}** |\n\n`;

  if (commit.body) {
    md += `## Description / Commit Body\n\n`;
    md += `> ${commit.body.replace(/\n/g, '\n> ')}\n\n`;
  }

  md += `## Change Breakdown\n\n`;
  md += `- **Added files**: ${commit.stats.addedCount}\n`;
  md += `- **Modified files**: ${commit.stats.modifiedCount}\n`;
  md += `- **Deleted files**: ${commit.stats.deletedCount}\n`;
  if (commit.stats.renamedCount) {
    md += `- **Renamed files**: ${commit.stats.renamedCount}\n`;
  }
  md += `\n`;

  if (commit.fileChanges.length > 0) {
    md += `## Changed Files List\n\n`;
    md += `| Status | File Path | Lines (+/-) |\n`;
    md += `| :--- | :--- | :--- |\n`;

    commit.fileChanges.forEach(f => {
      let statusBadge = '🟡 Modified';
      if (f.status === 'Added') statusBadge = '🟢 Added';
      else if (f.status === 'Deleted') statusBadge = '🔴 Deleted';
      else if (f.status === 'Renamed') statusBadge = '🔄 Renamed';

      const linesDiff = (f.added !== '-' || f.deleted !== '-') ? `+${f.added} / -${f.deleted}` : '-';

      // Check if file currently exists in project root for clickable link
      // Relative path from documentation/commits/<folder>/README.md is ../../../
      const exists = fs.existsSync(path.join(projectRoot, f.path));
      const fileDisplay = exists ? `[${f.path}](../../../${f.path})` : `\`${f.path}\``;

      if (f.status === 'Renamed') {
        md += `| ${statusBadge} | \`${f.oldPath}\` &rarr; ${fileDisplay} | ${linesDiff} |\n`;
      } else {
        md += `| ${statusBadge} | ${fileDisplay} | ${linesDiff} |\n`;
      }
    });
    md += `\n`;
  }

  // Navigation footer
  md += `---\n\n`;
  md += `<nav>\n`;
  if (prevCommit) {
    md += `  <a href="../${prevCommit.folderName}/README.md">&larr; Previous Commit (${prevCommit.hash})</a> | \n`;
  }
  md += `  <a href="../README.md">All Commits Index</a>\n`;
  if (nextCommit) {
    md += ` | <a href="../${nextCommit.folderName}/README.md">Next Commit (${nextCommit.hash}) &rarr;</a>\n`;
  }
  md += `</nav>\n`;

  const commitFilePath = path.join(commitFolder, 'README.md');
  fs.writeFileSync(commitFilePath, md, 'utf8');
}

function writeCommitsIndexDoc(commits) {
  const now = new Date().toISOString().replace('T', ' ').slice(0, 19);
  const projectName = path.basename(projectRoot);

  let md = `# Commits Documentation Index\n\n`;
  md += `**Project**: \`${projectName}\`  \n`;
  md += `**Generated**: ${now}  \n`;
  md += `**Total Commits Documented**: ${commits.length}  \n`;
  if (commits.length > 0) {
    md += `**Timeline**: ${commits[0].date.slice(0, 10)} to ${commits[commits.length - 1].date.slice(0, 10)}  \n\n`;
  }

  md += `This folder organizes documentation for **each individual commit** into dedicated folders for easy readability and isolated inspection.\n\n`;

  md += `## All Commits (Chronological)\n\n`;
  md += `| # | Hash | Date | Commit Message | Files Changed | Detailed Documentation Folder |\n`;
  md += `| :-: | :--- | :--- | :--- | :-: | :--- |\n`;

  commits.forEach(c => {
    md += `| ${c.index} | \`${c.hash}\` | ${c.date.slice(0, 10)} | ${c.subject.replace(/\|/g, '\\|')} | ${c.stats.totalFiles} | [📂 ${c.folderName}/](./${c.folderName}/README.md) |\n`;
  });

  md += `\n---\n`;
  md += `<a href="../README.md">&larr; Back to Main Documentation Index</a>\n`;

  fs.writeFileSync(path.join(commitsBaseDir, 'README.md'), md, 'utf8');
}

function writeMasterGitHistoryDoc(commits) {
  const now = new Date().toISOString().replace('T', ' ').slice(0, 19);
  const projectName = path.basename(projectRoot);

  if (commits.length === 0) {
    fs.writeFileSync(path.join(outputDir, 'GIT_HISTORY.md'), `# Project Git History: ${projectName}\n\nNo commits found.`, 'utf8');
    return;
  }

  const firstCommit = commits[0];
  const lastCommit = commits[commits.length - 1];

  const authorCounts = {};
  commits.forEach(c => {
    authorCounts[c.author] = (authorCounts[c.author] || 0) + 1;
  });

  let md = `# Project Git History & Evolution Documentation\n\n`;
  md += `**Project**: \`${projectName}\`  \n`;
  md += `**Generated**: ${now}  \n`;
  md += `**Total Commits**: ${commits.length}  \n`;
  md += `**Timeline**: ${firstCommit.date.slice(0, 10)} to ${lastCommit.date.slice(0, 10)}  \n\n`;

  md += `> [!TIP]\n`;
  md += `> Each commit now has its own dedicated folder under [**\`documentation/commits/\`**](./commits/README.md) for modular browsing!\n\n`;

  md += `## Overview\n\n`;
  md += `| Metric | Details |\n`;
  md += `| :--- | :--- |\n`;
  md += `| **Initial Commit** | \`${firstCommit.hash}\` (${firstCommit.date.slice(0, 10)}) - *${firstCommit.subject}* |\n`;
  md += `| **Latest Commit (HEAD)** | \`${lastCommit.hash}\` (${lastCommit.date.slice(0, 10)}) - *${lastCommit.subject}* |\n`;
  md += `| **Total Commits** | ${commits.length} |\n`;
  md += `| **Contributors** | ${Object.entries(authorCounts).map(([author, count]) => `${author} (${count})`).join(', ')} |\n\n`;

  md += `## Timeline Summary & Commit Folders\n\n`;
  md += `| # | Hash | Date | Author | Commit Message | Files Changed | Dedicated Commit Folder |\n`;
  md += `| :-: | :--- | :--- | :--- | :--- | :-: | :--- |\n`;

  commits.forEach(c => {
    md += `| ${c.index} | \`${c.hash}\` | ${c.date.slice(0, 10)} | ${c.author} | [${c.subject.replace(/\|/g, '\\|')}](#commit-${c.hash}) | ${c.stats.totalFiles} | [📂 ${c.folderName}/](./commits/${c.folderName}/README.md) |\n`;
  });
  md += `\n---\n\n`;

  md += `## Detailed Commit History (Chronological)\n\n`;

  commits.forEach(c => {
    md += `### Commit ${c.index}: \`${c.hash}\` - ${c.subject}\n\n`;
    md += `<a id="commit-${c.hash}"></a>\n\n`;
    md += `- **Date**: ${c.date}\n`;
    md += `- **Author**: ${c.author} &lt;${c.email}&gt;\n`;
    md += `- **Full Hash**: \`${c.fullHash}\`\n`;
    md += `- **Folder**: [**\`commits/${c.folderName}/\`**](./commits/${c.folderName}/README.md)\n`;
    md += `- **Change Summary**: ${c.stats.totalFiles} file(s) affected (${c.stats.addedCount} added, ${c.stats.modifiedCount} modified, ${c.stats.deletedCount} deleted${c.stats.renamedCount ? `, ${c.stats.renamedCount} renamed` : ''})\n\n`;

    if (c.body) {
      md += `> ${c.body.replace(/\n/g, '\n> ')}\n\n`;
    }

    if (c.fileChanges.length > 0) {
      const isLargeList = c.fileChanges.length > 10;

      if (isLargeList) {
        md += `<details>\n<summary><b>View all ${c.fileChanges.length} changed files</b> (Click to expand)</summary>\n\n`;
      }

      md += `| Status | File Path | Lines (+/-) |\n`;
      md += `| :--- | :--- | :--- |\n`;

      c.fileChanges.forEach(f => {
        let statusBadge = '🟡 Modified';
        if (f.status === 'Added') statusBadge = '🟢 Added';
        else if (f.status === 'Deleted') statusBadge = '🔴 Deleted';
        else if (f.status === 'Renamed') statusBadge = '🔄 Renamed';

        const linesDiff = (f.added !== '-' || f.deleted !== '-') ? `+${f.added} / -${f.deleted}` : '-';
        const exists = fs.existsSync(path.join(projectRoot, f.path));
        const fileDisplay = exists ? `[${f.path}](../${f.path})` : `\`${f.path}\``;

        if (f.status === 'Renamed') {
          md += `| ${statusBadge} | \`${f.oldPath}\` &rarr; ${fileDisplay} | ${linesDiff} |\n`;
        } else {
          md += `| ${statusBadge} | ${fileDisplay} | ${linesDiff} |\n`;
        }
      });

      if (isLargeList) {
        md += `\n</details>\n`;
      }
      md += `\n`;
    }

    md += `---\n\n`;
  });

  fs.writeFileSync(path.join(outputDir, 'GIT_HISTORY.md'), md, 'utf8');
}

function main() {
  const commits = parseCommits();

  // 1. Generate individual documentation folders for each commit
  for (let i = 0; i < commits.length; i++) {
    const prevCommit = i > 0 ? commits[i - 1] : null;
    const nextCommit = i < commits.length - 1 ? commits[i + 1] : null;
    writeIndividualCommitDoc(commits[i], prevCommit, nextCommit);
  }

  // 2. Generate documentation/commits/README.md
  writeCommitsIndexDoc(commits);

  // 3. Generate documentation/GIT_HISTORY.md
  writeMasterGitHistoryDoc(commits);

  console.log(JSON.stringify({
    success: true,
    message: `Generated documentation folders for all ${commits.length} commits in ${commitsBaseDir}`,
    commitsCount: commits.length,
    commitsDir: commitsBaseDir
  }));
}

main();
