# Handling a data-deletion request

[privacy.html](privacy.html) promises that emailing eagleadams86@gmail.com gets a user's
synced copy deleted. This is how to actually do that, and how to work out which record is
theirs.

Firebase project: **sprintvelocity-141b7**

## What exists, and where

Sync stores exactly one Firestore document per signed-in user:

    sprintvelocity/{uid}  →  { data, updatedAt }

`{uid}` is the user's Firebase Auth UID — see [`index.html`](index.html) (`docRef()`,
`Fs.doc(db, 'sprintvelocity', user.uid)`) and [`firestore.rules`](firestore.rules), which
refuses any read or write where the document name isn't the caller's own UID.

**The document contains nothing identifying.** No email, no display name, no sync UID goes
into the payload — that's deliberate, and there's a comment in `index.html` saying so. It's
good for privacy but it has one consequence that matters here: *you can never tell whose
data a document is by looking at Firestore.* Authentication holds the only email → UID
mapping there is.

## Finding their document

1. Firebase Console → **Authentication** → Users tab.
2. Search their email address in the search box.
3. Copy the **User UID** from that row.
4. Firestore → `sprintvelocity` → the document whose ID is exactly that UID is theirs.

Sign-in is Google-only (`GoogleAuthProvider` in `index.html`) and anonymous auth is not
enabled, so every account has a real email address attached. There is no category of user
you'd be unable to look up.

## Before deleting: check who's asking

The request must come from the same address that appears on the Auth record. Anyone can
email claiming to be someone else, and there is no undo — deleting the wrong person's PI
history destroys it permanently. If the sending address doesn't match a row in
Authentication, don't guess: reply and ask which address they signed in with.

## Deleting

Do these in order:

1. **Firestore first** — open `sprintvelocity/{uid}`, ⋮ menu → *Delete document*.
2. **Authentication second** — delete the user row.

The order isn't cosmetic. Deleting the Auth record first throws away the only email → UID
mapping, leaving an orphaned Firestore document that can never be attributed to anyone and
so can never be honestly deleted on request.

Deleting the Auth record matters on its own: their email address sitting in Firebase
Authentication is personal data whether or not any sprint data remains.

## What you cannot delete, and should say so

Be straight about these rather than implying a clean sweep:

- **Their local browser copy.** The app is offline-first and the local copy is the primary
  one. Only they can clear it — site data in browser settings, or the app's own clear-data
  control.
- **Share links they've already sent.** Snapshot links carry the data inside the URL
  itself; there is no server-side record to revoke. `index.html` is honest about this in the
  share UI ("no way to withdraw one once sent"). If they've shared a link, the copy in that
  URL is beyond anyone's reach, including yours.

Signing out, on its own, deletes nothing — it just stops future syncing.

## Reply template

> Done — your synced Sprint Velocity data has been deleted from the database, along with
> the account record holding your email address. Nothing of yours remains on my side.
>
> Two things I can't reach from here: the copy in your own browser (clear the site's data,
> or use the app's clear-data control), and any share link you've already sent — those
> carry the data in the link itself, so there's nothing on my end to revoke.

## Keeping this true

This document describes code as of the last time it was checked. If the sync path,
collection name, or sign-in providers change, update this file — a deletion runbook that
quietly describes the old schema is worse than none, because it deletes the wrong thing
confidently.
