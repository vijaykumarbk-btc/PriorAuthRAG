#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

function getProjectRoot(hookInput) {
  if (process.env.CLAUDE_PROJECT_ROOT) {
    return process.env.CLAUDE_PROJECT_ROOT;
  }
  if (hookInput && hookInput.workspacePaths && hookInput.workspacePaths.length > 0) {
    return hookInput.workspacePaths[0];
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

/**
 * Read Hook Input from stdin
 */
async function readHookInput() {
  return new Promise((resolve) => {
    let data = '';
    process.stdin.on('data', chunk => {
      data += chunk;
    });
    process.stdin.on('end', () => {
      try {
        resolve(JSON.parse(data));
      } catch (error) {
        resolve(null);
      }
    });
  });
}

// Load configuration from .plugin-config (project root)
function loadPluginConfig(projectRoot) {
  const configPath = path.join(projectRoot, '.plugin-config', 'hook-auto-docs.json');

  try {
    if (fs.existsSync(configPath)) {
      return JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
  } catch (error) {
    // Fall through to return default config
  }

  return {
    showLogs: false,
    outputDirectory: '',
    outputFile: '.project-structure.md',
    includeDirs: [],
    excludeDirs: [
      'node_modules', '.git', 'dist', 'build', 'coverage',
      '.next', 'out', '.nuxt', 'vendor', '.vscode', '.idea'
    ],
    includeExtensions: [],
    excludeExtensions: [],
    includeEmptyDirs: true
  };
}

/**
 * Check if file is in an included directory
 */
function isInIncludedDir(filePath, projectRoot, includedDirs) {
  if (!includedDirs || includedDirs.length === 0) {
    return true;
  }

  const relativePath = path.relative(projectRoot, filePath);
  return includedDirs.some(includedDir => {
    const normalizedDir = includedDir.replace(/\\/g, '/');
    const normalizedRelPath = relativePath.replace(/\\/g, '/');
    return normalizedRelPath.startsWith(normalizedDir + '/') || normalizedRelPath.startsWith(normalizedDir);
  });
}

/**
 * Check if file is in an excluded directory
 */
function isInExcludedDir(filePath, projectRoot, excludedDirs) {
  const relativePath = path.relative(projectRoot, filePath);
  const pathParts = relativePath.split(path.sep);

  return pathParts.some(part => {
    return excludedDirs.includes(part) || part.startsWith('.');
  });
}

/**
 * Check if file has valid extension
 */
function hasValidExtension(filePath, includeExtensions, excludeExtensions) {
  const ext = path.extname(filePath);

  if (includeExtensions && includeExtensions.length > 0) {
    if (!includeExtensions.includes(ext)) {
      return false;
    }
  }

  if (excludeExtensions && excludeExtensions.includes(ext)) {
    return false;
  }

  return true;
}

/**
 * Extract file path and operation from Hook Input (supports Claude Code & Antigravity)
 */
function getFileOperation(hookInput, projectRoot) {
  if (!hookInput) {
    return null;
  }

  let filePath = null;
  let operation = null;

  // 1. Claude Code format: { tool_name: "Write", tool_input: { file_path: "..." } }
  if (hookInput.tool_name && hookInput.tool_input) {
    const toolName = hookInput.tool_name.toLowerCase();
    const params = hookInput.tool_input;
    if (toolName === 'write') {
      filePath = params.file_path || params.path || params.TargetFile;
      operation = 'write';
    } else if (toolName === 'edit' || toolName === 'multiedit') {
      filePath = params.file_path || params.path || params.TargetFile;
      operation = 'edit';
    }
  }

  // 2. Antigravity format: { toolCall: { name: "write_to_file", args: { TargetFile: "..." } } }
  if (!filePath && hookInput.toolCall && hookInput.toolCall.name) {
    const toolName = hookInput.toolCall.name;
    const args = hookInput.toolCall.args || {};
    if (toolName === 'write_to_file') {
      filePath = args.TargetFile || args.filePath || args.file_path;
      operation = 'write';
    } else if (toolName === 'replace_file_content' || toolName === 'multi_replace_file_content') {
      filePath = args.TargetFile || args.filePath || args.file_path;
      operation = 'edit';
    }
  }

  if (!filePath) {
    return null;
  }

  // Convert to absolute path
  if (!path.isAbsolute(filePath)) {
    filePath = path.join(projectRoot, filePath);
  }

  return { filePath, operation };
}

/**
 * Load changes from tracking file
 */
function loadChanges(changesFile) {
  try {
    if (fs.existsSync(changesFile)) {
      const data = fs.readFileSync(changesFile, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {}
  return { files: [] };
}

/**
 * Save changes
 */
function saveChanges(changesFile, changes) {
  try {
    fs.writeFileSync(changesFile, JSON.stringify(changes, null, 2), 'utf8');
  } catch (error) {}
}

/**
 * Main function
 */
async function main() {
  const hookInput = await readHookInput();
  const projectRoot = getProjectRoot(hookInput);
  const config = loadPluginConfig(projectRoot);

  const INCLUDED_DIRS = config.includeDirs || [];
  const EXCLUDED_DIRS = config.excludeDirs || [
    'node_modules', '.git', 'dist', 'build', 'coverage',
    '.next', 'out', '.nuxt', 'vendor', '.vscode', '.idea'
  ];
  const INCLUDE_EXTENSIONS = config.includeExtensions || [];
  const EXCLUDE_EXTENSIONS = config.excludeExtensions || [];

  const PROJECT_NAME = path.basename(projectRoot);
  const PLUGIN_STATE_DIR = path.join(__dirname, '..', '.state');
  const CHANGES_FILE = path.join(PLUGIN_STATE_DIR, `${PROJECT_NAME}-structure-changes.json`);

  if (!fs.existsSync(PLUGIN_STATE_DIR)) {
    fs.mkdirSync(PLUGIN_STATE_DIR, { recursive: true });
  }

  const fileOp = getFileOperation(hookInput, projectRoot);

  if (fileOp) {
    if (hasValidExtension(fileOp.filePath, INCLUDE_EXTENSIONS, EXCLUDE_EXTENSIONS) &&
        !isInExcludedDir(fileOp.filePath, projectRoot, EXCLUDED_DIRS) &&
        isInIncludedDir(fileOp.filePath, projectRoot, INCLUDED_DIRS)) {
      const changes = loadChanges(CHANGES_FILE);
      const relativePath = path.relative(projectRoot, fileOp.filePath);

      if (!changes.files.includes(relativePath)) {
        changes.files.push(relativePath);
        saveChanges(CHANGES_FILE, changes);
      }
    }
  }

  // Antigravity PostToolUse contract expects {} on stdout
  console.log('{}');
  process.exit(0);
}

main();
