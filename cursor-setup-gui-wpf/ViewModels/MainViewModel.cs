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
        readonly ProjectRunner _projectRunner = new();
        readonly ToastService _toast = ToastService.Instance;

        // Navigation
        int _selectedNavIndex;
        public int SelectedNavIndex
        {
            get => _selectedNavIndex;
            set => Set(ref _selectedNavIndex, value);
        }

        public ThreadSafeObservableCollection<NavItem> NavItems { get; } = new();
        
        // ECC ViewModel - shared with ECCView for bilingual support
        public ECCViewModel ECCViewModel { get; } = new();
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

        // Backing fields for localized strings (required for OnPropertyChanged to work in WPF)
        // Initialize all at once to reduce code duplication
        string _installPageTitle = "", _installPageSubtitle = "", _installButtonText = "";
        string _languageLabel = "", _windowTitle = "", _appBrand = "", _appBrandSubtitle = "";
        string _vibeCoderTitle = "", _mcpTitle = "", _mcpSubtitle = "", _mcpSyncAllLabel = "", _mcpCheckStatusLabel = "";
        string _mcpInstalledLabel = "", _mcpNotInstalledLabel = "", _mcpOpenConfigLabel = "", _mcpLastSyncLabel = "";
        string _hooksPageTitle = "", _hooksPageDesc = "", _hooksPrescanTitle = "", _hooksPrescanDesc = "";
        string _hooksPrescanScriptLabel = "", _hooksPostinstallTitle = "", _hooksPostinstallDesc = "";
        string _hooksPostinstallScriptLabel = "", _hooksAboutTitle = "", _hooksAboutDesc = "";
        string _componentsTitle = "", _componentsSubtitle = "", _advancedTitle = "", _advancedSubtitle = "";
        string _btnSelectAll = "", _btnDeselectAll = "";
        string _installLocationLabel = "", _installLocationHint = "", _installBrowseLabel = "", _installNewFolderLabel = "";
        string _installForceLabel = "", _installSkipCursorLabel = "", _installBuildOptionsLabel = "";
        string _installOptionalLabel = "", _installBuildOptionsDesc = "", _installBuildMemoryLabel = "";
        string _installCompileKnowledgeLabel = "", _installBuildIndexLabel = "", _installBuildEmbeddingsLabel = "";
        string _installPackageFrameworkLabel = "", _installBuildExeNote = "", _installTipLabel = "";
        string _updatesTitle = "", _updatesSubtitle = "", _updatesCheckLabel = "", _updatesDownloadLabel = "";
        string _updatesChangelogLabel = "", _updatesCurrentVersionLabel = "", _updatesLatestVersionLabel = "";
        string _backupTitle = "", _backupSubtitle = "", _backupCreateLabel = "", _backupRestoreLabel = "";
        string _backupDeleteLabel = "", _backupRefreshLabel = "", _backupLocationLabel = "", _backupBrowseLabel = "";
        string _backupAutoLabel = "", _backupEmptyLabel = "", _backupConfigurationLabel = "", _backupSnapshotsLabel = "";
        string _settingsTitle = "", _settingsSubtitle = "", _settingsThemeLabel = "";
        string _settingsAutostartLabel = "", _settingsAutostartDescLabel = "";
        string _settingsNotifyCompleteLabel = "", _settingsNotifyErrorLabel = "";
        string _settingsLogPathLabel = "", _settingsBrowseLabel = "";
        string _settingsAppearanceLabel = "", _settingsStartupLabel = "", _settingsNotificationsLabel = "";
        string _settingsLoggingLabel = "", _settingsSaveLabel = "";
        string _frameworkTitle = "", _frameworkSubtitle = "", _btnStartLabel = "", _btnOpenLabel = "";
        string _btnRunLabel = "", _btnCancelLabel = "";
        string _frameworkDashboardLabel = "", _frameworkDashboardDesc = "";
        string _frameworkGraphLabel = "", _frameworkGraphDesc = "", _frameworkApiLabel = "", _frameworkApiDesc = "";
        string _frameworkScanLabel = "", _frameworkScanDesc = "", _frameworkIndexLabel = "", _frameworkIndexDesc = "";
        string _frameworkWarmLabel = "", _frameworkWarmDesc = "", _frameworkStatsLabel = "", _frameworkStatsDesc = "";
        string _frameworkSkillGraphLabel = "", _frameworkSkillGraphDesc = "";
        string _frameworkCodeGraphLabel = "", _frameworkCodeGraphDesc = "";
        string _frameworkSessionStatsLabel = "", _frameworkSessionStatsDesc = "";
        string _frameworkClearSessionLabel = "", _frameworkClearSessionDesc = "";
        string _frameworkRunningText = "", _frameworkServersTitle = "", _frameworkBuildTitle = "";
        string _frameworkGraphTitle = "", _frameworkAboutTitle = "", _frameworkAboutDesc = "";
        string _frameworkAboutCommands = "", _frameworkAboutCommandList = "";
        string _mcpDiscoveredToolsLabel = "";
        string _projectRunnerTitle = "", _projectRunnerSubtitle = "", _projectRunnerSelectProjectLabel = "";
        string _projectRunnerBrowseLabel = "", _projectRunnerDetectedProjectsLabel = "", _projectRunnerRunOnProjectLabel = "";
        string _projectRunnerAskPlaceholder = "", _projectRunnerCurrentPathLabel = "";
        string _projectRunnerRunningLabel = "", _projectRunnerAskTitle = "", _projectRunnerAskSubtitle = "";
        string _projectRunnerRunAskLabel = "", _projectRunnerOutputLabel = "", _projectRunnerClearLabel = "";
        string _itemsUnitLabel = "", _agentTitle = "", _agentInstalledLabel = "", _agentNotInstalledLabel = "";
        string _installForAllAgentsLabel = "";

        // Properties with backing fields (will be initialized in constructor)
        public string InstallButtonText { get => _installButtonText; set => Set(ref _installButtonText, value); }
        public string LanguageLabel { get => _languageLabel; set => Set(ref _languageLabel, value); }
        public string WindowTitle { get => _windowTitle; set => Set(ref _windowTitle, value); }
        public string AppBrand { get => _appBrand; set => Set(ref _appBrand, value); }
        public string AppBrandSubtitle { get => _appBrandSubtitle; set => Set(ref _appBrandSubtitle, value); }
        public string VibeCoderTitle { get => _vibeCoderTitle; set => Set(ref _vibeCoderTitle, value); }
        public string McpTitle { get => _mcpTitle; set => Set(ref _mcpTitle, value); }
        public string McpSubtitle { get => _mcpSubtitle; set => Set(ref _mcpSubtitle, value); }
        public string McpSyncAllLabel { get => _mcpSyncAllLabel; set => Set(ref _mcpSyncAllLabel, value); }
        public string McpCheckStatusLabel { get => _mcpCheckStatusLabel; set => Set(ref _mcpCheckStatusLabel, value); }
        public string McpInstalledLabel { get => _mcpInstalledLabel; set => Set(ref _mcpInstalledLabel, value); }
        public string McpNotInstalledLabel { get => _mcpNotInstalledLabel; set => Set(ref _mcpNotInstalledLabel, value); }
        public string McpOpenConfigLabel { get => _mcpOpenConfigLabel; set => Set(ref _mcpOpenConfigLabel, value); }
        public string McpLastSyncLabel { get => _mcpLastSyncLabel; set => Set(ref _mcpLastSyncLabel, value); }
        public string HooksPageTitle { get => _hooksPageTitle; set => Set(ref _hooksPageTitle, value); }
        public string HooksPageDesc { get => _hooksPageDesc; set => Set(ref _hooksPageDesc, value); }
        public string HooksPrescanTitle { get => _hooksPrescanTitle; set => Set(ref _hooksPrescanTitle, value); }
        public string HooksPrescanDesc { get => _hooksPrescanDesc; set => Set(ref _hooksPrescanDesc, value); }
        public string HooksPrescanScriptLabel { get => _hooksPrescanScriptLabel; set => Set(ref _hooksPrescanScriptLabel, value); }
        public string HooksPostinstallTitle { get => _hooksPostinstallTitle; set => Set(ref _hooksPostinstallTitle, value); }
        public string HooksPostinstallDesc { get => _hooksPostinstallDesc; set => Set(ref _hooksPostinstallDesc, value); }
        public string HooksPostinstallScriptLabel { get => _hooksPostinstallScriptLabel; set => Set(ref _hooksPostinstallScriptLabel, value); }
        public string HooksAboutTitle { get => _hooksAboutTitle; set => Set(ref _hooksAboutTitle, value); }
        public string HooksAboutDesc { get => _hooksAboutDesc; set => Set(ref _hooksAboutDesc, value); }
        public string ComponentsTitle { get => _componentsTitle; set => Set(ref _componentsTitle, value); }
        public string ComponentsSubtitle { get => _componentsSubtitle; set => Set(ref _componentsSubtitle, value); }
        public string AdvancedTitle { get => _advancedTitle; set => Set(ref _advancedTitle, value); }
        public string AdvancedSubtitle { get => _advancedSubtitle; set => Set(ref _advancedSubtitle, value); }
        public string BtnSelectAll { get => _btnSelectAll; set => Set(ref _btnSelectAll, value); }
        public string BtnDeselectAll { get => _btnDeselectAll; set => Set(ref _btnDeselectAll, value); }
        public string InstallPageTitle { get => _installPageTitle; set => Set(ref _installPageTitle, value); }
        public string InstallPageSubtitle { get => _installPageSubtitle; set => Set(ref _installPageSubtitle, value); }
        public string InstallLocationLabel { get => _installLocationLabel; set => Set(ref _installLocationLabel, value); }
        public string InstallLocationHint { get => _installLocationHint; set => Set(ref _installLocationHint, value); }
        public string InstallBrowseLabel { get => _installBrowseLabel; set => Set(ref _installBrowseLabel, value); }
        public string InstallNewFolderLabel { get => _installNewFolderLabel; set => Set(ref _installNewFolderLabel, value); }
        public string InstallForceLabel { get => _installForceLabel; set => Set(ref _installForceLabel, value); }
        public string InstallSkipCursorLabel { get => _installSkipCursorLabel; set => Set(ref _installSkipCursorLabel, value); }
        public string InstallBuildOptionsLabel { get => _installBuildOptionsLabel; set => Set(ref _installBuildOptionsLabel, value); }
        public string InstallOptionalLabel { get => _installOptionalLabel; set => Set(ref _installOptionalLabel, value); }
        public string InstallBuildOptionsDesc { get => _installBuildOptionsDesc; set => Set(ref _installBuildOptionsDesc, value); }
        public string InstallBuildMemoryLabel { get => _installBuildMemoryLabel; set => Set(ref _installBuildMemoryLabel, value); }
        public string InstallCompileKnowledgeLabel { get => _installCompileKnowledgeLabel; set => Set(ref _installCompileKnowledgeLabel, value); }
        public string InstallBuildIndexLabel { get => _installBuildIndexLabel; set => Set(ref _installBuildIndexLabel, value); }
        public string InstallBuildEmbeddingsLabel { get => _installBuildEmbeddingsLabel; set => Set(ref _installBuildEmbeddingsLabel, value); }
        public string InstallPackageFrameworkLabel { get => _installPackageFrameworkLabel; set => Set(ref _installPackageFrameworkLabel, value); }
        public string InstallBuildExeNote { get => _installBuildExeNote; set => Set(ref _installBuildExeNote, value); }
        public string InstallTipLabel { get => _installTipLabel; set => Set(ref _installTipLabel, value); }
        public string UpdatesTitle { get => _updatesTitle; set => Set(ref _updatesTitle, value); }
        public string UpdatesSubtitle { get => _updatesSubtitle; set => Set(ref _updatesSubtitle, value); }
        public string UpdatesCheckLabel { get => _updatesCheckLabel; set => Set(ref _updatesCheckLabel, value); }
        public string UpdatesDownloadLabel { get => _updatesDownloadLabel; set => Set(ref _updatesDownloadLabel, value); }
        public string UpdatesChangelogLabel { get => _updatesChangelogLabel; set => Set(ref _updatesChangelogLabel, value); }
        public string UpdatesCurrentVersionLabel { get => _updatesCurrentVersionLabel; set => Set(ref _updatesCurrentVersionLabel, value); }
        public string UpdatesLatestVersionLabel { get => _updatesLatestVersionLabel; set => Set(ref _updatesLatestVersionLabel, value); }
        public string BackupTitle { get => _backupTitle; set => Set(ref _backupTitle, value); }
        public string BackupSubtitle { get => _backupSubtitle; set => Set(ref _backupSubtitle, value); }
        public string BackupCreateLabel { get => _backupCreateLabel; set => Set(ref _backupCreateLabel, value); }
        public string BackupRestoreLabel { get => _backupRestoreLabel; set => Set(ref _backupRestoreLabel, value); }
        public string BackupDeleteLabel { get => _backupDeleteLabel; set => Set(ref _backupDeleteLabel, value); }
        public string BackupRefreshLabel { get => _backupRefreshLabel; set => Set(ref _backupRefreshLabel, value); }
        public string BackupLocationLabel { get => _backupLocationLabel; set => Set(ref _backupLocationLabel, value); }
        public string BackupBrowseLabel { get => _backupBrowseLabel; set => Set(ref _backupBrowseLabel, value); }
        public string BackupAutoLabel { get => _backupAutoLabel; set => Set(ref _backupAutoLabel, value); }
        public string BackupEmptyLabel { get => _backupEmptyLabel; set => Set(ref _backupEmptyLabel, value); }
        public string BackupConfigurationLabel { get => _backupConfigurationLabel; set => Set(ref _backupConfigurationLabel, value); }
        public string BackupSnapshotsLabel { get => _backupSnapshotsLabel; set => Set(ref _backupSnapshotsLabel, value); }
        public string SettingsTitle { get => _settingsTitle; set => Set(ref _settingsTitle, value); }
        public string SettingsSubtitle { get => _settingsSubtitle; set => Set(ref _settingsSubtitle, value); }
        public string SettingsThemeLabel { get => _settingsThemeLabel; set => Set(ref _settingsThemeLabel, value); }
        public string SettingsAutostartLabel { get => _settingsAutostartLabel; set => Set(ref _settingsAutostartLabel, value); }
        public string SettingsAutostartDescLabel { get => _settingsAutostartDescLabel; set => Set(ref _settingsAutostartDescLabel, value); }
        public string SettingsNotifyCompleteLabel { get => _settingsNotifyCompleteLabel; set => Set(ref _settingsNotifyCompleteLabel, value); }
        public string SettingsNotifyErrorLabel { get => _settingsNotifyErrorLabel; set => Set(ref _settingsNotifyErrorLabel, value); }
        public string SettingsLogPathLabel { get => _settingsLogPathLabel; set => Set(ref _settingsLogPathLabel, value); }
        public string SettingsBrowseLabel { get => _settingsBrowseLabel; set => Set(ref _settingsBrowseLabel, value); }
        public string SettingsAppearanceLabel { get => _settingsAppearanceLabel; set => Set(ref _settingsAppearanceLabel, value); }
        public string SettingsStartupLabel { get => _settingsStartupLabel; set => Set(ref _settingsStartupLabel, value); }
        public string SettingsNotificationsLabel { get => _settingsNotificationsLabel; set => Set(ref _settingsNotificationsLabel, value); }
        public string SettingsLoggingLabel { get => _settingsLoggingLabel; set => Set(ref _settingsLoggingLabel, value); }
        public string SettingsSaveLabel { get => _settingsSaveLabel; set => Set(ref _settingsSaveLabel, value); }
        public string FrameworkTitle { get => _frameworkTitle; set => Set(ref _frameworkTitle, value); }
        public string FrameworkSubtitle { get => _frameworkSubtitle; set => Set(ref _frameworkSubtitle, value); }
        public string BtnStartLabel { get => _btnStartLabel; set => Set(ref _btnStartLabel, value); }
        public string BtnOpenLabel { get => _btnOpenLabel; set => Set(ref _btnOpenLabel, value); }
        public string BtnRunLabel { get => _btnRunLabel; set => Set(ref _btnRunLabel, value); }
        public string BtnCancelLabel { get => _btnCancelLabel; set => Set(ref _btnCancelLabel, value); }
        public string FrameworkDashboardLabel { get => _frameworkDashboardLabel; set => Set(ref _frameworkDashboardLabel, value); }
        public string FrameworkDashboardDesc { get => _frameworkDashboardDesc; set => Set(ref _frameworkDashboardDesc, value); }
        public string FrameworkGraphLabel { get => _frameworkGraphLabel; set => Set(ref _frameworkGraphLabel, value); }
        public string FrameworkGraphDesc { get => _frameworkGraphDesc; set => Set(ref _frameworkGraphDesc, value); }
        public string FrameworkApiLabel { get => _frameworkApiLabel; set => Set(ref _frameworkApiLabel, value); }
        public string FrameworkApiDesc { get => _frameworkApiDesc; set => Set(ref _frameworkApiDesc, value); }
        public string FrameworkScanLabel { get => _frameworkScanLabel; set => Set(ref _frameworkScanLabel, value); }
        public string FrameworkScanDesc { get => _frameworkScanDesc; set => Set(ref _frameworkScanDesc, value); }
        public string FrameworkIndexLabel { get => _frameworkIndexLabel; set => Set(ref _frameworkIndexLabel, value); }
        public string FrameworkIndexDesc { get => _frameworkIndexDesc; set => Set(ref _frameworkIndexDesc, value); }
        public string FrameworkWarmLabel { get => _frameworkWarmLabel; set => Set(ref _frameworkWarmLabel, value); }
        public string FrameworkWarmDesc { get => _frameworkWarmDesc; set => Set(ref _frameworkWarmDesc, value); }
        public string FrameworkStatsLabel { get => _frameworkStatsLabel; set => Set(ref _frameworkStatsLabel, value); }
        public string FrameworkStatsDesc { get => _frameworkStatsDesc; set => Set(ref _frameworkStatsDesc, value); }
        public string FrameworkSkillGraphLabel { get => _frameworkSkillGraphLabel; set => Set(ref _frameworkSkillGraphLabel, value); }
        public string FrameworkSkillGraphDesc { get => _frameworkSkillGraphDesc; set => Set(ref _frameworkSkillGraphDesc, value); }
        public string FrameworkCodeGraphLabel { get => _frameworkCodeGraphLabel; set => Set(ref _frameworkCodeGraphLabel, value); }
        public string FrameworkCodeGraphDesc { get => _frameworkCodeGraphDesc; set => Set(ref _frameworkCodeGraphDesc, value); }
        public string FrameworkSessionStatsLabel { get => _frameworkSessionStatsLabel; set => Set(ref _frameworkSessionStatsLabel, value); }
        public string FrameworkSessionStatsDesc { get => _frameworkSessionStatsDesc; set => Set(ref _frameworkSessionStatsDesc, value); }
        public string FrameworkClearSessionLabel { get => _frameworkClearSessionLabel; set => Set(ref _frameworkClearSessionLabel, value); }
        public string FrameworkClearSessionDesc { get => _frameworkClearSessionDesc; set => Set(ref _frameworkClearSessionDesc, value); }
        public string FrameworkRunningText { get => _frameworkRunningText; set => Set(ref _frameworkRunningText, value); }
        public string FrameworkServersTitle { get => _frameworkServersTitle; set => Set(ref _frameworkServersTitle, value); }
        public string FrameworkBuildTitle { get => _frameworkBuildTitle; set => Set(ref _frameworkBuildTitle, value); }
        public string FrameworkGraphTitle { get => _frameworkGraphTitle; set => Set(ref _frameworkGraphTitle, value); }
        public string FrameworkAboutTitle { get => _frameworkAboutTitle; set => Set(ref _frameworkAboutTitle, value); }
        public string FrameworkAboutDesc { get => _frameworkAboutDesc; set => Set(ref _frameworkAboutDesc, value); }
        public string FrameworkAboutCommands { get => _frameworkAboutCommands; set => Set(ref _frameworkAboutCommands, value); }
        public string FrameworkAboutCommandList { get => _frameworkAboutCommandList; set => Set(ref _frameworkAboutCommandList, value); }
        public string McpDiscoveredToolsLabel { get => _mcpDiscoveredToolsLabel; set => Set(ref _mcpDiscoveredToolsLabel, value); }
        public string ProjectRunnerTitle { get => _projectRunnerTitle; set => Set(ref _projectRunnerTitle, value); }
        public string ProjectRunnerSubtitle { get => _projectRunnerSubtitle; set => Set(ref _projectRunnerSubtitle, value); }
        public string ProjectRunnerSelectProjectLabel { get => _projectRunnerSelectProjectLabel; set => Set(ref _projectRunnerSelectProjectLabel, value); }
        public string ProjectRunnerBrowseLabel { get => _projectRunnerBrowseLabel; set => Set(ref _projectRunnerBrowseLabel, value); }
        public string ProjectRunnerDetectedProjectsLabel { get => _projectRunnerDetectedProjectsLabel; set => Set(ref _projectRunnerDetectedProjectsLabel, value); }
        public string ProjectRunnerRunOnProjectLabel { get => _projectRunnerRunOnProjectLabel; set => Set(ref _projectRunnerRunOnProjectLabel, value); }
        public string ProjectRunnerAskPlaceholder { get => _projectRunnerAskPlaceholder; set => Set(ref _projectRunnerAskPlaceholder, value); }
        public string ProjectRunnerCurrentPathLabel { get => _projectRunnerCurrentPathLabel; set => Set(ref _projectRunnerCurrentPathLabel, value); }
        public string ProjectRunnerRunningLabel { get => _projectRunnerRunningLabel; set => Set(ref _projectRunnerRunningLabel, value); }
        public string ProjectRunnerAskTitle { get => _projectRunnerAskTitle; set => Set(ref _projectRunnerAskTitle, value); }
        public string ProjectRunnerAskSubtitle { get => _projectRunnerAskSubtitle; set => Set(ref _projectRunnerAskSubtitle, value); }
        public string ProjectRunnerRunAskLabel { get => _projectRunnerRunAskLabel; set => Set(ref _projectRunnerRunAskLabel, value); }
        public string ProjectRunnerOutputLabel { get => _projectRunnerOutputLabel; set => Set(ref _projectRunnerOutputLabel, value); }
        public string ProjectRunnerClearLabel { get => _projectRunnerClearLabel; set => Set(ref _projectRunnerClearLabel, value); }
        public string ItemsUnitLabel { get => _itemsUnitLabel; set => Set(ref _itemsUnitLabel, value); }
        public string AgentTitle { get => _agentTitle; set => Set(ref _agentTitle, value); }
        public string AgentInstalledLabel { get => _agentInstalledLabel; set => Set(ref _agentInstalledLabel, value); }
        public string AgentNotInstalledLabel { get => _agentNotInstalledLabel; set => Set(ref _agentNotInstalledLabel, value); }
        public string InstallForAllAgentsLabel { get => _installForAllAgentsLabel; set => Set(ref _installForAllAgentsLabel, value); }

        bool _isProjectRunnerRunning;
        public bool IsProjectRunnerRunning { get => _isProjectRunnerRunning; set { if (Set(ref _isProjectRunnerRunning, value)) OnPropertyChanged(nameof(IsProjectRunnerRunning)); } }

        string _projectRunnerOutput = "";
        public string ProjectRunnerOutput { get => _projectRunnerOutput; set => Set(ref _projectRunnerOutput, value); }

        string _selectedProjectPath = "";
        public string SelectedProjectPath { get => _selectedProjectPath; set => Set(ref _selectedProjectPath, value); }

        string _projectRunnerAskRequest = "";
        public string ProjectRunnerAskRequest { get => _projectRunnerAskRequest; set => Set(ref _projectRunnerAskRequest, value); }

        public ObservableCollection<string> DetectedProjects { get; } = new();

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
                    _settings.Current.Language = value.Code;
                    _settings.Save();
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
            LocalizationService.T("mcp.config_path", Installer.GetMcpConfigPath(SelectedAgent?.Agent ?? TargetAgent.Cursor));

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

        // ============ Localization Helpers ============
        
        /// <summary>
        /// Initialize all localized string properties from current culture.
        /// Call this in constructor and in RefreshStrings to update all UI labels.
        /// </summary>
        void InitLocalizedStrings()
        {
            WindowTitle = LocalizationService.T("app.title");
            AppBrand = LocalizationService.T("app.title_short");
            AppBrandSubtitle = LocalizationService.T("app.subtitle");
            InstallButtonText = LocalizationService.T("btn.install");
            LanguageLabel = LocalizationService.T("combobox.lang");
            VibeCoderTitle = LocalizationService.T("vibe_coder.label");
            
            // MCP labels
            McpTitle = LocalizationService.T("mcp.title");
            McpSubtitle = LocalizationService.T("mcp.subtitle");
            McpSyncAllLabel = LocalizationService.T("mcp.sync_all");
            McpCheckStatusLabel = LocalizationService.T("mcp.check_status");
            McpInstalledLabel = LocalizationService.T("mcp.installed");
            McpNotInstalledLabel = LocalizationService.T("mcp.not_installed");
            McpOpenConfigLabel = LocalizationService.T("mcp.opening_config");
            McpLastSyncLabel = LocalizationService.T("mcp.last_sync",
                McpServers.FirstOrDefault()?.LastSyncText ?? LocalizationService.T("mcp.last_sync_never"));
            McpDiscoveredToolsLabel = LocalizationService.T("mcp.discovered_tools");
            
            // Hooks page
            HooksPageTitle = LocalizationService.T("hooks.page_title");
            HooksPageDesc = LocalizationService.T("hooks.page_desc");
            HooksPrescanTitle = LocalizationService.T("hooks.prescan_title");
            HooksPrescanDesc = LocalizationService.T("hooks.prescan_desc");
            HooksPrescanScriptLabel = LocalizationService.T("hooks.prescan_script_label");
            HooksPostinstallTitle = LocalizationService.T("hooks.postinstall_title");
            HooksPostinstallDesc = LocalizationService.T("hooks.postinstall_desc");
            HooksPostinstallScriptLabel = LocalizationService.T("hooks.postinstall_script_label");
            HooksAboutTitle = LocalizationService.T("hooks.about_title");
            HooksAboutDesc = LocalizationService.T("hooks.about_desc");
            
            // Components
            ComponentsTitle = LocalizationService.T("components.title");
            ComponentsSubtitle = LocalizationService.T("components.subtitle");
            
            // Advanced
            AdvancedTitle = LocalizationService.T("advanced.title");
            AdvancedSubtitle = LocalizationService.T("advanced.subtitle");
            
            // Common buttons
            BtnSelectAll = LocalizationService.T("btn.select_all");
            BtnDeselectAll = LocalizationService.T("btn.deselect_all");
            
            // Install page
            InstallPageTitle = LocalizationService.T("install.page_title");
            InstallPageSubtitle = LocalizationService.T("install.page_subtitle");
            InstallLocationLabel = LocalizationService.T("install.location");
            InstallLocationHint = LocalizationService.T("install.location_hint");
            InstallBrowseLabel = LocalizationService.T("install.browse");
            InstallNewFolderLabel = LocalizationService.T("install.new_folder");
            InstallForceLabel = LocalizationService.T("install.force");
            InstallSkipCursorLabel = LocalizationService.T("install.skip_cursor");
            InstallBuildOptionsLabel = LocalizationService.T("install.build_options");
            InstallOptionalLabel = LocalizationService.T("install.optional");
            InstallBuildOptionsDesc = LocalizationService.T("install.build_options_desc");
            InstallBuildMemoryLabel = LocalizationService.T("install.build_memory");
            InstallCompileKnowledgeLabel = LocalizationService.T("install.compile_knowledge");
            InstallBuildIndexLabel = LocalizationService.T("install.build_index");
            InstallBuildEmbeddingsLabel = LocalizationService.T("install.build_embeddings");
            InstallPackageFrameworkLabel = LocalizationService.T("install.package_framework");
            InstallBuildExeNote = LocalizationService.T("install.build_exe_note");
            InstallTipLabel = LocalizationService.T("install.tip");
            
            // Updates
            UpdatesTitle = LocalizationService.T("updates.title");
            UpdatesSubtitle = LocalizationService.T("updates.subtitle");
            UpdatesCheckLabel = LocalizationService.T("updates.check");
            UpdatesDownloadLabel = LocalizationService.T("updates.download");
            UpdatesChangelogLabel = LocalizationService.T("updates.changelog");
            UpdatesCurrentVersionLabel = LocalizationService.T("updates.current_version");
            UpdatesLatestVersionLabel = LocalizationService.T("updates.latest_version");
            
            // Backup
            BackupTitle = LocalizationService.T("backup.title");
            BackupSubtitle = LocalizationService.T("backup.subtitle");
            BackupCreateLabel = LocalizationService.T("backup.create");
            BackupRestoreLabel = LocalizationService.T("backup.restore");
            BackupDeleteLabel = LocalizationService.T("backup.delete");
            BackupRefreshLabel = LocalizationService.T("backup.refresh");
            BackupLocationLabel = LocalizationService.T("backup.location");
            BackupBrowseLabel = LocalizationService.T("backup.browse");
            BackupAutoLabel = LocalizationService.T("backup.auto");
            BackupEmptyLabel = LocalizationService.T("backup.empty");
            BackupConfigurationLabel = LocalizationService.T("backup.configuration_label");
            BackupSnapshotsLabel = LocalizationService.T("backup.snapshots_label");
            
            // Settings
            SettingsTitle = LocalizationService.T("settings.title");
            SettingsSubtitle = LocalizationService.T("settings.subtitle");
            SettingsThemeLabel = LocalizationService.T("settings.theme");
            SettingsAutostartLabel = LocalizationService.T("settings.autostart");
            SettingsAutostartDescLabel = LocalizationService.T("settings.autostart_desc");
            SettingsNotifyCompleteLabel = LocalizationService.T("settings.notify_complete");
            SettingsNotifyErrorLabel = LocalizationService.T("settings.notify_error");
            SettingsLogPathLabel = LocalizationService.T("settings.log_path");
            SettingsBrowseLabel = LocalizationService.T("settings.browse");
            SettingsAppearanceLabel = LocalizationService.T("settings.appearance_label");
            SettingsStartupLabel = LocalizationService.T("settings.startup_label");
            SettingsNotificationsLabel = LocalizationService.T("settings.notifications_label");
            SettingsLoggingLabel = LocalizationService.T("settings.logging_label");
            SettingsSaveLabel = LocalizationService.T("settings.save_label");
            
            // Framework
            FrameworkTitle = LocalizationService.T("framework.title");
            FrameworkSubtitle = LocalizationService.T("framework.subtitle");
            BtnStartLabel = LocalizationService.T("btn.start");
            BtnOpenLabel = LocalizationService.T("btn.open");
            BtnRunLabel = LocalizationService.T("btn.run");
            BtnCancelLabel = LocalizationService.T("btn.cancel");
            FrameworkDashboardLabel = LocalizationService.T("framework.dashboard");
            FrameworkDashboardDesc = LocalizationService.T("framework.dashboard_desc");
            FrameworkGraphLabel = LocalizationService.T("framework.graph_viz");
            FrameworkGraphDesc = LocalizationService.T("framework.graph_viz_desc");
            FrameworkApiLabel = LocalizationService.T("framework.api_server");
            FrameworkApiDesc = LocalizationService.T("framework.api_server_desc");
            FrameworkScanLabel = LocalizationService.T("framework.scan");
            FrameworkScanDesc = LocalizationService.T("framework.scan_desc");
            FrameworkIndexLabel = LocalizationService.T("framework.build_index");
            FrameworkIndexDesc = LocalizationService.T("framework.build_index_desc");
            FrameworkWarmLabel = LocalizationService.T("framework.warm_cache");
            FrameworkWarmDesc = LocalizationService.T("framework.warm_cache_desc");
            FrameworkStatsLabel = LocalizationService.T("framework.stats");
            FrameworkStatsDesc = LocalizationService.T("framework.stats_desc");
            FrameworkSkillGraphLabel = LocalizationService.T("framework.skill_graph");
            FrameworkSkillGraphDesc = LocalizationService.T("framework.skill_graph_desc");
            FrameworkCodeGraphLabel = LocalizationService.T("framework.code_graph");
            FrameworkCodeGraphDesc = LocalizationService.T("framework.code_graph_desc");
            FrameworkSessionStatsLabel = LocalizationService.T("framework.session_stats");
            FrameworkSessionStatsDesc = LocalizationService.T("framework.session_stats_desc");
            FrameworkClearSessionLabel = LocalizationService.T("framework.clear_session");
            FrameworkClearSessionDesc = LocalizationService.T("framework.clear_session_desc");
            FrameworkRunningText = LocalizationService.T("framework.running");
            FrameworkServersTitle = LocalizationService.T("framework.dashboard_title");
            FrameworkBuildTitle = LocalizationService.T("framework.build_title");
            FrameworkGraphTitle = LocalizationService.T("framework.graph_title");
            FrameworkAboutTitle = LocalizationService.T("framework.about_title");
            FrameworkAboutDesc = LocalizationService.T("framework.about_desc");
            FrameworkAboutCommands = LocalizationService.T("framework.about_commands");
            FrameworkAboutCommandList = LocalizationService.T("framework.about_command_list");
            
            // Project Runner
            ProjectRunnerTitle = LocalizationService.T("project_runner.title");
            ProjectRunnerSubtitle = LocalizationService.T("project_runner.subtitle");
            ProjectRunnerSelectProjectLabel = LocalizationService.T("project_runner.select_project");
            ProjectRunnerBrowseLabel = LocalizationService.T("project_runner.browse");
            ProjectRunnerDetectedProjectsLabel = LocalizationService.T("project_runner.detected_projects");
            ProjectRunnerRunOnProjectLabel = LocalizationService.T("project_runner.run_on_project");
            ProjectRunnerAskPlaceholder = LocalizationService.T("project_runner.ask_placeholder");
            ProjectRunnerCurrentPathLabel = LocalizationService.T("project_runner.current_path");
            ProjectRunnerRunningLabel = LocalizationService.T("project_runner.running");
            ProjectRunnerAskTitle = LocalizationService.T("project_runner.ask_title");
            ProjectRunnerAskSubtitle = LocalizationService.T("project_runner.ask_subtitle");
            ProjectRunnerRunAskLabel = LocalizationService.T("project_runner.run_ask");
            ProjectRunnerOutputLabel = LocalizationService.T("project_runner.output");
            ProjectRunnerClearLabel = LocalizationService.T("project_runner.clear");
            
            // Common
            ItemsUnitLabel = LocalizationService.T("common.items_unit");
            AgentTitle = LocalizationService.T("agent.title");
            AgentInstalledLabel = LocalizationService.T("agent.installed");
            AgentNotInstalledLabel = LocalizationService.T("agent.not_installed");
            InstallForAllAgentsLabel = LocalizationService.T("install.all_agents");
        }
        public ObservableCollection<AgentSelectionItem> AvailableAgents { get; } = new();
        AgentSelectionItem _selectedAgent;
        public AgentSelectionItem SelectedAgent
        {
            get => _selectedAgent;
            set
            {
                if (Set(ref _selectedAgent, value) && value != null)
                {
                    OnPropertyChanged(nameof(SelectedAgentName));
                    OnPropertyChanged(nameof(SelectedAgentPrefix));
                    OnPropertyChanged(nameof(SelectedAgentPath));
                    OnPropertyChanged(nameof(IsClaudeCodeSelected));
                    OnPropertyChanged(nameof(IsGrokSelected));
                    OnPropertyChanged(nameof(IsCodexSelected));
                    OnPropertyChanged(nameof(IsCursorSelected));
                    OnPropertyChanged(nameof(IsAntigravitySelected));
                    OnPropertyChanged(nameof(IsWindsurfSelected));
                    OnPropertyChanged(nameof(IsClineSelected));
                    OnPropertyChanged(nameof(IsRooSelected));
                    OnPropertyChanged(nameof(McpConfigPathLabel));
                    CheckMcpStatus();
                }
            }
        }
        public string SelectedAgentName => SelectedAgent?.DisplayName ?? "Cursor IDE";
        public string SelectedAgentPrefix => SelectedAgent?.GatePrefix ?? "K";
        public string SelectedAgentPath => SelectedAgent?.SkillsPath ?? ".cursor/skills";
        public bool IsCursorSelected => SelectedAgent?.Agent == CursorSetupWpf.Services.TargetAgent.Cursor;
        public bool IsCodexSelected => SelectedAgent?.Agent == CursorSetupWpf.Services.TargetAgent.Codex;
        public bool IsClaudeCodeSelected => SelectedAgent?.Agent == CursorSetupWpf.Services.TargetAgent.ClaudeCode;
        public bool IsGrokSelected => SelectedAgent?.Agent == CursorSetupWpf.Services.TargetAgent.Grok;
        public bool IsAntigravitySelected => SelectedAgent?.Agent == CursorSetupWpf.Services.TargetAgent.Antigravity;
        public bool IsWindsurfSelected => SelectedAgent?.Agent == CursorSetupWpf.Services.TargetAgent.Windsurf;
        public bool IsClineSelected => SelectedAgent?.Agent == CursorSetupWpf.Services.TargetAgent.Cline;
        public bool IsRooSelected => SelectedAgent?.Agent == CursorSetupWpf.Services.TargetAgent.Roo;

        bool _installForAllAgents;
        public bool InstallForAllAgents
        {
            get => _installForAllAgents;
            set {
                if (Set(ref _installForAllAgents, value)) {
                    // Update the label when boolean changes
                    InstallForAllAgentsLabel = value 
                        ? LocalizationService.T("install.all_agents")
                        : LocalizationService.T("install.single_agent");
                }
            }
        }

        public ObservableCollection<AgentStatusItem> AgentStatuses { get; } = new();

        // Cross-agent commands
        public ICommand RefreshAgentStatusCommand { get; }
        public ICommand InstallForSelectedAgentCommand { get; }
        public ICommand InstallForAllAgentsCommand { get; }
        public ICommand OpenAgentDocsCommand { get; }

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

        // Project Runner commands
        public ICommand BrowseProjectPathCommand { get; }
        public ICommand RunProjectScanCommand { get; }
        public ICommand RunProjectIndexCommand { get; }
        public ICommand RunProjectWarmCommand { get; }
        public ICommand RunProjectStatsCommand { get; }
        public ICommand RunProjectGraphCommand { get; }
        public ICommand RunProjectAskCommand { get; }
        public ICommand CancelProjectRunnerCommand { get; }
        public ICommand ClearProjectOutputCommand { get; }
        public ICommand RefreshDetectedProjectsCommand { get; }

        public MainViewModel()
        {
            // Subscribe to culture changes for automatic UI refresh
            LocalizationService.CultureChanged += RefreshStrings;
            
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
            NavItems.Add(new NavItem { Icon = "\uE8A5", TitleKey = "tab.project_runner", Index = 10 });
            NavItems.Add(new NavItem { Icon = "\uE8A5", TitleKey = "tab.script_generator", Index = 11 });
            NavItems.Add(new NavItem { Icon = "\uE74D", TitleKey = "tab.ecc", Index = 12 });
            
            _settings.Load();
            _installPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".cursor");
            _backupLocation = _settings.DefaultBackupPath;
            
            // Languages (Default: Tiếng Việt)
            _languages.Add(new LanguageItem { Code = "vi", DisplayName = "Tiếng Việt" });
            _languages.Add(new LanguageItem { Code = "en", DisplayName = "English" });
            string preferredLang = string.IsNullOrWhiteSpace(_settings.Current.Language) ? "vi" : _settings.Current.Language;
            
            // Initialize all localized strings BEFORE setting culture (prevents empty UI)
            InitLocalizedStrings();
            
            // Set language AFTER initial strings are loaded
            _selectedLanguage = _languages.FirstOrDefault(l => l.Code.Equals(preferredLang, StringComparison.OrdinalIgnoreCase)) ?? _languages.First();
            LocalizationService.SetCulture(_selectedLanguage.Code);
            
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

            // Project Runner commands
            BrowseProjectPathCommand = new RelayCommand(BrowseProjectPath);
            RunProjectScanCommand = new AsyncRelayCommand(_ => RunProjectCommandAsync("scan"));
            RunProjectIndexCommand = new AsyncRelayCommand(_ => RunProjectCommandAsync("index"));
            RunProjectWarmCommand = new AsyncRelayCommand(_ => RunProjectCommandAsync("warm"));
            RunProjectStatsCommand = new AsyncRelayCommand(_ => RunProjectCommandAsync("stats"));
            RunProjectGraphCommand = new AsyncRelayCommand(_ => RunProjectCommandAsync("graph"));
            RunProjectAskCommand = new AsyncRelayCommand(_ => RunProjectAskAsync());
            CancelProjectRunnerCommand = new RelayCommand((Action)CancelProjectRunner);
            ClearProjectOutputCommand = new RelayCommand(_ => ProjectRunnerOutput = "");
            Action refreshAction = () => { RefreshDetectedProjects(); };
            RefreshDetectedProjectsCommand = new RelayCommand(refreshAction);

            // Cross-agent commands
            RefreshAgentStatusCommand = new RelayCommand(_ => RefreshAgentStatus());
            InstallForSelectedAgentCommand = new AsyncRelayCommand(_ => InstallForSelectedAgentAsync());
            InstallForAllAgentsCommand = new AsyncRelayCommand(_ => InstallForAllAgentsAsync());
            OpenAgentDocsCommand = new RelayCommand(OpenAgentDocs);

            // Initialize agents
            InitializeAgents();

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

            // Wire ProjectRunner events → output panel
            _projectRunner.LogAppended += msg => Application.Current?.Dispatcher.Invoke(() =>
            {
                if (string.IsNullOrEmpty(msg)) return;
                ProjectRunnerOutput += msg + "\n";
            });
            _projectRunner.OutputReceived += output => Application.Current?.Dispatcher.Invoke(() =>
            {
                ProjectRunnerOutput += output + "\n";
            });
            _projectRunner.ProcessExited += code => Application.Current?.Dispatcher.Invoke(() =>
            {
                IsProjectRunnerRunning = false;
                ProjectRunnerOutput += $"\n[PROJECT] Exit code: {code}\n";
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
            var agent = SelectedAgent?.Agent ?? CursorSetupWpf.Services.TargetAgent.Cursor;
            var (success, message) = await _installer.SyncMcpConfigAsync(InstallPath, agent);
            if (success)
            {
                var (hooksOk, hooksMsg) = await _installer.SyncHooksConfigAsync(InstallPath, agent);
                LogLines.Add(hooksOk ? "[HOOKS] " + hooksMsg : "[HOOKS] WARN: " + hooksMsg);

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
            var agent = SelectedAgent?.Agent ?? CursorSetupWpf.Services.TargetAgent.Cursor;
            var statuses = _installer.GetMcpStatus(agent);
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
            var agent = SelectedAgent?.Agent ?? CursorSetupWpf.Services.TargetAgent.Cursor;
            string path = arg as string ?? Installer.GetMcpConfigPath(agent);
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
            // Re-initialize all localized strings from current culture
            InitLocalizedStrings();
            
            // Notify UI for dynamic properties
            OnPropertyChanged(nameof(VersionChip));
            OnPropertyChanged(nameof(SelectedNavIndex));
            foreach (var nav in NavItems)
                nav.RefreshTitle();
            OnPropertyChanged(nameof(CanInstall));
            OnPropertyChanged(nameof(StatusText));
            OnPropertyChanged(nameof(SummaryText));
            OnPropertyChanged(nameof(McpConfigPathLabel));
            OnPropertyChanged(nameof(LastCheckedLabel));
            OnPropertyChanged(nameof(UpdateStatusText));
            OnPropertyChanged(nameof(HasNoBackups));
            OnPropertyChanged(nameof(InstallForAllAgentsLabel));
            OnPropertyChanged(nameof(McpLastSyncLabel));
            
            // Refresh all bound UI elements
            OnPropertyChanged(string.Empty);
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

        // ============ Project Runner ============
        void BrowseProjectPath(object? _)
        {
            var dialog = new Microsoft.Win32.OpenFolderDialog
            {
                Title = LocalizationService.T("project_runner.select_project"),
                InitialDirectory = Directory.Exists(SelectedProjectPath) ? SelectedProjectPath :
                    Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)
            };
            if (dialog.ShowDialog() == true)
            {
                SelectedProjectPath = dialog.FolderName;
                LogLines.Add("[PROJECT] Selected: " + SelectedProjectPath);
            }
        }

        async Task RunProjectCommandAsync(string command)
        {
            if (IsProjectRunnerRunning)
            {
                _toast.Warning(ProjectRunnerTitle, LocalizationService.T("framework.running_note"));
                return;
            }

            if (string.IsNullOrWhiteSpace(SelectedProjectPath))
            {
                _toast.Warning(ProjectRunnerTitle, LocalizationService.T("project_runner.no_project_selected"));
                return;
            }

            IsProjectRunnerRunning = true;
            ProjectRunnerOutput = "";

            try
            {
                await _projectRunner.RunCommandAsync(command, SelectedProjectPath);
            }
            catch (Exception ex)
            {
                _toast.Error(ProjectRunnerTitle, ex.Message);
                LogLines.Add("[PROJECT ERROR] " + ex.Message);
            }
            finally
            {
                IsProjectRunnerRunning = false;
            }
        }

        async Task RunProjectAskAsync()
        {
            if (IsProjectRunnerRunning)
            {
                _toast.Warning(ProjectRunnerTitle, LocalizationService.T("framework.running_note"));
                return;
            }

            if (string.IsNullOrWhiteSpace(SelectedProjectPath))
            {
                _toast.Warning(ProjectRunnerTitle, LocalizationService.T("project_runner.no_project_selected"));
                return;
            }

            if (string.IsNullOrWhiteSpace(ProjectRunnerAskRequest))
            {
                _toast.Warning(ProjectRunnerTitle, LocalizationService.T("project_runner.ask_placeholder"));
                return;
            }

            IsProjectRunnerRunning = true;
            ProjectRunnerOutput = "";

            try
            {
                await _projectRunner.RunAskAsync(ProjectRunnerAskRequest, SelectedProjectPath);
            }
            catch (Exception ex)
            {
                _toast.Error(ProjectRunnerTitle, ex.Message);
                LogLines.Add("[PROJECT ERROR] " + ex.Message);
            }
            finally
            {
                IsProjectRunnerRunning = false;
            }
        }

        void CancelProjectRunner(object? _)
        {
            _projectRunner.Cancel();
            _projectRunner.WaitForExit(TimeSpan.FromSeconds(5));
            IsProjectRunnerRunning = false;
        }

        // ─── Cross-Agent Methods ─────────────────────────────────────────

        void InitializeAgents()
        {
            AvailableAgents.Clear();
            foreach (var config in Installer.GetAgentCatalog())
            {
                AvailableAgents.Add(new AgentSelectionItem
                {
                    Agent = config.Agent,
                    DisplayName = config.Name,
                    GatePrefix = config.GatePrefix,
                    SkillsPath = config.SkillsPath,
                    InstallUrl = config.InstallUrl,
                    SupportsMcp = config.SupportsMcp,
                });
            }

            // Select detected agent or default to Cursor
            var detected = Installer.DetectCurrentAgent();
            var selected = AvailableAgents.FirstOrDefault(a => a.Agent == detected)
                ?? AvailableAgents.First();
            _selectedAgent = selected;
        }

        void RefreshAgentStatus()
        {
            var statuses = _installer.GetAgentInstallationStatus(InstallPath);
            Application.Current?.Dispatcher.Invoke(() =>
            {
                AgentStatuses.Clear();
                foreach (var (agent, installed, path) in statuses)
                {
                    var config = Installer.GetAgentConfig(agent);
                    AgentStatuses.Add(new AgentStatusItem
                    {
                        Agent = agent,
                        DisplayName = config?.Name ?? agent.ToString(),
                        IsInstalled = installed,
                        InstallPath = path,
                    });
                }
            });
        }

        void RefreshDetectedProjects()
        {
            DetectedProjects.Clear();
            var projects = ProjectRunner.DetectProjects(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile));
            foreach (var p in projects)
                DetectedProjects.Add(p);
            if (DetectedProjects.Count == 0)
                DetectedProjects.Add(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".cursor"));
        }

        async Task InstallForSelectedAgentAsync()
        {
            if (SelectedAgent == null) return;
            var (success, message) = await _installer.InstallForAgentAsync(
                SelectedAgent.Agent, InstallPath, BuildConfig(), BuildSelections());
            if (success)
            {
                _toast.Success(LocalizationService.T("agent.title"),
                    LocalizationService.T("agent.install_success", SelectedAgent.DisplayName));
            }
            else
            {
                _toast.Error(LocalizationService.T("agent.title"),
                    LocalizationService.T("agent.install_failed", message));
            }
            RefreshAgentStatus();
        }

        async Task InstallForAllAgentsAsync()
        {
            var (success, message) = await _installer.InstallForAllAgentsAsync(
                InstallPath, BuildConfig(), BuildSelections());
            if (success)
            {
                _toast.Success(LocalizationService.T("agent.title"),
                    LocalizationService.T("agent.all_agents_success"));
            }
            else
            {
                _toast.Warning(LocalizationService.T("agent.title"),
                    LocalizationService.T("agent.all_agents_partial", message));
            }
            RefreshAgentStatus();
        }

        void OpenAgentDocs(object? param)
        {
            if (param is string url && !string.IsNullOrWhiteSpace(url))
            {
                try
                {
                    Process.Start(new ProcessStartInfo { FileName = url, UseShellExecute = true });
                }
                catch { }
            }
            else if (SelectedAgent != null && !string.IsNullOrWhiteSpace(SelectedAgent.InstallUrl))
            {
                try
                {
                    Process.Start(new ProcessStartInfo { FileName = SelectedAgent.InstallUrl, UseShellExecute = true });
                }
                catch { }
            }
        }

        // ─── Project Runner Methods ──────────────────────────────────

        void CancelProjectRunner()
        {
            DetectedProjects.Clear();
            var projects = ProjectRunner.DetectProjects(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile));
            foreach (var p in projects)
                DetectedProjects.Add(p);

            if (DetectedProjects.Count == 0)
            {
                // Add default paths
                DetectedProjects.Add(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".cursor"));
            }
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

    // ─── Cross-Agent Helper Classes ────────────────────────────────────

    /// <summary>
    /// Represents an agent that can be selected for installation.
    /// </summary>
    public class AgentSelectionItem
    {
        public CursorSetupWpf.Services.TargetAgent Agent { get; init; }
        public string DisplayName { get; init; } = "";
        public string GatePrefix { get; init; } = "U";
        public string SkillsPath { get; init; } = "";
        public string InstallUrl { get; init; } = "";
        public bool SupportsMcp { get; init; }
    }

    /// <summary>
    /// Represents the installation status of an agent.
    /// </summary>
    public class AgentStatusItem
    {
        public CursorSetupWpf.Services.TargetAgent Agent { get; init; }
        public string DisplayName { get; init; } = "";
        public bool IsInstalled { get; init; }
        public string InstallPath { get; init; } = "";
        public string StatusLabel => IsInstalled ? LocalizationService.T("agent.installed") : LocalizationService.T("agent.not_installed");
    }
}
