using System;
using System.Globalization;
using System.Windows;
using System.Windows.Data;
using System.Windows.Media;

namespace CursorSetupWpf.Helpers
{
    public class IndexToVisibilityConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is int selectedIndex && parameter is string param)
            {
                if (int.TryParse(param, out int targetIndex))
                    return selectedIndex == targetIndex ? Visibility.Visible : Visibility.Collapsed;
            }
            return Visibility.Collapsed;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            => DependencyProperty.UnsetValue;
    }

    public class BoolToVisibilityConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            bool invert = parameter?.ToString() == "Invert";
            bool boolValue = value is bool b && b;
            if (invert) boolValue = !boolValue;
            return boolValue ? Visibility.Visible : Visibility.Collapsed;
        }
        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            => DependencyProperty.UnsetValue;
    }

    public class InverseBoolConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
            => value is bool b && !b;
        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            => value is bool b && !b;
    }

    /// <summary>
    /// Converts log line prefixes to WPF Brushes for colored log output.
    /// Dark slate-900 bg requires high-contrast, bright foregrounds.
    /// </summary>
    public class LogLevelToBrushConverter : IValueConverter
    {
        // Bright, high-contrast colors for dark background
        static readonly Brush ErrorBrush   = new SolidColorBrush(Color.FromRgb(239, 68,  68 ));   // Red-500
        static readonly Brush OkBrush       = new SolidColorBrush(Color.FromRgb(52,  211, 153));   // Emerald-400
        static readonly Brush WarnBrush     = new SolidColorBrush(Color.FromRgb(251, 191, 36 ));   // Amber-400
        static readonly Brush HeaderBrush   = new SolidColorBrush(Color.FromRgb(165, 180, 252));   // Indigo-300
        static readonly Brush NormalBrush   = new SolidColorBrush(Color.FromRgb(226, 232, 240));   // Slate-200 (readable on slate-900)

        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            string line = value as string ?? "";
            if (line.StartsWith("ERROR") || line.Contains("[ERROR]")) return ErrorBrush;
            if (line.StartsWith("    FAILED") || line.StartsWith("Loi") || line.StartsWith("LOI")) return ErrorBrush;
            if (line.StartsWith("    OK") || line.StartsWith("OK (")) return OkBrush;
            if (line.StartsWith("[SKIP-CAT]") || line.StartsWith("[SKIP]")) return WarnBrush;
            if (line.StartsWith("===")) return HeaderBrush;
            if (line.StartsWith("===>")) return HeaderBrush;
            return NormalBrush;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
            => DependencyProperty.UnsetValue;
    }
}
