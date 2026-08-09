# Sprint Predictability · Charlie’s Epic Sprint Planner

A sprint predictability tracker for Scrum Masters. Record what each team committed to,
what they actually finished, and what changed mid-sprint — the app works out commitment
completion, break-in, carryover and velocity, and flags each one against your targets.

**Live:** https://eagleadams86.github.io/sprint-velocity/

Built for Scrum Masters running several teams on a SAFe-style cadence: six sprints to a
Program Increment, with sprint 6 reserved for innovation and planning.

One of a pair: [Flow Metrics](https://eagleadams86.github.io/team-dashboard/) (the
`team-dashboard` repo — the app was renamed on screen only) is the
sibling app for weekly flow metrics, sharing this app's look and behaviour — the same sticky
header, button tabs, tiles, ⓘ help dialogs, theme picker and footer. **Each app's header
carries a link to the other**, next to the title — one click either way, from anywhere on
the page — and both still cross-link at the foot of the page. If a chrome rule changes in
one app, it should change in the other too.

---

## What it tracks

Per team, per sprint:

| Field | Meaning |
|---|---|
| **Points committed** | What the team signed up for at sprint planning |
| **Committed points completed** | How much of *that* commitment they finished |
| **Total points completed** | Everything finished, including work that arrived mid-sprint |
| **Added after start** | Break-in work |
| **Removed after start** | Work pulled back out |
| **Carried in** | Unfinished points inherited from the previous sprint |
| **Carried out** | Committed points not finished, rolling into the next sprint |
| **Brought in, then removed** | Work that arrived mid-sprint and left again — counted in neither break-in nor removed |

Plus free-text notes on **why** work was added, removed, or carried over — the context you
want in front of you at the retro, not three sprints later when nobody remembers. They sit
behind a **Why? (optional)** heading in the sprint form, folded away so the numbers and the
Save button fit on one screen; open it when you want it. A sprint that already has notes opens
with it unfolded, so nothing hides writing you can't see is there.

## The metrics

All four percentages use **committed points** as the denominator:

```
Commitment completion = committed points completed / points committed
Break-in %            = points added   / points committed
Removed %             = points removed / points committed
Carryover %           = points carried out / points committed
Velocity              = total points completed
```

### Targets

| | 🟢 Green | 🟡 Yellow | 🔴 Red |
|---|---|---|---|
| Commitment completion | ≥ 85% | 75–84% | < 75% |
| Break-in / Removed / Carryover | ≤ 15% | 16–20% | > 20% |

Colour is never the only signal — every figure also carries a ✓ / ! / ✕ glyph and a
screen-reader status, so the app is readable without colour vision.

The colours now pull their weight too. As of 3 August 2026 the shared theme pack's gate
checks the three status colours against **each other** under deuteranopia and protanopia,
not just against their backgrounds — previously the Sepia theme rendered "watch" and "off
target" in two colours that simulate to an identical shade for a red-green colourblind
reader, so the glyph was doing all the work on its own. The colours stay **RAG** — red, amber
and green, the convention every Scrum Master reads by — but "on target" is a green leaned
toward blue-green rather than a pure one, because red-green deficiency flattens the red-green
axis and a leaf green sits right on top of the red. All four themes now clear a CIE ΔE of 18
between the three figures.

On the light themes the status figures also sit on a **tinted panel** rather than carrying the
colour in a thin rule and the digits alone. Contrast rules force every status colour dark on a
pale card, and at that size three dark colours all read as near-black — the first version of
this change was flagged by colour-normal reviewers as well as a colourblind one. A filled panel
gives the eye a large area of the hue instead.

The **All teams** bar chart follows the same rule: each bar is drawn like the pill in the table
beneath it — the status tint as the fill, the status colour as the outline — rather than as a
solid block of the status colour. A solid bar had exactly the problem the tinted panels fixed,
only larger: on Light and Sepia the three bars rendered olive, maroon and bottle-green, and you
were being asked to tell three near-blacks apart across the width of a chart.

