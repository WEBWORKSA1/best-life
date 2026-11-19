# Best.Life

Free life-optimisation toolkit: the Life Score assessment, nine private browser tools, guides, an auto-updating video and research feed, challenges, lead capture and supporter pledges. Static HTML — served by GitHub Pages straight from the `main` branch root.

## Structure
- `build.py` + `content/` — generator and editorial content. Run `python3 build.py` after editing, then commit the regenerated HTML.
- `assets/` — CSS, JS (`app.js` shared, `tools.js` tools), images.
- `data/` — `videos.json`, `news.json` (rewritten daily by the workflow), `search.json`.
- `scripts/refresh.py` + `.github/workflows/refresh.yml` — daily auto-refresh (also runnable from the Actions tab).
- `docs/` — research log and the phase-wise build prompt.

## Owner checklist
1. **Custom domain** — in Settings → Pages set the custom domain to `best.life` and point DNS at GitHub Pages. AdSense reviews the root domain and reads `ads.txt` there.
2. **Forms** — submissions are relayed by FormSubmit. The first submission triggers a one-time activation email to the destination inbox; click it once and all forms go live.
3. **AdSense** — the loader is on every page (Auto ads). After approval, switch Auto ads on in the AdSense console. For EEA/UK traffic enable Google's consent message (Privacy & messaging).
4. **Donations** — pledges arrive by email; reply with your payment link. To take payments directly, link the tier buttons in `build.py` to your processor.
5. **Contest** — publish the prize and dates on `challenges.html` before opening a round.
