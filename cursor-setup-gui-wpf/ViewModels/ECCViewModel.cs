#nullable enable
using System;
using System.Collections.ObjectModel;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using CursorSetupWpf.Helpers;
using CursorSetupWpf.Services;

namespace CursorSetupWpf.ViewModels
{
    public class VibeToolItem : ViewModelBase
    {
        public string Id { get; set; } = "";
        public string Name { get; set; } = "";
        public string GatePrefix { get; set; } = "";
        public string Description { get; set; } = "";
        public bool IsInstalled { get; set; }
        
        // Localized name that updates with culture changes
        public string LocalizedName => LocalizationService.T($"vibe_tool.{Id}");
        public string LocalizedDescription => LocalizationService.T($"vibe_tool.{Id}_desc");
        
        public void RefreshLocalizedProperties()
        {
            OnPropertyChanged(nameof(LocalizedName));
            OnPropertyChanged(nameof(LocalizedDescription));
        }
    }

    public class HarnessItem : ViewModelBase
    {
        string _name = "";
        string _type = "";
        string _description = "";
        string _installPath = "";
        bool _isInstalled;
        bool _supportsHooks;
        bool _hasNativePlugin;

        public string Name { get => _name; set => Set(ref _name, value); }
        public string Type { get => _type; set => Set(ref _type, value); }
        public string Description { get => _description; set => Set(ref _description, value); }
        public string InstallPath { get => _installPath; set => Set(ref _installPath, value); }
        public bool IsInstalled 
        { 
            get => _isInstalled; 
            set 
            { 
                if (Set(ref _isInstalled, value))
                {
                    OnPropertyChanged(nameof(StatusText));
                }
            } 
        }
        public bool SupportsHooks { get => _supportsHooks; set => Set(ref _supportsHooks, value); }
        public bool HasNativePlugin { get => _hasNativePlugin; set => Set(ref _hasNativePlugin, value); }
        
        // Localized status text
        public string InstalledText => LocalizationService.T("ecc.installed");
        public string NotInstalledText => LocalizationService.T("ecc.not_installed");
        public string StatusText => IsInstalled ? InstalledText : NotInstalledText;
        
        // Public method to refresh localized properties when culture changes
        public void RefreshLocalizedProperties()
        {
            OnPropertyChanged(nameof(InstalledText));
            OnPropertyChanged(nameof(NotInstalledText));
            OnPropertyChanged(nameof(StatusText));
        }
    }

    public class InstallProfileItem : ViewModelBase
    {
        string _name = "";
        string _value = "";
        string _description = "";

        public string Name { get => _name; set => Set(ref _name, value); }
        public string Value { get => _value; set => Set(ref _value, value); }
        public string Description { get => _description; set => Set(ref _description, value); }
    }

    public class ECCViewModel : ViewModelBase
    {
        // Labels (using methods that call LocalizationService.T)
        public string ECCTitle => LocalizationService.T("ecc.title");
        public string ECCSubtitle => LocalizationService.T("ecc.subtitle");
        public string StatusLabel => LocalizationService.T("ecc.status");
        public string CloneRepoLabel => LocalizationService.T("ecc.clone");
        public string RefreshStatusLabel => LocalizationService.T("ecc.refresh");
        public string EnableHooksLabel => LocalizationService.T("ecc.hooks");
        public string HarnessesTitle => LocalizationService.T("ecc.harnesses");
        public string FeaturesTitle => LocalizationService.T("ecc.features");
        
