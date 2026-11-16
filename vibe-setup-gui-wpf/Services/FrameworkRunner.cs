#nullable enable
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading.Tasks;

namespace CursorSetupWpf.Services
{
    /// <summary>
    /// Launches cursor_framework CLI commands and optionally opens URLs.
    /// Supports: serve, serve-graph, serve-api, scan, index, warm, stats, graph, dump-graph
    /// </summary>
    public class FrameworkRunner
    {
        public event Action<string>? LogAppended;
        public event Action<string>? OutputReceived;
        public event Action<int>? ProcessExited;

        private Process? _currentProcess;
        private bool _isRunning;

        public bool IsRunning => _isRunning;

        /// <summary>
        /// Result from a framework command execution.
        /// </summary>
        public class RunResult
        {
            public int ExitCode { get; set; }
            public string Output { get; set; } = "";
            public string ErrorOutput { get; set; } = "";
            public TimeSpan Duration { get; set; }
            public bool Success => ExitCode == 0;
        }

        /// <summary>
        /// Known framework commands.
        /// </summary>
        public static readonly (string Name, string DisplayName, string Description, string Icon)[] KnownCommands = new[]
        {
            ("serve", "Dashboard Server", "Start the Dashboard HTTP server on port 8765", "\uE8A5"),
            ("serve-graph", "Graph Visualization", "Start D3 force-directed graph on port 8766", "\uE9D9"),
            ("serve-api", "API Server", "Start Cursor integration API on port 8767", "\uE968"),
            ("scan", "Scan Workspace", "Scan .cursor/ and print INDEX totals", "\uE8B7"),
            ("index", "Build Index", "Scan and write INDEX.json + INDEX.md", "\uE8A1"),
            ("warm", "Warm Cache", "Force full index + memory persist", "\uE898"),
            ("stats", "Statistics", "Print Workflow stats", "\uE9F9"),
            ("graph", "Skill Graph", "Print skill dependency graph as JSON", "\uE9D9"),
            ("dump-graph", "Code Graph", "Dump project code graph to file", "\uE8C8"),
            ("session-stats", "Session Stats", "Show session memory statistics", "\uE7BA"),
            ("session-clear", "Clear Session", "Clear session memory cache", "\uE74D"),
        };

