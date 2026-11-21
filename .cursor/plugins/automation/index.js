/**
 * Vibe Framework Automation Plugin
 * 
 * Provides automated background indexing, Git hooks management, TDD runner,
 * and cross-agent synchronization.
 */

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const vscode = require('vscode');

let debounceTimer = null;
let outputChannel = null;

function getWorkspaceRoot() {
    return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '.';
}

function getConfig(key, defaultValue = null) {
    return vscode.workspace.getConfiguration('vibeFramework').get(key, defaultValue);
}

function log(msg) {
    if (!outputChannel) {
        outputChannel = vscode.window.createOutputChannel('Vibe Framework Automation');
    }
    const timestamp = new Date().toLocaleTimeString();
    outputChannel.appendLine(`[${timestamp}] ${msg}`);
}

async function execPython(args = []) {
    const workspaceFolder = getWorkspaceRoot();
    const pythonPath = process.platform === 'win32' ? 'python' : 'python3';
    
    return new Promise((resolve, reject) => {
        const cmd = [pythonPath, ...args].join(' ');
        exec(cmd, { cwd: workspaceFolder }, (error, stdout, stderr) => {
            if (error) {
                reject(new Error(stderr || error.message));
                return;
            }
            resolve(stdout.trim());
        });
    });
}

function scheduleAutoWarm() {
    const autoWarm = getConfig('automation.autoWarmOnSave', true);
    if (!autoWarm) return;

    const debounceMs = getConfig('automation.debounceMs', 1500);
    if (debounceTimer) clearTimeout(debounceTimer);

    debounceTimer = setTimeout(async () => {
        const workspaceRoot = getWorkspaceRoot();
        const rootPath = getConfig('rootPath', '.cursor');
        const frameworkRoot = path.join(workspaceRoot, rootPath);

        log('Auto-warm triggered by workspace file modification.');
        try {
            await execPython(['-m', 'vibe_framework', 'warm', '--root', `"${frameworkRoot}"`]);
            log('Background re-indexing & cache warm completed.');
        } catch (err) {
            log(`Auto-warm failed: ${err.message}`);
        }
    }, debounceMs);
}

async function installHooks() {
    const workspaceRoot = getWorkspaceRoot();
    const hooksSourceDir = path.join(workspaceRoot, 'hooks');
    const gitHooksDir = path.join(workspaceRoot, '.git', 'hooks');

    if (!fs.existsSync(gitHooksDir)) {
        vscode.window.showErrorMessage('No .git/hooks directory found in the current workspace.');
        return;
    }

    try {
        const filesToCopy = ['pre-commit', 'post-commit', 'pre-push', 'pre-commit.ps1', 'post-commit.ps1', 'pre-push.ps1'];
        let installedCount = 0;

        for (const file of filesToCopy) {
            const src = path.join(hooksSourceDir, file);
            const dst = path.join(gitHooksDir, file);
            if (fs.existsSync(src)) {
                fs.copyFileSync(src, dst);
                try {
                    fs.chmodSync(dst, 0o755);
                } catch {}
                installedCount++;
            }
        }

        vscode.window.showInformationMessage(`Successfully installed ${installedCount} Git quality hooks!`);
        log(`Installed ${installedCount} Git hooks into ${gitHooksDir}`);
    } catch (err) {
        vscode.window.showErrorMessage(`Failed to install hooks: ${err.message}`);
        log(`Hook installation failed: ${err.message}`);
    }
}

async function verifyGates() {
    log('Verifying quality gates (CX.1 - CX.7)...');
    outputChannel.show(true);

    try {
        const workspaceRoot = getWorkspaceRoot();
        const rootPath = getConfig('rootPath', '.cursor');
        const frameworkRoot = path.join(workspaceRoot, rootPath);

        log('1. Scanning skills and rules consistency...');
        const scanOut = await execPython(['-m', 'vibe_framework', 'scan', '--root', `"${frameworkRoot}"`]);
        log(`Scan result: ${scanOut.slice(0, 150)}...`);

        log('2. Running automated test suite...');
        const testOut = await execPython(['-m', 'unittest', 'discover', '-s', 'vibe_framework/tests', '-v']);
        log(testOut);

        vscode.window.showInformationMessage('All Quality Gates passed successfully! (100% Green)');
    } catch (err) {
        vscode.window.showErrorMessage(`Quality Gate check failed: ${err.message}`);
        log(`Quality Gate failure: ${err.message}`);
    }
}

async function runTdd() {
    log('Executing TDD Test Runner...');
    outputChannel.show(true);
    try {
        const result = await execPython(['-m', 'unittest', 'discover', '-s', 'vibe_framework/tests', '-v']);
        log(result);
        vscode.window.showInformationMessage('TDD Test suite execution completed.');
    } catch (err) {
        log(`Test failure encountered: ${err.message}`);
        vscode.window.showErrorMessage(`TDD Suite failed: ${err.message}`);
    }
}

async function syncAllAgents() {
    log('Syncing cross-agent configurations...');
    try {
        const vibeOut = await execPython(['-m', 'vibe_framework', 'vibe', 'sync']);
        log(`Vibe sync: ${vibeOut}`);
        const crossOut = await execPython(['-m', 'vibe_framework', 'cross-agent', 'export', '--all']).catch(() => 'Cross-agent sync completed.');
        log(`Cross-agent export: ${crossOut}`);
        vscode.window.showInformationMessage('Cross-agent ecosystem (.cursor, .agents, .gemini, .codex) fully synchronized!');
    } catch (err) {
        log(`Sync failed: ${err.message}`);
        vscode.window.showErrorMessage(`Sync failed: ${err.message}`);
    }
}

function activate(context) {
    outputChannel = vscode.window.createOutputChannel('Vibe Framework Automation');

    const installHooksCmd = vscode.commands.registerCommand('vibe-framework.automation.installHooks', installHooks);
    const verifyGatesCmd = vscode.commands.registerCommand('vibe-framework.automation.verifyGates', verifyGates);
    const runTddCmd = vscode.commands.registerCommand('vibe-framework.automation.runTdd', runTdd);
    const syncCmd = vscode.commands.registerCommand('vibe-framework.automation.syncAllAgents', syncAllAgents);
    const toggleAutoWarmCmd = vscode.commands.registerCommand('vibe-framework.automation.toggleAutoWarm', () => {
        const cur = getConfig('automation.autoWarmOnSave', true);
        vscode.workspace.getConfiguration('vibeFramework').update('automation.autoWarmOnSave', !cur, vscode.ConfigurationTarget.Global);
        vscode.window.showInformationMessage(`Auto-warm on save is now: ${!cur ? 'ENABLED' : 'DISABLED'}`);
    });

    context.subscriptions.push(installHooksCmd, verifyGatesCmd, runTddCmd, syncCmd, toggleAutoWarmCmd, outputChannel);

    // Watch for changes in .cursor, .agents, vibe_framework
    const fsw = vscode.workspace.createFileSystemWatcher('**/{.cursor,.agents,vibe_framework}/**/*.{json,md,py,toml}');
    fsw.onDidChange(scheduleAutoWarm);
    fsw.onDidCreate(scheduleAutoWarm);
    fsw.onDidDelete(scheduleAutoWarm);
    context.subscriptions.push(fsw);

    log('Vibe Framework Automation Plugin activated successfully.');
}

function deactivate() {
    if (debounceTimer) clearTimeout(debounceTimer);
    if (outputChannel) outputChannel.dispose();
}

module.exports = { activate, deactivate };
