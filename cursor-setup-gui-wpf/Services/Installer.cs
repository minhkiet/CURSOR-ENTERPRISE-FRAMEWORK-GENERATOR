using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using CursorSetupWpf.Models;

namespace CursorSetupWpf.Services
{
    /// <summary>
    /// Supported vibe coding agents for cross-agent installation.
    /// </summary>
    public enum TargetAgent
    {
        Cursor,      // Cursor IDE - primary target
        Codex,       // Codex (cursor.com / origin.cursor.com)
        ClaudeCode,  // Claude Code (@cursor/codex)
        Grok,        // Grok (x.com/grok)
        Windsurf,    // WindSurf IDE
        Continue,    // Continue.dev
        Cline,      // Cline VSCode extension
        Roo,        // Roo Code
        Aider,      // Aider CLI
        GeminiCLI,   // Google Gemini CLI
        KimiCode,   // Kimi Code AI
        Zed,        // Zed AI Editor
        Copilot,    // GitHub Copilot
        Antigravity, // Antigravity
    }

    /// <summary>
    /// Standard AI/Vibe Code framework directories.
    /// Maps to all popular vibe coding tools.
    /// </summary>
    public static class FrameworkDirectories
    {
        // Primary framework roots (can contain skills, rules, agents, etc.)
        public static readonly Dictionary<string, string[]> PrimaryRoots = new()
        {
            { ".cursor", new[] { "skills", "rules", "agents", "commands", "hooks", "knowledge", "references", "workflows", "prompts", "templates", "memory", "scripts" } },
            { ".claude", new[] { "skills", "rules", "agents", "commands", "prompts" } },
            { ".codex", new[] { "skills", "prompts", "agents" } },
            { ".grok", new[] { "skills", "rules", "agents" } },
            { ".gemini", new[] { "skills", "commands" } },
            { ".windsurf", new[] { "rules", "workflows" } },
            { ".continue", new[] { "rules", "prompts" } },
            { ".aider", Array.Empty<string>() }, // Uses .aider.conf.yml
            { ".roo", new[] { "rules", "modes", "commands" } },
            { ".cline", new[] { "rules", "skills" } },
            { ".kiro", new[] { "steering", "specs" } },
            { ".qwen", new[] { "commands", "skills" } },
            { ".opencode", new[] { "agents", "commands", "skills" } },
            { ".factory", new[] { "droids", "skills" } },
            { ".vibe", new[] { "skills", "rules", "agents", "commands", "prompts", "workflows", "templates", "config" } },
            { ".agents", new[] { "skills", "rules", "workflows" } },
            { ".github", new[] { "copilot", "prompts", "instructions", "agents" } },
            { ".vscode", new[] { "settings.json", "tasks.json", "extensions.json" } },
        };

        // Skills directories per agent
        public static readonly Dictionary<string, string> SkillsDirs = new()
        {
            { "Cursor", ".cursor/skills" },
            { "Codex", ".cursor/skills" },
            { "ClaudeCode", ".claude/skills" },
            { "Grok", ".grok/skills" },
            { "GeminiCLI", ".gemini/skills" },
            { "Windsurf", ".windsurf/rules" },
            { "Continue", ".continue/rules" },
            { "Cline", ".cline/skills" },
            { "Roo", ".roo/rules" },
            { "Aider", ".aider" },
            { "KimiCode", ".vibe/skills" },
            { "Zed", ".zed" },
            { "Copilot", ".github/copilot" },
            { "Antigravity", ".gemini/skills" },
        };

        // Rules directories per agent
        public static readonly Dictionary<string, string> RulesDirs = new()
        {
            { "Cursor", ".cursor/rules" },
            { "Codex", ".cursor/rules" },
            { "ClaudeCode", ".claude/rules" },
            { "Grok", ".grok/rules" },
            { "GeminiCLI", ".gemini/rules" },
            { "Windsurf", ".windsurf/rules" },
            { "Continue", ".continue/rules" },
            { "Cline", ".cline/rules" },
            { "Roo", ".roo/rules" },
            { "KimiCode", ".vibe/rules" },
            { "Antigravity", ".gemini/rules" },
        };
    }

    /// <summary>
    /// Agent-specific installation configuration.
    /// </summary>
    public class AgentInstallConfig
    {
        public TargetAgent Agent { get; init; }
        public string Name { get; init; } = "";
        public string SkillsPath { get; init; } = "";
        public string RulesPath { get; init; } = "";
        public string AgentsPath { get; init; } = "";
        public string GatePrefix { get; init; } = "U";
        public string[] EnvVars { get; init; } = Array.Empty<string>();
        public string InstallUrl { get; init; } = "";
        public bool SupportsMcp { get; init; }
        public bool SupportsRules { get; init; } = true;
        public string Description { get; init; } = "";
        public string Icon { get; init; } = "\uE8B7"; // Default icon
    }

    public class Installer
    {
        public event Action<int, string> ProgressChanged = null!;  // 0-100, status message
        public event Action<string> LogAppended = null!;

        readonly string[] _buildStepScripts = new[]
        {
            "memory-builder/build-memory.ps1",
            "knowledge-compiler/compile-knowledge.ps1",
            "project-index-builder/build-index.ps1",
            "embedding-builder/build-embeddings.ps1",
            "packager.ps1",
        };

