/**
 * Cursor Framework Quick Actions Plugin
 * 
 * Provides quick access to common framework operations.
 */

const { exec } = require('child_process');
const path = require('path');
const vscode = require('vscode');

/**
 * Execute a Python script and return the output.
 */
async function execPython(script, args = []) {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '.';
    const pythonPath = process.platform === 'win32' ? 'python' : 'python3';
    
    return new Promise((resolve, reject) => {
        const cmd = [pythonPath, script, ...args].join(' ');
        exec(cmd, { cwd: workspaceFolder }, (error, stdout, stderr) => {
            if (error) {
                reject(new Error(stderr || error.message));
                return;
            }
            resolve(stdout.trim());
        });
    });
}

/**
 * Get configuration value.
 */
function getConfig(key, defaultValue = null) {
    return vscode.workspace.getConfiguration('cursorFramework').get(key, defaultValue);
}

/**
 * Get workspace root path.
 */
function getWorkspaceRoot() {
    return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '.';
}

/**
 * Format JSON for display.
 */
function formatJson(json) {
    try {
        return JSON.stringify(JSON.parse(json), null, 2);
    } catch {
        return json;
    }
}

/**
 * Show output in a new document.
 */
async function showInDocument(title, content) {
    const doc = await vscode.workspace.openTextDocument({
        content: content,
        language: 'json'
    });
    await vscode.window.showTextDocument(doc, { title });
}

/**
 * Activate the plugin.
 */
async function activate(context) {
    const workspaceRoot = getWorkspaceRoot();
    const rootPath = getConfig('rootPath', '.cursor');
    const memoryPath = getConfig('memoryPath', '.cache/memory.json');
    const frameworkRoot = path.join(workspaceRoot, rootPath);

    // Warm Cache Command
    const warmCmd = vscode.commands.registerCommand('cursor-framework.warm', async () => {
        try {
            const { Workflow } = await import(path.join(workspaceRoot, 'cursor_framework', 'workflow.js')).catch(() => null);
            
            // Fallback to CLI
            const output = await execPython('-m', ['cursor_framework', 'warm', '--root', frameworkRoot]);
            vscode.window.showInformationMessage('Framework cache warmed!');
            await showInDocument('Warm Cache Result', formatJson(output));
        } catch (error) {
            vscode.window.showErrorMessage(`Warm failed: ${error.message}`);
        }
    });

    // Stats Command
    const statsCmd = vscode.commands.registerCommand('cursor-framework.stats', async () => {
        try {
            const output = await execPython('-m', ['cursor_framework', 'stats', '--root', frameworkRoot]);
            await showInDocument('Framework Stats', formatJson(output));
        } catch (error) {
            vscode.window.showErrorMessage(`Stats failed: ${error.message}`);
        }
    });

    // Clear Cache Command
    const clearCmd = vscode.commands.registerCommand('cursor-framework.clear-cache', async () => {
        const choice = await vscode.window.showWarningMessage(
            'Clear framework cache? This will remove memory and index files.',
            'Clear', 'Cancel'
        );
        
        if (choice === 'Clear') {
            try {
                const output = await execPython('-m', ['cursor_framework', 'clear-cache', '--root', frameworkRoot, '--force']);
                vscode.window.showInformationMessage('Cache cleared!');
                await showInDocument('Clear Cache Result', formatJson(output));
            } catch (error) {
                vscode.window.showErrorMessage(`Clear failed: ${error.message}`);
            }
        }
    });

    // Scan Command
    const scanCmd = vscode.commands.registerCommand('cursor-framework.scan', async () => {
        try {
            const output = await execPython('-m', ['cursor_framework', 'scan', '--root', frameworkRoot]);
            await showInDocument('Scan Result', formatJson(output));
        } catch (error) {
            vscode.window.showErrorMessage(`Scan failed: ${error.message}`);
        }
    });

    // Dashboard Command
    const dashboardCmd = vscode.commands.registerCommand('cursor-framework.dashboard', async () => {
        const port = getConfig('dashboardPort', 8765);
        const uri = vscode.Uri.parse(`http://localhost:${port}`);
        await vscode.env.openExternal(uri);
        vscode.window.showInformationMessage(`Dashboard opened at http://localhost:${port}`);
    });

    // Dump Context Command
    const dumpCmd = vscode.commands.registerCommand('cursor-framework.dump-context', async () => {
        try {
            const output = await execPython('-m', ['cursor_framework', 'context', '--root', frameworkRoot]);
            await showInDocument('Context Dump', output);
        } catch (error) {
            vscode.window.showErrorMessage(`Dump failed: ${error.message}`);
        }
    });

    // Graph Command
    const graphCmd = vscode.commands.registerCommand('cursor-framework.graph', async () => {
        const port = 8766;
        const uri = vscode.Uri.parse(`http://localhost:${port}`);
        await vscode.env.openExternal(uri);
        vscode.window.showInformationMessage(`Skill graph opened at http://localhost:${port}`);
    });

    // Index Command
    const indexCmd = vscode.commands.registerCommand('cursor-framework.index', async () => {
        try {
            const output = await execPython('-m', ['cursor_framework', 'index', '--root', frameworkRoot]);
            vscode.window.showInformationMessage('Index rebuilt!');
            await showInDocument('Index Result', formatJson(output));
        } catch (error) {
            vscode.window.showErrorMessage(`Index failed: ${error.message}`);
        }
    });

    // Find Skills Command
    const findSkillsCmd = vscode.commands.registerCommand('cursor-framework.find-skills', async () => {
        const query = await vscode.window.showInputBox({
            prompt: 'Enter skill search query',
            placeHolder: 'e.g., "frontend", "security", "database"'
        });
        
        if (query) {
            try {
                // Use workflow ask to find relevant skills
                const wf = await import(path.join(workspaceRoot, 'cursor_framework', 'workflow.js')).catch(() => null);
                if (wf) {
                    const result = wf.Workflow.ask(query);
                    await showInDocument('Skills Discovery', result.context.text);
                }
            } catch (error) {
                vscode.window.showErrorMessage(`Find skills failed: ${error.message}`);
            }
        }
    });

    // Code Graph Command
    const codeGraphCmd = vscode.commands.registerCommand('cursor-framework.code-graph', async () => {
        try {
            const output = await execPython('-m', ['cursor_framework', 'dump-graph', '--root', workspaceRoot]);
            await showInDocument('Code Graph', formatJson(output));
        } catch (error) {
            vscode.window.showErrorMessage(`Code graph failed: ${error.message}`);
        }
    });

    // Register all commands
    context.subscriptions.push(
        warmCmd, statsCmd, clearCmd, scanCmd, dashboardCmd,
        dumpCmd, graphCmd, indexCmd, findSkillsCmd, codeGraphCmd
    );
}

/**
 * Deactivate the plugin.
 */
function deactivate() {}

module.exports = { activate, deactivate };
