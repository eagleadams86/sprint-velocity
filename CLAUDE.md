# Sprint Velocity

A sprint predictability tracker for Scrum Masters — commitment completion, break-in,
carryover and velocity across multiple teams. Deployed via GitHub Pages:
https://eagleadams86.github.io/sprint-velocity/

Charles uses this as a Scrum Master across several teams, and shares the **URL** with
fellow SMs — each person signs in with their own Google account and sees only their own
data. There is deliberately no shared-workspace/multi-SM-editing model.

- The app is **one file — `index.html`** (no build step), alongside `theme.css` and a
  vendored `chart.min.js`. Keep it that way: no npm, no bundler, no CDN calls.
- `theme.css` is a **copy of the generated file from `~/claude-theme-pack`** (private
  repo eagleadams86/claude-theme-pack), the source of truth for the palette of ALL apps —
  don't diverge it; palette changes go through the pack's `tokens.json` + contrast gate.
  App-specific tokens (chart series colours, threshold-band tints) live in the `<style>`
  block at the top of `index.html` instead. The four themes (Midnight default) are surfaced
  in the header picker **in alphabetical order** — Dark, Light, Midnight, Sepia — and an
  unrecognised stored value (including the retired forest/synthwave/solarized) falls back
  to midnight.
  Adding a theme means touching two places: the `<option>` list in the markup (which
  `THEMES` is read back from) and the array in the pre-paint boot script, which runs in
  `<head>` and can't see either — plus the pack itself, which is where themes live now.
- Series colours are defined **per theme but with a fixed hue per series** (committed grey,
  completed blue, velocity teal, added amber, removed violet, carried red). Only the shade
  changes; don't reassign a hue to make one theme prettier, the point is that a chart reads
  the same way in all four.
