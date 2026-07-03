using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CursorSetup
{
    public class SetupForm : Form
    {
        private Panel headerPanel;
        private Label titleLabel;
        private Label subtitleLabel;
        private Panel mainPanel;
        private TextBox pathTextBox;
        private Button browseButton;
        private Button installButton;
        private Button cancelButton;
        private ProgressBar progressBar;
        private TextBox logTextBox;
        private Label statusLabel;
        private CheckBox forceCheckBox;
        private CheckBox cursorCheckBox;
        private CheckBox buildScriptsCheckBox;
        private CheckBox chkMemory;
        private CheckBox chkKnowledge;
        private CheckBox chkIndex;
        private CheckBox chkEmbeddings;
        private CheckBox chkPackager;

        private string selectedPath;
        private string currentInstallPath;
        private bool isInstalling;

        private const string EMBEDDED_ZIP_NAME = "cursor-setup.zip";

        public SetupForm()
        {
            InitializeComponent();
            this.Load += SetupForm_Load;
        }

        private void SetupForm_Load(object sender, EventArgs e)
        {
            selectedPath = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                ".cursor"
            );
            pathTextBox.Text = selectedPath;
        }

        private void InitializeComponent()
        {
            this.Text = "Cursor Enterprise Framework - Setup";
            this.Size = new Size(820, 720);
            this.MinimumSize = new Size(820, 720);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.BackColor = Color.FromArgb(240, 240, 245);
            this.Font = new Font("Segoe UI", 9);

            // ---------- Header ----------
            headerPanel = new Panel
            {
                Dock = DockStyle.Top,
                Height = 90,
                BackColor = Color.FromArgb(30, 60, 114)
            };

            titleLabel = new Label
            {
                Text = "Cursor Enterprise Framework",
                Font = new Font("Segoe UI", 20, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(25, 15),
                AutoSize = true
            };

            subtitleLabel = new Label
            {
                Text = "v5.0.0 - Enterprise AI Coding Framework",
                Font = new Font("Segoe UI", 10),
                ForeColor = Color.FromArgb(180, 200, 230),
                Location = new Point(25, 50),
                AutoSize = true
            };

            headerPanel.Controls.AddRange(new Control[] { titleLabel, subtitleLabel });

            // ---------- Footer (Buttons) ----------
            Panel buttonPanel = new Panel
            {
                Dock = DockStyle.Bottom,
                Height = 60,
                BackColor = Color.FromArgb(235, 235, 240)
            };

            cancelButton = new Button
            {
                Text = "Cancel",
                Location = new Point(600, 13),
                Size = new Size(95, 34),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(200, 200, 205),
                Font = new Font("Segoe UI", 10),
                Cursor = Cursors.Hand
            };
            cancelButton.FlatAppearance.BorderSize = 0;
            cancelButton.Click += CancelButton_Click;

            installButton = new Button
            {
                Text = "Install",
                Location = new Point(705, 13),
                Size = new Size(95, 34),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(30, 120, 60),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                Cursor = Cursors.Hand
            };
            installButton.FlatAppearance.BorderSize = 0;
            installButton.Click += InstallButton_Click;

            buttonPanel.Controls.AddRange(new Control[] { cancelButton, installButton });

            // ---------- Main content ----------
            mainPanel = new Panel
            {
                Dock = DockStyle.Fill,
                Padding = new Padding(25, 18, 25, 18),
                BackColor = Color.FromArgb(245, 246, 250)
            };

            // Build content via TableLayoutPanel for proper sizing
            var rootTable = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 5,
                AutoSize = false
            };
            rootTable.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));

            // --- Row 1: Path selection ---
            var pathGroup = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 1,
                RowCount = 3,
                AutoSize = false,
                Height = 80
            };
            pathGroup.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            pathGroup.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            pathGroup.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            pathGroup.RowStyles.Add(new RowStyle(SizeType.AutoSize));

            var pathLabel = new Label
            {
                Text = "Installation Location",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                AutoSize = true,
                Margin = new Padding(0, 0, 0, 2)
            };
            var pathHintLabel = new Label
            {
                Text = "Select where Cursor Enterprise Framework will be installed",
                Font = new Font("Segoe UI", 9),
                ForeColor = Color.Gray,
                AutoSize = true,
                Margin = new Padding(0, 0, 0, 6)
            };

            var pathRow = new TableLayoutPanel
            {
                Dock = DockStyle.Fill,
                ColumnCount = 2,
                RowCount = 1,
                AutoSize = false,
                Height = 34
            };
            pathRow.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            pathRow.ColumnStyles.Add(new ColumnStyle(SizeType.Absolute, 100F));

            pathTextBox = new TextBox
            {
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 10),
                ReadOnly = true,
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Margin = new Padding(0, 0, 6, 0)
            };

            browseButton = new Button
            {
                Text = "Browse...",
                Dock = DockStyle.Fill,
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(100, 130, 180),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 9),
                Cursor = Cursors.Hand
            };
            browseButton.FlatAppearance.BorderSize = 0;
            browseButton.Click += BrowseButton_Click;

            pathRow.Controls.Add(pathTextBox, 0, 0);
            pathRow.Controls.Add(browseButton, 1, 0);

            pathGroup.Controls.Add(pathLabel, 0, 0);
            pathGroup.Controls.Add(pathHintLabel, 0, 1);
            pathGroup.Controls.Add(pathRow, 0, 2);

            // --- Row 2: Options ---
            var optionsGroup = new GroupBox
            {
                Text = "Install Options",
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 9, FontStyle.Bold),
                Padding = new Padding(10, 5, 10, 8),
                Margin = new Padding(0, 10, 0, 0),
                Height = 50
            };

            var optionsFlow = new FlowLayoutPanel
            {
                Dock = DockStyle.Fill,
                FlowDirection = FlowDirection.LeftToRight,
                WrapContents = true,
                AutoSize = false
            };

            forceCheckBox = new CheckBox
            {
                Text = "Overwrite existing files (--force)",
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Margin = new Padding(0, 3, 20, 0)
            };

            cursorCheckBox = new CheckBox
            {
                Text = "Skip Cursor running check",
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Margin = new Padding(0, 3, 20, 0)
            };

            optionsFlow.Controls.AddRange(new Control[] { forceCheckBox, cursorCheckBox });
            optionsGroup.Controls.Add(optionsFlow);

            // --- Row 3: Post-install scripts ---
            var scriptsGroup = new GroupBox
            {
                Text = "Post-Install Scripts",
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 9, FontStyle.Bold),
                Padding = new Padding(10, 5, 10, 8),
                Margin = new Padding(0, 10, 0, 0),
                AutoSize = true
            };

            var scriptsOuter = new TableLayoutPanel
            {
                Dock = DockStyle.Top,
                ColumnCount = 1,
                RowCount = 2,
                AutoSize = true
            };
            scriptsOuter.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100F));
            scriptsOuter.RowStyles.Add(new RowStyle(SizeType.AutoSize));
            scriptsOuter.RowStyles.Add(new RowStyle(SizeType.AutoSize));

            buildScriptsCheckBox = new CheckBox
            {
                Text = "Run post-install scripts after extraction",
                AutoSize = true,
                Font = new Font("Segoe UI", 9, FontStyle.Bold),
                Checked = true,
                Margin = new Padding(0, 0, 0, 4),
                ForeColor = Color.FromArgb(30, 100, 180)
            };
            buildScriptsCheckBox.CheckedChanged += BuildScriptsCheckBox_CheckedChanged;

            // Two-column flow for the 5 script checkboxes
            var scriptsFlow = new FlowLayoutPanel
            {
                Dock = DockStyle.Top,
                FlowDirection = FlowDirection.LeftToRight,
                WrapContents = true,
                AutoSize = true,
                Margin = new Padding(20, 2, 0, 0)
            };

            chkMemory = new CheckBox
            {
                Text = "Memory",
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Checked = true,
                Margin = new Padding(0, 2, 14, 0)
            };
            chkKnowledge = new CheckBox
            {
                Text = "Knowledge",
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Checked = true,
                Margin = new Padding(0, 2, 14, 0)
            };
            chkIndex = new CheckBox
            {
                Text = "Index",
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Checked = true,
                Margin = new Padding(0, 2, 14, 0)
            };
            chkEmbeddings = new CheckBox
            {
                Text = "Embeddings",
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Checked = true,
                Margin = new Padding(0, 2, 14, 0)
            };
            chkPackager = new CheckBox
            {
                Text = "Packager",
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Checked = true,
                Margin = new Padding(0, 2, 14, 0)
            };

            scriptsFlow.Controls.AddRange(new Control[]
            {
                chkMemory, chkKnowledge, chkIndex, chkEmbeddings, chkPackager
            });

            scriptsOuter.Controls.Add(buildScriptsCheckBox, 0, 0);
            scriptsOuter.Controls.Add(scriptsFlow, 0, 1);
            scriptsGroup.Controls.Add(scriptsOuter);

            // --- Row 4: Status + Progress bar ---
            var statusPanel = new Panel
            {
                Dock = DockStyle.Top,
                Height = 50,
                Margin = new Padding(0, 10, 0, 0)
            };

            statusLabel = new Label
            {
                Text = "Ready to install",
                Location = new Point(0, 0),
                AutoSize = true,
                Font = new Font("Segoe UI", 10),
                ForeColor = Color.FromArgb(50, 50, 50)
            };

            progressBar = new ProgressBar
            {
                Location = new Point(0, 24),
                Size = new Size(770, 20),
                Style = ProgressBarStyle.Continuous,
                BackColor = Color.FromArgb(220, 220, 230),
                ForeColor = Color.FromArgb(30, 100, 180),
                Anchor = AnchorStyles.Left | AnchorStyles.Right | AnchorStyles.Top
            };

            statusPanel.Controls.AddRange(new Control[] { statusLabel, progressBar });

            // --- Row 5: Log area ---
            var logGroup = new GroupBox
            {
                Text = "Installation Log",
                Dock = DockStyle.Fill,
                Font = new Font("Segoe UI", 9, FontStyle.Bold),
                Padding = new Padding(8, 5, 8, 8),
                Margin = new Padding(0, 10, 0, 0)
            };

            logTextBox = new TextBox
            {
                Dock = DockStyle.Fill,
                Multiline = true,
                ReadOnly = true,
                BackColor = Color.FromArgb(30, 30, 35),
                ForeColor = Color.FromArgb(200, 220, 200),
                Font = new Font("Consolas", 9),
                ScrollBars = ScrollBars.Vertical,
                BorderStyle = BorderStyle.None
            };

            logGroup.Controls.Add(logTextBox);

            // --- Assemble rootTable ---
            rootTable.RowStyles.Add(new RowStyle(SizeType.Absolute, 90F));   // path
            rootTable.RowStyles.Add(new RowStyle(SizeType.Absolute, 60F));   // options
            rootTable.RowStyles.Add(new RowStyle(SizeType.AutoSize));         // scripts
            rootTable.RowStyles.Add(new RowStyle(SizeType.Absolute, 55F));   // status+progress
            rootTable.RowStyles.Add(new RowStyle(SizeType.Percent, 100F));   // log

            rootTable.Controls.Add(pathGroup, 0, 0);
            rootTable.Controls.Add(optionsGroup, 0, 1);
            rootTable.Controls.Add(scriptsGroup, 0, 2);
            rootTable.Controls.Add(statusPanel, 0, 3);
            rootTable.Controls.Add(logGroup, 0, 4);

            mainPanel.Controls.Add(rootTable);

            this.Controls.AddRange(new Control[] { mainPanel, buttonPanel, headerPanel });
        }

        private void BuildScriptsCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            bool enabled = buildScriptsCheckBox.Checked;
            chkMemory.Enabled = enabled;
            chkKnowledge.Enabled = enabled;
            chkIndex.Enabled = enabled;
            chkEmbeddings.Enabled = enabled;
            chkPackager.Enabled = enabled;
        }

        private void BrowseButton_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog dialog = new FolderBrowserDialog())
            {
                dialog.Description = "Select installation folder for Cursor Enterprise Framework";
                dialog.ShowNewFolderButton = true;

                if (Directory.Exists(selectedPath))
                    dialog.SelectedPath = selectedPath;
                else
                {
                    try
                    {
                        Directory.CreateDirectory(selectedPath);
                        dialog.SelectedPath = selectedPath;
                        AppendLog($"Created directory: {selectedPath}");
                    }
                    catch
                    {
                        dialog.SelectedPath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                    }
                }

                if (dialog.ShowDialog() == DialogResult.OK)
                {
                    selectedPath = dialog.SelectedPath;
                    pathTextBox.Text = selectedPath;
                    AppendLog($"Selected: {selectedPath}");
                }
            }
        }

        private void NewFolderButton_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog dialog = new FolderBrowserDialog())
            {
                dialog.Description = "Select parent folder - a new .cursor folder will be created";
                dialog.ShowNewFolderButton = true;

                string parentPath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                if (Directory.Exists(selectedPath))
                    parentPath = Path.GetDirectoryName(selectedPath);
                dialog.SelectedPath = parentPath;

                if (dialog.ShowDialog() == DialogResult.OK)
                {
                    string newPath = Path.Combine(dialog.SelectedPath, ".cursor");

                    if (!Directory.Exists(newPath))
                    {
                        try
                        {
                            Directory.CreateDirectory(newPath);
                            AppendLog($"Created: {newPath}");
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show($"Could not create folder: {ex.Message}", "Error",
                                MessageBoxButtons.OK, MessageBoxIcon.Error);
                            return;
                        }
                    }

                    selectedPath = newPath;
                    pathTextBox.Text = selectedPath;
                }
            }
        }

        private void CancelButton_Click(object sender, EventArgs e)
        {
            if (isInstalling)
            {
                var result = MessageBox.Show(
                    "Installation in progress. Are you sure you want to cancel?",
                    "Confirm Cancel",
                    MessageBoxButtons.YesNo,
                    MessageBoxIcon.Warning
                );
                if (result == DialogResult.Yes)
                    Application.Exit();
            }
            else
                Application.Exit();
        }

        private async void InstallButton_Click(object sender, EventArgs e)
        {
            if (isInstalling) return;

            string finalInstallPath = selectedPath;

            if (!Directory.Exists(selectedPath) ||
                (Directory.Exists(selectedPath) && !Path.GetFileName(selectedPath).Equals(".cursor", StringComparison.OrdinalIgnoreCase)))
            {
                string autoCursorPath = Path.Combine(selectedPath, ".cursor");

                if (!selectedPath.EndsWith(".cursor", StringComparison.OrdinalIgnoreCase))
                {
                    if (Directory.Exists(autoCursorPath))
                    {
                        finalInstallPath = autoCursorPath;
                        AppendLog($"Using existing .cursor folder: {autoCursorPath}");
                    }
                    else if (!Directory.Exists(selectedPath))
                    {
                        try
                        {
                            Directory.CreateDirectory(selectedPath);
                            Directory.CreateDirectory(autoCursorPath);
                            finalInstallPath = autoCursorPath;
                            AppendLog($"Created: {selectedPath}");
                            AppendLog($"Created: {autoCursorPath}");
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show($"Could not create directory: {ex.Message}", "Error",
                                MessageBoxButtons.OK, MessageBoxIcon.Error);
                            return;
                        }
                    }
                    else
                    {
                        try
                        {
                            Directory.CreateDirectory(autoCursorPath);
                            finalInstallPath = autoCursorPath;
                            AppendLog($"Created: {autoCursorPath}");
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show($"Could not create directory: {ex.Message}", "Error",
                                MessageBoxButtons.OK, MessageBoxIcon.Error);
                            return;
                        }
                    }
                }
                else
                {
                    try
                    {
                        Directory.CreateDirectory(selectedPath);
                        AppendLog($"Created: {selectedPath}");
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show($"Could not create directory: {ex.Message}", "Error",
                            MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }
                }
            }

            isInstalling = true;
            currentInstallPath = finalInstallPath;
            installButton.Enabled = false;
            browseButton.Enabled = false;
            forceCheckBox.Enabled = false;
            cursorCheckBox.Enabled = false;
            buildScriptsCheckBox.Enabled = false;
            chkMemory.Enabled = false;
            chkKnowledge.Enabled = false;
            chkIndex.Enabled = false;
            chkEmbeddings.Enabled = false;
            chkPackager.Enabled = false;

            AppendLog("===========================================");
            AppendLog("Cursor Enterprise Framework Setup");
            AppendLog("===========================================");
            AppendLog($"Install to: {finalInstallPath}");

            try
            {
                await RunInstallationAsync();
            }
            catch (Exception ex)
            {
                AppendLog($"ERROR: {ex.Message}");
                MessageBox.Show($"Installation failed: {ex.Message}", "Error",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
                isInstalling = false;
                installButton.Enabled = true;
                browseButton.Enabled = true;
                forceCheckBox.Enabled = true;
                cursorCheckBox.Enabled = true;
                buildScriptsCheckBox.Enabled = true;
                chkMemory.Enabled = true;
                chkKnowledge.Enabled = true;
                chkIndex.Enabled = true;
                chkEmbeddings.Enabled = true;
                chkPackager.Enabled = true;
            }
        }

        private async Task RunInstallationAsync()
        {
            UpdateProgress(3, "Preparing installation...");

            if (!cursorCheckBox.Checked)
            {
                AppendLog("Checking if Cursor IDE is running...");
                if (IsCursorRunning())
                {
                    var result = MessageBox.Show(
                        "Cursor IDE appears to be running. Please close it before installation.\n\nClick 'Yes' to continue anyway, or 'No' to cancel.",
                        "Cursor Running",
                        MessageBoxButtons.YesNo,
                        MessageBoxIcon.Warning
                    );
                    if (result != DialogResult.Yes)
                    {
                        AppendLog("Installation cancelled by user.");
                        return;
                    }
                }
            }

            // Find the ZIP file (sidecar in same directory as exe)
            string exeDir = AppContext.BaseDirectory;
            string zipPath = Path.Combine(exeDir, EMBEDDED_ZIP_NAME);

            if (!File.Exists(zipPath))
            {
                string dir = exeDir;
                for (int i = 0; i < 3; i++)
                {
                    dir = Directory.GetParent(dir)?.FullName;
                    if (string.IsNullOrEmpty(dir)) break;
                    zipPath = Path.Combine(dir, EMBEDDED_ZIP_NAME);
                    if (File.Exists(zipPath)) break;
                }
            }

            if (!File.Exists(zipPath))
            {
                throw new Exception($"Framework archive not found: {EMBEDDED_ZIP_NAME}\n\nPlease ensure cursor-setup.zip is in the same folder as cursor-setup.exe.");
            }

            AppendLog($"Found framework archive: {zipPath}");

            UpdateProgress(8, "Extracting framework files...");
            AppendLog("Extracting framework content...");

            bool force = forceCheckBox.Checked;

            // Extract ZIP
            await ExtractZipAsync(zipPath, currentInstallPath, force, 8, 55);

            UpdateProgress(58, "Finalizing extraction...");

            // Run post-install scripts if enabled
            if (buildScriptsCheckBox.Checked)
            {
                AppendLog("");
                AppendLog("Running post-install scripts...");
                await RunPostInstallScriptsAsync();
            }

            UpdateProgress(95, "Finalizing...");

            UpdateProgress(100, "Installation complete!");
            AppendLog("");
            AppendLog("===========================================");
            AppendLog("Installation completed successfully!");
            AppendLog("===========================================");
            AppendLog($"Installed to: {currentInstallPath}");
            AppendLog("");
            AppendLog("Please restart Cursor IDE to load the new components.");

            MessageBox.Show(
                $"Cursor Enterprise Framework installed successfully!\n\nLocation: {currentInstallPath}\n\nPlease restart Cursor IDE.",
                "Installation Complete",
                MessageBoxButtons.OK,
                MessageBoxIcon.Information
            );
        }

        private async Task RunPostInstallScriptsAsync()
        {
            AppendLog("");
            AppendLog("===========================================");
            AppendLog("Running Post-Install Scripts");
            AppendLog("===========================================");

            string scriptsBase = Path.Combine(currentInstallPath, ".cursor", "scripts");

            // Define all available scripts with their checkbox references
            var allScripts = new[]
            {
                new { Name = "Memory Builder",     Path = Path.Combine(scriptsBase, "memory-builder", "build-memory.ps1"),          Checked = chkMemory },
                new { Name = "Knowledge Compiler",Path = Path.Combine(scriptsBase, "knowledge-compiler", "compile-knowledge.ps1"), Checked = chkKnowledge },
                new { Name = "Project Index",      Path = Path.Combine(scriptsBase, "project-index-builder", "build-index.ps1"),    Checked = chkIndex },
                new { Name = "Embeddings Builder", Path = Path.Combine(scriptsBase, "embedding-builder", "build-embeddings.ps1"),   Checked = chkEmbeddings },
                new { Name = "Framework Packager", Path = Path.Combine(scriptsBase, "packager.ps1"),                               Checked = chkPackager },
            };

            // Filter only selected scripts
            var scripts = allScripts.Where(s => s.Checked.Checked).ToArray();

            if (scripts.Length == 0)
            {
                AppendLog("No scripts selected. Skipping post-install.");
                return;
            }

            int total = scripts.Length;
            int current = 0;

            foreach (var script in scripts)
            {
                current++;
                int progressBase = 55 + (int)((current / (double)total) * 38);
                string stepStatus = $"[{current}/{total}] {script.Name}...";
                UpdateProgress(progressBase, stepStatus);

                if (!File.Exists(script.Path))
                {
                    AppendLog($"[SKIP] {script.Name} - script not found: {Path.GetFileName(script.Path)}");
                    continue;
                }

                AppendLog($"[RUN ] {script.Name}");
                AppendLog($"       {script.Path}");

                try
                {
                    await RunPowerShellScriptAsync(script.Path, "");
                    AppendLog($"[ OK ] {script.Name} - completed");
                }
                catch (Exception ex)
                {
                    AppendLog($"[WARN] {script.Name} - {ex.Message}");
                }

                await Task.Delay(200);
            }

            AppendLog("");
            AppendLog("Post-install scripts finished.");
        }

        private async Task RunPowerShellScriptAsync(string scriptPath, string arguments)
        {
            var psi = new ProcessStartInfo
            {
                FileName = "powershell.exe",
                Arguments = $"-ExecutionPolicy Bypass -NoProfile -File \"{scriptPath}\" {arguments}",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                WorkingDirectory = currentInstallPath,
                StandardOutputEncoding = Encoding.UTF8,
                StandardErrorEncoding = Encoding.UTF8
            };

            using (var process = new Process { StartInfo = psi })
            {
                var outputBuilder = new StringBuilder();
                var errorBuilder = new StringBuilder();

                process.OutputDataReceived += (s, e) =>
                {
                    if (!string.IsNullOrWhiteSpace(e.Data))
                    {
                        this.BeginInvoke(new Action(() =>
                        {
                            AppendLog($"       {e.Data.Trim()}");
                        }));
                    }
                };
                process.ErrorDataReceived += (s, e) =>
                {
                    if (!string.IsNullOrWhiteSpace(e.Data))
                    {
                        this.BeginInvoke(new Action(() =>
                        {
                            AppendLog($"       [ERR] {e.Data.Trim()}");
                        }));
                    }
                };

                process.Start();
                process.BeginOutputReadLine();
                process.BeginErrorReadLine();

                await Task.Run(() => process.WaitForExit(300000)); // 5 min timeout

                if (!process.HasExited)
                {
                    process.Kill();
                    throw new Exception("Script timed out (>5 min)");
                }

                if (process.ExitCode != 0)
                {
                    throw new Exception($"Script exited with code {process.ExitCode}");
                }
            }
        }

        private async Task ExtractZipAsync(string zipPath, string destDir, bool force, int startProgress, int endProgress)
        {
            await Task.Run(() =>
            {
                using (var archive = ZipFile.OpenRead(zipPath))
                {
                    int total = archive.Entries.Count;
                    int current = 0;
                    int progressRange = endProgress - startProgress;

                    foreach (var entry in archive.Entries)
                    {
                        if (string.IsNullOrEmpty(entry.Name)) continue;

                        string filePath = Path.Combine(destDir, entry.FullName);
                        string dir = Path.GetDirectoryName(filePath);

                        if (!string.IsNullOrEmpty(dir))
                            Directory.CreateDirectory(dir);

                        bool extract = true;
                        if (File.Exists(filePath) && !force)
                        {
                            extract = false;
                        }

                        if (extract)
                        {
                            try
                            {
                                entry.ExtractToFile(filePath, force);
                                if (current % 20 == 0)
                                {
                                    int prog = startProgress + (int)((current * (double)progressRange) / total);
                                    UpdateProgress(prog, $"Extracting files... {current}/{total}");
                                }
                            }
                            catch (Exception ex)
                            {
                                this.BeginInvoke(new Action(() => AppendLog($"[ERROR] {entry.FullName}: {ex.Message}")));
                            }
                        }

                        current++;
                    }
                }
            });
        }

        private bool IsCursorRunning()
        {
            var processes = new[] { "Cursor", "Cursor-bin", "cursor", "cursor-bin" };
            foreach (var name in processes)
            {
                var procs = Process.GetProcessesByName(name);
                if (procs.Length > 0)
                    return true;
            }
            return false;
        }

        private void UpdateProgress(int value, string status)
        {
            if (this.InvokeRequired)
            {
                this.BeginInvoke(new Action(() => UpdateProgress(value, status)));
                return;
            }
            progressBar.Value = Math.Min(value, 100);
            statusLabel.Text = status;
            statusLabel.Refresh();
        }

        private void AppendLog(string message)
        {
            if (this.InvokeRequired)
            {
                this.BeginInvoke(new Action(() => AppendLog(message)));
                return;
            }
            logTextBox.AppendText(message + Environment.NewLine);
            logTextBox.SelectionStart = logTextBox.Text.Length;
            logTextBox.ScrollToCaret();
        }

        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new SetupForm());
        }
    }
}