        // Real MCP packages live under {installPath}/mcp/<PackageDir> and expose
        // python -m <Module>. Legacy keys from older installers are removed on sync.
        // Version 4.0.0: Added Vercel and Browser MCP servers
        // Version 5.0.0: Added evondev-ui-ux skill
        static readonly (
            string ServerKey,
            string PackageDir,
            string Module,
            string DisplayName,
            string Description,
            string[] Tools
        )[] McpCatalog =
        {
            (
                "cursor-framework",
                "cursor-framework-mcp",
                "cursor_framework_mcp.server",
                "Framework MCP",
                "Cursor Enterprise Framework — rules, skills, agents registry.",
                new[]
                {
                    "get_rule", "get_skill", "get_agent", "analyze_task",
                    "load_skill_bundle", "get_essential_skills", "clear_cache",
                    "get_framework_status", "optimize_framework"
                }
            ),
            (
                "cursor-autopilot",
                "cursor-autopilot-mcp",
                "cursor_autopilot_mcp.server",
                "Autopilot MCP",
                "Auto-execution engine for workflows, gates, and suggestions.",
                new[]
                {
                    "auto_execute", "execute_workflow", "run_gate_validation",
                    "get_workflow_status", "abort_workflow", "list_workflows",
                    "estimate_cost", "suggest_optimization"
                }
            ),
            (
                "cursor-memory",
                "cursor-memory-mcp",
                "cursor_memory_mcp.server",
                "Memory MCP",
                "Persistent workspace memory and context management.",
                new[]
                {
                    "store_memory", "recall_memory", "compact_context",
                    "summarize_history", "get_context_stats", "prune_context",
                    "export_memory", "import_memory", "sync_to_disk"
                }
            ),
            // Version 4.0.0 - New MCP Servers
            (
                "vercel",
                null,
                null,
                "Vercel AI SDK",
                "Vercel AI SDK — deploy and manage AI projects with Vercel.",
                new[]
                {
                    "vercel_deploy", "vercel_model_list", "vercel_model_deploy"
                }
            ),
            (
                "browser",
                null,
                null,
                "Browser MCP",
                "Browser automation — web scraping, screenshots, and testing.",
                new[]
                {
                    "browser_navigate", "browser_snapshot", "browser_click",
                    "browser_type", "browser_screenshot"
                }
            ),
        };

        static readonly string[] LegacyMcpKeys = { "framework", "autopilot", "memory" };

    // ─── Cross-Agent Installation Catalog ────────────────────────────────────
    // Version 5.0.0: Added cross-agent installation support with all vibe coding tools