        // Static localized labels
        public string AgentsLabel => LocalizationService.T("ecc.agents");
        public string SkillsLabel => LocalizationService.T("ecc.skills");
        public string CommandsLabel => LocalizationService.T("ecc.commands");
        public string HooksMemoryLabel => LocalizationService.T("ecc.hooks_memory");
        public string HooksMemoryDesc => LocalizationService.T("ecc.hooks_memory_desc");
        public string AgentShieldLabel => LocalizationService.T("ecc.agent_shield");
        public string AgentShieldDesc => LocalizationService.T("ecc.agent_shield_desc");
        public string WorkflowLabel => LocalizationService.T("ecc.workflow");
        public string WorkflowDesc => LocalizationService.T("ecc.workflow_desc");
        public string InstallCommandsTitle => LocalizationService.T("ecc.install_commands");
        public string ClaudeCodeLabel => LocalizationService.T("ecc.claude_code");
        public string CodexLabel => LocalizationService.T("ecc.codex");
        public string CursorLabel => LocalizationService.T("ecc.cursor");
        public string GuidedSetupLabel => LocalizationService.T("ecc.guided_setup");
        public string ActiveVibeCoderLabel => LocalizationService.T("ecc.active_vibe_coder");
        public string GateLabel => LocalizationService.T("ecc.gate");
        public string NotInstalledLabel => LocalizationService.T("ecc.not_installed");
        public string InstalledLabel => LocalizationService.T("ecc.installed");
        public string InstallButtonLabel => LocalizationService.T("btn.install");
        
        // ECC Stats
        public string ECCVersion => "2.2.2";
        public int AgentCount => 68;
        public int SkillCount => 292;
        public int CommandCount => 94;

        // Vibe Tool Selector
        public ObservableCollection<VibeToolItem> AvailableVibeTools { get; } = new();
        
        VibeToolItem? _selectedVibeTool;
        public VibeToolItem? SelectedVibeTool
        {
            get => _selectedVibeTool;
            set
            {
                if (Set(ref _selectedVibeTool, value) && value != null)
                {
                    SelectedVibeCoder = value.LocalizedName;
                    GatePrefix = value.GatePrefix;
                }
            }
        }
        
        // Vibe Tool Selector labels
        public string VibeCoderLabel => LocalizationService.T("vibe_coder.label");
        public string SelectVibeCoderLabel => LocalizationService.T("vibe_coder.select");

        // Vibe Coder info (mirrors MainViewModel.SelectedAgent)
        string _selectedVibeCoder = "Cursor IDE";
        public string SelectedVibeCoder
        {
            get => _selectedVibeCoder;
            set => Set(ref _selectedVibeCoder, value);
        }

        string _gatePrefix = "K";
        public string GatePrefix
        {
            get => _gatePrefix;
            set => Set(ref _gatePrefix, value);
        }

        bool _isECCInstalled;
        public bool IsECCInstalled { get => _isECCInstalled; set => Set(ref _isECCInstalled, value); }

        public string InstallStatusText => IsECCInstalled
            ? LocalizationService.T("ecc.installed")
            : LocalizationService.T("ecc.not_installed");

        bool _enableHooks;
        public bool EnableHooks { get => _enableHooks; set => Set(ref _enableHooks, value); }

        // Profile selection
        public ObservableCollection<InstallProfileItem> Profiles { get; } = new();
        InstallProfileItem? _selectedProfile;
        public InstallProfileItem? SelectedProfile
        {
            get => _selectedProfile;
            set
            {
                if (Set(ref _selectedProfile, value))
                    OnPropertyChanged(nameof(SelectedProfileValue));
            }
        }
        public string SelectedProfileValue => SelectedProfile?.Value ?? "core";

        // Harness items
        public ObservableCollection<HarnessItem> HarnessItems { get; } = new();

        // Commands
        public ICommand CloneRepositoryCommand { get; }
        public ICommand RefreshStatusCommand { get; }
        public ICommand InstallHarnessCommand { get; }

        // Logging
        public ObservableCollection<string> LogLines { get; } = new();

        public ECCViewModel()
        {
            // Subscribe to culture changes for language refresh
            LocalizationService.CultureChanged += OnCultureChanged;
            
            // Initialize vibe coding tools
            InitializeVibeTools();
            
            // Initialize profiles
            Profiles.Add(new InstallProfileItem { Name = "Minimal", Value = "minimal", Description = "Rules + Agents" });
            Profiles.Add(new InstallProfileItem { Name = "Core", Value = "core", Description = "Full skills + commands" });
            Profiles.Add(new InstallProfileItem { Name = "Full", Value = "full", Description = "Everything + hooks" });
            _selectedProfile = Profiles.FirstOrDefault(p => p.Value == "core") ?? Profiles.FirstOrDefault();

            // Initialize harnesses
            InitializeHarnesses();

            // Initialize commands
            CloneRepositoryCommand = new AsyncRelayCommand(CloneRepositoryAsync);
            RefreshStatusCommand = new RelayCommand(_ => RefreshStatus());
            InstallHarnessCommand = new AsyncRelayCommand(InstallHarnessAsync);

            // Initial status check
            RefreshStatus();
        }
        
