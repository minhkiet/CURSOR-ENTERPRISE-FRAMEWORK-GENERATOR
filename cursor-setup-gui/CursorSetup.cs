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
    /// <summary>
    /// Lightweight i18n loader. Reads key=value pairs from Resources/{culture}.txt.
    /// Falls back to English when a key is missing in the active language.
    /// Default culture is Vietnamese ("vi").
    /// </summary>
    internal static class Lang
    {
        public const string DefaultCulture = "vi";
        private static readonly Dictionary<string, Dictionary<string, string>> _cache
            = new Dictionary<string, Dictionary<string, string>>(StringComparer.OrdinalIgnoreCase);
        private static string _current = DefaultCulture;

        public static event Action OnChanged;

        public static string Current
        {
            get { return _current; }
            set
            {
                if (string.Equals(_current, value, StringComparison.OrdinalIgnoreCase)) return;
                _current = value;
                if (OnChanged != null) OnChanged();
            }
        }

        public static string T(string key, params object[] args)
        {
            string value = Lookup(_current, key) ?? Lookup("en", key) ?? key;
            if (args != null && args.Length > 0)
                return string.Format(value, args);
            return value;
        }

        private static string Lookup(string culture, string key)
        {
            if (!_cache.ContainsKey(culture))
                _cache[culture] = Load(culture);
            string v;
            _cache[culture].TryGetValue(key, out v);
            return v;
        }

        private static Dictionary<string, string> Load(string culture)
        {
            var dict = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
            try
            {
                string path = Path.Combine(AppContext.BaseDirectory, "Resources", culture + ".txt");
                if (!File.Exists(path)) return dict;
                foreach (string raw in File.ReadAllLines(path))
                {
                    string line = raw.Trim();
                    if (line.Length == 0 || line.StartsWith("#")) continue;
                    int eq = line.IndexOf('=');
                    if (eq < 0) continue;
                    string k = line.Substring(0, eq).Trim();
                    string v = line.Substring(eq + 1).Trim();
                    dict[k] = v.Replace("\\n", "\n");
                }
            }
            catch { }
            return dict;
        }

        // ponytail: small English -> Vietnamese phrase dictionary for component descriptions.
        // Long descriptions are not translated (would need a real i18n DB); we only rewrite
        // the common leading clauses so the user gets a gist of what the component does.
        private static readonly Dictionary<string, string> _descVi = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
        {
            // ==== Skills ====
            { "Karpathy Coding Discipline", "Kỷ luật lập trình Karpathy" },
            { "Think Before Coding", "Suy nghĩ trước khi code" },
            { "Simplicity First", "Đơn giản là trên hết" },
            { "Surgical Changes", "Thay đổi có chọn lọc" },
            { "Goal-Driven Execution", "Thực thi theo mục tiêu" },
            { "Mandatory overlay for all coding tasks", "Lớp kỹ năng bắt buộc cho mọi task code" },
            { "Complements ponytail for YAGNI optimization", "Bổ sung cho ponytail để tối ưu YAGNI" },
            { "Comprehensive frontend code review skill", "Kỹ năng review frontend toàn diện" },
            { "with mandatory pre-review scope analysis", "kèm phân tích phạm vi trước review" },
            { "and post-review quality gates", "và gate chất lượng sau review" },
            { "Reviews for correctness, design quality, accessibility, performance, and taste",
              "Review tính đúng đắn, chất lượng thiết kế, accessibility, hiệu năng và thẩm mỹ" },
            { "Ponytail Skill - Lazy Senior Dev Mode", "Ponytail - Chế độ lập trình viên lười nhưng cao cấp" },
            { "Lazy Senior Dev Mode for Cursor Enterprise Framework", "Chế độ senior dev lười cho Cursor Enterprise Framework" },
            { "YAGNI optimization, minimal code", "Tối ưu YAGNI, code tối thiểu" },
            { "Complementary to karpathy-coding", "Bổ trợ cho karpathy-coding" },
            { "think first, then minimize", "nghĩ trước, rồi giảm thiểu" },
            { "Cursor Canvas is a live React app", "Cursor Canvas là ứng dụng React chạy trực tiếp" },
            { "the user can open beside the chat", "người dùng có thể mở cạnh khung chat" },
            { "mandatory pre-review scope analysis", "phân tích phạm vi trước review (bắt buộc)" },
            { "You MUST also read this skill", "Bạn PHẢI đọc skill này" },
            { "whenever you create, edit, or debug any .canvas.tsx file",
              "mỗi khi tạo, sửa hoặc debug file .canvas.tsx" },
            { "Bazi", "Tử Vi" },
            // ==== Generic ====
            { "Bộ não Vibe Coding cho AI", "Bộ não Vibe Coding cho AI" },
            { "Hướng dẫn kỹ năng", "Hướng dẫn kỹ năng" },
            { "Coding discipline", "Kỷ luật lập trình" },
            { "before and after code", "trước và sau khi viết code" },
            { "Review for five axes", "Review 5 trục" },
            { "correctness, design, accessibility, performance, taste",
              "tính đúng đắn, thiết kế, accessibility, hiệu năng, thẩm mỹ" },
            { "Anti-patterns", "Anti-patterns" },
            { "best practice", "best practice" },
            { "Use proactively", "Dùng chủ động" },
            { "before merge", "trước khi merge" },
            { "after any non-trivial code change", "sau mỗi thay đổi code đáng kể" },
            { "Senior Staff Engineer reviewing code changes", "Senior Staff Engineer review thay đổi code" },
            { "with rigorous five-axis standards", "với tiêu chuẩn 5 trục nghiêm ngặt" },
            { "Security Engineer for OWASP Top 10", "Security Engineer cho OWASP Top 10" },
            { "threat modeling, secrets, auth, and supply-chain",
              "threat modeling, secrets, auth, và supply-chain" },
            { "Use for any security review, payment flow, auth implementation, or pre-deploy audit",
              "Dùng cho mọi security review, payment flow, auth implementation, hoặc audit trước deploy" },
        };

        public static string Translate(string text)
        {
            if (string.IsNullOrEmpty(text)) return text;
            if (!string.Equals(_current, "vi", StringComparison.OrdinalIgnoreCase)) return text;

            // ponytail: try whole-phrase first, then leading-clause match.
            string result = text;
            foreach (var kv in _descVi)
            {
                if (result.IndexOf(kv.Key, StringComparison.OrdinalIgnoreCase) >= 0)
                    result = result.Replace(kv.Key, kv.Value);
            }
            return result;
        }
    }

    public class SetupForm : Form
    {
        private Panel headerPanel;
        private Label titleLabel;
        private Label subtitleLabel;
        private TabControl mainTabs;

        // Install tab controls
        private TextBox pathTextBox;
        private Button browseButton;
        private Button newFolderButton;
        private CheckBox forceCheckBox;
        private CheckBox cursorCheckBox;
        private Label installPathLabel;
        private Label installPathHintLabel;
        private Label installTipLabel;
        private GroupBox buildOptionsGroup;
        private Label buildOptionsDescLabel;
        private CheckBox buildMemoryCheckBox;
        private CheckBox compileKnowledgeCheckBox;
        private CheckBox buildIndexCheckBox;
        private CheckBox buildEmbeddingsCheckBox;
        private CheckBox packageFrameworkCheckBox;
        private Label buildNoteLabel;

        // Bottom (always visible)
        private ProgressBar progressBar;
        private TextBox logTextBox;
        private Label statusLabel;
        private Label summaryLabel;
        private Button installButton;
        private Button cancelButton;
        private ComboBox languageComboBox;

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
            this.Load += SetupForm_Load;
        }
        
        private async void SetupForm_Load(object sender, EventArgs e)
        {
            selectedPath = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                ".cursor"
            );
            pathTextBox.Text = selectedPath;

            // Scan ZIP for available categories (run async to avoid blocking UI)
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
                    if (parts.Length < 2) continue; // skip top-level files

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

        // Reads frontmatter `description:` or first non-heading line from a sample file inside the item.
        // Returns a short, sanitized description suitable for the ListView second column.
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

                    // Read up to 8 KB
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
                    // Strip BOM
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

            // For file-based categories the item IS the file: rules, agents, prompts,
            // references, workflows, memory, scripts. Templates, when the item is a
            // direct .md file (e.g. GETTING-STARTED.md), should also be read directly.
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
            // 1) Try YAML frontmatter `description: ...`
            // Normalize line endings
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

            // 2) Otherwise first non-empty, non-heading, non-metadata line
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
                    // Skip lines that are mostly markdown links / anchors
                    if (line.StartsWith("[") && line.Contains("](")) continue;
                    if (line.StartsWith("1.") || line.StartsWith("2.") || line.StartsWith("3.")) continue;
                    // Strip leading markdown emphasis
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

                        var lvi = new ListViewItem(item);
                        lvi.Checked = true; // checked by default
                        // ponytail: alternating row tint for readability
                        if (lv.Items.Count % 2 == 1)
                            lvi.BackColor = Color.FromArgb(248, 250, 253);
                        string showDesc = string.IsNullOrEmpty(desc) ? Lang.T("no_description") : Lang.Translate(desc);
                        lvi.SubItems.Add(showDesc);
                        lvi.ToolTipText = showDesc;
                        lv.Items.Add(lvi);                    }
                }
                lv.EndUpdate();
                UpdateCategoryCount(cat);
            }
        }
        
        private void InitializeComponent()
        {
            this.Text = Lang.T("app.title");
            this.Size = new Size(860, 800);
            this.MinimumSize = new Size(860, 800);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.BackColor = Color.FromArgb(245, 246, 250);

            // --- Header ---
            headerPanel = new Panel { Dock = DockStyle.Top, Height = 100, BackColor = Color.FromArgb(30, 60, 114) };

            titleLabel = new Label
            {
                Text = Lang.T("app.title_short"),
                Font = new Font("Segoe UI", 20, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(30, 18),
                AutoSize = true
            };

            subtitleLabel = new Label
            {
                Text = Lang.T("app.subtitle"),
                Font = new Font("Segoe UI", 10),
                ForeColor = Color.FromArgb(180, 200, 230),
                Location = new Point(30, 52),
                AutoSize = true
            };

            // Language picker (top-right, aligned with title row)
            Label langHeaderLabel = new Label
            {
                Text = Lang.T("combobox.lang") + ":",
                Font = new Font("Segoe UI", 9),
                ForeColor = Color.White,
                Location = new Point(640, 32),
                AutoSize = true
            };
            languageComboBox = new ComboBox
            {
                Location = new Point(700, 28),
                Size = new Size(105, 26),
                DropDownStyle = ComboBoxStyle.DropDownList,
                Font = new Font("Segoe UI", 9, FontStyle.Bold),
                BackColor = Color.White,
                ForeColor = Color.FromArgb(30, 60, 114),
                FlatStyle = FlatStyle.Flat
            };
            languageComboBox.Items.Add(new LangItem("vi", "Tiếng Việt"));
            languageComboBox.Items.Add(new LangItem("en", "English"));
            languageComboBox.SelectedIndex = 0; // Vietnamese by default
            languageComboBox.SelectedIndexChanged += LanguageComboBox_SelectedIndexChanged;

            summaryLabel = new Label
            {
                Text = Lang.T("loading_components"),
                Font = new Font("Segoe UI", 9, FontStyle.Italic),
                ForeColor = Color.FromArgb(180, 200, 230),
                Location = new Point(450, 70),
                AutoSize = true
            };

            headerPanel.Controls.AddRange(new Control[] { titleLabel, subtitleLabel, langHeaderLabel, languageComboBox, summaryLabel });

            // --- TabControl body ---
            mainTabs = new TabControl
            {
                Dock = DockStyle.Fill,
                Padding = new Point(12, 6),
                Font = new Font("Segoe UI", 9)
            };

            TabPage tpInstall = BuildInstallTab();
            tpInstall.Text = Lang.T("tab.install");
            TabPage tpComponents = BuildCategoryTab("components_desc",
                new[] { "rules", "skills", "agents", "commands", "hooks", "knowledge" });
            tpComponents.Text = Lang.T("tab.components");
            TabPage tpAdvanced = BuildCategoryTab("advanced_desc",
                new[] { "prompts", "references", "workflows", "templates", "memory", "scripts" });
            tpAdvanced.Text = Lang.T("tab.advanced");

            mainTabs.TabPages.Add(tpInstall);
            mainTabs.TabPages.Add(tpComponents);
            mainTabs.TabPages.Add(tpAdvanced);
            allTabPages.Add(tpInstall);
            allTabPages.Add(tpComponents);
            allTabPages.Add(tpAdvanced);

            // --- Bottom status panel ---
            Panel statusPanel = new Panel { Dock = DockStyle.Bottom, Height = 230, BackColor = Color.White, Padding = new Padding(20, 12, 20, 12) };

            statusLabel = new Label
            {
                Text = Lang.T("ready_to_install"),
                Location = new Point(0, 5),
                AutoSize = true,
                Font = new Font("Segoe UI", 10, FontStyle.Bold),
                ForeColor = Color.FromArgb(30, 60, 114)
            };

            progressBar = new ProgressBar
            {
                Location = new Point(0, 28),
                Size = new Size(820, 22),
                Style = ProgressBarStyle.Continuous,
                BackColor = Color.FromArgb(220, 220, 230),
                ForeColor = Color.FromArgb(30, 100, 180)
            };

            logTextBox = new TextBox
            {
                Location = new Point(0, 58),
                Size = new Size(820, 130),
                Multiline = true,
                ReadOnly = true,
                BackColor = Color.FromArgb(45, 45, 50),
                ForeColor = Color.FromArgb(200, 200, 200),
                Font = new Font("Consolas", 9),
                ScrollBars = ScrollBars.Vertical
            };

            // --- Button panel ---
            Panel buttonPanel = new Panel { Dock = DockStyle.Bottom, Height = 64, BackColor = Color.FromArgb(235, 236, 240) };

            cancelButton = new Button
            {
                Text = Lang.T("btn.cancel"),
                Location = new Point(570, 14),
                Size = new Size(110, 36),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(210, 210, 215),
                ForeColor = Color.FromArgb(50, 50, 60),
                Font = new Font("Segoe UI", 10)
            };
            cancelButton.FlatAppearance.BorderSize = 0;
            cancelButton.Cursor = Cursors.Hand;
            cancelButton.Click += CancelButton_Click;

            installButton = new Button
            {
                Text = Lang.T("btn.install"),
                Location = new Point(690, 14),
                Size = new Size(140, 36),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(30, 120, 60),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 10, FontStyle.Bold)
            };
            installButton.FlatAppearance.BorderSize = 0;
            installButton.Click += InstallButton_Click;

            buttonPanel.Controls.AddRange(new Control[] { cancelButton, installButton });

            statusPanel.Controls.AddRange(new Control[] { statusLabel, progressBar, logTextBox });

            // Z-order: header (top) -> tabs (fill) -> status (bottom) -> buttons (bottom-most)
            this.Controls.AddRange(new Control[] { mainTabs, statusPanel, buttonPanel, headerPanel });

            Lang.OnChanged += ApplyLocalization;
        }

        private TabPage BuildInstallTab()
        {
            TabPage tab = new TabPage { Text = Lang.T("tab.install"), Padding = new Padding(20) };

            installPathLabel = new Label
            {
                Text = Lang.T("install.location"),
                Font = new Font("Segoe UI", 11, FontStyle.Bold),
                Location = new Point(10, 15),
                AutoSize = true
            };

            installPathHintLabel = new Label
            {
                Text = Lang.T("install.location_hint"),
                Font = new Font("Segoe UI", 9),
                ForeColor = Color.Gray,
                Location = new Point(10, 38),
                AutoSize = true
            };

            pathTextBox = new TextBox
            {
                Location = new Point(10, 62),
                Size = new Size(640, 28),
                Font = new Font("Segoe UI", 10),
                ReadOnly = true,
                BackColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle
            };

            browseButton = new Button
            {
                Text = Lang.T("install.browse"),
                Location = new Point(660, 60),
                Size = new Size(120, 32),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(100, 130, 180),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 9)
            };
            browseButton.FlatAppearance.BorderSize = 0;
            browseButton.Click += BrowseButton_Click;

            newFolderButton = new Button
            {
                Text = Lang.T("install.new_folder"),
                Location = new Point(660, 98),
                Size = new Size(120, 28),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(70, 130, 80),
                ForeColor = Color.White,
                Font = new Font("Segoe UI", 8)
            };
            newFolderButton.FlatAppearance.BorderSize = 0;
            newFolderButton.Click += NewFolderButton_Click;

            forceCheckBox = new CheckBox
            {
                Text = Lang.T("install.force"),
                Location = new Point(10, 110),
                AutoSize = true,
                Font = new Font("Segoe UI", 9)
            };

            cursorCheckBox = new CheckBox
            {
                Text = Lang.T("install.skip_cursor"),
                Location = new Point(10, 138),
                AutoSize = true,
                Font = new Font("Segoe UI", 9)
            };

            installTipLabel = new Label
            {
                Text = Lang.T("install.tip"),
                Font = new Font("Segoe UI", 9, FontStyle.Italic),
                ForeColor = Color.Gray,
                Location = new Point(10, 175),
                AutoSize = true,
                MaximumSize = new Size(740, 0)
            };

            // Post-install build options (optional, default unchecked)
            buildOptionsGroup = new GroupBox
            {
                Text = Lang.T("install.build_options"),
                Location = new Point(10, 215),
                Size = new Size(820, 200),
                Font = new Font("Segoe UI", 9, FontStyle.Bold),
                ForeColor = Color.FromArgb(30, 60, 114)
            };

            buildOptionsDescLabel = new Label
            {
                Text = Lang.T("install.build_options_desc"),
                Location = new Point(15, 24),
                Size = new Size(790, 18),
                Font = new Font("Segoe UI", 8, FontStyle.Italic),
                ForeColor = Color.Gray
            };

            buildMemoryCheckBox = new CheckBox
            {
                Text = Lang.T("install.build_memory"),
                Location = new Point(25, 50),
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Checked = false
            };
            compileKnowledgeCheckBox = new CheckBox
            {
                Text = Lang.T("install.compile_knowledge"),
                Location = new Point(25, 75),
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Checked = false
            };
            buildIndexCheckBox = new CheckBox
            {
                Text = Lang.T("install.build_index"),
                Location = new Point(25, 100),
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Checked = false
            };
            buildEmbeddingsCheckBox = new CheckBox
            {
                Text = Lang.T("install.build_embeddings"),
                Location = new Point(25, 125),
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Checked = false
            };
            packageFrameworkCheckBox = new CheckBox
            {
                Text = Lang.T("install.package_framework"),
                Location = new Point(25, 150),
                AutoSize = true,
                Font = new Font("Segoe UI", 9),
                Checked = false
            };

            buildNoteLabel = new Label
            {
                Text = Lang.T("install.build_exe_note"),
                Location = new Point(45, 175),
                Size = new Size(770, 18),
                Font = new Font("Segoe UI", 8, FontStyle.Italic),
                ForeColor = Color.FromArgb(150, 100, 0)
            };

            buildOptionsGroup.Controls.AddRange(new Control[]
            {
                buildOptionsDescLabel,
                buildMemoryCheckBox, compileKnowledgeCheckBox, buildIndexCheckBox,
                buildEmbeddingsCheckBox, packageFrameworkCheckBox, buildNoteLabel
            });

            tab.Controls.AddRange(new Control[]
            {
                installPathLabel, installPathHintLabel, pathTextBox, browseButton, newFolderButton,
                forceCheckBox, cursorCheckBox, installTipLabel, buildOptionsGroup
            });
            return tab;
        }

        private TabPage BuildCategoryTab(string descKey, string[] categories)
        {
            TabPage tab = new TabPage { Text = Lang.T("tab." + (descKey == "components_desc" ? "components" : "advanced")),
                                         Padding = new Padding(10) };

            Label descLabel = new Label
            {
                Text = Lang.T(descKey),
                Font = new Font("Segoe UI", 9),
                ForeColor = Color.Gray,
                Location = new Point(10, 8),
                AutoSize = true
            };
            tab.Controls.Add(descLabel);
            tabDescLabels[tab] = descLabel;

            var entries = new List<(CheckBox, Label, ListView, string)>();

            int y = 32;
            foreach (string cat in categories)
            {
                bool isCore = CoreCategories.Contains(cat);

                CheckBox selectAll = new CheckBox
                {
                    Text = isCore ? Lang.T("always_installed", cat) : Lang.T("select_all", cat),
                    Location = new Point(10, y),
                    AutoSize = true,
                    Font = new Font("Segoe UI", 9, FontStyle.Bold),
                    Checked = true,
                    Enabled = !isCore
                };
                selectAll.CheckedChanged += (s, e) =>
                {
                    if (isCore) return;
                    if (categoryListBoxes.ContainsKey(cat))
                    {
                        ListView lv = categoryListBoxes[cat];
                        foreach (ListViewItem item in lv.Items)
                            item.Checked = selectAll.Checked;
                        UpdateCategoryCount(cat);
                    }
                };
                categorySelectAll[cat] = selectAll;
                tab.Controls.Add(selectAll);

                Label countLabel = new Label
                {
                    Text = "...",
                    Location = new Point(740, y + 2),
                    AutoSize = true,
                    Font = new Font("Segoe UI", 9),
                    ForeColor = Color.Gray
                };
                categoryCountLabels[cat] = countLabel;
                tab.Controls.Add(countLabel);

                ListView listView = new ListView
                {
                    Location = new Point(10, y + 22),
                    Size = new Size(800, 180),
                    View = View.Details,
                    CheckBoxes = true,
                    FullRowSelect = true,
                    GridLines = false,
                    HideSelection = false,
                    MultiSelect = false,
                    Font = new Font("Segoe UI", 9),
                    BorderStyle = BorderStyle.FixedSingle,
                    HeaderStyle = ColumnHeaderStyle.Nonclickable,
                    BackColor = Color.White
                };
                listView.Columns.Add(Lang.T("column.component"), 220);
                listView.Columns.Add(Lang.T("column.description"), 560);
                listView.ItemChecked += (s, e) =>
                {
                    BeginInvoke(new Action(() => UpdateCategoryCount(cat)));
                };
                categoryListBoxes[cat] = listView;
                tab.Controls.Add(listView);

                entries.Add((selectAll, countLabel, listView, cat));
                y += 22 + 180 + 8;
            }
            tabEntries[tab] = entries;
            return tab;
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
                UpdateSummary(); // computed
            else
                summaryLabel.Text = Lang.T("ready_to_install");

            installPathLabel.Text = Lang.T("install.location");
            installPathHintLabel.Text = Lang.T("install.location_hint");
            browseButton.Text = Lang.T("install.browse");
            newFolderButton.Text = Lang.T("install.new_folder");
            forceCheckBox.Text = Lang.T("install.force");
            cursorCheckBox.Text = Lang.T("install.skip_cursor");
            installTipLabel.Text = Lang.T("install.tip");
            buildOptionsGroup.Text = Lang.T("install.build_options");
            buildOptionsDescLabel.Text = Lang.T("install.build_options_desc");
            buildMemoryCheckBox.Text = Lang.T("install.build_memory");
            compileKnowledgeCheckBox.Text = Lang.T("install.compile_knowledge");
            buildIndexCheckBox.Text = Lang.T("install.build_index");
            buildEmbeddingsCheckBox.Text = Lang.T("install.build_embeddings");
            packageFrameworkCheckBox.Text = Lang.T("install.package_framework");
            buildNoteLabel.Text = Lang.T("install.build_exe_note");
            cancelButton.Text = Lang.T("btn.cancel");
            installButton.Text = Lang.T("btn.install");

            // Tabs
            int idx = 0;
            foreach (TabPage tp in allTabPages)
            {
                if (idx == 0) tp.Text = Lang.T("tab.install");
                else if (idx == 1) tp.Text = Lang.T("tab.components");
                else if (idx == 2) tp.Text = Lang.T("tab.advanced");
                idx++;
            }

            // Per-category controls
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
                    // Column headers
                    if (listView.Columns.Count >= 2)
                    {
                        listView.Columns[0].Text = Lang.T("column.component");
                        listView.Columns[1].Text = Lang.T("column.description");
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
            lbl.Text = Lang.T("selected_count", selected, total);
            lbl.ForeColor = (selected == total) ? Color.FromArgb(30, 120, 60) : Color.Gray;

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

            // Snapshot current selections
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

            // Find the ZIP file (sidecar in same directory as exe)
            string zipPath = FindZipPath();
            if (zipPath == null)
            {
                throw new Exception(Lang.T("log.zip_not_found", EMBEDDED_ZIP_NAME));
            }

            AppendLog(Lang.T("log.found_archive", zipPath));

            UpdateProgress(15, Lang.T("log.extracting_files"));
            AppendLog(Lang.T("log.extracting"));

            bool force = forceCheckBox.Checked;

            // Extract ZIP using snapshot
            await ExtractZipAsync(zipPath, currentInstallPath, force, snapshot, 15, 88);

            // Post-install build steps (if any checkbox is selected)
            if (GetSelectedBuildSteps().Count > 0)
            {
                UpdateProgress(89, Lang.T("log.post_install"));
                await RunPostInstallScriptsAsync(currentInstallPath);
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
                        if (string.IsNullOrEmpty(entry.Name)) continue; // Skip directory entries

                        current++;

                        // Check selection filter
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

        // Build step definitions: checkbox key -> relative script path (under .cursor/scripts/)
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
            // Scripts live in <project>/.cursor/scripts/<rel>. They expect the project root
            // as the current working directory. If user installed into <project>/.cursor,
            // cwd = <project>. Otherwise cwd = installDir.
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
                        // ponytail: stream output line-by-line to log; no temp file needed
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
                return true; // top-level file (e.g. .cursorrules) always extracted

            string topCategory = parts[0];
            // If category is not one we know about, extract (don't drop unknown content)
            if (!CategoryOrder.Any(c => string.Equals(c, topCategory, StringComparison.OrdinalIgnoreCase)))
                return true;

            // Core categories always extract
            if (CoreCategories.Contains(topCategory))
                return true;

            // If snapshot doesn't include the category, skip
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

            // Decide grouping key based on category structure
            // Folder-based categories: group by immediate subfolder
            bool folderBased = string.Equals(topCategory, "skills", StringComparison.OrdinalIgnoreCase)
                || string.Equals(topCategory, "knowledge", StringComparison.OrdinalIgnoreCase)
                || string.Equals(topCategory, "commands", StringComparison.OrdinalIgnoreCase)
                || string.Equals(topCategory, "hooks", StringComparison.OrdinalIgnoreCase)
                || string.Equals(topCategory, "templates", StringComparison.OrdinalIgnoreCase);

            string groupKey = parts[1]; // immediate child

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
            statusLabel.Text = "● " + status;
            // ponytail: color reflects state — green when 100, blue in-progress, gray idle
            if (value >= 100) statusLabel.ForeColor = Color.FromArgb(30, 120, 60);
            else if (value > 0) statusLabel.ForeColor = Color.FromArgb(30, 100, 180);
            else statusLabel.ForeColor = Color.FromArgb(80, 80, 90);
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

    internal class LangItem
    {
        public string Code { get; }
        public LangItem(string code, string display) { Code = code; Display = display; }
        public string Display { get; }
        public override string ToString() { return Display; }
    }
}