        static readonly AgentInstallConfig[] AgentCatalog =
        {
            // Primary IDEs
            new AgentInstallConfig
            {
                Agent = TargetAgent.Cursor,
                Name = "Cursor IDE",
                SkillsPath = ".cursor/skills",
                RulesPath = ".cursor/rules",
                AgentsPath = ".cursor/agents",
                GatePrefix = "K",
                EnvVars = new[] { "CURSOR_IDE", "CURSOR_PROJECT" },
                InstallUrl = "https://cursor.com",
                SupportsMcp = true,
                SupportsRules = true,
                Description = "AI-first code editor with integrated agent skills",
                Icon = "\uE8B7",
            },
            new AgentInstallConfig
            {
                Agent = TargetAgent.Codex,
                Name = "Codex (cursor.com)",
                SkillsPath = ".cursor/skills",
                RulesPath = ".cursor/rules",
                AgentsPath = ".cursor/agents",
                GatePrefix = "CX",
                EnvVars = new[] { "CODEX_ENABLED", "ORIGIN_HOST" },
                InstallUrl = "https://origin.cursor.com",
                SupportsMcp = true,
                SupportsRules = true,
                Description = "Cloud-powered coding agent from Cursor",
                Icon = "\uE8B7",
            },
            new AgentInstallConfig
            {
                Agent = TargetAgent.ClaudeCode,
                Name = "Claude Code (@cursor/codex)",
                SkillsPath = ".claude/skills",
                RulesPath = ".claude/rules",
                AgentsPath = ".claude/agents",
                GatePrefix = "C",
                EnvVars = new[] { "CLAUDE_IDE", "CLAUDE_API_KEY" },
                InstallUrl = "https://claude.com/code",
                SupportsMcp = true,
                SupportsRules = true,
                Description = "Anthropic's CLI for coding with Claude",
                Icon = "\uE8B7",
            },
            new AgentInstallConfig
            {
                Agent = TargetAgent.Grok,
                Name = "Grok (x.com/grok)",
                SkillsPath = ".grok/skills",
                RulesPath = ".grok/rules",
                AgentsPath = ".grok/agents",
                GatePrefix = "G",
                EnvVars = new[] { "GROK_API_KEY" },
                InstallUrl = "https://x.com/grok",
                SupportsMcp = false,
                SupportsRules = true,
                Description = "xAI's Grok CLI for coding assistance",
                Icon = "\uE8B7",
            },
            // VSCode Extensions
            new AgentInstallConfig
            {
                Agent = TargetAgent.Cline,
                Name = "Cline",
                SkillsPath = ".cline/skills",
                RulesPath = ".cline/rules",
                AgentsPath = ".cline/agents",
                GatePrefix = "CL",
                EnvVars = new[] { "ANTHROPIC_API_KEY" },
                InstallUrl = "https://marketplace.visualstudio.com/items?itemName=cline.clyde",
                SupportsMcp = true,
                SupportsRules = true,
                Description = "Autonomous coding agent for VSCode",
                Icon = "\uE8B7",
            },
            new AgentInstallConfig
            {
                Agent = TargetAgent.Continue,
                Name = "Continue.dev",
                SkillsPath = ".continue/rules",
                RulesPath = ".continue/rules",
                AgentsPath = ".continue/agents",
                GatePrefix = "CO",
                EnvVars = new[] { "OPENAI_API_KEY" },
                InstallUrl = "https://marketplace.visualstudio.com/items?itemName=Continue.continue",
                SupportsMcp = true,
                SupportsRules = true,
                Description = "Open-source AI coding assistant for VSCode/JetBrains",
                Icon = "\uE8B7",
            },
            // CLI Tools
            new AgentInstallConfig
            {
                Agent = TargetAgent.GeminiCLI,
                Name = "Google Gemini CLI",
                SkillsPath = ".gemini/skills",
                RulesPath = ".gemini/rules",
                AgentsPath = ".gemini/agents",
                GatePrefix = "GM",
                EnvVars = new[] { "GEMINI_API_KEY" },
                InstallUrl = "https://ai.google.dev/gemini-api",
                SupportsMcp = true,
                SupportsRules = true,
                Description = "Google's Gemini CLI for terminal-based coding",
                Icon = "\uE8B7",
            },
            new AgentInstallConfig
            {
                Agent = TargetAgent.KimiCode,
                Name = "Kimi Code AI",
                SkillsPath = ".vibe/skills",
                RulesPath = ".vibe/rules",
                AgentsPath = ".vibe/agents",
                GatePrefix = "KC",
                EnvVars = new[] { "KIMI_API_KEY" },
                InstallUrl = "https://kimi.moonshot.cn",
                SupportsMcp = true,
                SupportsRules = true,
                Description = "Moonshot AI's coding assistant",
                Icon = "\uE8B7",
            },
            new AgentInstallConfig
            {
                Agent = TargetAgent.Aider,
                Name = "Aider",
                SkillsPath = ".aider",
                RulesPath = ".aider",
                AgentsPath = ".aider",
                GatePrefix = "A",
                EnvVars = new[] { "AIDER_MODEL" },
                InstallUrl = "https://aider.chat",
                SupportsMcp = false,
                SupportsRules = true,
                Description = "CLI tool for pair programming with AI",
                Icon = "\uE8B7",
            },
            // Editors with AI
            new AgentInstallConfig
            {
                Agent = TargetAgent.Zed,
                Name = "Zed AI",
                SkillsPath = ".zed",
                RulesPath = ".zed",
                AgentsPath = ".zed/agents",
                GatePrefix = "Z",
                EnvVars = new[] { "ZEDAI_API_KEY" },
                InstallUrl = "https://zed.dev",
                SupportsMcp = false,
                SupportsRules = true,
                Description = "High-performance editor with AI integration",
                Icon = "\uE8B7",
            },
            new AgentInstallConfig
            {
                Agent = TargetAgent.Windsurf,
                Name = "WindSurf",
                SkillsPath = ".windsurf/rules",
                RulesPath = ".windsurf/rules",
                AgentsPath = ".windsurf/workflows",
                GatePrefix = "W",
                EnvVars = new[] { "WINDSURF_API_KEY" },
                InstallUrl = "https://codeium.com/windsurf",
                SupportsMcp = true,
                SupportsRules = true,
                Description = "Codeium's AI-powered IDE",
                Icon = "\uE8B7",
            },
            new AgentInstallConfig
            {
                Agent = TargetAgent.Copilot,
                Name = "GitHub Copilot",
                SkillsPath = ".github/copilot",
                RulesPath = ".github/copilot",
                AgentsPath = ".github/copilot",
                GatePrefix = "CP",
                EnvVars = new[] { "GITHUB_TOKEN" },
                InstallUrl = "https://github.com/features/copilot",
                SupportsMcp = false,
                SupportsRules = true,
                Description = "GitHub's AI pair programmer",
                Icon = "\uE8B7",
            },
            // Roo Code
            new AgentInstallConfig
            {
                Agent = TargetAgent.Roo,
                Name = "Roo Code",
                SkillsPath = ".roo/rules",
                RulesPath = ".roo/rules",
                AgentsPath = ".roo/modes",
                GatePrefix = "R",
                EnvVars = new[] { "OPENAI_API_KEY" },
                InstallUrl = "https://marketplace.visualstudio.com/items?itemName=rooveterinaryinc.roo-cline",
                SupportsMcp = true,
                SupportsRules = true,
                Description = "Flexible AI coding assistant for VSCode",
                Icon = "\uE8B7",
            },
            // Antigravity
            new AgentInstallConfig
            {
                Agent = TargetAgent.Antigravity,
                Name = "Antigravity",
                SkillsPath = ".gemini/skills",
                RulesPath = ".gemini/rules",
                AgentsPath = ".gemini/agents",
                GatePrefix = "AG",
                EnvVars = new[] { "GEMINI_API_KEY" },
                InstallUrl = "https://github.com",
                SupportsMcp = true,
                SupportsRules = true,
                Description = "Next-gen vibe coding tool",
                Icon = "\uE8B7",
            },
        };

    public async Task RunInstallationAsync(SetupConfig config, List<CategorySelection> selections)
        {
            string zipPath = ZipScanner.FindZipPath();
            if (zipPath == null)
                throw new Exception($"Framework archive not found: {ZipScanner.EMBEDDED_ZIP_NAME}");

            string installPath = ResolveInstallPath(config.InstallPath);
            Directory.CreateDirectory(installPath);

            ProgressChanged?.Invoke(10, "Extracting framework files...");
            await ExtractZipAsync(zipPath, installPath, config.ForceOverwrite, selections);

            ProgressChanged?.Invoke(80, "Registering MCP servers...");
            var (mcpOk, mcpMsg) = await SyncMcpConfigAsync(installPath);
            LogAppended?.Invoke(mcpOk ? $"[MCP] {mcpMsg}" : $"[MCP] WARN: {mcpMsg}");

            ProgressChanged?.Invoke(88, "Registering Cursor hooks...");
            var (hooksOk, hooksMsg) = await SyncHooksConfigAsync(installPath);
            LogAppended?.Invoke(hooksOk ? $"[HOOKS] {hooksMsg}" : $"[HOOKS] WARN: {hooksMsg}");

            ProgressChanged?.Invoke(92, "Running post-install scripts...");
            await RunPostInstallScriptsAsync(installPath, config);

            if (config.EnablePostInstallHook)
            {
                ProgressChanged?.Invoke(96, "Generating INDEX.json...");
                await RunPostInstallHookAsync(installPath, config);
            }

            ProgressChanged?.Invoke(100, "Installation complete!");
        }

