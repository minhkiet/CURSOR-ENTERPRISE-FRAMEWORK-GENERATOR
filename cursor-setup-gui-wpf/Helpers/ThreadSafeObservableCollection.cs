using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Collections.Specialized;
using System.Windows;
using System.Windows.Threading;

namespace CursorSetupWpf.Helpers
{
    /// <summary>
    /// Thread-safe ObservableCollection that marshals changes to the UI thread.
    /// Use this instead of ObservableCollection when items are added/removed from background threads.
    /// </summary>
    public class ThreadSafeObservableCollection<T> : ObservableCollection<T>
    {
        public ThreadSafeObservableCollection() : base() { }

        public ThreadSafeObservableCollection(IEnumerable<T> collection) : base(collection) { }

        protected override void OnCollectionChanged(NotifyCollectionChangedEventArgs e)
        {
            if (Application.Current?.Dispatcher.CheckAccess() == false)
            {
                Application.Current?.Dispatcher.BeginInvoke(
                    new Action(() => OnCollectionChanged(e)),
                    DispatcherPriority.Background);
                return;
            }
            base.OnCollectionChanged(e);
        }
    }
}
