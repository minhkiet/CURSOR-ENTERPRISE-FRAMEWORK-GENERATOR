using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.IO.Compression;
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
        
        private string selectedPath;
        private string currentInstallPath;
        private bool isInstalling;
        
        // Name of the embedded ZIP file (sidecar)
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
            this.Size = new Size(700, 550);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.BackColor = Color.FromArgb(240, 240, 245);
            
            headerPanel = new Panel { Dock = DockStyle.Top, Height = 120, BackColor = Color.FromArgb(30, 60, 114) };
            
            titleLabel = new Label
            {
                Text = "Cursor Enterprise Framework",
                Font = new Font("Segoe UI", 22, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(30, 25),
                AutoSize = true
            };
            
            subtitleLabel = new Label
            {
                Text = "v4.2.0 - Enterprise AI Coding Framework",
                Font = new Font("Segoe UI", 11),
                ForeColor = Color.FromArgb(180, 200, 230),
                Location = new Point(30, 60),
                AutoSize = true
            };
            
            headerPanel.Controls.AddRange(new Control[] { titleLabel, subtitleLabel });
            
            mainPanel = new Panel { Dock = DockStyle.Fill, Padding = new Padding(30, 20, 30, 20) };
            
            Label pathLabel = new Label
            {
                Text = "Installation Location",
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                Location = new Point(30, 20),
                AutoSize = true
            };
            
            Label pathHintLabel = new Label
            {
                Text = "Select where Cursor Enterprise Framework will be installed",
                Font = new Font("Segoe UI", 9),
                ForeColor = Color.Gray,
                Location = new Point(30, 42),
                AutoSize = true
            };
            
            pathTextBox = new TextBox
            {
                Location = new Point(30, 65),
                Size = new Size(500, 30),
                Font = new Font("Segoe UI", 10),
                ReadOnly = true,
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };
            
            browseButton = new Button
            {
                Text = "Browse...",
                Location = new Point(540, 63),
                Size = new Size(90, 32),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(100, 130, 180),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 9)
            };
            browseButton.FlatAppearance.BorderSize = 0;
            browseButton.Click += BrowseButton_Click;
            
            Button newFolderButton = new Button
            {
                Text = "+ New Folder",
                Location = new Point(540, 100),
                Size = new Size(90, 28),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(70, 130, 80),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 8)
            };
            newFolderButton.FlatAppearance.BorderSize = 0;
            newFolderButton.Click += NewFolderButton_Click;
            
            forceCheckBox = new CheckBox
            {
                Text = "Overwrite existing files (--force)",
                Location = new Point(30, 110),
                AutoSize = true,
                Font = new Font("Segoe UI", 9)
            };
            
            cursorCheckBox = new CheckBox
            {
                Text = "Skip Cursor running check",
                Location = new Point(30, 135),
                AutoSize = true,
                Font = new Font("Segoe UI", 9)
            };
            
            statusLabel = new Label
            {
                Text = "Ready to install",
                Location = new Point(30, 165),
                AutoSize = true,
                Font = new Font("Segoe UI", 10),
                ForeColor = Color.FromArgb(50, 50, 50)
            };
            
            progressBar = new ProgressBar
            {
                Location = new Point(30, 190),
                Size = new Size(600, 25),
                Style = ProgressBarStyle.Continuous,
                BackColor = Color.FromArgb(220, 220, 230),
                ForeColor = Color.FromArgb(30, 100, 180)
            };
            
            logTextBox = new TextBox
            {
                Location = new Point(30, 225),
                Size = new Size(600, 130),
                Multiline = true,
                ReadOnly = true,
                BackColor = Color.FromArgb(45, 45, 50),
                ForeColor = Color.FromArgb(200, 200, 200),
                Font = new Font("Consolas", 9),
                ScrollBars = ScrollBars.Vertical
            };
            
            Panel buttonPanel = new Panel { Dock = DockStyle.Bottom, Height = 60, BackColor = Color.FromArgb(235, 235, 240) };
            
            cancelButton = new Button
            {
                Text = "Cancel",
                Location = new Point(420, 12),
                Size = new Size(100, 35),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(200, 200, 205),
                Font = new Font("Segoe UI", 10)
            };
            cancelButton.FlatAppearance.BorderSize = 0;
            cancelButton.Click += CancelButton_Click;
            
            installButton = new Button
            {
                Text = "Install",
                Location = new Point(530, 12),
                Size = new Size(100, 35),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(30, 120, 60),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 10, FontStyle.Bold)
            };
            installButton.FlatAppearance.BorderSize = 0;
            installButton.Click += InstallButton_Click;
            
            buttonPanel.Controls.AddRange(new Control[] { cancelButton, installButton });
            
            mainPanel.Controls.AddRange(new Control[] 
            { 
                pathLabel, pathHintLabel, pathTextBox, browseButton, newFolderButton,
                forceCheckBox, cursorCheckBox, statusLabel, progressBar, logTextBox 
            });
            
            this.Controls.AddRange(new Control[] { mainPanel, buttonPanel, headerPanel });
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
            }
        }
        
        private async Task RunInstallationAsync()
        {
            UpdateProgress(5, "Preparing installation...");
            
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
                // Try looking in parent directories
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
            
            UpdateProgress(15, "Extracting framework files...");
            AppendLog("Extracting framework content...");
            
            bool force = forceCheckBox.Checked;
            
            // Extract ZIP
            await ExtractZipAsync(zipPath, currentInstallPath, force, 15, 90);
            
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
                        if (string.IsNullOrEmpty(entry.Name)) continue; // Skip directories
                        
                        string filePath = Path.Combine(destDir, entry.FullName);
                        string dir = Path.GetDirectoryName(filePath);
                        
                        if (!string.IsNullOrEmpty(dir))
                            Directory.CreateDirectory(dir);
                        
                        bool extract = true;
                        if (File.Exists(filePath) && !force)
                        {
                            AppendLog($"[SKIP] {entry.FullName}");
                            extract = false;
                        }
                        
                        if (extract)
                        {
                            try
                            {
                                entry.ExtractToFile(filePath, force);
                                AppendLog($"[COPY] {entry.FullName}");
                            }
                            catch (Exception ex)
                            {
                                AppendLog($"[ERROR] {entry.FullName}: {ex.Message}");
                            }
                        }
                        
                        current++;
                        int progress = startProgress + (int)((current * (double)progressRange) / total);
                        UpdateProgress(progress, $"Extracting files... {current}/{total}");
                    }
                }
            });
        }
        
        private bool IsCursorRunning()
        {
            var processes = new[] { "Cursor", "Cursor-bin", "cursor", "cursor-bin" };
            foreach (var name in processes)
            {
                var procs = System.Diagnostics.Process.GetProcessesByName(name);
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
