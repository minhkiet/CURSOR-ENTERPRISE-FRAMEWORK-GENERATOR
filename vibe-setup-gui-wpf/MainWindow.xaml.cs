using System.Windows;
using CursorSetupWpf.Services;

namespace CursorSetupWpf
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            LocalizationService.CultureChanged += () => { };
        }
    }
}