        void OnCultureChanged()
        {
            // Refresh all localized properties when culture changes
            RefreshStrings();
        }
        
        void RefreshStrings()
        {
            // Notify all localized properties have changed
            OnPropertyChanged(nameof(ECCTitle));
            OnPropertyChanged(nameof(ECCSubtitle));
            OnPropertyChanged(nameof(StatusLabel));
            OnPropertyChanged(nameof(CloneRepoLabel));
            OnPropertyChanged(nameof(RefreshStatusLabel));
            OnPropertyChanged(nameof(EnableHooksLabel));
            OnPropertyChanged(nameof(HarnessesTitle));
            OnPropertyChanged(nameof(FeaturesTitle));
            OnPropertyChanged(nameof(AgentsLabel));
            OnPropertyChanged(nameof(SkillsLabel));
            OnPropertyChanged(nameof(CommandsLabel));
            OnPropertyChanged(nameof(HooksMemoryLabel));
            OnPropertyChanged(nameof(HooksMemoryDesc));
            OnPropertyChanged(nameof(AgentShieldLabel));
            OnPropertyChanged(nameof(AgentShieldDesc));
            OnPropertyChanged(nameof(WorkflowLabel));
            OnPropertyChanged(nameof(WorkflowDesc));
            OnPropertyChanged(nameof(InstallCommandsTitle));
            OnPropertyChanged(nameof(ClaudeCodeLabel));
            OnPropertyChanged(nameof(CodexLabel));
            OnPropertyChanged(nameof(CursorLabel));
            OnPropertyChanged(nameof(GuidedSetupLabel));
            OnPropertyChanged(nameof(ActiveVibeCoderLabel));
            OnPropertyChanged(nameof(GateLabel));
            OnPropertyChanged(nameof(NotInstalledLabel));
            OnPropertyChanged(nameof(InstalledLabel));
            OnPropertyChanged(nameof(InstallButtonLabel));
            OnPropertyChanged(nameof(InstallStatusText));
            OnPropertyChanged(nameof(ECCVersion));
            OnPropertyChanged(nameof(AgentCount));
            OnPropertyChanged(nameof(SkillCount));
            OnPropertyChanged(nameof(CommandCount));
            OnPropertyChanged(nameof(VibeCoderLabel));
            OnPropertyChanged(nameof(SelectVibeCoderLabel));
            OnPropertyChanged(nameof(SelectedVibeCoder));
            
            // Refresh vibe tool localized properties
            foreach (var tool in AvailableVibeTools)
            {
                tool.RefreshLocalizedProperties();
            }
            
            // Refresh harness items status text
            foreach (var item in HarnessItems)
            {
                item.RefreshLocalizedProperties();
            }
        }

        void InitializeVibeTools()
        {
            AvailableVibeTools.Clear();
            AvailableVibeTools.Add(new VibeToolItem { Id = "cursor", GatePrefix = "K", Description = "Cursor IDE with AI-powered coding" });
            AvailableVibeTools.Add(new VibeToolItem { Id = "antigravity", GatePrefix = "A", Description = "Antigravity - Next-gen vibe coding" });
            AvailableVibeTools.Add(new VibeToolItem { Id = "codex", GatePrefix = "X", Description = "OpenAI Codex CLI" });
            AvailableVibeTools.Add(new VibeToolItem { Id = "claude_code", GatePrefix = "C", Description = "Anthropic Claude Code" });
            AvailableVibeTools.Add(new VibeToolItem { Id = "grok", GatePrefix = "G", Description = "xAI Grok CLI" });
            AvailableVibeTools.Add(new VibeToolItem { Id = "gemini", GatePrefix = "M", Description = "Google Gemini CLI" });
            AvailableVibeTools.Add(new VibeToolItem { Id = "zed", GatePrefix = "Z", Description = "Zed AI Editor" });
            AvailableVibeTools.Add(new VibeToolItem { Id = "kimi", GatePrefix = "K", Description = "Kimi Code AI" });
            AvailableVibeTools.Add(new VibeToolItem { Id = "copilot", GatePrefix = "H", Description = "GitHub Copilot CLI" });
            
            // Set default selection
            _selectedVibeTool = AvailableVibeTools.FirstOrDefault(t => t.Id == "cursor") 
                ?? AvailableVibeTools.FirstOrDefault();
            if (_selectedVibeTool != null)
            {
                _selectedVibeCoder = _selectedVibeTool.LocalizedName;
                _gatePrefix = _selectedVibeTool.GatePrefix;
            }
        }

