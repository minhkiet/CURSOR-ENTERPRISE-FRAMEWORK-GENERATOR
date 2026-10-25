using System.Diagnostics;
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Threading;

namespace CursorSetupWpf
{
    public partial class App : Application
    {
        static readonly string LogPath = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
            "CursorSetup", "cursor-setup-debug.log");

        static void Log(string msg)
        {
            try
            {
                Directory.CreateDirectory(Path.GetDirectoryName(LogPath)!);
                File.AppendAllText(LogPath, $"[{DateTime.Now:HH:mm:ss.fff}] {msg}\n");
            }
            catch { }
        }

        protected override void OnStartup(StartupEventArgs e)
        {
            Log("OnStartup START");

            // Global exception handlers
            AppDomain.CurrentDomain.UnhandledException += (_, args) =>
            {
                Log($"FATAL [AppDomain]: {args.ExceptionObject}");
                Environment.Exit(1);
            };
            DispatcherUnhandledException += (_, args) =>
            {
                Log($"FATAL [Dispatcher]: {args.Exception}");
                MessageBox.Show($"Unhandled error:\n{args.Exception}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                args.Handled = true;
            };
            TaskScheduler.UnobservedTaskException += (_, args) =>
            {
                Log($"ERROR [Task]: {args.Exception}");
                args.SetObserved();
            };

            base.OnStartup(e);
            Log("OnStartup END - MainWindow should now be visible");
        }
    }
}
