"""Patch App.xaml.cs to fix log path."""
from pathlib import Path

p = Path(r"cursor-setup-gui-wpf\App.xaml.cs")
s = p.read_text(encoding="utf-8")

old = r'static readonly string LogPath = @"D:\temp\cursor-setup-debug.log";'
new = ('static readonly string LogPath = Path.Combine(\n'
       '            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),\n'
       '            "CursorSetup", "cursor-setup-debug.log");')

if old not in s:
    print("SKIP: old not found")
    raise SystemExit(0)

p.write_text(s.replace(old, new), encoding="utf-8")
print("OK: log path updated to LocalAppData")
