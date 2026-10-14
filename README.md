# Graph Styler — landing & guide

Static landing/usage page for the [Graph Styler](https://github.com/moonweave/obsidian-graph-styler) Obsidian plugin.

**Live:** https://graph-styler.pages.dev

Vanilla HTML/CSS/JS (no build). Bilingual (KO/EN toggle). Deployed to Cloudflare Pages.

`index.html` is the canonical bilingual content source. After editing its `data-en` translations, run `python3 scripts/build-en.py` to regenerate `en/index.html`. Keep `sources.json` and the visible verification date aligned with product changes. The profile guide URL stays unchanged.

`assets/research-041/` contains actual research-wiki graph, Customize, group-preservation and export-option captures from Graph Styler 0.4.1 in Obsidian 1.14.4. Search/file sidebars and note titles are hidden. `assets/ui-041/` supplies synthetic-demo sharing and 3D settings plus an actual demo PNG export. Both languages use English UI captures. CSS enlarges panels without distorting images; links open originals. See `capture-provenance.json` for conditions. Historical `assets/ui/` files are retained but not referenced. Run `python3 scripts/verify-guide.py` to check structure, links, dimensions and coverage; actual browser rendering must also be inspected.

## Deploy
```
npx wrangler pages deploy . --project-name graph-styler --branch main
```

Made by [Moonweave](https://github.com/moonweave).
