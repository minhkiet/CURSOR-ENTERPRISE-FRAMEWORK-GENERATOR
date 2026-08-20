#nullable enable
using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Threading.Tasks;
using CursorSetupWpf.Models;

namespace CursorSetupWpf.Services
{
    /// <summary>
    /// Backs up and restores framework configuration files (rules, skills,
    /// agents, hooks, .cursorrules, mcp.json, etc.) as zipped snapshots.
    /// </summary>
    public class BackupService
    {
        public event Action<string>? LogAppended;

        public string GetBackupDirectory(string overridePath = "")
        {
            string dir = string.IsNullOrWhiteSpace(overridePath)
                ? Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
                    "cursor-setup-wpf", "backups")
                : overridePath;
            Directory.CreateDirectory(dir);
            return dir;
        }

        public List<BackupSnapshot> ListBackups(string directory)
        {
            var result = new List<BackupSnapshot>();
            try
            {
                if (!Directory.Exists(directory)) return result;
                foreach (var file in Directory.EnumerateFiles(directory, "*.zip", SearchOption.TopDirectoryOnly))
                {
                    var fi = new FileInfo(file);
                    result.Add(new BackupSnapshot
                    {
                        Name = Path.GetFileNameWithoutExtension(file),
                        Path = file,
                        Created = fi.CreationTime,
                        SizeBytes = fi.Length,
                    });
                }
            }
            catch { /* ignore */ }
            return result.OrderByDescending(b => b.Created).ToList();
        }

        public async Task<BackupSnapshot> CreateBackupAsync(string installPath, string directory)
        {
            return await Task.Run(() =>
            {
                Directory.CreateDirectory(directory);
                string name = $"cursor-setup-{DateTime.Now:yyyyMMdd-HHmmss}.zip";
                string dest = Path.Combine(directory, name);
                if (File.Exists(dest)) File.Delete(dest);

                if (Directory.Exists(installPath))
                {
                    ZipFile.CreateFromDirectory(installPath, dest, CompressionLevel.Optimal, false);
                }
                else
                {
                    // Create an empty marker so the user can see the backup ran.
                    using var fs = File.Create(dest);
                }

                LogAppended?.Invoke($"[BACKUP] created {dest}");

                var fi = new FileInfo(dest);
                return new BackupSnapshot
                {
                    Name = Path.GetFileNameWithoutExtension(dest),
                    Path = dest,
                    Created = fi.CreationTime,
                    SizeBytes = fi.Length,
                };
            });
        }

        public async Task<bool> RestoreBackupAsync(BackupSnapshot snapshot, string installPath)
        {
            return await Task.Run(() =>
            {
                try
                {
                    if (snapshot == null || !File.Exists(snapshot.Path))
                    {
                        LogAppended?.Invoke($"[BACKUP] restore failed: backup not found");
                        return false;
                    }
                    if (Directory.Exists(installPath))
                        Directory.Delete(installPath, true);
                    Directory.CreateDirectory(installPath);
                    ZipFile.ExtractToDirectory(snapshot.Path, installPath, true);
                    LogAppended?.Invoke($"[BACKUP] restored {snapshot.Path} → {installPath}");
                    return true;
                }
                catch (Exception ex)
                {
                    LogAppended?.Invoke($"[BACKUP] restore failed: {ex.Message}");
                    return false;
                }
            });
        }

        public bool DeleteBackup(BackupSnapshot snapshot)
        {
            try
            {
                if (snapshot != null && File.Exists(snapshot.Path))
                {
                    File.Delete(snapshot.Path);
                    return true;
                }
            }
            catch { }
            return false;
        }
    }
}