        string ResolveInstallPath(string path)
        {
            if (!Directory.Exists(path))
                Directory.CreateDirectory(path);

            string autoCursorPath = Path.Combine(path, ".cursor");
            if (!path.EndsWith(".cursor", StringComparison.OrdinalIgnoreCase))
            {
                if (Directory.Exists(autoCursorPath))
                    return autoCursorPath;
                Directory.CreateDirectory(autoCursorPath);
                return autoCursorPath;
            }
            return path;
        }

        async Task ExtractZipAsync(string zipPath, string destDir, bool force, List<CategorySelection> selections, int startPct = 10, int endPct = 85)
        {
            await Task.Run(() =>
            {
                var snapshot = selections.ToDictionary(s => s.Category, s => s.SelectedItems, StringComparer.OrdinalIgnoreCase);
                using var archive = ZipFile.OpenRead(zipPath);
                int total = archive.Entries.Count;
                int current = 0;
                int copied = 0, skipped = 0;

                foreach (var entry in archive.Entries)
                {
                    current++;
                    if (string.IsNullOrEmpty(entry.Name)) continue;

                    if (!ShouldExtract(entry.FullName, snapshot, out string reason))
                    {
                        LogAppended?.Invoke($"[SKIP-CAT] {entry.FullName} ({reason})");
                        int pct = startPct + (int)((current * (double)(endPct - startPct)) / total);
                        ProgressChanged?.Invoke(pct, $"Skipping... {current}/{total}");
                        continue;
                    }

                    string filePath = Path.Combine(destDir, entry.FullName);
                    string dir = Path.GetDirectoryName(filePath)!;
                    if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);

                    bool extract = true;
                    if (File.Exists(filePath) && !force)
                    {
                        // Overwrite empty/stub files left by older installs (e.g. 13-byte rules).
                        long existingLen = new FileInfo(filePath).Length;
                        if (existingLen > 64)
                        {
                            LogAppended?.Invoke($"[SKIP] {entry.FullName}");
                            extract = false;
                            skipped++;
                        }
                    }

                    if (extract)
                    {
                        try
                        {
                            entry.ExtractToFile(filePath, overwrite: true);
                            LogAppended?.Invoke($"[COPY] {entry.FullName}");
                            copied++;
                        }
                        catch (Exception ex)
                        {
                            LogAppended?.Invoke($"[ERROR] {entry.FullName}: {ex.Message}");
                        }
                    }

                    if (current % 10 == 0 || current == total)
                    {
                        int pct = startPct + (int)((current * (double)(endPct - startPct)) / total);
                        ProgressChanged?.Invoke(pct, $"Extracting... {current}/{total}");
                    }
                }
                LogAppended?.Invoke($"---");
                LogAppended?.Invoke($"Summary: {copied} copied, {skipped} skipped");
            });
        }

        bool ShouldExtract(string entryFullName, Dictionary<string, HashSet<string>> snapshot, out string reason)
        {
            reason = "";
            string normalized = entryFullName.Replace('\\', '/');
            var parts = normalized.Split('/');
            if (parts.Length < 2) return true;

            string topCategory = parts[0];
            if (!ZipScanner.CategoryOrder.Any(c => string.Equals(c, topCategory, StringComparison.OrdinalIgnoreCase)))
                return true;

            if (ZipScanner.CoreCategories.Contains(topCategory)) return true;

            if (!snapshot.ContainsKey(topCategory)) { reason = "category not selected"; return false; }
            if (snapshot[topCategory] == null || snapshot[topCategory].Count == 0) { reason = "category empty"; return false; }

            string groupKey = parts[1];
            if (!snapshot[topCategory].Contains(groupKey)) { reason = "group not selected"; return false; }
            return true;
        }

        async Task RunPostInstallScriptsAsync(string installDir, SetupConfig config)
        {
            string scriptsRoot = Path.Combine(installDir, "scripts");
            string workingDir = installDir;
            if (installDir.EndsWith(".cursor", StringComparison.OrdinalIgnoreCase))
                workingDir = Path.GetDirectoryName(installDir) ?? installDir;

            var refs = new[] { config.BuildMemory, config.CompileKnowledge, config.BuildIndex,
                               config.BuildEmbeddings, config.PackageFramework };

            // Timeout per script (seconds) - embedding-builder and packager need more time
            var timeouts = new[] { 120, 180, 120, 300, 180 };

            for (int i = 0; i < refs.Length; i++)
            {
                if (!refs[i]) continue;
                string scriptRel = _buildStepScripts[i];
                string scriptPath = Path.Combine(scriptsRoot, scriptRel);
                if (!File.Exists(scriptPath))
                {
                    LogAppended?.Invoke($"[SKIP] file not found: {scriptPath}");
                    continue;
                }

                LogAppended?.Invoke($"===> {scriptRel}");
                var sw = Stopwatch.StartNew();
                int rc = await RunProcessAsync("powershell.exe",
                    $"-NoProfile -ExecutionPolicy Bypass -File \"{scriptPath}\"",
                    workingDir, timeouts[i]);
                sw.Stop();

                if (rc == 0)
                    LogAppended?.Invoke($"    OK ({sw.Elapsed.TotalSeconds:F1}s)");
                else
                    LogAppended?.Invoke($"    FAILED (exit {rc})");
            }
        }

        async Task RunPostInstallHookAsync(string installDir, SetupConfig config)
        {
            try
            {
                string cmd = string.IsNullOrWhiteSpace(config.PostInstallScript)
                    ? "-m cursor_framework.indexer"
                    : config.PostInstallScript;
                LogAppended?.Invoke($"[hook] post-install: {cmd}");
                int code = await RunProcessAsync("python", $"{cmd} \"{installDir}\"", installDir, 60);
                if (code == 0)
                    LogAppended?.Invoke($"[hook] INDEX.json written");
                else
                    LogAppended?.Invoke($"[hook] indexer exited {code} (non-fatal)");
            }
            catch (Exception ex)
            {
                LogAppended?.Invoke($"[hook] skipped: {ex.Message}");
            }
        }

