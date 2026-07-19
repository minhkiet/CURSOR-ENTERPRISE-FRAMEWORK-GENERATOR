using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using CursorSetupWpf.Models;
using CursorSetupWpf.Services;

namespace CursorSetupWpf.ViewModels
{
    public class MainViewModel : ViewModelBase
    {
        readonly Installer _installer = new();

        // Navigation
        int _selectedNavIndex;
        public int SelectedNavIndex
        {
            get => _selectedNavIndex;
            set => Set(ref _selectedNavIndex, value);
        }

        public ObservableCollection<NavItem> NavItems { get; } = new();
        public ObservableCollection<SetupCategory> ComponentCategories { get; } = new();
        public ObservableCollection<SetupCategory> AdvancedCategories { get; } = new();

        // Strings (bound directly, updated when culture changes)
        // StatusText: stores either a static localized key (for dynamic updates)
        // or a raw string (for installer progress messages).
        // When a key is set, StatusText re-evaluates via LocalizationService.
        public string Str(string key) => LocalizationService.T(key);
        public string VersionChip => "v4.3";

        public string InstallButtonText => LocalizationService.T("btn.install");

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
        // Fill: pending=Slate700, active=Indigo600, done=Slate700 (checkmark)
        // Text: pending="", active="1/2/3/4", done=""
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
        Brush _step1Fill, _step2Fill, _step3Fill, _step4Fill;
        Brush _stepLine1Fill, _stepLine2Fill, _stepLine3Fill;
        string _step1Text = "", _step2Text = "", _step3Text = "", _step4Text = "";
        string _step1Label = "", _step2Label = "", _step3Label = "", _step4Label = "";

        // StatusText: stores either a static localized key (for dynamic updates)
        // or a raw string (for installer progress messages).
        // When a key is set, StatusText re-evaluates via LocalizationService.
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

        // Commands
        public ICommand BrowseCommand { get; }
        public ICommand NewFolderCommand { get; }
        public ICommand InstallCommand { get; }
        public ICommand CancelCommand { get; }
        public ICommand SelectAllComponentsCommand { get; }
        public ICommand DeselectAllComponentsCommand { get; }
        public ICommand SelectAllAdvancedCommand { get; }
        public ICommand DeselectAllAdvancedCommand { get; }

        public MainViewModel()
        {
            NavItems.Add(new NavItem { Icon = "\uE8B7", TitleKey = "tab.install", Index = 0 });
            NavItems.Add(new NavItem { Icon = "\uE8F1", TitleKey = "tab.components", Index = 1 });
            NavItems.Add(new NavItem { Icon = "\uE713", TitleKey = "tab.advanced", Index = 2 });
            NavItems.Add(new NavItem { Icon = "\uE943", TitleKey = "tab.hooks", Index = 3 });
            NavItems.Add(new NavItem { Icon = "\uE897", TitleKey = "tab.guide", Index = 4 });

            _installPath = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".cursor");

            BrowseCommand = new RelayCommand(Browse);
            NewFolderCommand = new RelayCommand(NewFolder);
            InstallCommand = new AsyncRelayCommand(async _ => await InstallAsync(_), _ => CanInstall);
            CancelCommand = new RelayCommand(Cancel);
            SelectAllComponentsCommand = new RelayCommand(_ => SelectAll(ComponentCategories));
            DeselectAllComponentsCommand = new RelayCommand(_ => DeselectAll(ComponentCategories));
            SelectAllAdvancedCommand = new RelayCommand(_ => SelectAll(AdvancedCategories));
            DeselectAllAdvancedCommand = new RelayCommand(_ => DeselectAll(AdvancedCategories));

            _installer.ProgressChanged += (pct, msg) =>
                Application.Current.Dispatcher.Invoke(() =>
                {
                    ProgressValue = pct;
                    StatusText = msg;
                });
            _installer.LogAppended += msg =>
                Application.Current.Dispatcher.Invoke(() => LogLines.Add(msg));

            // Initialize languages
            foreach (var code in LocalizationService.AvailableCultures)
                _languages.Add(new LanguageItem { Code = code, DisplayName = LocalizationService.CultureDisplayName(code) });
            _selectedLanguage = _languages.FirstOrDefault(l => l.Code == LocalizationService.Current) ?? _languages.First();

            LocalizationService.CultureChanged += RefreshStrings;

            ResetSteps();

            LoadCategoriesAsync();
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
                    // Core categories: install all items if none selected
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

            // Component categories
            var compCats = new[] { "rules", "skills", "agents", "commands", "hooks", "knowledge" };
            foreach (var catName in compCats)
                LoadCategory(catName, items, ComponentCategories);

            // Advanced categories
            var advCats = new[] { "prompts", "references", "workflows", "templates", "memory", "scripts" };
            foreach (var catName in advCats)
                LoadCategory(catName, items, AdvancedCategories);

            UpdateSummary();
            SetStatusKey("ready_to_install");
            LogLines.Add(LocalizationService.T("scanned_log", items.Count));
        }

        void LoadCategory(string catName, Dictionary<string, List<string>> items, ObservableCollection<SetupCategory> target)
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
            target.Add(cat);
        }

        void UpdateSummary()
        {
            int total = ComponentCategories.Sum(c => c.TotalCount) + AdvancedCategories.Sum(c => c.TotalCount);
            int selected = ComponentCategories.Sum(c => c.SelectedCount) + AdvancedCategories.Sum(c => c.SelectedCount);
            SummaryText = LocalizationService.T("summary.components", selected, total);
        }

        void RefreshStrings()
        {
            // Force all bound strings to refresh
            OnPropertyChanged(nameof(VersionChip));
            OnPropertyChanged(nameof(SelectedNavIndex));
            foreach (var nav in NavItems)
                OnPropertyChanged(nameof(nav.Title));
            OnPropertyChanged(nameof(Step1Label));
            OnPropertyChanged(nameof(Step2Label));
            OnPropertyChanged(nameof(Step3Label));
            OnPropertyChanged(nameof(Step4Label));
            OnPropertyChanged(nameof(InstallButtonText));
            OnPropertyChanged(nameof(CanInstall));
            OnPropertyChanged(nameof(StatusText));
            OnPropertyChanged(nameof(SummaryText));
        }

        void ResetSteps()
        {
            var pending = new SolidColorBrush(Color.FromRgb(51, 65, 85));   // Slate-700
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
            var pending = new SolidColorBrush(Color.FromRgb(51, 65, 85));   // Slate-700
            var active = new SolidColorBrush(Color.FromRgb(99, 102, 241)); // Indigo-500
            var done = new SolidColorBrush(Color.FromRgb(52, 211, 153));   // Emerald-400
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
        public string Title
        {
            get => LocalizationService.T(TitleKey);
        }
        public int Index { get; set; }
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
}
