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
the page — and both still cross-link at the foot of the page, next to a **How it works**
link to that app's README on GitHub. If a chrome rule changes in
one app, it should change in the other too.

---

## What It Tracks

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

There is deliberately **no free-text field anywhere in the app**. The figures come out of a
work Jira, and a comment box is the one place sensitive detail could ride along into the
saved copy — so beyond the short team/ART/PI names, only numbers and dates are ever saved.
(Earlier versions had optional per-sprint "Why?" notes; the feature was removed, and any
notes in a previously saved copy are scrubbed the next time the app opens, locally and from
the synced copy.)

This is why the two capacity levers below — [adjusting for a sprint that isn't
normal](#adjusting-for-a-sprint-that-isnt-normal) and [leaving a sprint out of the
average](#leaving-a-sprint-out-of-the-average) — record *why* as a pick from a fixed list
rather than in a box you type into. "Why did we drop that sprint?" is the obvious place to
want free text, and it's exactly where a ticket key or a colleague's name would end up in
the cloud. A code from the list carries the meaning and can't carry anything else.

## The Metrics

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

## Filling a Sprint from Jira

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

### Stories Re-Sized Mid-Sprint

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

Nothing is saved by pasting itself — reading the report only shows you the preview, and the
pasted text is never stored: it is read for its figures on the spot and discarded. Pressing
**Use these numbers** fills the boxes **and saves the sprint there and then**, so a paste you
were happy with can't be lost by closing the form. If the
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

## Recording a Sprint Before It's Over

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

### Counting a Sprint That's Still Running

**Count sprints that are still running**, on the Rolling 5 and All teams views, opts in-flight
sprints into every figure — the rolling window, the PI totals, the team comparison and the
capacity target. It's off by default, because the numbers genuinely aren't final.

It's for the last day or two of a sprint, when you're planning the next one and today's
provisional numbers beat last sprint's stale ones. When it's on, every view says so, and the
capacity target stops aiming at the running sprint and points at the one after it — once a
sprint is being counted as data, it isn't the sprint you're planning any more.

Sprints that haven't started are never counted either way; they have no results at all.

### Overwriting a Finished Sprint

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

### Dates Fill Themselves

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

### Carried in Fills Itself

Whenever you open a sprint that has no carried-in figure yet, it's filled with what the
previous sprint carried out — crossing a PI boundary if you're on sprint 1. A note under the
fields says which sprint it came from, and it never overwrites a number you've already
entered or typed.

### Blank Means Zero

An empty box saves as 0 — most sprint data arrives from the Jira paste, where a figure that
isn't there genuinely is nothing, and a `—` where the honest answer is "0 removed" just looks
like missing data.

The one figure that still shows `—` is a percentage with nothing committed: there's no
denominator to divide by, so it can't be a number, and those sprints stay out of averages
rather than dragging them down.

## The Four Views

- **Sprint** — one sprint in detail: the RAG tiles and a breakdown of where the committed
  points actually went.
- **Current PI** — all six sprints of a PI, with PI totals and a sprint-by-sprint chart.
- **Rolling 5** — the last five sprints for a team, crossing PI boundaries. Velocity and
  commitment completion on one chart — with a dashed **velocity trend line** fitted by
  ordinary least squares, the same treatment every chart in the sibling Flow Metrics app
  carries — and an instability chart plotting break-in, removed and carryover against
  shaded 15% / 20% threshold bands.
- **All teams** — every team's rolling averages side by side, plus each team's next-sprint
  target in one column, so the one that needs attention is obvious. It carries **two
  comparison tables**, the same sprints through two different averages — see below — and
  an **ART filter** across the top when your teams are grouped into ARTs.

A view is only offered once there's something in it. **All teams** appears when you have a
second team; **Current PI** and **Rolling 5** appear once the team you're on has a recorded
sprint, and step aside again if you switch to a team you haven't recorded anything for. With
no teams at all there are no tabs — just the welcome card. If the view you were on goes away,
you land back on **Sprint**.

### Trying It Without Typing Anything In

The welcome card offers **Load sample data** beside *Add your first team*: two teams
(Kestrel and Otter) on two ARTs, nine recorded sprints across two PIs, and no dates — so
every view, both comparison tables, the capacity target and the ART filter all have
something behind them on a first run. Two ARTs of one team each is deliberate: it's the
arrangement where the **All teams** ART filter actually does something.

It asks before it loads, and everything it adds is ordinary data you can edit or delete —
*Teams, ARTs & PIs* removes the teams and PIs, or *Start again* in the Back up dialog
clears the lot. Don't load it into a browser that already holds real sprints you care
about: it's added alongside them, not instead of them, and unpicking it is manual.

## The Two Comparison Tables

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

**Current PI** and **Rolling 5** each end their *The numbers* table with **one** summary
row, in whichever method that view's own figures already use:

| View | Summary row | Method |
|---|---|---|
| Current PI | **PI total** | Pooled — matches the dashboard, and its headline commitment-completion tile |
| Rolling 5 | **Average per sprint** | Average of sprints — matches every tile on the view |

Its committed and delivered figures follow the method: **totals** on the pooled row,
**per-sprint means** on the average row. The row carries an ⓘ explaining its own method and
pointing at where the other one lives — which is **All teams**, above, where the two sit
side by side over the same sprints and can actually be compared.

(Both views used to show the two methods as a pair of rows. That made every table answer a
question most readers weren't asking, so each view now shows the one that matches the
figures above it.)

The tiles at the top of Rolling 5 are all averages of sprints. Current PI's tiles are a
mix: *PI commitment completion* is pooled, *Average per sprint* is the average-of-sprints
figure, and a wide gap between them means one sprint is skewing the total.

Comparison 2 also carries **Actual complete** — everything delivered, break-in work
included, against what was committed. It goes above 100% when a team finished more than it
signed up for, which says throughput was high, not that the plan held.

## Grouping Teams into ARTs

If you support teams across more than one Agile Release Train, you can group them.
**Teams, ARTs & PIs** has an **ARTs** section: add one, then set each team's ART from the
picker in its own row of the Teams table. A team can be on one ART or none — being on none
is perfectly normal, and nothing forces you to use the feature at all.

An ART is a **label, not a level of maths**. Every figure in the app is still worked out per
team; there is no separate per-ART calculation, and grouping never changes a single number.
What it changes is what you're looking at:

- **All teams** gains an **ART** picker across the top — *All ARTs*, each ART by name, and
  *No ART* if any team is un-grouped. Everything below it follows: both comparison tables,
  both **All teams** footer rows, the chart, and the count of sprints still in flight. Pick
  *Payments ART* and the footer row reads **All teams on Payments ART**, worked out across
  that ART's teams only.
- The picker says how many teams it's hiding, the same way every other exclusion in the app
  says what it left out — a figure should never move for a reason that isn't on the page.
- With no filter, the table **sorts by ART** so a train's teams sit together, and each team
  carries its ART under its name. The header team picker groups the same way.

Deleting an ART is the cheapest delete in the app: it takes no team and no sprint with it —
the teams that were on it simply go back to having none.

Share links carry only the ARTs the teams in the link are actually on, so sharing one team
doesn't publish the names of every train you support.

## Target Capacity for the Next Sprint

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
an unanswered question rather than a small commitment. Comparison 1's **Next sprint target**
column and its total use the adjusted figures, and mark an adjusted team with a ⚑. It warns you when there are fewer than
three sprints of history, when the team's delivery swings by more than 30%, and when the
next sprint up is the IP sprint.

It's a starting point for the planning conversation, not a quota. The two sections below
are for the things the history structurally cannot see.

### Adjusting for a Sprint That Isn't Normal

The rolling window knows what the team has been finishing. It has no way of knowing that
three of them are on leave next sprint, that a bank holiday lands inside it, or that
somebody left last week — and all of those change what the team can actually take on.

**Adjust capacity** on the Target Capacity card records that as a single figure: how
available the team will be, as a percentage of a normal sprint. 100% is a normal sprint;
one person in five away for the whole sprint is roughly 80%; over 100% is allowed for the
rarer case of extra help or a longer sprint. The recommendation is multiplied by it and
nothing else changes — the averages, the velocity, the range and the history behind them
all stay exactly as they were. The card shows both figures (`80% of 24`), carries a
**⚑ Adjusted** badge, and explains it in *How this is worked out*, so the number can never
quietly become something other than what the sprints say.

Pick a reason from the list — leave or sickness, public holidays, a shorter sprint, someone
joining or leaving, someone on call, an event. It's a fixed list of options rather than a
text box on purpose; see [Your Data](#your-data).

Two kinds of change, and the tick box is the difference:

| | Leave it unticked | Tick **Keep this for later sprints too** |
|---|---|---|
| For | Leave, holidays, a one-off shorter sprint | Someone joined or left, a lasting change |
| Applies to | This sprint only | Every sprint until you change it |
| Why | It's over once the sprint is | The rolling window needs five sprints to catch up with a change in team size on its own |

A one-off set against a particular sprint always wins over the standing figure — they
never multiply, so the number on the card is always one you can reason about. **Remove
adjustment** clears both, along with any sprint scaling (below).

### Scaling a Sprint the Team Has Outgrown

Sometimes the problem isn't next sprint — it's that one sprint in the window was produced
by a different team. Say sprint 1 ran with three people and a fourth has since joined
permanently: S1's result now drags the recommendation down for as long as it stays in the
window, but excluding it would throw a real data point away.

The same **Adjust capacity** dialog lists the sprints behind the figure, each with a
percentage. Scale S1 to 133% and its result counts at four-people strength in the
average — there's a team-size helper ("3 then, 4 now") that works the percentage out for
you. The card shows a **⚖ scaled** badge and explains the working; the All teams target
carries the same ⚑ as an availability adjustment.

**Only the recommendation changes.** The sprint's own recorded figures are untouched in
every chart and table — the Sprint view, the Current PI totals, the Rolling 5 tiles and
both comparison tables all still show exactly what the team delivered. A scale needs no
expiry: it sits on its sprint and retires by itself when that sprint drops out of the
rolling window.

How the three levers differ:

| | Scale a past sprint | Availability | Leave a sprint out |
|---|---|---|---|
| Fixes | History from a smaller/bigger team | The coming sprint being abnormal | History that would mislead |
| Keeps the data point | Yes, re-weighted | — | No, window reaches further back |
| Expires | When the sprint leaves the window | One-off, or standing until changed | When you untick it |

One thing the adjustment surfaces that's easy to miss: **carry-over doesn't shrink when the
team does.** Work already carried in is still carried in, and it comes off the top of a
smaller sprint. When it fills the adjusted figure entirely the card says so — there's no
room to pull in new work at all, which is worth deciding deliberately at planning rather
than discovering at the end.

### Leaving a Sprint Out of the Average

Sometimes the problem is the history rather than the sprint ahead: a major incident took
a sprint over, the points were re-baselined onto a different scale, the team was largely
away, or a team merged and the sprints before it belong to a different team.

The sprint form's **Rolling 5** section takes a sprint out of the rolling average
and the capacity target, with a reason from the same kind of fixed list. Everything else
about the sprint is untouched — its own figures still show in the Sprint view, the Current
PI view and both comparison tables, and it's still a finished sprint rather than one faked
back to "planned" to hide it, which is how this used to have to be done.

The window still fills to five, reaching further back into the history the same way it does
for the IP sprint.

**Exclusions are never silent, and they say so on every page an excluded sprint appears
on:**

| Where | What you see |
|---|---|
| Sprint view | A **⚑ Left out of the rolling average** banner spelling out what it does and doesn't change, and the badge on the sprint's own heading |
| Sprint picker | `Sprint 2 — left out of the average`, before you even open it |
| Current PI | A **⚑ Left out of the rolling 5** badge on the sprint's row, and a caption naming it as **included** in this PI's totals |
| Rolling 5 | A badged line under the heading naming it and the reason, and a note on the numbers table explaining the gap in the sprint numbers |
| All teams | A ⚑ on the team's sprint count in both comparison tables, and a line under the heading naming which team lost which sprint |

Leaving a sprint out also breaks the promise that Comparison 2 reconciles with the Agile
Operations Dashboard, because the sprint is still in the Dashboard's total until it's
unselected there too. So that badge becomes conditional and names the sprint —
*"matches the Agile Operations Dashboard when S1 is unselected there too"* — as do the
method note beneath it and the ⓘ help on both pooled figures. The **Current PI** total
keeps the unconditional promise, because that view never drops the sprint in the first
place.

The Current PI wording matters: an exclusion reaches the rolling average, the All teams
comparison and the capacity target, and **nothing else**. The sprint's own figures and the
PI totals are untouched — that's the whole difference between this and setting the sprint
back to "planned" to hide it.

### Sprint 6 and the Rolling Average

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

## Your Data

`localStorage` in your own browser is the source of truth. **No account is needed and no
data leaves your machine** unless you choose to sign in.

What's saved per sprint is the seven figures, its dates, its status, and — if you've set
one — whether it's left out of the rolling average and which of the fixed reasons applies.
A capacity adjustment saves as a percentage and a reason code against a team and a sprint
slot. Nothing else.

The names you type — teams, ARTs and PIs — are **capped at 120 characters as they're
written**, not only on the way back in: the object you name is the one that reaches
`localStorage` and the cloud, so the cap is applied at the point of the rename as well as
at the boundary that reads a saved, imported or synced copy. Percentages and reason codes
pass that same boundary, so a hand-edited file can't widen either.

**Back up & restore** — the *Back up* button exports everything as a JSON file
(`sprint-velocity-YYYY-MM-DD.json`, dated in local time) and imports it back. Useful as a
backup, for moving between browsers, or for handing a colleague a starting point.

**Starting again** — folded away at the foot of the same dialog, under *Start again*, is
**Delete all data**. It's behind a fold on purpose: the one irreversible action in the app
shouldn't sit a mis-click away from Export. Pressing it opens a confirmation of its own that
says exactly how much is going ("This deletes 2 teams, 1 PI and 3 recorded sprints"), warns
you when you're signed in that the copy in your Google account goes too — your other devices
ask before clearing themselves — and offers the same JSON export as a last chance to keep any
of it. Your theme survives; it lives under its own key rather than with the data.

**Deletion requests** — [privacy.html](privacy.html) promises that emailing the address
there gets a user's synced copy deleted. [`DATA_DELETION.md`](DATA_DELETION.md) is the
runbook for doing it: how to map an email address to the right Firestore document (the
document ID is the Firebase Auth UID, and nothing inside the document identifies anyone),
what order to delete in, and which copies are genuinely beyond reach.

## Recent Changes

At the foot of the page there's a collapsed **Recent changes** box. Expand it and it fetches
the last 10 commits to `index.html` from the GitHub API and lists them newest first, each
one a link to the commit itself. Nothing is fetched until you open it, and if you're offline
it just says so.

Commit subject lines are written in plain English for this reason — the box is the app's
changelog, so the commit history *is* the release notes.

## Sharing a Read-Only Link

The *Share* button builds a link that shows someone your figures without them signing in —
useful for a stakeholder, a manager, or an SM covering for you. They get the Sprint, Current
PI and Rolling 5 views for the teams you picked, with every edit control gone.

It opens on the **most recent sprint that has data**, so the first thing they see is your
latest numbers rather than an empty slot — and it follows each team to its own latest sprint
if they switch between them.

You choose per link:

- **Which teams** — the team you're looking at is ticked by default; **Select all** takes the
  lot, and the count above the list says where you are. Sharing one team doesn't reveal the
  others, or even the names of PIs that team never ran in.
- **How much history** — all of it (the default), the last 2 PIs, this PI only, or the last 5
  or 10 sprints for each team. See below.
- **The All teams comparison view** — only offered when you've picked more than one team.

A link only ever carries names, numbers and dates — there is no free-text anywhere in the
data, so nothing written can travel by accident.

### How Much History

A link carries its data inside itself, so the longer your history grows, the longer the link
gets — and a very long one can be broken in half by a mail client on the way. **How much
history** is the way out of that: it shortens the link without you deleting a single sprint.

The sprint options are **per team**, so sharing three teams with "the last 10 sprints" gives
ten each rather than ten between them. The PI options are the other way round — a PI is a
program increment your teams share, so "this PI only" means the same PI for everybody and the
comparison views stay lined up.

**As much as fits in a mailable link** does the choosing for you: it works out the largest
window that still comes in under the length where mail clients start breaking links, and tells
you what it settled on. If your whole history already fits, it says so and leaves it alone.

The dialog says what you'd expect it to say and one thing you might not:

- how many sprints of your total went in, and how long the link came out;
- a team left with nothing by the window — likely with *this PI only* — is named and left out
  of the link entirely, rather than shipped as an empty tab;
- and if the window leaves a team with fewer than five finished sprints, it warns you, because
  **their Rolling 5 will then average fewer sprints than yours does** — trimming below five
  changes the figures rather than just the size of the link.

Whoever opens a trimmed link is told so in the banner at the top, so a figure that doesn't
match yours has a visible reason. They aren't told how much history sits behind it.

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

The same boundary now also guards the *shape* of what arrives: a payload whose team, PI or
sprint list isn't a list at all — or holds entries that aren't records — is coerced to a
sane shape instead of being copied in raw, where the first render after it would have thrown
on a blank page. The file import and share links still refuse a wrong file outright (the
shape is checked before it's coerced, so any old JSON can't slip through as an empty export).

The same boundary also checks that the data hangs together. A sprint that names a team or a
PI which isn't in the file is left out, because it would otherwise count towards the rolling
average while being impossible to open or even see — a figure moving with no sprint behind
it. The app's own *Delete PI* and *Delete Team* buttons tidy up after themselves, so this
only comes up with a hand-edited or damaged file. When it happens you're told how many
sprints were left out and why: an import says so before you commit to it, and a link or a
synced copy says so once it opens.

Links run to a few hundred characters for a typical team. If one gets long enough that a mail
client might break it across two lines, the dialog says so and points at the two things that
shorten it — fewer teams, or less history.

## Cross-Device Sync (Firebase, Free Tier — Optional)

Sync is **enabled** in this deployment, backed by the `sprintvelocity-141b7` Firebase
project — the `FIREBASE_CONFIG` object at the bottom `<script type="module">` block of
`index.html` points at it. Signing in is entirely optional: the app is fully usable, and
fully local, without it. Setting that constant back to `null` returns it to local-only mode
and hides all sync UI.

### Why Sign-In Doesn't Use Firebase's Popup

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

**How much can it hold?** One Firestore document per user, capped at 1 MiB. Now that a
sprint is nothing but numbers and dates, six teams through a full year — four PIs, 144
sprints — comes to well under 100 KB, so decades of history fit before the cap is anywhere
in sight. If you ever do reach it, the app tells you rather than failing quietly,
and the fix is to export a backup and delete a PI you no longer need.

That advice is now only given when the size is genuinely the problem. Firestore reports an
oversized document and a value it can't store under the same error code, and the app used
to assume the first — so a bug of its own once told a user to delete a PI. A remedy that
destroys data is never the guess: anything that isn't demonstrably about size now says the
fault is in the app, and asks for nothing to be deleted.

Underneath that, one rule holds everywhere: **an empty copy never beats a copy with data
in it**, whichever looks newer. Signing in on a browser with nothing in it yet puts an
empty copy in the cloud stamped with the current time, and without that rule the device
holding your actual sprints — stamped whenever you last edited it — would treat the empty
copy as newer and empty itself. Clearing everything deliberately still reaches your other
devices, but it asks before it takes effect on each one.

---

## Architecture

The icon — a sprint cycle opening at the commitment point, on the midnight tile
the whole app family wears — is drawn by `make_favicon.py` (Pillow). The inline
SVG in the page is what browsers show in the tab and what the header wears;
`favicon.ico` is the fallback a browser fetches from the site root on its own,
and what a bookmark uses. The script keeps the two the same picture rather than
leaving a binary nobody can review in a diff. Re-run it with
`python3 make_favicon.py`, then bump the `?v=` on every `favicon.ico` reference
— browsers hold on to an icon for a long time.

```
GitHub Pages (static hosting, this repo, main branch)
    ├── index.html    the whole app — markup, styles, logic, no build step
    ├── theme.css     shared design tokens (generated in the claude-theme-pack repo)
    ├── favicon.ico   the tab icon's fallback, drawn by make_favicon.py
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
what the app stores and where — linked from the app's footer, beside a **How it works** link
to this README (GitHub renders it on the repo's front page), for anyone who wants more than
the in-app ⓘ dialogs. Fellow Scrum Masters sign in
with their own Google accounts, so the policy exists for them as much as for the author:
what Firestore holds, that access rules confine each account to its own data, that share
links upload nothing, and how to have a synced copy deleted.

A Content Security Policy `<meta>` tag in `index.html` pins the page down as defence in
depth: scripts only from this origin, Firebase's CDN (`www.gstatic.com`) and Google's
sign-in client (`accounts.google.com`); network calls only to the Firebase endpoints sync
uses, `accounts.google.com` and the GitHub commits API; and the only frame allowed is
`accounts.google.com`, the Google Identity Services popup. **`apis.google.com` and
`<project>.firebaseapp.com` are deliberately absent** — the Firebase auth helper frame went
when sign-in moved to Google Identity Services, and the sync module uses `initializeAuth`
so the SDK never asks for the gapi iframe either (see [Why Sign-In Doesn't Use Firebase's
Popup](#why-sign-in-doesnt-use-firebases-popup)). If a new external endpoint is ever added,
it has to be added to the CSP too or the browser will (deliberately) block it.

## Working on It Locally

```bash
python3 -m http.server 8012
```

Then open http://localhost:8012. (The desktop app's preview pane reads
`.claude/launch.json`, which is set to the same port.)

**Tests:** open http://localhost:8012/tests.html — it loads the real `index.html` in a
hidden iframe and pins the pure functions — 96 checks in 18 groups: the Jira paste
pipeline and its estimate cells, the metrics and RAG bands, `avg` vs `pooled`, the trend
line, the shape and id sanitizers, the 120-character label cap, the ART grouping, the
sprint lifecycle, the share-link round trip and its history trimming, and the three
capacity levers (the availability adjustment, scaling a past sprint, and a sprint left out
of the rolling window) along with the boundary that stores their percentages and reason
codes. No build step
and no frameworks: the page either says "All N tests pass" in green or lists what broke.
Run it whenever those functions change; it needs the local server, since `file://` iframes
are blocked in some browsers.

**It only runs on localhost, and enforces that itself.** The test code writes nothing, but
the iframe boots the real app — and GitHub Pages publishes `tests.html` next to it, at
`/sprint-velocity/tests.html`, where that iframe would be your signed-in copy: sync would
start inside an invisible frame, and the "another device cleared its data" dialog could fire
where nobody can answer it. Two guards. The iframe carries `data-sv-tests`, which the sync
module checks so it never initialises in the harness; and a gate at the foot of `tests.html`
checks `location.hostname` and, anywhere but `localhost` / `127.0.0.1` / `[::1]`, never
creates the iframe at all — it explains why and says how to run the suite properly. CI
reaches the page on `localhost:8012`, so it is unaffected.

![tests](https://github.com/eagleadams86/sprint-velocity/actions/workflows/tests.yml/badge.svg)

The suite also runs on every push: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)
serves the folder, opens `tests.html` in headless Chromium and fails the build if the
summary goes red or the page throws — same workflow as the rest of the app family.

`theme.css` is a copy of the generated palette from the private `claude-theme-pack`
repo — the source of truth for the colours of every app in this family — and is left
byte-for-byte identical to it. The pack's contrast gate verifies every text and status
colour at WCAG AA on every surface it can sit on (page, card and the alt/pill
background), which covers even the way this app leans on red and green as the actual
reading rather than decoration — so the old block of app-local contrast corrections is
gone. The app still adds its own chart series colours and threshold-band tints at the
top of `index.html`.
