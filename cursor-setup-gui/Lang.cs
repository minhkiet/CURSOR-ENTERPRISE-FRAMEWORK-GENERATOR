using System;
using System.Collections.Generic;
using System.IO;

namespace CursorSetup
{
    /// <summary>
    /// Lightweight i18n loader. Reads key=value pairs from Resources/{culture}.txt.
    /// Falls back to English when a key is missing in the active language.
    /// Default culture is Vietnamese ("vi").
    /// </summary>
    internal static class Lang
    {
        public const string DefaultCulture = "vi";
        private static readonly Dictionary<string, Dictionary<string, string>> _cache
            = new Dictionary<string, Dictionary<string, string>>(StringComparer.OrdinalIgnoreCase);
        private static string _current = DefaultCulture;

        public static event Action OnChanged;

        public static string Current
        {
            get { return _current; }
            set
            {
                if (string.Equals(_current, value, StringComparison.OrdinalIgnoreCase)) return;
                _current = value;
                OnChanged?.Invoke();
            }
        }

        public static string T(string key, params object[] args)
        {
            string value = Lookup(_current, key) ?? Lookup("en", key) ?? key;
            if (args != null && args.Length > 0)
                return string.Format(value, args);
            return value;
        }

        private static string Lookup(string culture, string key)
        {
            if (!_cache.ContainsKey(culture))
                _cache[culture] = Load(culture);
            string v;
            _cache[culture].TryGetValue(key, out v);
            return v;
        }

        private static Dictionary<string, string> Load(string culture)
        {
            var dict = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
            try
            {
                string path = Path.Combine(AppContext.BaseDirectory, "Resources", culture + ".txt");
                if (!File.Exists(path)) return dict;
                foreach (string raw in File.ReadAllLines(path))
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

        private static readonly Dictionary<string, string> _descVi = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
        {
            { "Karpathy Coding Discipline", "Kỷ luật lập trình Karpathy" },
            { "Think Before Coding", "Suy nghĩ trước khi code" },
            { "Simplicity First", "Đơn giản là trên hết" },
            { "Surgical Changes", "Thay đổi có chọn lọc" },
            { "Goal-Driven Execution", "Thực thi theo mục tiêu" },
            { "Mandatory overlay for all coding tasks", "Lớp kỹ năng bắt buộc cho mọi task code" },
            { "Complements ponytail for YAGNI optimization", "Bổ sung cho ponytail để tối ưu YAGNI" },
            { "Comprehensive frontend code review skill", "Kỹ năng review frontend toàn diện" },
            { "with mandatory pre-review scope analysis", "kèm phân tích phạm vi trước review" },
            { "and post-review quality gates", "và gate chất lượng sau review" },
            { "Reviews for correctness, design quality, accessibility, performance, and taste",
              "Review tính đúng đắn, chất lượng thiết kế, accessibility, hiệu năng và thẩm mỹ" },
            { "Ponytail Skill - Lazy Senior Dev Mode", "Ponytail - Chế độ lập trình viên lười nhưng cao cấp" },
            { "Lazy Senior Dev Mode for Cursor Enterprise Framework", "Chế độ senior dev lười cho Cursor Enterprise Framework" },
            { "YAGNI optimization, minimal code", "Tối ưu YAGNI, code tối thiểu" },
            { "Complementary to karpathy-coding", "Bổ trợ cho karpathy-coding" },
            { "think first, then minimize", "nghĩ trước, rồi giảm thiểu" },
            { "Cursor Canvas is a live React app", "Cursor Canvas là ứng dụng React chạy trực tiếp" },
            { "the user can open beside the chat", "người dùng có thể mở cạnh khung chat" },
            { "mandatory pre-review scope analysis", "phân tích phạm vi trước review (bắt buộc)" },
            { "You MUST also read this skill", "Bạn PHẢI đọc skill này" },
            { "whenever you create, edit, or debug any .canvas.tsx file",
              "mỗi khi tạo, sửa hoặc debug file .canvas.tsx" },
            { "Bazi", "Tử Vi" },
            { "Bộ não Vibe Coding cho AI", "Bộ não Vibe Coding cho AI" },
            { "Hướng dẫn kỹ năng", "Hướng dẫn kỹ năng" },
            { "Coding discipline", "Kỷ luật lập trình" },
            { "before and after code", "trước và sau khi viết code" },
            { "Review for five axes", "Review 5 trục" },
            { "correctness, design, accessibility, performance, taste",
              "tính đúng đắn, thiết kế, accessibility, hiệu năng, thẩm mỹ" },
            { "Anti-patterns", "Anti-pattern" },
            { "best practice", "best practice" },
            { "Use proactively", "Dùng chủ động" },
            { "before merge", "trước khi merge" },
            { "after any non-trivial code change", "sau mỗi thay đổi code đáng kể" },
            { "Senior Staff Engineer reviewing code changes", "Senior Staff Engineer review thay đổi code" },
            { "with rigorous five-axis standards", "với tiêu chuẩn 5 trục nghiêm ngặt" },
            { "Security Engineer for OWASP Top 10", "Security Engineer cho OWASP Top 10" },
            { "threat modeling, secrets, auth, and supply-chain",
              "threat modeling, secrets, auth, và supply-chain" },
            { "Use for any security review, payment flow, auth implementation, or pre-deploy audit",
              "Dùng cho mọi security review, payment flow, auth implementation, hoặc audit trước deploy" }
        };

        public static string Translate(string text)
        {
            if (string.IsNullOrEmpty(text)) return text;
            if (!string.Equals(_current, "vi", StringComparison.OrdinalIgnoreCase)) return text;

            string result = text;
            foreach (var kv in _descVi)
            {
                if (result.IndexOf(kv.Key, StringComparison.OrdinalIgnoreCase) >= 0)
                    result = result.Replace(kv.Key, kv.Value);
            }
            return result;
        }
    }
}
