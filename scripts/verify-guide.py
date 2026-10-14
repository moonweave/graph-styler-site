"""Check the static guide's bilingual sections and local link targets."""
from html.parser import HTMLParser
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[1]


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
    ui_images = [image for image in page.images if "/ui/" in image.get("src", "")]
    assert len(ui_images) == 5, "five instructional screenshots required"
    for image in ui_images:
        data = (file.parent / image["src"]).read_bytes()
        width, height = struct.unpack(">II", data[16:24])
        assert (int(image["width"]), int(image["height"])) == (width, height), "image aspect ratio mismatch"
        assert image.get("alt"), "screenshot needs alt text"
assert pages[0].sections == pages[1].sections, "language sections drifted"
english = (ROOT / "en/index.html").read_text()
assert not re.search(r"[가-힣]", english), "untranslated Korean on English page"
assert 'href="../?lang=ko"' in english, "English page needs a working Korean link"
print("Guide structure, sections, assets, anchors, five screenshot dimensions and English navigation passed")
