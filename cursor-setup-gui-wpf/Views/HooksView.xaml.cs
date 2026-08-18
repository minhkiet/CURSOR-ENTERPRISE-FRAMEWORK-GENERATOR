using System.Windows.Controls;
using CursorSetupWpf.ViewModels;

namespace CursorSetupWpf.Views
{
    public partial class HooksView : UserControl
    {
        public HooksView()
        {
            InitializeComponent();
            // HooksView uses MainViewModel for hooks-related bindings
            DataContext = App.Current.MainWindow?.DataContext;
        }
    }
}