        void InitializeHarnesses()
        {
            HarnessItems.Clear();
            HarnessItems.Add(new HarnessItem
            {
                Name = "Claude Code",
                Type = "claude",
                Description = LocalizationService.T("ecc.harness_claude_desc"),
                InstallPath = "~/.claude",
                SupportsHooks = true,
                HasNativePlugin = true,
            });
            HarnessItems.Add(new HarnessItem
            {
                Name = "Codex",
                Type = "codex",
                Description = LocalizationService.T("ecc.harness_codex_desc"),
                InstallPath = "~/.codex",
                SupportsHooks = true,
                HasNativePlugin = true,
            });
            HarnessItems.Add(new HarnessItem
            {
                Name = "Cursor",
                Type = "cursor",
                Description = LocalizationService.T("ecc.harness_cursor_desc"),
                InstallPath = ".cursor",
                SupportsHooks = false,
                HasNativePlugin = false,
            });
            HarnessItems.Add(new HarnessItem
            {
                Name = "Gemini CLI",
                Type = "gemini",
                Description = LocalizationService.T("ecc.harness_gemini_desc"),
                InstallPath = ".gemini",
                SupportsHooks = false,
                HasNativePlugin = false,
            });
            HarnessItems.Add(new HarnessItem
            {
                Name = "Zed",
                Type = "zed",
                Description = LocalizationService.T("ecc.harness_zed_desc"),
                InstallPath = ".zed",
                SupportsHooks = false,
                HasNativePlugin = false,
            });
            HarnessItems.Add(new HarnessItem
            {
                Name = "Kimi Code",
                Type = "kimi",
                Description = LocalizationService.T("ecc.harness_kimi_desc"),
                InstallPath = ".kimi-code",
                SupportsHooks = false,
                HasNativePlugin = false,
            });
            HarnessItems.Add(new HarnessItem
            {
                Name = "GitHub Copilot",
                Type = "copilot",
                Description = LocalizationService.T("ecc.harness_copilot_desc"),
                InstallPath = ".github",
                SupportsHooks = false,
                HasNativePlugin = false,
            });
            HarnessItems.Add(new HarnessItem
            {
                Name = "Antigravity",
                Type = "antigravity",
                Description = LocalizationService.T("ecc.harness_antigravity_desc"),
                InstallPath = ".antigravity",
                SupportsHooks = false,
                HasNativePlugin = false,
            });
        }

        async Task CloneRepositoryAsync(object? _)
        {
            try
            {
                LogLines.Add($"[ECC] {LocalizationService.T("ecc.cloning_repo")}...");

                var cachePath = Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                    ".cache", "cursor-ecc", "ecc");

                // Check if already exists
                if (Directory.Exists(cachePath))
                {
                    LogLines.Add($"[ECC] {LocalizationService.T("ecc.repo_exists")}");
                    IsECCInstalled = true;
                    return;
                }

                // Clone using git
                var gitClone = new Process
                {
                    StartInfo = new ProcessStartInfo
                    {
                        FileName = "git",
                        Arguments = $"clone --branch main --depth 1 https://github.com/affaan-m/ECC \"{cachePath}\"",
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        CreateNoWindow = true,
                    }
                };

                gitClone.Start();
                await gitClone.WaitForExitAsync();

                if (gitClone.ExitCode == 0)
                {
                    LogLines.Add($"[ECC] {LocalizationService.T("ecc.repo_cloned")}: {cachePath}");
                    IsECCInstalled = true;
                    RefreshStatus();
                }
                else
                {
                    var error = await gitClone.StandardError.ReadToEndAsync();
                    LogLines.Add($"[ECC] {LocalizationService.T("ecc.clone_failed")}: {error}");
                }
            }
            catch (Exception ex)
            {
                LogLines.Add($"[ECC] {LocalizationService.T("ecc.error")}: {ex.Message}");
            }
        }