        /// <summary>
        /// Find python executable path.
        /// </summary>
        static string FindPython()
        {
            var candidates = new[]
            {
                "python",
                "python3",
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    "Programs", "Python", "Python311", "python.exe"),
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    "Programs", "Python", "Python310", "python.exe"),
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
                    "Programs", "Python", "Python39", "python.exe"),
            };

            foreach (var c in candidates)
            {
                try
                {
                    var psi = new ProcessStartInfo
                    {
                        FileName = c,
                        Arguments = "--version",
                        UseShellExecute = false,
                        CreateNoWindow = true,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true
                    };
                    using var p = Process.Start(psi);
                    if (p != null)
                    {
                        p.WaitForExit(2000);
                        if (p.ExitCode == 0) return c;
                    }
                }
                catch { }
            }
            return "python";
        }

        /// <summary>
        /// Walk up from a starting directory until we find cursor_framework.
        /// </summary>
        static string ScanUpwardsForFramework(string startDir)
        {
            try
            {
                var dir = Path.GetFullPath(startDir);
                var root = Path.GetPathRoot(dir);
                while (dir != null && !dir.Equals(root, StringComparison.OrdinalIgnoreCase))
                {
                    var candidate = Path.Combine(dir, "cursor_framework");
                    if (Directory.Exists(candidate) &&
                        (File.Exists(Path.Combine(candidate, "__init__.py")) ||
                         File.Exists(Path.Combine(candidate, "__main__.py"))))
                    {
                        return candidate;
                    }
                    dir = Path.GetDirectoryName(dir);
                }
            }
            catch { }
            return "";
        }

        /// <summary>
        /// Try to find cursor_framework relative to a known project structure.
        /// Looks for patterns like: .../cursor_framework/ (same level as cursor-setup-gui-wpf)
        /// </summary>
        static string FindInProjectStructure(string baseDir)
        {
            try
            {
                // Common patterns: project root contains both cursor_framework and cursor-setup-gui-wpf
                // e.g., D:\Projects\Cursor Framework\cursor_framework
                var dirs = new[] {
                    Path.Combine(baseDir, "..", "cursor_framework"),
                    Path.Combine(baseDir, "..", "..", "cursor_framework"),
                    Path.Combine(baseDir, "..", "..", "..", "cursor_framework"),
                    Path.Combine(baseDir, "..", "Cursor Enterprise Framework Generator", "cursor_framework"),
                    Path.Combine(baseDir, "..", "..", "Cursor Enterprise Framework Generator", "cursor_framework"),
                };

                foreach (var d in dirs)
                {
                    var full = Path.GetFullPath(d);
                    if (Directory.Exists(full) &&
                        (File.Exists(Path.Combine(full, "__init__.py")) ||
                         File.Exists(Path.Combine(full, "__main__.py"))))
                    {
                        return full;
                    }
                }
            }
            catch { }
            return "";
        }

        /// <summary>
        /// Find cursor_framework module path by scanning common locations.
        /// Order: installPath/cursor_framework → installPath/../cursor_framework →
        /// ~/.cursor/cursor_framework → AppContext.BaseDirectory/../cursor_framework
        /// → AppContext.BaseDirectory/../../cursor_framework → current directory
        /// </summary>
        static string FindFrameworkModulePath(string installPath)
        {
            var installParent = string.IsNullOrEmpty(installPath)
                ? ""
                : Path.GetDirectoryName(installPath.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar));

            var tryPaths = new List<string>
            {
                // Relative to install path
                Path.Combine(installPath, "cursor_framework"),
                Path.Combine(installParent ?? "", "cursor_framework"),
                // User profile default locations
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                    ".cursor", "cursor_framework"),
                // Relative to AppContext.BaseDirectory (for development builds)
                Path.Combine(AppContext.BaseDirectory, "cursor_framework"),
                Path.Combine(AppContext.BaseDirectory, "..", "cursor_framework"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "cursor_framework"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "cursor_framework"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "cursor_framework"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "cursor_framework"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "..", "..", "cursor_framework"),
                // Current directory and parent directories (for when running from project root)
                Environment.CurrentDirectory,
                Path.Combine(Environment.CurrentDirectory, "cursor_framework"),
                Path.GetFullPath(Path.Combine(Environment.CurrentDirectory, "..")),
                Path.GetFullPath(Path.Combine(Environment.CurrentDirectory, "..", "cursor_framework")),
                Path.GetFullPath(Path.Combine(Environment.CurrentDirectory, "..", "..")),
                Path.GetFullPath(Path.Combine(Environment.CurrentDirectory, "..", "..", "cursor_framework")),
            };

            foreach (var p in tryPaths)
            {
                try
                {
                    var fullPath = Path.GetFullPath(p);
                    if (Directory.Exists(fullPath) &&
                        (File.Exists(Path.Combine(fullPath, "__init__.py")) ||
                         File.Exists(Path.Combine(fullPath, "__main__.py"))))
                        return fullPath;
                }
                catch { }
            }

            // Final fallback: walk up from AppContext.BaseDirectory
            var found = ScanUpwardsForFramework(AppContext.BaseDirectory);
            if (!string.IsNullOrEmpty(found)) return found;

            // Walk up from current directory
            found = ScanUpwardsForFramework(Environment.CurrentDirectory);
            if (!string.IsNullOrEmpty(found)) return found;

            // Try project structure patterns
            found = FindInProjectStructure(AppContext.BaseDirectory);
            if (!string.IsNullOrEmpty(found)) return found;

            return "";
        }

        /// <summary>
        /// Run a cursor_framework command asynchronously with streaming output.
        /// timeoutSec: seconds until timeout (0 = no timeout, for server commands).
        /// </summary>
        public async Task RunCommandAsync(string command, string installPath, int timeoutSec = 60)
        {
            if (_isRunning)
            {
                LogAppended?.Invoke("[FRAMEWORK] A command is already running");
                return;
            }

            _isRunning = true;
            var sw = Stopwatch.StartNew();
            var outputBuilder = new StringBuilder();
            var errorBuilder = new StringBuilder();

            try
            {
                string python = FindPython();
                string modulePath = FindFrameworkModulePath(installPath);

                LogAppended?.Invoke($"[DEBUG] Python: {python}");
                LogAppended?.Invoke($"[DEBUG] Module path: {modulePath ?? "(null)"}");
                LogAppended?.Invoke($"[DEBUG] Install path: {installPath}");

                if (string.IsNullOrEmpty(modulePath))
                {
                    LogAppended?.Invoke("[FRAMEWORK] cursor_framework not found!");
                    OutputReceived?.Invoke($"ERROR: cursor_framework module not found.\nInstall path: {installPath}");
                    return;
                }

                string workingDir = Path.GetDirectoryName(modulePath) ?? installPath;

                // Build Python path to include the framework directory
                var psi = new ProcessStartInfo
                {
                    FileName = python,
                    Arguments = $"-m cursor_framework {command} --root \"{installPath}\"",
                    WorkingDirectory = workingDir,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    StandardOutputEncoding = Encoding.UTF8,
                    StandardErrorEncoding = Encoding.UTF8,
                };

                // Set PYTHONPATH so Python can locate cursor_framework
                var env = psi.Environment;
                env["PYTHONIOENCODING"] = "utf-8";
                env["PYTHONUTF8"] = "1";
                var frameworkParent = Path.GetDirectoryName(modulePath);
                if (!string.IsNullOrEmpty(frameworkParent))
                {
                    var existingPath = env.TryGetValue("PYTHONPATH", out var existing) ? existing : "";
                    env["PYTHONPATH"] = string.IsNullOrEmpty(existingPath)
                        ? frameworkParent
                        : existingPath + Path.PathSeparator + frameworkParent;
                }

                LogAppended?.Invoke($"[FRAMEWORK] Starting: {command}");
                LogAppended?.Invoke($"         {python} -m cursor_framework {command} --root \"{installPath}\"");
                LogAppended?.Invoke($"         PYTHONPATH={env["PYTHONPATH"]}");
                LogAppended?.Invoke($"         CWD={workingDir}");

                _currentProcess = new Process { StartInfo = psi, EnableRaisingEvents = true };
                _currentProcess.OutputDataReceived += (_, e) =>
                {
                    if (!string.IsNullOrEmpty(e.Data))
                    {
                        outputBuilder.AppendLine(e.Data);
                        OutputReceived?.Invoke(e.Data);
                        LogAppended?.Invoke("  " + e.Data);
                    }
                };
                _currentProcess.ErrorDataReceived += (_, e) =>
                {
                    if (!string.IsNullOrEmpty(e.Data))
                    {
                        errorBuilder.AppendLine(e.Data);
                        OutputReceived?.Invoke("[ERROR] " + e.Data);
                        LogAppended?.Invoke("  [ERR] " + e.Data);
                    }
                };

                _currentProcess.Start();
                _currentProcess.BeginOutputReadLine();
                _currentProcess.BeginErrorReadLine();

                // For server commands (timeout=0), wait indefinitely until cancelled
                if (timeoutSec <= 0)
                {
                    await Task.Run(() => _currentProcess.WaitForExit());
                }
                else
                {
                    var exited = await Task.Run(() => _currentProcess.WaitForExit(timeoutSec * 1000));

                    if (!exited)
                    {
                        try { _currentProcess.Kill(); } catch { }
                        LogAppended?.Invoke($"[FRAMEWORK] Timeout after {timeoutSec}s");
                        OutputReceived?.Invoke($"TIMEOUT: Command did not complete within {timeoutSec} seconds.");
                    }
                    else
                    {
                        sw.Stop();
                        var result = new RunResult
                        {
                            ExitCode = _currentProcess.ExitCode,
                            Output = outputBuilder.ToString(),
                            ErrorOutput = errorBuilder.ToString(),
                            Duration = sw.Elapsed,
                        };

                        if (result.Success)
                        {
                            LogAppended?.Invoke($"[FRAMEWORK] Completed in {sw.Elapsed.TotalSeconds:F1}s (exit {result.ExitCode})");
                        }
                        else
                        {
                            LogAppended?.Invoke($"[FRAMEWORK] Failed with exit code {result.ExitCode} after {sw.Elapsed.TotalSeconds:F1}s");
                        }

                        ProcessExited?.Invoke(result.ExitCode);
                    }
                }
            }
            catch (Exception ex)
            {
                sw.Stop();
                LogAppended?.Invoke($"[FRAMEWORK] Error: {ex.Message}");
                OutputReceived?.Invoke($"ERROR: {ex.Message}");
            }
            finally
            {
                _isRunning = false;
                _currentProcess?.Dispose();
                _currentProcess = null;
            }
        }

        /// <summary>
        /// Open a URL in the default browser.
        /// </summary>
        public void OpenBrowser(string url)
        {
            try
            {
                System.Diagnostics.Debug.WriteLine($"[FrameworkRunner] Opening browser: {url}");
                Process.Start(new ProcessStartInfo
                {
                    FileName = url,
                    UseShellExecute = true
                });
                LogAppended?.Invoke($"[FRAMEWORK] Opened browser: {url}");
            }
            catch (Exception ex)
            {
                var msg = $"[FRAMEWORK] Failed to open browser: {ex.Message}";
                System.Diagnostics.Debug.WriteLine(msg);
                LogAppended?.Invoke(msg);
            }
        }

        /// <summary>
        /// Cancel the currently running command.
        /// </summary>
        public void Cancel()
        {
            if (_isRunning && _currentProcess != null)
            {
                try
                {
                    _currentProcess.Kill();
                    LogAppended?.Invoke("[FRAMEWORK] Cancelled by user");
                }
                catch { }
            }
        }

        /// <summary>
        /// Wait for the active process to exit (with timeout). Used by the GUI
        /// after Cancel() so the "Running" banner can flip back.
        /// </summary>
        public bool WaitForExit(TimeSpan timeout)
        {
            try
            {
                if (_currentProcess != null && !_currentProcess.HasExited)
                    return _currentProcess.WaitForExit((int)timeout.TotalMilliseconds);
            }
            catch { }
            return true;
        }
    }
}
