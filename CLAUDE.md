# Sprint Velocity

A sprint predictability tracker for Scrum Masters — commitment completion, break-in,
carryover and velocity across multiple teams. Deployed via GitHub Pages:
https://eagleadams86.github.io/sprint-velocity/

Charles uses this as a Scrum Master across several teams, and shares the **URL** with
fellow SMs — each person's data stays in their own browser. There is deliberately no
shared-workspace/multi-SM-editing model. (It used to say "each person signs in with their
own Google account"; sync was removed on 2026-08-20, and the Auth list confirmed nobody
but Charles had ever actually signed in.)

- **⌕ Find / ⌘K is Money Map's window, ported (2026-08-23)** — `searchApp(st, query)` is PURE over the state it is handed and does NOT use the `teamById`/`piById`/`artById` helpers, which are bound to the live `state`; a search over a test fixture has to be a search over that fixture, and the sprint label is rebuilt from the lists in hand for the same reason. Two-character minimum, `SEARCH_CAP` of 80 with the overflow COUNTED so the cap is never silent, and the count span (`role="status"`) is the live region rather than the results list. `goToSearchHit` sets what the hit points at and then lets `renderTabs()` have the last word on the view — a PI hit asking for Team PI on a team with nothing in that PI falls back to Sprint by itself, so there is no second copy of the tab rules. `SEARCH_VIEW_LABEL` must name every `.tab[data-view]` and nothing else; a test asserts both directions. Mirrored into Flow Metrics and Golf Handicap in the same pass — a change to one belongs in all three — and the Task Dashboard has one too, which makes six windows in five apps plus the starter.
- **THE WINDOW ITSELF IS PINNED, PROPERTY BY PROPERTY, AND THE SAME BLOCK IS IN ALL SIX APPS VERBATIM (2026-08-23).** 700px on 18px of padding — the Back Up & Restore window's size, the family's other fixed-width window — with the heading, the intro line, the box, the hit and its three lines, and the "Nothing matches" line all declared inside the `#searchDialog` block rather than borrowed from whatever quiet-text class the app happens to have. That borrowing is what made one window into six: 360px and 420px wide, a 320px box inside a 360px dialog, a hittab at `--fs-sm` here and `--fs-xs` there, `.04em` typed out beside `--ls-label`, and four different colours on the same sentence. A change to any of it belongs in all six. Two details worth keeping: `#searchDialog > p` is the DIRECT child only (the results list's message is a `<p>` too, and an id in that selector would out-rank `.searchresults .hint` and hand it the intro line's colour), and the block deliberately declares NO dialog chrome — backdrop, shadow, a field's touch-height floor, and the max-height Money Map divides by its own zoom all belong to the app's `dialog` rule and are shared with every other window it opens.
- **The header buttons wear a glyph in front of the word** (2026-08-21) — plain text characters, NOT emoji and not an icon font: one more file to fetch is the last thing a header painted this early needs, and a text glyph inherits the theme's colour for free, so it can never become the thing that carries a meaning by hue. Each is `aria-hidden` — the word beside it is already the whole label. The glyphs are Money Map's own where the same button exists there (`⇩` Back up, `↗` Share, `⚙` settings), so one action looks the same in every app, and `☰` is the list/manage one the three list-managing apps share. Added to Sprint Predictability, Flow Metrics, Golf Handicap and PAPTrack in the same commit.
- The app is **one file — `index.html`** (no build step), alongside `theme.css` and a
  vendored `chart.min.js`. Keep it that way: no npm, no bundler, no CDN calls.
