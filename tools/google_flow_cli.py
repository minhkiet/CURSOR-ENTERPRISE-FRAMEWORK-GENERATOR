"""Google Flow image generation CLI for the framework asset pipeline.

The CLI uses a persistent Playwright profile so a Google sign-in survives across
runs. It never stores or prints credentials. Generated images are written under
``public/assets/generated/google-flow/<project>/`` with an ``asset-manifest.json``
and an optional global index at ``public/assets/generated/manifest.json``.

Examples::

    python tools/google_flow_cli.py --probe
    python tools/google_flow_cli.py --login
    python tools/google_flow_cli.py --prompt "bat tu ngu hanh thap than chart" --dry-run
    python tools/google_flow_cli.py --topic "bat tu ngu hanh thap than chart" --ratio 9:16 --dry-run
    python tools/google_flow_cli.py --prompt "bat tu ngu hanh thap than chart" --count 2
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

FLOW_URL = "https://flow.google.com/"
ASSET_SOURCE = "google-flow-ai"
DEFAULT_MODEL = "Nano Banana 2.1"
DEFAULT_RATIO = "1:1"
RATIO_SIZES = {
    "1:1": "1024x1024",
    "16:9": "1536x864",
    "9:16": "864x1536",
    "4:3": "1152x864",
    "3:4": "864x1152",
    "3:2": "1200x800",
    "2:3": "800x1200",
}
STYLE_PROMPTS = {
    "cinematic": "cinematic lighting, premium visual storytelling, shallow depth of field",
    "minimal": "minimal clean composition, generous negative space, restrained palette",
    "product": "premium product photography, soft studio lighting, crisp material detail",
    "illustration": "refined digital illustration, layered depth, cohesive color grading",
    "anime": "high-quality anime illustration, clean linework, expressive composition",
    "photoreal": "photorealistic rendering, natural light, lifelike textures",
}
REPO_ROOT = Path(__file__).resolve().parent.parent


class FlowLoginRequired(RuntimeError):
    """Raised when the persistent profile has no usable Google session."""


class FlowGenerationError(RuntimeError):
    """Raised when the Flow UI does not expose the expected controls."""


def slugify(value: str, max_len: int = 48) -> str:
    """Return a stable ASCII slug, including for Vietnamese input."""

    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug[:max_len].rstrip("-") or "image"


def normalize_ratio(width: int, height: int) -> str:
    """Return a reduced ``W:H`` ratio for supported positive dimensions."""

    if width < 1 or height < 1:
        return ""
    divisor = math.gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


def parse_ratio(text: str | None) -> str | None:
    """Detect an aspect ratio from a prompt or topic string."""

    if not text:
        return None

    patterns = (
        r"(?:--ar|aspect[- ]?ratio|ratio|t[yỷ] l[ệe]|ti le)\s*[:=]?\s*(\d{1,4})\s*[:/x×]\s*(\d{1,4})",
        r"\b(\d{1,4})\s*[x×]\s*(\d{1,4})\b",
        r"\b(\d{1,2}):(\d{1,2})\b",
    )
    for pattern in patterns:
        for width, height in re.findall(pattern, text, flags=re.IGNORECASE):
            ratio = normalize_ratio(int(width), int(height))
            if ratio in RATIO_SIZES:
                return ratio
    return None


def with_ratio(prompt: str, ratio: str) -> str:
    """Ensure the prompt carries the resolved ratio exactly once."""

    cleaned = re.sub(
        r"(?:--ar|aspect[- ]?ratio|ratio|t[yỷ] l[ệe]|ti le)\s*[:=]?\s*\d{1,4}\s*[:/x×]\s*\d{1,4}",
        " ",
        prompt,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"\s*,\s*", ", ", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip().strip(",").strip()
    return f"{cleaned} --ar {ratio}"


def size_for_ratio(ratio: str) -> str:
    """Return the default pixel size preset for a supported ratio."""

    return RATIO_SIZES.get(ratio, RATIO_SIZES[DEFAULT_RATIO])


def resolve_size(ratio: str, explicit: str | None) -> str:
    """Use an explicit WxH size when provided, otherwise the ratio preset."""

    if explicit and explicit.strip().lower() != "auto":
        match = re.fullmatch(r"\s*(\d{2,5})\s*[xX]\s*(\d{2,5})\s*", explicit)
        if match:
            return f"{int(match.group(1))}x{int(match.group(2))}"
    return size_for_ratio(ratio)


def build_auto_prompt(topic: str, ratio: str, style: str) -> str:
    """Create a complete Flow prompt from a short topic without an LLM call."""

    phrase = STYLE_PROMPTS.get(style, STYLE_PROMPTS["cinematic"])
    clean_topic = " ".join(topic.split())
    return (
        f"{clean_topic}, {phrase}, balanced composition, crisp details, "
        f"no watermark, no distorted text --ar {ratio}"
    )


def build_project_name(
    prompt: str,
    explicit: str | None = None,
    now: datetime | None = None,
) -> str:
    """Build a Flow project name using the framework's naming convention."""

    if explicit:
        return slugify(explicit, max_len=60)

    stamp = (now or datetime.now(timezone.utc)).strftime("%Y%m%d-%H%M%S")
    return f"flow-{slugify(prompt, max_len=40)}-{stamp}"


