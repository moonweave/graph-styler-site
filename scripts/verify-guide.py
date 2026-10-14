"""Check the static guide's bilingual sections and local link targets."""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.h1 = 0
        self.sections = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
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


pages = []
for filename in ("index.html", "en/index.html"):
    file = ROOT / filename
    html = file.read_text()
    page = Page()
    page.feed(html)
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
assert pages[0].sections == pages[1].sections, "language sections drifted"
english = (ROOT / "en/index.html").read_text()
assert not re.search(r"[가-힣]", english), "untranslated Korean on English page"
assert 'href="../?lang=ko"' in english, "English page needs a working Korean link"
print("Guide structure, sections, assets, anchors and English navigation passed")
