using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace CursorSetupWpf.Services
{
    /// <summary>
    /// Thin WPF wrapper around the existing Lang.cs logic.
    /// Reads key=value pairs from Resources/{culture}.txt.
    /// Default culture is Vietnamese ("vi").
    /// </summary>
    public static class LocalizationService
    {
        public const string DefaultCulture = "vi";
        private static readonly Dictionary<string, Dictionary<string, string>> _cache
            = new(StringComparer.OrdinalIgnoreCase);
        public static string Current { get; private set; } = DefaultCulture;
        public static event Action? CultureChanged;

        public static void SetCulture(string culture)
        {
            if (string.Equals(Current, culture, StringComparison.OrdinalIgnoreCase)) return;
            Current = culture;
            CultureChanged?.Invoke();
        }

        public static string T(string key, params object[] args)
        {
            // Ensure cache is populated on first call
            if (!_cache.ContainsKey(Current))
                _ = Load(Current);
            string value = Lookup(Current, key) ?? Lookup("en", key) ?? key;
            if (args != null && args.Length > 0)
                return string.Format(value, args);
            return value;
        }

        static string Lookup(string culture, string key)
        {
            if (!_cache.ContainsKey(culture))
                _cache[culture] = Load(culture);
            return _cache[culture].TryGetValue(key, out var v) ? v : null;
        }

        static Dictionary<string, string> Load(string culture)
        {
            var dict = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
            try
            {
                string path = Path.Combine(AppContext.BaseDirectory, "Resources", culture + ".txt");
                if (!File.Exists(path)) return dict;
                foreach (string raw in File.ReadAllLines(path, System.Text.Encoding.UTF8))
                {
                    string line = raw.Trim();
                    if (line.Length == 0 || line.StartsWith("#")) continue;
                    int eq = line.IndexOf('=');
                    if (eq < 0) continue;
                    string k = line.Substring(0, eq).Trim();
                    string v = line.Substring(eq + 1).Trim();
                    dict[k] = v.Replace("\\n", "\n");
                }
            }
            catch { }
            return dict;
        }

        public static string[] AvailableCultures => new[] { "vi", "en" };
        public static string CultureDisplayName(string code) =>
            code == "vi" ? "Tiếng Việt" : "English";
    }
}
