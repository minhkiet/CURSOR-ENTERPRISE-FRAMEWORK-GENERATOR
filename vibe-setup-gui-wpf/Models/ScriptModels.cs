using System;
using System.Collections.Generic;
using System.ComponentModel;

namespace CursorSetupWpf.Models
{
    /// <summary>
    /// Defines a single script block (a group of commands) that can be
    /// selected and included in a generated .bat file.
    /// </summary>
    public class ScriptBlock : INotifyPropertyChanged
    {
        private bool _isSelected = true;
        public string Id { get; set; } = "";
        public string Title { get; set; } = "";
        public string Description { get; set; } = "";
        public string Category { get; set; } = "";
        public string Icon { get; set; } = "\uE756";
        public List<ScriptLine> Lines { get; set; } = new();

        public bool IsSelected
        {
            get => _isSelected;
            set
            {
                if (_isSelected != value)
                {
                    _isSelected = value;
                    OnPropertyChanged(nameof(IsSelected));
                }
            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    public class ScriptLine
    {
        public string Command { get; set; } = "";
        public string Args { get; set; } = "";
        public string Comment { get; set; } = "";
        public string WorkDir { get; set; } = "";
        public bool Required { get; set; } = true;
    }

    /// <summary>
    /// Defines a complete script template (one .bat output file).
    /// </summary>
    public class ScriptTemplate : INotifyPropertyChanged
    {
        private bool _isSelected = true;
        public string Id { get; set; } = "";
        public string Name { get; set; } = "";
        public string FileName { get; set; } = "";
        public string Description { get; set; } = "";
        public string Category { get; set; } = "";
        public string Icon { get; set; } = "\uE756";
        public List<ScriptBlock> Blocks { get; set; } = new();

        public bool IsSelected
        {
            get => _isSelected;
            set
            {
                if (_isSelected != value)
                {
                    _isSelected = value;
                    OnPropertyChanged(nameof(IsSelected));
                }
            }
        }

        public event PropertyChangedEventHandler? PropertyChanged;

        protected void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
