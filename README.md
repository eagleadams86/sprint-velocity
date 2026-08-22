# Sprint Predictability · Charlie’s Epic Sprint Planner

A sprint predictability tracker for Scrum Masters. Record what each team committed to,
what they actually finished, and what changed mid-sprint — the app works out commitment
completion, break-in, carryover and velocity, and flags each one against your targets.

**Live:** https://eagleadams86.github.io/sprint-velocity/

Built for Scrum Masters running several teams on a SAFe-style cadence: six sprints to a
Program Increment, with sprint 6 reserved for innovation and planning — though
[**PIs are entirely optional**](#pis-are-optional), and a team running plain Scrum with
continuous sprint numbers works just as well.

One of a pair: [Flow Metrics](https://eagleadams86.github.io/team-dashboard/) (the
`team-dashboard` repo — the app was renamed on screen only) is the
sibling app for weekly flow metrics, sharing this app's look and behaviour — the same sticky
header, button tabs, tiles, ⓘ help dialogs, theme picker and footer. **Each app's footer
carries a button link to the other**, at the right-hand end of the row that holds the
**Privacy policy** and **How it works** links. If a chrome rule changes in
one app, it should change in the other too — with one noted exception, **what a tile is drawn
on**. Flow Metrics puts its tiles on the same surface as its cards; this app keeps them a shade
apart, because here that background carries meaning (neutral, green, amber, red, and the hero's
card surface, where Flow Metrics has one state and no targets) and because these tiles sit
*inside* a card where Flow Metrics' sit on the page — so the same change would dissolve them into
the box around them. The 4px-to-6px **left edge** that came with that change in Flow Metrics did
cross over: it is a mark rather than a fill, and it reads the same in both.

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
| **Sprint goal** | Met, not met, or not recorded — see [The Sprint Goal](#the-sprint-goal) |

Per team, per PI, it also tracks the **business value** on that team's PI objectives —
planned, achieved, and achieved from stretch — which is what the [predictability
measure](#predictability-and-the-art-pi-view) is worked out from.

There is deliberately **no free-text field anywhere in the app**. The figures come out of a
work Jira, and a comment box is the one place sensitive detail could ride along into the
saved copy — so beyond the short team/ART/PI names, only numbers and dates are ever saved.
That's why PI objectives are three numbers and not a list of titled objectives, and why the
sprint goal is a yes/no rather than the goal itself: a title or a goal statement is exactly
the sort of text this rule exists to keep out.
(Earlier versions had optional per-sprint "Why?" notes; the feature was removed, and any
notes in a previously saved copy are scrubbed the next time the app opens.)

This is why the two capacity levers below — [adjusting for a sprint that isn't
normal](#adjusting-for-a-sprint-that-isnt-normal) and [leaving a sprint out of the
average](#leaving-a-sprint-out-of-the-average) — record *why* as a pick from a fixed list
rather than in a box you type into. "Why did we drop that sprint?" is the obvious place to
want free text, and it's exactly where a ticket key or a colleague's name would end up in
the cloud. A code from the list carries the meaning and can't carry anything else.

## Across PIs

Every other view looks at a single PI, or at a fixed five-sprint window. **PI trend** is the
only one that is PI-grained over time, which makes it the only place the Inspect & Adapt
question can be asked: *not how the last PI went, but which way the train is moving.*

```
Every Team — Across 3 PIs

PI predictability        Commitment completion      Delivered
      86% ✓                    81% !                   429
PI 2026.3 — up 5.2         down 11.7 points        up 303 on
points on PI 2026.2        on PI 2026.2            PI 2026.2
```

The headline is **predictability**, because that's what goes on the I&A slide, and the chart
plots it per PI against the 80–100% band with a dashed trend line through it. Commitment
completion and delivered points sit beside it because a train can move one without the other
— and when they disagree, as they do above, that gap is usually the conversation.

### Comparing PIs that weren't the same train

**Each PI is measured over the teams that were actually in it.** A train that grew from two
teams to five didn't get better because there's more of it, so where the team count changes
the view says so:

> **⚑ Not the same train throughout** — These PIs cover different numbers of teams: PI 2026.1
> 2 teams, PI 2026.2 2 teams, PI 2026.3 5 teams. Predictability is each team's own measure
> averaged, so it compares fairly across a train that changed size; the **points** columns are
> totals and will move with the headcount whatever the teams did.

That's the reason the two methods are split the way they are. **Predictability** is the mean
of each team's own measure — every team counting once — which survives the comparison.
**Complete %** is pooled, matching the Current PI tab and the Agile Operations Dashboard, and
it doesn't.

A PI with nothing recorded is dropped rather than drawn as a hole, and a PI with no business
value recorded leaves a gap in the predictability line rather than reading as 0%. Both are
named under the heading.

There's deliberately **no total row**. Adding PIs together answers nothing — a programme's
history is a sequence, and the only summary worth having is which way it's going, which is
what the trend line is.

### What the next PI could hold

At the foot of the same view, because PI planning is exactly when you look at how the last
few went and then decide what to sign up for next:

| Team | Per sprint | Across 5 sprints |
|---|---|---|
| Team Baseline | 36 | 178 |
| Team Live Sprint | 23 ⚑ 90% | 113 |
| … | | |

It's each team's next-sprint target multiplied by the **delivery** sprints in a PI — five,
not six, since the IP sprint delivers none of it. That means it inherits the whole method
from [Rolling 5](#target-capacity-for-the-next-sprint), availability adjustments included, so
it can't drift from the card that explains the working. A second figure appears alongside it
for the [reliable commitment](#two-figures-not-one) where teams have one.

That second figure is only ever the *lower* of the two, which takes a little care across a
train. A team dragged down by one bad sprint has no floor below its own average — see
[Two figures, not one](#two-figures-not-one) — so it contributes its recommendation rather
than a "reliable" number that sits above it. The tile says how many teams actually brought a
floor when it isn't all of them, and the cautious total can never come out above the central
one.

A team that has never run a PI is left out and named — its capacity is on Rolling 5, where it
lives.

## PIs Are Optional

Sprints used to have to live inside a Program Increment: with a team recorded but no
PI, the app showed one card — *"Add a Program Increment First"* — and nothing else worked.
That's gone. **A PI is never required.**

Add a team, record sprints, and use the app indefinitely without one. Sprints numbered
1, 2, 3 … 47, a rolling average, a capacity target, a forecast, sprint goals, the All
teams comparison — none of it needs a PI. Only the two views that are *about* PIs do, and
they simply aren't there until you make one:

| | With no PI | Once a PI exists |
|---|---|---|
| Sprint, Rolling 5, All teams | ✅ | ✅ |
| **Current PI** | hidden | appears once the team has a sprint in one |
| **ART PI** | hidden | appears once an ART has a team on it |
| PI business value / predictability | — | per team, per PI |

### Starting without one, adding one later

Every sprint carries a **PI** picker, which now offers **No PI** alongside your PIs. That's
how a sprint moves into a PI after the fact — and back out again. Create the PI in *Teams,
ARTs & PIs* whenever it becomes useful, then set it on the sprints that belong to it.

**Sprints with no PI count as a team's oldest history.** That's the case this is built for:
you record sprints, later decide to run PIs, and everything from before the first PI is the
history that came before it. The consequence to know is the reverse — putting a *new* sprint
on "No PI" while PIs exist files it before all of them, so the form says so before you save.

**There's no IP sprint outside a PI.** Sprint 6 is the innovation-and-planning sprint
*because of where it sits inside a PI*; without one it's just the sixth sprint, so it counts
in the rolling window like any other and the "include sprint 6 (IP)" toggle doesn't appear
for a team that isn't running PIs.

### Deleting a PI no longer deletes its sprints

It used to destroy every sprint in that PI across every team, because a sprint couldn't
exist without one. Now it asks:

```
Delete PI 2026.3?
17 sprints across 5 teams are in this PI. You can keep them — the figures
are untouched, they simply stop being in a PI…

Either way, this PI's 4 business value records and 1 capacity adjustment
are deleted — both are defined by the PI and have nowhere to go without it.

[ Cancel ]              [ Delete the sprints too ]  [ Keep the sprints ]
```

Kept sprints are renumbered onto the end of the team's unassigned run, so no two sprints
end up sharing a slot. Business value and capacity adjustments go either way — both are
defined by the PI — and the dialog says so rather than letting them go quietly.

## The Sprint Goal

Every other figure here is about **points**. None of them can tell you whether the sprint
achieved what it was *for*.

A team can finish 95% of its commitment and miss the one outcome the sprint was planned
around. Another can drop half its points to an incident and still deliver the goal. Only the
team knows which happened, so it's a question on the sprint form — **Met**, **Not met**, or
**Not recorded** — and never something the app infers from the numbers.

**"Not recorded" is a real answer and is the default.** This is deliberately *not* the
[blank means zero](#blank-means-zero) rule that governs the rest of the form: a blank points
box really is zero points, but an unanswered goal is not a missed goal. Reading it as one
would invent a failure for every sprint recorded before this field existed — which is all of
them — and plenty of teams don't set sprint goals at all. Every rate below counts only the
sprints somebody actually answered, and says how many it left out.

Where it shows up:

- **Sprint** — a tile, when there's an answer. No answer, no tile: an unanswered question
  isn't a metric.
- **Current PI** — a ✓ or ✕ badge on each sprint's row. Not a tenth column: the table already
  scrolls sideways on a phone, and six rows is a countable number.
- **Rolling 5** — **Sprint goals met**, as a count: *"3 of 4"*. A count rather than a
  percentage because that's the sentence you say out loud at a retro, and over four or five
  sprints a percentage rounds to figures like 67% that imply precision they don't have.

### When the Points and the Goals Disagree

This is the finding the field exists for, and neither number can make it alone. Rolling 5
says so in plain words when the two clearly part company:

> **◎ The points land, the goals don't** — Team Headroom finished 98% of what they committed
> to, and met the sprint goal in only **2 of 5** sprints.

A team hitting its commitment while missing what the sprints were *for* doesn't have an
execution problem — it's planning the wrong work, and every points figure on the page will
keep reading green while that's true.

The reverse gets said too, and it's the kinder half:

> **◎ The goals land, the points don't** — Team Overcommitted met the sprint goal in all 4
> sprints in this window, on 70% commitment completion.

They're delivering what the sprints were for; what's off is the estimate of how much fits in
one. A run of amber commitment figures reads very differently once you know that.

Both need at least two answered sprints — one is an anecdote — and both fire only on a clear
disagreement, so an ordinary team with a mixed record stays quiet. Neither is colour-coded:
the point is precisely that the colour-coded tiles beside them are answering a different
question.

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
| PI predictability | 80–100% | 70–79%, 101–120% | < 70%, > 120% |

The last one is a **band**, not a threshold — it can be missed from either side, and both
sides mean something. See [Predictability and the ART PI
view](#predictability-and-the-art-pi-view).

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
change nothing. Only a recorded figure actually changing —
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

## The Six Views

- **Sprint** — one sprint in detail: the RAG tiles and a breakdown of where the committed
  points actually went.
- **Current PI** — all six sprints of a PI, with PI totals and a sprint-by-sprint chart,
  plus this team's **PI objectives** and the predictability measure worked out from them.
- **Rolling 5** — the last five sprints for a team, crossing PI boundaries. Velocity and
  commitment completion on one chart — with a dashed **velocity trend line** fitted by
  ordinary least squares, the same treatment every chart in the sibling Flow Metrics app
  carries — and an instability chart plotting break-in, removed and carryover against
  shaded 15% / 20% threshold bands.
- **PI trend** — every PI side by side, oldest first: predictability against the
  80–100% band with a trend line through it, and how far the latest PI moved from the one
  before. This is the Inspect & Adapt view — see [Across PIs](#across-pis).
- **ART PI** — the whole train's PI on one page: every team's points and business value side
  by side, the ART's **predictability measure**, and a chart of each team against the
  80–100% band. This is the RTE view — see [Predictability and the ART PI
  view](#predictability-and-the-art-pi-view).
- **All teams** — every team's rolling averages side by side, plus each team's next-sprint
  target in one column, so the one that needs attention is obvious. It carries **two
  comparison tables**, the same sprints through two different averages — see below — and
  an **ART filter** across the top when your teams are grouped into ARTs.

The last three look **across** teams rather than into the one you've selected, so they sit
apart from the other three in the tab row.

A view is only offered once there's something in it. **All teams** appears when you have a
second team; **Current PI** and **Rolling 5** appear once the team you're on has a recorded
sprint, and step aside again if you switch to a team you haven't recorded anything for;
**ART PI** appears once you have an ART with a team on it; **PI trend** once two PIs have
something recorded in them, because one point is a position rather than a direction. With
no teams at all there are no tabs — just the welcome card. If the view you were on goes away,
you land back on **Sprint**.

### The Demo — Trying It Without Typing Anything In

The welcome card offers **Load sample data** beside *Add your first team*. It isn't
filler: it's the app's demo, and the rule is that **every feature has to be reachable
from it**. Six teams — four across two ARTs with history over three PIs, one of them
running right now, plus a team on no ART and a team that doesn't use PIs at all — so
nothing in the app is a screen you have to imagine.

It lands you on that running sprint, because it's the one state the app can't show
without real dates. The other five teams are one click away in the team picker, and each is
**named for the one thing it's there to show** — so the picker reads as a contents page
rather than a list of names you'd have to open one by one:

| Team | ART | What it's there to show |
|---|---|---|
| **Team Live Sprint** | Payments | A sprint **running right now** — done-so-far, pace ("day 6 of 14, slightly behind") and carried-in. Its commitment is well over the suggestion, which is the one finding still actionable mid-sprint. Also a **⚑ standing team availability**, and the only team with **no business value recorded** — its PI is still running, which is why. Records **no sprint goals** either, so the goals tile is absent rather than showing a zero. |
| **Team Baseline** | Payments | The ordinary team: green, landing about 90% of what it signs up for. Spans **all three PIs**, so the [PI trend](#across-pis) has a team behind every point. Carries a **⚖ scaled sprint** (someone joined after it) and a sprint with work **↩ brought in then removed again**. Its PI predictability is 90% — **inside the band**. Sprint goals **3 of 4**, with one sprint unrecorded — the only place the "no goal recorded" caption appears. |
| **Team Overcommitted** | Platform | The team the targets exist to catch — around 70% completion and swinging from 14 to 26 points. Has a **⚑ sprint left out** for a major incident, and its next slot is the **IP sprint**, so it carries that caveat too. 59% predictability — **under the band**. It's also the team where the [**reliable commitment**](#two-figures-not-one) differs from the average enough to matter: 20 or 17 — and where **◎ the goals land and the points don't**. |
| **Team Headroom** | Platform | **↗ Room for more** — it clears its commitment then pulls extra work in, so it reads 98% commitment completion beside a **red 29% break-in**. The contradiction the [headroom note](#when-a-team-has-room-for-more) exists to resolve. It under-commits its objectives too: 113%, **over the band**, with the value coming partly from **stretch**. Steady enough that it gets **one** capacity figure rather than two — and it's the team where **◎ the points land and the goals don't**, at 2 of 5. |
| **Team New Start** | *none* | A brand-new team: **thin history**, a **⚑ one-off availability** for leave, and a carryover that then **fills the whole figure** — no room for new work at all. Being in no ART, it's also the **No ART** group on *All teams* and *ART PI*. |
| **Team No PI** | *none* | The team that [**doesn't run PIs**](#pis-are-optional) — sprints numbered **12–16**, continuous, past the six a PI holds. No IP sprint, no Current PI tab, and it's named on *ART PI* as not being in that PI at all. Deliberately carries nothing else: every other finding already belongs to a team above. |

Two ARTs of two plus two teams in neither is the arrangement where the *All teams* ART
filter and its *No ART* group both actually do something.

The business value is picked the same way — to make the *ART PI* view say something on a
first run. **Platform ART is the [cancelling case](#when-the-average-hides-the-train)**: Team
Overcommitted at 59% and Team Headroom at 113% average to 86%, so the train reads on target
while neither of its teams is, and the ⚑ note that catches it has something to catch. **Payments
ART** is scored from one of its two teams, so the "not scored yet" note has a team to name.
The two averaging methods land 1.7 points apart on Platform — don't tidy them into agreement, a
demo where the two methods always match teaches that they always do.

The demo also seeds the **forecast** box with 120 points, so that card shows a worked answer
the moment you reach it rather than an empty box — it holds no stored data, so seeding it
costs nothing and it lands differently on each team.

The running sprint's dates are counted from the day you load it, not baked in, so the
demo is still live whenever it's opened rather than stale from the day it was written.
Everything else is dateless on purpose — a sprint with no dates resolves as complete,
which is what keeps the other five teams fully in the averages.

The sample-data tests pin every finding in that table, so tidying the numbers can't
quietly leave a first run with nothing to look at. **Adding a feature means adding the
data that demonstrates it here, a row in this table, and a test** — a feature the demo
can't reach is a feature nobody you share this with will find.

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

## Predictability and the ART PI View

Commitment completion asks whether the **points** landed. It doesn't ask whether the
**objectives** did, and those are different questions — a team can finish 95% of its points
and miss the two objectives the PI was planned around.

So each team's PI can carry three business-value figures, entered on the **Current PI** tab
under *PI Objectives*:

| Figure | What it is |
|---|---|
| **Planned (committed)** | The value of the objectives the team committed to at PI planning |
| **Achieved** | How much of that committed value actually landed |
| **Achieved from stretch** | What the stretch objectives delivered on top |

```
PI predictability = (achieved + achieved from stretch) / planned
```

**Stretch value counts in the top half and never in the bottom half.** That's the whole
design of a stretch objective — it was never a commitment, so counting it as one would
penalise a team for planning stretch at all. It's also what lets an honest figure sit above
100%, the same shape as commitment completion exceeding 100% when work is re-sized upward.

There is deliberately **no field for an objective's title**, and there never will be. A title
is free text, and free text is the one thing this app doesn't store — see [What It
Tracks](#what-it-tracks). Three numbers off your PI planning sheet carry the measure and
can't carry a ticket key.

### The Band — Both Edges Are a Finding

This is the only figure in the app judged by a **band** rather than a one-sided threshold:

| | 🟢 Green | 🟡 Yellow | 🔴 Red |
|---|---|---|---|
| PI predictability | 80–100% | 70–79%, or 101–120% | Under 70%, or over 120% |

Under the band is the obvious finding. **Over it is a finding too**: a train that reliably
lands at 130% didn't have a good PI, it committed to less than it knew it could deliver — and
every other team's plan built on that commitment was wrong by the difference. Between 100%
and 120% it's amber rather than red, because stretch objectives are *supposed* to land
sometimes; that's what they're for. It only goes red when it's too big to be stretch.

Because "off target" means two opposite things here, every figure also says **which side** it
missed on, out loud — "below the 80–100% band", "above the 80–100% band" — rather than
leaving a colour and a ✕ to carry a direction they can't.

### The ART PI View

The **ART PI** tab is the train's page. Pick an ART and a PI and you get every team on it at
once: sprints counted, points committed and finished, commitment completion, business value
planned and delivered, and each team's predictability. It shares its ART picker with **All
teams**, so the scope follows you between the two.

The headline **ART predictability** tile is the average of the teams' own measures — every
team counting once, whatever the size of its plan. That's the measure SAFe defines and the
one an RTE reports at Inspect & Adapt. The footer row of the table underneath is the *other*
method: all the value pooled and divided once, so a team that planned three times as much
value pulls three times as hard. Same teams, same PI, two honest answers — the same
arrangement as [the two comparison tables](#the-two-comparison-tables), and each says which
it is.

**A team with nothing recorded is named, not quietly dropped.** It stays in every points
figure and sits out the predictability ones, and a ⚑ note above the tiles says which teams
those are and where to record them. A train figure worked out from three of five teams while
the page shows five is exactly the silent exclusion the rest of the app refuses.

### When the Average Hides the Train

A two-sided measure has a failure mode a one-sided one doesn't. A team that **under-delivered**
and a team that **under-committed** sit on opposite sides of the band and cancel each other
out, so the train's average lands neatly inside it:

```
Team Overcommitted   20 of 34 business value   =   59%   ✕ below the band
Team Headroom        34 of 30 business value   =  113%   ! above the band
                                   ART average =  86%   ✓ in the band
```

Two teams that both missed, reading as a train that hit. So whenever the ART figure is inside
the band and there are teams on **both** sides of it, the view says so above the tiles —
naming the teams, and pointing you at the rows instead of the headline. (The demo's Platform
ART is exactly this case, deliberately.)

## Teams, ARTs & PIs: the Window Itself

All three lists are managed in one window, and all three rows work the same way.

**A name is edited in place.** Type in the box; there is no *Rename* button and no prompt.
A prompt was a box on top of a box to change one word, and it could not show you the other
names while you picked one that fits beside them.

**× deletes**, in the same red the app's other destructive buttons use. What a delete takes
with it differs by row and the confirmation says so: a team takes its sprints, a PI takes
its sprints across every team, and an ART takes nothing at all — its teams simply go back to
being on none.

**↑ and ↓ reorder.** All three lists are *read* in the order you put them in: teams appear
in that order in every picker and down **All teams**, ARTs are the order their groups come
in, and PI order is the app's sense of time — the rolling window walks back through it. The
order you added things in is rarely the order you want to read them in a year later. The
arrows at each end of a list are disabled rather than hidden, so no row ever jumps under the
pointer, and moving something with the keyboard keeps your place on it.

Adding is the same shape: **+ Add** puts a row in with a working default name and lands the
cursor in it, already selected, so typing replaces it.

The [Flow Metrics](https://eagleadams86.github.io/team-dashboard/) **Teams & ARTs** window
works identically — the two apps share their chrome, so a row is a row in both.

## Grouping Teams into ARTs

If you support teams across more than one Agile Release Train, you can group them.
**Teams, ARTs & PIs** has an **ARTs** section: add one, then set each team's ART from the
picker in its own row of the Teams table. A team can be on one ART or none — being on none
is perfectly normal, and nothing forces you to use the feature at all.

An ART is **almost entirely a label rather than a level of maths**. Every points figure in
the app is worked out per team and then simply added up; grouping never changes a single one
of them. The one exception is the **predictability measure** on the [ART PI
view](#predictability-and-the-art-pi-view), which SAFe defines at train level and which has
nowhere else it could live. Everything else the grouping does is change what you're looking
at:

- **ART PI** appears at all — the train's own page, described above.
- **All teams** gains an **ART** picker across the top — *All ARTs*, each ART by name, and
  *No ART* if any team is un-grouped. Put the last un-grouped team on an ART and the *No ART*
  option goes with it, so a filter left sitting on it falls back to *All ARTs* rather than
  filtering to nothing behind a picker that no longer offers the option. The ART PI view
  shares the same picker, so the scope follows you between them. Everything below it follows: both comparison tables,
  both **All teams** footer rows, the chart, and the count of sprints still in flight. Pick
  *Payments ART* and the footer row reads **All teams on Payments ART**, worked out across
  that ART's teams only.
- The picker says how many teams it's hiding, the same way every other exclusion in the app
  says what it left out — a figure should never move for a reason that isn't on the page.
- With no filter, the table **sorts by ART** so a train's teams sit together, and each team
  carries its ART under its name. The header team picker groups the same way.

Deleting an ART is the cheapest delete in the app: it takes no team, no sprint and no
business value with it — the teams that were on it simply go back to having none.
(Deleting a **PI** is no longer expensive either — it
[offers to keep its sprints](#deleting-a-pi-no-longer-deletes-its-sprints).) The ART PI
tab goes away with the last ART, and the figures it showed are all still on each team's own
Current PI page.

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
how much **new work** that leaves to pull off the backlog, and — see
[Two figures, not one](#two-figures-not-one) below — a second commitment for a sprint that
has to hold. When the sprint it's aiming at is already
running and has a commitment recorded, it swaps the new-work figure for a comparison
against what the team actually signed up for — there's still time to descope. A running
sprint whose commitment hasn't been entered yet keeps the forecast, since 0 committed is
an unanswered question rather than a small commitment. Comparison 1's **Next sprint target**
column and its total use the adjusted figures, and mark an adjusted team with a ⚑. It warns you when there are fewer than
three sprints of history, when the team's delivery swings by more than 30%, and when the
next sprint up is the IP sprint.

It's a starting point for the planning conversation, not a quota. The sections below cover
the second figure, the forecast that runs the same numbers backwards, and then the things the
history structurally cannot see.

### Two Figures, Not One

**An average is met about half the time. That's what an average is.** Hand a team one number
and it gets read as a floor, and half their sprints then miss a commitment that was never
meant to be safe. A team whose last five sprints ran 5, 5, 5, 5 and 40 has an average of 12
and has cleared 12 exactly once.

So where it makes a difference, the card shows two:

| | |
|---|---|
| **Recommended commitment** | The average — the right number for an ordinary sprint |
| **Reliable commitment** | The largest commitment they met in **all but one** of the sprints in the window |

```
Team Overcommitted · last 4 sprints
  Recommended commitment   20   the average
  Reliable commitment      17   met in 3 of the last 4
```

The second figure is a **counted fact, not a statistic**. It's the second-lowest result in
the window, so "met in 3 of the last 4" is something you can check against the table further
down the page. It's deliberately not a percentile or a standard deviation: over five sprints
a percentile is an interpolation between two of the same five numbers, and a standard
deviation assumes a shape five points can't evidence.

Neither number is the safe answer on its own. Commit at the average and expect to miss about
half the time; commit at the floor every sprint and the team is quietly under-committed,
which comes back as break-in. The gap between the two is the size of the decision, and it
belongs to the planning session.

**The pair only appears when it changes something.** A steady team's two figures land within
a point of each other, and two tiles reading 23 and 23 teach nothing — so a steady team gets
one number and the recent range, which is itself the message. It needs three sprints, too:
dropping one of two leaves an anecdote.

There's one case where the arithmetic is honest and the display would not be. A team dragged
down by a single bad sprint — 10, 30, 32 — has an average of 24 and a second-lowest of 30,
so the "reliable" figure would sit *above* the recommendation. There's no safer number to
offer such a team, because the average is already below what they usually do, so the pair is
simply not shown and the swings warning speaks instead.

Both figures move with an availability adjustment, because both are recommendations for next
sprint. The **recent range** and the swings warning never do — those describe what already
happened, and a team knocked down for next month's leave must not read as erratic because of
it.

### How Long Would It Take?

The capacity card fixes the sprint and asks how much fits. The card below it turns that round:
type a number of story points — a backlog, an epic, a release — and it says how many sprints
that would take.

```
120 points would take 7 to 8 sprints.
PI 2026.3 has no delivery sprints left — the next slot is the IP sprint —
so all of this falls into the PI after it.

7 at the 20 points a sprint they average, 8 at the 17 they finished in 3 of the last 4.
```

**The rate is committed points finished, never velocity** — the same stance as the capacity
target, for the same reason. Velocity counts the break-in that turns up mid-sprint, and that
is by definition *not* the work you asked about. Forecast at velocity and you've assumed the
whole sprint goes to this piece while the interruptions keep arriving anyway, which is how a
confident date slips a sprint at a time.

It's always a **range**, from the same two rates the [capacity card](#two-figures-not-one)
shows, and each end names what it assumes. A single number would be a guess wearing a
forecast's clothes.

Where the team's dates are known it adds calendar weeks and a landing date. **Delivery
sprints and calendar sprints aren't the same thing**: unless you've opted the IP sprint into
the window, sprint 6 delivers none of this work, so a span long enough to cross one takes an
extra fortnight of calendar per crossing. The dates account for that. It also says whether
the work fits in the delivery sprints left in the current PI, which is the question this one
usually turns into.

**Nothing is typed here is saved**, and that's deliberate. A backlog total is only a number,
so the numbers-and-dates rule would allow storing it — but it goes stale the moment somebody
grooms the backlog, and a saved figure would have the app confidently forecasting from a
total nobody has checked since. Asking each time costs one box and can't be wrong.

Past **two PIs** it keeps the sprint count, drops the dates and says why. A rate taken from a
five-sprint window can't speak to the next hundred: the team, the backlog and the way you
size things will all have moved long before you get there.

### When a Team Has Room for More

The method has one blind spot, and it's the only one the app can spot for itself. The
recommendation is the average of committed points *completed*, so it can never rise above
what the team has been committing to. That's the right answer for a team that misses its
commitment, and a trap for one that clears it.

Work brought in late — because the commitment is finished, nearly finished, or blocked and
there's nothing else to pick up — lands in **break-in**, counts towards velocity, and is
invisible to committed-points-completed. Do that every sprint and the app keeps handing
back the figure the team already commits to, with the spare capacity they've just
demonstrated nowhere in the number.

So the card says it in words instead. When a clear majority of the window shows a sprint
whose commitment was finished *and* extra work completed on top, an amber **↗ Room for
more** badge appears above the tiles — the same badge-led line the *sprints left out*
notes use — saying how many sprints showed the pattern and roughly how many extra points
a sprint they took on. "How this is worked out" spells out what's behind it.

The amber is the same "there's something here to read" amber as *⚑ Adjusted* and *◐ In
progress*, not a RAG band: the finding is neither good news nor bad, and the tiles beside
it are where the colour-coded verdicts live. The ↗ carries the meaning on its own, so the
colour is never the only signal.

Three deliberate limits:

- **The recommendation itself doesn't move.** Adding the extra on would assume late work
  keeps turning up, which is the same mistake as committing to velocity — and unlike the
  commitment, none of it was planned. The note is a prompt for the planning session; the
  number stays a figure the team has proven it can finish.
- **It needs three sprints and a clear majority of them.** Two sprints are an anecdote, and
  this finding talks a team into signing up for more work.
- **It never fires for a team that over-commits on average.** That team already has the
  opposite problem, and the card tells them so instead — the two findings are worked out in
  one place so they can't both be on.

It also explains a reading that looks contradictory on the tiles above: a team can sit at
100% commitment completion and a red break-in figure at the same time. These figures can't
tell work a team went looking for from work that landed on them, so when the note is
showing and break-in is off target, the card says to read the two together.

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
in this browser and isn't part of your data, so it never goes into a backup file and a
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

## Getting the Numbers Out

Every table in the app carries a **Copy** and a **⬇ CSV** button in its heading:

| View | Table |
|---|---|
| **Current PI** | Sprint by sprint, with the PI total row |
| **Rolling 5** | The sprints in the window |
| **ART PI** | Every team on the train, with the ART row |
| **All teams** | Comparison 1 and Comparison 2, separately |

**Copy** puts the table on the clipboard tab-separated, which pastes as a real grid into a
status email, a slide or a spreadsheet. **⬇ CSV** downloads a file — `sprint-velocity-all-teams-avg-2026-08-20.csv`
— for keeping or for opening in Excel later. (Tabs for the clipboard because a pasted CSV
lands as a single column of text and has to be run through Text to Columns; a file has to be
a CSV because that's what a spreadsheet opens.)

**What you export is what you're looking at.** The tables are read off the page rather than
rebuilt from the stored data, so every filter you've set — which ART, which PI, whether
running sprints count, whether sprint 6 is in — is already applied, and the file can't
quietly disagree with the screen it came from. The display furniture is dropped: the ✓ / ! /
✕ glyphs, their screen-reader text, and the ⚑ markers, none of which are values. The
caption above each table already says what the ⚑ meant.

Percentages come out as they're shown — `84.6%`, not `0.8462` — because these go into
reports, and the [decimal rule](#the-metrics) that stops a figure contradicting its own
colour applies just as much on a slide.

**Cells that a spreadsheet would run as a formula are defused.** A name beginning `=`, `+`
or `@` gets a leading apostrophe, so opening the file can't execute anything. Everything the
app renders to HTML is escaped for the same class of reason; a CSV is simply another place
text goes somewhere it can be interpreted. A genuine negative number is left alone.

The buttons work in a [shared read-only link](#sharing-a-read-only-link) too. Everything else
a shared view takes away, it takes away because it would *write*; this writes nothing and can
only hand back figures already on the page — and letting the person you sent it to paste the
table into their own notes is rather the point.

For the whole dataset rather than one table, **Back up** still exports the complete JSON —
that's the one to keep, and the only one that can be restored.

## Your Data

`localStorage` in your own browser is the source of truth, and since
[sync was removed](#cross-device-sync-was-removed-2026-08-20) it is the **only** copy.
**No account is needed and no data leaves your machine** — the page's CSP names no external
origin at all, so the browser itself refuses to let it try.

What's saved per sprint is the seven figures, its dates, its status, and — if you've set
one — whether it's left out of the rolling average and which of the fixed reasons applies.
A capacity adjustment saves as a percentage and a reason code against a team and a sprint
slot. Nothing else.

The names you type — teams, ARTs and PIs — are **capped at 120 characters as they're
written**, not only on the way back in: the object you name is the one that reaches
`localStorage`, so the cap is applied as you type as well as at the boundary that reads a
saved, imported or shared copy. Percentages and reason codes
pass that same boundary, so a hand-edited file can't widen either.

**Back up & restore** — the *Back up* button exports everything as a JSON file
(`sprint-velocity-YYYY-MM-DD.json`, dated in local time) and imports it back. Useful as a
backup, for moving between browsers, or for handing a colleague a starting point.

**Starting again** — folded away at the foot of the same dialog, under *Start again*, is
**Delete all data**. It's behind a fold on purpose: the one irreversible action in the app
shouldn't sit a mis-click away from Export. Pressing it opens a confirmation of its own that
says exactly how much is going ("This deletes 2 teams, 1 PI and 3 recorded sprints") and
offers the same JSON export as a last chance to keep any of it. There is no "…and every
device you own" line any more: since sync was removed there is exactly one copy, and it is
the one in this browser. Your theme survives; it lives under its own key rather than with the data.

**If one device is behind** — every saved copy carries the data format the app that wrote
it understood. A copy written by a *newer* version than the one you're running won't be
opened: you get a card saying so, nothing is changed or deleted, and reloading picks up the
current version. That matters most on a device that's been offline for a while, where the
browser can still be running an older cached copy of the app while another device has moved
on. A backup file from a newer version is refused the same way, and a share link from one
tells the reader the link is fine and their copy of the app is behind.

**Deletion requests** — there is nothing left to delete. The app stopped syncing on
2026-08-20 and the Firestore collection was emptied by hand the same day, so no copy of
anyone's data exists on the server side. `DATA_DELETION.md` was the runbook for a deletion
request and was removed with the data it described: a runbook that confidently describes
something that no longer exists is worse than none. `git log` has it if the history is ever
wanted.

## Working Offline

The app keeps a copy of itself on your device, so it opens with no network at all — on a
train, on hotel wifi, or when the work VPN is being difficult. Your teams and sprints were
always local, so once the page itself loads everything works: adding sprints, the charts,
the targets, export, share links, backup and restore. There is no longer any part of the app
that needs the network — sync was the one exception, and it is gone.

What's kept is only the app's own public files — the page, the stylesheet, the chart
library and the icon, the same files anyone can read on GitHub. **Nothing of yours is ever
put there**, which matters more than it sounds: every one of these apps shares a single
browser origin, so that cache is not private to this app.

The network is always tried **first**, and the stored copy is used only when it genuinely
doesn't answer (or takes more than five seconds). So you can't be left running an old
version while you're online — and if a device does end up behind, the version check
described under [Your Data](#your-data) stops it misreading anything.

`sw-kill.js` sits in the repo unused, as an escape hatch: copying it over `sw.js` and
pushing makes every installed copy uninstall itself and go back to being an ordinary
online-only page.

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
GitHub Pages never sees them, and there is no one else in the path at all. Nothing is uploaded, no account is involved,
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
run code in your browser when you opened the link — reaching your own saved data, which the
read-only guard does not cover. The same check runs on an imported backup file.

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
sprints were left out and why: an import says so before you commit to it, and a link says so
once it opens.

Links run to a few hundred characters for a typical team. If one gets long enough that a mail
client might break it across two lines, the dialog says so and points at the two things that
shorten it — fewer teams, or less history.

## Cross-Device Sync Was Removed (2026-08-20)

This app used to offer optional Google sign-in, which mirrored your data to a Firestore
database in the `sprintvelocity-141b7` Firebase project. **It is gone.** Not disabled behind a
`null` config — removed: the module, the sign-in button, the which-copy-do-you-want dialog,
the `firestore.rules` file, `svAdopt()`/`svCounts()`/`cloudPush`/`cloudFlush`/`svSignedIn`
and every Google address in the Content-Security-Policy went in one commit. Flow Metrics, the
sibling app, had the identical module removed in the same sweep.

**Why.** This app holds figures copied out of a work Jira. Sync meant a copy of them sat in a
personal Firebase project, which is a place work data has no particular business being — and
the feature was carrying a fair amount of complexity for it: a hostname-blocking workaround,
a reconciliation dialog, an empty-copy-never-wins rule, a server-clock ordering scheme, and a
whole class of failure ("looks fine, hasn't pushed for weeks") that had to be surfaced in the
UI because it couldn't be prevented. Removing it deleted all of that at once.

**What replaces it.** **Back up** downloads a file; **Restore** reads one back. That is how
you move data between devices now, and it has the property sync never had: you can see
exactly what moved, and it goes nowhere you didn't put it.

**What the removal is worth checking against.** The claim is not "the Firebase code is gone"
— it is that the page cannot reach the network at all. The CSP at the top of `index.html`
names **no external origin**, and spells out `connect-src 'none'` rather than leaving it to
the default, because that is the directive that would carry work data off the device.
`tests.html` pins both, plus a word-list tripwire over the app's code (comments stripped to a
fixed point, so the note explaining the removal can still name Firebase and be findable by
grep) so a paste-back of the old module fails loudly rather than shipping.

**Leftovers are deleted, not merely unread.** `clearSyncLeftovers()` runs on every load and
removes `sv-sync-uid` and `sv-updated`. The first of those is a Google account id — the only
personally identifying thing this app ever wrote down — and keeping it after removing the
feature that needed it would be keeping an identifier for no reason. Pinned by a test that
plants both keys, boots the app and checks they are gone.

**The data written before the removal was deleted too**, on the same day — removing the
client deletes nothing server-side, so the `sprintvelocity` collection was emptied by hand in
the Firebase console as a separate deliberate step. `privacy.html` says so rather than
promising deletion on request, and `DATA_DELETION.md` went with the data it described.

**If it is ever wanted back**, `git log` has the whole module in one commit — including the
Google Identity Services workaround for corporate networks that block
`<project>.firebaseapp.com` **per hostname**, which was real, was measured, and would be
needed again. Putting it back means putting the CSP origins back too, and the tests above
will say so.


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
    ├── chart.min.js  vendored Chart.js UMD build — no CDN, no network needed
    ├── sw.js         service worker: keeps the files above on your device
    └── sw-kill.js    the escape hatch, if sw.js ever needs uninstalling
            ├── all state ──► browser localStorage (the source of truth, and the
            │                 only copy — sync was removed on 2026-08-20)
            ├── backup    ──► a JSON file you download and restore yourself; the
            │                 only way to move data between devices
            └── shared    ──► the URL fragment itself (#share=…), read-only, never
                              uploaded and never written back to localStorage
```

No server of our own. No build, no dependencies to install, no npm.

[`privacy.html`](https://eagleadams86.github.io/sprint-velocity/privacy.html) spells out
what the app stores and where — linked from the app's footer, beside a **How it works** link
to this README (GitHub renders it on the repo's front page), for anyone who wants more than
the in-app ⓘ dialogs. Fellow Scrum Masters use this app with their own data, so the policy
exists for them as much as for the author: what is stored, that it stays in their browser,
that share links upload nothing, and — for anyone who used sync before it was removed — how
to have the leftover copy deleted.

A Content Security Policy `<meta>` tag in `index.html` **names no external origin at all**.
Since sync was removed there is nothing for it to allow: no CDN, no Google, no analytics.
`default-src 'none'` is therefore the real rule rather than a formality, and each directive
is an exception it has to earn — including `connect-src 'none'`, spelled out rather than left
to the default because it is the one directive that would carry work data off the device, and
`worker-src 'self'` for `sw.js`, spelled out rather than resolved through the fallback chain.
If a new external endpoint is ever added,
it has to be added to the CSP too or the browser will (deliberately) block it.

## Working on It Locally

```bash
python3 -m http.server 8012
```

Then open http://localhost:8012. (The desktop app's preview pane reads
`.claude/launch.json`, which is set to the same port.)

**Tests:** open http://localhost:8012/tests.html — it loads the real `index.html` in a
hidden iframe and pins the pure functions. The page prints its own count and group total;
this paragraph deliberately doesn't, having said "96 checks in 18 groups" while the suite
ran 141 in 22. What it covers: the Jira paste
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
`/sprint-velocity/tests.html`, where that iframe would be reading and writing somebody's real
teams. A gate at the foot of `tests.html` checks `location.hostname` and, anywhere but
`localhost` / `127.0.0.1` / `[::1]`, never creates the iframe at all — it explains why and says how to run the suite properly. CI
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

## Ownership and Licence

Sprint Predictability is an independent personal project by Charles Adams — built on personally owned
hardware, with a personally paid-for Claude subscription, in a personal GitHub account. No
employer equipment, funding or code went into it, and since 2026-08-20 it has no server or
database behind it either: your data stays in your own browser.

It holds no employer information either, and that is a property of the design rather than a
promise: there is no free-text field anywhere in the app, and the storage whitelist admits
only numbers, dates and short fixed labels. Text you paste in is parsed in the browser and
thrown away — ticket keys, summaries and comments are never stored, transmitted or
committed. Adding a stored field means adding it to that whitelist, or it is deliberately
stripped.

Share it freely: it is [MIT licensed](LICENSE), so anyone — including a company you work
for — may use, modify and redistribute it. Running it inside an organisation conveys no
ownership of it; permission comes from that licence, granted by the author as copyright
holder. [NOTICE](NOTICE) records this in full.

## The Landmarks (2026-08-21)

`<main>` opens **above** the tab strip, not below it. It used to wrap the tab panel alone,
which had two consequences: the tabs sat in no landmark at all (axe-core's `region` rule),
and — the reason worth acting on — **the skip link jumped past them**, so a keyboard user who
took "Skip to content" had the entire tab row behind them, reachable only by shift-tabbing
back. The tabs and the panel they drive are one widget, so the landmark goes round both. The
share bar comes inside with them: it describes what is on screen, so it is content rather
than furniture.

`role="tabpanel"` still goes on the inner div and never on `<main>` — putting a role ON an
element IS its role, so it would silently replace the landmark. That older note stands
unchanged.

Every page in this repo passes axe-core at WCAG 2.1 A and AA plus its best-practice rules, in
all four themes, with data loaded and on every tab.