**Every other bar chart is drawn that way too.** A bar's area is a tint of its series colour —
the colour mixed most of the way toward the card behind it — with the full-strength colour on
the outline and in the texture stripes. The same contrast rule that darkens the status colours
darkens the series colours, so on the cream Sepia and white Light cards the charts used to read
as slabs of near-black sitting on a pale page. Moving the colour to the edge keeps the contrast
where the eye reads the boundary and gives the large area back to the card. Because the tint is
mixed toward the *card* and not toward white, the same rule works on the dark themes — there the
fill goes quiet and the outline is the bright thing.

Every tile on the Sprint, Current PI and Rolling 5 views has a small **ⓘ** button in its
top-right corner. Click it for a plain-English definition of that figure — what it means,
how it's worked out, and the target it's being judged against. It works in a shared
read-only link too, so someone you send figures to can look up a metric without asking.

A sprint with nothing committed shows `—` rather than 0% — there's no denominator — and is
left out of averages instead of dragging them down. Every other empty figure counts as 0.

Percentages display as whole numbers, except when rounding would land on the wrong side of
a target — 33 of 39 points is 84.6%, so it shows as `84.6%` in yellow rather than as `85%`
in yellow, which would look like a bug. That's the only time you'll see a decimal.

## Filling a sprint from Jira

Rather than retyping seven numbers, open the sprint's **Sprint Report** in Jira, copy the
whole thing, and paste it into **📋 Paste from Jira** at the top of the sprint form.

It works out every figure and shows you exactly how before filling anything in:

| Field | Where it comes from |
|---|---|
| Points committed | every issue **not** marked `*` — including ones later removed, since they were in the sprint when it started |
| Committed points completed | completed issues not marked `*` |
| Total points completed | the whole Completed Issues section |
| Added after start | every issue marked `*` (Jira's "added to sprint after start time") |
| Removed after start | the Issues Removed From Sprint section, minus anything that arrived mid-sprint and left again |
| Brought in, then removed | issues marked `*` that ended up removed — counted in neither break-in nor removed |
| Carried out | the Issues Not Completed section — *all* unfinished work |
| Carried in | not in the report; taken from the previous sprint (see below) |

Two things make this trustworthy rather than a guess. Jira prints its own **Story Points (N)**
total in each section header, so the app cross-checks its reading against Jira's and tells
you if they disagree. And issues with no estimate (`-`) count as zero rather than being
skipped.

### Stories re-sized mid-sprint

When an estimate changes during a sprint, Jira shows both — `8 → 2` on the row, and
`Story Points (21 → 15)` in the section header. The app reads both sides, and exactly one
figure uses the earlier one:

- **Points committed** takes the sizes **as they were at sprint start**. It records what the
  team signed up for, and re-sizing later can't rewrite that.
- **Everything else** — both completed figures, added, removed and carried out — takes the
  **current** sizes, because those are what the work turned out to be.

The preview tells you how many issues were re-sized and by how much; heavy re-sizing usually
means the work wasn't well understood at planning, which is worth raising at the retro.

Because both sides are parsed, the cross-check against Jira's totals runs on both too, so a
mis-read has two independent ways to show itself.

**Commitment completion can exceed 100%.** With the commitment fixed at sprint-start sizes
and delivery counted at current ones, a team that re-sizes work upward mid-sprint really did
deliver more than it committed to. That's shown as-is rather than capped, and the charts
scale to fit it.

**Work pulled in mid-sprint and then pulled back out nets to nothing.** It never joined the
commitment, and removing it didn't reduce the commitment either, so counting it as both
break-in *and* removed would penalise the team twice for churn that left no trace. It's
recorded on its own instead, and the Sprint view's *Where the points went* card says so when
it happened.

**Carried out is all unfinished work**, not `committed − completed`. If work broke in
mid-sprint and didn't finish, it still rolls into the next sprint, so it's counted — which
means carryover can be larger than the shortfall against the commitment.

Because of that, the *Where the points went* Committed bar shows only the carried-out points
that came **from the commitment**, and the card says so whenever that's less than the full
carryover figure on the tile. Its dropped slice is the removed points, capped at the
shortfall. Stacking the whole carryover figure into that bar used to overstate carryover and
leave "dropped" as a residual, which under-reported removed work — a sprint that dropped six
points read as one.

Nothing is saved by pasting itself — reading the report only shows you the preview. Pressing
**Use these numbers** fills the boxes **and saves the sprint there and then**, so a paste you
were happy with can't be lost by closing the form. Your "why" notes are never touched. If the
paste can't be read, it says so and shows what it did find rather than filling in zeros.

That save is undoable, **by the Cancel button and nothing else**. While it's outstanding the
button reads **Cancel & Undo Save**, and pressing it puts your data back exactly as it was,
right down to the figures the sprint already held. Press **Save sprint** instead and the
numbers stay, along with anything else you typed while you were in there.

Escape and clicking outside the form just close it and **keep** the save. Those are the two
things you hit by accident, and the whole point of saving at **Use these numbers** is that
closing the form can't cost you the paste — so undoing is left to the button you have to mean
to press.

If you're pasting over a sprint that has already finished and has real figures in it, the
usual "saving will change…" confirmation appears at **Use these numbers** rather than at Save
sprint, listing each figure that would change. Say no and the boxes are still filled in for
you to look at — nothing is saved until you press Save sprint yourself.

Both common paste shapes work — tab-separated rows and one-cell-per-line — since browsers
differ in how they copy tables. Which shape you've pasted is decided on a count of the
rows, so a stray issue key that copied onto a line of its own can't make an ordinary
report look like the other kind. Estimates are read from the rightmost cell holding an
actual figure, so a spare `-` in a column after the points can't mask them; an issue with
genuinely no estimate still reads as 0.

## Recording a sprint before it's over

You can create a sprint at planning time and top it up as it runs. An unfinished sprint is
**shown but never counted** — it stays out of every average, the rolling window, the PI
figures and the capacity target until it's done, so a sprint with a commitment and no
results yet doesn't read as a 0% disaster.

Status comes from the dates and looks after itself:

| | |
|---|---|
| Start date hasn't arrived | **Planned** |
| Today is on or before the end date | **In progress** |
| End date has passed | **Complete** |
| No dates at all | **Complete** |

A sprint with no dates counts as complete, so everything recorded before this existed keeps
working exactly as it did. The **Status** field on the sprint form overrides the dates
either way — useful if your team doesn't record dates, or closes a sprint late. An
overridden sprint stops looking after itself, and the form says so.

While a sprint is running the Sprint view swaps the result tiles for a progress read: points
done so far, **pace** (how much of the commitment is done against how much of the sprint has
elapsed — a rough guide, since work lands in lumps near the end), and break-in and removed
flagged against the usual 15% target, because those *are* meaningful mid-sprint. The
capacity target points at the running sprint and sits next to what the team actually
committed, so an over-commitment can be descoped now rather than carried over later.

Nothing is excluded silently — every view names what it's leaving out.

### Counting a sprint that's still running

**Count sprints that are still running**, on the Rolling 5 and All teams views, opts in-flight
sprints into every figure — the rolling window, the PI totals, the team comparison and the
capacity target. It's off by default, because the numbers genuinely aren't final.

It's for the last day or two of a sprint, when you're planning the next one and today's
provisional numbers beat last sprint's stale ones. When it's on, every view says so, and the
capacity target stops aiming at the running sprint and points at the one after it — once a
sprint is being counted as data, it isn't the sprint you're planning any more.

Sprints that haven't started are never counted either way; they have no results at all.

### Overwriting a finished sprint

Saving a sprint that has already finished asks first, listing exactly what would change:

```
PI 2026.3 · S3 finished on 14 Jul 2026 and already has data.

Saving will change:
  • Points committed: 38 → 99
  • Total points completed: 36 → 41

Save these changes?
```

It's there to catch the real accident — picking the wrong sprint from the dropdown, pasting
a Jira report over it and saving. Legitimate corrections go through with one click.

It stays quiet unless it needs to speak: no prompt for a sprint that's still running or
hasn't started, none for a new sprint in an empty slot, none if you open an old sprint and
change nothing, and none for adding a retro note. Only a recorded figure actually changing —
or the sprint being moved to another slot — triggers it.

### Dates fill themselves

Key the dates once and the rest of the programme follows. Sprints run on a fixed rhythm, so
a new sprint form works out its own start and end from a sprint that already has dates,
counting slots forward at the team's cadence — across PI boundaries included, so sprint 1 of
the next PI lands where it should.

| Sprint 1 | The next sprint gets |
|---|---|
| Mon 6 Jul → Fri 17 Jul | Mon 20 Jul → Fri 31 Jul |
| Mon 6 Jul → Sun 19 Jul | Mon 20 Jul → Sun 2 Aug |

The cadence is worked out from your dates, not assumed. With one dated sprint to go on, its
length is rounded to whole weeks — a Monday-to-Friday sprint is twelve days long but comes
round every fourteen, and a fortnightly team stays fortnightly. Once two sprints have dates,
the real gap between them is measured instead, so a team with a break between sprints, or a
three-week cadence, self-corrects.

The empty rows on the **Current PI** table show where each remaining sprint falls
(`No data — click to add · scheduled 17 Aug – 28 Aug`), so the whole PI is laid out before
any of it is filled in.

Like carried-in, it only ever fills empty boxes, and only for a sprint you haven't saved
yet. A note under the fields says which sprint the dates came from. Type your own and they
stick — including through a change of sprint number. **Sprints already recorded without
dates are left alone**, deliberately: dating them would flip them out of "complete" and pull
real history out of your averages.

### Carried in fills itself

Whenever you open a sprint that has no carried-in figure yet, it's filled with what the
previous sprint carried out — crossing a PI boundary if you're on sprint 1. A note under the
fields says which sprint it came from, and it never overwrites a number you've already
entered or typed.

### Blank means zero

An empty box saves as 0 — most sprint data arrives from the Jira paste, where a figure that
isn't there genuinely is nothing, and a `—` where the honest answer is "0 removed" just looks
like missing data.

The one figure that still shows `—` is a percentage with nothing committed: there's no
denominator to divide by, so it can't be a number, and those sprints stay out of averages
rather than dragging them down.

## The four views

- **Sprint** — one sprint in detail: the RAG tiles, a breakdown of where the committed
  points actually went, and the notes.
- **Current PI** — all six sprints of a PI, with PI totals and a sprint-by-sprint chart.
- **Rolling 5** — the last five sprints for a team, crossing PI boundaries. Velocity and
  commitment completion on one chart — with a dashed **velocity trend line** fitted by
  ordinary least squares, the same treatment every chart in the sibling Team Dashboard app
  carries — and an instability chart plotting break-in, removed and carryover against
  shaded 15% / 20% threshold bands.
- **All teams** — every team's rolling averages side by side, plus each team's next-sprint
  target in one column, so the one that needs attention is obvious. It carries **two
  comparison tables**, the same sprints through two different averages — see below.

A view is only offered once there's something in it. **All teams** appears when you have a
second team; **Current PI** and **Rolling 5** appear once the team you're on has a recorded
sprint, and step aside again if you switch to a team you haven't recorded anything for. With
no teams at all there are no tabs — just the welcome card. If the view you were on goes away,
you land back on **Sprint**.

## The two comparison tables

The All teams view shows the same rolling window twice, because there are two honest ways
to average a percentage and they answer different questions.

**Comparison 1 — average of sprints.** Each sprint's own percentage is worked out first,
then those percentages are averaged. Every sprint counts equally whatever its size.

**Comparison 2 — pooled totals.** Every point is added into one total and the percentage
taken once at the end. A bigger sprint pulls harder than a small one.

A team with two sprints — 6 of 9 committed points done, then 5 of 14 — scores **51%** by
the first method (67% and 36%, averaged) and **48%** by the second (11 of 23). Neither is
wrong; the first describes the typical sprint, the second describes the body of work.

| | Comparison 1 | Comparison 2 |
|---|---|---|
| Method | Average of each sprint's % | One pooled total, divided once |
| Weights sprints by size | No | Yes |
| Best for | Coaching a team — the habit | Reporting upward — the actual work |
| Matches the Agile Operations Dashboard | No | **Yes** |

**Comparison 2 is the one that reconciles with the Agile Operations Dashboard**, which
pools throughout.

Both tables end in an **All teams** row, and each applies its own table's method across every
team at once rather than averaging the rows above it — so neither row equals the mean of the
column it sits under. Comparison 1 counts every sprint from every team as one equal sprint, so
a team with six of them pulls six times as hard as a team with one; Comparison 2 pools every
point, exactly as the dashboard's Total does. The single exception is Comparison 1's
**next sprint target**: that's points rather than a rate, so the team targets simply add up.

**Current PI** and **Rolling 5** both put the two methods side by side at the foot of
their *The numbers* table, as a pair of summary rows:

| View | Average-of-sprints row | Pooled row (matches the dashboard) |
|---|---|---|
| Current PI | **Average per sprint** | **PI total** |
| Rolling 5 | **Average per sprint** | **Pooled total** |

On both, the pooled row's committed and delivered figures are **totals**, while the
average row's are **per-sprint means** — which is what makes the arithmetic visible.
Every summary row carries an ⓘ explaining its own method and naming the other.

The tiles at the top of Rolling 5 are all averages of sprints. Current PI's tiles are a
mix: *PI commitment completion* is pooled, *Average per sprint* is the average-of-sprints
figure, and a wide gap between them means one sprint is skewing the total.

Comparison 2 also carries **Actual complete** — everything delivered, break-in work
included, against what was committed. It goes above 100% when a team finished more than it
signed up for, which says throughput was high, not that the plan held.

## Target capacity for the next sprint

The Rolling 5 view turns the history into a number you can take into planning: **how many
points this team should commit to next sprint**.

It's the team's **average committed points completed** over the rolling window — the amount
of commitment they have actually been finishing, sprint after sprint.

The tempting number is average *velocity*, and it's the wrong one. Velocity includes the
break-in work that turns up mid-sprint. Commit to that figure and you've booked out the
very capacity the break-in is going to consume, so the team starts every sprint already
over-committed. That gap is how a fast team still misses its commitment every time.

The card also splits the total into what's **already carried over** from last sprint and
how much **new work** that leaves to pull off the backlog, and shows the recent range so
you can see how much faith the number deserves. When the sprint it's aiming at is already
running and has a commitment recorded, it swaps the new-work figure for a comparison
against what the team actually signed up for — there's still time to descope. A running
sprint whose commitment hasn't been entered yet keeps the forecast, since 0 committed is
an unanswered question rather than a small commitment. It warns you when there are fewer than
three sprints of history, when the team's delivery swings by more than 30%, and when the
next sprint up is the IP sprint.

It's a starting point for the planning conversation, not a quota — adjust it for leave,
holidays and whatever else the team knows about that the numbers don't.

### Sprint 6 and the rolling average

Sprint 6 is the innovation & planning sprint, so it's **excluded from the rolling average
by default** — an IP sprint isn't meant to look like a delivery sprint, and including it
makes every team look worse than they are. There's a toggle on the Rolling 5 and All teams
views if you'd rather count it. When it's excluded the window simply reaches further back,
so you still get five sprints.

## Themes

Four, shared with every other app in this family and listed alphabetically in the header
dropdown: Dark, Light, **Midnight** (deep indigo/navy — the default) and Sepia. (Forest,
Solarized and Synthwave were retired in August 2026; if you had one selected you'll now
see Midnight.) Your choice is remembered
in this browser and isn't part of your data, so it doesn't sync between devices and a
shared link never carries the sender's theme.

Every one of them meets WCAG AA contrast on every piece of text — the figures, the RAG
pills, the table captions — against each of the three backgrounds it can sit on. Each
series keeps the same hue throughout — committed grey, completed blue, velocity teal,
break-in amber, removed violet, carryover red — so a chart reads the same way whichever
palette you're in. Charts re-render on a switch, because their colours are resolved when
they're built.

**Which series is which never depends on the colour.** Every bar carries a fill texture as
well — committed plain, committed-completed hatched one way, total-completed the other,
carried out in horizontal lines, added work in dots — and the three lines on the instability
chart carry a dash pattern and a point shape (solid circle, dashed triangle, dash-dot
square). The texture is fixed per series in the same way the hue is, so it means the same
thing in all four themes, and it shows up in the chart legend and the hover tooltip as well
as on the bars.

This is deliberately not a colour fix. Red-green colour vision deficiency flattens the
red-green axis, leaving blue-yellow and lightness, which carry about three reliable levels
between them — and there are six series. Measured with the theme pack's simulation, the
committed grey and the velocity teal land within a CIE ΔE of 9–18 of each other in *every*
theme, and they're two of the three bars on the PI chart; a re-shading that cleared the
threshold did exist, but only by turning the committed bar near-black on the Light and Sepia
cards, and in Midnight only one candidate passed at all. The texture costs the palette
nothing and doesn't degrade. Stripes are the series' own colour at full strength over the
tinted fill, never a second colour — so the texture is also where a textured bar's contrast
lives, and it reads more clearly than it did when both fill and stripe were dark.

RAG state is never carried by colour alone — every tile and pill also has a glyph and a
spelled-out status for a screen reader. The view tabs work from the keyboard the way a tab
row is expected to: arrow keys move along the row and switch view, Home and End jump to the
ends, and the row takes a single stop in the tab order rather than one per tab.

Everything else is reachable from the keyboard too. The sprint and team names in every
table are real buttons, so you can tab to a row and press Enter to open it — clicking
anywhere in the row still works for a mouse. Each table names itself and marks its column
and row headings, so a screen reader reads "Sprint 3, carried out, 4" rather than nine
unattached numbers. Every dialog announces its own title, the sprint form's warnings and
auto-filled hints are tied to the boxes they refer to and read out when they change, and
pressing **Read it** on a Jira paste moves you to the result rather than leaving it
unannounced. Small targets like the ⓘ carry a 24px hit area without growing on screen, and
`prefers-reduced-motion` is honoured.

---

## Your data

`localStorage` in your own browser is the source of truth. **No account is needed and no
data leaves your machine** unless you choose to sign in.

**Back up & restore** — the *Back up* button exports everything as a JSON file
(`sprint-velocity-YYYY-MM-DD.json`, dated in local time) and imports it back. Useful as a
backup, for moving between browsers, or for handing a colleague a starting point.

**Deletion requests** — [privacy.html](privacy.html) promises that emailing the address
there gets a user's synced copy deleted. [`DATA_DELETION.md`](DATA_DELETION.md) is the
runbook for doing it: how to map an email address to the right Firestore document (the
document ID is the Firebase Auth UID, and nothing inside the document identifies anyone),
what order to delete in, and which copies are genuinely beyond reach.

## Recent changes

At the foot of the page there's a collapsed **Recent changes** box. Expand it and it fetches
the last 10 commits to `index.html` from the GitHub API and lists them newest first, each
one a link to the commit itself. Nothing is fetched until you open it, and if you're offline
it just says so.

Commit subject lines are written in plain English for this reason — the box is the app's
changelog, so the commit history *is* the release notes.

## Sharing a read-only link

The *Share* button builds a link that shows someone your figures without them signing in —
useful for a stakeholder, a manager, or an SM covering for you. They get the Sprint, Current
PI and Rolling 5 views for the teams you picked, with every edit control gone.

It opens on the **most recent sprint that has data**, so the first thing they see is your
latest numbers rather than an empty slot — and it follows each team to its own latest sprint
if they switch between them.

You choose per link:

- **Which teams** — the team you're looking at is ticked by default. Sharing one team doesn't
  reveal the others, or even the names of PIs that team never ran in.
- **The All teams comparison view** — only offered when you've picked more than one team.
- **Sprint notes** — your written comments on what was added, removed and carried over.
  **Off by default**, so candid retro commentary doesn't travel by accident.

**The data rides inside the link itself**, compressed into the part after the `#`. Browsers
never send that part to a server, so the figures go straight from your browser to theirs —
GitHub Pages, Firebase and Google never see them. Nothing is uploaded, no account is involved,
and opening a link cannot touch data the recipient already has saved in their own browser.

Two things to know:

- **It's a snapshot.** The numbers are frozen as they looked when you generated it. Later edits
  won't appear — send a fresh link when the figures move.
- **It can't be withdrawn.** Anyone holding the link can open it. Treat it like emailing a
  spreadsheet, not like a permission you can revoke.

A link you receive is treated as untrusted, because by definition it came from someone
else. Names have always been escaped before they reach the page; the ids that hold the
data together are now checked too, and anything that isn't a plain id is replaced with a
fresh one before the link renders. Without that, an id crafted to look like markup could
run code in your browser when you opened the link — reaching your own saved data and your
sign-in, neither of which the read-only guard covers. The same check runs on an imported
backup file and on the copy that comes down from sync.

The same boundary also checks that the data hangs together. A sprint that names a team or a
PI which isn't in the file is left out, because it would otherwise count towards the rolling
average while being impossible to open or even see — a figure moving with no sprint behind
it. The app's own *Delete PI* and *Delete Team* buttons tidy up after themselves, so this
only comes up with a hand-edited or damaged file. When it happens you're told how many
sprints were left out and why: an import says so before you commit to it, and a link or a
synced copy says so once it opens.

Links run to a few hundred characters for a typical team. If one gets long enough that a mail
client might break it across two lines, the dialog says so and suggests sharing fewer teams or
leaving notes out.

## Cross-device sync (Firebase, free tier — optional)

Sync is **enabled** in this deployment, backed by the `sprintvelocity-141b7` Firebase
project — the `FIREBASE_CONFIG` object at the bottom `<script type="module">` block of
`index.html` points at it. Signing in is entirely optional: the app is fully usable, and
fully local, without it. Setting that constant back to `null` returns it to local-only mode
and hides all sync UI.

### Why sign-in doesn't use Firebase's popup

Corporate web filters block individual `firebaseapp.com` hostnames unpredictably — the block
is per hostname, not the domain, so a sibling app working is no evidence this one will (the
sibling Team Dashboard's README tabulates three projects measured on one network on one day:
two blocked, one fine). Firebase's `signInWithPopup` opens its popup at
`<project>.firebaseapp.com/__/auth/handler`, so that block kills sign-in outright.

Sign-in therefore goes through **Google Identity Services**, the flow proven in Team
Dashboard: a popup straight to `accounts.google.com` returns an OAuth token that Firebase
exchanges for the same session via `signInWithCredential`. Same Google account, same
Firestore data, same rules — only the doorway differs. The old popup flow (and its
`firebaseapp.com` frame-src and `apis.google.com` CSP entries) is retired.

The sync module builds auth with `initializeAuth`, not `getAuth`, so `apis.google.com` is never
even requested. `getAuth()` always wires in `browserPopupRedirectResolver`, and on Safari, iOS
and mobile browsers the SDK initialises that resolver during startup — which loads
`apis.google.com/js/api.js` to build the gapi iframe that carries `signInWithPopup` and
`signInWithRedirect` results back to the page. This app calls neither, so nothing consumed it;
the visible symptom was a CSP error in the console on phones and in Safari, and nothing else.
Token refresh, sign-out and the cross-tab session all run elsewhere in the SDK and never touch
the resolver. Dropping it costs `signInWithPopup`/`signInWithRedirect`/phone sign-in, which now
raise `auth/argument-error`; if one is ever wanted, pass `browserPopupRedirectResolver` to that
call rather than reverting to `getAuth()`.

`GOOGLE_CLIENT_ID` at the top of the sync module is what this flow needs beyond
`FIREBASE_CONFIG`. It comes from
[console.cloud.google.com](https://console.cloud.google.com) → APIs & Services →
Credentials → the OAuth 2.0 Client ID named *Web client (auto created by Google Service)*,
whose **Authorized JavaScript origins** must list `https://eagleadams86.github.io` (and the
exact localhost origin you serve from, port included) — an unlisted origin makes Google
refuse with `origin_mismatch` before sign-in starts.

To recreate the setup from scratch (e.g. in a fork):

1. At [console.firebase.google.com](https://console.firebase.google.com), create a project
   (Analytics not needed)
2. **Build → Authentication → Get started → Google** — enable the Google sign-in provider
3. **Authentication → Settings → Authorized domains** — add `eagleadams86.github.io`
4. **Build → Firestore Database → Create database** (production mode), then paste these **Rules**:
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /sprintvelocity/{uid} {
         allow read, write: if request.auth != null && request.auth.uid == uid;
       }
     }
   }
   ```
5. **Project settings → Your apps → Add app → Web** — copy the `firebaseConfig` object and
   paste it as the value of `FIREBASE_CONFIG` in `index.html`

The same rules are kept as a checked-in copy in [`firestore.rules`](firestore.rules) — the
console is what's live, the file is the audit trail; if the rules ever change in the
console, update the file to match (same pattern as the paptrack-ios repo).

The config object is not a secret; access is controlled by the rules above, which restrict
every user to their own document. Each person who signs in — you or a colleague — gets
their own private data. Sharing the app means sharing the URL, not the data.

**How sync behaves:** `localStorage` stays in charge. The **first** time a given Google
account signs in on a browser, if both the browser and the cloud already hold data, a
dialog asks which to keep rather than guessing by timestamp — that guesswork once wiped a
browser's data in the sibling PAPTrack app. After that first reconciliation (tracked per
account via `sv-sync-uid`), and for live updates pushed from another device, whichever side
changed most recently wins. Signing out or losing connectivity just leaves the local copy
in charge.

**When sync stops working, it says so.** Every failure used to end in the browser console,
which nobody has open — so the button went on showing your name and the note went on
promising your data was reaching your other devices, while nothing had left the browser for
weeks. The button now reads **⚠️ Not syncing**, and the note at the foot of the page says
what went wrong and what to do about it. Nothing is ever lost when this happens: this
browser stays the source of truth and the cloud only mirrors it. There's no retry button
on purpose — Google already retries the temporary causes, the permanent ones wouldn't be
fixed by pressing anything, and the state clears itself the moment a save gets through.

**How much can it hold?** One Firestore document per user, capped at 1 MiB. Six teams
through a full year — four PIs, 144 sprints, with written notes on every one — comes to
about 133 KB, or 13% of that. Roughly eight years of that pace before it fills, or four if
the notes run long. If you ever do reach it, the app tells you rather than failing quietly,
and the fix is to export a backup and delete a PI you no longer need.

Underneath that, one rule holds everywhere: **an empty copy never beats a copy with data
in it**, whichever looks newer. Signing in on a browser with nothing in it yet puts an
empty copy in the cloud stamped with the current time, and without that rule the device
holding your actual sprints — stamped whenever you last edited it — would treat the empty
copy as newer and empty itself. Clearing everything deliberately still reaches your other
devices, but it asks before it takes effect on each one.

---

## Architecture

```
GitHub Pages (static hosting, this repo, main branch)
    ├── index.html    the whole app — markup, styles, logic, no build step
    ├── theme.css     shared design tokens (generated in the claude-theme-pack repo)
    └── chart.min.js  vendored Chart.js UMD build — no CDN, no network needed
            ├── all state ──► browser localStorage (source of truth, works offline)
            ├── signed in ──► Firestore doc sprintvelocity/{uid} (optional;
            │                 newer-wins by updatedAt with the empty-never-beats-data
            │                 guard; live onSnapshot updates)
            ├── shared    ──► the URL fragment itself (#share=…), read-only, never
            │                 uploaded and never written back to localStorage
            └── changelog ──► GitHub commits API, read-only, fetched on first expand
```

No server of our own. No build, no dependencies to install, no npm.

[`privacy.html`](https://eagleadams86.github.io/sprint-velocity/privacy.html) spells out
what the app stores and where — linked from the app's footer. Fellow Scrum Masters sign in
with their own Google accounts, so the policy exists for them as much as for the author:
what Firestore holds, that access rules confine each account to its own data, that share
links upload nothing, and how to have a synced copy deleted.

A Content Security Policy `<meta>` tag in `index.html` pins the page down as defence in
depth: scripts only from this origin and Firebase's CDN, network calls only to the
Firebase endpoints sync uses plus the GitHub commits API, and no frames except the app's
own Firebase auth helper. If a new external endpoint is ever added, it has to be added to
the CSP too or the browser will (deliberately) block it.

## Working on it locally

```bash
python3 -m http.server 8012
```

Then open http://localhost:8012. (The desktop app's preview pane reads
`.claude/launch.json`, which is set to the same port.)

**Tests:** open http://localhost:8012/tests.html — it loads the real `index.html` in a
hidden iframe and pins the pure functions (the Jira paste parser, the metrics and RAG
bands, `avg` vs `pooled`, the id sanitizer, the sprint lifecycle). No build step and no
frameworks: the page either says "All N tests pass" in green or lists what broke. Run it
whenever those functions change; it needs the local server, since `file://` iframes are
blocked in some browsers.

`theme.css` is a copy of the generated palette from the private `claude-theme-pack`
repo — the source of truth for the colours of every app in this family — and is left
byte-for-byte identical to it. The pack's contrast gate verifies every text and status
colour at WCAG AA on every surface it can sit on (page, card and the alt/pill
background), which covers even the way this app leans on red and green as the actual
reading rather than decoration — so the old block of app-local contrast corrections is
gone. The app still adds its own chart series colours and threshold-band tints at the
top of `index.html`.