        public static bool IsCursorRunning()
        {
            return new[] { "Cursor", "Cursor-bin", "cursor", "cursor-bin" }
                .Any(name => Process.GetProcessesByName(name).Length > 0);
        }

        async Task<int> RunProcessAsync(string fileName, string args, string workingDir, int timeoutSec = 120)
        {
            var psi = new ProcessStartInfo(fileName, args)
            {
                WorkingDirectory = workingDir,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                StandardOutputEncoding = Encoding.UTF8,
                StandardErrorEncoding = Encoding.UTF8,
            };

            using var proc = Process.Start(psi);
            if (proc == null) return -1;

            var stdoutTask = proc.StandardOutput.ReadToEndAsync();
            var stderrTask = proc.StandardError.ReadToEndAsync();
            var exitedTask = Task.Run(() => proc.WaitForExit(timeoutSec * 1000));

            var completed = await Task.WhenAny(exitedTask, Task.Delay(timeoutSec * 1000));
            if (completed != exitedTask)
            {
                try { proc.Kill(); } catch { }
                return -1;
            }

            foreach (var line in (await stdoutTask).Split('\n'))
                if (!string.IsNullOrWhiteSpace(line)) LogAppended?.Invoke("    " + line.Trim());
            foreach (var line in (await stderrTask).Split('\n'))
                if (!string.IsNullOrWhiteSpace(line)) LogAppended?.Invoke("    " + line.Trim());

            return proc.ExitCode;
        }

        // ===================== MCP Server Sync =====================

        /// <summary>
        /// Path to global MCP configuration file per target agent.
        /// </summary>
        public static string GetMcpConfigPath(TargetAgent agent = TargetAgent.Cursor)
        {
            string home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            string appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            if (string.IsNullOrEmpty(appData))
                appData = Path.Combine(home, ".config");

            return agent switch
            {
                TargetAgent.Cursor => Path.Combine(home, ".cursor", "mcp.json"),
                TargetAgent.Codex => Path.Combine(home, ".codex", "mcp.json"),
                TargetAgent.ClaudeCode => Path.Combine(home, ".claude", "mcp.json"),
                TargetAgent.Antigravity => Path.Combine(home, ".gemini", "antigravity", "mcp.json"),
                TargetAgent.Windsurf => Path.Combine(home, ".codeium", "windsurf", "mcp_config.json"),
                TargetAgent.Cline => Path.Combine(appData, "Code", "User", "globalStorage", "saoudrizwan.claude-dev", "settings", "cline_mcp_settings.json"),
                TargetAgent.Roo => Path.Combine(appData, "Code", "User", "globalStorage", "rooveterinaryinc.roo-cline", "settings", "cline_mcp_settings.json"),
                _ => Path.Combine(home, ".cursor", "mcp.json"),
            };
        }

        public static string GetMcpConfigPath() => GetMcpConfigPath(TargetAgent.Cursor);

        /// <summary>
        /// Path to global hooks configuration per target agent.
        /// </summary>
        public static string GetHooksConfigPath(TargetAgent agent = TargetAgent.Cursor)
        {
            string home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            return agent switch
            {
                TargetAgent.ClaudeCode => Path.Combine(home, ".claude", "hooks.json"),
                TargetAgent.Antigravity => Path.Combine(home, ".gemini", "antigravity", "hooks.json"),
                _ => Path.Combine(home, ".cursor", "hooks.json"),
            };
        }

        public static string GetHooksConfigPath() => GetHooksConfigPath(TargetAgent.Cursor);

        /// <summary>
        /// Returns true if any of the framework's MCP servers are already registered.
        /// </summary>
        public static bool CheckMcpInstalled(TargetAgent agent = TargetAgent.Cursor)
        {
            try
            {
                string path = GetMcpConfigPath(agent);
                if (!File.Exists(path)) return false;
                using var doc = JsonDocument.Parse(File.ReadAllText(path));
                if (!doc.RootElement.TryGetProperty("mcpServers", out var servers))
                    return false;
                return McpCatalog.Any(entry =>
                    servers.TryGetProperty(entry.ServerKey, out _));
            }
            catch
            {
                return false;
            }
        }

        public static bool CheckMcpInstalled() => CheckMcpInstalled(TargetAgent.Cursor);

        /// <summary>
        /// Build mcpServers entries pointing at packages under {installPath}/mcp/.
        /// </summary>
        static Dictionary<string, object> BuildFrameworkMcpServers(string installPath)
        {
            string mcpRoot = Path.Combine(installPath, "mcp");
            var servers = new Dictionary<string, object>(StringComparer.OrdinalIgnoreCase);

            foreach (var entry in McpCatalog)
            {
                // Handle external MCP servers (vercel, browser) that don't have PackageDir/Module
                if (string.IsNullOrEmpty(entry.PackageDir) || string.IsNullOrEmpty(entry.Module))
                {
                    // Vercel MCP - HTTP endpoint
                    if (entry.ServerKey == "vercel")
                    {
                        servers[entry.ServerKey] = new Dictionary<string, object>
                        {
                            ["url"] = "https://mcp.vercel.com",
                            ["description"] = entry.Description,
                        };
                    }
                    // Browser MCP - npx based
                    else if (entry.ServerKey == "browser")
                    {
                        servers[entry.ServerKey] = new Dictionary<string, object>
                        {
                            ["command"] = "npx",
                            ["args"] = new[] { "-y", "@modelcontextprotocol/server-browser" },
                            ["description"] = entry.Description,
                        };
                    }
                    continue;
                }

                // Local MCP servers (python -m)
                string cwd = Path.Combine(mcpRoot, entry.PackageDir);
                if (!Directory.Exists(cwd))
                {
                    // Fall back to install root if package folder missing (still write entry).
                    cwd = mcpRoot;
                }

                servers[entry.ServerKey] = new Dictionary<string, object>
                {
                    ["command"] = "python",
                    ["args"] = new[] { "-m", entry.Module },
                    ["cwd"] = cwd,
                    ["env"] = new Dictionary<string, string>
                    {
                        ["CURSOR_WORKSPACE_ROOT"] = installPath,
                    },
                    ["description"] = entry.Description,
                };
            }

            return servers;
        }

