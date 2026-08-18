using System.Diagnostics;
using System;
using System.IO;
using System.Windows;

namespace CursorSetupWpf
{
    public partial class App : Application
    {
        static readonly string LogPath = @"D:\temp\cursor-setup-debug.log";

        static void Log(string msg)
        {
            try
            {
                File.AppendAllText(LogPath, $"[{DateTime.Now:HH:mm:ss.fff}] {msg}\n");
            }
            catch { }
        }

        protected override void OnStartup(StartupEventArgs e)
        {
            Log("OnStartup START");
            base.OnStartup(e);
            Log("OnStartup END");
        }
    }
}
