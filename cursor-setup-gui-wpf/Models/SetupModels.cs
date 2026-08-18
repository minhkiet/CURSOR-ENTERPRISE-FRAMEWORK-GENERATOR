using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;

namespace CursorSetupWpf.Models
{
    public class SetupCategory : INotifyPropertyChanged
    {
        private bool _isExpanded = true;
        private int _selectedCount;

        public string Name { get; set; } = "";
        public bool IsCore { get; set; }
        public ObservableCollection<SetupItem> Items { get; set; } = new();

        public bool IsExpanded
        {
            get => _isExpanded;
            set { _isExpanded = value; OnPropertyChanged(nameof(IsExpanded)); }
        }

        public int SelectedCount
        {
            get => _selectedCount;
            set { _selectedCount = value; OnPropertyChanged(nameof(SelectedCount)); }
        }

        public int TotalCount => Items.Count;
        public bool AllSelected => Items.All(i => i.IsSelected);

        public string SelectionLabel => $"{SelectedCount}/{TotalCount}";

        public void UpdateSelection()
        {
            SelectedCount = Items.Count(i => i.IsSelected);
            OnPropertyChanged(nameof(AllSelected));
            OnPropertyChanged(nameof(SelectionLabel));
        }

        public void SelectAll(bool selected)
        {
            foreach (var item in Items)
                item.IsSelected = selected;
            UpdateSelection();
        }

        public event PropertyChangedEventHandler? PropertyChanged;
        protected void OnPropertyChanged(string name) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }

    public class SetupItem : INotifyPropertyChanged
    {
        private bool _isSelected = true;
        private string _description = "";
        public event PropertyChangedEventHandler PropertyChanged;

        public int Index { get; set; }
        public string Name { get; set; } = "";

        public bool IsSelected
        {
            get => _isSelected;
            set { _isSelected = value; PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(IsSelected))); }
        }

        public string Description
        {
            get => _description;
            set { _description = value; PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Description))); }
        }
    }

    public class SetupConfig
    {
        public string InstallPath { get; set; } = "";
        public bool ForceOverwrite { get; set; }
        public bool SkipCursorCheck { get; set; }
        public bool BuildMemory { get; set; }
        public bool CompileKnowledge { get; set; }
        public bool BuildIndex { get; set; }
        public bool BuildEmbeddings { get; set; }
        public bool PackageFramework { get; set; }
        public bool EnablePreScanHook { get; set; } = true;
        public bool EnablePostInstallHook { get; set; } = true;
        public string PreScanScript { get; set; } = "-m cursor_framework.indexer --validate";
        public string PostInstallScript { get; set; } = "-m cursor_framework.indexer";
    }

    public class CategorySelection
    {
        public string Category { get; set; } = "";
        public HashSet<string> SelectedItems { get; set; } = new();
    }

    /// <summary>
    /// Status of an MCP server (framework, autopilot, memory, ...).
    /// Surfaces whether the server is installed and how many tools it provides.
    /// </summary>
    public class McpServerStatus : INotifyPropertyChanged
    {
        private bool _isInstalled;
        private int _toolCount;
        private DateTime? _lastSync;
        private string _configPath = "";
        private string _status = "";

        public string Name { get; set; } = "";
        public string DisplayName { get; set; } = "";
        public string Description { get; set; } = "";
        public string ServerKey { get; set; } = ""; // The key used inside mcp.json

        public bool IsInstalled
        {
            get => _isInstalled;
            set
            {
                if (_isInstalled == value) return;
                _isInstalled = value;
                OnPropertyChanged(nameof(IsInstalled));
                OnPropertyChanged(nameof(StatusIcon));
                OnPropertyChanged(nameof(StatusText));
            }
        }

        public int ToolCount
        {
            get => _toolCount;
            set
            {
                if (_toolCount == value) return;
                _toolCount = value;
                OnPropertyChanged(nameof(ToolCount));
                OnPropertyChanged(nameof(StatusText));
            }
        }

        public DateTime? LastSync
        {
            get => _lastSync;
            set
            {
                if (_lastSync == value) return;
                _lastSync = value;
                OnPropertyChanged(nameof(LastSync));
                OnPropertyChanged(nameof(LastSyncText));
            }
        }

        public string ConfigPath
        {
            get => _configPath;
            set { _configPath = value; OnPropertyChanged(nameof(ConfigPath)); }
        }

        public string Status
        {
            get => _status;
            set
            {
                if (_status == value) return;
                _status = value;
                OnPropertyChanged(nameof(Status));
            }
        }

        public string StatusIcon => IsInstalled ? "\uE73E" : "\uE711"; // check / cancel
        public string StatusText
        {
            get
            {
                if (!IsInstalled) return "Not Installed";
                if (ToolCount > 0) return $"Installed ({ToolCount} tools)";
                return "Installed";
            }
        }
        public string LastSyncText =>
            LastSync.HasValue ? LastSync.Value.ToString("yyyy-MM-dd HH:mm") : "Never";

        public event PropertyChangedEventHandler? PropertyChanged;
        protected void OnPropertyChanged(string name) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }

    /// <summary>
    /// A single MCP tool entry — discovered from tool catalogs.
    /// </summary>
    public class McpToolEntry
    {
        public string Name { get; set; } = "";
        public string Description { get; set; } = "";
        public string Server { get; set; } = "";
    }

    /// <summary>
    /// User preferences persisted to %APPDATA%\\cursor-setup-wpf\\settings.json.
    /// </summary>
    public class AppSettings
    {
        public string Theme { get; set; } = "Indigo"; // Indigo, Light, Dark, System
        public bool AutoStartWithWindows { get; set; }
        public bool NotifyOnComplete { get; set; } = true;
        public bool NotifyOnError { get; set; } = true;
        public string LogFileLocation { get; set; } = "";
        public bool AutoBackupBeforeInstall { get; set; } = true;
        public string BackupLocation { get; set; } = "";
        public string DefaultInstallPath { get; set; } = "";
    }

    /// <summary>
    /// A backup snapshot of framework configuration files.
    /// </summary>
    public class BackupSnapshot
    {
        public string Name { get; set; } = "";
        public string Path { get; set; } = "";
        public DateTime Created { get; set; }
        public long SizeBytes { get; set; }

        public string DisplayLabel =>
            $"{Name}   ·   {Created:yyyy-MM-dd HH:mm}   ·   {FormatSize(SizeBytes)}";

        static string FormatSize(long bytes)
        {
            string[] units = { "B", "KB", "MB", "GB" };
            double size = bytes;
            int unit = 0;
            while (size >= 1024 && unit < units.Length - 1)
            {
                size /= 1024;
                unit++;
            }
            return $"{size:0.#} {units[unit]}";
        }
    }

    /// <summary>
    /// Toast notification entry surfaced by ToastService.
    /// </summary>
    public class ToastNotification : INotifyPropertyChanged
    {
        private double _opacity = 1.0;
        public string Title { get; set; } = "";
        public string Message { get; set; } = "";
        public string Level { get; set; } = "info"; // success, error, info, warning
        public DateTime Created { get; set; } = DateTime.Now;
        public string Glyph => Level switch
        {
            "success" => "\uE73E",
            "error" => "\uE783",
            "warning" => "\uE7BA",
            _ => "\xE946"
        };

        public double Opacity
        {
            get => _opacity;
            set
            {
                if (Math.Abs(_opacity - value) < 0.001) return;
                _opacity = value;
                OnPropertyChanged(nameof(Opacity));
            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;
        protected void OnPropertyChanged(string name) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }
}
