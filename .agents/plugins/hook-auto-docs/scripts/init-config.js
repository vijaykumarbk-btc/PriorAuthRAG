#!/usr/bin/env node

/**
 * Initialization script for Auto Docs plugin
 * Runs at session start to ensure user configuration file exists
 */

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
const configDir = path.join(projectRoot, '.plugin-config');
const configPath = path.join(configDir, 'hook-auto-docs.json');

/**
 * Read plugin version from plugin.json (cross-platform safe)
 */
function getPluginVersion() {
  const possiblePaths = [
    path.join(__dirname, '..', 'plugin.json'),
    path.join(__dirname, '..', '.claude-plugin', 'plugin.json')
  ];
  for (const p of possiblePaths) {
    try {
      if (fs.existsSync(p)) {
        const pluginJson = JSON.parse(fs.readFileSync(p, 'utf8'));
        if (pluginJson.version) return pluginJson.version;
      }
    } catch (e) {}
  }
  return '1.4.1';
}

const PLUGIN_VERSION = getPluginVersion();

// Default configuration with all available options
const defaultConfig = {
  showLogs: false,
  outputDirectory: '',
  outputFile: '.project-structure.md',
  includeDirs: [],
  excludeDirs: [
    'node_modules',
    '.git',
    'dist',
    'build',
    'coverage',
    '.next',
    'out',
    '.nuxt',
    'vendor',
    '.vscode',
    '.idea'
  ],
  includeExtensions: [],
  excludeExtensions: [],
  includeEmptyDirs: true
};

/**
 * Initialize or migrate configuration file
 */
function initializeConfig() {
  try {
    // Create .plugin-config directory if it doesn't exist
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }

    // Check if config file exists
    if (fs.existsSync(configPath)) {
      try {
        const existingConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));

        // If version matches, no migration needed
        if (existingConfig._pluginVersion === PLUGIN_VERSION) {
          return;
        }

        // Migrate: merge existing config with new defaults
        const migratedConfig = {
          ...defaultConfig,           // New fields with defaults
          ...existingConfig,          // Preserve existing user settings
          _pluginVersion: PLUGIN_VERSION
        };

        fs.writeFileSync(configPath, JSON.stringify(migratedConfig, null, 2), 'utf8');
      } catch (error) {
        // If parse fails, create new config
        fs.writeFileSync(configPath, JSON.stringify({
          ...defaultConfig,
          _pluginVersion: PLUGIN_VERSION
        }, null, 2), 'utf8');
      }
    } else {
      // Create new config file
      fs.writeFileSync(configPath, JSON.stringify({
        ...defaultConfig,
        _pluginVersion: PLUGIN_VERSION
      }, null, 2), 'utf8');
    }
  } catch (error) {
    // Fail silently - don't block session start if config creation fails
  }
}

initializeConfig();
console.log('{}');
process.exit(0);
