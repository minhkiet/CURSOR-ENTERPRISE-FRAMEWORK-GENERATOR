#nullable enable
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CursorSetupWpf.Services;

public sealed record PythonRuntimeInfo(bool IsAvailable, string Command, string Version, string Detail);

public sealed record SkillImportOperationResult(
    string Status,
    string Summary,
    string Output,
    string Runtime,
    string WorkspaceRoot,
    string TargetPath);

/// <summary>
/// Runs the repository's additive-only GitHub skill importer with an explicit
/// interpreter. It never falls back to a shell command that could resolve to a
/// Windows Store shim without first probing the runtime.
/// </summary>
public sealed class GitHubSkillService
{
    private readonly string _applicationDirectory;

    public GitHubSkillService()
    {
        _applicationDirectory = AppContext.BaseDirectory;
    }

    public string FindWorkspaceRoot(string? preferredRoot = null)
    {
        var candidates = new List<string>();
        if (!string.IsNullOrWhiteSpace(preferredRoot)) candidates.Add(preferredRoot);
        candidates.Add(_applicationDirectory);
        candidates.Add(Directory.GetCurrentDirectory());

        foreach (var candidate in candidates)
        {
            var current = SafeFullPath(candidate);
            for (var i = 0; i < 8 && !string.IsNullOrWhiteSpace(current); i++)
            {
                if (File.Exists(Path.Combine(current, "tools", "skill_installer.py")) &&
                    Directory.Exists(Path.Combine(current, "vibe-code-framework")))
                    return current;
                current = Directory.GetParent(current)?.FullName ?? "";
            }
        }

        return SafeFullPath(preferredRoot) ?? SafeFullPath(_applicationDirectory) ?? Directory.GetCurrentDirectory();
    }

    public string GetTargetPath(string workspaceRoot) =>
        Path.Combine(workspaceRoot, "vibe-code-framework", "03-skills");

    public async Task<PythonRuntimeInfo> ProbePythonAsync(string workspaceRoot)
    {
        foreach (var candidate in GetPythonCandidates(workspaceRoot))
        {
            var result = await RunProcessAsync(candidate.FileName, candidate.Arguments,
                workspaceRoot, timeoutMs: 12000);
            if (result.ExitCode == 0 && !string.IsNullOrWhiteSpace(result.Combined))
            {
                var version = result.Combined.Trim().Split('\n', StringSplitOptions.RemoveEmptyEntries).FirstOrDefault() ?? "Python";
                return new PythonRuntimeInfo(true, candidate.DisplayName, version, "Interpreter verified");
            }
        }

        return new PythonRuntimeInfo(
            false,
            "",
            "",
            "No usable Python interpreter was found. A Windows Store shim is not an interpreter.");
    }

    public async Task<SkillImportOperationResult> RunImportAsync(
        string workspaceRoot,
        string repository,
        string skillPath,
        string reference,
        string name,
        bool dryRun)
    {
        workspaceRoot = SafeFullPath(workspaceRoot) ?? "";
        var targetPath = GetTargetPath(workspaceRoot);
        if (!Directory.Exists(workspaceRoot))
            return Blocked("Workspace root does not exist.", workspaceRoot, targetPath);
        if (!Directory.Exists(Path.Combine(workspaceRoot, "vibe-code-framework")))
            return Blocked("Workspace root is not a Resource Hub root; select a directory containing vibe-code-framework.", workspaceRoot, targetPath);

        var scriptPath = Path.Combine(workspaceRoot, "tools", "skill_installer.py");
        if (!File.Exists(scriptPath))
        {
            scriptPath = FindBundledScript();
        }
        if (string.IsNullOrWhiteSpace(scriptPath) || !File.Exists(scriptPath))
            return Blocked("The additive GitHub importer script is not available.", workspaceRoot, targetPath);

        var runtime = await ProbePythonAsync(workspaceRoot);
        if (!runtime.IsAvailable)
            return new SkillImportOperationResult("BLOCKED", runtime.Detail, "", "", workspaceRoot, targetPath);

        var candidate = GetPythonCandidates(workspaceRoot)
            .FirstOrDefault(asyncCandidate => asyncCandidate.DisplayName == runtime.Command);
        if (candidate == null)
            return Blocked("The verified Python command could not be resolved.", workspaceRoot, targetPath);

        var args = new List<string>(candidate.Arguments)
        {
            scriptPath,
            "add-github",
            "--repo", repository,
            "--skill-path", skillPath,
            "--ref", reference,
            "--target", "vibe-code-framework/03-skills",
        };
        if (!string.IsNullOrWhiteSpace(name))
        {
            args.Add("--name");
            args.Add(name);
        }
        if (dryRun) args.Add("--dry-run");

        var process = await RunProcessAsync(candidate.FileName, args, workspaceRoot, timeoutMs: 120000);
        var output = process.Combined.Trim();
        var status = process.ExitCode == 0 ? (dryRun ? "DRY_RUN_PASS" : "IMPORTED") : "FAIL";
        var summary = process.ExitCode == 0
            ? (dryRun ? "Dry-run passed; no files were written." : "Skill imported additively and provenance was recorded.")
            : (string.IsNullOrWhiteSpace(output) ? "The importer returned a non-zero exit code." : output.Split('\n').LastOrDefault() ?? "Import failed.");
        return new SkillImportOperationResult(status, summary, output, runtime.Version, workspaceRoot, targetPath);
    }

