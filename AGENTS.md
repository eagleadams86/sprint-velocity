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
  Stripes are the series colour at *full strength* over the tinted fill (see the bar-drawing
  bullet below), never a second colour — the stripe is where a textured bar's 3:1 non-text
  contrast now lives. They used to be the colour pushed further from the card because the fill
  was the flat colour; the fill is the thing that moves now, so don't reinstate the push.
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
  and commitment-completion tile; the PI "Average per sprint" tile and every Rolling 5 figure
  are `avg()`. Don't "fix" one to agree with the other, and don't let a new figure pick a
  method silently — say which it is in the UI.
- **Both comparison tables end in an `All teams` row, each in its own table's method**
  (`allMean` on `avg()`, `allPooled` on `pooled()`), taken across every counted sprint from
  every team — **never** the mean of the rows above, so neither equals the mean of its own
  column and a six-sprint team pulls six times as hard as a one-sprint team. The lone plain
  sum is Comparison 1's next-sprint target: points, not a rate, so the column adds up. The
  `methodnote` under Comparison 2 explains both rows; keep it in step if either changes.
- **Current PI and Rolling 5 carry ONE summary row each, in the method that view's own
  figures already use** (asked for 2026-08-18): Current PI keeps **PI total** (pooled, matching
  its headline commitment-completion tile), Rolling 5 keeps **Average per sprint** (matching
  every tile on the view). They used to show both methods as a pair of rows so the gap between
  them read as a difference in method rather than an error; with one row that job falls to its
  `helpBtn`, which must still name its method outright AND say where the other one lives —
  don't let either help drift into describing a row that isn't there, which is what the
  removed `piAvgRow`/`rollPooledRow` entries did before they were deleted. **All teams still
  shows both methods side by side** (Comparison 1 and 2), which is where to send anyone who
  wants to compare them. Rolling 5 also keeps its **tiles on `avg()` only** — a fuller pooled
  treatment there (extra tile cards, a worked-example note) was built and rejected as too
  much for the view, so don't rebuild it.