def iso_timestamp(now: datetime | None = None) -> str:
    value = now or datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_manifest(
    project: str,
    prompt: str,
    source_url: str,
    images: Iterable[dict[str, Any]],
    model: str = DEFAULT_MODEL,
    ratio: str | None = None,
    size: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Build an asset manifest compatible with the image-workflow template."""

    assets: list[dict[str, Any]] = []
    for image in images:
        entry = dict(image)
        entry.setdefault("source", ASSET_SOURCE)
        entry.setdefault("prompt", prompt)
        entry.setdefault("sourceUrl", source_url)
        if model:
            entry.setdefault("model", model)
        if ratio:
            entry.setdefault("ratio", ratio)
        if size:
            entry.setdefault("size", size)
        assets.append(entry)

    return {
        "project": project,
        "generated": iso_timestamp(now),
        "source": ASSET_SOURCE,
        "sourceUrl": source_url,
        "model": model,
        "ratio": ratio,
        "size": size,
        "prompt": prompt,
        "assets": assets,
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def update_asset_index(path: Path, manifest: dict[str, Any]) -> None:
    """Upsert a project's assets into the global generated-assets index."""

    data: dict[str, Any] = {"version": 1, "projects": []}
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            loaded = {}
        if isinstance(loaded, dict) and isinstance(loaded.get("projects"), list):
            data = loaded

    projects = [
        item
        for item in data["projects"]
        if isinstance(item, dict) and item.get("project") != manifest["project"]
    ]
    projects.append(
        {
            "project": manifest["project"],
            "generated": manifest["generated"],
            "prompt": manifest.get("prompt", ""),
            "assets": manifest.get("assets", []),
        }
    )

    data["version"] = 1
    data["updated"] = iso_timestamp()
    data["projects"] = projects
    write_json(path, data)


def display_path(path: Path) -> str:
    """Prefer a repo-relative path inside manifests."""

    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def extension_for(url: str, content_type: str | None = None) -> str:
    """Infer a safe image extension from a URL or HTTP content type."""

    content_type = (content_type or "").lower()
    if "jpeg" in content_type or "jpg" in content_type:
        return "jpg"
    if "webp" in content_type:
        return "webp"
    if "png" in content_type:
        return "png"

    clean_url = url.split("?", 1)[0].split("#", 1)[0].lower()
    for ext in ("webp", "jpeg", "jpg", "png", "gif"):
        if clean_url.endswith(f".{ext}"):
            return "jpg" if ext == "jpeg" else ext
    return "png"


def _first_visible(locators: Iterable[Any]) -> Any | None:
    for locator in locators:
        try:
            count = locator.count()
        except Exception:
            continue
        for index in range(count):
            item = locator.nth(index)
            try:
                if item.is_visible():
                    return item
            except Exception:
                continue
    return None


def find_button(page: Any, patterns: Iterable[str], selectors: Iterable[str] = ()) -> Any | None:
    """Find the first visible button matching a role name or CSS selector."""

    for pattern in patterns:
        locator = page.get_by_role("button", name=re.compile(pattern, re.IGNORECASE))
        button = _first_visible([locator])
        if button is not None:
            return button

    for selector in selectors:
        button = _first_visible([page.locator(selector)])
        if button is not None:
            return button
    return None


def find_option(page: Any, patterns: Iterable[str], selectors: Iterable[str] = ()) -> Any | None:
    """Find a visible model/ratio option across common ARIA roles."""

    for role in ("radio", "option", "menuitemradio", "button"):
        for pattern in patterns:
            locator = page.get_by_role(role, name=re.compile(pattern, re.IGNORECASE))
            option = _first_visible([locator])
            if option is not None:
                return option

    for selector in selectors:
        option = _first_visible([page.locator(selector)])
        if option is not None:
            return option
    return None


def select_model(page: Any, model: str, timeout_ms: int) -> bool:
    """Select the requested Flow model when its control is exposed."""

    aliases = [model, model.replace(".", " ")]
    if model == DEFAULT_MODEL:
        aliases.extend(["Nano Banana 2", "Nano Banana"])
    patterns = [rf"^{re.escape(alias)}$" for alias in dict.fromkeys(aliases)]
    option = find_option(
        page,
        patterns,
        [f'button:has-text("{alias}")' for alias in dict.fromkeys(aliases)],
    )
    if option is None:
        print(f"[flow] Model control for '{model}' not found; using Flow default.", file=sys.stderr)
        return False
    option.click()
    page.wait_for_timeout(min(1000, timeout_ms))
    return True


def apply_generation_options(
    page: Any,
    options: dict[str, Any],
    timeout_ms: int,
) -> dict[str, bool]:
    """Apply model, ratio and size controls before submitting a prompt."""

    model_selected = select_model(page, options["model"], timeout_ms)

    ratio = options["ratio"]
    option = find_option(
        page,
        [rf"^{re.escape(ratio)}$", rf"aspect ratio.*{re.escape(ratio)}"],
        [f'button:has-text("{ratio}")', f'[role="radio"]:has-text("{ratio}")'],
    )
    ratio_selected = False
    if option is not None:
        option.click()
        page.wait_for_timeout(min(800, timeout_ms))
        ratio_selected = True

    size_applied = False
    size_box = _first_visible(
        [
            page.get_by_role("textbox", name=re.compile(r"size|resolution|k[ií]ch th[uư]|dimension", re.I)),
            page.locator('input[aria-label*="size" i]'),
            page.locator('input[placeholder*="resolution" i]'),
        ]
    )
    if size_box is not None:
        try:
            size_box.fill(options["size"])
            size_box.press("Enter")
            size_applied = True
        except Exception:
            size_applied = False

    return {
        "modelSelected": model_selected,
        "ratioSelected": ratio_selected,
        "sizeApplied": size_applied,
    }


def find_textbox(page: Any) -> Any | None:
    return _first_visible(
        [
            page.get_by_role("textbox"),
            page.locator("textarea"),
            page.locator('[contenteditable="true"]'),
            page.locator('input[aria-label*="prompt" i]'),
        ]
    )


def is_login_page(page: Any) -> bool:
    url = (page.url or "").lower()
    if "accounts.google.com" in url or "/signin" in url:
        return True
    email = page.locator('input[type="email"], input[name="identifier"]')
    try:
        return email.count() > 0 and email.first.is_visible()
    except Exception:
        return False


def enter_flow_app(page: Any, timeout_ms: int) -> None:
    """Move from Flow's public landing page into the signed-in app."""

    entry = find_button(page, [r"create with google flow"])
    if entry is None:
        return
    entry.click()
    page.wait_for_timeout(min(3000, timeout_ms))


def open_flow_app(page: Any, timeout_ms: int) -> None:
    """Open Flow and enter the app when the public landing page is shown."""

    page.goto(FLOW_URL, wait_until="domcontentloaded", timeout=timeout_ms)
    page.wait_for_timeout(min(1500, timeout_ms))
    enter_flow_app(page, timeout_ms)


def create_project(page: Any, project_name: str, timeout_ms: int) -> bool:
    """Create or rename a Flow project when the UI exposes a project control."""

    button = find_button(
        page,
        [
            r"new project",
            r"create project",
            r"t[oạ]o (d[uự] án|project)",
        ],
        [
            'button[aria-label*="project" i]',
            '[role="button"][aria-label*="project" i]',
        ],
    )
    if button is None:
        print("[flow] No explicit project control; using Flow's current/auto project.")
        return False

    button.click()
    page.wait_for_timeout(min(1500, timeout_ms))

    name_box = _first_visible(
        [
            page.get_by_role("textbox", name=re.compile(r"project name|t[eê]n (d[uự] án|project)", re.I)),
            page.locator('input[aria-label*="project name" i]'),
            page.locator('input[placeholder*="project name" i]'),
        ]
    )
    if name_box is None:
        print(f"[flow] Project control clicked; Flow did not expose a name field ({project_name}).")
        return True

    name_box.fill(project_name)
    confirm = find_button(page, [r"^create$", r"^save$", r"^t[oạ]o$", r"confirm", r"rename"])
    if confirm is not None:
        confirm.click()
    else:
        name_box.press("Enter")
    page.wait_for_timeout(min(1500, timeout_ms))
    return True


def wait_for_login(page: Any, timeout_ms: int) -> None:
    """Wait until the persistent profile is no longer on a Google sign-in page."""

    deadline = time.monotonic() + timeout_ms / 1000
    while time.monotonic() < deadline:
        if not is_login_page(page):
            return
        page.wait_for_timeout(1000)
    raise FlowLoginRequired("Timed out while waiting for Google sign-in.")


def image_sources(page: Any) -> list[str]:
    """Return visible, non-tiny image URLs in DOM order."""

    sources: list[str] = []
    for image in page.locator("img").all():
        try:
            src = image.get_attribute("src") or ""
            if not src or src.startswith("data:"):
                continue
            width = image.evaluate("(element) => element.naturalWidth || 0") or 0
            if width and width < 200:
                continue
            sources.append(src)
        except Exception:
            continue
    return list(dict.fromkeys(sources))


def collect_new_images(page: Any, baseline: list[str], count: int, timeout_ms: int) -> list[str]:
    """Poll Flow's canvas until new generated images appear."""

    known = set(baseline)
    deadline = time.monotonic() + timeout_ms / 1000
    newest: list[str] = []
    while time.monotonic() < deadline:
        newest = [src for src in image_sources(page) if src not in known]
        if len(newest) >= count:
            break
        page.wait_for_timeout(1000)
    return newest[:count]


def save_image_from_url(page: Any, src: str, path: Path, timeout_ms: int) -> tuple[bool, str]:
    """Download an image URL using the browser's authenticated request context."""

    try:
        response = page.request.get(
            src,
            headers={"Referer": page.url or FLOW_URL},
            timeout=timeout_ms,
        )
        if not response.ok:
            return False, ""
        content_type = response.headers.get("content-type", "")
        body = response.body()
        if not content_type.lower().startswith("image/") and not body[:4].startswith((b"\x89PNG", b"\xff\xd8\xff")):
            return False, ""
        path.write_bytes(body)
        return True, content_type
    except Exception:
        return False, ""


def save_image_from_download(page: Any, src: str, path: Path, timeout_ms: int) -> bool:
    """Fall back to Flow's Download button for blob/data image previews."""

    image = None
    for candidate in page.locator("img").all():
        try:
            if (candidate.get_attribute("src") or "") == src:
                image = candidate
                break
        except Exception:
            continue

    button = None
    if image is not None:
        container = image.locator("xpath=ancestor::*[self::div or self::article or self::figure][1]")
        button = find_button(
            container,
            [r"download", r"t[aả]i (xu[aố]ng|v[eề])"],
            ['button[aria-label*="download" i]'],
        )
    if button is None:
        button = find_button(page, [r"download", r"t[aả]i (xu[aố]ng|v[eề])"])
    if button is None:
        return False

    try:
        with page.expect_download(timeout=timeout_ms) as download_info:
            button.click()
        download = download_info.value
        download.save_as(str(path))
        return path.exists()
    except Exception:
        return False


def probe(page: Any) -> None:
    """Print a compact UI snapshot for diagnosing Flow selectors."""

    print(f"[flow] URL: {page.url}")
    print(f"[flow] Title: {page.title()}")
    try:
        body_text = page.locator("body").inner_text(timeout=5000)
    except Exception:
        body_text = ""
    print("[flow] Body:", body_text[:3000].replace("\n", " | "))
    try:
        buttons = page.get_by_role("button").all_inner_texts()[:50]
    except Exception:
        buttons = []
    print("[flow] Buttons:", buttons)
    try:
        links = page.locator("a").evaluate_all(
            "(elements) => elements.map((element) => ({text: element.innerText.trim(), href: element.href})).filter((item) => item.href).slice(0, 40)"
        )
    except Exception:
        links = []
    print("[flow] Links:", links)
    try:
        entry_button = page.get_by_role("button", name=re.compile(r"Create with Google Flow", re.I)).first
        print("[flow] Entry button:", entry_button.evaluate("(element) => element.outerHTML.slice(0, 1200)"))
    except Exception:
        pass
    print("[flow] Login page:", is_login_page(page))


def resolve_generation_options(args: argparse.Namespace) -> dict[str, Any]:
    """Resolve prompt, model, ratio and size from CLI arguments."""

    topic = (args.topic or "").strip()
    explicit_prompt = (args.prompt or "").strip()
    if not topic and not explicit_prompt:
        raise FlowGenerationError("Provide --prompt or --topic.")

    explicit_ratio = args.ratio if args.ratio and args.ratio.lower() != "auto" else None
    if explicit_prompt:
        ratio = explicit_ratio or parse_ratio(explicit_prompt) or DEFAULT_RATIO
        prompt = with_ratio(explicit_prompt, ratio)
    else:
        ratio = explicit_ratio or parse_ratio(topic) or DEFAULT_RATIO
        prompt = build_auto_prompt(topic, ratio, args.style or "cinematic")

    return {
        "topic": topic,
        "prompt": prompt,
        "model": (args.model or DEFAULT_MODEL).strip(),
        "ratio": ratio,
        "size": resolve_size(ratio, args.size),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", help="Prompt used to generate the image(s).")
    parser.add_argument("--topic", help="Short topic; the CLI builds a complete Flow prompt from it.")
    parser.add_argument("--project", help="Explicit project name; auto-generated when omitted.")
    parser.add_argument("--count", type=int, default=1, help="Number of images to save (default: 1).")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Flow image model (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--ratio",
        default="auto",
        choices=["auto", *RATIO_SIZES],
        help="Aspect ratio; 'auto' parses the prompt/topic (default: auto).",
    )
    parser.add_argument(
        "--size",
        default="auto",
        help="Pixel size such as 1536x864; 'auto' uses the ratio preset.",
    )
    parser.add_argument(
        "--style",
        default="cinematic",
        choices=list(STYLE_PROMPTS),
        help="Prompt style used with --topic (default: cinematic).",
    )
    parser.add_argument(
        "--output-dir",
        default="public/assets/generated/google-flow",
        help="Root directory for generated project assets.",
    )
    parser.add_argument(
        "--profile-dir",
        default=".cache/google-flow/profile",
        help="Persistent browser profile directory (keeps Google login).",
    )
    parser.add_argument(
        "--index",
        default="public/assets/generated/manifest.json",
        help="Global generated-assets index. Use --no-index to skip.",
    )
    parser.add_argument("--channel", default="chrome", help="Playwright browser channel (default: chrome).")
    parser.add_argument("--headless", action="store_true", help="Run without a visible browser window.")
    parser.add_argument("--login", action="store_true", help="Open Flow and wait for a one-time Google sign-in.")
    parser.add_argument("--probe", action="store_true", help="Print a compact UI snapshot and exit.")
    parser.add_argument(
        "--probe-entry",
        action="store_true",
        help="Click 'Create with Google Flow', then print a compact UI snapshot.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print the planned project/paths without a browser.")
    parser.add_argument("--no-index", action="store_true", help="Do not update the global asset index.")
    parser.add_argument("--timeout-ms", type=int, default=120000, help="Generation timeout in ms.")
    parser.add_argument("--login-timeout-ms", type=int, default=300000, help="One-time login timeout in ms.")

    args = parser.parse_args(argv)
    if args.count < 1:
        parser.error("--count must be >= 1")
    if not any((args.prompt, args.topic, args.login, args.probe, args.probe_entry, args.dry_run)):
        parser.error("provide --prompt, --topic, --login, --probe, --probe-entry, or --dry-run")
    return args


def run_generation(args: argparse.Namespace) -> int:
    if args.prompt or args.topic:
        options = resolve_generation_options(args)
    else:
        options = {
            "topic": "",
            "prompt": "",
            "model": DEFAULT_MODEL,
            "ratio": DEFAULT_RATIO,
            "size": size_for_ratio(DEFAULT_RATIO),
        }

    project = build_project_name(
        args.topic or args.prompt or args.project or "flow",
        explicit=args.project,
    )
    output_dir = Path(args.output_dir).resolve()
    project_dir = output_dir / project
    manifest_path = project_dir / "asset-manifest.json"
    index_path = Path(args.index).resolve()
    profile_dir = Path(args.profile_dir).resolve()

    if args.dry_run:
        print(json.dumps(
            {
                "project": project,
                "prompt": options["prompt"] or None,
                "model": options["model"],
                "ratio": options["ratio"],
                "size": options["size"],
                "outputDir": display_path(project_dir),
                "manifest": display_path(manifest_path),
                "index": None if args.no_index else display_path(index_path),
                "profile": display_path(profile_dir),
            },
            ensure_ascii=False,
            indent=2,
        ))
        return 0

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise FlowGenerationError(
            "Playwright is not installed. Run: pip install playwright"
        ) from exc

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            channel=args.channel or None,
            headless=args.headless,
            accept_downloads=True,
            viewport={"width": 1440, "height": 900},
        )
        page = context.pages[0] if context.pages else context.new_page()

        if args.probe:
            page.goto(FLOW_URL, wait_until="domcontentloaded", timeout=args.timeout_ms)
            page.wait_for_timeout(min(1500, args.timeout_ms))
            probe(page)
            context.close()
            return 0

        open_flow_app(page, args.timeout_ms)

        if args.probe_entry:
            probe(page)
            context.close()
            return 0

        if args.login:
            print("[flow] Sign in in the opened browser; this profile will remember the session.")
            wait_for_login(page, args.login_timeout_ms)
            print("[flow] Login detected. You can close this window and rerun with --prompt.")
            context.close()
            return 0

        if is_login_page(page):
            context.close()
            raise FlowLoginRequired(
                "Google sign-in is required. Run with --login once, then rerun with --prompt."
            )

        selected = apply_generation_options(page, options, args.timeout_ms)
        print(f"[flow] Options: {json.dumps(selected, ensure_ascii=False)}")

        create_project(page, project, args.timeout_ms)
        baseline = image_sources(page)

        textbox = find_textbox(page)
        if textbox is None:
            context.close()
            raise FlowGenerationError("Could not find a prompt textbox on the Flow page.")
        textbox.fill(options["prompt"])

        generate_button = find_button(
            page,
            [r"generate", r"create", r"t[aạ]o", r"sinh"],
            ['button[aria-label*="generate" i]', '[role="button"][aria-label*="generate" i]'],
        )
        if generate_button is None:
            context.close()
            raise FlowGenerationError("Could not find Flow's Generate button.")
        generate_button.click()

        sources = collect_new_images(page, baseline, args.count, args.timeout_ms)
        if not sources:
            context.close()
            raise FlowGenerationError("No generated image appeared before the timeout.")

        project_dir.mkdir(parents=True, exist_ok=True)
        assets: list[dict[str, Any]] = []
        for index, src in enumerate(sources, start=1):
            path = project_dir / f"{slugify(project, 48)}-{index}.tmp"
            saved, content_type = save_image_from_url(page, src, path, args.timeout_ms)
            if saved:
                ext = extension_for(src, content_type)
                final_path = path.with_suffix(f".{ext}")
                path.replace(final_path)
            else:
                path.unlink(missing_ok=True)
                ext = extension_for(src)
                final_path = path.with_suffix(f".{ext}")
                if not save_image_from_download(page, src, final_path, args.timeout_ms):
                    continue

            data = final_path.read_bytes()
            assets.append(
                {
                    "name": final_path.name,
                    "path": display_path(final_path),
                    "source": ASSET_SOURCE,
                    "sourceUrl": src,
                    "prompt": options["prompt"],
                    "model": options["model"],
                    "ratio": options["ratio"],
                    "size": options["size"],
                    "bytes": len(data),
                    "fileSize": f"{max(1, round(len(data) / 1024))}KB",
                }
            )

        context.close()

    if not assets:
        raise FlowGenerationError("Flow produced previews but no image could be saved.")

    manifest = build_manifest(
        project,
        options["prompt"],
        FLOW_URL,
        assets,
        model=options["model"],
        ratio=options["ratio"],
        size=options["size"],
    )
    write_json(manifest_path, manifest)
    if not args.no_index:
        update_asset_index(index_path, manifest)

    print(json.dumps(
        {
            "project": project,
            "prompt": options["prompt"],
            "model": options["model"],
            "ratio": options["ratio"],
            "size": options["size"],
            "manifest": display_path(manifest_path),
            "assets": [item["path"] for item in assets],
            "index": None if args.no_index else display_path(index_path),
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    args = parse_args(argv)
    try:
        return run_generation(args)
    except FlowLoginRequired as exc:
        print(f"[flow] {exc}", file=sys.stderr)
        print(
            "[flow] Next: python tools/google_flow_cli.py --login",
            file=sys.stderr,
        )
        return 2
    except FlowGenerationError as exc:
        print(f"[flow] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