        void RefreshStatus()
        {
            // Check if ECC is installed in common locations
            var possiblePaths = new[]
            {
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".cache", "cursor-ecc", "ecc"),
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".claude"),
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".ecc"),
            };

            IsECCInstalled = possiblePaths.Any(Directory.Exists);

            // Check harness installations
            foreach (var item in HarnessItems)
            {
                var path = item.InstallPath;
                if (path.StartsWith("~"))
                    path = Path.Combine(
                        Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                        path.Substring(2));

                item.IsInstalled = Directory.Exists(path) && File.Exists(Path.Combine(path, ".ecc-installed"));
            }
        }

        async Task InstallHarnessAsync(object? parameter)
        {
            if (parameter is not HarnessItem harness)
                return;

            try
            {
                LogLines.Add($"[ECC] {LocalizationService.T("ecc.installing")} {harness.Name}...");

                // For Claude Code and Codex, use npm
                if (harness.HasNativePlugin)
                {
                    var npmCmd = new Process
                    {
                        StartInfo = new ProcessStartInfo
                        {
                            FileName = "npx",
                            Arguments = $"ecc-universal@2.2.2 install --profile {SelectedProfileValue} --target {harness.Type}",
                            UseShellExecute = false,
                            RedirectStandardOutput = true,
                            RedirectStandardError = true,
                            CreateNoWindow = true,
                        }
                    };

                    npmCmd.Start();
                    await npmCmd.WaitForExitAsync();

                    if (npmCmd.ExitCode == 0)
                    {
                        LogLines.Add($"[ECC] {harness.Name} {LocalizationService.T("ecc.install_success")}");
                        harness.IsInstalled = true;
                    }
                    else
                    {
                        var error = await npmCmd.StandardError.ReadToEndAsync();
                        LogLines.Add($"[ECC] {harness.Name} {LocalizationService.T("ecc.install_failed")}: {error}");
                    }
                }
                else
                {
                    // For other harnesses, use install.sh
                    var cachePath = Path.Combine(
                        Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                        ".cache", "cursor-ecc", "ecc");

                    if (!Directory.Exists(cachePath))
                    {
                        LogLines.Add($"[ECC] {LocalizationService.T("ecc.repo_not_found")}");
                        return;
                    }

                    var installScript = Path.Combine(cachePath,
                        OperatingSystem.IsWindows() ? "install.ps1" : "install.sh");

                    if (!File.Exists(installScript))
                    {
                        LogLines.Add($"[ECC] {LocalizationService.T("ecc.install_script_not_found")}");
                        return;
                    }

                    var args = OperatingSystem.IsWindows()
                        ? $"-File \"{installScript}\" --profile {SelectedProfileValue} --target {harness.Type}"
                        : $"./install.sh --profile {SelectedProfileValue} --target {harness.Type}";

                    var installProc = new Process
                    {
                        StartInfo = new ProcessStartInfo
                        {
                            FileName = OperatingSystem.IsWindows() ? "pwsh" : "bash",
                            Arguments = args,
                            UseShellExecute = false,
                            RedirectStandardOutput = true,
                            RedirectStandardError = true,
                            CreateNoWindow = true,
                            WorkingDirectory = cachePath,
                        }
                    };

                    installProc.Start();
                    await installProc.WaitForExitAsync();

                    if (installProc.ExitCode == 0)
                    {
                        LogLines.Add($"[ECC] {harness.Name} {LocalizationService.T("ecc.install_success")}");
                        harness.IsInstalled = true;
                    }
                    else
                    {
                        var error = await installProc.StandardError.ReadToEndAsync();
                        LogLines.Add($"[ECC] {harness.Name} {LocalizationService.T("ecc.install_failed")}: {error}");
                    }
                }
            }
            catch (Exception ex)
            {
                LogLines.Add($"[ECC] {LocalizationService.T("ecc.error")}: {ex.Message}");
            }
        }
    }
}
