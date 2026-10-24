using System.Windows;
using System.Windows.Controls;
using CursorSetupWpf.ViewModels;

namespace CursorSetupWpf.Views
{
    public partial class ECCView : UserControl
    {
        public ECCView()
        {
            InitializeComponent();
            Loaded += OnLoaded;
        }

        void OnLoaded(object sender, RoutedEventArgs e)
        {
            // Ensure DataContext is set to MainViewModel for proper binding
            if (DataContext is not MainViewModel)
            {
                // Try to find MainViewModel from visual tree
                var parent = this.Parent;
                while (parent != null)
                {
                    if (parent is FrameworkElement fe && fe.DataContext is MainViewModel mainVm)
                    {
                        DataContext = mainVm;
                        break;
                    }
                    parent = (parent as FrameworkElement)?.Parent ?? 
                             (parent as FrameworkContentElement)?.Parent;
                }
            }
        }
    }
}
