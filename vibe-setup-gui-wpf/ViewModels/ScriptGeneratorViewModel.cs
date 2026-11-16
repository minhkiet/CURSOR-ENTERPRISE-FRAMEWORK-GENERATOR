using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Input;
using CursorSetupWpf.Helpers;
using CursorSetupWpf.Models;
using CursorSetupWpf.Services;

namespace CursorSetupWpf.ViewModels
{
    public class ScriptGeneratorViewModel : ViewModelBase
    {
        readonly ScriptGeneratorService _service = new();
        // ═══════════════════════════════════════════════════════════════
        // String Resources (localized) — static calls to LocalizationService.T()
        // ═══════════════════════════════════════════════════════════════
        public string ScriptGenTitle => LocalizationService.T("script_gen.title");
        public string ScriptGenSubtitle => LocalizationService.T("script_gen.subtitle");
        public string ScriptGenFilterLabel => LocalizationService.T("script_gen.filter_label");
        public string ScriptGenProjectLabel => LocalizationService.T("script_gen.project_label");
        public string ScriptGenOutputLabel => LocalizationService.T("script_gen.output_label");
        public string ScriptGenUsePsLabel => LocalizationService.T("script_gen.use_ps");
        public string ScriptGenBlocksLabel => LocalizationService.T("script_gen.blocks_label");
        public string ScriptGenPreviewLabel => LocalizationService.T("script_gen.preview_label");
        public string ScriptGenGenerateAllTip => LocalizationService.T("script_gen.generate_all_tip");
        public string BtnSelectAll => LocalizationService.T("btn.select_all");
        public string BtnDeselectAll => LocalizationService.T("btn.deselect_all");
        public string BtnGenerateSelected => LocalizationService.T("script_gen.generate_selected");
        public string BtnGenerateAll => LocalizationService.T("script_gen.generate_all");
        public string BtnCopyPreview => LocalizationService.T("script_gen.copy_preview");
        public string BtnSavePreview => LocalizationService.T("script_gen.save_preview");
        public string BtnOpenOutput => LocalizationService.T("script_gen.open_output");

        public string ScriptUnitsLabel => LocalizationService.T("script_gen.scripts_unit");
        public string CommandUnitsLabel => LocalizationService.T("script_gen.commands_unit");

        // ═══════════════════════════════════════════════════════════════
        // Collections
        // ═══════════════════════════════════════════════════════════════
        public ObservableCollection<KeyValuePair<string, string>> Categories { get; } = new();

        public ObservableCollection<ScriptTemplate> AllTemplates { get; } = new();
        public ObservableCollection<ScriptTemplate> FilteredTemplates { get; } = new();

        KeyValuePair<string, string> _selectedCategory = new("all", "All");
        public KeyValuePair<string, string> SelectedCategory
        {
            get => _selectedCategory;
            set
            {
                if (Set(ref _selectedCategory, value))
                    ApplyFilter();
            }
        }

        string _searchText = "";
        public string SearchText
        {
            get => _searchText;
            set
            {
                if (Set(ref _searchText, value))
                    ApplyFilter();
            }
        }

        ScriptTemplate _selectedTemplate = null!;
        public ScriptTemplate SelectedTemplate
        {
            get => _selectedTemplate;
            set
            {
                if (Set(ref _selectedTemplate, value))
                    UpdatePreview();
            }
        }

        string _projectPath = "";
        public string ProjectPath
        {
            get => _projectPath;
            set
            {
                if (Set(ref _projectPath, value))
                    UpdatePreview();
            }
        }

        string _outputDir = "";
        public string OutputDir
        {
            get => _outputDir;
            set => Set(ref _outputDir, value);
        }

        bool _usePowerShell = false;
        public bool UsePowerShell
        {
            get => _usePowerShell;
            set
            {
                if (Set(ref _usePowerShell, value))
                    UpdatePreview();
            }
        }

        string _previewContent = "";
        public string PreviewContent
        {
            get => _previewContent;
            set => Set(ref _previewContent, value);
        }

        string _statusMessage = "";
        public string StatusMessage
        {
            get => _statusMessage;
            set => Set(ref _statusMessage, value);
        }

        public int SelectedCount => AllTemplates.Count(t => t.IsSelected);
        public int TotalCount => AllTemplates.Count;

        // ═══════════════════════════════════════════════════════════════
        // Commands
        // ═══════════════════════════════════════════════════════════════
        public ICommand BrowseProjectCommand { get; }
        public ICommand BrowseOutputCommand { get; }
        public ICommand SelectAllCommand { get; }
        public ICommand DeselectAllCommand { get; }
        public ICommand GenerateSelectedCommand { get; }
        public ICommand GenerateAllCommand { get; }
        public ICommand CopyPreviewCommand { get; }
        public ICommand SavePreviewCommand { get; }
        public ICommand OpenOutputCommand { get; }

