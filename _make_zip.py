import sys, zipfile
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
src.mkdir(parents=True, exist_ok=True)
(src / "rules").mkdir(exist_ok=True)
(src / "rules" / "test.mdc").write_text("# test rule\n")
(src / "rules" / "core.mdc").write_text("# core rule\n")

with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.write(src / "rules" / "test.mdc", "rules/test.mdc")
    zf.write(src / "rules" / "core.mdc", "rules/core.mdc")

print(f"created {dst} ({dst.stat().st_size} bytes)")