- **The print stylesheet takes furniture OFF; it never re-lays-out** (2026-08-22). A print
  design that rearranges anything is a second design to keep in step with the first, and it
  always falls behind — so `@media print` hides controls (`.tabs`, the header's buttons and
  selects, `[data-export]`, `.tile-help`, `.toolbarcard`, dialogs, the toast), flattens
  `.rowbtn` to plain text (hiding it would empty every table's first column) and does nothing
  else to the layout. **`printForPaper()` swaps `data-theme` to `light` for the length of the
  job and re-renders**, which is how these rules own not one colour of their own: they borrow
  the pack's Light palette rather than becoming a print palette that would need keeping in
  step with `tokens.json`. The re-render is not optional — the charts are CANVASES painted
  from `cssVar()` reads at draw time, so swapping the tokens under them would print a Midnight
  chart on a white page. Two listeners (`beforeprint`, and a `print` media-query change for
  the WebKit paths that don't fire it) because neither covers every browser; the swap is
  idempotent and `_was` is captured only on the way in, so both firing costs nothing and
  cannot lose the theme the reader chose. `print-color-adjust: exact` is then asked for BY
  NAME on the elements whose background carries meaning — tiles, pills, badges, chart boxes —
  rather than with `*`: browsers drop background colour to save ink, which is right for
  decoration and wrong for the RAG tints and the shaded threshold bands. It still reads
  without any of them, because every figure carries its ✓ / ! / ✕ — and
  `html, body { background: #fff }` is the floor for a browser that fires neither signal, so
  the worst case is a themed page rather than a full-bleed Midnight one. `#printMeta` is
  written on every render rather than from the print hook (one fewer thing to be wrong:
  whatever is on screen is what comes out) and is the only print-ONLY content on the page. **The scope controls can be
  hidden because every caption already spells out what they did** — "with sprint 6 excluded",
  "includes S3, still running", which ART, which sprints are left out. If a new control ever
  changes a figure WITHOUT the page saying so in prose, that rule breaks and the control has
  to stay on paper.
- `theme.css` is a **copy of the generated file from `~/claude-theme-pack`** (private
  repo eagleadams86/claude-theme-pack), the source of truth for the palette of ALL apps —
  don't diverge it; palette changes go through the pack's `tokens.json` + contrast gate.
  App-specific tokens (chart series colours, threshold-band tints) live in the `<style>`
  block at the top of `index.html` instead. **Those sit OUTSIDE the pack's
  `check_contrast.py` gate, and that is the trade this arrangement makes** (recorded
  2026-08-20, after an audit asked why 24 colour values — six series across four themes —
  were defined outside the source of truth). Chart series aren't pack tokens; the pack has
  no concept of "this app's six series", so gating them would mean teaching it a per-app
  section. What that costs: nothing re-checks them when the palette moves. All six were
  verified by hand at that audit — they clear AA and they avoid the red-green axis (slate,
  blue, teal, amber, violet, rose). **Re-check them by hand whenever the pack's surface
  tokens change**, and keep `SERIES_TEXTURE`, which is what actually tells them apart.
  Golf Handicap carries the same note for its two. The four themes (Midnight is the base palette; **`auto` is the default** since 2026-08-22, and follows the reader's system) are surfaced
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
  options and `hidden` on the team picker. The header paints well before the script at the
  foot of the page runs, so anything filled in by JS grows on screen: empty selects went
  40px → 120px. The worst case was the sign-in button, which appeared only once the Firebase
  SDK had come over the network and re-wrapped the row onto a second line, shoving the whole
  page down 42px; that button went with sync on 2026-08-20, and the rule it taught stays.
  Starting hidden costs nothing; growing does. If you add header chrome, give it its final
  width in the HTML.
- `chart.min.js` is a **vendored third-party build — do not hand-edit.**
- **`package.json` exists ONLY so Dependabot has a manifest to scan** (added 2026-08-22).
  Not a package, not a build step, nothing is ever installed from it — CI passes `--omit=dev`
  precisely so npm does not download the library this repo already vendors. This repo was the
  **fourth** carrier of the identical Chart.js 4.4.1 bytes and the only one with no manifest,
  so a Chart.js advisory reached lottery, team-dashboard and financial-plan and reached
  nothing here — in one of the two apps holding figures copied out of a work Jira. Dependabot
  cannot re-vendor a file, so a version-bump PR would raise the manifest while the app went on
  serving the old bytes; a test pins the manifest against the vendored file, which makes a
  manifest-only bump FAIL and turns the PR into the right instruction: update the file too, in
  all four repos that carry it (lottery, team-dashboard, financial-plan, sprint-velocity). A
  second test pins `--omit=dev` in the workflow, because dropping it would quietly start
  downloading the vendored library on every run and nothing else would notice.
- **`metrics()` and `rag()` in `index.html` are the only places the numbers are
  calculated.** Every tile, table and chart reads from them. Thresholds change in one spot.
- **The eight RAG boundaries are SETTINGS, not constants** (2026-08-22). `TARGET_DEFAULTS`
  holds the shipped eight; `tgt()` merges `state.settings.targets` over them and is called at
  the moment a figure is judged — **never snapshotted into a const**, which is the whole point:
  a ⓘ opened after a target changed has to read the new one, so the three `TARGET_*` help
  sentences became FUNCTIONS and `openHelp()` calls `h.target` if it is callable. Anything new
  that states a threshold in words, a caption, an `aria-label` or a chart band reads `tgt()`
  too — grep for `tgt()` before writing a number. `TARGET_FIELDS` owns the per-field range and
  is what both the dialog and the boundary validate against, so a new target means one entry
  there and nothing else. **Only the difference from the default is stored**, so a browser
  that never opened the dialog and one reset with *Back to the defaults* hold the same thing
  and a later change to a default reaches both. `targetProblems()` refuses a self-contradicting
  set (green under its own red, a band ceiling under its floor) — those are shape rules, not
  taste: rag() would otherwise have a branch nothing can reach. Targets **travel in a share
  link** (numbers only) because a figure the sender flagged amber arriving green is worse than
  not sharing, and the ⚙ button is hidden in a shared view — not because it would write, but
  because it would RE-JUDGE somebody else's figures.
- **Two averaging methods, both deliberate.** `avg()` is the mean of each sprint's own
  percentage (every sprint equal); `pooled()` sums the points and divides once (bigger sprints
  weigh more). The Compare Teams view shows both — Comparison 1 uses `avg()`, Comparison 2 uses
  `pooled()` — over the *same* sprint set, so they can only ever differ by method. **Comparison
  2 is the method the Agile Operations Dashboard uses**, as is the PI view's "PI total" row
  and commitment-completion tile; the PI "Average per sprint" tile and every Rolling 5 figure
  are `avg()`. Don't "fix" one to agree with the other, and don't let a new figure pick a
  method silently — say which it is in the UI.
- **Both comparison tables end in an `Compare Teams` row, each in its own table's method**
  (`allMean` on `avg()`, `allPooled` on `pooled()`), taken across every counted sprint from
  every team — **never** the mean of the rows above, so neither equals the mean of its own
  column and a six-sprint team pulls six times as hard as a one-sprint team. The lone plain
  sum is Comparison 1's next-sprint target: points, not a rate, so the column adds up. The
  `methodnote` under Comparison 2 explains both rows; keep it in step if either changes.
- **Team PI and Rolling 5 carry ONE summary row each, in the method that view's own
  figures already use** (asked for 2026-08-18): Team PI keeps **PI total** (pooled, matching
  its headline commitment-completion tile), Rolling 5 keeps **Average per sprint** (matching
  every tile on the view). They used to show both methods as a pair of rows so the gap between
  them read as a difference in method rather than an error; with one row that job falls to its
  `helpBtn`, which must still name its method outright AND say where the other one lives —
  don't let either help drift into describing a row that isn't there, which is what the
  removed `piAvgRow`/`rollPooledRow` entries did before they were deleted. **Compare Teams still
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
  Money Map's Preferences width. Back up and Delete stay narrow: they are a few lines each, and
  Money Map keeps its short ones narrow for the same reason. **The help window is no longer a
  width at all** — since 2026-08-23 its own text sizes it (see the info-dot block above). Share is still
  on the 880px base — widen it only if asked. (The sync chooser shared that base until sync
  was removed.)
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
  a card heading — and want the gap. The two "left out" notes on Rolling 5 and Compare Teams open
  their own line, where the same 6px pushed the pill out of line with the heading and
  sub-heading stacked directly above it: the one element on the card meant to catch the eye
  was the only thing not aligned. Same trap as the `.tile-help` spacing rule below — a margin
  written for one position is wrong in the other.
- **A WINDOW IS NAMED FOR THE HEADING IT SITS BESIDE, IN TITLE CASE** (2026-08-27, from a
  sweep of all 129 help windows in the family after Money Map's due block was split). Two
  things changed here and both were this app alone.
  - **Titles are Title Case now** — 37 of the 45 were sentence case ("Commitment
    completion", "PI predictability", "Done so far"), against Title Case in every other
    app and in every other heading in this one. `#helpTitle` is a heading; the standing
    rule covers it. **A tile LABEL is not a heading and is untouched** — it renders
    uppercase from `.tile .label`'s `text-transform` anyway, so the two never had to
    match character for character, which is why this could drift unnoticed.
    `PI`/`ART`/`BV` are preserved; small words stay lowercase mid-title ("Average per
    Sprint", "Teams in the Band"). "Done So Far" is capitalised because *so far* is an
    adverbial phrase, not a preposition — the one the mechanical pass got wrong.
  - **Three windows were opening from two headings each**, which is the other half of the
    one-dot rule. On PI by Team, "ART predictability" and "Teams in the band" both opened
    a window titled for the first; a "Commitment completion" tile opened one titled "ART
    total", which names the row at the foot of the table and not the tile beside the
    reader. Both tiles have their own entry now (`artInBand`, `artCommitCompletion`), each
    cross-referring to the other method rather than restating it. On PI Trend, two tiles
    inside a card headed **What the Next PI Could Hold** both opened a window of exactly
    that name — so the dot moved onto the card heading and off both tiles, which is the
    hoist Money Map's `monthRows` already made: an explanation that answers for the CARD
    is drawn once, on the card.
  - **A blanket source sweep is NOT how this is tested, and that is deliberate.** A
    `tile(...)` scan cannot tell one view from another, nor two mutually exclusive
    branches of one view apart — `renderSprintView` names `breakIn` and `removed` twice
    each, in its in-progress branch and its finished branch, and only ever draws one. It
    went in as a sweep first and reported exactly those. The three fixes are pinned
    individually instead; the general form needs the DOM with data on all seven views.
- **THE INFO DOT AND THE HELP WINDOW ARE FAMILY-WIDE BLOCKS, DECLARED PROPERTY BY PROPERTY,
  AND THE SAME IN EVERY APP THAT HAS ONE (2026-08-23).** A change to either belongs in all of
  them.
  - The dot (`helpBtn` → `.tile-help`) is a 16px outlined circled **"i"**: `margin-left: 7px`
    (zeroed inside `.tile .label`, a flex row that already pins it right — that one line is
    app-specific and stays outside the block), `min-height: 0` for the sibling whose bare
    `<button>` rule puts a 38.5px floor under everything, and a 24px tap target from an
    unpainted `::after` so a tile row never gets taller. `td:has(.tile-help)` is `nowrap` so a
    wrapping label can't orphan the circle onto a line of its own. Icons must never sit flush
    against the word — a standing preference of Charles's across all his projects. Golf
    Handicap and the NY calculator drew a "?" in a filled 18px pill until this date; "i" won
    because "?" is what a browser already puts on its own help cursor and in a form's
    validation bubble, and it asks a question where this thing answers one.
  - **The hover fills with `--surface-alt`, which is Flow Metrics' and not this app's old
    `--bg-card`,** and specifically not Money Map's `--focus-border`: a hover that borrows the
    focus colour says "focused" to anybody reading the two states side by side.
  - The window is sized by its TEXT — `#helpBody` capped at a 66-character measure,
    `#helpDialog` at `width: fit-content` — so it takes the measure as its width. **This app's
    half of the drift was that measure**: it capped the WINDOW at `46ch`, resolved against the
    dialog's own 16px, so about 50 characters of 15px text, while Money Map read to 66 and
    Flow Metrics to about 80. Most entries now open at 666px with 624px of text, the family
    figure. `piDelivered` opens at 565px and that is the rule working, not a bug: it is one
    77-character sentence, and a window sized to its text is smaller when there is less of it.
  - **`#helpTarget` takes the same 66ch, and is deliberately outside the shared block.** The
    target line under the definition is a second paragraph no sibling has, and without a cap a
    long one would set the window's width instead of the definition it belongs to.
  - **The type, the colour and the padding are in the block too** (2026-08-23, a second pass
    after Charles spotted differences between the windows). `#helpTitle` at `--fs-md`/600,
    `#helpBody` at `--text-secondary`, paragraph margins at 10px, `#helpBody strong` lifted
    to `--text-primary`, and `padding: 20px` on the window itself. Nothing here moved — this
    app was already on all of it — but the rules are declared rather than inherited, because
    inheritance is exactly what let the seven windows drift apart: an unset heading weight
    defaulted to bold on two pages, an unset paragraph colour came out `--text-primary` on
    one, and the dialog padding differed by app.
  - **A NOTE OVER ~380 CHARACTERS IS PARAGRAPHS, AND IT BOLDS THE CLAIM IT TURNS ON**
    (2026-08-23). All 45 entries were a single paragraph before that and nine ran past 400
    characters, which is a wall of text on a phone. The threshold is length rather than
    taste: under about 380 a note is two or three sentences and breaking it up is its own
    kind of unreadable, so **35 of the 45 are deliberately left whole** and `tests.html`
    only holds the long ones to the rule. **`<em>` is a separate channel and is left
    alone** — it marks a contrastive word inside a sentence (`<em>after</em> the sprint
    started`), where bold marks the claim. At most one bold run per paragraph, pinned.
    Money Map and Flow Metrics reached the same place by a different route: their bodies
    are arrays of paragraphs built with `createElement`, because those two write help with
    `textContent` and never markup. This app's bodies have always been template literals
    with `<em>` in them, so `<p>` and `<strong>` are simply the next tags along.
  - `tests.html` pins all of it, and scans only the dots written out as literals — about a
    third of them; the rest come from a tile spec as `helpBtn(helpKey, label)`. What covers
    those is the guard that `helpBtn` returns `''` for a key with no entry, so a wrong key
    draws no dot rather than a dot onto an empty window.
- **Blank means 0.** `val()` saves 0 for an empty box and `metrics()` uses `num()` throughout.
  Blanks were once kept as `null` so a half-typed sprint couldn't read as real results; the
  sprint lifecycle now does that job, data mostly arrives via the Jira paste where absent
  really is zero, and a `—` where the answer is 0 looked like missing data.
- **`goalMet` is the app's ONE tri-state field, and absent is a real answer.** true, false,
  or the key not there because nobody recorded a goal. **This is deliberately not the
  blank-means-zero rule above** — a blank points box really is zero points, but an unanswered
  goal is not a missed goal, and treating it as one invents a failure for every sprint
  recorded before the field existed, which is all of them. It therefore needs its own
  `keepKnown` kind: `'tribool'` keeps a value only when `typeof v === 'boolean'`, where
  `'bool'` would coerce a `null` into `false` and silently record a missed goal. The form
  writes it in `buildSprintRecord()` **after** the object literal, so "not recorded" is the
  key's ABSENCE — never `null`, never `undefined` (which `JSON.stringify` drops silently, so
  the key would read as "never set" rather than announcing itself).
  Same shape as `capacityScale`, which deletes rather than storing its no-op. `confirmOverwrite`
  compares it separately, because `OVERWRITE_FIELDS` goes through `num()` and would read both
  `false` and absent as 0.
- **Every goal figure counts over the sprints that ANSWERED, and hands back what it left
  out.** `goalRecord()` returns `recorded` and `missing` beside `met` for exactly that reason:
  "3 of 4" printed beside a chart of five sprints is the silent exclusion this app refuses
  everywhere else, so the tile's foot names the ones with no goal. `pct` is null when nothing
  is recorded, the same rule as every other percentage.
- **The Rolling 5 tile is a COUNT, not a percentage** — "3 of 4" is what somebody says at a
  retro, and over four or five sprints a percentage rounds to figures like 67% that imply a
  precision four answers don't have. On the Team PI table the goal is a **badge on the
  row**, not a tenth column: that table already scrolls sideways on a phone, and six rows is
  countable by eye. The Sprint view shows a tile only when there IS an answer — an unanswered
  question is not a metric, the same rule the PI predictability tile follows.
- **`goalGapKind()` is the finding the field exists for, and neither number can make it alone.**
  A team hitting its commitment while missing what the sprints were FOR is planning the wrong
  work, and every points figure on the page keeps reading green while that is true; the
  reverse is worth saying too and is the kinder half. It needs two answered sprints and fires
  only on a clear disagreement (points green + goals under half, or points red + goals all
  met), so an ordinary mixed record stays quiet. **Prose and a glyph, never a colour** — the
  finding is precisely that the colour-coded tiles beside it answer a different question, so
  painting it would be its own contradiction. Same rule as the headroom and cancelling notes.
  It was an IIFE inside the Rolling 5 view until 2026-08-22, when **Compare Teams** gained a
  Sprint goals column and needed the same finding: one function now, because two copies of a
  rule this particular drift the first time either is tuned. Note it reads `rag()`, so it
  follows the targets — "the points land" is a target judgement, not a fixed 85%.
- **Compare Teams shows a DIRECTION as well as a level** (2026-08-22). Every figure on that page
  is an average, and a team climbing 60→85 prints the same number as one sliding 95→85 —
  opposite findings, one cell. `trendCell()` draws `sparkline()` plus the change in words, off
  the same `linearTrend()` fit the Rolling 5 chart uses, so one bad sprint at an end cannot
  flip it; `MIN_TREND_POINTS` is 3 because two points are a slope. Three things about it are
  load-bearing: the sparkline is **colourless** (the pill beside it already carries the RAG,
  and two colour languages in adjacent cells teach a reader to trust neither), the direction
  is a **word** (so nothing is lost without colour vision), and that word is **visible text**
  — `cellText()` strips `aria-hidden`, so the SVG and the arrow leave the CSV and "up 12" is
  all that lands in the file. Words rather than "+12" because `csvCell()` has to defuse a cell
  opening with `+`. No trend on the footer row: a line through every team's sprints pooled is
  a shape with no team behind it.
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
- **A PI IS OPTIONAL, AND `piId: null` IS A REAL ANSWER (2026-08-20).** A team's sprints
  live on one of two tracks: the **unassigned track** (`piId: null`), which is the app's
  pre-history, or a PI's. The unassigned track sorts before every PI, is numbered
  continuously, and the IP-sprint rule does not exist on it. Everything else follows from
  that one sentence. `piRank()` states the ordering rather than leaning on `piIndex()`
  returning `-1` — that `-1` was an accident that happened to be right, and the next person
  to "fix" `findIndex` would take the rule with it. `piKey()` collapses `''`, `undefined`
  and `null` to one comparable value, because a `<select>`'s none-option hands back `''`
  while the store holds `null`: without it `findSprint` misses its own sprint and the save
  path writes a duplicate instead of editing the one in front of you. Four don'ts:
  - **Don't clamp `sprints.sprintNumber`.** It is typed `'num'`, which looks like an
    oversight and is now load-bearing: clamping to `SPRINTS_PER_PI` would rewrite every
    unassigned sprint past 6 onto slot 6 and collide them all. `sprintNum` is bounded by
    `MAX_SPRINT_NO` (999) instead — six-to-a-PI is a property of a PI, enforced by the
    picker, not by the boundary.
  - **Don't measure across the two tracks.** `slotIndex()` puts unassigned slots in a band
    (`PI_LESS_BAND`) far below PI 0 so an unassigned S47 can never land on a real PI slot;
    a *difference* across the bands is meaningless, not merely large, so `teamCadence()`
    refuses the stride (falling back to the week-snapped length) and `cadenceDates()`
    returns null. `sameBand()` is the guard.
  - **Don't make `objectives` PI-optional.** PI business value is defined per team **per
    PI**; there is no such thing as unassigned business value, and `piId` there stays `'id'`.
  - **Don't aim a new slot at unassigned S1.** `piId: null` used to mean "we can't say
    where the next sprint goes" — which is what `targetSprintSlot()` returned when a team
    ran off the end of its last PI with no next one created. It now names a REAL track, and
    slot 1 out there is usually the oldest sprint the team has, so the capacity card aimed
    at it: `availabilityFor()` handed next sprint the availability recorded against a
    sprint from before the first PI, and Adjust Capacity would have written a second plan
    onto the same slot. `nextUnassignedSlot()` is the one answer — one past the highest
    number already out there — and all three callers read it: the sprint-number picker
    ("the next one"), `unassignPiSprints()` (appending a deleted PI's sprints) and
    `targetSprintSlot()`. Found and fixed 2026-08-21; pinned in tests.html.
  - **Don't reinstate the PI-orphan drop.** See the next bullet.
- **A sprint whose PI is missing is UN-GROUPED, not dropped — and that reverses an older
  rule in this file.** The drop was right while a PI was compulsory: an orphan moved a
  rolling average with nothing on screen behind it, because no PI-based view could show it.
  That justification is gone — an unassigned sprint is now an ordinary, visible sprint — so
  a broken PI reference costs the grouping and nothing else, exactly as a missing ART costs
  a team its grouping and nothing else. **A missing TEAM is still fatal** and still feeds
  `sanitizeIds.dropped` + `orphanNote()`: there is no view a team-less sprint appears on.
  The un-grouping gets its own counter (`sanitizeIds.unassigned`) and its own sentence
  (`unassignedNote()`) — counted into `pruned` as well so boot persists the repair, but
  reported out loud, because a sprint losing its PI is a change to what is on screen. That
  is the `strippedNotes` shape, not the silent `objectives` one.
- **The IP-sprint rule applies inside a PI and nowhere else**, through one predicate,
  `isIpSlot(s)` — the `isCounted()` discipline, so no two callers can disagree. Sprint 6 of
  a team with no PI is an ordinary sprint; dropping it from the window because of its number
  would be the worst kind of exclusion, and the toggle that would put it back is a sentence
  about a PI that team hasn't got. So `rollingToolbar()` takes an `ipApplies` flag and hides
  the toggle entirely where it means nothing, and the Rolling 5 heading stops claiming
  "sprint 6 (IP) excluded" over a table that plainly lists S6.
- **PI-scoped views leave out teams with nothing in the selected PI, and name them.** With a
  PI compulsory every team was in one, so `renderArtPiView()` mapping every shown team was
  safe; now a PI-less team would appear as a row of zeros, which reads as a team that
  delivered nothing rather than one that isn't in this PI. `renderTabs()` hides **Current
  PI** without a PI (and for a team with no PI'd sprint) as well as **PI by Team**.
- **Deleting a PI asks whether to keep its sprints, and the renumbering is not optional.**
  It used to destroy every sprint in the PI across every team, which was the only coherent
  answer while a sprint needed one. `unassignPiSprints()` appends them past the team's
  current highest unassigned number — a PI's S1–S6 landing on an existing unassigned S1–S6
  would put two sprints in one slot and make `findSprint` non-deterministic. Business value
  and capacity plans die either way (both are defined by the PI) and the dialog says so.
  It also **discloses the one place the ordering rule bites backwards**: kept sprints move
  *before* any remaining PIs, because unassigned is the oldest track.
- **The demo's Team No PI exists to show the app working with no PI, and carries nothing
  else.** Sprints 12–16 — continuous, past six, and a 16th that could not exist in a
  six-slot PI. No ART, no scale, no exclusion, no dates, no goals, no business value: every
  one of those findings already belongs to another team, and a second owner would blur which
  team teaches what.

- **An ART is a grouping of teams, and ONE figure's worth of maths.** `state.arts` is a flat
  list beside `teams` and `pis`, and a team carries an optional `artId`. **No POINTS figure
  is ever worked out per ART** — an ART's points are simply what its teams' points come to
  under the two methods the Compare Teams view already applies, so `metrics()` never learns the
  concept exists. The single exception, added with the PI by Team view, is
  `artPredictability()`: SAFe defines the predictability measure at train level, so there is
  nowhere else it could live. It reads `state.objectives`, not `metrics()`, and it does not
  touch a points figure — keep that line where it is. This rule used to read "a label, not a
  level of maths"; if a second per-ART calculation is ever proposed, that is the moment to
  ask whether it is really defined at train level or just convenient there. `teamsInArt()` and `groupTeamsByArt()` are pure (they take the team list
  rather than reading state) and pinned in tests.html; `groupTeamsByArt()` is a **stable**
  sort, so grouping never reshuffles teams inside a train. Assignment is a `<select>` in the
  team's own row of Teams & PIs rather than a team-picker inside each ART: it reads the way
  the data does, and it can't put a team on two trains. The header team picker groups with
  plain `<optgroup>` once an ART exists.
- **PI business value is `state.objectives` — one record per TEAM per PI, never per
  objective.** `{ id, teamId, piId, plannedBv, actualBv, stretchBv }`, a fifth collection
  beside `plans` and handled exactly like it: id remapping, orphan removal, dedupe by key,
  a `keepKnown` spec, delete-team/delete-PI cascades, and a place in the share payload.
  **Not one record per objective, and don't "improve" it into one** — an objective's
  identity is its title, a title is free text, and free text is the one thing this app
  refuses to store (the `REASONS` rule, one level up). Three numbers carry the whole measure
  and cannot carry a ticket key. There is no title field in `#bvDialog` and there must never
  be one.
- **Stretch value is in the NUMERATOR and never the DENOMINATOR** (`bvFigures()`).
  `plannedBv` is the committed objectives only; `delivered` is `actualBv + stretchBv`. Put
  stretch into the denominator and a team is penalised for planning stretch at all, which is
  the opposite of what stretch is for — and the measure loses the only honest way it can
  read above 100%. Same shape as commitment completion exceeding 100% on a re-sized sprint.
- **`rag(v, 'predictability')` is the app's only BAND, and both edges are findings.**
  `PRED_BAND_LOW`/`PRED_BAND_HIGH` (80–100) green, out to `PRED_UNDER_RED`/`PRED_OVER_RED`
  (70/120) amber, beyond them red. Over 100% is amber rather than red up to 120 because
  stretch objectives are *supposed* to land sometimes. Every other scale here is one-sided,
  so a reader arrives assuming higher is better and reads 130% as the best team on the
  train — which is why `TARGET_PREDICTABILITY` has to state both edges and say why the top
  one exists. **`RAG_TEXT` cannot carry this**: "Off target" is the same two words for 40%
  and 140%. `predictabilityStatus()` supplies the direction and `predPill()` is the only
  way a predictability figure should reach the page, so no site can render one without it.
  `pill()`'s third argument exists solely for this.
- **The ART and PI pickers share ONE card on the PI by Team view** (`artToolbar`'s `extra`
  argument). Both narrow the same page, so two stacked cards read as two unrelated settings
  and cost a card's height to say it. The PI picker is built **above** that view's early
  returns and passed to all three `artToolbar` calls, because both empty-state cards tell the
  reader to change a picker — an empty state that names a control and then withholds it is a
  dead end. `wireArtToolbar()` wires both controls for the same reason: three exit paths, one
  place to remember. The PI label stopped being `sr-only` when a second picker joined it —
  two adjacent selects have to be told apart on sight, not only by a screen reader.
- **`piTrend()` is the only PI-GRAINED view over time, and each PI is measured over the teams
  that were actually IN it.** That last clause is the whole design. A train that grew from two
  teams to five did not get better because there is more of it, so a PI's row carries its own
  `teamsIn` and the view says so when the count changes. It is also why the two methods split
  the way they do: **predictability is the MEAN of the teams' own measures** (every team once,
  so it survives a train changing size, and the same method `renderArtPiView`'s tile uses so
  the two views can't disagree about one PI), while **commitment completion is POOLED**
  (matching Team PI and the Dashboard) and openly does not survive it. A PI with nothing
  recorded is a GAP, not a zero — `any` is false and the view drops it rather than plotting a
  hole as a collapse; a PI with no business value leaves a hole in the predictability line for
  the same reason. **There is deliberately no total row**: adding PIs together answers
  nothing, a programme's history is a sequence, and the only summary worth having is the
  direction, which is what `linearTrend()` draws.
- **The trend tab needs TWO PIs**, because one point is a position rather than a direction and
  the chart would be a single dot. It is cross-team like PI by Team and Compare Teams, so it takes the
  same `shareMeta.allTeams` rule and joins the same right-hand tab group — the `margin-left:
  auto` now belongs to the FIRST VISIBLE of `trend`/`art`/`teams`, with each zeroing every
  later sibling, or two auto margins split the free space and break the group apart.
- **`piCapacityCard()` is the forward half of that view, and it multiplies rather than
  re-deriving.** Each team's `nextSprintTarget()` times the DELIVERY sprints in a PI
  (`SPRINTS_PER_PI - 1` — the IP sprint delivers none of it), so it inherits the whole method
  including both availability levers and cannot drift from the Rolling 5 card that explains
  the working. It covers only teams that have been in a PI, matching the table above it, and
  names any it left out — a team that doesn't run PIs has no place under a heading about the
  next PI, and its target is on Rolling 5 where it lives.
- **The demo carries THREE PIs so the trend has a direction** (≈75% → 81% → 86%, climbing out
  of the band into it). Two points are a line and say nothing about whether a train is
  steadying or drifting. The two earlier PIs cover two teams against 2026.3's five, which is
  also deliberate: it is what makes the "not the same train throughout" note fire, and it
  demonstrates the one thing the view has to get right. Don't tidy the three into agreement,
  and don't level them off.
- **`renderArtPiView()` is the RTE view, and it reads the PI, not the rolling window** —
  objectives are planned and scored per PI, so a five-sprint window crossing a PI boundary
  would answer a question nobody asked. It **shares `settings.artFilter` with Compare Teams**
  rather than keeping a second picker: two controls meaning the same thing and disagreeing
  is worse than either. Its tab takes Compare Teams' shared-view rule as well
  (`shareMeta.allTeams`) — it is a comparison ACROSS teams, so a sender who declined to
  publish one must not have it handed back through another tab.
- **The tile is `mean`, the footer row is `pooled`, and both say so.** Same deliberate pair
  as `avg()`/`pooled()`: SAFe defines the measure as the average of the teams' own, so that
  gets the tile; pooling answers the other question and gets the row. The `methodnote` under
  the table names both. Don't "fix" one to agree with the other.
- **The cancelling case is the reason that view carries prose.** A two-sided measure lets an
  under-delivering team and an under-committing team cancel out, so the train's average
  lands inside the band while neither team is in it — 59% and 113% average to 86%. The
  condition is the MECHANISM (mean is green, and at least one team on each side), not a
  proxy like "fewer than half in band": it cannot fire on a healthy train and cannot miss a
  cancelling one. Glyph and prose, **never a colour** — the finding is that the colour is
  misleading, so a second colour would be its own contradiction (same reasoning as the
  headroom note).
- **A team with no business value recorded is NAMED, and `hasBv()` is what makes that
  possible.** A record of three zeroes ("planned nothing") and no record at all ("nobody has
  filled this in") are different answers, so the empty record is deleted rather than stored
  and the ART view says which teams it left out of the predictability figures. It stays in
  every points figure. Same never-silent rule as `orphanNote()` and `excludedTeamsLine()`.
- **An orphaned objective is `pruned`, not `dropped`, and the distinction is the toast.** An
  orphaned sprint moves a rolling average with nothing on screen behind it, which is what
  `orphanNote()` exists to announce; business value is only ever read for a team and PI both
  on the page, so an orphan changes no figure and is inert bytes riding along in the saved
  copy. Plumbing gets a silent boot `save()`, not a sentence.
- **`adoptState()` stamps `version: SCHEMA`, and that is load-bearing.** Both paths that
  replace `state` from outside (boot's `load()` and Restore) go through it — there was a
  third, `svAdopt()`, until sync was removed — and
  each has already refused anything stamped newer. Letting the incoming `version` win instead
  means a browser that upgrades, opens a copy saved by the old build and saves it back writes
  the OLD number over data now holding new fields — and the next older build to read it sails
  straight past `haltForNewerData()` and strips them. Invisible while `SCHEMA` had never moved
  off 1; found the day it moved to 2. Pinned in tests.html.
- **PI Trend, PI by Team and Compare Teams are the CROSS-TEAM group and sit apart from the other
  three**, which look into the selected team. Only the first of the pair takes the
  `margin-left: auto` — two auto margins in a flex row split the free space and would put a
  gap between them as well — so the rule hands it to `[data-view="art"]:not([hidden])` and
  the sibling combinator zeroes Compare Teams' when PI by Team is on the page. Below 470px it is off
  entirely, and the pair falls onto the second row together, which is where it should be.
- **The Compare Teams view filters once, at the top.** `renderTeamsView()` derives `shown` from
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
- **A team whose ART is missing is un-grouped, never dropped** — and since 2026-08-20 a
  sprint whose PI is missing is treated the same way, so this is no longer the exception it
  was once described as. An ART changes no figure, so a broken label must not cost a team its
  sprints; it reads as "No ART" on screen, which is where it can be seen and fixed. Same for
  a saved filter naming an ART that's gone, and same for Delete ART, which is the one delete
  in Teams & PIs with no confirm because it destroys nothing.
- `rollingSprints()` is the chokepoint — filtering there covers Rolling 5, Compare Teams and the
  capacity target at once. The PI view filters separately via its own `closed` list.
- Exclusions must never be silent: every view that drops a sprint says which one and why
  (`openSprintsNote()`). A sprint sitting outside the numbers unnoticed is worse than the
  bug this replaced.
- `fmtPct()` takes the RAG scale and drops to one decimal when rounding would cross a
  threshold, so a displayed figure never contradicts the colour next to it (84.6% must not
  render as "85%" in yellow). Any new percentage display must pass its scale.
- Sprint 6 is the IP sprint **of a PI**: excluded from the rolling window by default, with a
  toggle — and only for sprints actually in a PI (`isIpSlot`).
- `nextSprintTarget()` recommends a commitment from **mean committed-points-completed**,
  deliberately *not* mean velocity — velocity includes break-in, so committing to it
  over-commits the team. Don't "improve" it into a velocity-based figure; the reasoning is
  in the comment above the function and in the card's "How this is worked out". **`forecast()`
  reads the same rate for the same reason** — the two must not drift apart.
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
  Its badge is **⚖, deliberately not a third meaning for ⚑** (the Compare Teams target ⚑ covers
  both levers, with sr-only text saying which); a scale on an excluded sprint is inert and
  the card must not claim it (`scales` is built from the window, which is what makes that
  true). A scale needs no expiry — it retires when its sprint leaves the window.
- **Everything on the capacity card that describes the PAST reads `baseRecommended`.**
  "They finished an average of X", `overCommitting`, the average-velocity comparison —
  those are facts about the history and the adjusted figure states them wrongly. Only the
  recommendation, `reliable`, `newWork` and `overBy` move with availability, and
  `spread`/`steady`/`low`/`high` stay on the base too or a team knocked down for leave reads
  as erratic for no reason. This was
  a real bug in the first cut: the card said the team "finished an average of 19.2" when the
  sprints said 24.
- **The card shows TWO commitment figures, and `recommended` is still the mean.** An average
  is met about half the time by definition, so one number gets read as a floor and half the
  team's sprints then miss a commitment that was never meant to be safe (5, 5, 5, 5, 40 has
  a mean of 12 and cleared it once). `reliableBase` is the **second-lowest** result — the
  largest commitment met in all but one sprint — and `reliable` is that times availability,
  exactly like `recommended`. **Deliberately not a percentile or a standard deviation**: over
  a `ROLLING_WINDOW` of five, a percentile is an interpolation between two of the same five
  numbers and an SD assumes a shape five points can't evidence, whereas "met in 4 of the
  last 5" is a counted fact the reader can check against the table below it. `reliableMet`
  and `meanMet` are **counted, not derived** — ties at the bottom really do mean all of them.
  This does NOT contradict the don't-fold-headroom-in rule one bullet up: that forbids
  raising the commitment on unplanned work, and this adds a FLOOR below it. Nothing here
  moves `recommended`.
- **`hasFloor` is what stops the pair reading as nonsense, and its subtraction is
  load-bearing.** It needs three sprints (dropping one of two leaves an anecdote) and a gap
  of at least a point (two tiles saying 23 and 23 teach nothing — a steady team getting one
  figure IS the message). It also silently covers the left-skewed case: 10, 30, 32 has a mean
  of 24 and a second-lowest of 30, so the "reliable" figure would sit ABOVE the
  recommendation. **Don't clamp the floor to the recommendation to "fix" that** — it would
  invent a figure none of the team's sprints support. There is no safer number to offer a
  team whose mean is already below what they usually do, and the swings caveat speaks instead.
- **The floor reads the SCALED results; `low`/`high`/`spread` stay raw.** It is a planning
  output, and scale is what corrects the history to today's team — same basis as
  `planningBase`. The raw range is a history sentence and must not move with next sprint's
  leave, which is the same rule the `spread`/`steady` bullet above already states. The
  fold-out quotes `planningBase` rather than "the figure above", because on an adjusted team
  the tile shows the adjusted number and the two would disagree.
- **The demo reaches the floor through Team Overcommitted (20 vs 17) and Team Baseline, and
  deliberately not through an ADJUSTED team.** Team Live Sprint is the only team with a standing
  availability and its three-sprint window puts the second-lowest exactly on the mean, so
  `hasFloor` is false there. Bending Team Live Sprint's figures to reach the adjusted
  foot-string would disturb the live sprint, its pace reading and its over-commitment finding
  — all pinned — to demonstrate a formatting branch the Recommended tile already demos on
  Team New Start ("50% of 13"). The adjusted floor is covered by a test instead. That was a
  decision, not an oversight.
- **`forecast()` runs the capacity numbers backwards, and uses the SAME rate — committed
  points finished, never velocity.** Velocity counts break-in, which by definition is not the
  piece of work being forecast, so forecasting at it assumes the whole sprint goes to this
  work while the interruptions keep arriving anyway. That is the same reasoning as
  `nextSprintTarget()`'s and it must not drift: a forecast at velocity is the identical
  mistake as committing to velocity, one step further out. It always returns a RANGE from
  `meanRate` and `floorRate`, and those two are kept apart **by what they are, not by which
  is bigger** — the card names each end ("the 20 they average", "the 17 they finished in 3 of
  the last 4"), those sentences are not interchangeable, and which is faster genuinely swaps
  for a left-skewed team (see `hasFloor`). `Math.ceil` on both ends: you do not finish in 4.4
  sprints.
- **A STANDING availability applies across the horizon; a ONE-OFF does not.** `team.availability`
  is a lasting change and holds for every sprint in the span; a `plans` entry is leave next
  fortnight, and stretching it over ten sprints would forecast a team as permanently
  short-staffed off one holiday. The card says which it did, either way — `lastingAdjustment`
  and `oneOffIgnored` exist so it can.
- **Delivery sprints are not calendar sprints, and the dates have to know it.** Unless the
  team counts it, sprint 6 delivers none of the work, so a span long enough to cross one
  takes an extra stride of calendar per crossing. `calendarSlots()` walks the slots from the
  one being planned rather than multiplying, because how many IP sprints land inside the
  horizon depends on where it starts.
- **`FORECAST_HORIZON` is two PIs, and past it the card keeps the count but drops the
  dates.** A rate from a five-sprint window cannot speak to the next hundred sprints, and a
  specific date four years out is a straight-faced absurdity. It also bounds the slot walk
  against a mistyped backlog, and suppresses the does-it-fit-this-PI clause, which is not a
  question anybody has about 5,000 sprints.
- **Every field on the forecast card is stored, the backlog total included** (2026-08-27; the
  rate, growth, lost sprints and fold since 2026-08-26). This line used to say the opposite and
  the argument was real — a backlog total goes stale the moment anyone grooms the backlog, so a
  stored one has the app forecasting from a figure nobody has checked since. It lost to the
  thing that actually happened: a reload kept every knob on the card and threw away only the
  number that made sense of them. `forecastPoints` lives in `state.settings` with its four
  siblings, on the same `keepKnown` whitelist and under the same **no schema bump** reasoning —
  an older build stripping it costs a restored total and nothing else, because the card asks
  again and the placeholder says what it is asking for. **A new field here must be added to that
  whitelist or it will be deliberately stripped on the way back in**, which is the general rule
  and the one this field was missing. Unchanged: **`wireForecast` re-renders THIS CARD'S result
  region only, never `render()`** — a full re-render rebuilds the input and takes the caret with
  it, so every keystroke would land in a fresh empty box. The `save()` beside that redraw is new.
- **Carry-over does not shrink with the team.** `carryoverFills` exists because work already
  carried in comes off the top of a smaller sprint, so a big adjustment can leave no room for
  new work at all. It's the most actionable thing the feature surfaces — keep it visible.
- **The headroom signal is PROSE, and must stay prose.** `hasHeadroom` fires when a clear
  majority of the window finished essentially the whole commitment (`CLEARED_PCT`) *and*
  completed extra work on top — the shape you get when work is pulled in late because the
  commitment is done, close to done or blocked. The recommendation can never exceed what the
  team committed to, so that spare capacity is structurally invisible to it. **Do not fold
  `headroomExtra` into `recommended`, and do not add a "stretch" tile.** The extra is
  unplanned break-in; adding it on is committing to velocity by another name, which is the
  one mistake this whole card exists to prevent.
- **THE SAMPLE DATA IS THE DEMO, and a feature isn't finished until it reaches it.**
  `loadSample()` is what a person sent a share link explores and what the app is shown
  with, so every feature must be visible from it. Adding one means adding the data that
  demonstrates it, a line in the roster comment above `loadSample()`, a row in the README's
  demo table, and a test in the sample-data group — that group exists precisely because
  these are ordinary-looking figures a later edit would tidy, and tidying them leaves a
  first run with nothing to look at. **Each demo team is NAMED FOR THE ONE THING IT SHOWS**
  — Team Baseline, Team Live Sprint, Team Overcommitted, Team Headroom, Team New Start, Team
  No PI — so the picker reads as a contents page and a reader who lands on a card already
  knows which finding they are looking at; a new demo team gets a name of the same kind, and
  renaming one back to a bird or a place would leave the demo teaching nothing until you had
  read every one of its numbers. Every number in there is load-bearing: Team Baseline's scale
  sits inside the rolling window (outside it a scale is inert), Team Overcommitted ends at S5
  so the next slot is the IP sprint, Team Headroom's S2 lands at 92% so the note reads "4 of
  the last 5", Team New Start's carryover exceeds its halved figure. **The business value is picked
  the same way**: one team inside the band, one under, one over (Team Headroom, whose objectives
  are under-committed just as its points are), one team unscored so the ⚑ note has something to
  name, and Platform ART arranged as the cancelling case so the "average is hiding this" note
  fires on a first run. A demo whose predictability figures are all healthy teaches a two-sided
  measure as a one-sided one. **The sprint goals are picked the same way and must not be tidied
  into agreement with the points**: Team Headroom reads best on every points figure and meets 2
  of 5 goals (the ◎ note), Team Overcommitted reads worst and meets all of them (the note
  reversed), Team Baseline is mixed with one sprint unrecorded (the only home for the "no goal
  recorded" caption), and Team Live Sprint and Team New Start record none so the tile can be
  absent. A demo where the goals always agree with the points teaches that they always do, and
  the field would have nothing to show for itself. Team Live Sprint is the ONLY dated team, and
  its dates are counted from `Date.now()` so the running sprint is still running whenever the
  demo is opened; everything else is dateless because a dateless sprint resolves complete.
  **The 2026-08-22 features were fitted to the same rule.** Team Baseline and Team Headroom
  each have nine sprints, which is what gives the demo two teams with a **History** tab — and
  both are arranged so the whole-history direction disagrees with the five-sprint one (up 11
  vs level; up 14 vs down 1), because that disagreement is the argument for the view and a
  demo where the two agree would teach that they always do. The **Trend** column needs all
  four of its answers present, and gets them: up, down, level, and Team New Start's two
  sprints reading `—`. Two of the seven can't be demonstrated with data — a changed
  **target** (so the welcome card names the ⚙ button instead) and the **importer** (whose
  own two buttons, *Download a template* and *Paste an example*, are its demo, and the
  template is generated from whichever team you are on so it round-trips through
  `parseImport()`; a test asserts that it does).
- **The headroom note is a `.badge` line, and its amber is NOT a RAG band.** It takes the
  same badge-led `.sub.exnote` shape as the "sprints left out" notes, for the same reason
  `excludedLine()` gives: it started life last on the card, after the fold-out and beside
  the caveats, which is where the eye stops. It now sits under the sub-heading, above the
  tiles. The amber is the ⚑ / ◐ amber — "there is something here to read", like an adjusted
  figure or a sprint in flight — so **never wire it to `rag()`**: the finding is neither
  good news nor bad, and the tiles beside it are where the colour-coded verdicts live. The
  ↗ carries the meaning without the colour, per the never-colour-alone rule.
- **`overCommitting` and `hasHeadroom` are computed in `nextSprintTarget`, not the card**,
  and headroom is suppressed when `overCommitting` is on. The card used to work the first one
  out again for its own prose; one home is what makes the two mutually exclusive by
  construction rather than by luck of the wording. Three sprints minimum, same reason `thin`
  exists — this one talks a team into signing up for more work.
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
  the heading), the sprint picker (`sprintPickerNote()`), the Team PI row and caption,
  the Rolling 5 heading (`excludedLine()`) and its numbers-table caption, and both Compare Teams
  comparison tables (`excludedTag()`) plus `excludedTeamsLine()` above the chart drawn from
  those same windows. **Say what it does NOT touch too** — the PI totals still count an
  excluded sprint, and a reader who sees a ⚑ will otherwise assume they don't.
  **`excludedInRange()` WALKS THE WINDOW BACKWARDS, the same walk `rollingSprints()` fills
  it with, and it must stay that shape.** Three versions, each naming a different subset:
  anchoring on the oldest *kept* sprint and looking forward made the oldest sprint the one it
  could never name — exclude the first of four and the window went from four sprints to three
  with nothing on Rolling 5 or Compare Teams to say so, while Sprint and Team PI (which read
  `s.excluded` per sprint) were fine. `counted.slice(-ROLLING_WINDOW).filter(excluded)` fixed
  that and still under-reported whenever the exclusions clustered: with sprints 1–7 and S1, S2
  and S3 all out, the window is four sprints and only S3 got named. Walking it is the only
  version that cannot drift from the window, because it *is* the window's own walk; it stops
  at `ROLLING_WINDOW` kept sprints or `ROLLING_WINDOW` skipped ones. Both window-based views
  read this one function, so both go silent together — if a report says "it shows in some
  views and not others", this is the seam. Pinned by the oldest-sprint test in tests.html.
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
  The badge first read "⚑ Left out of the average", which on the Team PI table sits two
  rows above a summary line literally called **Average per sprint** that counts the sprint in
  full. Charles's reaction was "is it left out or not on the PI tab?" — the badge and the
  table it was in read as a flat contradiction. "The rolling N" is the app's own name for the
  window (the tab is Rolling 5, the in-flight banner already used it) and can't collide with
  a PI average; the sprint form's fieldset is named the same, so the pointer and the control
  match. Where a correction is needed it goes INSIDE the sentence making the claim ("finished
  sprints only — S1 included"), never as a second sentence after the full stop; trailing
  corrections arrive after the reader has already believed the badge.
  **⚑ now means two things in the Compare Teams table** — sprints left out on the Sprints
  column, capacity adjusted on the Next sprint target column — so the caption spells out
  which is which; don't add a third use without doing the same. `excluded` and
  `excludeReason` are written by `buildSprintRecord()`, not merely read by `openSprint()`:
  that function rebuilds the whole record, so a field without a form input is dropped on the
  next edit (the `addedThenRemoved` lesson).
- **The CSV/Copy export reads the RENDERED TABLE, never state, and that is the design.**
  Every exportable table is already the product of filters the user chose — the ART picker,
  the two rolling toggles, which PI is selected, which sprints are excluded — so a second
  code path building "the same" rows from `state` would have to reproduce all of them and
  would drift from the screen the first time one changed. `tableToRows()` + `exportButtons()`
  + one delegated listener on `viewsEl` serve all five tables; adding a table means giving it
  an `id` and dropping `exportButtons()` into its `.row.cardhead`, nothing else.
- **`cellText()` strips `[aria-hidden="true"]` as the general rule**, with `.sr-only`,
  `.badge`, `.tile-help` and `.artname` as named cases. Anything hidden from assistive
  technology is DECORATION and decoration is not data — that one selector is what catches the
  bare ⚑/⚖ markers on the Compare Teams table, which are aria-hidden spans with an `.sr-only`
  sentence beside them rather than `.badge` elements, and which otherwise exported a sprint
  count of 4 as the text `4 ⚑` and cost the column its numbers.
- **`tests.html` carries a render SMOKE WALK, and it is not a substitute for the tests
  around it.** Everything else in that file calls a pure function or reads `index.html` as
  text, which left the render layer entirely unexecuted — measured on 2026-08-27, and the
  measurement is the point: `renderTeamsView` (24KB), `renderPiView`, `renderHistoryView`, `renderPiTrendView` and 111
  others sat at zero, and four of the seven tabs had never been drawn. A throw in any of them
  would have shipped green. The walk boots a SECOND, FULL-SIZE frame (the suite's own is
  1x1px, where a render draws into a box with no room and proves nothing), populates it,
  visits every view and opens every window, and fails if the frame throws OR if a panel
  comes back empty — the second half matters, because a render that threw half way leaves an
  element that is present and with nothing in it, which no "did it throw" check would notice.
  **It writes nothing**, and that is enforced rather than intended: `save()` and `confirm()` are top-level declarations in a classic script, so they are
  properties of the frame's window and are replaced before anything is pressed — a tab click
  calls save(), and an unstubbed walk would have written six demo teams over the reader's own
  board on the shared origin. `sv-data` is read back at the end and compared. The walk visits
  every tab ONCE PER TEAM, because four of the views are decided per team.
  Verified by breaking a render on purpose and watching the suite go red where nothing else
  did — do that again if you ever doubt it is still connected. The starter carries the same
  walk, so a new app inherits one.
- **Rows are padded to the widest row.** The PI table's empty slots are one cell with
  `colspan`, which would otherwise emit a two-column row in a nine-column file — valid CSV,
  and every spreadsheet then reads the rest of that row against the wrong headings.
- **A CSV is the one place text leaves this app for somewhere it can be INTERPRETED, and it
  is escaped accordingly.** A cell opening with one of OWASP's six leads — `=` `+` `-` `@`
  TAB CR — is a formula to Excel, Numbers and Sheets alike, so `csvCell()` prefixes it with
  an apostrophe: the same reasoning as `esc()` for HTML, in a different grammar. The tab and
  the carriage return are in the set because a reader that strips the leading whitespace then
  finds the formula underneath.
  **`PLAIN_NUMBER` is the carve-out, and the question it asks is "is the WHOLE cell a
  number?"** — a real figure (`-5`, `+4.3`) goes through, because quoting it would break the
  arithmetic people export a CSV to do. Until 2026-08-27 this was a lookahead,
  `^-(?![0-9.])`, which asked only whether the character after the sign was a digit and so
  let `-3abc`, `-1+1` and `-3+cmd|' /c calc'!A0` straight out of the app; it also sent every
  leading `+` to the escape, which would have made a signed figure text. **The same two lines
  are now in all seven exporters in the family** (here, Flow Metrics, Golf Handicap, PAPTrack,
  the starter and both lottery pages) — a change to the rule belongs in all of them.
  `toTsv()` carries the identical guard: the clipboard lands in the same spreadsheet the file
  would have opened in, so it is not the safer door. Quoting is separate and triggers on `"`,
  `,` or a newline
  — and **the comma case is not hypothetical**: `fmtNum()` groups thousands, so a four-figure
  points total arrives as `1,234` and an unquoted row silently gains a column.
  **Money Map is the one deliberate exception**: its `csvCell()` takes an `isText` flag and
  guards only the cells it knows are text, which is possible there because it builds its rows
  from state and knows which is which. This one scrapes the DOM and cannot, hence the
  value-based carve-out. That is a different answer to the same question rather than a repo
  that is behind — but if the guard is ever widened, widen both, and check its reasoning
  before assuming so.
- **Two clipboard routes, then a message.** `navigator.clipboard` needs a secure context and,
  in several browsers, a permission or a trusted gesture; `execCommand('copy')` is deprecated
  and is what works when the first is refused. If both fail the toast points at the CSV
  button rather than leaving a control that appears to do nothing. The temporary textarea is
  positioned off-screen, **not `display: none`** — a hidden element cannot be selected, so the
  copy would take nothing. TSV for the clipboard and CSV for the file, deliberately: a pasted
  CSV lands as one column of text, and a file has to be a CSV to open as a spreadsheet.
  A `﻿` BOM leads the file or Excel on Windows reads UTF-8 as Latin-1 and mangles any
  accented team name.
- **Export buttons stay ON in a shared view, unlike every other control there.** Everything
  else `viewOnly` strips is stripped because it would WRITE — that is what `wireEditRows()`
  is doing to the row buttons. Export writes nothing and reads the rendered table, so it can
  only hand back figures already on the recipient's screen. Sharing a link is how a fellow SM
  gets these numbers; letting them paste the table into their own notes is the point of the
  feature, not a hole in it.
- **A card heading that shares its line with a control needs `.row.cardhead`.** `.card > h2`
  stops matching once the heading sits inside a flex row, and it silently falls back to the
  browser's default h2 — half again the size of every other heading on the page. The class
  restores the treatment and carries the 4px the heading's own margin contributed.
- RAG state must never be conveyed by colour alone — tiles and pills carry a glyph and an
  `sr-only` status. Every theme is WCAG AA on the figures; keep them that way.
- **A RAG surface is a tint fill plus a status-colour edge, everywhere** — `.tile`, `.pill` and
  the Compare Teams bars all pair `--green`/`--amber`/`--red` with their `-bg` tint. `ragVar()` is
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
  tab only when the view behind it has nothing to say: **Compare Teams** needs a second team,
  **Team PI** needs a PI *and* a sprint of the active team's inside one, **PI Trend** needs
  two PIs with something in them, **Rolling 5**
  needs at least one recorded sprint *for the active team*
  (so they come and go as you switch teams), **History** needs MORE than `ROLLING_WINDOW`
  sprints for that team — below that it would be Rolling 5 under another heading, and a tab
  that duplicates its neighbour teaches a reader the tabs don't mean anything —
  and with no teams at all the whole row goes
  rather than leaving a lone Sprint tab over the welcome card. If the stored view's tab has
  just been hidden it falls back to `sprint`, corrected **in memory** — a render must never
  `save()`, which would write over the stored copy. **A shared view keeps its own rule for All
  teams** (`shareMeta.allTeams`, which the sender opts into and which already requires two
  teams): that check moved out of `openSharedView()` into `renderTabs()`, so don't
  reinstate it there.
- **History is the view with NO window, and that is its whole definition** (2026-08-22).
  Every other per-team view looks through one — five sprints, or six — which left a team with
  three PIs behind it holding eighteen sprints nothing could show sprint by sprint (PI Trend
  flattens them to one point per PI). It deliberately does **not** call `rollingSprints()`:
  the two rolling toggles narrow a window and this view has none, so every sprint is listed,
  with the in-flight and left-out ones drawn and marked rather than dropped. Its Direction
  tile is `trendChange()` over the whole run, and the demo is built so it disagrees with the
  five-sprint figure on both long-history teams — that disagreement IS the argument for the
  view, and a test pins it so tidying those numbers can't quietly remove it.
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
- **`SCHEMA` is what makes that boundary safe against OLDER code, and it exists because
  of the service worker.** The allowlists above DELETE any key they don't know, which is
  exactly right for a hostile payload and exactly wrong for a copy written by a NEWER
  build: an older tab would strip the fields it has never heard of, render what's left,
  and SAVE the stripped copy on the next edit — the missing fields gone silently. So
  `version` (`SCHEMA`, currently **5** — `objectives` took it off 1, `goalMet` to 3,
  optional `piId` to 4, `settings.targets` to 5) rides into localStorage and every backup
  file, and these boundaries compare it:
  - `load()` calls **`haltForNewerData()`** — a full-screen card, no render, and a `throw`
    that aborts the rest of the script block so nothing can save over the newer copy. It
    reuses `viewOnly` (and `window.svViewOnly`) rather than inventing a second flag, so
    `save()` is already a no-op and the service-worker block registers nothing. (`svAdopt()`
    was the second caller and wrote the newer document to localStorage **verbatim** before
    halting, because a copy arriving from another device really was the newest there was;
    both went with sync on 2026-08-20.)
  - `load()`'s check is deliberately OUTSIDE the `try` whose `catch` returns
    `blankState()`: that catch is right for corrupt JSON and catastrophic here, because a
    blank state the app then saves overwrites the good copy with nothing.
  - The **Restore** path refuses the file with a toast and does NOT halt — nothing has
    arrived yet and what's on screen is still good.
  - Share links carry their own `SHARE_PAYLOAD_V` (a different thing from `SHARE_FORMAT`,
    which is only how the bytes are packed). `decodeShare()` marks the error
    `newerVersion` so the card can say the link is fine and this copy is behind, rather
    than sending the reader off to chase a fresh link.
  **The `piId`-optional bump is the sharpest case this repo has had**: a SCHEMA-3 build
  reading a copy that holds unassigned sprints runs the old orphan filter, `piIds.has(null)`
  is false, and it DELETES every one of them — then saves that. A whole pre-PI history gone
  from opening one stale cached tab. That is exactly what
  `haltForNewerData()` is for, and without the bump it never fires.
  **Bump `SCHEMA` in the same commit that adds or repurposes a saved field, widen the
  allowlists in that same commit, and check `adoptState()` still stamps the new number** — a bump without the allowlist change protects a field
  the boundary then strips anyway. UI-only state (theme, active tab) needs no bump.
  All four boundaries are pinned in tests.html.
  **`settings.targets` took it to 5 on 2026-08-22, and it is the case that shows where the
  "UI state needs no bump" line actually falls**: a target looks like a preference, sits in
  `settings` next to `view`, and still earns the bump — because it is SAVED and because an
  older build that stripped it would go on judging every figure in the file against 85/15/20
  while the tiles said otherwise. Wrong colours on a portfolio slide is quiet enough to be
  worth halting for. The theme is the counter-example and still needs no bump: it lives under
  its own key and changes nothing about the data.
- **`sanitizeIds()` must never invent a key, and `cleanKey()` is why.** `x.id = clean(x.id)`
  on an **absent** key looks harmless and isn't: `clean()` returns what it was given, and
  the assignment creates the key holding `undefined`. `JSON.stringify` drops that silently,
  so the key reads as "never set" on the next load rather than announcing itself.
  **This was far worse when the app synced**, and the history is worth keeping: `setDoc()`
  walked the *live* object and Firestore rejected the whole document over one `undefined`
  with `invalid-argument`, which is what shipping `settings.artFilter` did on 2026-08-12 —
  every browser holding a copy saved before ARTs existed stopped syncing until something
  happened to set the field, and the local copy gave no sign of it. Sync is gone; the rule
  is not. Add an optional field and it goes through `cleanKey()` too. Pinned in tests.html
  by *key*, not by value — `x === undefined` passes either way.
- **Retired with sync, but the lesson generalises.** `describeSyncError()` learned that
  `invalid-argument` did not mean "too big" — Firestore reported both an oversized document
  and an unstorable value under that one code, and assuming the first meant an app bug told
  the user to export a backup and **delete a PI**. Whenever error copy here suggests a
  remedy: a remedy that destroys data must never be the guess.
- **The same boundary drops orphans.** After the remapping (never before it — a remapped
  sprint isn't an orphan), a sprint whose `teamId` or `piId` names nothing in the same
  payload is removed, and the count left on `sanitizeIds.dropped`. Nothing threw without
  this: `teamSprints()`/`rollingSprints()` counted the orphan into the Rolling 5 average
  while every PI-based view couldn't show it, its PI never reaching the picker — a figure
  moving with no visible sprint behind it. Delete PI / Delete Team filter `state.sprints`
  correctly, so this only arrives from a hand-edited or damaged payload. **Only the TEAM half
  still drops** — the PI half un-groups instead, see the PI-optional rule above. All four
  callers **say so** (`orphanNote()` / `unassignedNote()`), per the never-silent-exclusion rule: the import names it in
  its confirm, before the user commits; the share view toasts after `render()`; `load()`
  hands the count to `bootOrphans` because a toast raised during parse is gone before
  there's anything to look at.
- Charts resolve their colours from CSS custom properties at construction time, so a theme
  switch has to rebuild them (`render()` does this). Chart animation is deliberately off.
- **Cross-device sync was REMOVED on 2026-08-20 — don't put it back without asking.**
  Google sign-in + one Firestore doc per user at `sprintvelocity/{uid}`, project
  `sprintvelocity-141b7`, went at Charles's request, in the same sweep as the identical
  module in Flow Metrics. This app holds figures copied out of a work Jira, and the answer
  to "where does that live" is now "one browser, and nowhere else".
  - **It was removed, not disabled.** The module, `#syncBtn`, the which-copy dialog,
    `firestore.rules`, `svAdopt()`, `svCounts()`, `cloudPush`/`cloudFlush`/`svSignedIn` and
    every Google address in the CSP went together. Setting `FIREBASE_CONFIG = null` would
    have left the code, the origins and the CSP in place — which is not the same claim.
  - **The pins are in `tests.html`.** A CSP naming no host at all and `connect-src 'none'`
    spelled out; no module script; no `import(`; a word-list tripwire over `appCode()` —
    the app source with every comment stripped **to a fixed point**, because a one-pass
    strip leaves `<!--` behind and a half-stripped source would let a word through. Comments
    are exempt deliberately: the note where the module used to be names Firebase so a grep
    lands somewhere useful. Plus a live boot proving the leftover keys are deleted. If you
    are reinstating sync, those tests are the specification of what you are undoing.
  - **`clearSyncLeftovers()` deletes `sv-sync-uid` and `sv-updated` on every load.**
    `sv-sync-uid` is a Google account id, the only personally identifying thing this app
    ever wrote down; leaving it after removing the feature would be keeping an identifier
    for nothing.
  - **`svGet` survives; `svAdopt` and `svCounts` did not.** tests.html reads the live state
    through `svGet`, which is worth keeping — a suite that asks the app what it holds beats
    one reaching into a closure. `svAdopt` had no caller but sync (Restore builds its own
    state), so it went, and with it the "store a newer copy verbatim before halting"
    behaviour: that made sense only when the incoming copy was genuinely the newest in
    existence. Boot's `load()` is now the only caller of `haltForNewerData()`.
  - **The `undefined` rule STAYS even though its original reason went.** `cleanKey` never
    creates a key holding `undefined` because Firestore refused the whole document over one
    — that is how `settings.artFilter` stopped sync for every browser with a pre-ARTs copy.
    Firestore is gone; the rule is not, because `JSON.stringify` drops an undefined
    silently, so such a field reads as "never set" on the next load instead of announcing
    itself. Same for `goalMet` and `capacityScale` deleting rather than storing a no-op.
  - **What was lost with it, and would have to be rebuilt**: the Google Identity Services
    workaround for corporate filters that block `firebaseapp.com` **per hostname** (proven
    in Team Dashboard first, measured, and not something a fresh implementation would think
    of), the never-guess-by-timestamp reconciliation, the empty-copy-never-wins rule, the
    `serverAt` ordering and the surfaced-not-logged failure reporting. All in one commit in
    `git log`.
  - **The Firestore data was deleted too, 2026-08-20**, by hand in the console — removing a
    client deletes nothing server-side, so this was a separate deliberate step. The
    `sprintvelocity` collection is empty, and `DATA_DELETION.md` was removed with the data it
    described (a runbook that confidently describes something that no longer exists deletes
    the wrong thing).
  - **Charles's account was the ONLY one that ever signed in**, confirmed from the Firebase
    Authentication list on 2026-08-20. The premise this repo was built on — fellow Scrum
    Masters signing in with their own Google accounts, each getting a private doc — never
    actually happened. So no third party's data was ever in that database, the deletion cost
    nobody anything, and `privacy.html` no longer carries a deletion-request route because it
    would be offering a service to an empty set. Read the older docs with that in mind.
  - The project `sprintvelocity-141b7` and Charles's own Auth row still exist. Deleting the
    project outright is a further step nobody has taken; it would also kill the API key
    GitHub's secret scanner flags on this repo.
- **The Rolling 5 velocity chart carries a dashed `linearTrend()` line** (ordinary least
  squares, ported from Team Dashboard; nulls skipped). It's drawn muted — a reading of the
  bars, not a new series — and `linearTrend()` is a pure function pinned by tests.html.
- **A TILE ROW FILLS ONE LINE WHEN THE LINE HAS ROOM, AND SPLITS INTO EQUAL ROWS WHEN IT
  DOES NOT (2026-08-23, family-wide).** Never a full row with a lone tile stranded under it:
  the eye finishes the row, finds a gap, and goes looking for the thing that should have been
  there. Money Map hit it first — six net-worth tiles came out five across with the sixth
  alone — and every app with a variable-count tile row now answers it the same way. Here that
  is a six-tile sprint group whose sixth tile is the sprint goal, which was reading as an
  afterthought rather than as the sixth answer.
  - **The COUNT comes from `:has(> :nth-child(N):last-child)`** — "exactly N children". Every
    group in this app is built from conditionals (`inFlight`, `pace`, `hasGoal`), so the count
    is not knowable when the CSS is written; asking the DOM is the only way to know it.
  - **The WIDTH comes from a CONTAINER query, never the viewport.** `:has(> .tiles)` makes the
    row's own parent the named container `tiles`, so the width asked about is the width the
    tiles actually get, card padding already taken off. A tile group inside a card in a
    `.cards2` half is nowhere near the viewport's width, and a media query would answer the
    wrong question for it. Where no container is found the row keeps the plain auto-fit line,
    which is what it always had.
  - **The thresholds are the 160px minimum tile and the 12px gap multiplied out**: 2→332,
    3→504, 4→676, 5→848, 6→1020, 7→1192, 8→1364. Narrowest first, so the widest rule that
    matches wins. tests.html reads those two numbers back out of the CSS and checks every
    threshold against them, so raising the minimum tile fails the suite rather than quietly
    making a row too tight.
  - **Only counts that leave rows differing by at most one tile are offered, and never a row
    holding a single tile.** Five go 5, or 3 + 2, or one per line — never 2 + 2 + 1. Seven go
    7 or 4 + 3. Where the only alternative would strand one tile the row drops to a single
    column and stacks. Nine or more keeps auto-fit; no group in this app comes near it.
  - **A SHORT LAST ROW IS STRETCHED TO FINISH THE LINE**, never left with a hole at the end of
    it: `lcm(columns, last row)` tracks, the full rows' tiles spanning `lcm/columns` and the
    last row's `lcm/last row`, so 3 + 2 is six tracks at span 2 and span 3. That is Golf
    Handicap's hand-counted grid generalised — its own file says those spans have to be redone
    by hand if a tile is ever added. The stretch is undone at the width where the tiles all fit
    on one line, and **on BOTH selectors**: `:nth-child` out-ranks a bare `> *` and would
    otherwise carry its span into the wider layout.
  - **Flow Metrics has the same block against its `.tiles.group`**, with its own 200px floor.
    Its plain `.tiles` is the deliberate exception in both apps: it is always exactly four
    tiles, one per dimension, and spelling out four columns is already gap-free.
- **THE TILE'S LEFT EDGE IS 6px, AND ITS BACKGROUND DELIBERATELY DID NOT FOLLOW (2026-08-21).**
  Flow Metrics moved its tiles onto `--surface` — the ground its cards and tables are on — and
  widened the left edge from 4px to 6px in the same change, because once the fill no longer told
  a tile from a card, the edge had to. Charles asked for **the edge and only the edge** here.
  Two reasons the background stayed, and the second is the one that settles it:
  - **This tile's background carries meaning.** It is a five-value scale — neutral, green, amber,
    red, and the hero's `--bg-card` — where Flow Metrics has one state, because Flow Metrics has
    no targets to be good or bad against. The neutral is the ground the other four are read
    against.
  - **These tiles sit INSIDE a card; Flow Metrics' sit on the page.** Give them the card's own
    background and the only edge left is the 1px `--border`, a hairline chosen to be quiet — the
    same declaration that unifies that app dissolves these into the box around them. Both states
    were rendered in all four themes before deciding.
  A mirror-and-fix-the-hero option was costed and not taken: the hero would need a new cue (a
  6px `--focus-border` edge is the readiest), and so would the neutrals, which is a redesign of
  this app's tile rather than a copy of the sibling's. The edge is pinned in tests.html as a
  RELATIONSHIP — heavier than the other three borders, and the same width on a RAG tile, which
  sets the colour and never the width — not at 6px, so the number stays tunable.
- **The chrome is shared with Team Dashboard** (the `claude-team-dashboard` repo; the app
  itself is titled **Flow Metrics** on screen — display-only rename, every identifier still
  says team-dashboard) — sticky header, brand mark, button tabs, tiles, ⓘ help,
  footer. The two apps are meant to read as one family; if a chrome rule
  changes here, change it there too (and vice versa). **Each app's footer carries an
  `.applink` to the other** — a plain `<a class="btn small applink">`, no script, mirrored
  in Team Dashboard. It sat in the header beside the title until 2026-08-20, when it moved
  down to the foot of the page and took the place of the plain-text cross-link that used to
  sit on the `.privacy-links` line: **one crossing per page, not two.** It is still
  navigation rather than another thing to do to the data, so it stays visible in a shared
  view. The footer is a flex row — the notes wrapped in `.footnotes`, the link after them
  with `margin: 0 19px 0 auto`, so it sits at the right edge bottom-aligned with the last
  note, and wraps onto its own line (still right-aligned) on a narrow window. The 19px
  mirrors the notes' 19px indent. `.brand` carries the `margin-right: auto` that pushes the
  header controls right again, and `.applink` still needs `display: inline-flex` because
  `.btn.small` pins its height with `min-height`, which an inline box ignores.
- **It is INSTALLABLE, and the manifest is four files agreeing with each other** (2026-08-22,
  the day after Flow Metrics; this app was the last of the family without one). `manifest.webmanifest`,
  `<link rel="manifest">`, `<link rel="apple-touch-icon">`, `<meta name="theme-color">`, the four
  PNGs `make_favicon.py` now writes, the `manifest-src 'self'` directive and five new entries in
  `sw.js`'s `SHELL` — change one and check the others. Five things are load-bearing:
  - **`manifest-src 'self'` has to be SPELLED OUT.** A manifest is covered by no other
    directive, so under `default-src 'none'` the fetch is refused and "Install app" silently
    stops appearing — nothing errors, nothing shows, and it works perfectly on a browser you
    are not testing with. It admits a static JSON file on this origin and nothing else.
  - **`scope` is `./`, never `/`.** Every app in the family is served from ONE origin, so an
    absolute scope would capture Flow Metrics and Money Map into this app's installed window.
    The same reasoning as the service worker's scope, and the test asserts it by name.
  - **The manifest and its icons are on the offline SHELL.** An installed copy is the one most
    likely to be opened with no network at all, and a launcher re-reads both to draw the
    window; without them a cold offline start shows a blank icon and can drop out of
    standalone. They are files already public in this repo, so the origin-wide-cache rule is
    unchanged — and the justification for them is written ABOVE the array, not between its
    entries, because the suite pulls every quoted string out of that array and an apostrophe
    in a comment inside it would hand the check a fake entry.
  - **Three icons, three jobs.** The `any` pair and `favicon.ico` are ROUNDED (nothing masks
    them); the maskable is FULL BLEED with square corners (a launcher crops it, so rounding
    would round a picture about to be rounded again); `apple-touch-icon.png` is square and
    OPAQUE (Apple masks it, and a rounded source leaves a pale seam inside the curve). The
    maskable safe zone is radius 25.6 in the 64 viewport and this mark reaches 23.5 — the
    commitment dot sits ON the ring, so 17 + 6.5. Widen the ring or enlarge the dot and
    re-check that sum; the docstring carries it.
  - **`theme-color` is a literal in the head and repainted by `applyTheme()`.** The literal has
    to be there because it must be right before any script runs, and it is only ever right for
    Midnight — so `paintThemeColor()` rewrites it from the pack's own `--bg`, never from a
    colour of this app's own. Under **Auto** the palette moves with nobody touching the
    picker, and the `prefers-color-scheme` listener at the foot of the file — added the same
    morning, for the charts — covers the title bar too, because it calls `applyTheme()`. That
    is the point of putting the repaint THERE: one call site, so the bar and the charts cannot
    disagree about which palette is in force. Anything else that has to follow the theme goes
    into `applyTheme()` as well, not into a second listener.
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
  hosted localStorage — one browser origin shared with every other app on the account — has
  to stay clean of anything sensitive, so the
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
  reaches localStorage immediately — and ONLY when something was scrubbed: since 2026-09-01
  the six typed forecast fields are `numOrBlank`, so their stated `''` is a value rather than
  a repair, and a null tribool is absent rather than repaired; before that every boot counted
  at least one and saved). Rebuilt objects only ever gain keys that are present
  and valid, so the boundary can never create a key holding `undefined` — the `cleanKey`
  rule above. **A new stored field must be added to the
  `keepKnown` spec or it will be silently stripped** — that's the point, and the same-named
  test in tests.html pins it. The only free-text left is the short team/ART/PI names. The
  sprint form's one disclosure is `#jiraBlock`, closed on every `openSprint()`.
  **The bulk importer is the first thing that could have widened this and deliberately does
  not** (2026-08-22). `parseImport()` takes a pasted spreadsheet, and the rule that shapes all
  of it is that a `team` or `pi` cell is **looked up and then discarded**: it finds a row that
  already exists and never creates one. So the only things that path can write are the same
  figures, dates and tri-state goal the sprint form writes — a bulk importer able to create a
  team from pasted text would be a free-text field with extra steps. `settings.targets` is the
  one NESTED object crossing `keepKnown()`, and it gets the same treatment one level down:
  only the eight keys `TARGET_FIELDS` names, each clamped to that field's range, everything
  else counted in `pruned` and dropped. Note the `kind !== 'targets'` exemption on the general
  pruned test — a rebuilt object is never `===` the one that came in, so without it every boot
  would count itself a scrub and `save()`.
  **The capacity levers' reason codes are a fixed enum (`REASONS`) and must never become a
  text box.** "Why did we drop that sprint?" is the obvious place for someone to reach for
  free text later, and it is exactly where a ticket key or a colleague's name would ride into
  a saved copy, a backup or a share link. The `'reason'` kind in `keepKnown()` pins the value to the list and an unknown
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
  Save" while a snapshot is held. It stays on the button rather than moving to the toast, and
  the reason changed on 2026-08-22 — `toast()` CAN hold a control now (see the delete undo
  below), but this undo belongs to a dialog that is still open and whose Cancel is the thing
  the user is already reaching for. A toast that expires while the form is still on screen
  would be worse than the button, not better.
- **A delete can be taken back, and the toast is where the offer lives** (2026-08-22).
  `undoable(fn)` stringifies the seven collections before `fn` runs and hands back a
  `restore()`; `undoableToast()` wraps that with the re-render and a toast carrying an **Undo**
  button. A **whole-state snapshot, not a hand-written inverse**: the four deletes reach four
  collections and two settings between them, and an inverse per delete is a list somebody has
  to remember to extend the next time one learns to tidy up after itself. Three deliberate
  limits: it is **one step, not a stack** (what an undo history should survive — a reload? an
  import? — has no obvious answer here, and a half-answered one is worse than none); the
  **`confirm()` before each delete stays**, because one toast replaces the next so Undo is an
  offer rather than a guarantee; and **Delete all data deliberately has none** — that one is
  meant to be hard, it already says exactly how much is going and offers the backup that is
  the real way back, and a 10-second Undo would quietly make it the easiest destructive thing
  in the app. `toast(msg, action)` gained the button: `pointer-events` go to `auto` and the
  timeout to 10s ONLY when there is one, because a plain toast swallowing a click on whatever
  is under it for 2.6 seconds is worse than the toast. **The countdown pauses while the toast
  holds focus** (`focusin`/`focusout` → `toast._go()`) — a keyboard reader has to tab to that
  button, and a timer that expires while they are standing on it is worse than not offering
  one. And **`#toastAction` wears the TOAST's colours, not a button's**: the toast is an
  inverted pill (`--btn-bg` behind `--btn-text`), so an ordinary `.btn` in it is styled for
  the page behind it and axe measured 2.5:1 in Midnight and 3.3:1 in Light. `color: inherit`
  plus a `currentColor` outline is the pack's own pair and clears its gate by construction —
  the rule being that a contrast fix REUSES an existing token and never invents one, or the
  palette drifts a patch at a time. A test pins that it names no colour of its own.
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
  after `#` is sent to a server, which is the whole reason this needs no account and no
  network. `buildSharePayload()` emits a **trimmed copy** — chosen teams only,
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
  recipient's own views count or exclude it by the usual rules. **A PI window never carries
  pre-PI sprints (2026-09-01)** — they rank -1 in program order, and `-1 > newest - n` let them
  through whenever the window reached past the first PI, while both notes said earlier history
  was excluded; with no PI in the payload at all the window is the whole history.
- **The window's exclusions are never silent, on both sides.** A team the window leaves empty
  is dropped from the payload (never *all* of them — `decodeShare()` refuses a teamless
  payload) and named in the dialog, because shipping it lands the recipient on an empty sprint
  card. Cutting a team below `ROLLING_WINDOW` warns too: that changes the *figures* the
  recipient sees, not just the length of the link. The recipient's banner says a window is in
  force, built by `shareRangeNote()` from `range: { kind, n }` — **two numbers, never a
  sentence the sender wrote**, so a hand-edited link has no text to inject — and deliberately
  without a total, so the sender isn't publishing how much history exists behind it. Since
  2026-09-01 `sanitizeIds` PINS it beside `label` and `sharedAt`: `kind` ∈ {pi, sprint}, `n` a
  whole number from 1 to `MAX_SPRINT_NO`, anything else dropped — `n: '1e400'` printed "the
  last Infinity PIs".
- **"As much as fits" bisects, and must keep checking `shareSeq` between trials.** Link length
  only grows with the window, so `fitShareWindow()` binary-searches it in about six encodes
  instead of fifty. It searches sprints, not PIs: a PI step is six sprints and overshoots by
  thousands of characters. With several encodes in flight, checking the sequence only at the
  end would let a stale search finish over a fresh one.
- **`save()` is the view-mode chokepoint.** `viewOnly` makes it a no-op, and because it's the
  one place that writes localStorage, that single guard is what guarantees a shared link
  can't overwrite the viewer's own data — often another SM in the same browser.
  `window.svViewOnly` mirrors the flag for the service-worker block, which is a script of
  its own; keep both. (It was load-bearing for a third reason until 2026-08-20: without it
  the sync module would initialise in a shared view and `onAuthStateChanged` →
  `startSync()` → `svAdopt()` would replace the shared payload with the viewer's cloud copy
  and push it straight back.)
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
  textContent the shared-view path rewrites). Other SMs use this app with their own data, so
  it exists for them: what is stored, that it stays in their browser, that share links
  upload nothing, and — for anyone who used sync before 2026-08-20 — the deletion contact.
  Effective date is **2026-08-20**, moved when sync was removed. If share links or what the
  app stores ever change, update it and its date in the same commit.
- **README.md is the index** — keep it current whenever the app meaningfully changes.
- After changes: **browser-test locally first** (`python3 -m http.server 8012`, or the
  desktop app's preview pane via `.claude/launch.json`), then commit, push, verify the
  Pages deploy, and spot-check live. Any local server + browser works — don't hunt for a
  specific tool.
- **`tests.html` busts its own cache, on the frames AND on the source fetches (2026-08-22),
  and that is not tidiness.** `const BUST = '?t=' + Date.now()` goes on every hidden
  `iframe.src` and through `bustFetch()` on every read of a file this repo ships. The frame
  cache and the HTTP cache are different caches and they can disagree: in the lottery repo
  the same harness reported **all-green against a page three features out of date**, because
  the source-level tests were reading the file off the server while the frames ran a copy the
  browser had cached. Nothing errored; the new code was simply never run. A suite that can
  pass against a build which exists nowhere is worse than no suite — it turns "untested" into
  "verified". **If a test passes when you expected it to fail, check
  `document.getElementById('app').contentWindow` has the function you just wrote before
  believing anything.** The GitHub API call at the foot of the file is deliberately left
  un-busted: it is somebody else's endpoint, not a file we ship.
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
- Write commit subject lines in plain English a non-developer can read. The in-app
  "Recent changes" box that made them user-facing was removed on 2026-08-18 (in every app
  in the family, with the GitHub API dropped from each page's CSP), but the habit stands:
  the commit history is still the only record of what changed.
- **There IS a service worker, and it was refused for a long time.** The three
  objections were right to be made; two turned out to be answerable by design
  rather than by abstention, and the third is what the whole thing is built
  around. Recorded because the next person to touch this needs the reasoning:
  - *"A resident process on the shared origin."* Bounded. A worker's scope
    cannot exceed its own directory without the `Service-Worker-Allowed` header,
    and GitHub Pages cannot send headers — so this one structurally cannot see
    Flow Metrics or financial-plan. Locally, where the app is served from the
    root, it does control `tests.html`; the allowlist is what makes that
    harmless, not the scope.
  - *"Caches are ORIGIN-wide, not per app."* True, and it does not go away — any
    page on the origin can read this cache, and the sibling workers share the
    store. The answer is the rule in `sw.js`: **only files already public in
    this repo are ever cached** (`./`, `chart.min.js`, `theme.css`,
    `privacy.html`, `favicon.ico`). Nothing in there is anything an attacker
    could not read straight off GitHub, and the data stays in localStorage,
    which every page on the origin could already reach. It cuts the other way
    too — `activate` must only ever delete caches with this app's `sv-shell-`
    prefix, or it wipes a sibling's.
  - *"A caching bug serves stale code to an app whose data shape moves."* Still
    the real risk. **The worker is network-first for everything**: you can only
    be served cached code on a visit where the network did not answer. The
    braces to that belt is `SCHEMA` / `haltForNewerData()` above — a saved copy
    from a newer build is refused rather than run through sanitizeIds(), which
    would strip the fields that build added.
- **The page's CSP does not apply to the worker.** It takes its policy from its
  own script's HTTP response headers, and Pages cannot set headers, so `sw.js`
  runs with **no CSP at all**, permanently installed. Hence: tiny, no `eval`, no
  `importScripts`, no dynamic import, no cross-origin URL anywhere in it — and
  hence `worker-src 'self'` spelled out in the page CSP rather than left to the
  `worker-src → child-src → script-src` fallback chain, which would inherit
  script-src's gstatic and accounts.google.com hosts.
- **`sw-kill.js` is the escape hatch, and it exists BEFORE it is needed.** A bad
  page is fixed by pushing a new one; a bad worker is resident and can keep
  serving itself. `cp sw-kill.js sw.js`, commit, push — every installed copy
  then clears this app's caches, unregisters itself and reloads its windows.
- **Two traps, both of which fail silently:** `cache.addAll` is all-or-nothing
  (one 404 rejects the whole precache, install fails, and there is no offline at
  all while the app looks perfectly healthy online); and **`install` fires once
  per script version**, so if the cache is later evicted nothing rebuilds it and
  offline decays to "whatever the last online visit happened to request". Hence
  `topUp()`, fetching entries one by one, pinged by the page on every load via a
  `shell-check` message — the repair must be able to run without a new worker
  version to hang it on.
- **`shellKey()` matches on the PATH, not the URL**, because the markup asks for
  `favicon.ico?v=1`: keyed on the full URL, the precached favicon would never be
  the entry that answers. `index.html` folds onto `./` for the same reason.
- Registration is guarded three ways, all load-bearing: **not in a frame** (or a
  `tests.html` run would install a worker and then test whatever it had cached),
  **not under `window.svViewOnly`** — which covers both a shared view and a page
  stopped by `haltForNewerData()`, since the halt's `throw` cannot reach a
  separate script block — and **on `load`**.
- **Testing it locally will mislead you.** The browser holds its own copy of
  `sw.js`, and a byte-identical script fires no `install`, so edits appear to do
  nothing and an emptied cache appears not to refill. `await reg.update()`
  before judging any of it. Related: a suite run against a registered dev worker
  is testing the cache, not the disk — unregister it on localhost before
  trusting a green run.
- The scope is `./`, never absolute: on the local server the app is at the root,
  not under `/sprint-velocity/`, and an absolute scope is simply invalid there.

## One chart, filling the window (2026-08-30)

**Every card that draws a chart carries a ⤢ button that lifts the card into a
fixed overlay filling the window under the header.** Flow Metrics' feature
(2026-08-21) — these two apps share their chrome, so a change to it in one
belongs in the other; Money Map and the starter carry it too. It is NOT the
Fullscreen API and NOT a modal `<dialog>`: the phrase that shaped it is "with
the menu still visible", and both of those take the header away.
`#chartMaxi` is an ordinary fixed div at z-index 15 against the header's 20,
starting at `--maxi-top` (the header's MEASURED height) and outside `.wrap`,
which goes `inert` while it is open.

**The card is MOVED, not copied.** Every chart is drawn into a canvas found by
id and a theme change destroys and rebuilds all of them; a second canvas up
there would leave those redraws painting the copy left on the page. A hidden
`.chart-slot` holds the card's seat.

**The one thing this app has to do that Flow Metrics does not:** every view
rebuilds `viewsEl.innerHTML` wholesale, so the maximised card would be orphaned
and its placeholder thrown away with the markup round it. `render()` calls
`maxiSuspend()` as its first line and `maxiResume(id)` at both of its exits: the
card comes down, the view is drawn again, and the card carrying the same CANVAS
ID goes back up. Nothing paints in between, so there is no flicker. This is the
ordinary path — the team picker sits in the header that deliberately stays live.
For the same reason the buttons are added at the end of every render
(`syncMaxiButtons`) rather than once at boot as they are there.

**Two traps, both found the day this shipped, both fixed in all four apps that
carry the feature:**
- **`.chart-max svg { pointer-events: none; }`** — pressing the button rewrites
  its own innerHTML to the arrows-in icon, which DETACHES whatever the pointer
  landed on, and a detached node answers null to every `closest()` a delegated
  handler further up asks. Money Map's card heading acted on that null and
  folded the card instead of filling the window.
- **`.chart-max[hidden] { display: none; }`** — `.chart-max` declares
  `display: flex`, and an author rule beats the browser's own
  `[hidden] { display: none }` whatever the specificities. `btn.hidden = true`
  read back true over a button anybody could see, offering a chart that is not
  drawn. **A test that asserts `btn.hidden` is deaf to this**: read the computed
  display.

`maxiCard()`, `openMaxi(card)`, `closeMaxi()`, `maxiReady(card)` and
`chartIn(card)` are top-level function declarations, so the suite drives the
real thing through the frame's window.

## Pinning the tab row (2026-09-03)

**The tab row held at the top of the window while the page scrolls under it**,
off by default and toggled from a 📌 at the end of the row. Asked for in Flow
Metrics first and mirrored here at Charles's word, so a change belongs in both —
and in Money Map, which has the same button. `data-pin` on `<html>` set by the
head script before first paint, `--pin-top` measured from the header's real
rectangle, `sv-pin` in localStorage.

- **THE TAB ROW AND NOTHING ELSE, and that is the difference from Flow Metrics.**
  That app pins its tabs together with a control strip, because the strip is
  shared markup outside the panel meaning the same thing on both its number
  views. Everything under the tabs HERE is inside `#views` and is rewritten per
  view — the PI picker on Sprint, an ART picker on three of the others, two
  toolbar cards on Compare Teams — so there is no second row that is the same row
  from one view to the next. Pinned by an assertion that the row's next sibling
  IS `#views`, so a later port of the sibling's second row cannot happen by
  accident.
- **The margin became padding.** A margin is transparent, so pinned, the page
  scrolled through a 20px window under the row. Same 20px, same total height —
  which is what makes the toggle cost no reflow, asserted by measuring the view's
  top and the document height both ways.
- **`measurePinTop()` runs at the end of `render()`**, both exits, as well as
  from the ResizeObserver: `renderTabs()` takes tabs away and puts them back,
  which rewraps the row, and **an observer is delivered with the next rendering
  step, which a background window does not have**.
- **Z-index 12 is penned in on both sides**: under the header's 20 and under
  `#chartMaxi`'s 15, because a maximised chart covers the page and `.wrap` is
  inert underneath it.

**No phone rule for the PIN, deliberately.** Flow Metrics needs one because it
pins two rows and has to drop one on a phone; there is only one row here.

**The tabs themselves became one scrolling row instead** (2026-09-03, asked for
the same day and for the pin's sake). Seven tabs need about 800px in a line — six
come to 670 and the button another 38 — so on a phone they wrapped to three rows,
170px against a header of 210, which pinned was nearly half the screen. `nowrap`
plus `overflow-x: auto` under 820px makes it 42, and it is harmless where they
fit: a nowrap row only scrolls when there is something to scroll.
- **The pin button is NOT in the scroller**, which is the whole reason `.tabrow`
  exists as a wrapper — inside `.tabs` it would scroll away with them.
- **renderTabs() nudges the chosen tab into view**, only when it is actually off
  an end (a row that re-centres on a tab you can see shuffles on every render),
  by RECTANGLE and not `offsetLeft` (whose offsetParent is the page, so the two
  numbers are in different frames), and **never `scrollIntoView`** — that is free
  to scroll the PAGE to satisfy the vertical axis. Money Map's arithmetic.
- **The suite measures the row against a TAB, not against a number**: the row
  also carries the pin's 20px band and a scrollbar, so a literal would be pinning
  those as much as the thing it is about.

Its own `t()` with its own 1280x900 frame: the shared frame is 1px wide, and a
sticky offset measured there is measuring nothing.

## Stepping between charts in full screen (2026-09-03)

**A `‹` and a `›` beside the ⤢ walk the charts on the view without coming back
down.** Charles asked for it on 2026-09-03; built first in Flow Metrics and
ported here the same day, so a change belongs in both.

- **The arrows live in the OVERLAY, not in a card**, and here that is doubly
  load-bearing. A step moves one card out and another in, and a button inside the
  card would be detached under the pointer mid-press — a detached button takes
  the keyboard's focus to `<body>` with it. On top of that, `#views` is thrown
  away and rebuilt on every render, so a nav inside a card would go with it.
- **`maxiCard()` reads `#chartMaxi > .card`, not `firstElementChild`.** The
  overlay is no longer empty when nothing is up: it holds the arrows and the live
  region permanently.
- **The walk is whatever `#views` holds**, which IS the view the reader is on,
  because this app rewrites it wholesale per tab. There is no way to step into a
  tab they are not looking at. Rolling 5 is the only view with two charts today,
  so it is the only place the arrows appear.
- **A step is `detachMaxi()` + `attachMaxi()`** — the same pair `render()` uses,
  and for the same reason: nothing is painted between them, so the window never
  blinks and the scroll position, the inert `.wrap` and `--maxi-top` are all left
  alone. This is the same window with a different chart in it.
- **`maxiResume()` re-reads the arrows AFTER `attachMaxi()`, not before.**
  `syncMaxiButtons()` runs first, while the overlay is still empty, and correctly
  reads the walk as nothing at all.
- **`.maxi-nav` is positioned from a sum that includes the card's 1px BORDER**
  (20 + 1 + 13 down; + 26 + 6 across), because an absolutely positioned box is
  offset from its containing block's *padding* box.

- **The arrow-key handler skips ARIA ROLES, not just form controls.** Money Map
  found it on 2026-09-03: its Net Worth card carries an "as of" radio pair INSIDE
  the card, so it is still reachable while that card fills the window, and Right
  both moved the month and stepped the chart. A `<button role="radio">` is not an
  `<input>`. The guard names radiogroup, tablist, listbox, menu, menubar, slider,
  spinbutton, grid and tree, and the same list is in all four apps — nothing here
  puts such a control inside a chart card TODAY, which is exactly why it would be
  missed the day something does.

Its own `t()` with its own 1280x900 frame. **A test that holds a card across a
render is holding a node that no longer exists** — `#views` was rebuilt under it,
so the assertions after the re-render compare NAMES.

## The Manage Dialog's Rows (2026-08-20)

Teams, ARTs and PIs are all edited the same way now, and the same way Flow Metrics edits
its own — Charles asked for the two to match, and the two apps share their chrome.

- **A name is edited in place, not behind a Rename button and a `prompt()`.** One
  `[data-name-<kind>]` box per row, `oninput`, capped at 120 where it is written (maxlength
  stops typing past it but not a paste). **None of the three handlers may call
  `renderManage()`** — that would replace the very box being typed in. `render()` is enough
  for teams and PIs, whose names appear only in the chrome outside this dialog.
- **An ART's name is the exception**, because it is printed inside every team's ART picker.
  That handler calls `renderManageTeamRows()` — the teams table extracted for exactly this,
  markup and its four handlers together — which rebuilds the pickers and leaves the ARTs
  table, and so the box being typed in, alone. Don't collapse it back into `renderManage`.
- **`+ Add` no longer prompts.** It pushes a row with a working default name and focuses the
  box, already selected. A prompt would have been the only place left in the dialog asking
  for a name in a box on top of a box, and it refused to add anything at all on Cancel,
  which is a strange answer to "+ Add team".
- **Delete is `.icon-btn.danger`; the arrows are plain `.icon-btn`.** The base hover is
  neutral and `.danger` is what turns it red — the same split `.btn` / `.btn.danger` already
  uses. Moving something is not destructive and must not light up as though it were.
- **All three lists reorder**, not just PIs. PI order was always this app's sense of time;
  team and ART order are read too, down every picker and every Compare Teams table. Reordering
  permutes an array that was always there, so **no new field and no version bump**.
  `reorderById` is the permutation on its own, split out so tests.html can pin it without
  writing anything — this suite is read-only about storage and must stay that way.
- **Ends are disabled rather than hidden**: a button that vanishes at the top of a list makes
  the row jump and moves the delete under the pointer.
- **A PI row's count says what it is counting** (2026-09-02). It read a bare "17 sprints",
  four lines under the section's own note saying *Each PI holds 6 sprints* — so "6 sprints"
  beside PI 2026.1 read as a PI that was full, and 17 as one holding three times what a PI
  can hold. The figure was right throughout: it is every TEAM's sprints in that PI, which is
  the sentence the Delete PI dialog has always used ("17 sprints across 4 teams are in this
  PI"). The row says the same thing now, and an empty PI reads "No sprints yet" rather than
  "0 sprints across 0 teams". Nothing else on the row moved.
- **`moveInList` restores focus after the re-render**, or moving something with the keyboard
  loses your place entirely — the row is rebuilt, so the focused button no longer exists. If
  it lands disabled, focus goes to its opposite number on the same row.
- The dialog tests render a fixture through `withState` + `renderManage()` rather than
  reading whatever the app holds: the suite boots an app with no teams, and these tables are
  only written when `renderManage` runs. It writes nothing to storage, so the read-only
  promise still holds — and the last test puts the app's own rows back.

## The Settings-Window Furniture Is Shared, Rules Included (2026-09-02)

`.manage-head`, `.manage-note`, `.grid.two` and — since 2026-09-02 — **`.manage-sec`** are one
set of parts used by the four windows that hold app-wide settings: Flow Metrics' *Settings* and
*Teams, ARTs & Stages*, this app's *Targets*, and Golf Handicap's *League Handicap*.

- **`.manage-sec` is a section and the rule that ends it:** `border-top: 1px solid
  var(--border-strong)`, `padding-top`/`margin-top` from `--sp-7`, and `:first-of-type` takes
  the spacing without the rule — above the first section is the window's own heading or the
  sentence describing the whole window, and a line under either reads as the end of a section
  rather than the start of one.
- **It came from Flow Metrics**, whose Settings window Charles read as "big and a bit hard to
  read": six unrelated settings under two headings. This window has three short sections and
  would not have earned the complaint alone; it took the rule the same day because the four
  windows are read as one screen, and a divider in some of them is drift rather than design.
- **The spacing lives on the section, not on the heading row.** Every heading row carried its
  own inline `margin-top` (16, 18 or 20px depending on the window) until this change.
- **`Teams, ARTs & PIs` took it the same week, and was very nearly missed.** The first pass
  did Targets alone, on the settings-window argument above, which left the window Flow
  Metrics names in its own markup as the design lead for its Teams window as the one without
  the rule the copy had. Its three headings were bare `<strong style="font-size:…">` in rows
  carrying `margin-top:20px`, and its two notes were `.sub.muted` with the size and margin
  written out inline; they are `.manage-head` and `.manage-note` now, which also lifts the
  notes from `--text-muted` to the family's `--text-secondary`. **The rule is not "the
  settings windows" but "the windows the two apps are read side by side"** — a section
  heading in one and not the other is drift wherever it sits. Pinned as the whole list, so a
  fourth thing to manage has to say which section it is.
- No new colour, no fill, no shadow (pack rule 14), and `.manage-head` itself is unchanged, so
  nothing here touches the theme pack.

## Fields, Dialogs and Scroll Boxes (2026-08-20)

- **Every modal opens through `openModal(dlg)`, never `showModal()` directly.**
  `showModal()` runs the spec's dialog focusing steps — the `autofocus` element, or failing
  that the FIRST FOCUSABLE one — and there is no `autofocus` anywhere in the file, so which
  dialogs raised a phone's keyboard was decided entirely by which happened to open with a
  text box — Adjust capacity did, because its markup opens on the
  availability box; Back up, Share and the sprint form (whose first control is the Paste
  from Jira disclosure) did not. The keyboard then covers half the dialog before it has been read. On a
  COARSE pointer `openModal` moves focus off the field and onto the dialog itself.
  - **Focus still goes INTO the dialog** — that part is not optional, or a keyboard or
    screen-reader user is stranded outside a thing covering the page. The CONTAINER is what
    the ARIA practices offer for this case: every dialog here carries `aria-labelledby`, so
    it announces itself, and Tab reaches the first field. `tabIndex` is set at open rather
    than in the markup — a dialog is a focus target only for that moment.
  - **`(pointer: coarse)`, NOT a width breakpoint.** The keyboard is a fact about touch, not
    width: a desktop window dragged narrow keeps its click-and-type, a wide tablet is spared.
  - **`raisesKeyboard(el)` is pure and pinned** over `{tagName, type}`, so the type list is a
    test rather than a rediscovery. It is a no-op when the browser landed on a button, a
    picker or a disclosure, which is what leaves those dialogs exactly as they were.
  - A dialog that genuinely wants the keyboard needs no special case: call `openModal` and
    then focus the field yourself afterwards, which simply wins.
  Ported from Money Map, and mirrored across the app family the same afternoon.
- **A box you land on has its contents SELECTED**, so typing replaces the value
  rather than running on to the end of it — one delegated `focusin` listener
  (`SELECT_ON_FOCUS`), which bubbles where `focus` does not, so it covers every
  field including the ones built a moment before a dialog is shown, with nothing
  to remember when adding one. Ported from Money Map 2026-08-20 and now in every
  app in the family. Four things it must keep doing:
  - **The type list is a WHITELIST.** A date, a checkbox, a range and a file
    picker have no text for `select()` to take, and a type nobody has thought
    about is left alone rather than silently swept in.
  - **A TEXTAREA is never touched** — the `INPUT` check does it. A box you write
    several lines into should not be one keystroke from gone, and unlike a
    mistyped figure there is nothing on screen to retype it from.
  - **`data-keep-caret` is the by-hand opt-out for a single-line PROSE field**,
    which the TEXTAREA rule cannot catch. Nothing here carries it — the Jira box is a
    TEXTAREA and everything else is a figure — but it is wired so the next one has it.
  - **The one-shot `mouseup` guard is load-bearing, and only for a POINTER-driven
    focus.** A click focuses on mousedown and then places the caret on mouseup,
    which collapses the selection made a moment earlier: without it the feature
    works from the keyboard and looks broken with a mouse, which is how everybody
    would meet it. A `{once:true}` listener left hanging after a Tab would sit
    there and eat the caret placement of a later, deliberate click — hence
    `focusFromPointer`, set on a capturing `pointerdown`. Clicking a second time
    places the caret normally (the field is focused by then, so no focusin
    fires), and that is the way back in for editing rather than replacing.
  It does not fight `openModal`: on a touch screen focus goes to the dialog, so
  nothing is selected until you tap a field.
- **A horizontal scroll box must carry `position: relative`.** `overflow-x: auto` is the
  whole design for `.tablewrap`, and the Compare Teams comparison table is what made it visible — content too wide for a phone scrolls inside its card and the
  page stays the width of the screen. On iOS that only half worked: WebKit clipped it on
  screen but still counted its full width in the DOCUMENT's scrollable area, so the page
  itself became horizontally scrollable into a band of nothing. Measured on iOS 27 at a
  402px viewport: `documentElement.scrollWidth` 906 against a 402px body. `position:
  relative` is what fixes it and nothing weaker does — a stacking context alone
  (`isolation: isolate`) leaves it at 906, and so does spelling out `overflow-y`;
  `contain: paint` works but takes the containing block for fixed descendants with it.
  Chrome and Firefox were always right here, so it is only ever visible on a phone.
- **Date fields are `appearance: none`, and that lives in `theme.css`, not here.** WebKit
  ignores an author `box-sizing` on a natively drawn control, so `width: 100%` on a date
  input meant the column PLUS its padding and border and the box hung over its neighbour.
  See rule 11 in the theme pack's CLAUDE.md; don't re-fix it locally.

## The Privacy Page Carries the Family Footer (2026-08-21)

Every public page in this account carries the same three things at the foot: the privacy
policy, the repo under the label **How it works**, and the authorship line. The APP's footer
has had all three for a while. `privacy.html` had **none** of them until now — and it is a
public page reached by a link in that very footer, so anybody who followed it landed on a
document with no way back to the thing it documents and no statement of who wrote it. The
lottery site's privacy page had grown the footer first and was the only one; the other four
were brought into line together rather than one at a time, because a convention held by one
page out of five is not a convention.

- **No privacy link in it**, unlike the app's own footer — you are standing on that page. That
  absence is asserted, not just omitted: the test checks there is no `href="privacy.html"`.
- **The authorship line is the app's own, verbatim**, which means the two-link form here: *independent personal project* points at **NOTICE**
  (who owns it) and *MIT licensed* points at **LICENSE** (the terms). Getting those two the
  wrong way round is the mistake the app's own footer comment records.
- `.foot` and `.foot a` are copied from the lottery page's stylesheet unchanged, so all five
  read identically. Muted, inheriting the link colour — provenance at the foot of a document
  rather than something to click on the way in.
- **Pinned in `tests.html`**, so the next page added to this repo cannot quietly ship without
  it.
- **It is a real `<footer>`, and the policy is in a real `<main>`** (2026-08-21, a day after
  the footer itself). A styled `<p>` is not a landmark, and a page whose only landmark is
  contentinfo is worse than one with none — the actual policy would sit in no landmark at all.
  So both went in together.
  - **`</main>` closes BEFORE the `<footer>`, and that ordering is the whole thing.** A
    `<footer>` nested inside `main`, `article` or `section` is **not** contentinfo — it is a
    plain footer for that section. So `.wrap` stays an ordinary `<div>` rather than becoming
    the `<main>`, which would have swallowed the footer and left the page with no contentinfo
    at all while looking correct in the source. A test asserts the ORDER, not just the tags.
  - The back link stays outside `<main>` — it is navigation, not the document.
  - **The tests strip HTML comments and match the footer by its class**, because the notes
    beside both elements name them in prose and one of those notes lives in the `<style>`
    block, which an HTML-comment strip does not reach. Without both, a page that had lost the
    element and kept the comment explaining it would still pass. That is not hypothetical —
    it is how the first version of this test failed.
  - **The strip is a LOOP, not a single `.replace()`** (2026-08-21, `stripHtmlComments`).
    One pass over a multi-character delimiter can leave a NEW opener behind that the pass has
    already gone past, so a single pass is only as good as the input is well-formed — CodeQL's
    `js/incomplete-multi-character-sanitization` flagged exactly this line, and it was open on
    five of the nine public repos at once. Nothing here renders what it strips, so there was
    no vulnerability; the reason to fix it is that a helper that can be fooled about what is
    commented out is one that can miss a live off-origin script, which is what these suites
    exist to catch. Same helper, same wording, in every sibling repo's suite.
  - `.foot` sets `margin`, not `margin-top`, so the rule no longer depends on which element
    carries it: a `<p>` brought a UA bottom margin with it and a `<footer>` does not.

- **`<main>` opens ABOVE the tab strip (2026-08-21), not around the panel alone.** Two things
  were wrong with the old placement: the tabs were in no landmark (axe-core's `region` rule),
  and the skip link jumped straight past them — a keyboard user who took "Skip to content"
  had the whole tab row behind them and could only reach it by shift-tabbing back. The tabs
  and the panel they drive are one widget, so the landmark goes round both, and `#shareBar`
  comes inside with them because it describes what is on screen. `role="tabpanel"` still goes
  on the inner div and NEVER on `<main>`: putting a role on an element is its role, and it
  would silently replace the landmark. Every page here now passes axe-core at WCAG 2.1 A/AA
  plus best-practice, in all four themes, with data loaded, on every tab and with every
  header dialog open.

- **The privacy page's back link lives in a `<nav>` (2026-08-21).** It stays OUTSIDE `<main>`
  — it is navigation, not the document — but "outside main" is not the same as "outside every
  landmark", which is where it sat: axe-core's `region` rule found it on all six privacy pages
  at once. The `<nav>` carries an `aria-label` naming where it goes back to.
- **The base field rule's TYPE LIST is the theme pack's own** (2026-08-22). `select,
  textarea, input[type=text|number|date|month|search|tel|url|email|password]` — the same
  list the pack enumerates in its coarse-pointer rule. It has to stay a whitelist (a
  checkbox handed a surface, a border and padding stops being a checkbox), but a whitelist
  grown by hand is a field that arrives silently UNSTYLED, wearing the browser's own box
  beside fields wearing the theme's. Nothing fails and nothing logs. It has happened twice
  in this family in opposite directions: Flow Metrics was missing `date`, Golf Handicap was
  missing `search`. Borrowing the pack's list is what stops it being a fresh discovery each
  time, since it answers the same question ("is this a thing you type into?") in the one
  place that should. **Adding a type to one means adding it to the other.**
  `input[type=search]` also takes `appearance: none`, like the pack's date fields, because
  the native inset shape ignores the border and radius — that removes Chromium's native ×
  too, so a search box with no other way to clear itself should offer one.
  **Sprint Predictability is the design lead**; Flow Metrics, Money Map and Golf Handicap
  carry the identical list. PAPTrack and the dashboard style fields by CONTAINER
  (`.field input`) and by class (`.ctl`) instead — element selectors, which have no
  equivalent gap — and the lottery pages style their few fields per component. Those three
  are deliberately NOT converted; don't "finish the job" by giving them a type list.
- **A BOX IS AS WIDE AS WHAT GOES IN IT (2026-08-27).** A width is right for a name or a
  pasted export, whose length nobody can predict, and wrong for a number, where the length is
  written in the markup two attributes away: the eight boxes in Targets were 523px each for a
  percentage that cannot exceed 400, and a story-point count in the sprint form was 249px.
  `input[type=number]` takes `calc(var(--digits, 4) * 1ch + 38px)`; **`--digits` IS the `max`
  attribute, in digits, and belongs on the same tag** — the two are one fact and splitting them
  is how they drift. The 38px is padding, border and the spinner no engine reports a width for.
  The **default of 4** is the right answer for the boxes that genuinely have no maximum (a
  sprint's committed points is a number this app does not bound); a box that DOES declare a
  `max` must declare digits enough for it, and where a **placeholder** is wider than the digits
  — `then` and `now` on the team-size boxes, `e.g. 120` on the backlog total — the digits answer
  to the placeholder instead. A `max` written as `${CONST}` must take its digits from the same
  constant. The suite checks all of that against the source, and it caught a deliberately
  narrowed box on the first run.
  It replaced five hand-set inline widths (110/80/76/70/64px), each set by eye and none checked
  against its own box — which is exactly how Flow Metrics ended up with a target box four
  characters wide holding a five-character number. `input[type=date]` gets a figure of its own
  (170px), deliberately generous: what it holds is the LOCALE's rendering of a date.
  **`width: 100%` on a container rule beats the shared one**, so `.grid.two > div > input` and
  `.grid-fields > div > input` exclude number and date by `:not([type=number]):not([type=date])`
  rather than the shared rule being given more specificity — the claim those rules make ("a box
  for words of unknown length fills its cell") is worth keeping. `.grid-fields` keeps handing
  every input its `margin-top: auto` and `height: 40px`, which are what hold a row of mixed
  fields on one line; only the width and the 260px ceiling are excluded.
  **Sprint Predictability is the design lead**, and Flow Metrics carries the same rule.
- **Decorative glyphs on buttons are `aria-hidden` everywhere, not just in the header.** The
  header row got the treatment on 2026-08-21 and the rest of the app did not, so a screen
  reader still read "downwards black arrow, Export JSON" in every dialog. Around 50 buttons
  across the family were wrapped in the same pass. The sync button was the exception that
  proved it (until it went with sync on 2026-08-20): its label was rewritten with
  `textContent` as the state changed, so a span there would have been blown away — it carried
  an `aria-label`, re-stated in every branch of its `updateUI()` so it could never be left
  describing the previous state. The pattern still applies to any control whose label is
  rewritten with `textContent`.

## Six Fixes From the 2026-09-01 Audit

A bug audit of the three work apps on 2026-09-01 (three auditors, each finding
reproduced headless before it was reported) found six here that the suite did not
cover. Each has a test now, proven to fail first by reverting the fix.

- **The PI picker rebuilds the number list BEFORE projecting dates (fix 1).** `#f_pi` had two `change` listeners: the shared prefill one (registered first, for `f_pi`
  and `f_num`) and the list-rebuild one. So the dates were projected for the number the form
  was still showing, and only then did the rebuild find that number had no slot in the new PI
  and drop the picker to Sprint 1 — without projecting again. A new sprint 7 moved into an
  empty PI saved as Sprint 1 with slot 7's dates and status `planned`. The prefill listener is
  now `f_num`-only and the PI listener rebuilds, then calls `maybePrefillCarriedIn()` and
  `maybePrefillDates()` itself. Order of registration was the whole bug.

- **A section total is a cell that is nothing but the total (fix 2).** `JIRA_TOTAL` was tested on every line before `JIRA_KEY`, and a match `continue`d — so a
  row summarised "Show story points (3) on the epic card" overwrote the section's claimed total
  with 3 and vanished as a row; the checksum fired with a false message and "Use These Numbers"
  would save the wrong figures. `totalCell(line)` now returns a total only from a line that
  does not start with a key AND has a whole tab-cell matching `JIRA_TOTAL_CELL` (`^…$`): the
  header's last cell in a tabbed copy, a line of its own in a flattened one. Section-header
  lines keep the old loose match — they are identified by `JIRA_SECTIONS` first.

- **A PI window never carries pre-PI history (fix 3).** `trimShareSprints` ranked a PI-less sprint -1 and kept `at(s) > newest - n`, so "the last
  2 PIs" over a one-PI history shipped every pre-PI sprint while `shareScopeNote` said "This
  link holds the last 2 PIs" and `shareRangeNote` said "earlier history isn't included". In the
  one feature whose point is limiting what leaves the browser, the control promised less than
  it sent. Pre-PI sprints are dropped under a PI scope now; `newest < 0` (no PI at all) still
  means everything. Sprint scopes are unchanged — they count sprints.

- **A sprint number a PI has no slot for reads as Sprint 1 (fix 4).** `activeSprintNum` is kept across a team switch on purpose (a working position), but a
  PI-less team's sprint 16 carried onto a PI'd team gave three answers at once: the picker
  showed Sprint 1 (no option matched), the empty card said "no data for sprint 16 of PI
  2026.3", and Add Sprint opened a form titled Sprint 16 with Sprint 1 selected
  (`editing.sprintNumber` 16, save writes S1). `renderSprintView` clamps the number it READS
  to `SPRINTS_PER_PI` when a PI is set and does not save it — the stored position stays the
  reader's and follows them back to the PI-less team.

- **A blank state has nothing for the boot scrub to repair (fix 5).** `blankState()` states the six typed forecast fields as `''` and `forecastTypedOn` as
  null; `keepKnown` read `''` as `num` → 0 (a repair) and dropped the null tribool (a repair),
  and `adoptState()` then reinstated the null from `blankState()`, so the next boot counted it
  again: `pruned` was 7 on a clean first boot and 1 for ever after, and the "one save at boot,
  only when something was actually removed or repaired" comment was false. `numOrBlank` keeps
  `''` as `''`; a null tribool skips the count. Sprint figures stay `num` — there `''` → 0 is
  the documented "Blank Means Zero".

- **The share range is pinned at the boundary (fix 6).** `range` was in `TOP` (allowed through) but, unlike `label` and `sharedAt` right below it,
  never typed: `{ kind: 'pi', n: '1e400' }` rendered "It holds the last Infinity PIs". Only
  `kind`/`n` are ever read, numerically, so no script could ride in — but a value the banner
  prints is a value this pass pins. Now: kind must be `pi` or `sprint`, `n` is floored and
  clamped to `[1, MAX_SPRINT_NO]`, a stray key goes, and a non-object or unknown kind is
  dropped (the banner then says nothing about a window). A well-formed range counts no repair.

## Fixes From the 2026-09-03 Audit

A second audit on 2026-09-03 — the day the pin, the scrolling tab row and the
full-screen stepping shipped — found six here. Each has a test in a group named
"(2026-09-03 audit)", proven to fail first against the unfixed index.html; the
ones that need a real size boot their own 1280x900 frame through `inFrame()`.

- **A step never leaves the keyboard on the page underneath (fix 1).** Opening with ⤢
  focuses that ⤢; `maxiStep()` then moved its card back into `.wrap`, which is inert while
  the window is up, so the browser dropped focus onto `<body>` and the next arrow press went
  to nothing. The rule, in one sentence: a step lands focus on the arrow that pressed it, or
  on the new card's ⤢, never on the page underneath. The arrows live in the overlay and are
  never moved, so one holding focus keeps it; `maxiStep()` now only acts when the active
  element is gone or outside `#chartMaxi`, and focuses the new card's ⤢ with `preventScroll`
  like every other focus() here. Family-wide: Flow Metrics and Money Map had the same fault.
