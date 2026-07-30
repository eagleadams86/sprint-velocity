# Sprint Velocity

A sprint predictability tracker for Scrum Masters. Record what each team committed to,
what they actually finished, and what changed mid-sprint — the app works out commitment
completion, break-in, carryover and velocity, and flags each one against your targets.

**Live:** https://eagleadams86.github.io/sprint-velocity/

Built for Scrum Masters running several teams on a SAFe-style cadence: six sprints to a
Program Increment, with sprint 6 reserved for innovation and planning.

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
want in front of you at the retro, not three sprints later when nobody remembers.

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

Nothing is saved by pasting. **Use these numbers** fills the boxes, you check them, and the
sprint saves only when you press Save sprint. Your "why" notes are never touched. If the
paste can't be read, it says so and shows what it did find rather than filling in zeros.

Both common paste shapes work — tab-separated rows and one-cell-per-line — since browsers
differ in how they copy tables.

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
  commitment completion on one chart, and an instability chart plotting break-in, removed
  and carryover against shaded 15% / 20% threshold bands.
- **All teams** — every team's rolling averages side by side, plus each team's next-sprint
  target in one column, so the one that needs attention is obvious.

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
you can see how much faith the number deserves. It warns you when there are fewer than
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

Seven, picked from the dropdown in the header: **Midnight** (deep indigo/navy, the
default), Dark, Light, Forest, Sepia, Solarized and Synthwave. Your choice is remembered
in this browser and isn't part of your data, so it doesn't sync between devices and a
shared link never carries the sender's theme.

Every one of them meets WCAG AA contrast on the figures, and each series keeps the same
hue throughout — committed grey, completed blue, velocity teal, break-in amber, removed
violet, carryover red — so a chart reads the same way whichever palette you're in. Charts
re-render on a switch, because their colours are resolved when they're built.

---

## Your data

`localStorage` in your own browser is the source of truth. **No account is needed and no
data leaves your machine** unless you choose to sign in.

**Back up & restore** — the *Back up* button exports everything as a JSON file and imports it
back. Useful as a backup, for moving between browsers, or for handing a colleague a
starting point.

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

Links run to a few hundred characters for a typical team. If one gets long enough that a mail
client might break it across two lines, the dialog says so and suggests sharing fewer teams or
leaving notes out.

## Cross-device sync (Firebase, free tier — optional)

Sync is **enabled** in this deployment, backed by the `sprintvelocity-141b7` Firebase
project — the `FIREBASE_CONFIG` object at the bottom `<script type="module">` block of
`index.html` points at it. Signing in is entirely optional: the app is fully usable, and
fully local, without it. Setting that constant back to `null` returns it to local-only mode
and hides all sync UI.

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

---

## Architecture

```
GitHub Pages (static hosting, this repo, main branch)
    ├── index.html    the whole app — markup, styles, logic, no build step
    ├── theme.css     shared design tokens (copied from the lottery repo)
    └── chart.min.js  vendored Chart.js UMD build — no CDN, no network needed
            ├── all state ──► browser localStorage (source of truth, works offline)
            ├── signed in ──► Firestore doc sprintvelocity/{uid} (optional;
            │                 last-write-wins by updatedAt, live onSnapshot updates)
            └── shared    ──► the URL fragment itself (#share=…), read-only, never
                              uploaded and never written back to localStorage
```

No server of our own. No build, no dependencies to install, no npm.

## Working on it locally

```bash
python3 -m http.server 8012
```

Then open http://localhost:8012. (The desktop app's preview pane reads
`.claude/launch.json`, which is set to the same port.)

`theme.css` is a copy of the canonical palette that lives in the
[lottery](https://github.com/eagleadams86/lottery) repo and is left byte-for-byte
identical to it. The app adds its own chart series colours and threshold-band tints at
the top of `index.html`, plus a short block of contrast corrections: this app leans on
red and green to *mean* something, and a few of the borrowed palettes — Solarized most of
all — sit under WCAG AA at that job. Those nudges live in `index.html` so the shared
`theme.css` never has to diverge.
