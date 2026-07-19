using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CursorSetup
{
    public partial class SetupForm : Form
    {
        // Cached per-tab references for re-localization
        private List<TabPage> allTabPages = new List<TabPage>();
        private Dictionary<TabPage, Label> tabDescLabels = new Dictionary<TabPage, Label>();
        private Dictionary<TabPage, List<(CheckBox sa, Label count, ListView list, string cat)>> tabEntries
            = new Dictionary<TabPage, List<(CheckBox, Label, ListView, string)>>();

        // Categories (components + advanced)
        private Dictionary<string, ListView> categoryListBoxes = new Dictionary<string, ListView>();
        private Dictionary<string, Label> categoryCountLabels = new Dictionary<string, Label>();
        private Dictionary<string, CheckBox> categorySelectAll = new Dictionary<string, CheckBox>();
        // Per-category description lookup: { category -> { itemName -> description } }
        private Dictionary<string, Dictionary<string, string>> categoryDescriptions
            = new Dictionary<string, Dictionary<string, string>>(StringComparer.OrdinalIgnoreCase);

        private string selectedPath;
        private string currentInstallPath;
        private bool isInstalling;

        // Hooks (optional, fail-safe). Set true to enable Python framework
        // integration: pre-scan validates ZIP contents, post-install writes
        // INDEX.json via the cursor_framework.indexer module. Both hooks
        // gracefully degrade if Python is not on PATH. Wired to the Hooks tab
        // checkboxes (default ON) so users can disable either hook.
        private bool enablePreScanHook = true;
        private bool enablePostInstallHook = true;
        private string preScanScript = "-m cursor_framework.indexer --validate";
        private string postInstallScript = "-m cursor_framework.indexer";

        // Discovered categories from ZIP
        private Dictionary<string, List<string>> categoryItems = new Dictionary<string, List<string>>();
        // Selected items per category (user choice)
        private Dictionary<string, HashSet<string>> selectedItems = new Dictionary<string, HashSet<string>>();

        // Display order for tabs
        private static readonly string[] CategoryOrder = new[]
        {
            "rules", "skills", "agents", "commands", "hooks", "knowledge",
            "prompts", "references", "workflows", "templates", "memory", "scripts"
        };

        // Top-level categories that the user MUST always install (core runtime)
        private static readonly HashSet<string> CoreCategories = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
        {
            "scripts", "memory"
        };

        // Name of the embedded ZIP file (sidecar)
        private const string EMBEDDED_ZIP_NAME = "cursor-setup.zip";

        public SetupForm()
        {
            InitializeComponent();

            // Wire up modern paint hooks that the Designer can't express
            // declaratively (OwnerDraw tab strip, themed progress bar, ghost
            // buttons). Single line per control — keep wiring local.
            mainTabs.DrawItem += MainTabs_DrawItem;
            progressBar.Paint += (s, e) => SetupTheme.PaintProgress((ProgressBar)s, e);
            cancelButton.Paint += (s, e) => SetupTheme.PaintGhostButton((Button)s, e);
            cancelButton.MouseEnter += (s, e) => cancelButton.Invalidate();
            cancelButton.MouseLeave += (s, e) => cancelButton.Invalidate();

            installTab = BuildInstallTab();
            mainTabs.TabPages.Add(installTab);
            allTabPages.Add(installTab);

            BuildDynamicTabs();

            // Localize everything on first load (tabs are built in English by
            // default; ApplyLocalization translates to the active Lang.Current).
            ApplyLocalization();

            this.Load += SetupForm_Load;
        }

        private void MainTabs_DrawItem(object sender, DrawItemEventArgs e)
        {
            if (e.Index < 0 || e.Index >= mainTabs.TabPages.Count) return;
            string text = mainTabs.TabPages[e.Index].Text;
            SetupTheme.PaintTab(e, mainTabs, text, e.Index == mainTabs.SelectedIndex);
        }

        private void BuildDynamicTabs()
        {
            TabPage tpComponents = BuildCategoryTab("components_desc",
                new[] { "rules", "skills", "agents", "commands", "hooks", "knowledge" });
            tpComponents.Text = Lang.T("tab.components");
            mainTabs.TabPages.Add(tpComponents);
            allTabPages.Add(tpComponents);

            TabPage tpAdvanced = BuildCategoryTab("advanced_desc",
                new[] { "prompts", "references", "workflows", "templates", "memory", "scripts" });
            tpAdvanced.Text = Lang.T("tab.advanced");
            mainTabs.TabPages.Add(tpAdvanced);
            allTabPages.Add(tpAdvanced);

            buildToolTip.SetToolTip(buildMemoryCheckBox, Lang.T("install.build_memory_tt"));
            buildToolTip.SetToolTip(compileKnowledgeCheckBox, Lang.T("install.compile_knowledge_tt"));
            buildToolTip.SetToolTip(buildIndexCheckBox, Lang.T("install.build_index_tt"));
            buildToolTip.SetToolTip(buildEmbeddingsCheckBox, Lang.T("install.build_embeddings_tt"));
            buildToolTip.SetToolTip(packageFrameworkCheckBox, Lang.T("install.package_framework_tt"));

            // Hooks tab — optional Python framework integration. Built
            // programmatically to avoid editing Designer.cs.
            mainTabs.TabPages.Add(BuildHooksTab());
        }

        // --- Hooks tab (programmatic — no Designer.cs changes) -----------
        private TabPage _hooksTab;
        private CheckBox _hooksPreScanCheckBox;
        private CheckBox _hooksPostInstallCheckBox;
        private TextBox _hooksPreScanScriptBox;
        private TextBox _hooksPostInstallScriptBox;
        private Label _hooksHintLabel;

        private TabPage BuildHooksTab()
        {
            _hooksTab = new TabPage { Name = "hooksTab", BackColor = SetupTheme.FormBack, Padding = new Padding(24, 20, 24, 20) };

            var desc = new Label
            {
                AutoSize = true,
                Font = SetupTheme.FontBody,
                ForeColor = SetupTheme.Slate500,
                Location = new Point(0, 0),
                MaximumSize = new Size(1020, 0),
                Text = Lang.T("hooks.desc"),
            };
            _hooksTab.Controls.Add(desc);

            // Pre-scan card
            Panel preCard = new Panel
            {
                BackColor = SetupTheme.CardBack,
                Location = new Point(0, 56),
                Size = new Size(960, 100),
                Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
            };
            preCard.Paint += (s, e) => SetupTheme.PaintCard(preCard, e);

            int y = 56;
            _hooksPreScanCheckBox = new CheckBox
            {
                AutoSize = true,
                Checked = true,
                Font = SetupTheme.FontLabel,
                ForeColor = SetupTheme.Slate900,
                Location = new Point(20, 14),
                Text = Lang.T("hooks.prescan_label"),
            };
            preCard.Controls.Add(_hooksPreScanCheckBox);

            var preScanHint = new Label
            {
                AutoSize = true,
                ForeColor = SetupTheme.Slate500,
                Location = new Point(40, 40),
                Font = SetupTheme.FontBody,
                Text = Lang.T("hooks.prescan_script_label"),
            };
            preCard.Controls.Add(preScanHint);

            _hooksPreScanScriptBox = new TextBox
            {
                Font = SetupTheme.FontMono,
                ForeColor = SetupTheme.Slate900,
                Location = new Point(40, 62),
                PlaceholderText = "-m cursor_framework.indexer --validate",
                Size = new Size(900, 28),
                BorderStyle = BorderStyle.FixedSingle,
                BackColor = Color.White,
                Text = "-m cursor_framework.indexer --validate",
            };
            preCard.Controls.Add(_hooksPreScanScriptBox);

            _hooksTab.Controls.Add(preCard);

            // Post-install card
            y += 100 + 16;
            Panel postCard = new Panel
            {
                BackColor = SetupTheme.CardBack,
                Location = new Point(0, y),
                Size = new Size(960, 100),
                Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
            };
            postCard.Paint += (s, e) => SetupTheme.PaintCard(postCard, e);

            _hooksPostInstallCheckBox = new CheckBox
            {
                AutoSize = true,
                Checked = true,
                Font = SetupTheme.FontLabel,
                ForeColor = SetupTheme.Slate900,
                Location = new Point(20, 14),
                Text = Lang.T("hooks.postinstall_label"),
            };
            postCard.Controls.Add(_hooksPostInstallCheckBox);

            var postHint = new Label
            {
                AutoSize = true,
                ForeColor = SetupTheme.Slate500,
                Location = new Point(40, 40),
                Font = SetupTheme.FontBody,
                Text = Lang.T("hooks.postinstall_script_label"),
            };
            postCard.Controls.Add(postHint);

            _hooksPostInstallScriptBox = new TextBox
            {
                Font = SetupTheme.FontMono,
                ForeColor = SetupTheme.Slate900,
                Location = new Point(40, 62),
                PlaceholderText = "-m cursor_framework.indexer",
                Size = new Size(900, 28),
                BorderStyle = BorderStyle.FixedSingle,
                BackColor = Color.White,
                Text = "-m cursor_framework.indexer",
            };
            postCard.Controls.Add(_hooksPostInstallScriptBox);

            _hooksTab.Controls.Add(postCard);

            // Footer hint
            y += 100 + 24;
            _hooksHintLabel = new Label
            {
                AutoSize = true,
                Font = new Font("Segoe UI", 9.5F, FontStyle.Italic),
                ForeColor = SetupTheme.Slate500,
                Location = new Point(0, y),
                MaximumSize = new Size(1020, 0),
                Text = Lang.T("hooks.hint"),
            };
            _hooksTab.Controls.Add(_hooksHintLabel);

            // Wire UI state → backing fields. Handlers capture backing
            // fields so /hooks tab reflects changes immediately.
            _hooksPreScanCheckBox.CheckedChanged += (s, e) =>
                enablePreScanHook = _hooksPreScanCheckBox.Checked;
            _hooksPostInstallCheckBox.CheckedChanged += (s, e) =>
                enablePostInstallHook = _hooksPostInstallCheckBox.Checked;
            _hooksPreScanScriptBox.TextChanged += (s, e) =>
                preScanScript = _hooksPreScanScriptBox.Text;
            _hooksPostInstallScriptBox.TextChanged += (s, e) =>
                postInstallScript = _hooksPostInstallScriptBox.Text;

            _hooksTab.Text = Lang.T("tab.hooks");
            return _hooksTab;
        }

        private async void SetupForm_Load(object sender, EventArgs e)
        {
            selectedPath = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                ".cursor"
            );
            pathTextBox.Text = selectedPath;

            string zipPath = FindZipPath();
            if (zipPath == null)
            {
                AppendLog("ERROR: " + Lang.T("scan_archive_not_found"));
                AppendLog(Lang.T("place_zip_hint"));
                if (summaryLabel != null)
                    summaryLabel.Text = "cursor-setup.zip not found";
                return;
            }

            statusLabel.Text = Lang.T("scanning");
            AppendLog("Scanning: " + zipPath);

            try
            {
                await Task.Run(() =>
                {
                    categoryItems = ScanCategoriesFromZip(zipPath);
                });

                // Optional pre-scan hook: validate ZIP via Python framework.
                if (enablePreScanHook)
                {
                    await RunPreScanHookAsync(zipPath);
                }

                PopulateCategoryListBoxes();
                UpdateSummary();
                AppendLog(Lang.T("scanned_log", categoryItems.Count));
                statusLabel.Text = Lang.T("ready_to_install");
            }
            catch (Exception ex)
            {
                AppendLog(Lang.T("scan_error", ex.Message));
                statusLabel.Text = Lang.T("scan_failed");
            }
        }

        private string FindZipPath()
        {
            string exeDir = AppContext.BaseDirectory;
            string[] candidates = new[]
            {
                Path.Combine(exeDir, EMBEDDED_ZIP_NAME),
                Path.Combine(Directory.GetCurrentDirectory(), EMBEDDED_ZIP_NAME)
            };
            string dir = exeDir;
            for (int i = 0; i < 3; i++)
            {
                dir = Directory.GetParent(dir)?.FullName;
                if (string.IsNullOrEmpty(dir)) break;
                candidates = candidates.Concat(new[] { Path.Combine(dir, EMBEDDED_ZIP_NAME) }).ToArray();
            }
            foreach (string c in candidates)
            {
                if (File.Exists(c)) return c;
            }
            return null;
        }

        private Dictionary<string, List<string>> ScanCategoriesFromZip(string zipPath)
        {
            var result = new Dictionary<string, List<string>>(StringComparer.OrdinalIgnoreCase);
            using (var archive = ZipFile.OpenRead(zipPath))
            {
                foreach (var entry in archive.Entries)
                {
                    if (string.IsNullOrEmpty(entry.FullName)) continue;
                    string normalized = entry.FullName.Replace('\\', '/');
                    var parts = normalized.Split('/');
                    if (parts.Length < 2) continue;

                    string topCategory = parts[0];
                    if (!CategoryOrder.Contains(topCategory, StringComparer.OrdinalIgnoreCase))
                        continue;

                    if (!result.ContainsKey(topCategory))
                        result[topCategory] = new List<string>();

                    string groupKey = parts[1];
                    if (!result[topCategory].Contains(groupKey))
                        result[topCategory].Add(groupKey);
                }
            }

            foreach (string c in CategoryOrder)
                if (!result.ContainsKey(c))
                    result[c] = new List<string>();
            return result;
        }

        private string ExtractDescription(string zipPath, string topCategory, string item)
        {
            try
            {
                using (var archive = ZipFile.OpenRead(zipPath))
                {
                    string sampleEntry = FindSampleEntry(archive, topCategory, item);
                    if (sampleEntry == null) return "";

                    var entry = archive.GetEntry(sampleEntry);
                    if (entry == null) return "";

                    const int maxBytes = 8 * 1024;
                    int toRead = (int)Math.Min((long)maxBytes, entry.Length);
                    if (toRead <= 0) return "";

                    byte[] buffer = new byte[toRead];
                    using (var s = entry.Open())
                    {
                        int read = 0;
                        while (read < toRead)
                        {
                            int n = s.Read(buffer, read, toRead - read);
                            if (n <= 0) break;
                            read += n;
                        }
                        if (read < toRead) Array.Resize(ref buffer, read);
                    }

                    string text = System.Text.Encoding.UTF8.GetString(buffer);
                    if (text.Length > 0 && text[0] == '\uFEFF') text = text.Substring(1);

                    return ExtractDescriptionFromText(text, topCategory, item);
                }
            }
            catch
            {
                return "";
            }
        }

        private string FindSampleEntry(ZipArchive archive, string topCategory, string item)
        {
            string prefix = topCategory + "/" + item + "/";
            string[] preferredNames;
            if (string.Equals(topCategory, "skills", StringComparison.OrdinalIgnoreCase))
                preferredNames = new[] { "SKILL.md", "README.md" };
            else if (string.Equals(topCategory, "commands", StringComparison.OrdinalIgnoreCase)
                  || string.Equals(topCategory, "hooks", StringComparison.OrdinalIgnoreCase))
                preferredNames = new[] { "command.md", "hook.md", "README.md", "index.md" };
            else if (string.Equals(topCategory, "knowledge", StringComparison.OrdinalIgnoreCase))
                preferredNames = new[] { "architecture.md", "best-practice.md", "README.md", "faq.md", "glossary.md" };
            else if (string.Equals(topCategory, "templates", StringComparison.OrdinalIgnoreCase))
                preferredNames = new[] { "GETTING-STARTED.md", "README.md", "index.md" };
            else
                preferredNames = new[] { "README.md", "index.md" };

            foreach (string name in preferredNames)
            {
                string p = prefix + name;
                if (archive.GetEntry(p) != null) return p;
            }

            if (string.Equals(topCategory, "rules", StringComparison.OrdinalIgnoreCase)
             || string.Equals(topCategory, "agents", StringComparison.OrdinalIgnoreCase)
             || string.Equals(topCategory, "prompts", StringComparison.OrdinalIgnoreCase)
             || string.Equals(topCategory, "references", StringComparison.OrdinalIgnoreCase)
             || string.Equals(topCategory, "workflows", StringComparison.OrdinalIgnoreCase)
             || string.Equals(topCategory, "memory", StringComparison.OrdinalIgnoreCase)
             || string.Equals(topCategory, "scripts", StringComparison.OrdinalIgnoreCase)
             || string.Equals(topCategory, "templates", StringComparison.OrdinalIgnoreCase))
            {
                string p = topCategory + "/" + item;
                if (archive.GetEntry(p) != null) return p;
            }

            foreach (var e in archive.Entries)
            {
                if (e.FullName.Replace('\\', '/').StartsWith(prefix, StringComparison.OrdinalIgnoreCase)
                    && !string.IsNullOrEmpty(e.Name))
                    return e.FullName;
            }
            return null;
        }

        private string ExtractDescriptionFromText(string text, string topCategory, string item)
        {
            string desc = "";
            string norm = text.Replace("\r\n", "\n").Replace("\r", "\n");
            if (norm.StartsWith("---"))
            {
                int endIdx = norm.IndexOf("\n---", 3);
                if (endIdx > 0)
                {
                    string fm = norm.Substring(3, endIdx - 3);
                    foreach (string rawLine in fm.Split('\n'))
                    {
                        string line = rawLine.Trim();
                        if (line.StartsWith("description:", StringComparison.OrdinalIgnoreCase))
                        {
                            desc = line.Substring("description:".Length).Trim();
                            if (desc.Length >= 2 &&
                                ((desc[0] == '"' && desc[desc.Length - 1] == '"')
                              || (desc[0] == '\'' && desc[desc.Length - 1] == '\'')))
                                desc = desc.Substring(1, desc.Length - 2);
                            break;
                        }
                    }
                }
            }

            if (string.IsNullOrEmpty(desc))
            {
                foreach (string rawLine in norm.Split('\n'))
                {
                    string line = rawLine.Trim().TrimEnd('\r');
                    if (line.Length == 0) continue;
                    if (line.StartsWith("#")) continue;
                    if (line.StartsWith("---")) continue;
                    if (line.StartsWith(">")) continue;
                    if (line.StartsWith("```")) continue;
                    if (System.Text.RegularExpressions.Regex.IsMatch(line, @"^[A-Za-z][A-Za-z _-]{0,30}:\s"))
                        continue;
                    if (line.StartsWith("[") && line.Contains("](")) continue;
                    if (line.StartsWith("1.") || line.StartsWith("2.") || line.StartsWith("3.")) continue;
                    string stripped = line.TrimStart('*', '_', '>', '-', ' ');
                    if (stripped.Length == 0) continue;
                    desc = stripped;
                    break;
                }
            }

            if (string.IsNullOrEmpty(desc)) return "";

            desc = System.Text.RegularExpressions.Regex.Replace(desc, @"\s+", " ").Trim();
            if (desc.Length > 200) desc = desc.Substring(0, 197) + "...";
            return desc;
        }

        private void PopulateCategoryListBoxes()
        {
            string zipPath = FindZipPath();
            foreach (var kv in categoryListBoxes)
            {
                string cat = kv.Key;
                ListView lv = kv.Value;
                lv.Items.Clear();
                lv.BeginUpdate();

                if (!categoryDescriptions.ContainsKey(cat))
                    categoryDescriptions[cat] = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

                if (categoryItems.ContainsKey(cat))
                {
                    var sorted = categoryItems[cat].OrderBy(s => s, StringComparer.OrdinalIgnoreCase).ToArray();
                    foreach (string item in sorted)
                    {
                        string desc = (zipPath != null) ? ExtractDescription(zipPath, cat, item) : "";
                        categoryDescriptions[cat][item] = desc;

                        int index = lv.Items.Count + 1;
                        var lvi = new ListViewItem(index.ToString());
                        lvi.Checked = true;
                        if (lv.Items.Count % 2 == 1)
                            lvi.BackColor = SetupTheme.Slate50;
                        lvi.SubItems.Add(item);
                        string showDesc = string.IsNullOrEmpty(desc) ? Lang.T("no_description") : Lang.Translate(desc);
                        lvi.SubItems.Add(showDesc);
                        lvi.ToolTipText = showDesc;
                        lv.Items.Add(lvi);
                    }
                }
                lv.EndUpdate();
                UpdateCategoryCount(cat);
            }
        }

        private void ApplyLocalization()
        {
            if (this.InvokeRequired)
            {
                this.BeginInvoke(new Action(ApplyLocalization));
                return;
            }
            this.Text = Lang.T("app.title");
            titleLabel.Text = Lang.T("app.title_short");
            subtitleLabel.Text = Lang.T("app.subtitle");
            if (summaryLabel.Text.StartsWith("Components:", StringComparison.OrdinalIgnoreCase)
                || summaryLabel.Text.StartsWith("Thành phần:", StringComparison.OrdinalIgnoreCase))
                UpdateSummary();
            else
                summaryLabel.Text = Lang.T("ready_to_install");

            installPathLabel.Text = Lang.T("install.location");
            installPathHintLabel.Text = Lang.T("install.location_hint");
            browseButton.Text = Lang.T("install.browse");
            newFolderButton.Text = Lang.T("install.new_folder");
            forceCheckBox.Text = Lang.T("install.force");
            cursorCheckBox.Text = Lang.T("install.skip_cursor");
            installTipLabel.Text = Lang.T("install.tip");
            // buildOptionsGroup is now a flat Panel; the title lives in
            // buildHeaderLabel (created in BuildInstallTab). Set via label.
            buildOptionsDescLabel.Text = Lang.T("install.build_options_desc");
            buildMemoryCheckBox.Text = Lang.T("install.build_memory");
            compileKnowledgeCheckBox.Text = Lang.T("install.compile_knowledge");
            buildIndexCheckBox.Text = Lang.T("install.build_index");
            buildEmbeddingsCheckBox.Text = Lang.T("install.build_embeddings");
            packageFrameworkCheckBox.Text = Lang.T("install.package_framework");
            buildNoteLabel.Text = Lang.T("install.build_exe_note");
            if (buildToolTip != null)
            {
                buildToolTip.SetToolTip(buildMemoryCheckBox, Lang.T("install.build_memory_tt"));
                buildToolTip.SetToolTip(compileKnowledgeCheckBox, Lang.T("install.compile_knowledge_tt"));
                buildToolTip.SetToolTip(buildIndexCheckBox, Lang.T("install.build_index_tt"));
                buildToolTip.SetToolTip(buildEmbeddingsCheckBox, Lang.T("install.build_embeddings_tt"));
                buildToolTip.SetToolTip(packageFrameworkCheckBox, Lang.T("install.package_framework_tt"));
            }
            cancelButton.Text = Lang.T("btn.cancel");
            installButton.Text = Lang.T("btn.install");

            int idx = 0;
            foreach (TabPage tp in allTabPages)
            {
                if (idx == 0) tp.Text = Lang.T("tab.install");
                else if (idx == 1) tp.Text = Lang.T("tab.components");
                else if (idx == 2) tp.Text = Lang.T("tab.advanced");
                idx++;
            }

            foreach (var kv in tabEntries)
            {
                TabPage tp = kv.Key;
                if (tabDescLabels.ContainsKey(tp))
                    tabDescLabels[tp].Text = Lang.T(tp == allTabPages[1] ? "components_desc" : "advanced_desc");

                foreach (var entry in kv.Value)
                {
                    var (sa, countLabel, listView, cat) = entry;
                    bool isCore = CoreCategories.Contains(cat);
                    sa.Text = isCore ? Lang.T("always_installed", cat) : Lang.T("select_all", cat);
                    if (listView.Columns.Count >= 3)
                    {
                        listView.Columns[0].Text = Lang.T("column.index");
                        listView.Columns[1].Text = Lang.T("column.component");
                        listView.Columns[2].Text = Lang.T("column.description");
                    }
                    UpdateCategoryCount(cat);
                }
            }
        }

        private void LanguageComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (languageComboBox.SelectedItem is LangItem li)
                Lang.Current = li.Code;
        }

        private void UpdateCategoryCount(string cat)
        {
            if (!categoryListBoxes.ContainsKey(cat)) return;
            ListView lv = categoryListBoxes[cat];
            int total = lv.Items.Count;
            int selected = lv.CheckedItems.Count;
            Label lbl = categoryCountLabels[cat];
            lbl.Text = $"{selected}/{total}";
            lbl.ForeColor = (selected == total) ? SetupTheme.Indigo600 : SetupTheme.Slate500;

            if (categorySelectAll.ContainsKey(cat))
            {
                CheckBox sa = categorySelectAll[cat];
                if (!CoreCategories.Contains(cat))
                    sa.Checked = (selected == total);
            }

            UpdateSummary();
        }

        private void UpdateSummary()
        {
            int total = 0;
            int selected = 0;
            foreach (var kv in categoryListBoxes)
            {
                total += kv.Value.Items.Count;
                selected += kv.Value.CheckedItems.Count;
            }
            if (summaryLabel != null)
                summaryLabel.Text = Lang.T("summary.components", selected, total);
        }

        private void BrowseButton_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog dialog = new FolderBrowserDialog())
            {
                dialog.Description = Lang.T("install.location");
                dialog.ShowNewFolderButton = true;

                if (Directory.Exists(selectedPath))
                    dialog.SelectedPath = selectedPath;
                else
                {
                    try
                    {
                        Directory.CreateDirectory(selectedPath);
                        dialog.SelectedPath = selectedPath;
                        AppendLog(Lang.T("log.created", selectedPath));
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
                    AppendLog("Selected: " + selectedPath);
                }
            }
        }

        private void NewFolderButton_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog dialog = new FolderBrowserDialog())
            {
                dialog.Description = Lang.T("install.location_hint");
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
                            AppendLog(Lang.T("log.created", newPath));
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show(ex.Message, Lang.T("msgbox.dir_error_msg"),
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
                    Lang.T("msgbox.cancel_confirm_msg"),
                    Lang.T("msgbox.cancel_confirm_title"),
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
                        AppendLog(Lang.T("log.using_existing", autoCursorPath));
                    }
                    else if (!Directory.Exists(selectedPath))
                    {
                        try
                        {
                            Directory.CreateDirectory(selectedPath);
                            Directory.CreateDirectory(autoCursorPath);
                            finalInstallPath = autoCursorPath;
                            AppendLog(Lang.T("log.created", selectedPath));
                            AppendLog(Lang.T("log.created", autoCursorPath));
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show(ex.Message, Lang.T("msgbox.dir_error_title"),
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
                            AppendLog(Lang.T("log.created", autoCursorPath));
                        }
                        catch (Exception ex)
                        {
                            MessageBox.Show(ex.Message, Lang.T("msgbox.dir_error_title"),
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
                        AppendLog(Lang.T("log.created", selectedPath));
                    }
                    catch (Exception ex)
                    {
                        MessageBox.Show(ex.Message, Lang.T("msgbox.dir_error_title"),
                            MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }
                }
            }

            isInstalling = true;
            currentInstallPath = finalInstallPath;
            installButton.Enabled = false;
            browseButton.Enabled = false;
            newFolderButton.Enabled = false;
            forceCheckBox.Enabled = false;
            cursorCheckBox.Enabled = false;
            mainTabs.Enabled = false;
            installButton.Text = Lang.T("btn.please_wait");

            var snapshot = SnapshotSelections();
            int totalSelected = snapshot.Sum(kv => kv.Value.Count);
            AppendLog("===========================================");
            AppendLog(Lang.T("log.install_header"));
            AppendLog("===========================================");
            AppendLog(Lang.T("log.install_to", finalInstallPath));
            AppendLog(Lang.T("log.selected_components"));
            foreach (var kv in snapshot)
            {
                if (kv.Value.Count == 0) continue;
                AppendLog("  - " + kv.Key + ": " + kv.Value.Count);
            }
            AppendLog(Lang.T("log.total_selected", totalSelected));

            try
            {
                await RunInstallationAsync(snapshot);
            }
            catch (Exception ex)
            {
                AppendLog("ERROR: " + ex.Message);
                MessageBox.Show(ex.Message, Lang.T("msgbox.error_title"),
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
                isInstalling = false;
                installButton.Enabled = true;
                browseButton.Enabled = true;
                newFolderButton.Enabled = true;
                forceCheckBox.Enabled = true;
                cursorCheckBox.Enabled = true;
                mainTabs.Enabled = true;
            }
        }

        private Dictionary<string, HashSet<string>> SnapshotSelections()
        {
            var snap = new Dictionary<string, HashSet<string>>(StringComparer.OrdinalIgnoreCase);
            foreach (var kv in categoryListBoxes)
            {
                var set = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
                foreach (ListViewItem item in kv.Value.CheckedItems)
                    set.Add(item.Text);
                if (CoreCategories.Contains(kv.Key) && set.Count == 0
                    && categoryItems.ContainsKey(kv.Key))
                {
                    foreach (var x in categoryItems[kv.Key])
                        set.Add(x);
                }
                snap[kv.Key] = set;
            }
            return snap;
        }

        private async Task RunInstallationAsync(Dictionary<string, HashSet<string>> snapshot)
        {
            UpdateProgress(5, Lang.T("log.preparing"));

            if (!cursorCheckBox.Checked)
            {
                AppendLog(Lang.T("log.checking_cursor"));
                if (IsCursorRunning())
                {
                    var result = MessageBox.Show(
                        Lang.T("log.cursor_running_msg"),
                        Lang.T("log.cursor_running_title"),
                        MessageBoxButtons.YesNo,
                        MessageBoxIcon.Warning
                    );
                    if (result != DialogResult.Yes)
                    {
                        AppendLog(Lang.T("log.cancelled_by_user"));
                        return;
                    }
                }
            }

            string zipPath = FindZipPath();
            if (zipPath == null)
            {
                throw new Exception(Lang.T("log.zip_not_found", EMBEDDED_ZIP_NAME));
            }

            AppendLog(Lang.T("log.found_archive", zipPath));

            UpdateProgress(15, Lang.T("log.extracting_files"));
            AppendLog(Lang.T("log.extracting"));

            bool force = forceCheckBox.Checked;

            await ExtractZipAsync(zipPath, currentInstallPath, force, snapshot, 15, 88);

            if (GetSelectedBuildSteps().Count > 0)
            {
                UpdateProgress(89, Lang.T("log.post_install"));
                await RunPostInstallScriptsAsync(currentInstallPath);
            }

            // Optional post-install hook: write INDEX.json via Python framework
            // so the dashboard / workflow module has a fresh asset index ready.
            if (enablePostInstallHook)
            {
                UpdateProgress(96, Lang.T("log.hook_post_install"));
                await RunPostInstallHookAsync(currentInstallPath);
            }

            UpdateProgress(95, Lang.T("log.finalizing"));

            UpdateProgress(100, Lang.T("log.complete"));
            AppendLog("");
            AppendLog("===========================================");
            AppendLog(Lang.T("log.complete_header"));
            AppendLog("===========================================");
            AppendLog(Lang.T("log.installed_to", currentInstallPath));
            AppendLog("");
            AppendLog(Lang.T("log.restart_cursor"));

            MessageBox.Show(
                Lang.T("msgbox.complete_msg", currentInstallPath),
                Lang.T("msgbox.complete_title"),
                MessageBoxButtons.OK,
                MessageBoxIcon.Information
            );
        }

        private async Task ExtractZipAsync(string zipPath, string destDir, bool force,
            Dictionary<string, HashSet<string>> snapshot, int startProgress, int endProgress)
        {
            await Task.Run(() =>
            {
                using (var archive = ZipFile.OpenRead(zipPath))
                {
                    int total = archive.Entries.Count;
                    int current = 0;
                    int progressRange = endProgress - startProgress;
                    int copied = 0;
                    int skipped = 0;
                    int skippedCat = 0;

                    foreach (var entry in archive.Entries)
                    {
                        if (string.IsNullOrEmpty(entry.Name)) continue;

                        current++;

                        if (!ShouldExtractEntry(entry.FullName, snapshot, out string skipReason))
                        {
                            skippedCat++;
                            AppendLog(Lang.T("log.skip_cat_action", entry.FullName, skipReason));
                            UpdateProgress(startProgress + (int)((current * (double)progressRange) / total),
                                Lang.T("log.skipping", current, total));
                            continue;
                        }

                        string filePath = Path.Combine(destDir, entry.FullName);
                        string dir = Path.GetDirectoryName(filePath);

                        if (!string.IsNullOrEmpty(dir))
                            Directory.CreateDirectory(dir);

                        bool extract = true;
                        if (File.Exists(filePath) && !force)
                        {
                            AppendLog(Lang.T("log.skip_action", entry.FullName));
                            extract = false;
                            skipped++;
                        }

                        if (extract)
                        {
                            try
                            {
                                entry.ExtractToFile(filePath, force);
                                AppendLog(Lang.T("log.copy_action", entry.FullName));
                                copied++;
                            }
                            catch (Exception ex)
                            {
                                AppendLog(Lang.T("log.error_action", entry.FullName, ex.Message));
                            }
                        }

                        UpdateProgress(startProgress + (int)((current * (double)progressRange) / total),
                            Lang.T("log.extracting_progress", current, total));
                    }

                    AppendLog("---");
                    AppendLog(Lang.T("log.summary", copied, skipped, skippedCat));
                }
            });
        }

        private TabPage BuildInstallTab()
        {
            TabPage tab = new TabPage { Text = Lang.T("tab.install"), Padding = new Padding(24, 20, 24, 20), BackColor = SetupTheme.FormBack };

            // === Section: Installation Location ============================
            installPathLabel = new Label
            {
                Text = Lang.T("install.location"),
                Font = new Font("Segoe UI Semibold", 11.5F, FontStyle.Bold),
                ForeColor = SetupTheme.Slate900,
                Location = new Point(0, 0),
                AutoSize = true
            };

            installPathHintLabel = new Label
            {
                Text = Lang.T("install.location_hint"),
                Font = SetupTheme.FontBody,
                ForeColor = SetupTheme.Slate500,
                Location = new Point(0, 26),
                AutoSize = true
            };

            // Card panel that wraps the path row — visual grouping
            Panel pathCard = new Panel
            {
                BackColor = SetupTheme.CardBack,
                Location = new Point(0, 58),
                Size = new Size(960, 90),
                Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right,
            };
            pathCard.Paint += (s, e) => SetupTheme.PaintCard(pathCard, e);

            pathTextBox = new TextBox
            {
                Location = new Point(16, 14),
                Size = new Size(720, 28),
                Font = SetupTheme.FontBody,
                ForeColor = SetupTheme.Slate900,
                ReadOnly = true,
                BackColor = Color.White,
                BorderStyle = BorderStyle.None,
                Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
            };

            browseButton = new Button
            {
                Text = Lang.T("install.browse"),
                Location = new Point(745, 8),
                Size = new Size(100, 38),
                Anchor = AnchorStyles.Top | AnchorStyles.Right
            };
            SetupTheme.WireFlatButton(browseButton, SetupTheme.Indigo600, SetupTheme.Indigo500,
                (b, ev) => SetupTheme.PaintButton(b, ev, SetupTheme.Indigo600, SetupTheme.Indigo500));
            browseButton.ForeColor = Color.White;
            browseButton.Font = SetupTheme.FontBody;
            browseButton.Click += BrowseButton_Click;

            newFolderButton = new Button
            {
                Text = Lang.T("install.new_folder"),
                Location = new Point(853, 8),
                Size = new Size(96, 38),
                Anchor = AnchorStyles.Top | AnchorStyles.Right
            };
            SetupTheme.WireFlatButton(newFolderButton, Color.White, SetupTheme.Slate100,
                (b, ev) => SetupTheme.PaintButton(b, ev, Color.White, SetupTheme.Slate100));
            newFolderButton.ForeColor = SetupTheme.Slate700;
            newFolderButton.Font = SetupTheme.FontBody;
            newFolderButton.FlatAppearance.BorderColor = SetupTheme.Slate200;
            newFolderButton.FlatAppearance.BorderSize = 1;
            newFolderButton.Click += NewFolderButton_Click;

            pathCard.Controls.Add(pathTextBox);
            pathCard.Controls.Add(browseButton);
            pathCard.Controls.Add(newFolderButton);

            // === Section: Toggles ===========================================
            Panel togglePanel = new Panel
            {
                BackColor = Color.Transparent,
                Location = new Point(0, 165),
                Size = new Size(960, 64),
                Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
            };

            forceCheckBox = new CheckBox
            {
                Text = Lang.T("install.force"),
                Location = new Point(0, 0),
                AutoSize = true,
                Font = SetupTheme.FontBody,
                ForeColor = SetupTheme.Slate700,
                Anchor = AnchorStyles.Top | AnchorStyles.Left
            };

            cursorCheckBox = new CheckBox
            {
                Text = Lang.T("install.skip_cursor"),
                Location = new Point(0, 30),
                AutoSize = true,
                Font = SetupTheme.FontBody,
                ForeColor = SetupTheme.Slate700,
                Anchor = AnchorStyles.Top | AnchorStyles.Left
            };

            togglePanel.Controls.Add(forceCheckBox);
            togglePanel.Controls.Add(cursorCheckBox);

            installTipLabel = new Label
            {
                Text = "  " + Lang.T("install.tip"),
                Font = new Font("Segoe UI", 9.5F, FontStyle.Italic),
                ForeColor = SetupTheme.Slate500,
                Location = new Point(0, 246),
                AutoSize = true,
                MaximumSize = new Size(960, 0),
                Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
            };

            // === Section: Build Options =====================================
            buildOptionsGroup = new Panel
            {
                Location = new Point(0, 294),
                Size = new Size(960, 220),
                BackColor = SetupTheme.CardBack,
                Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
            };
            buildOptionsGroup.Paint += (s, e) => SetupTheme.PaintCard(buildOptionsGroup, e);

            var buildHeaderLabel = new Label
            {
                Text = Lang.T("install.build_options"),
                Font = new Font("Segoe UI Semibold", 11F, FontStyle.Bold),
                ForeColor = SetupTheme.Slate900,
                Location = new Point(20, 18),
                AutoSize = true
            };

            buildOptionsDescLabel = new Label
            {
                Text = Lang.T("install.build_options_desc"),
                Location = new Point(20, 44),
                Size = new Size(920, 18),
                Font = new Font("Segoe UI", 9F, FontStyle.Italic),
                ForeColor = SetupTheme.Slate500,
                Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
            };

            // Two columns of build checkboxes for a denser, cleaner look
            int colX1 = 20, colX2 = 480;
            int rowH = 28;
            int startY = 76;

            buildMemoryCheckBox = MakeThemedCheckbox(Lang.T("install.build_memory"), new Point(colX1, startY));
            compileKnowledgeCheckBox = MakeThemedCheckbox(Lang.T("install.compile_knowledge"), new Point(colX2, startY));
            buildIndexCheckBox = MakeThemedCheckbox(Lang.T("install.build_index"), new Point(colX1, startY + rowH));
            buildEmbeddingsCheckBox = MakeThemedCheckbox(Lang.T("install.build_embeddings"), new Point(colX2, startY + rowH));
            packageFrameworkCheckBox = MakeThemedCheckbox(Lang.T("install.package_framework"), new Point(colX1, startY + rowH * 2));

            buildNoteLabel = new Label
            {
                Text = "ⓘ  " + Lang.T("install.build_exe_note"),
                Location = new Point(20, 188),
                Size = new Size(920, 18),
                Font = new Font("Segoe UI", 9F, FontStyle.Italic),
                ForeColor = Color.FromArgb(180, 130, 0),
                Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
            };

            buildOptionsGroup.Controls.Add(buildHeaderLabel);
            buildOptionsGroup.Controls.Add(buildOptionsDescLabel);
            buildOptionsGroup.Controls.Add(buildMemoryCheckBox);
            buildOptionsGroup.Controls.Add(compileKnowledgeCheckBox);
            buildOptionsGroup.Controls.Add(buildIndexCheckBox);
            buildOptionsGroup.Controls.Add(buildEmbeddingsCheckBox);
            buildOptionsGroup.Controls.Add(packageFrameworkCheckBox);
            buildOptionsGroup.Controls.Add(buildNoteLabel);

            tab.Controls.AddRange(new Control[]
            {
                installPathLabel, installPathHintLabel, pathCard, togglePanel,
                installTipLabel, buildOptionsGroup
            });
            return tab;
        }

        private static CheckBox MakeThemedCheckbox(string text, Point location)
        {
            return new CheckBox
            {
                Text = text,
                Location = location,
                AutoSize = true,
                Font = SetupTheme.FontBody,
                ForeColor = SetupTheme.Slate700,
                Checked = false,
            };
        }

        public TabPage BuildCategoryTab(string descKey, string[] categories)
        {
            string tabTitle = descKey == "components_desc" ? Lang.T("tab.components") : Lang.T("tab.advanced");
            TabPage tab = new TabPage
            {
                Text = tabTitle,
                Padding = new Padding(24, 20, 24, 20),
                BackColor = SetupTheme.FormBack
            };

            Panel categoryScrollPanel = new Panel
            {
                Dock = DockStyle.Fill,
                AutoScroll = true,
                Padding = new Padding(0),
                BackColor = SetupTheme.FormBack
            };
            tab.Controls.Add(categoryScrollPanel);

            string descText = descKey == "components_desc"
                ? Lang.T("components_desc")
                : Lang.T("advanced_desc");
            Label descLabel = new Label
            {
                Text = descText,
                Font = SetupTheme.FontBody,
                ForeColor = SetupTheme.Slate500,
                Location = new Point(0, 0),
                AutoSize = true,
                MaximumSize = new Size(960, 0),
                Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
            };
            categoryScrollPanel.Controls.Add(descLabel);
            tabDescLabels[tab] = descLabel;

            var entries = new List<(CheckBox sa, Label count, ListView list, string cat)>();

            int y = 36;
            foreach (string cat in categories)
            {
                bool isCore = CoreCategories.Contains(cat);

                // === Per-category card panel (rounded white surface) =========
                Panel catCard = new Panel
                {
                    Location = new Point(0, y),
                    Size = new Size(960, 220),
                    BackColor = SetupTheme.CardBack,
                    Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
                };
                catCard.Paint += (s, e) => SetupTheme.PaintCard(catCard, e);

                // Category header (left: select-all checkbox; right: count chip)
                string selectAllText = isCore
                    ? $"✓  {Lang.T("always_installed", cat)}"
                    : Lang.T("select_all", cat);

                CheckBox selectAll = new CheckBox
                {
                    Text = selectAllText,
                    Location = new Point(16, 16),
                    AutoSize = true,
                    Font = SetupTheme.FontLabel,
                    ForeColor = SetupTheme.Slate900,
                    Checked = true,
                    Enabled = !isCore,
                    Anchor = AnchorStyles.Top | AnchorStyles.Left
                };
                string catCopy = cat;
                selectAll.CheckedChanged += (s, e) =>
                {
                    if (isCore) return;
                    if (categoryListBoxes.ContainsKey(catCopy))
                    {
                        ListView lv = categoryListBoxes[catCopy];
                        foreach (ListViewItem item in lv.Items)
                            item.Checked = selectAll.Checked;
                        UpdateCategoryCount(catCopy);
                    }
                };
                categorySelectAll[cat] = selectAll;
                catCard.Controls.Add(selectAll);

                Label countLabel = new Label
                {
                    Text = "0/0",
                    Location = new Point(880, 18),
                    AutoSize = false,
                    Size = new Size(70, 22),
                    Font = new Font("Segoe UI Semibold", 9F, FontStyle.Bold),
                    ForeColor = SetupTheme.Slate500,
                    TextAlign = ContentAlignment.MiddleRight,
                    Anchor = AnchorStyles.Top | AnchorStyles.Right
                };
                categoryCountLabels[cat] = countLabel;
                catCard.Controls.Add(countLabel);

                // ListView — modern flat surface, no grid lines, themed rows
                ListView listView = new ListView
                {
                    Location = new Point(16, 50),
                    Size = new Size(928, 154),
                    View = View.Details,
                    CheckBoxes = true,
                    FullRowSelect = true,
                    GridLines = false,
                    HideSelection = false,
                    MultiSelect = false,
                    Font = SetupTheme.FontBody,
                    ForeColor = SetupTheme.Slate900,
                    BorderStyle = BorderStyle.None,
                    HeaderStyle = ColumnHeaderStyle.Nonclickable,
                    BackColor = Color.White,
                    OwnerDraw = true,
                    Anchor = AnchorStyles.Top | AnchorStyles.Left | AnchorStyles.Right
                };

                // Header style: subtle, slate-100 background
                listView.Columns.Add("#", 50);
                listView.Columns.Add(Lang.T("column.component"), 200);
                listView.Columns.Add(Lang.T("column.description"), 0);
                listView.DrawColumnHeader += (s, e) =>
                {
                    using (var bg = new SolidBrush(SetupTheme.Slate100))
                        e.Graphics.FillRectangle(bg, e.Bounds);
                    TextRenderer.DrawText(e.Graphics, e.Header.Text,
                        new Font("Segoe UI Semibold", 9F, FontStyle.Bold),
                        new Rectangle(e.Bounds.X + 10, e.Bounds.Y, e.Bounds.Width - 10, e.Bounds.Height),
                        SetupTheme.Slate500,
                        TextFormatFlags.VerticalCenter | TextFormatFlags.EndEllipsis);
                };
                listView.DrawItem += (s, e) => e.DrawDefault = true;
                listView.DrawSubItem += (s, e) =>
                {
                    if (e.ColumnIndex == 0)
                    {
                        // Index column — small slate text, right-aligned
                        TextRenderer.DrawText(e.Graphics, e.SubItem.Text,
                            new Font("Segoe UI", 8.5F), e.Bounds,
                            SetupTheme.Slate400,
                            TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter);
                    }
                    else
                    {
                        e.DrawDefault = true;
                    }
                };

                listView.ColumnWidthChanging += (s, e) =>
                {
                    if (e.ColumnIndex == listView.Columns.Count - 1)
                    {
                        int fixedWidth = listView.Columns[0].Width + listView.Columns[1].Width + SystemInformation.VerticalScrollBarWidth;
                        int newDescWidth = Math.Max(180, listView.ClientSize.Width - fixedWidth);
                        e.NewWidth = newDescWidth;
                    }
                };
                listView.Resize += (s, e) =>
                {
                    int fixedWidth = listView.Columns[0].Width + listView.Columns[1].Width + SystemInformation.VerticalScrollBarWidth;
                    int descWidth = Math.Max(180, listView.ClientSize.Width - fixedWidth);
                    if (listView.Columns[listView.Columns.Count - 1].Width != descWidth)
                        listView.Columns[listView.Columns.Count - 1].Width = descWidth;
                };
                string catCopy2 = cat;
                listView.ItemChecked += (s, e) =>
                {
                    BeginInvoke(new Action(() => UpdateCategoryCount(catCopy2)));
                };
                categoryListBoxes[cat] = listView;
                catCard.Controls.Add(listView);

                categoryScrollPanel.Controls.Add(catCard);
                entries.Add((selectAll, countLabel, listView, cat));
                y += 220 + 12;
            }
            tabEntries[tab] = entries;
            return tab;
        }

        private readonly string[] _buildStepScripts = new string[]
        {
            "memory-builder/build-memory.ps1",
            "knowledge-compiler/compile-knowledge.ps1",
            "project-index-builder/build-index.ps1",
            "embedding-builder/build-embeddings.ps1",
            "packager.ps1",
        };

        private List<CheckBox> GetSelectedBuildSteps()
        {
            var refs = new[] { buildMemoryCheckBox, compileKnowledgeCheckBox, buildIndexCheckBox,
                               buildEmbeddingsCheckBox, packageFrameworkCheckBox };
            return refs.Where(b => b != null && b.Checked).ToList();
        }

        private async Task RunPostInstallScriptsAsync(string installDir)
        {
            string scriptsRoot = Path.Combine(installDir, "scripts");
            string workingDir = installDir;
            if (installDir.EndsWith(".cursor", StringComparison.OrdinalIgnoreCase))
            {
                string parent = Path.GetDirectoryName(installDir);
                if (!string.IsNullOrEmpty(parent)) workingDir = parent;
            }

            var steps = GetSelectedBuildSteps();
            await Task.Run(() =>
            {
                for (int i = 0; i < steps.Count; i++)
                {
                    string scriptRel = _buildStepScripts[i];
                    string scriptPath = Path.Combine(scriptsRoot, scriptRel);
                    AppendLog(Lang.T("log.post_step", scriptRel));
                    var sw = System.Diagnostics.Stopwatch.StartNew();

                    if (!File.Exists(scriptPath))
                    {
                        AppendLog("    [SKIP] file not found: " + scriptPath);
                        continue;
                    }

                    var psi = new System.Diagnostics.ProcessStartInfo
                    {
                        FileName = "powershell.exe",
                        Arguments = "-NoProfile -ExecutionPolicy Bypass -File \"" + scriptPath + "\"",
                        WorkingDirectory = workingDir,
                        UseShellExecute = false,
                        RedirectStandardOutput = true,
                        RedirectStandardError = true,
                        CreateNoWindow = true,
                        StandardOutputEncoding = System.Text.Encoding.UTF8,
                        StandardErrorEncoding = System.Text.Encoding.UTF8,
                    };

                    using (var proc = System.Diagnostics.Process.Start(psi))
                    {
                        proc.OutputDataReceived += (s, e) => { if (e.Data != null) AppendLog("    " + e.Data); };
                        proc.ErrorDataReceived += (s, e) => { if (e.Data != null) AppendLog("    " + e.Data); };
                        proc.BeginOutputReadLine();
                        proc.BeginErrorReadLine();
                        proc.WaitForExit();
                        sw.Stop();

                        if (proc.ExitCode == 0)
                            AppendLog(Lang.T("log.post_done", sw.Elapsed.TotalSeconds));
                        else
                            AppendLog(Lang.T("log.post_failed", proc.ExitCode));
                    }
                }
            });
        }

        private bool ShouldExtractEntry(string entryFullName, Dictionary<string, HashSet<string>> snapshot, out string reason)
        {
            reason = "";
            string normalized = entryFullName.Replace('\\', '/');
            var parts = normalized.Split('/');
            if (parts.Length < 2)
                return true;

            string topCategory = parts[0];
            if (!CategoryOrder.Any(c => string.Equals(c, topCategory, StringComparison.OrdinalIgnoreCase)))
                return true;

            if (CoreCategories.Contains(topCategory))
                return true;

            if (!snapshot.ContainsKey(topCategory))
            {
                reason = "category not selected";
                return false;
            }

            var set = snapshot[topCategory];
            if (set == null || set.Count == 0)
            {
                reason = "category empty";
                return false;
            }

            bool folderBased = string.Equals(topCategory, "skills", StringComparison.OrdinalIgnoreCase)
                || string.Equals(topCategory, "knowledge", StringComparison.OrdinalIgnoreCase)
                || string.Equals(topCategory, "commands", StringComparison.OrdinalIgnoreCase)
                || string.Equals(topCategory, "hooks", StringComparison.OrdinalIgnoreCase)
                || string.Equals(topCategory, "templates", StringComparison.OrdinalIgnoreCase);

            string groupKey = parts[1];

            if (!set.Contains(groupKey))
            {
                reason = folderBased ? "subfolder not selected" : "file not selected";
                return false;
            }
            return true;
        }

        private bool IsCursorRunning()
        {
            var processes = new[] { "Cursor", "Cursor-bin", "cursor", "cursor-bin" };
            foreach (string name in processes)
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
            progressBar.Invalidate(); // re-paint rounded bar
            statusLabel.Text = "●  " + status;
            if (value >= 100)
            {
                statusLabel.ForeColor = SetupTheme.StatusDone;
                summaryLabel.ForeColor = SetupTheme.StatusDone;
            }
            else if (value > 0)
            {
                statusLabel.ForeColor = SetupTheme.StatusActive;
                summaryLabel.ForeColor = SetupTheme.Slate900;
            }
            else
            {
                statusLabel.ForeColor = SetupTheme.StatusIdle;
                summaryLabel.ForeColor = SetupTheme.Slate900;
            }
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

        // --- Python framework hooks (optional, fail-safe) -----------------
        // These hooks bridge the GUI installer to the cursor_framework Python
        // library (Index/Memory/Dashboard). They never block installation —
        // if Python is missing or errors out, we log and continue.

        /// <summary>
        /// Pre-scan hook: invoke `python -m cursor_framework.indexer --validate`
        /// against the ZIP to surface malformed archives before extraction.
        /// Default behavior: skip silently (hook is advisory).
        /// </summary>
        private async Task RunPreScanHookAsync(string zipPath)
        {
            try
            {
                // ponytail: use user-configurable script path from Hooks tab.
                string cmd = string.IsNullOrWhiteSpace(preScanScript)
                    ? "-m cursor_framework.indexer --validate"
                    : preScanScript;
                AppendLog("[hook] pre-scan: " + cmd);
                int code = await RunPythonAsync(
                    cmd + " \"" + zipPath + "\"",
                    timeoutSeconds: 30);
                if (code == 0)
                    AppendLog("[hook] pre-scan: OK");
                else
                    AppendLog("[hook] pre-scan: validator exited " + code + " (non-fatal)");
            }
            catch (Exception ex)
            {
                AppendLog("[hook] pre-scan skipped: " + ex.Message);
            }
        }

        /// <summary>
        /// Post-install hook: write INDEX.json into the installed .cursor/
        /// directory so Dashboard + Workflow modules see a fresh asset index.
        /// </summary>
        private async Task RunPostInstallHookAsync(string installDir)
        {
            try
            {
                string cmd = string.IsNullOrWhiteSpace(postInstallScript)
                    ? "-m cursor_framework.indexer"
                    : postInstallScript;
                AppendLog("[hook] post-install: " + cmd);
                int code = await RunPythonAsync(
                    cmd + " \"" + installDir + "\"",
                    timeoutSeconds: 60);
                if (code == 0)
                    AppendLog("[hook] INDEX.json written at " +
                              Path.Combine(installDir, "INDEX.json"));
                else
                    AppendLog("[hook] indexer exited " + code + " (non-fatal)");
            }
            catch (Exception ex)
            {
                AppendLog("[hook] post-install skipped: " + ex.Message);
            }
        }

        /// <summary>
        /// Run a python command with a hard timeout. Returns process exit code,
        /// or -1 on timeout / python-not-found. Never throws.
        /// </summary>
        private async Task<int> RunPythonAsync(string args, int timeoutSeconds)
        {
            var psi = new System.Diagnostics.ProcessStartInfo("python", args)
            {
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
            };
            using var p = System.Diagnostics.Process.Start(psi);
            if (p == null) return -1;

            var stdoutTask = p.StandardOutput.ReadToEndAsync();
            var stderrTask = p.StandardError.ReadToEndAsync();
            var exitedTask = Task.Run(() => p.WaitForExit(timeoutSeconds * 1000));

            var completed = await Task.WhenAny(exitedTask, Task.Delay(timeoutSeconds * 1000));
            if (completed != exitedTask)
            {
                try { p.Kill(); } catch { }
                return -1;
            }
            await Task.WhenAll(stdoutTask, stderrTask);
            return p.ExitCode;
        }

        [STAThread]
        public static void Main(string[] args)
        {
            // ponytail: --install-zip <path> [--silent] unblocks automated
            // install testing (CI, scripted setup). Silent mode skips UI:
            // extract only, exit 0 success / 1 failure.
            if (args.Length > 0 && args[0] == "--silent")
            {
                string zip = null;
                for (int i = 1; i < args.Length - 1; i++)
                {
                    if (args[i] == "--install-zip") { zip = args[i + 1]; break; }
                }
                if (zip == null)
                {
                    File.WriteAllText("cursor-setup-cli.log",
                        "--silent requires --install-zip <path>\n");
                    Environment.Exit(2);
                }
                int rc = RunSilentInstallAsync(zip).GetAwaiter().GetResult();
                Environment.Exit(rc);
            }

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new SetupForm());
        }

        /// <summary>
        /// Silent-mode installer: extract zip to standard install path,
        /// skip post-install scripts (no UI to gather settings).
        /// Returns process exit code (0 success, 1 failure).
        /// </summary>
        private static async Task<int> RunSilentInstallAsync(string zipPath)
        {
            // ponytail: WinExe suppresses stdio. Redirect to log file so CI
            // can capture results. Path: <zip>.install.log next to input.
            string logPath = zipPath + ".install.log";
            using var log = new StreamWriter(logPath, append: false) { AutoFlush = true };
            try
            {
                if (!File.Exists(zipPath))
                {
                    log.WriteLine($"FAIL: zip not found: {zipPath}");
                    return 1;
                }
                string projectRoot = Directory.GetParent(
                    Directory.GetCurrentDirectory()).FullName;
                string installPath = Path.Combine(projectRoot, ".cursor");
                Directory.CreateDirectory(installPath);

                using (var archive = System.IO.Compression.ZipFile.OpenRead(zipPath))
                {
                    int total = archive.Entries.Count;
                    int current = 0;
                    int copied = 0;
                    foreach (var entry in archive.Entries)
                    {
                        current++;
                        string filePath = Path.Combine(installPath, entry.FullName);
                        if (string.IsNullOrEmpty(entry.Name)) continue; // directory
                        Directory.CreateDirectory(Path.GetDirectoryName(filePath));
                        entry.ExtractToFile(filePath, overwrite: true);
                        copied++;
                        if (current % 50 == 0 || current == total)
                        {
                            log.WriteLine($"[{current}/{total}] {entry.FullName}");
                        }
                    }
                    log.WriteLine($"extracted {copied}/{total} files");
                }
                log.WriteLine($"OK: extracted to {installPath}");
                return 0;
            }
            catch (Exception ex)
            {
                log.WriteLine($"FAIL: {ex.GetType().Name}: {ex.Message}");
                return 1;
            }
        }
    }
}
