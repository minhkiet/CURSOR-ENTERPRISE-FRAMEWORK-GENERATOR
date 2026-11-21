/**
 * Vibe Framework Status Line Plugin
 * 
 * Provides real-time status bar telemetry for Vibe Enterprise Framework.
 */

const { exec } = require('child_process');
const path = require('path');
const vscode = require('vscode');

let statusBarItem;
let refreshTimer = null;

function getWorkspaceRoot() {
    return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '.';
}

function getConfig(key, defaultValue = null) {
    return vscode.workspace.getConfiguration('vibeFramework').get(key, defaultValue);
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

async function updateStatusBar() {
    if (!statusBarItem) return;

    const enabled = getConfig('statusLine.enabled', true);
    if (!enabled) {
        statusBarItem.hide();
        return;
    }

    const rootPath = getConfig('rootPath', '.cursor');
    const workspaceRoot = getWorkspaceRoot();
    const frameworkRoot = path.join(workspaceRoot, rootPath);
    const showTokens = getConfig('statusLine.showTokens', true);
    const showSkills = getConfig('statusLine.showSkills', true);

    try {
        const rawOutput = await execPython(['-m', 'vibe_framework', 'stats', '--root', `"${frameworkRoot}"`]);
        let parsed = null;
        try {
            parsed = JSON.parse(rawOutput);
        } catch {
            parsed = null;
        }

        const skillsCount = parsed?.skills_count ?? parsed?.total_skills ?? parsed?.indexer?.total_skills ?? 'OK';
        const rulesCount = parsed?.rules_count ?? parsed?.total_rules ?? parsed?.indexer?.total_rules ?? '';
        const tokensCount = parsed?.total_tokens ?? parsed?.memory?.tokens ?? null;

        let label = '$(zap) Cursor';
        let details = [];
        if (showSkills && skillsCount !== undefined) {
            details.push(`${skillsCount} skills`);
        }
        if (rulesCount) {
            details.push(`${rulesCount} rules`);
        }
        if (showTokens && tokensCount !== null) {
            details.push(`${tokensCount} tokens`);
        }

        statusBarItem.text = details.length > 0 ? `${label}: Ready (${details.join(' | ')})` : `${label}: Ready`;
        statusBarItem.tooltip = `Vibe Enterprise Framework\nStatus: Warm & Operational\nSkills: ${skillsCount}\nRules: ${rulesCount}\nClick for Quick Menu`;
        statusBarItem.backgroundColor = undefined;
        statusBarItem.show();
    } catch (err) {
        statusBarItem.text = '$(warning) Cursor: Cache Cold';
        statusBarItem.tooltip = `Framework cache requires warming.\nClick to warm now.\nError: ${err.message}`;
        statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
        statusBarItem.show();
    }
}

async function showQuickMenu() {
    const workspaceRoot = getWorkspaceRoot();
    const rootPath = getConfig('rootPath', '.cursor');
    const frameworkRoot = path.join(workspaceRoot, rootPath);

    const items = [
        { label: '$(flame) Warm Cache', description: 'Re-index skills and warm memory', action: 'warm' },
        { label: '$(symbol-structure) Rebuild Index', description: 'Scan and write INDEX.json & INDEX.md', action: 'index' },
        { label: '$(dashboard) Open Dashboard', description: 'Launch browser dashboard (port 8765)', action: 'dashboard' },
        { label: '$(sync) Multi-Agent Vibe Sync', description: 'Sync rules across Cursor, Claude, and Codex', action: 'vibe' },
        { label: '$(checklist) Spec Kit Status', description: 'Check SDD specifications and task status', action: 'spec' },
        { label: '$(graph) View Skill Graph', description: 'Open interactive dependency graph', action: 'graph' },
        { label: '$(trash) Clear Cache', description: 'Wipe cache memory and temporary indices', action: 'clear' }
    ];

    const selected = await vscode.window.showQuickPick(items, {
        placeHolder: 'Select Vibe Enterprise Framework Action'
    });

    if (!selected) return;

    try {
        switch (selected.action) {
            case 'warm':
                await execPython(['-m', 'vibe_framework', 'warm', '--root', `"${frameworkRoot}"`]);
                vscode.window.showInformationMessage('Framework cache warmed successfully!');
                await updateStatusBar();
                break;
            case 'index':
                await execPython(['-m', 'vibe_framework', 'index', '--root', `"${frameworkRoot}"`]);
                vscode.window.showInformationMessage('Framework index rebuilt!');
                await updateStatusBar();
                break;
            case 'dashboard':
                vscode.commands.executeCommand('vibe-framework.dashboard');
                break;
            case 'vibe':
                const vibeOut = await execPython(['-m', 'vibe_framework', 'vibe', 'sync']);
                vscode.window.showInformationMessage(`Vibe Sync complete! ${vibeOut.slice(0, 80)}...`);
                break;
            case 'spec':
                const specOut = await execPython(['-m', 'vibe_framework', 'spec', 'status']);
                const doc = await vscode.workspace.openTextDocument({ content: specOut, language: 'text' });
                await vscode.window.showTextDocument(doc);
                break;
            case 'graph':
                vscode.commands.executeCommand('vibe-framework.graph');
                break;
            case 'clear':
                vscode.commands.executeCommand('vibe-framework.clear-cache');
                await updateStatusBar();
                break;
        }
    } catch (error) {
        vscode.window.showErrorMessage(`Action failed: ${error.message}`);
    }
}

function activate(context) {
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'vibe-framework.status-line.menu';
    context.subscriptions.push(statusBarItem);

    const refreshCmd = vscode.commands.registerCommand('vibe-framework.status-line.refresh', async () => {
        await updateStatusBar();
        vscode.window.showInformationMessage('Vibe Framework status refreshed.');
    });

    const menuCmd = vscode.commands.registerCommand('vibe-framework.status-line.menu', async () => {
        await showQuickMenu();
    });

    const toggleCmd = vscode.commands.registerCommand('vibe-framework.status-line.toggle', () => {
        const current = getConfig('statusLine.enabled', true);
        vscode.workspace.getConfiguration('vibeFramework').update('statusLine.enabled', !current, vscode.ConfigurationTarget.Global);
        if (current) {
            statusBarItem.hide();
        } else {
            updateStatusBar();
        }
    });

    context.subscriptions.push(refreshCmd, menuCmd, toggleCmd);

    // Initial load
    updateStatusBar();

    // Auto-refresh timer
    const interval = getConfig('statusLine.refreshInterval', 30000);
    if (interval > 0) {
        refreshTimer = setInterval(updateStatusBar, interval);
    }

    // Refresh on save for relevant files
    const watcher = vscode.workspace.onDidSaveTextDocument(doc => {
        const p = doc.fileName.replace(/\\/g, '/');
        if (p.includes('/.cursor/') || p.includes('/.agents/') || p.includes('/vibe_framework/')) {
            updateStatusBar();
        }
    });
    context.subscriptions.push(watcher);
}

function deactivate() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
        refreshTimer = null;
    }
    if (statusBarItem) {
        statusBarItem.dispose();
    }
}

module.exports = { activate, deactivate };
