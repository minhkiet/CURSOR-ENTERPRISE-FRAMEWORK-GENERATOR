using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
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
                    string dir = Path.GetDirectoryName(filePath);
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
                    workingDir);
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

        async Task<int> RunProcessAsync(string fileName, string args, string workingDir, int timeoutSec = 30)
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
    }
}
