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
        private GroupBox buildOptionsGroup;
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
            titleLabel = new Label();
            subtitleLabel = new Label();
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
            // headerPanel
            // 
            headerPanel.BackColor = Color.FromArgb(245, 246, 250);
            headerPanel.Controls.Add(titleLabel);
            headerPanel.Controls.Add(subtitleLabel);
            headerPanel.Dock = DockStyle.Top;
            headerPanel.Location = new Point(0, 0);
            headerPanel.Margin = new Padding(3, 4, 3, 4);
            headerPanel.Name = "headerPanel";
            headerPanel.Size = new Size(976, 83);
            headerPanel.TabIndex = 2;
            // 
            // titleLabel
            // 
            titleLabel.AutoSize = true;
            titleLabel.Font = new Font("Segoe UI", 16F, FontStyle.Bold);
            titleLabel.ForeColor = Color.FromArgb(30, 60, 114);
            titleLabel.Location = new Point(22, 14);
            titleLabel.Name = "titleLabel";
            titleLabel.Size = new Size(553, 45);
            titleLabel.TabIndex = 0;
            titleLabel.Text = "Cursor Enterprise Framework Setup";
            // 
            // subtitleLabel
            // 
            subtitleLabel.AutoSize = true;
            subtitleLabel.Font = new Font("Segoe UI", 9F);
            subtitleLabel.ForeColor = Color.Gray;
            subtitleLabel.Location = new Point(22, 57);
            subtitleLabel.Name = "subtitleLabel";
            subtitleLabel.Size = new Size(514, 25);
            subtitleLabel.TabIndex = 1;
            subtitleLabel.Text = "Enterprise-grade rules, skills, agents, and automation for Cursor";
            // 
            // mainTabs
            // 
            mainTabs.Dock = DockStyle.Fill;
            mainTabs.Font = new Font("Segoe UI", 10F);
            mainTabs.ItemSize = new Size(120, 36);
            mainTabs.Location = new Point(0, 83);
            mainTabs.Margin = new Padding(3, 4, 3, 4);
            mainTabs.Name = "mainTabs";
            mainTabs.SelectedIndex = 0;
            mainTabs.Size = new Size(976, 755);
            mainTabs.SizeMode = TabSizeMode.Fixed;
            mainTabs.TabIndex = 1;
            // 
            // bottomPanel
            // 
            bottomPanel.Controls.Add(progressBar);
            bottomPanel.Controls.Add(statusLabel);
            bottomPanel.Controls.Add(summaryLabel);
            bottomPanel.Controls.Add(buttonStrip);
            bottomPanel.Controls.Add(logTextBox);
            bottomPanel.Dock = DockStyle.Bottom;
            bottomPanel.Location = new Point(0, 505);
            bottomPanel.Margin = new Padding(3, 4, 3, 4);
            bottomPanel.Name = "bottomPanel";
            bottomPanel.Size = new Size(976, 333);
            bottomPanel.TabIndex = 0;
            // 
            // progressBar
            // 
            progressBar.Dock = DockStyle.Top;
            progressBar.Location = new Point(0, 58);
            progressBar.Margin = new Padding(3, 4, 3, 4);
            progressBar.Name = "progressBar";
            progressBar.Size = new Size(976, 10);
            progressBar.TabIndex = 0;
            // 
            // statusLabel
            // 
            statusLabel.Dock = DockStyle.Top;
            statusLabel.Font = new Font("Segoe UI", 9F);
            statusLabel.Location = new Point(0, 29);
            statusLabel.Name = "statusLabel";
            statusLabel.Padding = new Padding(7, 0, 7, 0);
            statusLabel.Size = new Size(976, 29);
            statusLabel.TabIndex = 1;
            statusLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // summaryLabel
            // 
            summaryLabel.Dock = DockStyle.Top;
            summaryLabel.Font = new Font("Segoe UI", 9F);
            summaryLabel.Location = new Point(0, 0);
            summaryLabel.Name = "summaryLabel";
            summaryLabel.Padding = new Padding(7, 0, 7, 0);
            summaryLabel.Size = new Size(976, 29);
            summaryLabel.TabIndex = 2;
            summaryLabel.TextAlign = ContentAlignment.MiddleLeft;
            // 
            // buttonStrip
            // 
            buttonStrip.Controls.Add(cancelButton);
            buttonStrip.Controls.Add(languageComboBox);
            buttonStrip.Controls.Add(installButton);
            buttonStrip.Dock = DockStyle.Bottom;
            buttonStrip.Location = new Point(0, 285);
            buttonStrip.Margin = new Padding(3, 4, 3, 4);
            buttonStrip.Name = "buttonStrip";
            buttonStrip.Padding = new Padding(9, 5, 9, 5);
            buttonStrip.Size = new Size(976, 48);
            buttonStrip.TabIndex = 3;
            // 
            // cancelButton
            // 
            cancelButton.Anchor = AnchorStyles.Left;
            cancelButton.BackColor = Color.FromArgb(180, 190, 200);
            cancelButton.FlatAppearance.BorderSize = 0;
            cancelButton.FlatStyle = FlatStyle.Flat;
            cancelButton.Font = new Font("Segoe UI", 9F);
            cancelButton.ForeColor = Color.FromArgb(50, 50, 50);
            cancelButton.Location = new Point(0, 0);
            cancelButton.Margin = new Padding(3, 4, 3, 4);
            cancelButton.Name = "cancelButton";
            cancelButton.Size = new Size(111, 36);
            cancelButton.TabIndex = 0;
            cancelButton.Text = "Cancel";
            cancelButton.UseVisualStyleBackColor = false;
            cancelButton.Click += CancelButton_Click;
            // 
            // languageComboBox
            // 
            languageComboBox.Anchor = AnchorStyles.Left;
            languageComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
            languageComboBox.Location = new Point(129, 7);
            languageComboBox.Margin = new Padding(3, 4, 3, 4);
            languageComboBox.Name = "languageComboBox";
            languageComboBox.Size = new Size(177, 33);
            languageComboBox.TabIndex = 1;
            languageComboBox.SelectedIndexChanged += LanguageComboBox_SelectedIndexChanged;
            // 
            // installButton
            // 
            installButton.Anchor = AnchorStyles.Right;
            installButton.BackColor = Color.FromArgb(30, 120, 60);
            installButton.FlatAppearance.BorderSize = 0;
            installButton.FlatStyle = FlatStyle.Flat;
            installButton.Font = new Font("Segoe UI", 10F, FontStyle.Bold);
            installButton.ForeColor = Color.White;
            installButton.Location = new Point(754, 0);
            installButton.Margin = new Padding(3, 4, 3, 4);
            installButton.Name = "installButton";
            installButton.Size = new Size(111, 36);
            installButton.TabIndex = 2;
            installButton.Text = "Install";
            installButton.UseVisualStyleBackColor = false;
            installButton.Click += InstallButton_Click;
            // 
            // logTextBox
            // 
            logTextBox.BackColor = Color.FromArgb(248, 250, 253);
            logTextBox.BorderStyle = BorderStyle.None;
            logTextBox.Dock = DockStyle.Fill;
            logTextBox.Font = new Font("Consolas", 9F);
            logTextBox.Location = new Point(0, 0);
            logTextBox.Margin = new Padding(3, 4, 3, 4);
            logTextBox.Multiline = true;
            logTextBox.Name = "logTextBox";
            logTextBox.ReadOnly = true;
            logTextBox.ScrollBars = ScrollBars.Vertical;
            logTextBox.Size = new Size(976, 333);
            logTextBox.TabIndex = 4;
            // 
            // buildToolTip
            // 
            buildToolTip.ToolTipTitle = "Info";
            // 
            // SetupForm
            // 
            AutoScaleDimensions = new SizeF(10F, 25F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.FromArgb(245, 246, 250);
            ClientSize = new Size(976, 838);
            Controls.Add(bottomPanel);
            Controls.Add(mainTabs);
            Controls.Add(headerPanel);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Margin = new Padding(3, 4, 3, 4);
            MinimumSize = new Size(909, 751);
            Name = "SetupForm";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Cursor Enterprise Framework Setup";
            WindowState = FormWindowState.Maximized;
            headerPanel.ResumeLayout(false);
            headerPanel.PerformLayout();
            bottomPanel.ResumeLayout(false);
            buttonStrip.ResumeLayout(false);
            bottomPanel.PerformLayout();
            ResumeLayout(false);
        }

        #endregion
    }
}
