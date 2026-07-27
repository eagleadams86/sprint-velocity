# Sprint Velocity

A sprint predictability tracker for Scrum Masters — commitment completion, break-in,
carryover and velocity across multiple teams. Deployed via GitHub Pages:
https://eagleadams86.github.io/sprint-velocity/

Charles uses this as a Scrum Master across several teams, and shares the **URL** with
fellow SMs — each person signs in with their own Google account and sees only their own
data. There is deliberately no shared-workspace/multi-SM-editing model.

- The app is **one file — `index.html`** (no build step), alongside `theme.css` and a
  vendored `chart.min.js`. Keep it that way: no npm, no bundler, no CDN calls.
- `theme.css` is a **copy** of the canonical palette in the lottery repo — don't diverge
  it. App-specific tokens (chart series colours, threshold-band tints) live in the
  `<style>` block at the top of `index.html` instead. Only Light and Midnight are surfaced
  in the theme picker.
- `chart.min.js` is a **vendored third-party build — do not hand-edit.**
- **`metrics()` and `rag()` in `index.html` are the only places the numbers are
  calculated.** Every tile, table and chart reads from them. Thresholds change in one spot.
- Sprints with `committed === 0` must keep returning `null` percentages, not zeros — they
  render as `—` and drop out of averages. Same for any figure not yet entered: `val()` saves
  `null` for a blank box and `metrics()` keeps it null. **Never coerce these to 0** — that
  is what made a mid-flight sprint read as a 0% result. `sum()` coerces (it would go NaN);
  `avg()` filters (that null-skipping is what the whole lifecycle leans on).
- **Sprint lifecycle:** `sprintStatus()` resolves planned/active/complete from the dates,
  overridable per sprint via `status`. Only `isCounted()` sprints feed averages, the rolling
  window, PI tiles and the capacity target. **No dates → complete** is deliberate: all
  pre-lifecycle data is dateless and was entered as finished work; changing that would
  silently pull real history out of the averages.
- `rollingSprints()` is the chokepoint — filtering there covers Rolling 5, All teams and the
  capacity target at once. The PI view filters separately via its own `closed` list.
- Exclusions must never be silent: every view that drops a sprint says which one and why
  (`openSprintsNote()`). A sprint sitting outside the numbers unnoticed is worse than the
  bug this replaced.
- `fmtPct()` takes the RAG scale and drops to one decimal when rounding would cross a
  threshold, so a displayed figure never contradicts the colour next to it (84.6% must not
  render as "85%" in yellow). Any new percentage display must pass its scale.
- Sprint 6 is the IP sprint: **excluded from the rolling window by default**, with a toggle.
- `nextSprintTarget()` recommends a commitment from **mean committed-points-completed**,
  deliberately *not* mean velocity — velocity includes break-in, so committing to it
  over-commits the team. Don't "improve" it into a velocity-based figure; the reasoning is
  in the comment above the function and in the card's "How this is worked out".
- RAG state must never be conveyed by colour alone — tiles and pills carry a glyph and an
  `sr-only` status. Both themes are WCAG AA; keep them that way.
- Charts resolve their colours from CSS custom properties at construction time, so a theme
  switch has to rebuild them (`render()` does this). Chart animation is deliberately off.
- Optional cross-device sync is ported from PAPTrack: Google sign-in + one Firestore doc
  per user at `sprintvelocity/{uid}`, backed by the `sprintvelocity-141b7` Firebase project.
  `FIREBASE_CONFIG` controls it; set it to `null` to force fully-local mode. The config is
  a public client config, not a secret — access is enforced by the Firestore rules. The
  first-sign-in "which copy do you want to keep?" dialog is load-bearing; don't replace it
  with timestamp guessing.
- Firebase authorized domain is `eagleadams86.github.io`, so sync works at this
  `/sprint-velocity/` path unchanged.
- **README.md is the index** — keep it current whenever the app meaningfully changes.
- After changes: **browser-test locally first** (`python3 -m http.server 8012`, or the
  desktop app's preview pane via `.claude/launch.json`), then commit, push, verify the
  Pages deploy, and spot-check live. Any local server + browser works — don't hunt for a
  specific tool.
- Write commit subject lines in plain English a non-developer can read.
