"""Replace FindFrameworkModulePath."""
from pathlib import Path

p = Path(r"cursor-setup-gui-wpf\Services\FrameworkRunner.cs")
s = p.read_text(encoding="utf-8")

# Step 1: locate and remove the old method body
marker = "static string FindFrameworkModulePath(string installPath)"
idx = s.find(marker)
assert idx != -1
end_marker = 'return "";\n        }\n'
end_idx = s.find(end_marker, idx)
assert end_idx != -1
end_idx += len(end_marker)

print(f"OLD METHOD RANGE: {idx}..{end_idx}")
print("OLD METHOD:")
print(s[idx:end_idx])
print("=" * 60)
