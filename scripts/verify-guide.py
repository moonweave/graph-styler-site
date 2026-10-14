"""Check the static guide's bilingual sections and local link targets."""
from html.parser import HTMLParser
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]


def image_size(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return struct.unpack(">II", data[16:24])
    assert data.startswith(b"\xff\xd8"), "expected PNG or JPEG capture"
    offset = 2
    while offset < len(data):
        assert data[offset] == 0xFF
        while data[offset] == 0xFF:
            offset += 1
        marker = data[offset]
        offset += 1
        length = struct.unpack(">H", data[offset:offset + 2])[0]
        if marker in {0xC0, 0xC1, 0xC2}:
            height, width = struct.unpack(">HH", data[offset + 3:offset + 7])
            return width, height
        offset += length
    raise AssertionError("JPEG dimensions missing")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.h1 = 0
        self.sections = set()
        self.stack = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(tag)
        if tag == "img":
            self.images.append(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, "duplicate ID"
            self.ids.add(attrs["id"])
        if tag == "section":
            self.sections.add(attrs.get("id"))
        if tag == "h1":
            self.h1 += 1
        for key in ("href", "src"):
            if key in attrs:
                self.links.append(attrs[key])

    def handle_endtag(self, tag):
        if tag in {"meta", "link", "img", "br", "input", "hr"}:
            return
        assert self.stack and self.stack.pop() == tag, f"invalid nesting at </{tag}>"


pages = []
for filename in ("index.html", "en/index.html"):
    file = ROOT / filename
    html = file.read_text()
    page = Page()
    page.feed(html)
    assert not page.stack, "unclosed elements"
    assert page.h1 == 1, "one H1 required"
    assert "0.4.1" in html and "2026-10-14" in html
    assert "graph-view-content" not in html, "obsolete CSS selector"
    for link in page.links:
        if link.startswith("#"):
            assert link[1:] in page.ids, f"broken anchor: {link}"
        elif not re.match(r"[a-z]+:", link):
            local = file.parent / link.split("?")[0].split("#")[0]
            assert local.exists(), f"missing local file: {local}"
    pages.append(page)
    assert "assets/ui/" not in html, "historical UI capture still referenced"
    ui_images = page.images
    expected = {"overview.jpg", "vaporwave.jpg", "sunset.jpg", "groups.jpg", "customize.jpg", "share.jpg", "3d-panel.jpg", "3d-layouts.jpg", "export-options.jpg", "export-result.png"}
    assert {Path(image["src"]).name for image in ui_images} == expected, "current capture coverage incomplete"
    for image in ui_images:
        data = (file.parent / image["src"]).read_bytes()
        width, height = image_size(data)
        assert (int(image["width"]), int(image["height"])) == (width, height), "image aspect ratio mismatch"
        assert image.get("alt"), "screenshot needs alt text"
assert pages[0].sections == pages[1].sections, "language sections drifted"
english = (ROOT / "en/index.html").read_text()
assert not re.search(r"[가-힣]", english), "untranslated Korean on English page"
assert 'href="../?lang=ko"' in english, "English page needs a working Korean link"
css = (ROOT / "style.css").read_text()
for selector in (".hero-shot img", ".gallery img"):
    rule = re.search(re.escape(selector) + r"\s*\{([^}]+)\}", css)
    assert rule and re.search(r"height:\s*auto\s*;", rule[1]), f"{selector} must preserve rendered image ratio"
print("Guide structure, current screenshot coverage, JPEG/PNG dimensions and English navigation passed")
