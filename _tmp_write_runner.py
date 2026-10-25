import base64
from pathlib import Path
B64 = "BASE64"
content = base64.b64decode(B64).decode("utf-8")
Path(r"cursor-setup-gui-wpf\Services\FrameworkRunner.cs").write_text(content, encoding="utf-8")
print("wrote", len(content))