        /// <summary>
        /// Merge framework servers into existing mcp.json. Always refreshes our keys
        /// (so broken legacy module paths get fixed) while preserving user servers.
        /// </summary>
        static Dictionary<string, object> MergeMcpConfig(
            Dictionary<string, object> existing,
            string installPath)
        {
            var existingServers = new Dictionary<string, object>(StringComparer.OrdinalIgnoreCase);
            if (existing.TryGetValue("mcpServers", out var raw)
                && raw is JsonElement elem
                && elem.ValueKind == JsonValueKind.Object)
            {
                foreach (var prop in elem.EnumerateObject())
                    existingServers[prop.Name] = JsonSerializer.Deserialize<object>(prop.Value.GetRawText())!;
            }
            else if (raw is Dictionary<string, object> dict)
            {
                foreach (var kv in dict) existingServers[kv.Key] = kv.Value;
            }

            foreach (var legacy in LegacyMcpKeys)
                existingServers.Remove(legacy);

            var frameworkServers = BuildFrameworkMcpServers(installPath);
            foreach (var kv in frameworkServers)
                existingServers[kv.Key] = kv.Value;

            existing["mcpServers"] = existingServers;
            existing["version"] = "1.0";
            existing["syncedAt"] = DateTime.UtcNow.ToString("o");
            return existing;
        }