- **Colour is not what tells the six series apart — texture is.** `SERIES_TEXTURE` gives each
  series a fixed fill pattern the same way the palette gives it a fixed hue (committed solid,
  completed `/`, velocity `\`, added dots, carried horizontal, removed cross), built as a
  CanvasPattern by `seriesFill()`; the three churn *lines*, where a fill is no use, carry a
  dash pattern and a point shape instead. Chart.js takes a pattern anywhere a colour goes, so
  legend swatches and tooltip boxes get the cue for free. Measured with the pack's
  `simulate()`/`delta_e()` at its threshold of 18: committed vs velocity is deltaE 9.1–17.5 in
  **every** theme and they are two of the three PI-chart bars; committed vs carried fails in
  midnight and sepia. Six categories don't fit on the blue-yellow axis that survives red-green
  deficiency — it carries about three levels — so no re-shading fixes this. Re-shading was
  measured anyway: it clears the gate only by driving committed to near-black on the light and
  sepia cards, and in midnight exactly **one** candidate passed, at 19.0 against a threshold of
  18. Don't swap the texture back out for a colour tweak, and don't re-hue.
  Stripes are the series colour pushed *further from the card* (toward black on a light card,
  white on a dark one), never a second colour, so a textured bar can't spend the 3:1 non-text
  contrast the flat colour already had.
- **`--c-completed` vs `--c-removed` is deltaE 0.4 in sepia and is deliberately left alone.**
  Blue is never in the churn chart and violet is never in the others, so nothing ever asks you
  to tell those two apart. Only pairs that share a chart have to clear the gate — measuring all
  15 pairs makes the palette look far worse than it reads.
- The old **contrast corrections** block is gone: the theme pack's gate now verifies every
  text and status token at 4.5:1 on `--bg`, `--surface` and `--surface-alt` in all four
  themes, so the shared palette needs no local nudges. If a palette problem surfaces, fix
  it in the pack's `tokens.json` (every app benefits) rather than re-introducing overrides
  here — that's the drift policy in the pack's CLAUDE.md.
- If an app-local override is ever unavoidable, target `[data-theme="…"]` blocks, **not
  `:root`** — a `:root` rule in the app's own `<style>` sits after every `[data-theme]`
  block at equal specificity and would repaint all themes. (Note: in the pack's theme.css
  the `:root` palette is Midnight, not Light.)
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
  2 is the method the Agile Operations Dashboard uses**, as is the PI view's "PI total" row
  and commitment-completion tile, and Rolling 5's "Pooled total" row; the PI "Average per
  sprint" tile/row and every Rolling 5 tile are `avg()`. Don't "fix" one to agree with the
  other, and don't let a new figure pick a method silently — say which it is in the UI.
- Current PI and Rolling 5 each show the two methods as **a pair of footer rows** on their
  numbers table, average first then pooled, each with a `helpBtn` naming its method and the
  other. Rolling 5 deliberately keeps its **tiles on `avg()` only** — a fuller pooled
  treatment there (extra tile cards, a worked-example note) was built and rejected as too
  much for the view, so don't rebuild it.
- **Help buttons (`helpBtn`) need breathing room**: `.tile-help` carries `margin-left: 7px`,
  zeroed inside `.tile .label` (a flex row that already pins it right). `td:has(.tile-help)`
  is `nowrap` so a wrapping label can't orphan the circle onto a line of its own. This is a
  standing preference of Charles's across all his projects — icons must never sit flush
  against the word.
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
- **A RAG surface is a tint fill plus a status-colour edge, everywhere** — `.tile`, `.pill` and
  the All teams bars all pair `--green`/`--amber`/`--red` with their `-bg` tint. `ragVar()` is
  the one place that maps a value to those custom properties, so a chart can't drift from the
  pill beside it; don't inline the ternary back into a dataset. Solid status-coloured bars are
  what this replaced: the contrast gate forces all three colours dark on Light and Sepia, so a
  large solid area reads olive/maroon/bottle-green — three near-blacks — which is the same
  failure the tinted tiles fixed. The view tabs
  are a real tablist: `aria-controls` onto `#views` (`role="tabpanel"`), roving `tabindex`
  set in `render()` beside `aria-selected`, and arrow/Home/End wired at the foot of the
  file, skipping hidden tabs. `role="tabpanel"` sits on the inner `#views` div, **not on
  `<main>`** — putting it on the element replaces its role, which silently cost the page its
  main landmark once already.
- **A clickable row needs a real control in it.** Every table's first cell is a
  `<th scope="row">` holding a `.rowbtn` — a `<tr>` can't take focus, and giving it a button
  role would break the grid semantics that make nine numeric columns readable. The row keeps
  its own click handler for the mouse and the button stops propagation, or the editor opens
  twice and `showModal()` throws. `wireEditRows()` replaces the button with plain text in a
  shared view rather than leaving a control that focuses and does nothing.
- **Row-header cells need re-styling back.** The `th` rules are written for column headings,
  so `tbody th, tfoot th` undo the uppercase/grey/small treatment, and `tfoot th` re-takes the
  bold total styling from `tfoot td`. `th:has(.tile-help)` carries the nowrap guard now that
  the summary labels are `th`.
- **Live regions must stay in the tree.** `#sprintWarn`, `#shareMeta` and `#shareWarn` are
  `role="status"` and are emptied rather than `hidden` — an element toggled out of the tree
  announces nothing on the way back — with `.warn:empty` collapsing them visually. The Jira
  preview is deliberately *not* a live region: it's far too long to read aloud, so `box.focus()`
  moves the user to it instead.
- **Ids from outside are not trusted.** `sanitizeIds()` runs on everything entering through
  `load()`, `decodeShare()`, the JSON import and `svAdopt()`, replacing any id that isn't
  `[A-Za-z0-9_-]{1,64}` with a fresh one and rewriting every reference through the same map.
  Names were always escaped; ids go into attributes (`data-id`, `<option value>`) in a dozen
  places and weren't, so a crafted share link could run script — which `viewOnly` does
  nothing about, since injected code doesn't go through `save()`. Render sites escape too.
  Don't add a render site that interpolates an id raw, and don't drop the boundary check.
- Charts resolve their colours from CSS custom properties at construction time, so a theme
  switch has to rebuild them (`render()` does this). Chart animation is deliberately off.
- Optional cross-device sync is ported from PAPTrack: Google sign-in + one Firestore doc
  per user at `sprintvelocity/{uid}`, backed by the `sprintvelocity-141b7` Firebase project.
  `FIREBASE_CONFIG` controls it; set it to `null` to force fully-local mode. The config is
  a public client config, not a secret — access is enforced by the Firestore rules. The
  first-sign-in "which copy do you want to keep?" dialog is load-bearing; don't replace it
  with timestamp guessing. Underneath it, **an empty copy never beats a copy with data in
  it**, whichever is newer — the dialog only fires when both sides hold data, so without
  that rule a fresh browser's empty push (stamped `now`) silently emptied the device that
  had the sprints. Keep both halves; the guard is what makes the dialog's narrow trigger
  safe.
- **Sync failures are surfaced, not logged.** `syncError` + `setSyncError()`/`clearSyncError()`
  drive `updateUI()`, so the button reads "⚠️ Not syncing" and the privacy note carries the
  cause and the remedy; `describeSyncError()` maps Firestore codes to plain English. Every
  catch site feeds it — the debounced push, `startSync()`, and the `onSnapshot` **error
  callback** (a listener that errors is dropped by Firestore and never fires again, so
  without that second argument another device's updates just stop arriving). A successful
  `pushNow()` is the only thing that clears it, which is why there's deliberately no retry
  button: transient causes are retried by the SDK, permanent ones (oversized doc, rules)
  aren't fixed by pressing anything, and the next save recovers the state on its own. The
  toast fires on the *transition* only, never per retry. Sizing context: 6 teams × 1 year
  with notes ≈ 133 KB against Firestore's 1 MiB, so the cap is ~8 years away — the
  visibility is the point, not a size guard.
- Firebase authorized domain is `eagleadams86.github.io`, so sync works at this
  `/sprint-velocity/` path unchanged.
- **Paste from Jira:** `parseJiraSprintReport()` / `deriveFromJira()` are pure functions on
  text — no DOM, no network, nothing saved (the saving happens in `applyJiraNumbers()`, further
  down). They only ever produce the seven figures, so the
  lifecycle and blank-vs-zero rules apply unchanged. Committed = every issue **not** marked
  `*` (removed ones included — they were in the sprint at start); carried out = the whole
  not-completed section, which can exceed `committed − completed`. Handles both tab-separated
  and one-cell-per-line pastes; browsers differ — decided on a **count** of rows of each
  shape, not on whether a bare issue key appears anywhere, since one stray key used to flip
  a tabbed report into the flattened branch and throw most of it away. `pointsFromCells()`
  takes the rightmost cell holding a real figure rather than the last cell outright, so a
  trailing `-` can't zero a row; a genuinely unestimated issue still reads 0. **Estimates can be a range** — Jira writes a
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
- **"Use these numbers" saves the sprint**, it doesn't just fill the boxes — losing a whole
  Jira paste by closing the form was the easier mistake to make. `buildSprintRecord()` reads
  the form and `commitSprint()` writes it; both are shared with Save sprint so the two paths
  can't drift, and neither toasts, closes or re-renders — the caller does that.
- **That auto-save is revertible, and the revert is the load-bearing half.** `pendingJiraSave`
  snapshots the record that was there (deep copy), plus `activePiId`/`activeSprintNum`, taken
  **before** the write and **only on the first press** — a second "Use these numbers" must not
  snapshot the copy the first one saved.
- **Only the Cancel button reverts.** Escape and a backdrop click close the dialog and keep the
  save — they're the two exits you hit by accident, and the point of saving at "Use these
  numbers" is that closing the form can't cost you the paste, so undoing takes the deliberate
  button. Save sprint keeps it too, and Delete clears the snapshot rather than fighting it.
  Nothing clears the snapshot on the keep paths: `openSprint()` resets it, so it can't outlive
  its sprint.
- **Don't move that revert onto the dialog's `close` event.** It's the obvious hook for "the
  user backed out" and it was written that way first: the event is dispatched as a queued task
  and never fired at all under Electron, so the undo silently didn't happen — strictly worse
  than not offering one. It would also be wrong now, since `close` can't tell Cancel from the
  two exits that are supposed to keep the save.
- The undo has to be **visible**: `setCancelLabel()` switches the button to "Cancel & Undo
  Save" while a snapshot is held. It can't live in the toast — `toast()` is `textContent`-only
  and `pointer-events: none`, so it can't hold a control.
- `confirmOverwrite()` guards a finished sprint from an accidental save, listing the
  field-level changes rather than asking a vague "are you sure?" — a warning nobody reads is
  worse than none. It deliberately stays silent for running/planned/new sprints, for a no-op
  save, and for notes-only edits; keep that narrow, or it becomes noise people click through.
  **It fires at "Use these numbers", not only at Save sprint**, and that placement is
  load-bearing: once the auto-save has replaced the stored record, the save-time check compares
  that record against itself, finds nothing changed and stays silent. Declining it fills the
  boxes without saving — the pre-auto-save behaviour, and the toast says so.
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
- Write commit subject lines in plain English a non-developer can read. **They are now
  user-facing**: the "Recent changes" box at the foot of the page fetches the last 10
  commits touching `index.html` from the GitHub API and lists the subject lines verbatim,
  each linking to its commit. Write them for a reader, not for a diff.
- The changelog fetches **on first expand, not on load**, so it costs nothing for the
  common case, and it only renders an `<a>` when the API's `html_url` is a real
  `https://github.com/` link (a `<span>` otherwise) — the same guard the lottery calculator
  uses, so a hostile URL from the API can't become a `javascript:` href.
