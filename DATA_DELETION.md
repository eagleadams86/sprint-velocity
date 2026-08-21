# Handling a data-deletion request

> **Sync was removed from the app on 2026-08-20.** Nothing new is written to Firebase from
> anywhere, and the client code, the sign-in button and the `firestore.rules` file are gone
> from this repo. **This runbook is still live**, because removing the client does not
> delete what the server already holds: every document written before that date is still
> there, and [privacy.html](privacy.html) still promises that emailing
> eagleadams86@gmail.com gets it deleted.
>
> The standing question this raises, which is a decision rather than a task: the whole
> collection could be deleted at once, or the Firebase project deleted outright, which would
> retire this document with it. Until that happens, the procedure below is what honours the
> promise.

Firebase project: **sprintvelocity-141b7**

## What exists, and where

Sync stored exactly one Firestore document per signed-in user:

    sprintvelocity/{uid}  →  { data, updatedAt }

`{uid}` is the user's Firebase Auth UID. The code that wrote it (`docRef()`,
`Fs.doc(db, 'sprintvelocity', user.uid)`) and the security rules that confined each account
to its own document were both removed with sync — `git log` has them if you need to check
what the shape was. The rules are still deployed in the console, and that is what still
guards the documents; nothing about removing the client changed them.

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

Sign-in was Google-only and anonymous auth was never enabled, so every account has a real
email address attached. There is no category of user you'd be unable to look up.

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

- **Their local browser copy.** The local copy is now the *only* copy the app itself uses.
  Only they can clear it — site data in browser settings, or the app's own clear-data
  control.
- **Share links they've already sent.** Snapshot links carry the data inside the URL
  itself; there is no server-side record to revoke. `index.html` is honest about this in the
  share UI ("no way to withdraw one once sent"). If they've shared a link, the copy in that
  URL is beyond anyone's reach, including yours.

Note that the app no longer signs anyone in at all, so there is no "sign out and it stops"
step to offer: syncing already stopped for everyone on 2026-08-20. What remains is purely
historical, which is what makes deleting it on request the whole of the job.

## Reply template

> Done — the Sprint Velocity data that was synced to your account has been deleted from the
> database, along with the account record holding your email address. Nothing of yours
> remains on my side.
>
> For context: the app stopped syncing to Google entirely on 20 August 2026 — it now keeps
> everything in your own browser and has no server behind it — so what I deleted was the
> copy left over from before that.
>
> Two things I can't reach from here: the copy in your own browser (clear the site's data,
> or use the app's clear-data control), and any share link you've already sent — those
> carry the data in the link itself, so there's nothing on my end to revoke.

## Keeping this true

This document describes what is in the Firebase console, not what is in this repo — the
code it used to describe is gone. It stays accurate as long as the collection name and the
sign-in provider in the console stay as they are. **When the collection or the project is
finally deleted, delete this file and the promise in `privacy.html` in the same commit** — a
deletion runbook that quietly describes something that no longer exists is worse than none,
because it deletes the wrong thing confidently.