        /// <summary>
        /// Synchronize ~/.cursor/mcp.json with packages under <paramref name="installPath"/>/mcp.
        /// <summary>
        /// Synchronize MCP configuration with packages under <paramref name="installPath"/>/mcp
        /// for the specified target agent.
        /// </summary>
        public async Task<(bool Success, string Message)> SyncMcpConfigAsync(string? installPath = null, TargetAgent agent = TargetAgent.Cursor)
        {
            return await Task.Run(() =>
            {
                try
                {
                    string resolvedInstall = string.IsNullOrWhiteSpace(installPath)
                        ? Path.Combine(
                            Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                            ".cursor")
                        : ResolveInstallPath(installPath);

                    string path = GetMcpConfigPath(agent);
                    string dir = Path.GetDirectoryName(path)!;
                    if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);

                    Dictionary<string, object> existing = new();
                    if (File.Exists(path))
                    {
                        try
                        {
                            string raw = File.ReadAllText(path);
                            if (!string.IsNullOrWhiteSpace(raw))
                            {
                                using var doc = JsonDocument.Parse(raw);
                                existing = JsonSerializer.Deserialize<Dictionary<string, object>>(
                                    doc.RootElement.GetRawText()) ?? new();
                            }
                        }
                        catch (Exception ex)
                        {
                            LogAppended?.Invoke($"[MCP] existing mcp.json unreadable, recreating: {ex.Message}");
                        }
                    }

                    var merged = MergeMcpConfig(existing, resolvedInstall);
                    var opts = new JsonSerializerOptions { WriteIndented = true };
                    string jsonOutput = JsonSerializer.Serialize(merged, opts);
                    File.WriteAllText(path, jsonOutput);
                    LogAppended?.Invoke($"[MCP] synced global agent config: {path}");

                    // Also write local workspace copy
                    try
                    {
                        string localMcp = Path.Combine(resolvedInstall, "mcp.json");
                        File.WriteAllText(localMcp, jsonOutput);
                        LogAppended?.Invoke($"[MCP] synced workspace config: {localMcp}");
                    }
                    catch (Exception ex)
                    {
                        LogAppended?.Invoke($"[MCP] local mcp copy notice: {ex.Message}");
                    }

                    return (true, $"Synced {McpCatalog.Length} MCP servers to {path}");
                }
                catch (Exception ex)
                {
                    LogAppended?.Invoke($"[MCP] sync failed: {ex.Message}");
                    return (false, ex.Message);
                }
            });
        }

        // ===================== Hooks Sync =====================

        /// <summary>
        /// Write/merge hooks.json for the specified target agent.
        /// Registers sessionStart from agent-hooks when the script is present.
        /// </summary>
        public async Task<(bool Success, string Message)> SyncHooksConfigAsync(string? installPath = null, TargetAgent agent = TargetAgent.Cursor)
        {
            return await Task.Run(() =>
            {
                try
                {
                    string resolvedInstall = string.IsNullOrWhiteSpace(installPath)
                        ? Path.Combine(
                            Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                            ".cursor")
                        : ResolveInstallPath(installPath);

                    string hooksPath = GetHooksConfigPath(agent);
                    string cursorHome = Path.GetDirectoryName(hooksPath)!;
                    Directory.CreateDirectory(cursorHome);

                    // Prefer script inside the Cursor user home (where hooks.json lives).
                    string sessionScriptRel = "agent-hooks/session-start.sh";
                    string sessionScriptAbs = Path.Combine(cursorHome, sessionScriptRel.Replace('/', Path.DirectorySeparatorChar));

                    // If install landed elsewhere, copy agent-hooks into ~/.cursor so relative paths work.
                    if (!File.Exists(sessionScriptAbs))
                    {
                        string srcDir = Path.Combine(resolvedInstall, "agent-hooks");
                        string destDir = Path.Combine(cursorHome, "agent-hooks");
                        if (Directory.Exists(srcDir))
                        {
                            CopyDirectory(srcDir, destDir);
                            sessionScriptAbs = Path.Combine(destDir, "session-start.sh");
                        }
                    }

                    var hooksObj = new Dictionary<string, object>(StringComparer.OrdinalIgnoreCase);
                    if (File.Exists(hooksPath))
                    {
                        try
                        {
                            using var doc = JsonDocument.Parse(File.ReadAllText(hooksPath));
                            if (doc.RootElement.TryGetProperty("hooks", out var existingHooks)
                                && existingHooks.ValueKind == JsonValueKind.Object)
                            {
                                foreach (var prop in existingHooks.EnumerateObject())
                                {
                                    hooksObj[prop.Name] = JsonSerializer.Deserialize<object>(prop.Value.GetRawText())!;
                                }
                            }
                        }
                        catch (Exception ex)
                        {
                            LogAppended?.Invoke($"[HOOKS] existing hooks.json unreadable: {ex.Message}");
                        }
                    }

                    if (File.Exists(sessionScriptAbs))
                    {
                        // Cursor user-hook commands are relative to ~/.cursor/
                        hooksObj["sessionStart"] = new object[]
                        {
                            new Dictionary<string, object>
                            {
                                ["command"] = "./agent-hooks/session-start.sh"
                            }
                        };
                    }
                    else
                    {
                        LogAppended?.Invoke("[HOOKS] agent-hooks/session-start.sh not found — hooks map left as-is");
                    }

                    var payload = new Dictionary<string, object>
                    {
                        ["version"] = 1,
                        ["hooks"] = hooksObj,
                        ["syncedAt"] = DateTime.UtcNow.ToString("o"),
                    };

                    var opts = new JsonSerializerOptions { WriteIndented = true };
                    File.WriteAllText(hooksPath, JsonSerializer.Serialize(payload, opts));
                    int count = hooksObj.Count;
                    LogAppended?.Invoke($"[HOOKS] synced {hooksPath} ({count} event(s))");
                    return (true, $"Synced hooks.json ({count} event(s)) to {hooksPath}");
                }
                catch (Exception ex)
                {
                    LogAppended?.Invoke($"[HOOKS] sync failed: {ex.Message}");
                    return (false, ex.Message);
                }
            });
        }

        // ─── Cross-Agent Installation Methods ────────────────────────────────

        /// <summary>
        /// Get all supported agent configurations.
        /// </summary>
        public static IReadOnlyList<AgentInstallConfig> GetAgentCatalog() => AgentCatalog;

        /// <summary>
        /// Get agent configuration by type.
        /// </summary>
        public static AgentInstallConfig? GetAgentConfig(TargetAgent agent)
        {
            foreach (var config in AgentCatalog)
                if (config.Agent == agent) return config;
            return null;
        }

        /// <summary>
        /// Detect which agent is currently running.
        /// </summary>
        public static TargetAgent DetectCurrentAgent()
        {
            if (Environment.GetEnvironmentVariable("CURSOR_IDE") != null ||
                Environment.GetEnvironmentVariable("CURSOR_PROJECT") != null)
                return TargetAgent.Cursor;
            if (Environment.GetEnvironmentVariable("CODEX_ENABLED") != null ||
                Environment.GetEnvironmentVariable("ORIGIN_HOST") != null)
                return TargetAgent.Codex;
            if (Environment.GetEnvironmentVariable("CLAUDE_IDE") != null ||
                Environment.GetEnvironmentVariable("CLAUDE_API_KEY") != null)
                return TargetAgent.ClaudeCode;
            if (Environment.GetEnvironmentVariable("GROK_API_KEY") != null)
                return TargetAgent.Grok;
            return TargetAgent.Cursor; // default to Cursor
        }

        /// <summary>
        /// Get the base path for a specific agent's framework installation.
        /// </summary>
        public static string GetAgentInstallPath(TargetAgent agent, string basePath)
        {
            var config = GetAgentConfig(agent);
            if (config == null) return basePath;

            string agentPath = config.SkillsPath.Split('/')[0]; // e.g. ".cursor", ".claude", ".grok"
            return Path.Combine(basePath, agentPath);
        }

        /// <summary>
        /// Install framework for a specific agent.
        /// </summary>
        public async Task<(bool Success, string Message)> InstallForAgentAsync(
            TargetAgent agent,
            string installBasePath,
            SetupConfig config,
            List<CategorySelection> selections)
        {
            try
            {
                var agentConfig = GetAgentConfig(agent);
                if (agentConfig == null)
                    return (false, $"Unknown agent: {agent}");

                string zipPath = ZipScanner.FindZipPath();
                if (zipPath == null)
                    return (false, "Framework archive not found");

                // Determine install path based on agent
                string installPath;
                if (agent == TargetAgent.Cursor || agent == TargetAgent.Codex)
                {
                    // Cursor and Codex share the same path
                    installPath = ResolveInstallPath(installBasePath);
                }
                else
                {
                    // Claude Code and Grok have separate paths
                    installPath = Path.Combine(installBasePath, agentConfig.SkillsPath.Split('/')[0]);
                    if (!Directory.Exists(installPath))
                        Directory.CreateDirectory(installPath);
                }

                LogAppended?.Invoke($"[AGENT] Installing for {agentConfig.Name}...");
                LogAppended?.Invoke($"[AGENT] Gate prefix: {agentConfig.GatePrefix}");
                LogAppended?.Invoke($"[AGENT] Skills path: {agentConfig.SkillsPath}");
                LogAppended?.Invoke($"[AGENT] Install path: {installPath}");

                // Extract framework files
                ProgressChanged?.Invoke(10, $"Extracting files for {agentConfig.Name}...");
                await ExtractZipAsync(zipPath, installPath, config.ForceOverwrite, selections);

                // Sync MCP for agents that support it
                if (agentConfig.SupportsMcp)
                {
                    ProgressChanged?.Invoke(80, "Syncing MCP servers...");
                    var (mcpOk, mcpMsg) = await SyncMcpConfigAsync(installPath, agentConfig.Agent);
                    LogAppended?.Invoke(mcpOk ? $"[MCP] {mcpMsg}" : $"[MCP] WARN: {mcpMsg}");
                }

                // Sync hooks
                ProgressChanged?.Invoke(88, "Syncing hooks...");
                var (hooksOk, hooksMsg) = await SyncHooksConfigAsync(installPath, agentConfig.Agent);
                LogAppended?.Invoke(hooksOk ? $"[HOOKS] {hooksMsg}" : $"[HOOKS] WARN: {hooksMsg}");

                // Write agent manifest
                var manifestPath = Path.Combine(installPath, "agent-manifest.json");
                var manifest = new Dictionary<string, object>
                {
                    ["agent"] = agentConfig.Agent.ToString().ToLowerInvariant(),
                    ["name"] = agentConfig.Name,
                    ["gate_prefix"] = agentConfig.GatePrefix,
                    ["skills_path"] = agentConfig.SkillsPath,
                    ["rules_path"] = agentConfig.RulesPath,
                    ["agents_path"] = agentConfig.AgentsPath,
                    ["supports_mcp"] = agentConfig.SupportsMcp,
                    ["supports_rules"] = agentConfig.SupportsRules,
                    ["installed_at"] = DateTime.UtcNow.ToString("o"),
                };
                await File.WriteAllTextAsync(manifestPath,
                    JsonSerializer.Serialize(manifest, new JsonSerializerOptions { WriteIndented = true }));
                LogAppended?.Invoke($"[AGENT] Manifest written: {manifestPath}");

                ProgressChanged?.Invoke(100, $"Installation for {agentConfig.Name} complete!");
                return (true, $"Installed for {agentConfig.Name} at {installPath}");
            }
            catch (Exception ex)
            {
                LogAppended?.Invoke($"[AGENT] Installation failed: {ex.Message}");
                return (false, ex.Message);
            }
        }

        /// <summary>
        /// Install framework for all supported agents.
        /// </summary>
        public async Task<(bool Success, string Message)> InstallForAllAgentsAsync(
            string installBasePath,
            SetupConfig config,
            List<CategorySelection> selections)
        {
            var results = new List<(TargetAgent Agent, bool Success, string Message)>();

            foreach (var agentConfig in AgentCatalog)
            {
                LogAppended?.Invoke($"=== Installing for {agentConfig.Name} ===");
                var (success, message) = await InstallForAgentAsync(
                    agentConfig.Agent, installBasePath, config, selections);
                results.Add((agentConfig.Agent, success, message));
                LogAppended?.Invoke($"    Result: {(success ? "OK" : "FAILED")} - {message}");
            }

            int successCount = results.Count(r => r.Success);
            int totalCount = results.Count;
            bool allSuccess = successCount == totalCount;

            string summary = $"Cross-agent installation: {successCount}/{totalCount} agents installed successfully";
            LogAppended?.Invoke($"[AGENT] {summary}");

            return (allSuccess, summary);
        }

        /// <summary>
        /// Get installation status for all agents.
        /// </summary>
        public List<(TargetAgent Agent, bool IsInstalled, string Path)> GetAgentInstallationStatus(string basePath)
        {
            var status = new List<(TargetAgent, bool, string)>();

            foreach (var config in AgentCatalog)
            {
                string agentPath;
                if (config.Agent == TargetAgent.Cursor || config.Agent == TargetAgent.Codex)
                {
                    agentPath = ResolveInstallPath(basePath);
                }
                else
                {
                    agentPath = Path.Combine(basePath, config.SkillsPath.Split('/')[0]);
                }

                string manifestPath = Path.Combine(agentPath, "agent-manifest.json");
                bool installed = File.Exists(manifestPath);

                status.Add((config.Agent, installed, agentPath));
            }

            return status;
        }

        static void CopyDirectory(string sourceDir, string destDir)
        {
            Directory.CreateDirectory(destDir);
            foreach (string file in Directory.GetFiles(sourceDir))
            {
                string dest = Path.Combine(destDir, Path.GetFileName(file));
                File.Copy(file, dest, overwrite: true);
            }
            foreach (string sub in Directory.GetDirectories(sourceDir))
            {
                CopyDirectory(sub, Path.Combine(destDir, Path.GetFileName(sub)));
            }
        }

        /// <summary>
        /// Return the full MCP server status snapshot for the UI.
        /// </summary>
        public List<McpServerStatus> GetMcpStatus(TargetAgent agent = TargetAgent.Cursor)
        {
            var installedKeys = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            DateTime? lastSync = null;
            string path = GetMcpConfigPath(agent);
            try
            {
                if (File.Exists(path))
                {
                    lastSync = File.GetLastWriteTime(path);
                    using var doc = JsonDocument.Parse(File.ReadAllText(path));
                    if (doc.RootElement.TryGetProperty("mcpServers", out var servers)
                        && servers.ValueKind == JsonValueKind.Object)
                    {
                        foreach (var prop in servers.EnumerateObject())
                            installedKeys.Add(prop.Name);
                    }
                }
            }
            catch { /* ignore — just return empty */ }

            var result = new List<McpServerStatus>();
            foreach (var entry in McpCatalog)
            {
                bool registered = installedKeys.Contains(entry.ServerKey);
                result.Add(new McpServerStatus
                {
                    Name = entry.ServerKey,
                    ServerKey = entry.ServerKey,
                    DisplayName = entry.DisplayName,
                    Description = entry.Description,
                    IsInstalled = registered,
                    ToolCount = registered ? entry.Tools.Length : 0,
                    LastSync = lastSync,
                    ConfigPath = path,
                });
            }
            return result;
        }

        /// <summary>
        /// Enumerate all MCP tools that would be exposed after sync.
        /// </summary>
        public List<McpToolEntry> GetMcpTools()
        {
            var list = new List<McpToolEntry>();
            foreach (var entry in McpCatalog)
            {
                foreach (var tool in entry.Tools)
                {
                    list.Add(new McpToolEntry
                    {
                        Name = tool,
                        Server = entry.ServerKey,
                        Description = $"{entry.DisplayName} → {tool}",
                    });
                }
            }
            return list;
        }
    }
}
