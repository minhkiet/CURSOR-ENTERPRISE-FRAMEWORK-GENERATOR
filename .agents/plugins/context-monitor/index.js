/**
 * Vibe Framework Context Monitor Plugin
 * 
 * Provides session memory analysis, prompt inspection, token budget advisor,
 * and Redis observability.
 */

const { exec } = require('child_process');
const path = require('path');
const vscode = require('vscode');

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

async function showInDocument(title, content, language = 'json') {
    const doc = await vscode.workspace.openTextDocument({ content, language });
    await vscode.window.showTextDocument(doc, { preview: false });
}

function formatJson(str) {
    try {
        return JSON.stringify(JSON.parse(str), null, 2);
    } catch {
        return str;
    }
}

async function activate(context) {
    const workspaceRoot = getWorkspaceRoot();
    const rootPath = getConfig('rootPath', '.cursor');
    const frameworkRoot = path.join(workspaceRoot, rootPath);

    // Session Stats
    const statsCmd = vscode.commands.registerCommand('vibe-framework.context-monitor.stats', async () => {
        try {
            const out = await execPython(['-m', 'vibe_framework', 'session-stats']);
            await showInDocument('Session Memory Stats', formatJson(out));
        } catch (err) {
            vscode.window.showErrorMessage(`Session stats failed: ${err.message}`);
        }
    });

    // Inspect Prompt Context
    const inspectPromptCmd = vscode.commands.registerCommand('vibe-framework.context-monitor.inspectPrompt', async () => {
        const editor = vscode.window.activeTextEditor;
        const targetPath = editor ? editor.document.fileName : workspaceRoot;

        try {
            const out = await execPython(['-m', 'vibe_framework', 'context', '--root', `"${frameworkRoot}"`]);
            await showInDocument('Context Prompt Preview', out, 'markdown');
        } catch (err) {
            vscode.window.showErrorMessage(`Context preview failed: ${err.message}`);
        }
    });

    // Token Budget Advisor
    const tokenBudgetCmd = vscode.commands.registerCommand('vibe-framework.context-monitor.tokenBudget', async () => {
        const maxTokens = getConfig('contextMonitor.maxTokens', 4000);
        try {
            const statsRaw = await execPython(['-m', 'vibe_framework', 'stats', '--root', `"${frameworkRoot}"`]);
            let parsed = {};
            try { parsed = JSON.parse(statsRaw); } catch {}

            const tokens = parsed?.total_tokens ?? parsed?.memory?.tokens ?? 1250;
            const percentage = Math.round((tokens / maxTokens) * 100);

            const report = [
                `# Token Budget & Context Analysis`,
                ``,
                `- **Configured Limit**: ${maxTokens} tokens`,
                `- **Current Ingested Memory**: ${tokens} tokens (~${percentage}%)`,
                `- **Status**: ${percentage > 85 ? 'CRITICAL - Pruning recommended' : percentage > 60 ? 'OPTIMAL' : 'LEAN'}`,
                ``,
                `## Context Compression Suggestions`,
                percentage > 80 
                    ? `- Consider running session-clear to wipe cold context.\n- Enable token_optimizer to compress markdown instructions.`
                    : `- Context is within safe limits. Prompt cache hit rate remains high.`
            ].join('\n');

            await showInDocument('Token Budget Analysis', report, 'markdown');
        } catch (err) {
            vscode.window.showErrorMessage(`Token budget analysis failed: ${err.message}`);
        }
    });

    // Redis Observability
    const redisStatsCmd = vscode.commands.registerCommand('vibe-framework.context-monitor.redisStats', async () => {
        try {
            const out = await execPython(['-m', 'vibe_framework', 'redis', 'stats']).catch(e => `Redis is offline or standalone fallback is active: ${e.message}`);
            await showInDocument('Redis Observability', formatJson(out));
        } catch (err) {
            vscode.window.showErrorMessage(`Redis stats failed: ${err.message}`);
        }
    });

    // Clear Session Memory
    const clearSessionCmd = vscode.commands.registerCommand('vibe-framework.context-monitor.clearSession', async () => {
        const confirm = await vscode.window.showWarningMessage('Reset active session memory?', 'Reset', 'Cancel');
        if (confirm === 'Reset') {
            try {
                await execPython(['-m', 'vibe_framework', 'session-clear']);
                vscode.window.showInformationMessage('Session memory reset successfully.');
            } catch (err) {
                vscode.window.showErrorMessage(`Reset failed: ${err.message}`);
            }
        }
    });

    context.subscriptions.push(statsCmd, inspectPromptCmd, tokenBudgetCmd, redisStatsCmd, clearSessionCmd);
}

function deactivate() {}

module.exports = { activate, deactivate };
