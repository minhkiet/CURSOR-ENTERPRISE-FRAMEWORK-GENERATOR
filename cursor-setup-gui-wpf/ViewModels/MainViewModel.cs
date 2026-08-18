#nullable enable
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using CursorSetupWpf.Helpers;
using CursorSetupWpf.Models;
using CursorSetupWpf.Services;

namespace CursorSetupWpf.ViewModels
{
    public class MainViewModel : ViewModelBase
    {
        readonly Installer _installer = new();
        readonly SettingsService _settings = new();
        readonly BackupService _backup = new();
        readonly FrameworkRunner _framework = new();
        readonly ToastService _toast = ToastService.Instance;

        // Navigation
        int _selectedNavIndex;
        public int SelectedNavIndex
        {
            get => _selectedNavIndex;
            set => Set(ref _selectedNavIndex, value);
        }

        public ThreadSafeObservableCollection<NavItem> NavItems { get; } = new();
        public ThreadSafeObservableCollection<SetupCategory> ComponentCategories { get; } = new();
        public ThreadSafeObservableCollection<SetupCategory> AdvancedCategories { get; } = new();
        public ThreadSafeObservableCollection<McpServerStatus> McpServers { get; } = new();
        public ThreadSafeObservableCollection<McpToolEntry> McpTools { get; } = new();
        public ThreadSafeObservableCollection<BackupSnapshot> Backups { get; } = new();
        public ThreadSafeObservableCollection<ChangelogEntry> ChangelogEntries { get; } = new();
        public ThreadSafeObservableCollection<ThemeItem> AvailableThemes { get; } = new();
        public ObservableCollection<ToastNotification> Toasts => _toast.Toasts;

        // Strings (bound directly, updated when culture changes)
        public string Str(string key) => LocalizationService.T(key);
        public string VersionChip => "v4.3";

        public string InstallButtonText => LocalizationService.T("btn.install");
        public string LanguageLabel => LocalizationService.T("combobox.lang");
        public string WindowTitle => LocalizationService.T("app.title");
        public string AppBrand => LocalizationService.T("app.title_short");
        public string AppBrandSubtitle => LocalizationService.T("app.subtitle");

        // MCP labels
        public string McpTitle => LocalizationService.T("mcp.title");
        public string McpSubtitle => LocalizationService.T("mcp.subtitle");
        public string McpSyncAllLabel => LocalizationService.T("mcp.sync_all");
        public string McpCheckStatusLabel => LocalizationService.T("mcp.check_status");
        public string McpInstalledLabel => LocalizationService.T("mcp.installed");
        public string McpNotInstalledLabel => LocalizationService.T("mcp.not_installed");
        public string McpOpenConfigLabel => LocalizationService.T("mcp.opening_config");
        public string McpLastSyncLabel =>
            LocalizationService.T("mcp.last_sync",
                McpServers.FirstOrDefault()?.LastSyncText ?? LocalizationService.T("mcp.last_sync_never"));

        // Hooks page labels
        public string HooksPageTitle => LocalizationService.T("hooks.page_title");
        public string HooksPageDesc => LocalizationService.T("hooks.page_desc");
        public string HooksPrescanTitle => LocalizationService.T("hooks.prescan_title");
        public string HooksPrescanDesc => LocalizationService.T("hooks.prescan_desc");
        public string HooksPrescanScriptLabel => LocalizationService.T("hooks.prescan_script_label");
        public string HooksPostinstallTitle => LocalizationService.T("hooks.postinstall_title");
        public string HooksPostinstallDesc => LocalizationService.T("hooks.postinstall_desc");
        public string HooksPostinstallScriptLabel => LocalizationService.T("hooks.postinstall_script_label");
        public string HooksAboutTitle => LocalizationService.T("hooks.about_title");
        public string HooksAboutDesc => LocalizationService.T("hooks.about_desc");

        // Components page labels
        public string ComponentsTitle => LocalizationService.T("components.title");
        public string ComponentsSubtitle => LocalizationService.T("components.subtitle");

        // Advanced page labels
        public string AdvancedTitle => LocalizationService.T("advanced.title");
        public string AdvancedSubtitle => LocalizationService.T("advanced.subtitle");

        // Common button labels
        public string BtnSelectAll => LocalizationService.T("btn.select_all");
        public string BtnDeselectAll => LocalizationService.T("btn.deselect_all");

        // Install page labels
        public string InstallPageTitle => LocalizationService.T("install.page_title");
        public string InstallPageSubtitle => LocalizationService.T("install.page_subtitle");
        public string InstallLocationLabel => LocalizationService.T("install.location");
        public string InstallLocationHint => LocalizationService.T("install.location_hint");
        public string InstallBrowseLabel => LocalizationService.T("install.browse");
        public string InstallNewFolderLabel => LocalizationService.T("install.new_folder");
        public string InstallForceLabel => LocalizationService.T("install.force");
        public string InstallSkipCursorLabel => LocalizationService.T("install.skip_cursor");
        public string InstallBuildOptionsLabel => LocalizationService.T("install.build_options");
        public string InstallOptionalLabel => LocalizationService.T("install.optional");
        public string InstallBuildOptionsDesc => LocalizationService.T("install.build_options_desc");
        public string InstallBuildMemoryLabel => LocalizationService.T("install.build_memory");
        public string InstallCompileKnowledgeLabel => LocalizationService.T("install.compile_knowledge");
        public string InstallBuildIndexLabel => LocalizationService.T("install.build_index");
        public string InstallBuildEmbeddingsLabel => LocalizationService.T("install.build_embeddings");
        public string InstallPackageFrameworkLabel => LocalizationService.T("install.package_framework");
        public string InstallBuildExeNote => LocalizationService.T("install.build_exe_note");
        public string InstallTipLabel => LocalizationService.T("install.tip");

        // Updates labels
        public string UpdatesTitle => LocalizationService.T("updates.title");
        public string UpdatesSubtitle => LocalizationService.T("updates.subtitle");
        public string UpdatesCheckLabel => LocalizationService.T("updates.check");
        public string UpdatesDownloadLabel => LocalizationService.T("updates.download");
        public string UpdatesChangelogLabel => LocalizationService.T("updates.changelog");
        public string UpdatesCurrentVersionLabel => LocalizationService.T("updates.current_version");
        public string UpdatesLatestVersionLabel => LocalizationService.T("updates.latest_version");

        // Backup labels
        public string BackupTitle => LocalizationService.T("backup.title");
        public string BackupSubtitle => LocalizationService.T("backup.subtitle");
        public string BackupCreateLabel => LocalizationService.T("backup.create");
        public string BackupRestoreLabel => LocalizationService.T("backup.restore");
        public string BackupDeleteLabel => LocalizationService.T("backup.delete");
        public string BackupRefreshLabel => LocalizationService.T("backup.refresh");
        public string BackupLocationLabel => LocalizationService.T("backup.location");
        public string BackupBrowseLabel => LocalizationService.T("backup.browse");
        public string BackupAutoLabel => LocalizationService.T("backup.auto");
        public string BackupEmptyLabel => LocalizationService.T("backup.empty");
        public string BackupConfigurationLabel => LocalizationService.T("backup.configuration_label");
        public string BackupSnapshotsLabel => LocalizationService.T("backup.snapshots_label");

