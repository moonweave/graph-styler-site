# Graph Styler — landing & guide

Static landing/usage page for the [Graph Styler](https://github.com/moonweave/obsidian-graph-styler) Obsidian plugin.

**Live:** https://graph-styler.pages.dev

Vanilla HTML/CSS/JS (no build). Bilingual (KO/EN toggle). Deployed to Cloudflare Pages.

`index.html` is the canonical bilingual content source. After editing its `data-en` translations, run `python3 scripts/build-en.py` to regenerate `en/index.html`. Keep `sources.json` and the visible verification date aligned with product changes. The profile guide URL stays unchanged.

`assets/ui-041/` contains fresh, unedited full-window captures taken through Computer Use on 2026-10-14, with Graph Styler 0.4.1 in Obsidian 1.14.4. Both guide languages use the same English UI captures with localized captions. CSS focuses on the right panel without altering image files; links open the complete originals. The PNG result was generated through the actual Export button. All notes are synthetic demo notes. See `capture-provenance.json` for the released-code hash and capture conditions. Historical `assets/ui/` files are retained but never referenced in the guide. Run `python3 scripts/verify-guide.py` to check nesting, local links, image dimensions and current-capture coverage.

## Deploy
```
npx wrangler pages deploy . --project-name graph-styler --branch main
```

Made by [Moonweave](https://github.com/moonweave).