        // ═══════════════════════════════════════════════════════════════
        // Constructor
        // ═══════════════════════════════════════════════════════════════
        public ScriptGeneratorViewModel()
        {
            // Subscribe to culture changes for language refresh
            LocalizationService.CultureChanged += RefreshStrings;
            
            InitCategories();

            // Load templates
            foreach (var t in _service.GetTemplates())
                AllTemplates.Add(t);

            // Default selections
            _projectPath = Directory.Exists(_projectPath)
                ? _projectPath
                : Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);

            _outputDir = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
                "CursorScripts");

            // Select first template
            if (AllTemplates.Count > 0)
            {
                _selectedTemplate = AllTemplates[0];
                // Must call UpdatePreview() here because we set the backing field directly,
                // bypassing the property setter that would normally trigger it
                UpdatePreview();
            }

            ApplyFilter();

            // Commands
            BrowseProjectCommand = new RelayCommand(BrowseProject);
            BrowseOutputCommand = new RelayCommand(BrowseOutput);
            SelectAllCommand = new RelayCommand(_ => SelectAll());
            DeselectAllCommand = new RelayCommand(_ => DeselectAll());
            GenerateSelectedCommand = new RelayCommand(_ => GenerateSelected(), _ => SelectedTemplate != null);
            GenerateAllCommand = new RelayCommand(_ => GenerateAll());
            CopyPreviewCommand = new RelayCommand(_ => CopyPreview(), _ => !string.IsNullOrEmpty(PreviewContent));
            SavePreviewCommand = new RelayCommand(_ => SavePreview(), _ => !string.IsNullOrEmpty(PreviewContent) && SelectedTemplate != null);
            OpenOutputCommand = new RelayCommand(_ => OpenOutput(), _ => Directory.Exists(OutputDir));