        // Settings labels
        public string SettingsTitle => LocalizationService.T("settings.title");
        public string SettingsSubtitle => LocalizationService.T("settings.subtitle");
        public string SettingsThemeLabel => LocalizationService.T("settings.theme");
        public string SettingsAutostartLabel => LocalizationService.T("settings.autostart");
        public string SettingsAutostartDescLabel => LocalizationService.T("settings.autostart_desc");
        public string SettingsNotifyCompleteLabel => LocalizationService.T("settings.notify_complete");
        public string SettingsNotifyErrorLabel => LocalizationService.T("settings.notify_error");
        public string SettingsLogPathLabel => LocalizationService.T("settings.log_path");
        public string SettingsBrowseLabel => LocalizationService.T("settings.browse");
        public string SettingsAppearanceLabel => LocalizationService.T("settings.appearance_label");
        public string SettingsStartupLabel => LocalizationService.T("settings.startup_label");
        public string SettingsNotificationsLabel => LocalizationService.T("settings.notifications_label");
        public string SettingsLoggingLabel => LocalizationService.T("settings.logging_label");
        public string SettingsSaveLabel => LocalizationService.T("settings.save_label");

        // Framework labels
        public string FrameworkTitle => LocalizationService.T("framework.title");
        public string FrameworkSubtitle => LocalizationService.T("framework.subtitle");
        public string BtnStartLabel => LocalizationService.T("btn.start");
        public string BtnOpenLabel => LocalizationService.T("btn.open");
        public string BtnRunLabel => LocalizationService.T("btn.run");
        public string BtnCancelLabel => LocalizationService.T("btn.cancel");
        public string FrameworkDashboardLabel => LocalizationService.T("framework.dashboard");
        public string FrameworkDashboardDesc => LocalizationService.T("framework.dashboard_desc");
        public string FrameworkGraphLabel => LocalizationService.T("framework.graph_viz");
        public string FrameworkGraphDesc => LocalizationService.T("framework.graph_viz_desc");
        public string FrameworkApiLabel => LocalizationService.T("framework.api_server");
        public string FrameworkApiDesc => LocalizationService.T("framework.api_server_desc");
        public string FrameworkScanLabel => LocalizationService.T("framework.scan");
        public string FrameworkScanDesc => LocalizationService.T("framework.scan_desc");
        public string FrameworkIndexLabel => LocalizationService.T("framework.build_index");
        public string FrameworkIndexDesc => LocalizationService.T("framework.build_index_desc");
        public string FrameworkWarmLabel => LocalizationService.T("framework.warm_cache");
        public string FrameworkWarmDesc => LocalizationService.T("framework.warm_cache_desc");
        public string FrameworkStatsLabel => LocalizationService.T("framework.stats");
        public string FrameworkStatsDesc => LocalizationService.T("framework.stats_desc");
        public string FrameworkSkillGraphLabel => LocalizationService.T("framework.skill_graph");
        public string FrameworkSkillGraphDesc => LocalizationService.T("framework.skill_graph_desc");
        public string FrameworkCodeGraphLabel => LocalizationService.T("framework.code_graph");
        public string FrameworkCodeGraphDesc => LocalizationService.T("framework.code_graph_desc");
        public string FrameworkSessionStatsLabel => LocalizationService.T("framework.session_stats");
        public string FrameworkSessionStatsDesc => LocalizationService.T("framework.session_stats_desc");
        public string FrameworkClearSessionLabel => LocalizationService.T("framework.clear_session");
        public string FrameworkClearSessionDesc => LocalizationService.T("framework.clear_session_desc");
        public string FrameworkRunningText => LocalizationService.T("framework.running");
        public string FrameworkServersTitle => LocalizationService.T("framework.dashboard_title");
        public string FrameworkBuildTitle => LocalizationService.T("framework.build_title");
        public string FrameworkGraphTitle => LocalizationService.T("framework.graph_title");
        public string FrameworkAboutTitle => LocalizationService.T("framework.about_title");
        public string FrameworkAboutDesc => LocalizationService.T("framework.about_desc");
        public string FrameworkAboutCommands => LocalizationService.T("framework.about_commands");
        public string FrameworkAboutCommandList => LocalizationService.T("framework.about_command_list");

        // MCP labels
        public string McpDiscoveredToolsLabel => LocalizationService.T("mcp.discovered_tools");

        bool _isFrameworkRunning;
        public bool IsFrameworkRunning { get => _isFrameworkRunning; set { if (Set(ref _isFrameworkRunning, value)) OnPropertyChanged(nameof(IsFrameworkRunning)); } }

        string _runningCommandText = "";
        public string RunningCommandText { get => _runningCommandText; set => Set(ref _runningCommandText, value); }

        // Localization
        ObservableCollection<LanguageItem> _languages = new();
        public ObservableCollection<LanguageItem> Languages => _languages;
        LanguageItem _selectedLanguage;
        public LanguageItem SelectedLanguage
        {
            get => _selectedLanguage;
            set
            {
                if (Set(ref _selectedLanguage, value) && value != null)
                {
                    LocalizationService.SetCulture(value.Code);
                    RefreshStrings();
                }
            }
        }

        // Install path
        string _installPath;
        public string InstallPath
        {
            get => _installPath;
            set
            {
                if (Set(ref _installPath, value))
                    OnPropertyChanged(nameof(CanInstall));
            }
        }

        bool _forceOverwrite;
        public bool ForceOverwrite { get => _forceOverwrite; set => Set(ref _forceOverwrite, value); }

        bool _skipCursorCheck;
        public bool SkipCursorCheck { get => _skipCursorCheck; set => Set(ref _skipCursorCheck, value); }

        bool _buildMemory;
        public bool BuildMemory { get => _buildMemory; set => Set(ref _buildMemory, value); }

        bool _compileKnowledge;
        public bool CompileKnowledge { get => _compileKnowledge; set => Set(ref _compileKnowledge, value); }

        bool _buildIndex;
        public bool BuildIndex { get => _buildIndex; set => Set(ref _buildIndex, value); }

        bool _buildEmbeddings;
        public bool BuildEmbeddings { get => _buildEmbeddings; set => Set(ref _buildEmbeddings, value); }

        bool _packageFramework;
        public bool PackageFramework { get => _packageFramework; set => Set(ref _packageFramework, value); }

        // Hooks
        bool _enablePreScanHook = true;
        public bool EnablePreScanHook { get => _enablePreScanHook; set => Set(ref _enablePreScanHook, value); }

        bool _enablePostInstallHook = true;
        public bool EnablePostInstallHook { get => _enablePostInstallHook; set => Set(ref _enablePostInstallHook, value); }

        string _preScanScript = "-m cursor_framework.indexer --validate";
        public string PreScanScript { get => _preScanScript; set => Set(ref _preScanScript, value); }

        string _postInstallScript = "-m cursor_framework.indexer";
        public string PostInstallScript { get => _postInstallScript; set => Set(ref _postInstallScript, value); }

        // Progress / Status
        int _progressValue;
        public int ProgressValue { get => _progressValue; set => Set(ref _progressValue, value); }

