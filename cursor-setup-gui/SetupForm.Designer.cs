using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Windows.Forms;

namespace CursorSetup
{
    partial class SetupForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        // Header
        private Panel headerPanel;
        private Label titleLabel;
        private Label subtitleLabel;
        private Label versionChip;
        private Panel headerAccent;

        // Tab container
        private TabControl mainTabs;

        // Bottom panel + button strip
        private Panel bottomPanel;
        private Panel buttonStrip;

        // Bottom: log + progress
        private TextBox logTextBox;
        private ProgressBar progressBar;
        private Label statusLabel;
        private Label summaryLabel;

        // Button strip: cancel | language | install
        private Button cancelButton;
        private ComboBox languageComboBox;
        private Button installButton;

        // Install tab (built dynamically but declared here)
        private TabPage installTab;

        // Install tab controls
        private TextBox pathTextBox;
        private Button browseButton;
        private Button newFolderButton;
        private CheckBox forceCheckBox;
        private CheckBox cursorCheckBox;
        private Label installPathLabel;
        private Label installPathHintLabel;
        private Label installTipLabel;
        private Panel buildOptionsGroup;
        private Label buildOptionsDescLabel;
        private CheckBox buildMemoryCheckBox;
        private CheckBox compileKnowledgeCheckBox;
        private CheckBox buildIndexCheckBox;
        private CheckBox buildEmbeddingsCheckBox;
        private CheckBox packageFrameworkCheckBox;
        private Label buildNoteLabel;
        private ToolTip buildToolTip;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            components = new Container();
            ComponentResourceManager resources = new ComponentResourceManager(typeof(SetupForm));
            headerPanel = new Panel();
            headerAccent = new Panel();
            titleLabel = new Label();
            subtitleLabel = new Label();
            versionChip = new Label();
            mainTabs = new TabControl();
            bottomPanel = new Panel();
            progressBar = new ProgressBar();
            statusLabel = new Label();
            summaryLabel = new Label();
            buttonStrip = new Panel();
            cancelButton = new Button();
            languageComboBox = new ComboBox();
            installButton = new Button();
            logTextBox = new TextBox();
            buildToolTip = new ToolTip(components);
            headerPanel.SuspendLayout();
            bottomPanel.SuspendLayout();
            buttonStrip.SuspendLayout();
            SuspendLayout();
            //
            // headerPanel — top brand strip with indigo accent on the left
            //
            headerPanel.BackColor = SetupTheme.HeaderBack;
            headerPanel.Controls.Add(headerAccent);
            headerPanel.Controls.Add(titleLabel);
            headerPanel.Controls.Add(subtitleLabel);
            headerPanel.Controls.Add(versionChip);
            headerPanel.Dock = DockStyle.Top;
            headerPanel.Location = new Point(0, 0);
            headerPanel.Margin = new Padding(0);
            headerPanel.Name = "headerPanel";
            headerPanel.Size = new Size(1100, 96);
            headerPanel.TabIndex = 2;
            //
            // headerAccent — 4px indigo bar at the very left edge
            //
            headerAccent.BackColor = SetupTheme.Indigo600;
            headerAccent.Dock = DockStyle.Left;
            headerAccent.Location = new Point(0, 0);
            headerAccent.Name = "headerAccent";
            headerAccent.Size = new Size(4, 96);
            headerAccent.TabIndex = 4;
            //
            // titleLabel
            //
            titleLabel.AutoSize = true;
            titleLabel.Font = SetupTheme.FontTitle;
            titleLabel.ForeColor = SetupTheme.Slate900;
            titleLabel.Location = new Point(28, 18);
            titleLabel.Name = "titleLabel";
            titleLabel.Size = new Size(560, 38);
            titleLabel.TabIndex = 0;
            titleLabel.Text = "Cursor Enterprise Framework";
            //
            // subtitleLabel
            //
            subtitleLabel.AutoSize = true;
            subtitleLabel.Font = SetupTheme.FontSubtitle;
            subtitleLabel.ForeColor = SetupTheme.Slate500;
            subtitleLabel.Location = new Point(28, 56);
            subtitleLabel.Name = "subtitleLabel";
            subtitleLabel.Size = new Size(560, 23);
            subtitleLabel.TabIndex = 1;
            subtitleLabel.Text = "Enterprise-grade rules, skills, agents, and automation for Cursor";
            //
            // versionChip — small pill on the right side of the header
            //
            versionChip.Anchor = AnchorStyles.Top | AnchorStyles.Right;
            versionChip.AutoSize = false;
            versionChip.BackColor = SetupTheme.Indigo50;
            versionChip.Font = new Font("Segoe UI Semibold", 8.5F, FontStyle.Bold);
            versionChip.ForeColor = SetupTheme.Indigo600;
            versionChip.Location = new Point(1010, 32);
            versionChip.Name = "versionChip";
            versionChip.Size = new Size(70, 26);
            versionChip.TabIndex = 3;
            versionChip.Text = "v4.3.0";
            versionChip.TextAlign = ContentAlignment.MiddleCenter;
            //
            // mainTabs — flat strip with custom draw
            //
            mainTabs.Appearance = TabAppearance.FlatButtons;
            mainTabs.BackColor = SetupTheme.TabBack;
            mainTabs.Dock = DockStyle.Fill;
            mainTabs.DrawMode = TabDrawMode.OwnerDrawFixed;
            mainTabs.Font = SetupTheme.FontTab;
            mainTabs.ItemSize = new Size(140, 42);
            mainTabs.Location = new Point(0, 96);
            mainTabs.Margin = new Padding(0);
            mainTabs.Name = "mainTabs";
            mainTabs.Padding = new Point(20, 6);
            mainTabs.SelectedIndex = 0;
            mainTabs.Size = new Size(1100, 720);
            mainTabs.SizeMode = TabSizeMode.Normal;
            mainTabs.TabIndex = 1;
            //
            // bottomPanel
            //
            bottomPanel.BackColor = SetupTheme.FormBack;
            bottomPanel.Controls.Add(progressBar);
            bottomPanel.Controls.Add(statusLabel);
            bottomPanel.Controls.Add(summaryLabel);
            bottomPanel.Controls.Add(buttonStrip);
            bottomPanel.Controls.Add(logTextBox);
            bottomPanel.Dock = DockStyle.Bottom;
            bottomPanel.Location = new Point(0, 505);
            bottomPanel.Margin = new Padding(0);
            bottomPanel.Name = "bottomPanel";
            bottomPanel.Size = new Size(1100, 333);
            bottomPanel.TabIndex = 0;
            //
            // progressBar — themed via Paint event in SetupForm
            //
            progressBar.Dock = DockStyle.Top;
            progressBar.Location = new Point(0, 58);
            progressBar.Margin = new Padding(0, 8, 0, 0);
            progressBar.Name = "progressBar";
            progressBar.Size = new Size(1100, 8);
            progressBar.TabIndex = 0;
            //
            // statusLabel — top of bottom panel
            //
            statusLabel.BackColor = SetupTheme.FormBack;
            statusLabel.Dock = DockStyle.Top;
            statusLabel.Font = SetupTheme.FontBody;
            statusLabel.ForeColor = SetupTheme.Slate500;
            statusLabel.Location = new Point(0, 29);
            statusLabel.Name = "statusLabel";
            statusLabel.Padding = new Padding(24, 0, 24, 0);
            statusLabel.Size = new Size(1100, 29);
            statusLabel.TabIndex = 1;
            statusLabel.Text = "●  Initializing…";
            statusLabel.TextAlign = ContentAlignment.MiddleLeft;
            //
            // summaryLabel — just above status
            //
            summaryLabel.BackColor = SetupTheme.FormBack;
            summaryLabel.Dock = DockStyle.Top;
            summaryLabel.Font = SetupTheme.FontLabel;
            summaryLabel.ForeColor = SetupTheme.Slate900;
            summaryLabel.Location = new Point(0, 0);
            summaryLabel.Name = "summaryLabel";
            summaryLabel.Padding = new Padding(24, 0, 24, 0);
            summaryLabel.Size = new Size(1100, 29);
            summaryLabel.TabIndex = 2;
            summaryLabel.TextAlign = ContentAlignment.MiddleLeft;
            //
            // buttonStrip
            //
            buttonStrip.BackColor = SetupTheme.HeaderBack;
            buttonStrip.Controls.Add(cancelButton);
            buttonStrip.Controls.Add(languageComboBox);
            buttonStrip.Controls.Add(installButton);
            buttonStrip.Dock = DockStyle.Bottom;
            buttonStrip.Location = new Point(0, 285);
            buttonStrip.Margin = new Padding(0);
            buttonStrip.Name = "buttonStrip";
            buttonStrip.Padding = new Padding(24, 10, 24, 10);
            buttonStrip.Size = new Size(1100, 48);
            buttonStrip.TabIndex = 3;
            //
            // cancelButton — ghost style
            //
            cancelButton.Anchor = AnchorStyles.Left;
            cancelButton.BackColor = Color.White;
            cancelButton.FlatAppearance.BorderSize = 0;
            cancelButton.FlatStyle = FlatStyle.Flat;
            cancelButton.Font = SetupTheme.FontBody;
            cancelButton.ForeColor = SetupTheme.Slate700;
            cancelButton.Location = new Point(0, 0);
            cancelButton.Margin = new Padding(0);
            cancelButton.Name = "cancelButton";
            cancelButton.Size = new Size(120, 38);
            cancelButton.TabIndex = 0;
            cancelButton.Text = "Cancel";
            cancelButton.UseVisualStyleBackColor = false;
            cancelButton.Cursor = Cursors.Hand;
            cancelButton.Click += CancelButton_Click;
            //
            // languageComboBox
            //
            languageComboBox.Anchor = AnchorStyles.Left;
            languageComboBox.BackColor = Color.White;
            languageComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
            languageComboBox.FlatStyle = FlatStyle.Flat;
            languageComboBox.Font = SetupTheme.FontBody;
            languageComboBox.ForeColor = SetupTheme.Slate700;
            languageComboBox.Location = new Point(140, 7);
            languageComboBox.Margin = new Padding(0);
            languageComboBox.Name = "languageComboBox";
            languageComboBox.Size = new Size(170, 32);
            languageComboBox.TabIndex = 1;
            languageComboBox.SelectedIndexChanged += LanguageComboBox_SelectedIndexChanged;
            //
            // installButton — primary CTA (gradient indigo→emerald)
            //
            installButton.Anchor = AnchorStyles.Right;
            installButton.BackColor = SetupTheme.Indigo600;
            installButton.FlatAppearance.BorderSize = 0;
            installButton.FlatStyle = FlatStyle.Flat;
            installButton.Font = SetupTheme.FontCta;
            installButton.ForeColor = Color.White;
            installButton.Location = new Point(910, 0);
            installButton.Margin = new Padding(0);
            installButton.Name = "installButton";
            installButton.Size = new Size(166, 40);
            installButton.TabIndex = 2;
            installButton.Text = "Install";
            installButton.UseVisualStyleBackColor = false;
            installButton.Cursor = Cursors.Hand;
            installButton.Paint += (s, e) => SetupTheme.PaintPrimaryCta((Button)s, e);
            installButton.MouseEnter += (s, e) => installButton.Invalidate();
            installButton.MouseLeave += (s, e) => installButton.Invalidate();
            installButton.Click += InstallButton_Click;
            //
            // logTextBox
            //
            logTextBox.BackColor = SetupTheme.LogBack;
            logTextBox.BorderStyle = BorderStyle.None;
            logTextBox.Dock = DockStyle.Fill;
            logTextBox.Font = SetupTheme.FontMono;
            logTextBox.ForeColor = SetupTheme.LogFore;
            logTextBox.Location = new Point(0, 0);
            logTextBox.Margin = new Padding(0);
            logTextBox.Multiline = true;
            logTextBox.Name = "logTextBox";
            logTextBox.ReadOnly = true;
            logTextBox.ScrollBars = ScrollBars.Vertical;
            logTextBox.Size = new Size(1100, 237);
            logTextBox.TabIndex = 4;
            logTextBox.WordWrap = false;
            //
            // buildToolTip
            //
            buildToolTip.ToolTipTitle = "Info";
            //
            // SetupForm
            //
            AutoScaleDimensions = new SizeF(9F, 21F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = SetupTheme.FormBack;
            ClientSize = new Size(1100, 838);
            Controls.Add(bottomPanel);
            Controls.Add(mainTabs);
            Controls.Add(headerPanel);
            Icon = (Icon)resources.GetObject("$this.Icon");
            MinimumSize = new Size(960, 760);
            Name = "SetupForm";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Cursor Enterprise Framework — Setup";
            headerPanel.ResumeLayout(false);
            headerPanel.PerformLayout();
            bottomPanel.ResumeLayout(false);
            bottomPanel.PerformLayout();
            buttonStrip.ResumeLayout(false);
            ResumeLayout(false);
        }

        #endregion
    }
}
