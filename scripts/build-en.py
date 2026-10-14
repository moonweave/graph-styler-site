"""Generate the English page from index.html's existing data-en translations."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class EnglishPage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.output = []
        self.suppressed = 0
        self.language_link = False

    def handle_starttag(self, tag, attrs):
        if self.suppressed:
            if tag not in VOID:
                self.suppressed += 1
            return
        attrs = dict(attrs)
        translation = attrs.pop("data-en", None)
        attrs.pop("data-ko", None)
        if tag == "html":
            attrs["lang"] = "en"
        if tag == "meta" and attrs.get("name") == "description":
            attrs["content"] = "Graph Styler 0.4.1 guide: themes, color group preservation, experimental 3D, sharing and PNG export."
        if tag == "link" and attrs.get("rel") == "canonical":
            attrs["href"] = "https://graph-styler.pages.dev/en/"
        if tag == "meta" and attrs.get("property") == "og:url":
            attrs["content"] = "https://graph-styler.pages.dev/en/"
        if tag == "meta" and attrs.get("property") == "og:description":
            attrs["content"] = "Themes, your own color groups, experimental 3D and PNG export."
        for key in ("src", "href"):
            value = attrs.get(key, "")
            if value.startswith("assets/") or value in ("style.css", "script.js"):
                attrs[key] = "../" + value
        if attrs.get("data-lang"):
            language = attrs.pop("data-lang")
            attrs["class"] = "lang-btn active" if language == "en" else "lang-btn"
            attrs["href"] = "./" if language == "en" else "../?lang=ko"
            tag = "a"
            self.language_link = True
        if attrs.get("href", "").endswith("/README.ko.md"):
            attrs["href"] = attrs["href"].replace("/README.ko.md", "/README.md")
        text = "".join(f' {key}="{escape(value, quote=True)}"' if value is not None else f" {key}" for key, value in attrs.items())
        self.output.append(f"<{tag}{text}>")
        if tag == "title":
            translation = "Graph Styler — Your Obsidian graph, one click away"
        if translation is not None:
            self.output.append(translation)
            if tag not in VOID:
                self.suppressed = 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if self.suppressed:
            self.suppressed -= 1
            if self.suppressed:
                return
        if tag == "button" and self.language_link:
            tag = "a"
            self.language_link = False
        self.output.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.suppressed:
            self.output.append(data)

    def handle_entityref(self, name):
        self.handle_data(f"&{name};")

    def handle_charref(self, name):
        self.handle_data(f"&#{name};")

    def handle_decl(self, decl):
        self.output.append(f"<!{decl}>")

    def handle_comment(self, data):
        if not self.suppressed:
            self.output.append(f"<!--{data}-->")


if __name__ == "__main__":
    parser = EnglishPage()
    parser.feed((ROOT / "index.html").read_text())
    result = "".join(parser.output)
    target = ROOT / "en/index.html"
    if "--check" in sys.argv:
        if target.read_text() != result:
            raise SystemExit("English page is stale; run python3 scripts/build-en.py")
    else:
        target.write_text(result)
