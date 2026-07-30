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
  `<style>` block at the top of `index.html` instead. All seven palettes are surfaced in
  the header picker **in alphabetical order**, **midnight is the default**, and an
  unrecognised stored value falls back to it. Adding a theme means touching two places:
  the `<option>` list in the markup (which `THEMES` is read back from) and the array in
  the pre-paint boot script, which runs in `<head>` and can't see either.
- Series colours are defined **per theme but with a fixed hue per series** (committed grey,
  completed blue, velocity teal, added amber, removed violet, carried red). Only the shade
  changes; don't reassign a hue to make one theme prettier, the point is that a chart reads
  the same way in all seven.
- The **contrast corrections** block in `index.html` overrides a handful of `theme.css`
  tokens for light, dark, midnight, solarized and sepia. It exists because the shared
  palettes were written for pages where red and green are decoration and `--text-muted` is
  a caption colour; here the RAG colours *are* the reading (Solarized's red was 2.8:1 on
  its own card) and muted text carries table cells, the `—` pill and the privacy note.
  Correcting them in the app keeps `theme.css` identical to the lottery copy. Every text
  token now clears 4.5:1 on `--bg-card`, `--bg-card-alt` and `--bg` in all seven themes;
  measured ratios are in the comment, so re-check them if you touch it.
- Light is corrected via `[data-theme="light"]`, **not `:root`** — its palette lives in
  `:root` in theme.css, but a `:root` rule in the app's own `<style>` sits after every
  `[data-theme]` block at equal specificity and would repaint all seven themes.
- **Everything in the header row is written into the markup at its final size** — the theme
  options, the sync button's signed-out label, and `hidden` on the team picker. The header
  paints well before the script at the foot of the page runs, so anything filled in by JS
  grows on screen: empty selects went 40px → 120px, and the sync button appeared only once
  the Firebase SDK had come over the network, which re-wrapped the row onto a second line
  and shoved the whole page down 42px. Starting hidden costs nothing; growing does. If you
  add header chrome, give it its final width in the HTML.
- The sync button is therefore **visible by default and hidden on failure**, not the other
  way round. The shared-view path hides it from the classic script (which runs during
  parse) rather than leaving it to the deferred module, so a visitor never sees a sign-in
  button blink in and out.
- `chart.min.js` is a **vendored third-party build — do not hand-edit.**
- **`metrics()` and `rag()` in `index.html` are the only places the numbers are
  calculated.** Every tile, table and chart reads from them. Thresholds change in one spot.
- **Two averaging methods, both deliberate.** `avg()` is the mean of each sprint's own
  percentage (every sprint equal); `pooled()` sums the points and divides once (bigger sprints
  weigh more). The All teams view shows both — Comparison 1 uses `avg()`, Comparison 2 uses
  `pooled()` — over the *same* sprint set, so they can only ever differ by method. **Comparison
  2 is the method the Agile Operations Dashboard uses**, as is the PI view's total row/tile
  and Rolling 5's "Pooled total" footer row; the PI "Average per sprint" tile and every
  Rolling 5 tile are `avg()`. Don't "fix" one to agree with the other, and don't let a new
  figure pick a method silently — say which it is in the UI.
- Rolling 5 deliberately keeps the **tiles at the top on `avg()` only** and shows the pooled
  figures **only as a second footer row** on its table. A fuller pooled treatment there was
  built and rejected as too much for the view — don't rebuild it.
- **Blank means 0.** `val()` saves 0 for an empty box and `metrics()` uses `num()` throughout.
  Blanks were once kept as `null` so a half-typed sprint couldn't read as real results; the
  sprint lifecycle now does that job, data mostly arrives via the Jira paste where absent
  really is zero, and a `—` where the answer is 0 looked like missing data.
- The one surviving `null` is a **percentage with `committed === 0`** — no denominator, so it
  renders as `—` and `avg()` skips it. Keep that; don't turn it into 0%.
- **Sprint lifecycle:** `sprintStatus()` resolves planned/active/complete from the dates,
  overridable per sprint via `status`. Only `isCounted()` sprints feed averages, the rolling
  window, PI tiles and the capacity target. **No dates → complete** is deliberate: all
  pre-lifecycle data is dateless and was entered as finished work; changing that would
  silently pull real history out of the averages.
- **Sprint dates project from the team's cadence** (`teamCadence()` / `cadenceDates()`): a new
  sprint form fills its own dates by counting slots from the latest dated sprint, and empty
  rows on the PI table show where they'd fall. The stride is *measured* once two sprints have
  dates, otherwise the anchor's length snapped to whole weeks — a Mon–Fri sprint is 12 days
  long and recurs every 14, so a raw length would drift onto the weekend. It fills only empty
  boxes on an **unsaved** sprint: dating an existing dateless sprint would flip it out of
  complete and silently pull history from the averages, which is the one thing the lifecycle
  rules exist to prevent. `f_start.dataset.auto` marks a projection as still ours, so changing
  the sprint number re-projects but a hand-typed date survives.
