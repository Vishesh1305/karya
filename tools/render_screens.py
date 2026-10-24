"""Render the Karya reference boards to PNG screenshots.

Usage (from the repository root, after `pip install playwright` and
`playwright install chromium` on your own machine):

    python3 tools/render_screens.py
    python3 tools/render_screens.py --scale 1 --only Desktop-Today

By default the boards are rendered with the fonts that
design/reference/html/fonts.css provides. Run
design/reference/fonts/fetch-fonts.sh first so fonts.css embeds the true
fonts; otherwise the boards need network access to Google Fonts.

--substitute-css FILE injects a stylesheet after load. It was used once,
in an environment without network access, to map the four families to
locally available stand-ins. Screenshots made that way are approximate and
are labeled as such in design/reference/README.md.
"""
import argparse, json, sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "design" / "reference"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html-dir", default=str(REF / "html"))
    ap.add_argument("--out-dir", default=str(REF / "screens"))
    ap.add_argument("--boards", default=str(REF / "boards.json"))
    ap.add_argument("--scale", type=float, default=2.0, help="device scale factor (2 matches a Retina display)")
    ap.add_argument("--only", nargs="*", help="board names to render")
    ap.add_argument("--substitute-css", help="stylesheet injected after load (stand-in fonts)")
    ap.add_argument("--block-network", action="store_true", help="abort all http(s) requests")
    a = ap.parse_args()

    boards = json.loads(Path(a.boards).read_text())
    if a.only:
        boards = [b for b in boards if b["name"] in a.only]
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    sub = Path(a.substitute_css).read_text() if a.substitute_css else None

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for b in boards:
            ctx = browser.new_context(viewport={"width": b["width"], "height": b["height"]},
                                      device_scale_factor=a.scale)
            page = ctx.new_page()
            if a.block_network:
                page.route("http*://**", lambda r: r.abort())
            page.goto((Path(a.html_dir) / f"{b['name']}.html").resolve().as_uri(), wait_until="load")
            if sub:
                page.add_style_tag(content=sub)
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(300)
            target = out / f"{b['name']}.png"
            page.screenshot(path=str(target), full_page=False)
            print(f"{target}  {b['width']}x{b['height']} at {a.scale}x")
            ctx.close()
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
