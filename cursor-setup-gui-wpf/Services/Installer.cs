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

        // Known MCP servers. Each entry mirrors the catalog the framework ships with.
        static readonly (string ServerKey, string DisplayName, string Description, string[] Tools)[] McpCatalog = new[]
        {
            (
                "framework",
                "Framework MCP",
                "Cursor Enterprise Framework — rules, skills, agents and command discovery.",
                new[] { "list_rules", "list_skills", "list_agents", "search_knowledge", "validate_setup" }
            ),
            (
                "autopilot",
                "Autopilot MCP",
                "Multi-step task automation and orchestration over the framework catalog.",
                new[] { "run_plan", "stream_progress", "abort_task", "list_workflows" }
            ),
            (
                "memory",
                "Memory MCP",
                "Persistent workspace memory and short-term recall cache for Cursor sessions.",
                new[] { "memory_get", "memory_set", "memory_search", "memory_clear", "memory_index" }
            ),
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

            ProgressChanged?.Invoke(85, "Running post-install scripts...");
            await RunPostInstallScriptsAsync(installPath, config);

            if (config.EnablePostInstallHook)
            {
                ProgressChanged?.Invoke(95, "Generating INDEX.json...");
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
                        LogAppended?.Invoke($"[SKIP] {entry.FullName}");
                        extract = false;
                        skipped++;
                    }

                    if (extract)
                    {
                        try
                        {
                            entry.ExtractToFile(filePath, force);
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
        /// Path to Cursor's global MCP configuration file (per Cursor docs: ~/.cursor/mcp.json).
        /// </summary>
        public static string GetMcpConfigPath()
        {
            string home = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            return Path.Combine(home, ".cursor", "mcp.json");
        }

        /// <summary>
        /// Returns true if any of the framework's MCP servers are already registered.
        /// </summary>
        public static bool CheckMcpInstalled()
        {
            try
            {
                string path = GetMcpConfigPath();
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

        /// <summary>
        /// Build the canonical mcp.json content from the catalog. The exact command/args
        /// are placeholders that match the framework's plugin runner; users can edit
        /// afterwards without losing the keys.
        /// </summary>
        static Dictionary<string, object> BuildDefaultMcpConfig()
        {
            var servers = new Dictionary<string, object>();
            foreach (var entry in McpCatalog)
            {
                servers[entry.ServerKey] = new
                {
                    command = "python",
                    args = new[] { "-m", $"cursor_framework.mcp.{entry.ServerKey}" },
                    env = new Dictionary<string, string>(),
                    description = entry.Description,
                    tools = entry.Tools
                };
            }
            return new Dictionary<string, object>
            {
                ["mcpServers"] = servers,
                ["version"] = "1.0",
                ["syncedAt"] = DateTime.UtcNow.ToString("o"),
            };
        }

        /// <summary>
        /// Merge our default servers with an existing mcp.json so user customizations are preserved.
        /// </summary>
        static Dictionary<string, object> MergeMcpConfig(Dictionary<string, object> existing)
        {
            var defaults = BuildDefaultMcpConfig();
            var existingServers = new Dictionary<string, object>();
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

            if (!defaults.TryGetValue("mcpServers", out var defaultServersObj)
                || defaultServersObj is not Dictionary<string, object> defaultServers)
                return existing;

            foreach (var kv in defaultServers)
                if (!existingServers.ContainsKey(kv.Key))
                    existingServers[kv.Key] = kv.Value;

            existing["mcpServers"] = existingServers;
            existing["version"] = "1.0";
            existing["syncedAt"] = DateTime.UtcNow.ToString("o");
            return existing;
        }

        /// <summary>
        /// Synchronize ~/.cursor/mcp.json with the framework's MCP catalog. Merges
        /// with existing user configuration so any customizations are preserved.
        /// </summary>
        public async Task<(bool Success, string Message)> SyncMcpConfigAsync()
        {
            return await Task.Run(() =>
            {
                try
                {
                    string path = GetMcpConfigPath();
                    string dir = Path.GetDirectoryName(path)!;
                    Directory.CreateDirectory(dir);

                    Dictionary<string, object> existing = new();
                    if (File.Exists(path))
                    {
                        try
                        {
                            string raw = File.ReadAllText(path);
                            if (!string.IsNullOrWhiteSpace(raw))
                            {
                                using var doc = JsonDocument.Parse(raw);
                                existing = JsonSerializer.Deserialize<Dictionary<string, object>>(doc.RootElement.GetRawText()) ?? new();
                            }
                        }
                        catch (Exception ex)
                        {
                            LogAppended?.Invoke($"[MCP] existing mcp.json unreadable, recreating: {ex.Message}");
                        }
                    }

                    var merged = MergeMcpConfig(existing);
                    var opts = new JsonSerializerOptions { WriteIndented = true };
                    File.WriteAllText(path, JsonSerializer.Serialize(merged, opts));
                    LogAppended?.Invoke($"[MCP] synced {path}");
                    return (true, $"Synced {McpCatalog.Length} MCP servers to {path}");
                }
                catch (Exception ex)
                {
                    LogAppended?.Invoke($"[MCP] sync failed: {ex.Message}");
                    return (false, ex.Message);
                }
            });
        }

        /// <summary>
        /// Return the full MCP server status snapshot for the UI.
        /// </summary>
        public List<McpServerStatus> GetMcpStatus()
        {
            var installedKeys = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            DateTime? lastSync = null;
            try
            {
                string path = GetMcpConfigPath();
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
                bool installed = installedKeys.Contains(entry.ServerKey);
                result.Add(new McpServerStatus
                {
                    Name = entry.ServerKey,
                    ServerKey = entry.ServerKey,
                    DisplayName = entry.DisplayName,
                    Description = entry.Description,
                    IsInstalled = installed,
                    ToolCount = installed ? entry.Tools.Length : 0,
                    LastSync = lastSync,
                    ConfigPath = GetMcpConfigPath(),
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