    private string FindBundledScript()
    {
        var bundled = Path.Combine(_applicationDirectory, "tools", "skill_installer.py");
        return File.Exists(bundled) ? bundled : "";
    }

    private static SkillImportOperationResult Blocked(string detail, string workspaceRoot, string targetPath) =>
        new("BLOCKED", detail, "", "", workspaceRoot, targetPath);

    private static string? SafeFullPath(string? path)
    {
        if (string.IsNullOrWhiteSpace(path)) return null;
        try { return Path.GetFullPath(path); } catch { return null; }
    }

    private static IEnumerable<PythonCandidate> GetPythonCandidates(string workspaceRoot)
    {
        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var candidates = new List<PythonCandidate>();
        var explicitPath = Environment.GetEnvironmentVariable("PYTHON_EXECUTABLE");
        if (!string.IsNullOrWhiteSpace(explicitPath)) candidates.Add(new(explicitPath, Array.Empty<string>(), explicitPath));

        foreach (var root in new[] { workspaceRoot, AppContext.BaseDirectory })
        {
            foreach (var relative in new[] { @".venv\Scripts\python.exe", @"venv\Scripts\python.exe", @"env\Scripts\python.exe" })
            {
                var path = Path.Combine(root, relative);
                if (File.Exists(path)) candidates.Add(new(path, Array.Empty<string>(), path));
            }
        }

        candidates.Add(new("py", new[] { "-3" }, "py"));
        candidates.Add(new("python", Array.Empty<string>(), "python"));
        return candidates.Where(c => seen.Add(c.DisplayName));
    }

    private static async Task<ProcessResult> RunProcessAsync(
        string fileName,
        IEnumerable<string> arguments,
        string workingDirectory,
        int timeoutMs)
    {
        using var process = new Process
        {
            StartInfo = new ProcessStartInfo
            {
                FileName = fileName,
                WorkingDirectory = Directory.Exists(workingDirectory) ? workingDirectory : AppContext.BaseDirectory,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                StandardOutputEncoding = Encoding.UTF8,
                StandardErrorEncoding = Encoding.UTF8,
            }
        };
        foreach (var argument in arguments) process.StartInfo.ArgumentList.Add(argument);

        try
        {
            if (!process.Start()) return new ProcessResult(-1, "", "Could not start process.");
            var stdout = process.StandardOutput.ReadToEndAsync();
            var stderr = process.StandardError.ReadToEndAsync();
            using var timeout = new System.Threading.CancellationTokenSource(timeoutMs);
            try { await process.WaitForExitAsync(timeout.Token); }
            catch (OperationCanceledException)
            {
                try { process.Kill(entireProcessTree: true); } catch { }
                return new ProcessResult(-1, await stdout, "Process timed out.");
            }
            var output = await stdout;
            var error = await stderr;
            return new ProcessResult(process.ExitCode, output, error);
        }
        catch (Exception ex)
        {
            return new ProcessResult(-1, "", ex.Message);
        }
    }

    private sealed record PythonCandidate(string FileName, IReadOnlyList<string> Arguments, string DisplayName);
    private sealed record ProcessResult(int ExitCode, string Output, string Error)
    {
        public string Combined => string.IsNullOrWhiteSpace(Error) ? Output : $"{Output}\n{Error}";
    }
}
