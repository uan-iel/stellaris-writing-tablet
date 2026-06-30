from pathlib import Path
import math
import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "src-tauri" / "icons"
ICONSET_DIR = ICON_DIR / "Stellaris.iconset"


def make_icon(size: int) -> Image.Image:
    scale = size / 512
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    radius = int(92 * scale)
    draw.rounded_rectangle(
        (0, 0, size - 1, size - 1),
        radius=radius,
        fill=(3, 10, 16, 255),
        outline=(211, 158, 87, 180),
        width=max(1, int(5 * scale)),
    )

    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse(
        (int(110 * scale), int(92 * scale), int(430 * scale), int(430 * scale)),
        fill=(36, 89, 130, 74),
    )
    image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(int(28 * scale))))
    draw = ImageDraw.Draw(image)

    stars = [
        (104, 124, 1.8, (232, 243, 255, 220)),
        (180, 96, 1.4, (244, 198, 126, 210)),
        (306, 84, 1.7, (226, 241, 255, 220)),
        (398, 148, 1.3, (244, 198, 126, 205)),
        (110, 336, 1.5, (226, 241, 255, 210)),
        (398, 362, 1.8, (244, 198, 126, 220)),
    ]
    for x, y, r, color in stars:
        cx = int(x * scale)
        cy = int(y * scale)
        rr = max(1, int(r * scale))
        draw.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=color)

    center = (size // 2, size // 2)
    ring_box = (
        int(108 * scale),
        int(108 * scale),
        int(404 * scale),
        int(404 * scale),
    )
    draw.ellipse(ring_box, outline=(224, 166, 89, 185), width=max(2, int(4 * scale)))
    draw.ellipse(
        (
            int(154 * scale),
            int(154 * scale),
            int(358 * scale),
            int(358 * scale),
        ),
        outline=(224, 166, 89, 78),
        width=max(1, int(2 * scale)),
    )

    points = [
        (178, 304, "gold"),
        (222, 242, "blue"),
        (256, 178, "gold"),
        (312, 250, "blue"),
        (360, 202, "gold"),
    ]
    coords = [(int(x * scale), int(y * scale)) for x, y, _ in points]
    for start, end in zip(coords, coords[1:]):
        draw.line((*start, *end), fill=(224, 166, 89, 150), width=max(1, int(3 * scale)))

    for x, y, tone in points:
        cx = int(x * scale)
        cy = int(y * scale)
        base = (255, 218, 143, 255) if tone == "gold" else (209, 238, 255, 255)
        halo = (255, 181, 64, 90) if tone == "gold" else (72, 162, 255, 92)
        star_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        star_draw = ImageDraw.Draw(star_layer)
        star_draw.ellipse(
            (
                cx - int(22 * scale),
                cy - int(22 * scale),
                cx + int(22 * scale),
                cy + int(22 * scale),
            ),
            fill=halo,
        )
        image.alpha_composite(star_layer.filter(ImageFilter.GaussianBlur(int(9 * scale))))
        draw = ImageDraw.Draw(image)
        rr = max(2, int(7 * scale))
        draw.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=base)
        draw.line((cx - rr * 2, cy, cx + rr * 2, cy), fill=base, width=max(1, int(2 * scale)))
        draw.line((cx, cy - rr * 2, cx, cy + rr * 2), fill=base, width=max(1, int(2 * scale)))

    crescent_outer = (
        int(218 * scale),
        int(214 * scale),
        int(294 * scale),
        int(290 * scale),
    )
    crescent_inner = (
        int(238 * scale),
        int(204 * scale),
        int(316 * scale),
        int(282 * scale),
    )
    draw.ellipse(crescent_outer, fill=(238, 205, 145, 255))
    draw.ellipse(crescent_inner, fill=(3, 10, 16, 255))

    for angle in range(0, 360, 45):
        radian = math.radians(angle)
        x1 = center[0] + math.cos(radian) * 180 * scale
        y1 = center[1] + math.sin(radian) * 180 * scale
        x2 = center[0] + math.cos(radian) * 205 * scale
        y2 = center[1] + math.sin(radian) * 205 * scale
        draw.line((x1, y1, x2, y2), fill=(224, 166, 89, 80), width=max(1, int(2 * scale)))

    return image


def save_pngs() -> None:
    ICON_DIR.mkdir(parents=True, exist_ok=True)
    sizes = {
        "icon.png": 512,
        "32x32.png": 32,
        "128x128.png": 128,
        "128x128@2x.png": 256,
        "Square30x30Logo.png": 30,
        "Square44x44Logo.png": 44,
        "Square71x71Logo.png": 71,
        "Square89x89Logo.png": 89,
        "Square107x107Logo.png": 107,
        "Square142x142Logo.png": 142,
        "Square150x150Logo.png": 150,
        "Square284x284Logo.png": 284,
        "Square310x310Logo.png": 310,
        "StoreLogo.png": 50,
    }

    for filename, size in sizes.items():
        make_icon(size).save(ICON_DIR / filename)

    make_icon(256).save(ICON_DIR / "icon.ico", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])


def save_icns() -> None:
    if ICONSET_DIR.exists():
        shutil.rmtree(ICONSET_DIR)
    ICONSET_DIR.mkdir()

    iconset_sizes = [
        ("icon_16x16.png", 16),
        ("icon_16x16@2x.png", 32),
        ("icon_32x32.png", 32),
        ("icon_32x32@2x.png", 64),
        ("icon_128x128.png", 128),
        ("icon_128x128@2x.png", 256),
        ("icon_256x256.png", 256),
        ("icon_256x256@2x.png", 512),
        ("icon_512x512.png", 512),
        ("icon_512x512@2x.png", 1024),
    ]

    for filename, size in iconset_sizes:
        make_icon(size).save(ICONSET_DIR / filename)

    subprocess.run(
        ["iconutil", "-c", "icns", str(ICONSET_DIR), "-o", str(ICON_DIR / "icon.icns")],
        check=True,
    )
    shutil.rmtree(ICONSET_DIR)


if __name__ == "__main__":
    save_pngs()
    save_icns()
    print(f"Generated Stellaris icons in {ICON_DIR}")