        // Step progress: each step has a fill color and a number/check
        public Brush Step1Fill { get => _step1Fill; set => Set(ref _step1Fill, value); }
        public Brush Step2Fill { get => _step2Fill; set => Set(ref _step2Fill, value); }
        public Brush Step3Fill { get => _step3Fill; set => Set(ref _step3Fill, value); }
        public Brush Step4Fill { get => _step4Fill; set => Set(ref _step4Fill, value); }
        public Brush StepLine1Fill { get => _stepLine1Fill; set => Set(ref _stepLine1Fill, value); }
        public Brush StepLine2Fill { get => _stepLine2Fill; set => Set(ref _stepLine2Fill, value); }
        public Brush StepLine3Fill { get => _stepLine3Fill; set => Set(ref _stepLine3Fill, value); }
        public string Step1Text { get => _step1Text; set => Set(ref _step1Text, value); }
        public string Step2Text { get => _step2Text; set => Set(ref _step2Text, value); }
        public string Step3Text { get => _step3Text; set => Set(ref _step3Text, value); }
        public string Step4Text { get => _step4Text; set => Set(ref _step4Text, value); }
        public string Step1Label { get => _step1Label; set => Set(ref _step1Label, value); }
        public string Step2Label { get => _step2Label; set => Set(ref _step2Label, value); }
        public string Step3Label { get => _step3Label; set => Set(ref _step3Label, value); }
        public string Step4Label { get => _step4Label; set => Set(ref _step4Label, value); }
        Brush _step1Fill = null!;
        Brush _step2Fill = null!;
        Brush _step3Fill = null!;
        Brush _step4Fill = null!;
        Brush _stepLine1Fill = null!;
        Brush _stepLine2Fill = null!;
        Brush _stepLine3Fill = null!;
        string _step1Text = "", _step2Text = "", _step3Text = "", _step4Text = "";
        string _step1Label = "", _step2Label = "", _step3Label = "", _step4Label = "";

        // StatusText
        string _statusKey = "";
        string _statusText = "";
        public string StatusText
        {
            get => !string.IsNullOrEmpty(_statusKey)
                ? LocalizationService.T(_statusKey)
                : _statusText;
            set { _statusKey = ""; Set(ref _statusText, value); }
        }
        void SetStatusKey(string key)
        {
            _statusKey = key;
            _statusText = "";
            OnPropertyChanged(nameof(StatusText));
        }

        string _summaryText = "";
        public string SummaryText { get => _summaryText; set => Set(ref _summaryText, value); }

        bool _isInstalling;
        public bool IsInstalling { get => _isInstalling; set => Set(ref _isInstalling, value); }

        bool _isComplete;
        public bool IsComplete { get => _isComplete; set => Set(ref _isComplete, value); }

        ObservableCollection<string> _logLines = new();
        public ObservableCollection<string> LogLines => _logLines;

        public bool CanInstall => !string.IsNullOrWhiteSpace(InstallPath) && !IsInstalling;

        // ============ MCP-specific computed properties ============
        public int InstalledCount => McpServers.Count(s => s.IsInstalled);
        public int TotalCount => McpServers.Count;
        public string McpConfigPathLabel =>
            LocalizationService.T("mcp.config_path", Installer.GetMcpConfigPath());

        // ============ Updates-specific computed properties ============
        public string CurrentVersion { get; } = "v4.3.0";
        string _latestVersion = "v4.3.0";
        public string LatestVersion { get => _latestVersion; set => Set(ref _latestVersion, value); }
        bool _hasUpdate;
        public bool HasUpdate { get => _hasUpdate; set => Set(ref _hasUpdate, value); }
        DateTime? _lastChecked;
        public DateTime? LastChecked
        {
            get => _lastChecked;
            set { if (Set(ref _lastChecked, value)) OnPropertyChanged(nameof(LastCheckedLabel)); }
        }
        public string LastCheckedLabel =>
            LastChecked.HasValue
                ? LocalizationService.T("updates.last_checked", LastChecked.Value.ToString("yyyy-MM-dd HH:mm"))
                : LocalizationService.T("updates.last_checked_never");
        public string UpdateStatusText => HasUpdate
            ? LocalizationService.T("updates.update_available")
            : LocalizationService.T("updates.up_to_date");

        // ============ Backup-specific properties ============
        string _backupLocation = "";
        public string BackupLocation
        {
            get => _backupLocation;
            set { if (Set(ref _backupLocation, value)) OnPropertyChanged(nameof(HasNoBackups)); }
        }
        bool _autoBackup = true;
        public bool AutoBackup { get => _autoBackup; set => Set(ref _autoBackup, value); }
        public bool HasNoBackups => Backups.Count == 0;

        // ============ Settings-specific properties ============
        ThemeItem _selectedTheme;
        public ThemeItem SelectedTheme { get => _selectedTheme; set => Set(ref _selectedTheme, value); }
        public bool AutoStartWithWindows
        {
            get => _settings.Current.AutoStartWithWindows;
            set { _settings.Current.AutoStartWithWindows = value; OnPropertyChanged(nameof(AutoStartWithWindows)); }
        }
        public bool NotifyOnComplete
        {
            get => _settings.Current.NotifyOnComplete;
            set { _settings.Current.NotifyOnComplete = value; OnPropertyChanged(nameof(NotifyOnComplete)); }
        }
        public bool NotifyOnError
        {
            get => _settings.Current.NotifyOnError;
            set { _settings.Current.NotifyOnError = value; OnPropertyChanged(nameof(NotifyOnError)); }
        }
        public string LogFileLocation
        {
            get => string.IsNullOrWhiteSpace(_settings.Current.LogFileLocation)
                ? _settings.DefaultLogPath
                : _settings.Current.LogFileLocation;
            set { _settings.Current.LogFileLocation = value; OnPropertyChanged(nameof(LogFileLocation)); }
        }

        // ============ Commands ============
        public ICommand BrowseCommand { get; }
        public ICommand NewFolderCommand { get; }
        public ICommand InstallCommand { get; }
        public ICommand CancelCommand { get; }
        public ICommand SelectAllComponentsCommand { get; }
        public ICommand DeselectAllComponentsCommand { get; }
        public ICommand SelectAllAdvancedCommand { get; }
        public ICommand DeselectAllAdvancedCommand { get; }
        public ICommand SyncMcpCommand { get; }
        public ICommand CheckMcpStatusCommand { get; }
        public ICommand OpenMcpConfigCommand { get; }
        public ICommand CheckForUpdatesCommand { get; }
        public ICommand DownloadUpdateCommand { get; }
        public ICommand CreateBackupCommand { get; }
        public ICommand RefreshBackupsCommand { get; }
        public ICommand RestoreBackupCommand { get; }
        public ICommand DeleteBackupCommand { get; }
        public ICommand BrowseBackupLocationCommand { get; }
        public ICommand SaveSettingsCommand { get; }
        public ICommand BrowseLogLocationCommand { get; }
        public ICommand DismissToastCommand { get; }

