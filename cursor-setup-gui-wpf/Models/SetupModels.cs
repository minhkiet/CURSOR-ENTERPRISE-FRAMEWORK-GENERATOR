using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;

namespace CursorSetupWpf.Models
{
    public class SetupCategory : INotifyPropertyChanged
    {
        private bool _isExpanded = true;
        private int _selectedCount;

        public string Name { get; set; } = "";
        public bool IsCore { get; set; }
        public ObservableCollection<SetupItem> Items { get; set; } = new();

        public bool IsExpanded
        {
            get => _isExpanded;
            set { _isExpanded = value; OnPropertyChanged(nameof(IsExpanded)); }
        }

        public int SelectedCount
        {
            get => _selectedCount;
            set { _selectedCount = value; OnPropertyChanged(nameof(SelectedCount)); }
        }

        public int TotalCount => Items.Count;
        public bool AllSelected => Items.All(i => i.IsSelected);

        public string SelectionLabel => $"{SelectedCount}/{TotalCount}";

        public void UpdateSelection()
        {
            SelectedCount = Items.Count(i => i.IsSelected);
            OnPropertyChanged(nameof(AllSelected));
            OnPropertyChanged(nameof(SelectionLabel));
        }

        public void SelectAll(bool selected)
        {
            foreach (var item in Items)
                item.IsSelected = selected;
            UpdateSelection();
        }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged(string name) =>
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }

    public class SetupItem : INotifyPropertyChanged
    {
        private bool _isSelected = true;
        private string _description = "";
        public event PropertyChangedEventHandler PropertyChanged;

        public int Index { get; set; }
        public string Name { get; set; } = "";

        public bool IsSelected
        {
            get => _isSelected;
            set { _isSelected = value; PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(IsSelected))); }
        }

        public string Description
        {
            get => _description;
            set { _description = value; PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(nameof(Description))); }
        }
    }

    public class SetupConfig
    {
        public string InstallPath { get; set; } = "";
        public bool ForceOverwrite { get; set; }
        public bool SkipCursorCheck { get; set; }
        public bool BuildMemory { get; set; }
        public bool CompileKnowledge { get; set; }
        public bool BuildIndex { get; set; }
        public bool BuildEmbeddings { get; set; }
        public bool PackageFramework { get; set; }
        public bool EnablePreScanHook { get; set; } = true;
        public bool EnablePostInstallHook { get; set; } = true;
        public string PreScanScript { get; set; } = "-m cursor_framework.indexer --validate";
        public string PostInstallScript { get; set; } = "-m cursor_framework.indexer";
    }

    public class CategorySelection
    {
        public string Category { get; set; } = "";
        public HashSet<string> SelectedItems { get; set; } = new();
    }
}
