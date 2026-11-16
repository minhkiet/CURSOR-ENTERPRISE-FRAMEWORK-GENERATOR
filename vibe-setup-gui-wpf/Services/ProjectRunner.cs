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
    /// Runs cursor_framework CLI commands for a specific project workspace.
    /// Allows selecting a project folder and executing framework tools on it.
    /// </summary>
    public class ProjectRunner
    {
        public event Action<string>? LogAppended;
        public event Action<string>? OutputReceived;
        public event Action<int>? ProcessExited;

        private Process? _currentProcess;
        private bool _isRunning;

        public bool IsRunning => _isRunning;

        /// <summary>
        /// Project workspace path for running commands.
        /// </summary>
        public string? CurrentProjectPath { get; private set; }

        /// <summary>
        /// Known framework commands with descriptions.
        /// </summary>
        public static readonly (string Name, string DisplayName, string Description, string Icon, string Category)[] KnownCommands = new[]
        {
            // Dashboard commands (servers)
            ("serve", "Dashboard Server", "Start the Dashboard HTTP server", "\uE8A5", "Servers"),
            ("serve-graph", "Graph Visualization", "Start D3 force-directed graph", "\uE9D9", "Servers"),
            ("serve-api", "API Server", "Start Cursor integration API", "\uE968", "Servers"),
            
            // Build commands
            ("scan", "Scan Workspace", "Scan .cursor/ and print INDEX totals", "\uE8B7", "Build"),
            ("index", "Build Index", "Scan and write INDEX.json + INDEX.md", "\uE8A1", "Build"),
            ("warm", "Warm Cache", "Force full index + memory persist", "\uE898", "Build"),
            ("stats", "Statistics", "Print Workflow stats", "\uE9F9", "Build"),
            
            // Graph commands
            ("graph", "Skill Graph", "Print skill dependency graph as JSON", "\uE9D9", "Graph"),
            ("dump-graph", "Code Graph", "Dump project code graph to file", "\uE8C8", "Graph"),
            
            // Session commands
            ("session-stats", "Session Stats", "Show session memory statistics", "\uE7BA", "Session"),
            ("session-clear", "Clear Session", "Clear session memory cache", "\uE74D", "Session"),
        };

        /// <summary>
        /// Available project detection paths.
        /// </summary>
        public static readonly (string Name, string DefaultPath, string Description)[] ProjectPaths = new[]
        {
            ("User .cursor", Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".cursor"), "Global user-level framework"),
            ("Cursor IDE Settings", Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "Cursor", "User", "globalStorage"), "Cursor IDE global storage"),
            ("Current Project", ".cursor", "Project-level .cursor folder (if exists)"),
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
        /// Find cursor_framework module path.
        /// </summary>
        static string FindFrameworkModulePath(string installPath)
        {
            var tryPaths = new List<string>
            {
                Path.Combine(installPath, "cursor_framework"),
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".cursor", "cursor_framework"),
                Path.Combine(AppContext.BaseDirectory, "cursor_framework"),
                Path.Combine(AppContext.BaseDirectory, "..", "cursor_framework"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "cursor_framework"),
                Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "cursor_framework"),
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
            return "";
        }

        /// <summary>
        /// Set the current project path for commands.
        /// </summary>
        public void SetProjectPath(string path)
        {
            CurrentProjectPath = path;
            LogAppended?.Invoke($"[PROJECT] Project path set to: {path}");
        }

        /// <summary>
        /// Detect if a project has a .cursor folder.
        /// </summary>
        public static List<string> DetectProjects(string basePath)
        {
            var projects = new List<string>();
            try
            {
                var searchRoot = Directory.Exists(basePath) ? basePath : Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                
                // Look for .cursor folders
                foreach (var dir in Directory.GetDirectories(searchRoot, "*", SearchOption.TopDirectoryOnly))
                {
                    var cursorDir = Path.Combine(dir, ".cursor");
                    if (Directory.Exists(cursorDir))
                    {
                        projects.Add(dir);
                    }
                }
            }
            catch { }
            return projects;
        }

        /// <summary>
        /// Run a cursor_framework command asynchronously with streaming output.
        /// </summary>
        public async Task RunCommandAsync(string command, string? projectPath = null, int timeoutSec = 60)
        {
            if (_isRunning)
            {
                LogAppended?.Invoke("[PROJECT RUNNER] A command is already running");
                return;
            }

            var targetPath = projectPath ?? CurrentProjectPath ?? Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            _isRunning = true;
            var sw = Stopwatch.StartNew();
            var outputBuilder = new StringBuilder();
            var errorBuilder = new StringBuilder();

            try
            {
                string python = FindPython();
                string modulePath = FindFrameworkModulePath(targetPath);

                LogAppended?.Invoke($"[DEBUG] Python: {python}");
                LogAppended?.Invoke($"[DEBUG] Module path: {modulePath ?? "(null)"}");
                LogAppended?.Invoke($"[DEBUG] Target path: {targetPath}");

                if (string.IsNullOrEmpty(modulePath))
                {
                    LogAppended?.Invoke("[PROJECT RUNNER] cursor_framework not found!");
                    OutputReceived?.Invoke($"ERROR: cursor_framework module not found.\nTarget path: {targetPath}");
                    return;
                }

                string workingDir = Path.GetDirectoryName(modulePath) ?? targetPath;

                var psi = new ProcessStartInfo
                {
                    FileName = python,
                    Arguments = $"-m cursor_framework {command} --root \"{targetPath}\"",
                    WorkingDirectory = workingDir,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    StandardOutputEncoding = Encoding.UTF8,
                    StandardErrorEncoding = Encoding.UTF8,
                };

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

                LogAppended?.Invoke($"[PROJECT RUNNER] Running: {command} on {targetPath}");
                LogAppended?.Invoke($"         {python} -m cursor_framework {command} --root \"{targetPath}\"");

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
                        LogAppended?.Invoke($"[PROJECT RUNNER] Timeout after {timeoutSec}s");
                        OutputReceived?.Invoke($"TIMEOUT: Command did not complete within {timeoutSec} seconds.");
                    }
                    else
                    {
                        sw.Stop();
                        LogAppended?.Invoke($"[PROJECT RUNNER] Completed in {sw.Elapsed.TotalSeconds:F1}s (exit {_currentProcess.ExitCode})");
                        ProcessExited?.Invoke(_currentProcess.ExitCode);
                    }
                }
            }
            catch (Exception ex)
            {
                sw.Stop();
                LogAppended?.Invoke($"[PROJECT RUNNER] Error: {ex.Message}");
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
        /// Run the 'ask' command with a natural language request.
        /// </summary>
        public async Task RunAskAsync(string request, string? projectPath = null, int maxTokens = 4000)
        {
            if (_isRunning)
            {
                LogAppended?.Invoke("[PROJECT RUNNER] A command is already running");
                return;
            }

            var targetPath = projectPath ?? CurrentProjectPath ?? Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            _isRunning = true;
            var sw = Stopwatch.StartNew();
            var outputBuilder = new StringBuilder();

            try
            {
                string python = FindPython();
                string modulePath = FindFrameworkModulePath(targetPath);

                if (string.IsNullOrEmpty(modulePath))
                {
                    LogAppended?.Invoke("[PROJECT RUNNER] cursor_framework not found!");
                    return;
                }

                string workingDir = Path.GetDirectoryName(modulePath) ?? targetPath;

                var psi = new ProcessStartInfo
                {
                    FileName = python,
                    Arguments = $"-m cursor_framework ask \"{request}\" --root \"{targetPath}\" --max-tokens {maxTokens}",
                    WorkingDirectory = workingDir,
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    StandardOutputEncoding = Encoding.UTF8,
                    StandardErrorEncoding = Encoding.UTF8,
                };

                var env = psi.Environment;
                env["PYTHONIOENCODING"] = "utf-8";
                var frameworkParent = Path.GetDirectoryName(modulePath);
                if (!string.IsNullOrEmpty(frameworkParent))
                {
                    var existingPath = env.TryGetValue("PYTHONPATH", out var existing) ? existing : "";
                    env["PYTHONPATH"] = string.IsNullOrEmpty(existingPath)
                        ? frameworkParent
                        : existingPath + Path.PathSeparator + frameworkParent;
                }

                LogAppended?.Invoke($"[PROJECT RUNNER] Asking: \"{request}\"");
                LogAppended?.Invoke($"         max-tokens: {maxTokens}");

                _currentProcess = new Process { StartInfo = psi, EnableRaisingEvents = true };
                _currentProcess.OutputDataReceived += (_, e) =>
                {
                    if (!string.IsNullOrEmpty(e.Data))
                    {
                        outputBuilder.AppendLine(e.Data);
                        OutputReceived?.Invoke(e.Data);
                    }
                };

                _currentProcess.Start();
                _currentProcess.BeginOutputReadLine();

                await Task.Run(() => _currentProcess.WaitForExit(120000));

                sw.Stop();
                LogAppended?.Invoke($"[PROJECT RUNNER] Ask completed in {sw.Elapsed.TotalSeconds:F1}s");
                ProcessExited?.Invoke(_currentProcess.ExitCode);
            }
            catch (Exception ex)
            {
                LogAppended?.Invoke($"[PROJECT RUNNER] Error: {ex.Message}");
            }
            finally
            {
                _isRunning = false;
                _currentProcess?.Dispose();
                _currentProcess = null;
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
                    LogAppended?.Invoke("[PROJECT RUNNER] Cancelled by user");
                }
                catch { }
            }
        }

        /// <summary>
        /// Wait for the active process to exit.
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