        // Framework commands
        public ICommand StartDashboardCommand { get; }
        public ICommand StartGraphServerCommand { get; }
        public ICommand StartApiServerCommand { get; }
        public ICommand RunFrameworkScanCommand { get; }
        public ICommand RunFrameworkIndexCommand { get; }
        public ICommand RunFrameworkWarmCommand { get; }
        public ICommand RunFrameworkStatsCommand { get; }
        public ICommand RunFrameworkGraphCommand { get; }
        public ICommand RunFrameworkDumpGraphCommand { get; }
        public ICommand RunFrameworkSessionStatsCommand { get; }
        public ICommand RunFrameworkClearSessionCommand { get; }
        public ICommand OpenBrowserCommand { get; }
        public ICommand CancelFrameworkCommand { get; }

        public MainViewModel()
        {
            // Nav items
            NavItems.Add(new NavItem { Icon = "\uE8B7", TitleKey = "tab.install", Index = 0 });
            NavItems.Add(new NavItem { Icon = "\uE8F1", TitleKey = "tab.components", Index = 1 });
            NavItems.Add(new NavItem { Icon = "\uE713", TitleKey = "tab.advanced", Index = 2 });
            NavItems.Add(new NavItem { Icon = "\uE768", TitleKey = "tab.hooks", Index = 3 });
            NavItems.Add(new NavItem { Icon = "\uE912", TitleKey = "tab.mcp", Index = 4 });
            NavItems.Add(new NavItem { Icon = "\uE777", TitleKey = "tab.updates", Index = 5 });
            NavItems.Add(new NavItem { Icon = "\uE895", TitleKey = "tab.backup", Index = 6 });
            NavItems.Add(new NavItem { Icon = "\uE713", TitleKey = "tab.settings", Index = 7 });
            NavItems.Add(new NavItem { Icon = "\uE82D", TitleKey = "tab.guide", Index = 8 });
            NavItems.Add(new NavItem { Icon = "\uE8F9", TitleKey = "tab.framework", Index = 9 });
            
            _settings.Load();
            _installPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".cursor");
            _backupLocation = _settings.DefaultBackupPath;
            
            // Languages
            _languages.Add(new LanguageItem { Code = "vi", DisplayName = "Tiếng Việt" });
            _languages.Add(new LanguageItem { Code = "en", DisplayName = "English" });
            _selectedLanguage = _languages.First();
            
            // Initialize Commands
            BrowseCommand = new RelayCommand(Browse);
            NewFolderCommand = new RelayCommand(NewFolder);
            InstallCommand = new AsyncRelayCommand(InstallAsync);
            CancelCommand = new RelayCommand(Cancel);

            // Component/Advanced selection commands
            SelectAllComponentsCommand = new RelayCommand(_ => SelectAll(ComponentCategories));
            DeselectAllComponentsCommand = new RelayCommand(_ => DeselectAll(ComponentCategories));
            SelectAllAdvancedCommand = new RelayCommand(_ => SelectAll(AdvancedCategories));
            DeselectAllAdvancedCommand = new RelayCommand(_ => DeselectAll(AdvancedCategories));

            // MCP commands
            SyncMcpCommand = new AsyncRelayCommand(SyncMcpAsync);
            CheckMcpStatusCommand = new RelayCommand(_ => CheckMcpStatus());
            OpenMcpConfigCommand = new RelayCommand(OpenMcpConfig);

            // Updates commands
            CheckForUpdatesCommand = new AsyncRelayCommand(CheckForUpdatesAsync);
            DownloadUpdateCommand = new RelayCommand(DownloadUpdate);

            // Backup commands
            CreateBackupCommand = new AsyncRelayCommand(CreateBackupAsync);
            RefreshBackupsCommand = new RelayCommand(_ => RefreshBackups());
            RestoreBackupCommand = new AsyncRelayCommand(async p => await RestoreBackupAsync(p as BackupSnapshot));
            DeleteBackupCommand = new RelayCommand(DeleteBackup);
            BrowseBackupLocationCommand = new RelayCommand(BrowseBackupLocation);

            // Settings commands
            SaveSettingsCommand = new RelayCommand(SaveSettings);
            BrowseLogLocationCommand = new RelayCommand(BrowseLogLocation);

            // Toast command
            DismissToastCommand = new RelayCommand(DismissToast);

