# Graph Styler — landing & guide

Static landing/usage page for the [Graph Styler](https://github.com/moonweave/obsidian-graph-styler) Obsidian plugin.

**Live:** https://graph-styler.pages.dev

Vanilla HTML/CSS/JS (no build). Bilingual (KO/EN toggle). Deployed to Cloudflare Pages.

`index.html` is the canonical bilingual content source. After editing its `data-en` translations, run `python3 scripts/build-en.py` to regenerate `en/index.html`. Keep `sources.json` and the visible verification date aligned with product changes. The profile guide URL stays unchanged.

All guide images use `assets/research-041/`: actual research-wiki, Graph Styler 0.4.1, Obsidian 1.14.4, dark app theme, English UI. The 2,054-note Vaporwave PNG was exported through the native button; one administrative note was excluded for publication. Only general research-topic hub titles remain visible. CSS enlarges panels without distorting originals. Historical demo assets are retained but never referenced. See `capture-provenance.json`. Run `python3 scripts/verify-guide.py` and inspect actual browser rendering before publication.

## Deploy
```
npx wrangler pages deploy . --project-name graph-styler --branch main
```

Made by [Moonweave](https://github.com/moonweave).
