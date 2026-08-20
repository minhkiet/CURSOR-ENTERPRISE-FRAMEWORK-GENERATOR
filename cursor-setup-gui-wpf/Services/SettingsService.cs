#nullable enable
using System;
using System.IO;
using System.Text.Json;
using CursorSetupWpf.Models;

namespace CursorSetupWpf.Services
{
    /// <summary>
    /// Persists user preferences to %APPDATA%\cursor-setup-wpf\settings.json.
    /// </summary>
    public class SettingsService
    {
        static string SettingsDir =>
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "cursor-setup-wpf");

        static string SettingsPath => Path.Combine(SettingsDir, "settings.json");

        public AppSettings Current { get; private set; } = new();

        public event Action? Changed;

        public void Load()
        {
            try
            {
                if (!File.Exists(SettingsPath)) return;
                string raw = File.ReadAllText(SettingsPath);
                if (string.IsNullOrWhiteSpace(raw)) return;
                var loaded = JsonSerializer.Deserialize<AppSettings>(raw);
                if (loaded != null) Current = loaded;
            }
            catch
            {
                Current = new AppSettings();
            }
        }

        public void Save()
        {
            try
            {
                Directory.CreateDirectory(SettingsDir);
                var opts = new JsonSerializerOptions { WriteIndented = true };
                File.WriteAllText(SettingsPath, JsonSerializer.Serialize(Current, opts));
                Changed?.Invoke();
            }
            catch
            {
                // Best-effort. Settings persistence is not fatal.
            }
        }

        public string DefaultInstallPath =>
            string.IsNullOrWhiteSpace(Current.DefaultInstallPath)
                ? Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".cursor")
                : Current.DefaultInstallPath;

        public string DefaultBackupPath =>
            string.IsNullOrWhiteSpace(Current.BackupLocation)
                ? Path.Combine(SettingsDir, "backups")
                : Current.BackupLocation;

        public string DefaultLogPath =>
            string.IsNullOrWhiteSpace(Current.LogFileLocation)
                ? Path.Combine(SettingsDir, "logs", "setup.log")
                : Current.LogFileLocation;
    }
}
