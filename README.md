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

A sprint with nothing committed shows `—` rather than 0%, and is left out of averages
instead of dragging them down.

Percentages display as whole numbers, except when rounding would land on the wrong side of
a target — 33 of 39 points is 84.6%, so it shows as `84.6%` in yellow rather than as `85%`
in yellow, which would look like a bug. That's the only time you'll see a decimal.

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

Light and Midnight (deep indigo/navy), both meeting WCAG AA contrast. The toggle is in the
header; your choice is remembered. Charts re-render on a theme switch so their colours
follow along.

---

## Your data

`localStorage` in your own browser is the source of truth. **No account is needed and no
data leaves your machine** unless you choose to sign in.

**Back up & restore** — the *Data* button exports everything as a JSON file and imports it
back. Useful as a backup, for moving between browsers, or for handing a colleague a
starting point.

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
            └── signed in ──► Firestore doc sprintvelocity/{uid} (optional;
                              last-write-wins by updatedAt, live onSnapshot updates)
```

No server of our own. No build, no dependencies to install, no npm.

## Working on it locally

```bash
python3 -m http.server 8012
```

Then open http://localhost:8012. (The desktop app's preview pane reads
`.claude/launch.json`, which is set to the same port.)

`theme.css` is a copy of the canonical palette that lives in the
[lottery](https://github.com/eagleadams86/lottery) repo — the app only adds its own chart
series colours and threshold-band tints, defined at the top of `index.html`.
