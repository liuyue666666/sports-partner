"""Generate minimal 81x81 PNG tab bar icons for WeChat mini program."""

from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    raise SystemExit("Install Pillow: pip install pillow")

ICONS_DIR = Path(__file__).resolve().parent.parent / "miniapp" / "static" / "icons"

CONFIG = [
    ("home", "#999999", "#07c160"),
    ("match", "#999999", "#07c160"),
    ("activity", "#999999", "#07c160"),
    ("profile", "#999999", "#07c160"),
]


def make_icon(path: Path, color: str) -> None:
    img = Image.new("RGBA", (81, 81), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([16, 16, 65, 65], fill=color)
    img.save(path)


def main() -> None:
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    for name, normal, active in CONFIG:
        make_icon(ICONS_DIR / f"{name}.png", normal)
        make_icon(ICONS_DIR / f"{name}-active.png", active)
    print(f"Generated icons in {ICONS_DIR}")


if __name__ == "__main__":
    main()