- `isCounted()` also honours `settings.includeInProgress` (default off), which opts running
  sprints into every figure for last-day planning. It's deliberately one predicate so no two
  views can disagree; `targetSprintSlot()` then stops aiming at the running sprint, since a
  sprint being counted as data isn't the one you're planning. Planned sprints never count.
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
  `sr-only` status. Every theme is WCAG AA on the figures; keep them that way.
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
- **Paste from Jira:** `parseJiraSprintReport()` / `deriveFromJira()` are pure functions on
  text — no DOM, no network, nothing saved. They only ever pre-fill form inputs, so the
  lifecycle and blank-vs-zero rules apply unchanged. Committed = every issue **not** marked
  `*` (removed ones included — they were in the sprint at start); carried out = the whole
  not-completed section, which can exceed `committed − completed`. Handles both tab-separated
  and one-cell-per-line pastes; browsers differ. **Estimates can be a range** — Jira writes a
  mid-sprint re-estimate as `8 → 2` on a row and `Story Points (21 → 15)` in a header, so
  `parsePoints()` returns `{start, current}`. **Only `committed` uses `jiraStart()`** — it
  records what was signed up for; every other figure uses `jiraCurrent()`, what the work
  turned out to be. Both sides are checksummed against Jira's own totals — don't collapse
  this back to a single number, it silently zeroed re-estimated rows before.
- An issue that is **both** starred and in the removed section is netted out of `added` *and*
  `removed`, and tracked as `addedThenRemoved` — it never joined the commitment, so counting
  it twice would penalise churn that left no trace. It is a **stored sprint field with its own
  form input**: without that, editing a sprint would silently drop it.
- A consequence of that split: **commitment completion can exceed 100%** when a team re-sizes
  upward. It's shown as-is, so completion axes use `suggestedMax: 110`, never `max` — a hard
  cap clips a real reading off the top of the chart. Jira's `Story Points (N)` per section is
  used as a checksum and any mismatch is shown to the user — **keep that visible**, it's what
  makes shipping without every real-world Jira variant safe. A section absent from the paste
  fills its field with 0 — Jira omits a section when nothing fell into it.
- `confirmOverwrite()` guards a finished sprint from an accidental save, listing the
  field-level changes rather than asking a vague "are you sure?" — a warning nobody reads is
  worse than none. It deliberately stays silent for running/planned/new sprints, for a no-op
  save, and for notes-only edits; keep that narrow, or it becomes noise people click through.
- **Read-only share links** put the data in the URL fragment (`#share=<marker>.<base64url>`,
  marker 1 = `deflate-raw`, 0 = plain JSON for browsers without `CompressionStream`). Nothing
  after `#` is sent to a server, which is the whole reason this needs no Firestore rules, no
  account and no network. `buildSharePayload()` emits a **trimmed copy** — chosen teams only,
  only the PIs their sprints reference, notes stripped unless asked for, and never anything
  identifying. Don't shortcut it to serialising `state`.
- **`save()` is the view-mode chokepoint.** `viewOnly` makes it a no-op, and because it's the
  one place that writes localStorage *and* calls `cloudPush()`, that single guard is what
  guarantees a shared link can't overwrite the viewer's own data — often another SM in the same
  browser. The sync module is gated separately via `window.svViewOnly`: if it initialised,
  `onAuthStateChanged` → `startSync()` → `svAdopt()` would replace the shared payload with the
  viewer's cloud copy and push it straight back. Keep both guards.
- UI state still moves in memory in view mode (tabs, team picker, toggles) — it just isn't
  persisted. Rows that open the sprint editor lose both handler and `.clickable` class via
  `wireEditRows()`; All-teams rows stay live because switching team is navigation, not editing.
- A shared view opens on the team's **latest sprint with data** (`focusLatestSprint()`), not on
  the payload's stored position — applied on load and on every team switch, so old links benefit
  too. Your own copy deliberately keeps the sprint you were last on: that's a working position
  you chose, not a starting point handed to you.
- A share link decodes **asynchronously**, so boot paints a holding card instead of calling
  `render()` — otherwise the viewer's own teams flash on screen under a "shared view" banner.
  A failed decode shows an error card and **never** falls through to their own data.
- **README.md is the index** — keep it current whenever the app meaningfully changes.
- After changes: **browser-test locally first** (`python3 -m http.server 8012`, or the
  desktop app's preview pane via `.claude/launch.json`), then commit, push, verify the
  Pages deploy, and spot-check live. Any local server + browser works — don't hunt for a
  specific tool.
- Write commit subject lines in plain English a non-developer can read.