- **The `REASONS` labels are short because they are `<option>` text on a phone.** A 375px
  screen leaves about 210px inside the control; the first draft ran to 267px ("Training,
  conference or company event"), so the longest reasons were cut off in the CLOSED select —
  the one place the chosen reason has to be readable. Widening the field fixed the desktop
  and could not fix the phone, so the labels themselves had to fit; `#adjustDialog
  .grid-fields` also gives the reason the room the percentage box doesn't need. They double
  as the tail of a sentence ("S1 left out (a major incident)"), so keep any new one a phrase,
  not a clause, and re-measure against ~210px.
- **The three working dialogs — sprint form, Teams & PIs, Adjust Capacity — are all 1100px**,
  Money Map's Preferences width. Back up, Delete and the help sheet stay narrow: they are a few
  lines each, and Money Map keeps its short ones narrow for the same reason. Share and the sync
  chooser are still on the 880px base — widen them only if asked.
- **A `.grid-fields` control is capped at 260px, and that cap is what makes a wide dialog
  survivable.** `auto-fit` hands a short row all the width there is: at 1100px the three
  Commitment fields took 336px each for a two-digit number, and the lone reason picker in
  Rolling 5 came out **1032px** wide. The track still stretches so the labels stay spread; only
  the box stops. Verified to cost nothing at 343/700/1100px — the cap only bites on the short
  rows it exists for.
- **`#adjustDialog` is 1100px — Money Map's Preferences width (`--dialog-w-wide` there), asked
  for 2026-08-18 so the two apps' two-up dialogs match.** Its panels sit SIDE BY SIDE above
  1140px (`.adjustcols`), and that breakpoint is chosen so each column lands at ~520px, wide
  enough for the availability `.grid-fields` to keep its own two columns with the Why picker
  (which holds sentences) uncut. Don't lower it: at a ~340px column the picker clips, which is
  the bug the widened column existed to fix. Below it the sections stack at full width. Three
  regimes to check when touching this dialog — side-by-side ≥1140px, stacked in between, and
  single-column fields on a phone. **Both panels are `<fieldset>` + `<legend>`, and that is what makes
  them line up**: a legend sits on the box's top border and pushes its contents down, so the
  left panel as a plain `.formpanel` started half a line higher than the fieldset beside it.
  Equal heights come from the grid's default `align-items: stretch` — don't reinstate
  `align-items: start`. Two side-by-side panels in this app should be the same element.
- **A shared text class must not be scoped to where it happens to be used first.**
  `.sub` had its size and colour on `.card > .sub` — a DIRECT card child — so all 21 `.sub`
  paragraphs inside the seven dialogs matched nothing and rendered at the body's 15px at
  full text brightness: bigger and louder than the identical class on the page behind.
  Reported as "the text in this pop-up is much larger than the rest of the app". The size
  and colour now live on plain `.sub`; only the MARGIN stays card-scoped, because dialogs
  set their own spacing inline and hoisting it would move every one of them. Check a new
  shared class renders the same in a card, a dialog and a table before shipping it.
- **`.badge`'s `margin-left: 6px` is for a badge that FOLLOWS text, and `.badge:first-child`
  zeroes it.** Four of the six badge sites sit after something — a sprint name in a table row,
  a card heading — and want the gap. The two "left out" notes on Rolling 5 and All teams open
  their own line, where the same 6px pushed the pill out of line with the heading and
  sub-heading stacked directly above it: the one element on the card meant to catch the eye
  was the only thing not aligned. Same trap as the `.tile-help` spacing rule below — a margin
  written for one position is wrong in the other.
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
- **An ART is a grouping of teams and nothing else.** `state.arts` is a flat list beside
  `teams` and `pis`, a team carries an optional `artId`, and **no figure anywhere is worked
  out per ART** — an ART's numbers are simply what its teams' numbers come to under the two
  methods the All teams view already applies, so `metrics()` and `rag()` never learn the
  concept exists. `teamsInArt()` and `groupTeamsByArt()` are pure (they take the team list
  rather than reading state) and pinned in tests.html; `groupTeamsByArt()` is a **stable**
  sort, so grouping never reshuffles teams inside a train. Assignment is a `<select>` in the
  team's own row of Teams & PIs rather than a team-picker inside each ART: it reads the way
  the data does, and it can't put a team on two trains. The header team picker groups with
  plain `<optgroup>` once an ART exists.
- **The All teams view filters once, at the top.** `renderTeamsView()` derives `shown` from
  `state.settings.artFilter` before anything else, and both tables, both footer rows, the
  chart and the in-flight count all come off that one list — so no corner of the page can
  still be counting teams the picker left out. Its exclusions are never silent, the same
  rule as every other view: `artToolbar()` says how many teams are hidden, and the footer
  row says which scope it covers ("All teams on Payments ART") rather than a flat "All
  teams" that would read as the whole portfolio in a screenshot.
- **`ART_NONE` is `~none`, deliberately not a legal id.** `~` fails `ID_OK`, so no ART
  arriving in a share link or a hand-edited file can collide with the sentinel — which is
  why `sanitizeIds()` has to *skip* it when cleaning `settings.artFilter`. Clean it and the
  "teams on no ART" filter becomes a fresh uid matching nothing.
- **A team whose ART is missing is un-grouped, never dropped** — unlike an orphaned sprint
  on the same boundary. An ART changes no figure, so a broken label must not cost a team its
  sprints; it reads as "No ART" on screen, which is where it can be seen and fixed. Same for
  a saved filter naming an ART that's gone, and same for Delete ART, which is the one delete
  in Teams & PIs with no confirm because it destroys nothing.
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
- **Availability scales the OUTPUT and never the method.** The window still averages
  committed points completed; `baseRecommended` is that mean and `recommended` is it times
  the percentage. Two levers, deliberately not one: a `plans` entry is a one-off against a
  slot, `team.availability` is the standing figure for a lasting change like someone joining
  or leaving. **The slot entry wins outright — they never multiply.** 80% of 90% is not a
  figure anyone can hold in their head at planning, and the card has to be able to say
  plainly which one is in force. Don't model headcount, working days or per-person
  availability: that is people data on a shared origin, it breaks the numbers-and-dates rule
  below, and points-per-head is a bad model anyway. One dimensionless figure is the whole
  design.
- **`capacityScale` re-weights ONE sprint's result inside `nextSprintTarget()` and is read
  nowhere else** — not `metrics()`, not a chart, not a table, and deliberately not the
  Dashboard-reconciliation condition (`dashCond`), because the pooled comparisons read
  `metrics()` and genuinely don't move. `planningBase` is the mean of the scaled results and
  is what availability multiplies; `baseRecommended` stays the raw mean. Scale corrects the
  INPUT history, availability scales the OUTPUT sprint — different dimensions, so unlike the
  two availability homes they DO compose by multiplication. It is **the one stored sprint
  field with no input on the sprint form** (it belongs to capacity planning, edited from
  Adjust Capacity), so `commitSprint()` preserves an existing numeric scale when the incoming
  record lacks one — remove that and every Save sprint or Jira re-paste silently strips it.
  Absent means 100: set back to 100 the key is DELETED, never written as 100 or undefined.
  Its badge is **⚖, deliberately not a third meaning for ⚑** (the All teams target ⚑ covers
  both levers, with sr-only text saying which); a scale on an excluded sprint is inert and
  the card must not claim it (`scales` is built from the window, which is what makes that
  true). A scale needs no expiry — it retires when its sprint leaves the window.
- **Everything on the capacity card that describes the PAST reads `baseRecommended`.**
  "They finished an average of X", `overCommitting`, the average-velocity comparison —
  those are facts about the history and the adjusted figure states them wrongly. Only the
  recommendation, `newWork` and `overBy` move with availability, and `spread`/`steady` stay
  on the base too or a team knocked down for leave reads as erratic for no reason. This was
  a real bug in the first cut: the card said the team "finished an average of 19.2" when the
  sprints said 24.
- **Carry-over does not shrink with the team.** `carryoverFills` exists because work already
  carried in comes off the top of a smaller sprint, so a big adjustment can leave no room for
  new work at all. It's the most actionable thing the feature surfaces — keep it visible.
- **`plans` is the second collection with orphan handling**, and it follows `sprints`
  exactly: id remapping first, orphan drop after (never before), the count joining
  `sanitizeIds.dropped` so `orphanNote()` reports both together. It also **de-duplicates by
  slot** — a second entry for one slot is invisible on screen and would outlive "Remove
  adjustment", which reads as the button not working. Delete Team and Delete PI filter it
  alongside `state.sprints`.
- **A sprint is excluded from the forecast with `excluded`, not by faking its status.**
  Setting a finished sprint to `planned` was the only way to do this before and it
  misrepresents the sprint in every other view; `updateStatusHint()` now points at the real
  control. The filter lives in `rollingSprints()` beside the IP-sprint rule so all three
  callers agree. **The never-silent rule applies to the user's own exclusions most of all,
  and it means every page the sprint appears on, not one of them**: the first cut only put a
  clause on the end of the Rolling 5 subtitle — fifth in a run-on line, after the sprint
  span, the IP note and the still-running note — and Charles's verdict was that it wasn't
  clear anywhere. A rule technically satisfied and never read is not satisfied. The five
  sites are the Sprint view (its own banner via `excludedWhy()`, plus `excludedBadge()` on
  the heading), the sprint picker (`sprintPickerNote()`), the Current PI row and caption,
  the Rolling 5 heading (`excludedLine()`) and its numbers-table caption, and both All teams
  comparison tables (`excludedTag()`) plus `excludedTeamsLine()` above the chart drawn from
  those same windows. **Say what it does NOT touch too** — the PI totals still count an
  excluded sprint, and a reader who sees a ⚑ will otherwise assume they don't.
  **`excludedInRange()` is `counted.slice(-ROLLING_WINDOW).filter(excluded)` — the window as
  it WOULD have been with nothing excluded — and it must stay that shape.** It first anchored
  on the oldest *kept* sprint and looked forward from there, which by construction made the
  oldest sprint the one it could never name: exclude the first of four and the window went
  from four sprints to three with nothing on Rolling 5 or All teams to say so, while Sprint
  and Current PI (which read `s.excluded` per sprint) were fine. Both window-based views read
  this one function, so both went silent together — if a report says "it shows in some views
  and not others", this is the seam. Pinned by the oldest-sprint test in tests.html.
  **The Agile Operations Dashboard reconciliation claim is now CONDITIONAL wherever an
  exclusion can reach it.** A sprint left out here is still in the Dashboard's total until it
  is unselected there too, so "matches the Agile Operations Dashboard" becomes "…when S1 is
  unselected there too" — the tag on Comparison 2 (which gains `.tag.cond` so a sentence can
  wrap where a two-word label never had to), its `.sub`, the `methodnote`, and the
  `teamsPooled` / `rollPooledRow` help. **The PI view's claims stay unconditional and must**:
  it filters on its own `closed` list rather than through `rollingSprints()`, so it never
  loses a sprint this way. That asymmetry is pinned by a test — if the PI view ever starts
  reading the window, `piTotalRow` and `piCommitCompletion` become wrong too.
  **Never call the window "the average" in an exclusion label — name it "the rolling N".**
  The badge first read "⚑ Left out of the average", which on the Current PI table sits two
  rows above a summary line literally called **Average per sprint** that counts the sprint in
  full. Charles's reaction was "is it left out or not on the PI tab?" — the badge and the
  table it was in read as a flat contradiction. "The rolling N" is the app's own name for the
  window (the tab is Rolling 5, the in-flight banner already used it) and can't collide with
  a PI average; the sprint form's fieldset is named the same, so the pointer and the control
  match. Where a correction is needed it goes INSIDE the sentence making the claim ("finished
  sprints only — S1 included"), never as a second sentence after the full stop; trailing
  corrections arrive after the reader has already believed the badge.
  **⚑ now means two things in the All teams table** — sprints left out on the Sprints
  column, capacity adjusted on the Next sprint target column — so the caption spells out
  which is which; don't add a third use without doing the same. `excluded` and
  `excludeReason` are written by `buildSprintRecord()`, not merely read by `openSprint()`:
  that function rebuilds the whole record, so a field without a form input is dropped on the
  next edit (the `addedThenRemoved` lesson).
- **A card heading that shares its line with a control needs `.row.cardhead`.** `.card > h2`
  stops matching once the heading sits inside a flex row, and it silently falls back to the
  browser's default h2 — half again the size of every other heading on the page. The class
  restores the treatment and carries the 4px the heading's own margin contributed.
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
  set in `renderTabs()` beside `aria-selected`, and arrow/Home/End wired at the foot of the
  file, skipping hidden tabs. `role="tabpanel"` sits on the inner `#views` div, **not on
  `<main>`** — putting it on the element replaces its role, which silently cost the page its
  main landmark once already.
- **`renderTabs()` is the one place that decides which views are on offer**, and it hides a
  tab only when the view behind it has nothing to say: **All teams** needs a second team,
  **Current PI** and **Rolling 5** need at least one recorded sprint *for the active team*
  (so they come and go as you switch teams), and with no teams at all the whole row goes
  rather than leaving a lone Sprint tab over the welcome card. If the stored view's tab has
  just been hidden it falls back to `sprint`, corrected **in memory** — a render must never
  `save()`, which would push to the cloud. **A shared view keeps its own rule for All
  teams** (`shareMeta.allTeams`, which the sender opts into and which already requires two
  teams): that check moved out of `openSharedView()` into `renderTabs()`, so don't
  reinstate it there.
- **The sprint button is `.primary` only while it says "Add Sprint".** On an empty slot it's
  the one thing to do on the page, so it matches "Add your first team" and "Add a PI"; once
  the sprint exists it says "Edit Sprint" and drops back to a plain `.btn`, because it is
  then toolbar chrome beside the pickers and the inverted fill made it the loudest thing on
  a page full of figures. Don't make both states match.
- **Every bar is a tint fill plus a full-strength edge, not a slab of its colour** — the same
  rule as the RAG surfaces above, extended to the categorical series bars. This is now a
  cross-app convention (rule 3 in `~/claude-theme-pack/CLAUDE.md`, also in the lottery
  portfolio); it adds no tokens, so it's a drawing rule rather than a palette one. `tintOf()` mixes the
  series colour toward `--surface` (the *card*, not white, which is what makes one constant work
  in all four themes: on the dark themes the fill goes quiet and the outline is the bright
  thing), and `seriesBar()` is the one place that pairs that fill with `borderColor` +
  `borderWidth: 2` + `borderSkipped: false` — never set `backgroundColor: seriesFill(…)` on a
  dataset by hand, or the bar keeps the tint and loses the edge that carries its contrast.
  This is what fixed "the charts are dark compared to the rest of the sepia/light theme": the
  3:1 non-text rule forces every series colour dark on a pale card, so three or four bars read
  as slabs of near-black. Two tint strengths, both deliberate: `BAR_TINT` (.68) for a textured
  series, whose stripes put full-strength colour back over about a third of the bar, and
  `BAR_TINT_SOLID` (.45) for committed, which has only its outline and washed out to invisible
  on the white Light card at .68. Lines are untouched — a 2px line is not a large flat area, so
  it keeps the full-strength colour.
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
- **Shapes from outside are not trusted either.** `coerceShape()` runs in front of
  `sanitizeIds()` at every entry point, forcing `teams`/`arts`/`pis`/`sprints` to arrays of
  objects and `settings` to an object — without it, `Object.assign(blankState(), parsed)`
  copies `teams: "junk"` or a null entry straight into state and the next render throws on
  a blank page. Order matters at the two rejecting callers: the import and `decodeShare()`
  shape-check the RAW parse first and coerce second, or coercion would turn any JSON into
  a valid empty export. Pinned in tests.html.
- **Ids from outside are not trusted.** `sanitizeIds()` runs on everything entering through
  `load()`, `decodeShare()`, the JSON import and `svAdopt()`, replacing any id that isn't
  `[A-Za-z0-9_-]{1,64}` with a fresh one and rewriting every reference through the same map.
  Names were always escaped; ids go into attributes (`data-id`, `<option value>`) in a dozen
  places and weren't, so a crafted share link could run script — which `viewOnly` does
  nothing about, since injected code doesn't go through `save()`. Render sites escape too.
  Don't add a render site that interpolates an id raw, and don't drop the boundary check.
- **`sanitizeIds()` must never invent a key, and `cleanKey()` is why.** `x.id = clean(x.id)`
  on an **absent** key looks harmless and isn't: `clean()` returns what it was given, and
  the assignment creates the key holding `undefined`. `JSON.stringify` drops that, so
  localStorage and every export look perfect — but `setDoc()` walks the *live* object and
  Firestore rejects the whole document over one `undefined`, with `invalid-argument`. That
  is what shipping `settings.artFilter` did on 2026-08-12: every browser holding a copy
  saved before ARTs existed stopped syncing until something happened to set the field, and
  the local copy gave no sign of it. Add an optional field and it goes through `cleanKey()`
  too. Pinned in tests.html by *key*, not by value — `x === undefined` passes either way.
- **`pushNow()` sends the state through JSON, exactly as `save()` writes it locally**
  (`forCloud()`), so the two copies are the same bytes by construction rather than nearly
  so. Don't "simplify" it back to passing `state` straight to `setDoc()`: that asymmetry —
  localStorage silently dropping what Firestore refuses outright — is the whole mechanism
  of the bug above.
- **`invalid-argument` does not mean "too big".** Firestore reports both an oversized
  document and an unstorable value under that one code, and `describeSyncError()` used to
  assume the first, so an app bug told the user to export a backup and **delete a PI**.
  The size wording now appears only when Firestore's own message mentions size; anything
  else says the fault is in the app and asks for nothing to be deleted. A remedy that
  destroys data must never be the guess.
- **The same boundary drops orphans.** After the remapping (never before it — a remapped
  sprint isn't an orphan), a sprint whose `teamId` or `piId` names nothing in the same
  payload is removed, and the count left on `sanitizeIds.dropped`. Nothing threw without
  this: `teamSprints()`/`rollingSprints()` counted the orphan into the Rolling 5 average
  while every PI-based view couldn't show it, its PI never reaching the picker — a figure
  moving with no visible sprint behind it. Delete PI / Delete Team filter `state.sprints`
  correctly, so this only arrives from a hand-edited or damaged payload. All four callers
  **say so** (`orphanNote()`), per the never-silent-exclusion rule: the import names it in
  its confirm, before the user commits; the share view and `svAdopt()` toast after
  `render()`; `load()` hands the count to `bootOrphans` because a toast raised during parse
  is gone before there's anything to look at.
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
  of numbers-and-dates sprints is well under 100 KB against Firestore's 1 MiB, so the cap
  is decades away — the visibility is the point, not a size guard.
- Firebase authorized domain is `eagleadams86.github.io`, so sync works at this
  `/sprint-velocity/` path unchanged.
- **Sign-in goes through Google Identity Services, not Firebase's popup** — the flow proven
  in Team Dashboard, because corporate filters block individual `firebaseapp.com` hostnames
  unpredictably (per hostname, not the domain — a sibling working proves nothing). A popup
  straight to accounts.google.com returns an OAuth token, exchanged for the same Firebase
  session via `signInWithCredential`. `GOOGLE_CLIENT_ID` (top of the sync module) is this
  project's OAuth web client — it is NOT part of `FIREBASE_CONFIG`, and the client's
  Authorized JavaScript origins must list the serving origin (port included) or Google
  refuses with origin_mismatch. The CSP carries accounts.google.com in
  script-src/connect-src/frame-src; the old popup fallback and its firebaseapp.com
  frame-src / apis.google.com entries were retired 2026-08-07 once the client ID landed.
  Auth is built with `initializeAuth`, **not `getAuth`** — `getAuth()` always wires in
  `browserPopupRedirectResolver`, which Safari/iOS/mobile initialise at startup, pulling in
  apis.google.com/js/api.js for the popup-redirect gapi iframe nothing here reads (it showed
  up only as a CSP console error). Don't go back to `getAuth()` to "fix" a popup/redirect
  call — pass the resolver to that call instead. Same change in Team Dashboard.
- **The Rolling 5 velocity chart carries a dashed `linearTrend()` line** (ordinary least
  squares, ported from Team Dashboard; nulls skipped). It's drawn muted — a reading of the
  bars, not a new series — and `linearTrend()` is a pure function pinned by tests.html.
- **The chrome is shared with Team Dashboard** (the `claude-team-dashboard` repo; the app
  itself is titled **Flow Metrics** on screen — display-only rename, every identifier still
  says team-dashboard) — sticky header, brand mark, button tabs, tiles, ⓘ help,
  footer, changelog box. The two apps are meant to read as one family; if a chrome rule
  changes here, change it there too (and vice versa). **Each app's header carries an
  `.applink` to the other** — a plain `<a class="btn small applink">`, no script, mirrored
  in Team Dashboard — sitting with the title rather than in the control cluster: it is
  navigation, not another thing to do to the data, and it stays visible in a shared view.
  `.applink` (not `.brand`, whose margin is now plain `0`) carries the `margin-right: auto`
  that pushes the controls right, and needs `display: inline-flex` because `.btn.small`
  pins its height with `min-height`, which an inline box ignores. The footer keeps its
  cross-link too.
- **Each app wears its own mark in the header, from the same family tile** — midnight page,
  soft disc in the corner, one gradient stroke in the accent, the same shapes Money Map and
  PAPTrack use. Here it's the sprint cycle; Flow Metrics has three weeks of bars. It is
  drawn twice, by `make_favicon.py` (Pillow → `favicon.ico`) and as the inline SVG data URI
  in `<head>`, and the two must stay the same picture — the SVG is what a browser actually
  shows, the `.ico` is the fallback it fetches from the site root on its own and what the
  header `<img>` wears. Re-running the script means bumping `?v=` on **every**
  `favicon.ico` reference, `privacy.html` included, or the old icon stays cached for months.
  The two extra tints (`#a5b4fc`, `#141c33`) are artwork, not palette: they came from Money
  Map's icon and are copied byte-for-byte rather than re-picked, so nothing new enters the
  theme pack. `.brand img` sits in the text's own flow with `vertical-align: middle` —
  **don't make `.brand` a flex row** the way Money Map does. This brand line wraps on a
  phone, and as flex items the title and the "· Charlie's Epic…" span become two columns,
  so the subtitle wraps inside a narrow one beside the title instead of running on below it.
- **Only numbers and dates are ever saved — there is deliberately NO free-text field in the
  data (2026-08-12).** The figures come out of Charles's work Jira, and the copy in GitHub-
  hosted localStorage and Google's Firestore has to stay clean of anything sensitive, so the
  old per-sprint `notes` object (four "Why?" textareas) was **removed on purpose — don't add
  a comment/notes field back**. `sanitizeIds()` enforces this as a **whitelist, not a
  blocklist** (added 2026-08-13): `keepKnown()` rebuilds every team/ART/PI/sprint/settings
  object from only the keys the app knows, pins each value to its type (numbers must be
  finite numbers, dates must match `YYYY-MM-DD` or become `''`, status must be one of the
  four, names capped at 120), and drops stray top-level keys too — except the share-meta
  keys (`v`/`sharedAt`/`label`/`allTeams`/`range`), which the shared-view banner needs and
  which never persist because `save()` is a no-op there. `notes` is still counted separately
  in `sanitizeIds.strippedNotes` (it gets the boot toast — a person's own writing went
  away); everything else lands in `sanitizeIds.pruned` (a silent boot `save()`, so the scrub
  reaches localStorage immediately and the cloud on the next sync). Rebuilt objects only
  ever gain keys that are present and valid, so the boundary can never create a key holding
  `undefined` — the Firestore rule below. **A new stored field must be added to the
  `keepKnown` spec or it will be silently stripped** — that's the point, and the same-named
  test in tests.html pins it. The only free-text left is the short team/ART/PI names. The
  sprint form's one disclosure is `#jiraBlock`, closed on every `openSprint()`.
  **The capacity levers' reason codes are a fixed enum (`REASONS`) and must never become a
  text box.** "Why did we drop that sprint?" is the obvious place for someone to reach for
  free text later, and it is exactly where a ticket key or a colleague's name would ride into
  the cloud. The `'reason'` kind in `keepKnown()` pins the value to the list and an unknown
  code becomes `'other'`; labels render from the map, never from the stored value. The
  `'pct'` kind clamps 0–200 rather than merely checking finiteness, because the figure
  MULTIPLIES the recommendation and an unbounded one would put nonsense on the planning card. Sibling
  rule in Flow Metrics: `cleanWorkType()` + `normalizeSettings`' whitelist.
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
- **Every dialog sets `overscroll-behavior: contain`, and it is not cosmetic.** A scroll
  container that has run out of scroll hands the rest of the gesture to its parent, so
  reaching the foot of a dialog carried straight on into the page behind it — the app
  scrolling away under a dialog still open and still covering it. Reported on a phone in
  Money Map, where a dialog nearly always scrolls and the gesture is a flick that doesn't
  stop at the boundary; all four apps shared the default. `contain`, never `none`: the
  dialog's own scrolling is untouched, only the hand-off is. **A new scrollable region
  that sits OVER the page needs the same.** Verifying it needs a REAL device — the desktop
  preview pane's synthetic scrolls aren't hit-tested to the element under the cursor, so
  the page moves and the dialog doesn't, which looks like the bug whether or not it is
  there. Reproduced and confirmed fixed in iOS Safari on the simulator.
- **The toast is a POPOVER (`popover="manual"`), and that is the only way it can be seen
  while a dialog is open.** A modal `<dialog>` sits in the browser's TOP LAYER, which paints
  above every z-index in the ordinary document, so a toast fired from an open dialog was
  drawn under it AND under its backdrop — invisible, indistinguishable from a button that
  does nothing. It was reported that way in Money Map, about the share dialog's "Copy link",
  which is the case that has to work: copying deliberately leaves the dialog open, so the
  toast is the only thing that says it happened. **Anything else that has to appear over a
  dialog needs the same treatment** — a bigger z-index cannot reach the top layer. Four
  things `toast()` keeps doing: it raises the popover BEFORE writing the text (a popover is
  `display:none` until shown, and a live region announces a change it was present for); it
  reads a layout property in between, or the `display` flip means the `opacity:0` state is
  never painted and the fade is skipped; it drops out of the top layer 250ms after fading,
  so a spent toast is never parked above whatever opens next; and it is `manual`, so nothing
  else can dismiss it and Escape still belongs to the dialog underneath. The CSS undoes the
  UA's own `[popover]` rules (`inset: 0`, `margin: auto`, a border and a background). On a
  browser with no popover support the attribute is inert and the toast is exactly the fixed
  element it always was. Mirrored in Flow Metrics, Golf Handicap and Money Map — all four
  shared this chrome and all four had the bug.
- `confirmOverwrite()` guards a finished sprint from an accidental save, listing the
  field-level changes rather than asking a vague "are you sure?" — a warning nobody reads is
  worse than none. It deliberately stays silent for running/planned/new sprints, for a no-op
  save; keep that narrow, or it becomes noise people click through.
  **It fires at "Use these numbers", not only at Save sprint**, and that placement is
  load-bearing: once the auto-save has replaced the stored record, the save-time check compares
  that record against itself, finds nothing changed and stays silent. Declining it fills the
  boxes without saving — the pre-auto-save behaviour, and the toast says so.
- **Read-only share links** put the data in the URL fragment (`#share=<marker>.<base64url>`,
  marker 1 = `deflate-raw`, 0 = plain JSON for browsers without `CompressionStream`). Nothing
  after `#` is sent to a server, which is the whole reason this needs no Firestore rules, no
  account and no network. `buildSharePayload()` emits a **trimmed copy** — chosen teams only,
  only the PIs their sprints reference, and never anything
  identifying. Don't shortcut it to serialising `state`. It carries **only the ARTs the
  included teams are on** (the same rule as `usedPis`) and deliberately **not** the sender's
  `artFilter`: the link already holds exactly the teams they picked, and opening it
  pre-filtered would hide some of them behind a picker the recipient has no reason to open.
- **How much history a link carries is the second lever, beside teams.**
  `trimShareSprints()` applies it and is **pure** (it takes the PI list rather than reading
  state) so tests.html can pin it; `parseShareScope()` turns the picker value into its scope.
  Sprint windows are **per team** — a two-team link must not spend its whole window on the
  busier team — and PI windows are **global**, because a PI is a program increment the teams
  share and cutting it per team would leave the comparison views on different quarters. It
  runs **before `usedPis`** in `buildSharePayload()`, or a link cut back to this PI still
  carries the names of the PIs it no longer reaches. Unlike `rollingSprints()` it applies
  neither `isCounted()` nor the IP-sprint rule: a link carries what was recorded, and the
  recipient's own views count or exclude it by the usual rules.
- **The window's exclusions are never silent, on both sides.** A team the window leaves empty
  is dropped from the payload (never *all* of them — `decodeShare()` refuses a teamless
  payload) and named in the dialog, because shipping it lands the recipient on an empty sprint
  card. Cutting a team below `ROLLING_WINDOW` warns too: that changes the *figures* the
  recipient sees, not just the length of the link. The recipient's banner says a window is in
  force, built by `shareRangeNote()` from `range: { kind, n }` — **two numbers, never a
  sentence the sender wrote**, so a hand-edited link has no text to inject — and deliberately
  without a total, so the sender isn't publishing how much history exists behind it.
- **"As much as fits" bisects, and must keep checking `shareSeq` between trials.** Link length
  only grows with the window, so `fitShareWindow()` binary-searches it in about six encodes
  instead of fifty. It searches sprints, not PIs: a PI step is six sprints and overshoots by
  thousands of characters. With several encodes in flight, checking the sequence only at the
  end would let a stale search finish over a fresh one.
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
- **`privacy.html` is the privacy policy** (static page, midnight theme, linked from the app
  footer via `.privacy-links` — deliberately a separate element from `#privacyNote`, whose
  textContent the sync code rewrites). Other SMs sign in with their own Google accounts, so
  it exists for them: what Firestore holds, that rules confine each account to its own data,
  that share links upload nothing, and the deletion contact. If sync, share links, or what
  the app stores ever changes, update it and its effective date in the same commit.
- **README.md is the index** — keep it current whenever the app meaningfully changes.
- After changes: **browser-test locally first** (`python3 -m http.server 8012`, or the
  desktop app's preview pane via `.claude/launch.json`), then commit, push, verify the
  Pages deploy, and spot-check live. Any local server + browser works — don't hunt for a
  specific tool.
- **`tests.html` pins the pure functions — open it (same local server) and check "All N
  tests pass" whenever you touch the Jira parser, `metrics()`/`rag()`/`fmtPct()`,
  `avg()`/`pooled()`, `sanitizeIds()` or `sprintStatus()`.** It loads the real
  `index.html` in a hidden iframe and calls the functions directly — no build step, no
  copies — so it needs `http://localhost` (file:// iframes are blocked in some
  browsers). **It also refuses to run anywhere else, and that is load-bearing:** Pages
  publishes `tests.html` beside the app, where the iframe would be the signed-in copy and
  `onAuthStateChanged` would start a real sync — or raise the which-copy dialog — inside an
  invisible frame. Two guards, both needed: the iframe carries `data-sv-tests`, which the
  sync module checks before `init()`, and the gate at the foot of `tests.html` never creates
  the iframe at all off localhost (booting the app IS the side effect, so the check can't
  live in the load handler). Don't put the iframe back in the markup. CI runs the same page
  **`file://` is deliberately NOT in `LOCAL_HOSTS`**: it has no hostname, and `''` used to sit in that list on the reasoning that the suite couldn't run there anyway — but that sent it down the iframe branch, where the frame silently fails to load and the suite blamed the app. Opening the file off disk now gets the advice that fixes it, and a frame that never loaded the app is reported as a setup problem rather than as every test failing at once.
  headless on every push (`.github/workflows/tests.yml`) on `localhost:8012`, so the gate
  lets it through, and fails the build if the summary goes red. `window.__svTestHooks` at the foot of the classic script exists solely to
  hand it `fmtPct` (a `const`, invisible on `window`); function declarations it reaches
  directly. When a rule in this file changes, change the matching test in the same
  commit.
- Write commit subject lines in plain English a non-developer can read. **They are now
  user-facing**: the "Recent changes" box at the foot of the page fetches the last 10
  commits touching `index.html` from the GitHub API and lists the subject lines verbatim,
  each linking to its commit. Write them for a reader, not for a diff.
- The changelog fetches **on first expand, not on load**, so it costs nothing for the
  common case, and it only renders an `<a>` when the API's `html_url` is a real
  `https://github.com/` link (a `<span>` otherwise) — the same guard the lottery calculator
  uses, so a hostile URL from the API can't become a `javascript:` href.
