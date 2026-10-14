# Graph Styler — landing & guide

Static landing/usage page for the [Graph Styler](https://github.com/moonweave/obsidian-graph-styler) Obsidian plugin.

**Live:** https://graph-styler.pages.dev

Vanilla HTML/CSS/JS (no build). Bilingual (KO/EN toggle). Deployed to Cloudflare Pages.

`index.html` is the canonical bilingual content source. After editing its `data-en` translations, run `python3 scripts/build-en.py` to regenerate `en/index.html`. Keep `sources.json` and the visible verification date aligned with product changes. The profile guide URL stays unchanged.

`assets/ui/` contains unmodified public captures from the plugin's `0.4.1` documentation assets. These images were captured before the new preservation option and newer 3D selectors; captions explicitly identify that limit. Do not present them as newly captured 0.4.1 UI. The language switch selects the corresponding Korean/English image and full-size link. Run `python3 scripts/verify-guide.py` to check nesting, local links and PNG dimensions.

## Deploy
```
npx wrangler pages deploy . --project-name graph-styler --branch main
```

Made by [Moonweave](https://github.com/moonweave).
