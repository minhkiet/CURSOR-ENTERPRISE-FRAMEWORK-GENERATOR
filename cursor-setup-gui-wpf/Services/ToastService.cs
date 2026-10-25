#nullable enable
using System;
using System.Collections.ObjectModel;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Threading;
using CursorSetupWpf.Models;

namespace CursorSetupWpf.Services
{
    /// <summary>
    /// Centralized toast notification dispatcher. Views bind to Toasts to render
    /// queued notifications and call Dismiss when the user closes them.
    /// </summary>
    public class ToastService
    {
        public ObservableCollection<ToastNotification> Toasts { get; } = new();

        public event Action<ToastNotification>? Added;
        public event Action<ToastNotification>? Removed;

        static ToastService? _instance;
        public static ToastService Instance => _instance ??= new ToastService();

        public void Show(string title, string message, string level = "info", int autoDismissMs = 4000)
        {
            Application.Current?.Dispatcher.Invoke(() =>
            {
                var toast = new ToastNotification
                {
                    Title = title,
                    Message = message,
                    Level = level,
                };
                Toasts.Add(toast);
                Added?.Invoke(toast);

                if (autoDismissMs > 0)
                {
                    var dispatcher = Application.Current?.Dispatcher ?? Dispatcher.CurrentDispatcher;
                    Task.Delay(autoDismissMs).ContinueWith(_ =>
                    {
                        dispatcher.Invoke(() => Dismiss(toast));
                    });
                }
            });
        }

        public void Success(string title, string message) =>
            Show(title, message, "success", 3500);

        public void Error(string title, string message) =>
            Show(title, message, "error", 6000);

        public void Info(string title, string message) =>
            Show(title, message, "info", 4000);

        public void Warning(string title, string message) =>
            Show(title, message, "warning", 5000);

        public void Dismiss(ToastNotification toast)
        {
            Application.Current?.Dispatcher.Invoke(() =>
            {
                if (!Toasts.Contains(toast)) return;
                Toasts.Remove(toast);
                Removed?.Invoke(toast);
            });
        }

        public void Clear()
        {
            Application.Current?.Dispatcher.Invoke(() =>
            {
                var copy = new System.Collections.Generic.List<ToastNotification>(Toasts);
                Toasts.Clear();
                foreach (var t in copy) Removed?.Invoke(t);
            });
        }
    }
}
