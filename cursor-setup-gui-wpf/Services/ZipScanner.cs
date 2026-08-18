using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Threading.Tasks;

namespace CursorSetupWpf.Services
{
    public static class ZipScanner
    {
        public static readonly string[] CategoryOrder = new[]
        {
            "rules", "skills", "agents", "commands", "hooks", "knowledge",
            "prompts", "references", "workflows", "templates", "memory", "scripts",
            "mcp"  // MCP tools: cursor-framework-mcp, cursor-autopilot-mcp, cursor-memory-mcp
        };

        public static readonly HashSet<string> CoreCategories = new(StringComparer.OrdinalIgnoreCase)
        {
            "scripts", "memory", "mcp"
        };

        public static string EMBEDDED_ZIP_NAME = "cursor-setup.zip";

        public static Dictionary<string, List<string>> ScanCategories(string zipPath)
        {
            var result = new Dictionary<string, List<string>>(StringComparer.OrdinalIgnoreCase);
            using var archive = ZipFile.OpenRead(zipPath);
            foreach (var entry in archive.Entries)
            {
                if (string.IsNullOrEmpty(entry.FullName)) continue;
                string normalized = entry.FullName.Replace('\\', '/');
                var parts = normalized.Split('/');
                if (parts.Length < 2) continue;

                string topCategory = parts[0];
                if (!CategoryOrder.Contains(topCategory, StringComparer.OrdinalIgnoreCase))
                    continue;

                if (!result.ContainsKey(topCategory))
                    result[topCategory] = new List<string>();

                string groupKey = parts[1];
                if (!result[topCategory].Contains(groupKey))
                    result[topCategory].Add(groupKey);
            }

            foreach (string c in CategoryOrder)
                if (!result.ContainsKey(c))
                    result[c] = new List<string>();
            return result;
        }

        public static string FindZipPath()
        {
            string exeDir = AppContext.BaseDirectory;
            string[] candidates = new[]
            {
                Path.Combine(exeDir, EMBEDDED_ZIP_NAME),
                Path.Combine(Directory.GetCurrentDirectory(), EMBEDDED_ZIP_NAME)
            };
            string dir = exeDir;
            for (int i = 0; i < 3; i++)
            {
                dir = Directory.GetParent(dir)?.FullName!;
                if (string.IsNullOrEmpty(dir)) break;
                candidates = candidates.Concat(new[] { Path.Combine(dir, EMBEDDED_ZIP_NAME) }).ToArray();
            }
            foreach (string c in candidates)
                if (File.Exists(c)) return c;
            return null!;
        }

        public static string ExtractDescription(string zipPath, string topCategory, string item)
        {
            try
            {
                using var archive = ZipFile.OpenRead(zipPath);
                string sampleEntry = FindSampleEntry(archive, topCategory, item);
                if (sampleEntry == null) return "";

                var entry = archive.GetEntry(sampleEntry);
                if (entry == null) return "";

                const int maxBytes = 8 * 1024;
                int toRead = (int)Math.Min((long)maxBytes, entry.Length);
                if (toRead <= 0) return "";

                byte[] buffer = new byte[toRead];
                using var s = entry.Open();
                int read = 0;
                while (read < toRead)
                {
                    int n = s.Read(buffer, read, toRead - read);
                    if (n <= 0) break;
                    read += n;
                }
                if (read < toRead) Array.Resize(ref buffer, read);

                string text = System.Text.Encoding.UTF8.GetString(buffer);
                if (text.Length > 0 && text[0] == '\uFEFF') text = text.Substring(1);
                return ExtractDescriptionFromText(text);
            }
            catch { return ""; }
        }

        static string FindSampleEntry(ZipArchive archive, string topCategory, string item)
        {
            string prefix = topCategory + "/" + item + "/";
            string[] preferredNames;
            if (string.Equals(topCategory, "skills", StringComparison.OrdinalIgnoreCase))
                preferredNames = new[] { "SKILL.md", "README.md" };
            else if (string.Equals(topCategory, "commands", StringComparison.OrdinalIgnoreCase) ||
                     string.Equals(topCategory, "hooks", StringComparison.OrdinalIgnoreCase))
                preferredNames = new[] { "command.md", "hook.md", "README.md", "index.md" };
            else if (string.Equals(topCategory, "knowledge", StringComparison.OrdinalIgnoreCase))
                preferredNames = new[] { "architecture.md", "best-practice.md", "README.md", "faq.md", "glossary.md" };
            else if (string.Equals(topCategory, "templates", StringComparison.OrdinalIgnoreCase))
                preferredNames = new[] { "GETTING-STARTED.md", "README.md", "index.md" };
            else
                preferredNames = new[] { "README.md", "index.md" };

            foreach (string name in preferredNames)
            {
                string p = prefix + name;
                if (archive.GetEntry(p) != null) return p;
            }

            foreach (var e in archive.Entries)
            {
                if (e.FullName.Replace('\\', '/').StartsWith(prefix, StringComparison.OrdinalIgnoreCase)
                    && !string.IsNullOrEmpty(e.Name))
                    return e.FullName;
            }
            return null!;
        }

        static string ExtractDescriptionFromText(string text)
        {
            string norm = text.Replace("\r\n", "\n").Replace("\r", "\n");
            if (norm.StartsWith("---"))
            {
                int endIdx = norm.IndexOf("\n---", 3);
                if (endIdx > 0)
                {
                    string fm = norm.Substring(3, endIdx - 3);
                    foreach (string rawLine in fm.Split('\n'))
                    {
                        string line = rawLine.Trim();
                        if (line.StartsWith("description:", StringComparison.OrdinalIgnoreCase))
                        {
                            string desc = line.Substring("description:".Length).Trim();
                            if (desc.Length >= 2 &&
                                ((desc[0] == '"' && desc[desc.Length - 1] == '"') ||
                                 (desc[0] == '\'' && desc[desc.Length - 1] == '\'')))
                                desc = desc.Substring(1, desc.Length - 2);
                            return desc;
                        }
                    }
                }
            }

            foreach (string rawLine in norm.Split('\n'))
            {
                string line = rawLine.Trim().TrimEnd('\r');
                if (line.Length == 0) continue;
                if (line.StartsWith("#")) continue;
                if (line.StartsWith("---")) continue;
                if (line.StartsWith(">")) continue;
                if (line.StartsWith("```")) continue;
                if (System.Text.RegularExpressions.Regex.IsMatch(line, @"^[A-Za-z][A-Za-z _-]{0,30}:\s"))
                    continue;
                if (line.StartsWith("[") && line.Contains("](")) continue;
                if (line.StartsWith("1.") || line.StartsWith("2.") || line.StartsWith("3.")) continue;
                string stripped = line.TrimStart('*', '_', '>', '-', ' ');
                if (stripped.Length == 0) continue;
                return stripped;
            }
            return "";
        }
    }
}
