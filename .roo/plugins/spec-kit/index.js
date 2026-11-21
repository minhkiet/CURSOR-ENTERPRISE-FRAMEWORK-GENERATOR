/**
 * Vibe Framework Spec Kit Plugin
 * 
 * Provides interactive Spec-Driven Development (SDD) tooling:
 * Init, List, Status, Validate, and Constitution.
 */

const { exec } = require('child_process');
const vscode = require('vscode');

function getWorkspaceRoot() {
    return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '.';
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

async function showInDocument(title, content, language = 'markdown') {
    const doc = await vscode.workspace.openTextDocument({ content, language });
    await vscode.window.showTextDocument(doc, { preview: false });
}

function activate(context) {
    // Init Feature Spec
    const initCmd = vscode.commands.registerCommand('vibe-framework.spec-kit.init', async () => {
        const featureName = await vscode.window.showInputBox({
            prompt: 'Enter feature name (kebab-case)',
            placeHolder: 'e.g. payment-flow, user-auth, oauth-provider'
        });

        if (!featureName) return;

        try {
            const out = await execPython(['-m', 'vibe_framework', 'spec', 'init', featureName]);
            vscode.window.showInformationMessage(`Specification initialized for: ${featureName}`);
            await showInDocument(`Spec - ${featureName}`, out);
        } catch (err) {
            vscode.window.showErrorMessage(`Spec initialization failed: ${err.message}`);
        }
    });

    // List All Specs
    const listCmd = vscode.commands.registerCommand('vibe-framework.spec-kit.list', async () => {
        try {
            const out = await execPython(['-m', 'vibe_framework', 'spec', 'list']);
            await showInDocument('All Specifications', out);
        } catch (err) {
            vscode.window.showErrorMessage(`Listing specs failed: ${err.message}`);
        }
    });

    // Feature Spec Status
    const statusCmd = vscode.commands.registerCommand('vibe-framework.spec-kit.status', async () => {
        const featureName = await vscode.window.showInputBox({
            prompt: 'Enter feature name to check status',
            placeHolder: 'Leave blank to inspect global status'
        });

        try {
            const args = ['-m', 'vibe_framework', 'spec', 'status'];
            if (featureName) args.push(featureName);
            const out = await execPython(args);
            await showInDocument('Spec Status', out);
        } catch (err) {
            vscode.window.showErrorMessage(`Spec status failed: ${err.message}`);
        }
    });

    // Validate Spec
    const validateCmd = vscode.commands.registerCommand('vibe-framework.spec-kit.validate', async () => {
        const featureName = await vscode.window.showInputBox({
            prompt: 'Enter feature name to validate against Constitution',
            placeHolder: 'e.g. core-auth'
        });

        if (!featureName) return;

        try {
            const out = await execPython(['-m', 'vibe_framework', 'spec', 'validate', featureName]);
            vscode.window.showInformationMessage(`Validation complete for ${featureName}!`);
            await showInDocument(`Validation - ${featureName}`, out);
        } catch (err) {
            vscode.window.showErrorMessage(`Validation failed: ${err.message}`);
        }
    });

    // View Constitution
    const constitutionCmd = vscode.commands.registerCommand('vibe-framework.spec-kit.constitution', async () => {
        try {
            const out = await execPython(['-m', 'vibe_framework', 'spec', 'constitution']);
            await showInDocument('Project Constitution', out);
        } catch (err) {
            vscode.window.showErrorMessage(`Failed to load constitution: ${err.message}`);
        }
    });

    context.subscriptions.push(initCmd, listCmd, statusCmd, validateCmd, constitutionCmd);
}

function deactivate() {}

module.exports = { activate, deactivate };
