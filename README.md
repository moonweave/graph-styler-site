# Graph Styler — landing & guide

Static landing/usage page for the [Graph Styler](https://github.com/moonweave/obsidian-graph-styler) Obsidian plugin.

**Live:** https://graph-styler.pages.dev

Vanilla HTML/CSS/JS (no build). Bilingual (KO/EN toggle). Deployed to Cloudflare Pages.

`index.html` is the canonical bilingual content source. After editing its `data-en` translations, run `python3 scripts/build-en.py` to regenerate `en/index.html`. Keep `sources.json` and the visible verification date aligned with product changes. The profile guide URL stays unchanged.

## Deploy
```
npx wrangler pages deploy . --project-name graph-styler --branch main
```

Made by [Moonweave](https://github.com/moonweave).