            // Framework server commands (these run indefinitely until cancelled)
            StartDashboardCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("serve", isServer: true));
            StartGraphServerCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("serve-graph", isServer: true));
            StartApiServerCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("serve-api", isServer: true));
            OpenBrowserCommand = new RelayCommand(OpenBrowser);

            // Framework build/utility commands (these complete within timeout)
            RunFrameworkScanCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("scan"));
            RunFrameworkIndexCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("index"));
            RunFrameworkWarmCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("warm"));
            RunFrameworkStatsCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("stats"));
            RunFrameworkGraphCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("graph"));
            RunFrameworkDumpGraphCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("dump-graph"));
            RunFrameworkSessionStatsCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("session-stats"));
            RunFrameworkClearSessionCommand = new AsyncRelayCommand(_ => RunFrameworkCommandAsync("session-clear"));
            CancelFrameworkCommand = new RelayCommand(CancelFramework);

            // Wire FrameworkRunner events → log panel
            _framework.LogAppended += msg => Application.Current?.Dispatcher.Invoke(() =>
            {
                if (string.IsNullOrEmpty(msg)) return;
                LogLines.Add(msg);
                TrimLogLines();
            });
            _framework.ProcessExited += code => Application.Current?.Dispatcher.Invoke(() =>
            {
                IsFrameworkRunning = false;
                RunningCommandText = "";
                LogLines.Add($"[FRAMEWORK] Process exited with code {code}");
                TrimLogLines();
            });

            // Initialize data on startup
            ResetSteps();
            SeedChangelog();
            LoadCategoriesAsync();
            RefreshBackups();
            LoadThemes();
        }

        void Browse(object? _)
        {
            var dialog = new Microsoft.Win32.OpenFolderDialog
            {
                Title = LocalizationService.T("install.location"),
                InitialDirectory = Directory.Exists(InstallPath) ? InstallPath :
                    Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)
            };
            if (dialog.ShowDialog() == true)
            {
                InstallPath = dialog.FolderName;
                LogLines.Add("Selected: " + InstallPath);
            }
        }

        void NewFolder(object? _)
        {
            var dialog = new Microsoft.Win32.OpenFolderDialog
            {
                Title = LocalizationService.T("install.new_folder"),
                InitialDirectory = Directory.Exists(InstallPath) ?
                    Path.GetDirectoryName(InstallPath) :
                    Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)
            };
            if (dialog.ShowDialog() == true)
            {
                var newPath = Path.Combine(dialog.FolderName, ".cursor");
                if (!Directory.Exists(newPath))
                    Directory.CreateDirectory(newPath);
                InstallPath = newPath;
                LogLines.Add("Created: " + newPath);
            }
        }

        async Task InstallAsync(object? _)
        {
            if (IsInstalling) return;
            IsInstalling = true;
            IsComplete = false;
            ProgressValue = 0;
            LogLines.Clear();
            ResetSteps();
            SetActiveStep(1);
            SetStatusKey("log.preparing");

            if (!SkipCursorCheck && Installer.IsCursorRunning())
            {
                var result = MessageBox.Show(
                    LocalizationService.T("log.cursor_running_msg"),
                    LocalizationService.T("log.cursor_running_title"),
                    MessageBoxButton.YesNo, MessageBoxImage.Warning);
                if (result != MessageBoxResult.Yes)
                {
                    LogLines.Add("Cancelled by user");
                    IsInstalling = false;
                    return;
                }
            }

            // Optional pre-install backup
            if (AutoBackup && Directory.Exists(InstallPath))
            {
                try
                {
                    LogLines.Add("[BACKUP] pre-install snapshot…");
                    await _backup.CreateBackupAsync(InstallPath, _backup.GetBackupDirectory(BackupLocation));
                    if (_settings.Current.NotifyOnComplete)
                        _toast.Info(LocalizationService.T("backup.title"),
                            LocalizationService.T("backup.created", DateTime.Now.ToString("HH:mm")));
                }
                catch (Exception ex)
                {
                    LogLines.Add("[BACKUP] skipped: " + ex.Message);
                }
            }

            try
            {
                var selections = BuildSelections();
                var config = BuildConfig();

                LogLines.Add("===========================================");
                LogLines.Add(LocalizationService.T("log.install_header"));
                LogLines.Add("===========================================");
                LogLines.Add(LocalizationService.T("log.install_to", InstallPath));

                SetActiveStep(2);
                await _installer.RunInstallationAsync(config, selections);

                SetActiveStep(3);
                IsComplete = true;
                SetStatusKey("log.complete");
                ProgressValue = 100;
                SetActiveStep(4);

                if (_settings.Current.NotifyOnComplete)
                    _toast.Success(
                        LocalizationService.T("msgbox.complete_title"),
                        LocalizationService.T("msgbox.complete_msg", InstallPath));

                MessageBox.Show(
                    LocalizationService.T("msgbox.complete_msg", InstallPath),
                    LocalizationService.T("msgbox.complete_title"),
                    MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                LogLines.Add("ERROR: " + ex.Message);
                SetStatusKey("scan_failed");
                SetActiveStep(0);
                if (_settings.Current.NotifyOnError)
                    _toast.Error(
                        LocalizationService.T("msgbox.error_title"),
                        ex.Message);
                MessageBox.Show(ex.Message,
                    LocalizationService.T("msgbox.error_title"),
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                IsInstalling = false;
            }
        }

        void Cancel(object? _)
        {
            if (IsInstalling)
            {
                var result = MessageBox.Show(
                    LocalizationService.T("msgbox.cancel_confirm_msg"),
                    LocalizationService.T("msgbox.cancel_confirm_title"),
                    MessageBoxButton.YesNo, MessageBoxImage.Warning);
                if (result != MessageBoxResult.Yes) return;
            }
            Application.Current.Shutdown();
        }

        SetupConfig BuildConfig() => new SetupConfig
        {
            InstallPath = InstallPath,
            ForceOverwrite = ForceOverwrite,
            SkipCursorCheck = SkipCursorCheck,
            BuildMemory = BuildMemory,
            CompileKnowledge = CompileKnowledge,
            BuildIndex = BuildIndex,
            BuildEmbeddings = BuildEmbeddings,
            PackageFramework = PackageFramework,
            EnablePreScanHook = EnablePreScanHook,
            EnablePostInstallHook = EnablePostInstallHook,
            PreScanScript = PreScanScript,
            PostInstallScript = PostInstallScript,
        };

        List<CategorySelection> BuildSelections()
        {
            var result = new List<CategorySelection>();
            foreach (var cat in ComponentCategories.Concat(AdvancedCategories))
            {
                var sel = new CategorySelection
                {
                    Category = cat.Name,
                    SelectedItems = new HashSet<string>(
                        cat.Items.Where(i => i.IsSelected).Select(i => i.Name),
                        StringComparer.OrdinalIgnoreCase)
                };
                if (ZipScanner.CoreCategories.Contains(cat.Name) && sel.SelectedItems.Count == 0)
                {
                    sel.SelectedItems = new HashSet<string>(
                        cat.Items.Select(i => i.Name), StringComparer.OrdinalIgnoreCase);
                }
                result.Add(sel);
            }
            return result;
        }

        void SelectAll(IEnumerable<SetupCategory> cats)
        {
            foreach (var cat in cats)
                if (!cat.IsCore)
                    cat.SelectAll(true);
        }

        void DeselectAll(IEnumerable<SetupCategory> cats)
        {
            foreach (var cat in cats)
                if (!cat.IsCore)
                    cat.SelectAll(false);
        }

        async void LoadCategoriesAsync()
        {
            string zipPath = ZipScanner.FindZipPath();
            if (zipPath == null)
            {
                LogLines.Add("ERROR: " + LocalizationService.T("scan_archive_not_found"));
                LogLines.Add(LocalizationService.T("place_zip_hint"));
                return;
            }

            SetStatusKey("scanning");
            LogLines.Add("Scanning: " + zipPath);

            var items = await Task.Run(() => ZipScanner.ScanCategories(zipPath));

            // Extract descriptions in background, then update UI
            await Task.Run(() =>
            {
                var compCats = new[] { "rules", "skills", "agents", "commands", "hooks", "knowledge" };
                foreach (var catName in compCats)
                    PrepareCategory(catName, items, ComponentCategories);

                var advCats = new[] { "prompts", "references", "workflows", "templates", "memory", "scripts" };
                foreach (var catName in advCats)
                    PrepareCategory(catName, items, AdvancedCategories);
            });

            UpdateSummary();
            SetStatusKey("ready_to_install");
            LogLines.Add(LocalizationService.T("scanned_log", items.Count));
        }

        void PrepareCategory(string catName, Dictionary<string, List<string>> items, ObservableCollection<SetupCategory> target)
        {
            var cat = new SetupCategory
            {
                Name = catName,
                IsCore = ZipScanner.CoreCategories.Contains(catName),
                IsExpanded = true
            };

            if (items.TryGetValue(catName, out var groups))
            {
                string zipPath = ZipScanner.FindZipPath();
                int idx = 1;
                foreach (var group in groups.OrderBy(g => g, StringComparer.OrdinalIgnoreCase))
                {
                    string desc = zipPath != null
                        ? ZipScanner.ExtractDescription(zipPath, catName, group) : "";
                    cat.Items.Add(new SetupItem
                    {
                        Index = idx++,
                        Name = group,
                        Description = desc,
                        IsSelected = true
                    });
                }
            }

            cat.PropertyChanged += (_, e) =>
            {
                if (e.PropertyName == nameof(SetupCategory.SelectedCount))
                    UpdateSummary();
            };

            cat.UpdateSelection();
            Application.Current?.Dispatcher.Invoke(() => target.Add(cat));
        }

        void UpdateSummary()
        {
            int total = ComponentCategories.Sum(c => c.TotalCount) + AdvancedCategories.Sum(c => c.TotalCount);
            int selected = ComponentCategories.Sum(c => c.SelectedCount) + AdvancedCategories.Sum(c => c.SelectedCount);
            SummaryText = LocalizationService.T("summary.components", selected, total);
        }

        // ============ MCP Sync ============
        async Task SyncMcpAsync()
        {
            SetStatusKey("scanning");
            var (success, message) = await _installer.SyncMcpConfigAsync();
            if (success)
            {
                _toast.Success(LocalizationService.T("mcp.title"),
                    LocalizationService.T("mcp.sync_success", McpCatalog.Count));
                LogLines.Add("[MCP] " + message);
            }
            else
            {
                _toast.Error(LocalizationService.T("mcp.title"),
                    LocalizationService.T("mcp.sync_failed", message));
            }
            CheckMcpStatus();
        }

        Task CheckMcpStatusAsync()
        {
            CheckMcpStatus();
            return Task.CompletedTask;
        }

        void CheckMcpStatus()
        {
            var statuses = _installer.GetMcpStatus();
            var tools = _installer.GetMcpTools();
            Application.Current?.Dispatcher.Invoke(() =>
            {
                McpServers.Clear();
                foreach (var s in statuses) McpServers.Add(s);
                McpTools.Clear();
                foreach (var t in tools) McpTools.Add(t);
                OnPropertyChanged(nameof(InstalledCount));
                OnPropertyChanged(nameof(TotalCount));
                OnPropertyChanged(nameof(McpConfigPathLabel));
                OnPropertyChanged(nameof(McpLastSyncLabel));
            });
        }

        void OpenMcpConfig(object? arg)
        {
            string path = arg as string ?? Installer.GetMcpConfigPath();
            try
            {
                if (File.Exists(path))
                {
                    Process.Start(new ProcessStartInfo
                    {
                        FileName = path,
                        UseShellExecute = true,
                    });
                    _toast.Info(LocalizationService.T("mcp.title"),
                        LocalizationService.T("mcp.opening_config"));
                }
                else
                {
                    _toast.Warning(LocalizationService.T("mcp.title"),
                        LocalizationService.T("mcp.not_installed"));
                }
            }
            catch (Exception ex)
            {
                _toast.Error(LocalizationService.T("mcp.title"), ex.Message);
            }
        }

        // ============ Updates ============
        async Task CheckForUpdatesAsync()
        {
            SetStatusKey("scanning");
            // Simulated update check — wire up to a real feed when available.
            await Task.Delay(700);
            LatestVersion = CurrentVersion;
            HasUpdate = false;
            LastChecked = DateTime.Now;
            _toast.Success(LocalizationService.T("updates.title"),
                LocalizationService.T("updates.up_to_date"));
        }

        // ============ Framework Tools ============
        async Task RunFrameworkCommandAsync(string command, bool isServer = false)
        {
            if (IsFrameworkRunning)
            {
                _toast.Warning(FrameworkTitle, LocalizationService.T("framework.running_note"));
                return;
            }

            IsFrameworkRunning = true;
            RunningCommandText = $"{FrameworkRunningText} {command}";

            try
            {
                // Server commands run indefinitely, others complete within timeout
                int timeout = isServer ? 0 : 60;
                await _framework.RunCommandAsync(command, InstallPath, timeout);
            }
            catch (Exception ex)
            {
                _toast.Error(FrameworkTitle, ex.Message);
                LogLines.Add("[FRAMEWORK] Error: " + ex.Message);
            }
            finally
            {
                // Servers (timeout=0) reset IsFrameworkRunning only via CancelFramework /
                // ProcessExited. Short-running commands finish and flip the flag here.
                if (!isServer)
                {
                    IsFrameworkRunning = false;
                    RunningCommandText = "";
                }
            }
        }

        void TrimLogLines()
        {
            const int MaxLines = 500;
            if (LogLines.Count > MaxLines)
            {
                Application.Current?.Dispatcher.Invoke(() =>
                {
                    while (LogLines.Count > MaxLines)
                        LogLines.RemoveAt(0);
                });
            }
        }

        void DownloadUpdate(object? _)
        {
            if (!HasUpdate) return;
            _toast.Info(LocalizationService.T("updates.title"),
                LocalizationService.T("updates.download_started"));
        }

        void SeedChangelog()
        {
            ChangelogEntries.Clear();
            ChangelogEntries.Add(new ChangelogEntry
            {
                Version = "v4.3.0",
                Date = new DateTime(2026, 7, 22),
                Description = "MCP server sync, glassmorphic UI, toast notifications and tabbed navigation."
            });
            ChangelogEntries.Add(new ChangelogEntry
            {
                Version = "v4.2.0",
                Date = new DateTime(2026, 5, 12),
                Description = "Embeddings builder, multi-language vi/en and modernized indigo theme."
            });
            ChangelogEntries.Add(new ChangelogEntry
            {
                Version = "v4.1.0",
                Date = new DateTime(2026, 3, 1),
                Description = "Hooks page, knowledge compiler and pre-scan validator."
            });
        }

        // ============ Backup ============
        async Task CreateBackupAsync()
        {
            try
            {
                var snap = await _backup.CreateBackupAsync(InstallPath, _backup.GetBackupDirectory(BackupLocation));
                RefreshBackups();
                _toast.Success(LocalizationService.T("backup.title"),
                    LocalizationService.T("backup.created", snap.Created.ToString("HH:mm")));
            }
            catch (Exception ex)
            {
                _toast.Error(LocalizationService.T("backup.title"), ex.Message);
            }
        }

        void RefreshBackups()
        {
            Backups.Clear();
            foreach (var b in _backup.ListBackups(_backup.GetBackupDirectory(BackupLocation)))
                Backups.Add(b);
            OnPropertyChanged(nameof(HasNoBackups));
        }

        void LoadThemes()
        {
            AvailableThemes.Clear();
            AvailableThemes.Add(new ThemeItem { Code = "Indigo", DisplayName = "Indigo" });
            AvailableThemes.Add(new ThemeItem { Code = "Slate", DisplayName = "Slate" });
            AvailableThemes.Add(new ThemeItem { Code = "Emerald", DisplayName = "Emerald" });
            AvailableThemes.Add(new ThemeItem { Code = "Rose", DisplayName = "Rose" });

            // Set default selection
            _selectedTheme = AvailableThemes.FirstOrDefault(t => t.Code == _settings.Current.Theme)
                ?? AvailableThemes.First();
            OnPropertyChanged(nameof(SelectedTheme));
        }

        async Task RestoreBackupAsync(BackupSnapshot? snapshot)
        {
            if (snapshot == null) return;
            var confirm = MessageBox.Show(
                LocalizationService.T("backup.restore_confirm_msg"),
                LocalizationService.T("backup.restore_confirm_title"),
                MessageBoxButton.YesNo, MessageBoxImage.Question);
            if (confirm != MessageBoxResult.Yes) return;

            try
            {
                bool ok = await _backup.RestoreBackupAsync(snapshot, InstallPath);
                if (ok)
                    _toast.Success(LocalizationService.T("backup.title"),
                        LocalizationService.T("backup.restored"));
            }
            catch (Exception ex)
            {
                _toast.Error(LocalizationService.T("backup.title"), ex.Message);
            }
        }

        void DeleteBackup(object? arg)
        {
            if (arg is not BackupSnapshot snap) return;
            var confirm = MessageBox.Show(
                LocalizationService.T("backup.delete_confirm_msg"),
                LocalizationService.T("backup.delete_confirm_title"),
                MessageBoxButton.YesNo, MessageBoxImage.Question);
            if (confirm != MessageBoxResult.Yes) return;
            if (_backup.DeleteBackup(snap))
                RefreshBackups();
        }

        void BrowseBackupLocation(object? _)
        {
            var dialog = new Microsoft.Win32.OpenFolderDialog
            {
                Title = LocalizationService.T("backup.location"),
                InitialDirectory = Directory.Exists(BackupLocation) ? BackupLocation :
                    Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)
            };
            if (dialog.ShowDialog() == true)
                BackupLocation = dialog.FolderName;
        }

        // ============ Settings ============
        void SaveSettings(object? _)
        {
            try
            {
                _settings.Current.Theme = SelectedTheme?.Code ?? "Indigo";
                _settings.Current.BackupLocation = BackupLocation;
                _settings.Current.AutoBackupBeforeInstall = AutoBackup;
                _settings.Current.DefaultInstallPath = InstallPath;
                _settings.Save();
                _toast.Success(LocalizationService.T("settings.title"),
                    LocalizationService.T("settings.saved"));
            }
            catch (Exception ex)
            {
                _toast.Error(LocalizationService.T("settings.title"), ex.Message);
            }
        }

        void BrowseLogLocation(object? _)
        {
            var dialog = new Microsoft.Win32.OpenFolderDialog
            {
                Title = LocalizationService.T("settings.log_path"),
                InitialDirectory = Directory.Exists(LogFileLocation) ? Path.GetDirectoryName(LogFileLocation) :
                    Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)
            };
            if (dialog.ShowDialog() == true)
                LogFileLocation = Path.Combine(dialog.FolderName, "setup.log");
        }

        void RefreshStrings()
        {
            OnPropertyChanged(nameof(VersionChip));
            OnPropertyChanged(nameof(SelectedNavIndex));
            foreach (var nav in NavItems)
                nav.RefreshTitle();
            OnPropertyChanged(nameof(Step1Label));
            OnPropertyChanged(nameof(Step2Label));
            OnPropertyChanged(nameof(Step3Label));
            OnPropertyChanged(nameof(Step4Label));
            OnPropertyChanged(nameof(InstallButtonText));
            OnPropertyChanged(nameof(LanguageLabel));
            OnPropertyChanged(nameof(WindowTitle));
            OnPropertyChanged(nameof(AppBrand));
            OnPropertyChanged(nameof(AppBrandSubtitle));
            OnPropertyChanged(nameof(CanInstall));
            OnPropertyChanged(nameof(StatusText));
            OnPropertyChanged(nameof(SummaryText));

            // MCP / Updates / Backup / Settings labels
            OnPropertyChanged(nameof(McpTitle));
            OnPropertyChanged(nameof(McpSubtitle));
            OnPropertyChanged(nameof(McpSyncAllLabel));
            OnPropertyChanged(nameof(McpCheckStatusLabel));
            OnPropertyChanged(nameof(McpInstalledLabel));
            OnPropertyChanged(nameof(McpNotInstalledLabel));
            OnPropertyChanged(nameof(McpOpenConfigLabel));
            OnPropertyChanged(nameof(McpConfigPathLabel));
            OnPropertyChanged(nameof(McpLastSyncLabel));

            OnPropertyChanged(nameof(UpdatesTitle));
            OnPropertyChanged(nameof(UpdatesSubtitle));
            OnPropertyChanged(nameof(UpdatesCheckLabel));
            OnPropertyChanged(nameof(UpdatesDownloadLabel));
            OnPropertyChanged(nameof(UpdatesChangelogLabel));
            OnPropertyChanged(nameof(UpdatesCurrentVersionLabel));
            OnPropertyChanged(nameof(UpdatesLatestVersionLabel));
            OnPropertyChanged(nameof(LastCheckedLabel));
            OnPropertyChanged(nameof(UpdateStatusText));

            OnPropertyChanged(nameof(BackupTitle));
            OnPropertyChanged(nameof(BackupSubtitle));
            OnPropertyChanged(nameof(BackupCreateLabel));
            OnPropertyChanged(nameof(BackupRestoreLabel));
            OnPropertyChanged(nameof(BackupDeleteLabel));
            OnPropertyChanged(nameof(BackupRefreshLabel));
            OnPropertyChanged(nameof(BackupLocationLabel));
            OnPropertyChanged(nameof(BackupBrowseLabel));
            OnPropertyChanged(nameof(BackupAutoLabel));
            OnPropertyChanged(nameof(BackupEmptyLabel));

            OnPropertyChanged(nameof(SettingsTitle));
            OnPropertyChanged(nameof(SettingsSubtitle));
            OnPropertyChanged(nameof(SettingsThemeLabel));
            OnPropertyChanged(nameof(SettingsAutostartLabel));
            OnPropertyChanged(nameof(SettingsAutostartDescLabel));
            OnPropertyChanged(nameof(SettingsNotifyCompleteLabel));
            OnPropertyChanged(nameof(SettingsNotifyErrorLabel));
            OnPropertyChanged(nameof(SettingsLogPathLabel));
            OnPropertyChanged(nameof(SettingsBrowseLabel));

            OnPropertyChanged(nameof(FrameworkTitle));
            OnPropertyChanged(nameof(FrameworkSubtitle));
            OnPropertyChanged(nameof(BtnStartLabel));
            OnPropertyChanged(nameof(BtnOpenLabel));
            OnPropertyChanged(nameof(BtnRunLabel));
            OnPropertyChanged(nameof(BtnCancelLabel));
            OnPropertyChanged(nameof(FrameworkDashboardLabel));
            OnPropertyChanged(nameof(FrameworkDashboardDesc));
            OnPropertyChanged(nameof(FrameworkGraphLabel));
            OnPropertyChanged(nameof(FrameworkGraphDesc));
            OnPropertyChanged(nameof(FrameworkApiLabel));
            OnPropertyChanged(nameof(FrameworkApiDesc));
            OnPropertyChanged(nameof(FrameworkScanLabel));
            OnPropertyChanged(nameof(FrameworkScanDesc));
            OnPropertyChanged(nameof(FrameworkIndexLabel));
            OnPropertyChanged(nameof(FrameworkIndexDesc));
            OnPropertyChanged(nameof(FrameworkWarmLabel));
            OnPropertyChanged(nameof(FrameworkWarmDesc));
            OnPropertyChanged(nameof(FrameworkStatsLabel));
            OnPropertyChanged(nameof(FrameworkStatsDesc));
            OnPropertyChanged(nameof(FrameworkSkillGraphLabel));
            OnPropertyChanged(nameof(FrameworkSkillGraphDesc));
            OnPropertyChanged(nameof(FrameworkCodeGraphLabel));
            OnPropertyChanged(nameof(FrameworkCodeGraphDesc));
            OnPropertyChanged(nameof(FrameworkSessionStatsLabel));
            OnPropertyChanged(nameof(FrameworkSessionStatsDesc));
            OnPropertyChanged(nameof(FrameworkClearSessionLabel));
            OnPropertyChanged(nameof(FrameworkClearSessionDesc));
            OnPropertyChanged(nameof(FrameworkServersTitle));
            OnPropertyChanged(nameof(FrameworkBuildTitle));
            OnPropertyChanged(nameof(FrameworkGraphTitle));
            OnPropertyChanged(nameof(FrameworkAboutTitle));
            OnPropertyChanged(nameof(FrameworkAboutDesc));
            OnPropertyChanged(nameof(FrameworkAboutCommands));
            OnPropertyChanged(nameof(FrameworkAboutCommandList));

            OnPropertyChanged(nameof(McpDiscoveredToolsLabel));

            // Hooks page
            OnPropertyChanged(nameof(HooksPageTitle));
            OnPropertyChanged(nameof(HooksPageDesc));
            OnPropertyChanged(nameof(HooksPrescanTitle));
            OnPropertyChanged(nameof(HooksPrescanDesc));
            OnPropertyChanged(nameof(HooksPrescanScriptLabel));
            OnPropertyChanged(nameof(HooksPostinstallTitle));
            OnPropertyChanged(nameof(HooksPostinstallDesc));
            OnPropertyChanged(nameof(HooksPostinstallScriptLabel));
            OnPropertyChanged(nameof(HooksAboutTitle));
            OnPropertyChanged(nameof(HooksAboutDesc));

            OnPropertyChanged(nameof(ComponentsTitle));
            OnPropertyChanged(nameof(ComponentsSubtitle));
            OnPropertyChanged(nameof(AdvancedTitle));
            OnPropertyChanged(nameof(AdvancedSubtitle));
            OnPropertyChanged(nameof(BtnSelectAll));
            OnPropertyChanged(nameof(BtnDeselectAll));

            // Install page
            OnPropertyChanged(nameof(InstallPageTitle));
            OnPropertyChanged(nameof(InstallPageSubtitle));
            OnPropertyChanged(nameof(InstallLocationLabel));
            OnPropertyChanged(nameof(InstallLocationHint));
            OnPropertyChanged(nameof(InstallBrowseLabel));
            OnPropertyChanged(nameof(InstallNewFolderLabel));
            OnPropertyChanged(nameof(InstallForceLabel));
            OnPropertyChanged(nameof(InstallSkipCursorLabel));
            OnPropertyChanged(nameof(InstallBuildOptionsLabel));
            OnPropertyChanged(nameof(InstallOptionalLabel));
            OnPropertyChanged(nameof(InstallBuildOptionsDesc));
            OnPropertyChanged(nameof(InstallBuildMemoryLabel));
            OnPropertyChanged(nameof(InstallCompileKnowledgeLabel));
            OnPropertyChanged(nameof(InstallBuildIndexLabel));
            OnPropertyChanged(nameof(InstallBuildEmbeddingsLabel));
            OnPropertyChanged(nameof(InstallPackageFrameworkLabel));
            OnPropertyChanged(nameof(InstallBuildExeNote));
            OnPropertyChanged(nameof(InstallTipLabel));

            OnPropertyChanged(nameof(SettingsAppearanceLabel));
            OnPropertyChanged(nameof(SettingsStartupLabel));
            OnPropertyChanged(nameof(SettingsNotificationsLabel));
            OnPropertyChanged(nameof(SettingsLoggingLabel));
            OnPropertyChanged(nameof(SettingsSaveLabel));

            OnPropertyChanged(nameof(BackupConfigurationLabel));
            OnPropertyChanged(nameof(BackupSnapshotsLabel));
        }

        void DismissToast(object? arg)
        {
            if (arg is ToastNotification toast)
                _toast.Dismiss(toast);
        }

        void OpenBrowser(object? url)
        {
            if (url is string uri && !string.IsNullOrWhiteSpace(uri))
            {
                LogLines.Add($"[BROWSER] Opening: {uri}");
                try
                {
                    // Try direct URL launch first
                    var psi = new ProcessStartInfo
                    {
                        FileName = uri,
                        UseShellExecute = true
                    };
                    Process.Start(psi);
                    LogLines.Add("[BROWSER] Launched successfully");
                }
                catch (Exception ex)
                {
                    var errorMsg = $"[BROWSER] Error: {ex.Message}";
                    LogLines.Add(errorMsg);
                    _toast.Error(FrameworkTitle, $"Cannot open browser: {ex.Message}");
                }
            }
            else
            {
                LogLines.Add($"[BROWSER] Invalid URL: '{url}'");
            }
        }

        void CancelFramework(object? _)
        {
            _framework.Cancel();
            // Wait for the killed process to exit so IsFrameworkRunning can flip back
            // and the server card shows the right state. Bounded wait to avoid hanging.
            _framework.WaitForExit(TimeSpan.FromSeconds(5));
            IsFrameworkRunning = false;
            RunningCommandText = "";
        }

        void ResetSteps()
        {
            var pending = new SolidColorBrush(Color.FromRgb(51, 65, 85));
            Step1Fill = pending; Step1Text = "";
            Step2Fill = pending; Step2Text = "";
            Step3Fill = pending; Step3Text = "";
            Step4Fill = pending; Step4Text = "";
            StepLine1Fill = pending;
            StepLine2Fill = pending;
            StepLine3Fill = pending;
            Step1Label = LocalizationService.T("step.prepare");
            Step2Label = LocalizationService.T("step.extract");
            Step3Label = LocalizationService.T("step.deploy");
            Step4Label = LocalizationService.T("step.complete");
        }

        void SetActiveStep(int step)
        {
            var pending = new SolidColorBrush(Color.FromRgb(51, 65, 85));
            var active = new SolidColorBrush(Color.FromRgb(99, 102, 241));
            var done = new SolidColorBrush(Color.FromRgb(52, 211, 153));
            if (step >= 1) { Step1Fill = done; Step1Text = "\u2713"; StepLine1Fill = done; }
            else { Step1Fill = active; Step1Text = "1"; }
            if (step >= 2) { Step2Fill = done; Step2Text = "\u2713"; StepLine2Fill = done; }
            else { Step2Fill = step == 2 ? active : pending; Step2Text = step == 2 ? "2" : ""; }
            if (step >= 3) { Step3Fill = done; Step3Text = "\u2713"; StepLine3Fill = done; }
            else { Step3Fill = step == 3 ? active : pending; Step3Text = step == 3 ? "3" : ""; }
            Step4Fill = step >= 4 ? done : pending;
            Step4Text = step >= 4 ? "\u2713" : "";
        }
    }

    public class NavItem : ViewModelBase
    {
        public string Icon { get; set; } = "";
        public string TitleKey { get; set; } = "";
        public string Title => LocalizationService.T(TitleKey);
        public int Index { get; set; }

        /// <summary>
        /// Notifies WPF that the Title property has changed so bindings refresh
        /// when the active culture changes.
        /// </summary>
        public void RefreshTitle() => OnPropertyChanged(nameof(Title));
    }

    public class LogEntry
    {
        public string Message { get; set; } = "";
        public string Level { get; set; } = "INFO";
    }

    public class LanguageItem
    {
        public string Code { get; set; } = "";
        public string DisplayName { get; set; } = "";
    }

    public class ThemeItem
    {
        public string Code { get; set; } = "";
        public string DisplayName { get; set; } = "";
    }

    public class ChangelogEntry
    {
        public string Version { get; set; } = "";
        public DateTime Date { get; set; }
        public string Description { get; set; } = "";
    }

    static class McpCatalog
    {
        public static int Count { get; } = 3;
    }
}