            // Wire template changes to preview updates
            foreach (var t in AllTemplates)
            {
                t.PropertyChanged += (_, e) =>
                {
                    if (e.PropertyName == nameof(ScriptTemplate.IsSelected))
                    {
                        OnPropertyChanged(nameof(SelectedCount));
                        ApplyFilter(); // re-filter so selected-only mode could work
                    }
                    if (e.PropertyName == nameof(ScriptTemplate.Blocks))
                        UpdatePreview();
                };

                foreach (var block in t.Blocks)
                {
                    block.PropertyChanged += (s, e) => UpdatePreview();
                }
            }
        }

        // ═══════════════════════════════════════════════════════════════
        // Logic
        // ═══════════════════════════════════════════════════════════════
        void InitCategories()
        {
            string currentKey = _selectedCategory.Key ?? "all";
            Categories.Clear();
            Categories.Add(new KeyValuePair<string, string>("all", LocalizationService.T("script_gen.cat_all")));
            Categories.Add(new KeyValuePair<string, string>("web", LocalizationService.T("script_gen.cat_web")));
            Categories.Add(new KeyValuePair<string, string>("desktop", LocalizationService.T("script_gen.cat_desktop")));
            Categories.Add(new KeyValuePair<string, string>("deploy", LocalizationService.T("script_gen.cat_deploy")));
            Categories.Add(new KeyValuePair<string, string>("database", LocalizationService.T("script_gen.cat_database")));
            Categories.Add(new KeyValuePair<string, string>("ai", LocalizationService.T("script_gen.cat_ai")));
            Categories.Add(new KeyValuePair<string, string>("utility", LocalizationService.T("script_gen.cat_utility")));
            _selectedCategory = Categories.FirstOrDefault(c => c.Key == currentKey);
            if (string.IsNullOrEmpty(_selectedCategory.Key) && Categories.Count > 0)
                _selectedCategory = Categories[0];
            OnPropertyChanged(nameof(SelectedCategory));
        }

        void RefreshStrings()
        {
            InitCategories();
            // Notify all localized properties have changed
            OnPropertyChanged(nameof(ScriptUnitsLabel));
            OnPropertyChanged(nameof(CommandUnitsLabel));
            OnPropertyChanged(nameof(ScriptGenTitle));
            OnPropertyChanged(nameof(ScriptGenSubtitle));
            OnPropertyChanged(nameof(ScriptGenFilterLabel));
            OnPropertyChanged(nameof(ScriptGenProjectLabel));
            OnPropertyChanged(nameof(ScriptGenOutputLabel));
            OnPropertyChanged(nameof(ScriptGenUsePsLabel));
            OnPropertyChanged(nameof(ScriptGenBlocksLabel));
            OnPropertyChanged(nameof(ScriptGenPreviewLabel));
            OnPropertyChanged(nameof(ScriptGenGenerateAllTip));
            OnPropertyChanged(nameof(BtnSelectAll));
            OnPropertyChanged(nameof(BtnDeselectAll));
            OnPropertyChanged(nameof(BtnGenerateSelected));
            OnPropertyChanged(nameof(BtnGenerateAll));
            OnPropertyChanged(nameof(BtnCopyPreview));
            OnPropertyChanged(nameof(BtnSavePreview));
            OnPropertyChanged(nameof(BtnOpenOutput));
            OnPropertyChanged(string.Empty);
        }
        
        void ApplyFilter()
        {
            FilteredTemplates.Clear();
            string cat = _selectedCategory.Key;
            string search = _searchText?.Trim().ToLowerInvariant() ?? "";

            foreach (var t in AllTemplates)
            {
                bool matchCat = cat == "all" ||
                    string.Equals(t.Category, cat, StringComparison.OrdinalIgnoreCase);

                bool matchSearch = string.IsNullOrWhiteSpace(search) ||
                    t.Name.ToLowerInvariant().Contains(search) ||
                    t.Description.ToLowerInvariant().Contains(search);

                if (matchCat && matchSearch)
                    FilteredTemplates.Add(t);
            }
        }

        void UpdatePreview()
        {
            if (SelectedTemplate == null)
            {
                PreviewContent = "";
                return;
            }

            string project = string.IsNullOrWhiteSpace(ProjectPath)
                ? "%USERPROFILE%"
                : ProjectPath;

            PreviewContent = _service.GenerateBat(SelectedTemplate, project, UsePowerShell);
        }

        void BrowseProject(object? _)
        {
            var dialog = new Microsoft.Win32.OpenFolderDialog
            {
                Title = ScriptGenProjectLabel,
                InitialDirectory = Directory.Exists(ProjectPath) ? ProjectPath :
                    Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)
            };
            if (dialog.ShowDialog() == true)
            {
                ProjectPath = dialog.FolderName;
                StatusMessage = $"{LocalizationService.T("script_gen.project_selected")}: {ProjectPath}";
            }
        }

        void BrowseOutput(object? _)
        {
            var dialog = new Microsoft.Win32.OpenFolderDialog
            {
                Title = ScriptGenOutputLabel,
                InitialDirectory = Directory.Exists(OutputDir) ? OutputDir :
                    Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments)
            };
            if (dialog.ShowDialog() == true)
                OutputDir = dialog.FolderName;
        }

        void SelectAll()
        {
            foreach (var t in AllTemplates)
                t.IsSelected = true;
            OnPropertyChanged(nameof(SelectedCount));
        }

        void DeselectAll()
        {
            foreach (var t in AllTemplates)
                t.IsSelected = false;
            OnPropertyChanged(nameof(SelectedCount));
        }

        void GenerateSelected()
        {
            if (SelectedTemplate == null) return;
            SaveOutputDir();
            var result = _service.SaveBat(SelectedTemplate, ProjectPath, OutputDir, UsePowerShell);
            if (result.Success)
            {
                StatusMessage = $"✓ {SelectedTemplate.Name}: {result.Path}";
                OpenOutput();
            }
            else
            {
                StatusMessage = $"✗ Error: {result.Message}";
            }
        }

        void GenerateAll()
        {
            SaveOutputDir();
            var results = _service.SaveAllBats(AllTemplates, ProjectPath, OutputDir);
            int success = results.Count(r => r.Success);
            int failed = results.Count(r => !r.Success);

            if (failed == 0)
                StatusMessage = $"✓ All {success} scripts saved to {OutputDir}";
            else
                StatusMessage = $"✓ {success} saved, ✗ {failed} failed";

            if (success > 0)
                OpenOutput();
        }

        void CopyPreview()
        {
            if (string.IsNullOrEmpty(PreviewContent)) return;
            try
            {
                Clipboard.SetText(PreviewContent);
                StatusMessage = "✓ Script copied to clipboard";
            }
            catch (Exception ex)
            {
                StatusMessage = $"✗ Copy failed: {ex.Message}";
            }
        }

        void SavePreview()
        {
            if (SelectedTemplate == null || string.IsNullOrEmpty(PreviewContent)) return;
            SaveOutputDir();
            var result = _service.SaveBat(SelectedTemplate, ProjectPath, OutputDir, UsePowerShell);
            if (result.Success)
            {
                StatusMessage = $"✓ Saved: {result.Path}";
                OpenOutput();
            }
            else
            {
                StatusMessage = $"✗ Error: {result.Message}";
            }
        }

        void OpenOutput()
        {
            if (!Directory.Exists(OutputDir)) return;
            try
            {
                Process.Start(new ProcessStartInfo
                {
                    FileName = "explorer.exe",
                    Arguments = OutputDir,
                    UseShellExecute = true
                });
            }
            catch (Exception ex)
            {
                StatusMessage = $"✗ Cannot open folder: {ex.Message}";
            }
        }

        void SaveOutputDir()
        {
            if (string.IsNullOrWhiteSpace(OutputDir))
            {
                OutputDir = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
                    "CursorScripts");
            }
            if (!Directory.Exists(OutputDir))
                Directory.CreateDirectory(OutputDir);
        }
    }
}
