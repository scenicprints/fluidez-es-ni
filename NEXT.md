# START HERE — what to build next

**The course is written. Two jobs left, in this order: make the reader able to
look every word up, then publish.** Both are approved — see *THE JOB* below.
Read `HANDOFF.md` in this same folder for the full context, the gates and the
reasoning behind them. This file is the short version.

| | | |
|---|---|---|
| Stories | **185 / 185** | 77,544 running words |
| Scenes | **95** | was 40 |
| Patterns | **52** | was 5, and two of those five were dead |
| Verbs | **123 verbs, 6 tenses** | was 45 and 3 |

All of it passes the gates. **None of it is published** except the dictionary
and `verbs.json` — see *What already goes live on every push* below.

---

## The one-paragraph version

Kevin Wagner is learning Nicaraguan Spanish because **his wife is
Nicaraguan**. He needs to talk to her and to her family — love, arguments,
apology, being teased by in-laws, funerals, holidays. Every word must be
**Managua Spanish**: voseo, never tú, never vosotros, no Mexicanisms, no
Peninsular vocabulary. This is enforced by a build gate, not by care. The app
also teaches Nicaragua itself — customs, holidays, geography — but **Spanish is
the focal point** and the vocabulary schedule decides story order.

---

## Do this first, every session

```bash
cd <this repo>
python .github/scripts/stage.py --root .
```

That prints exactly where things stand and writes `content/plan/PROGRESS.md`.
It never publishes anything.

---

## Where the course stands

| Phase | | Written |
|---|---|---|
| 0 | Survival | 16 / 16 |
| 1 | Getting Around | 18 / 18 |
| 2 | Connecting | 26 / 26 |
| 3 | Holding Your Own | 26 / 26 |
| 4 | Close to the Heart | 35 / 35 |
| 5 | Fitting In | 26 / 26 |
| 6 | Sounding Local | 20 / 20 |
| 7 | Native-Like | 18 / 18 |

**185 of 185. 77,544 running words. 1,714 words taught, median seven
encounters, 691 reaching ten. Dialect clean across lessons AND scenes: 763
voseo forms, zero off-dialect.**

Story length ran ~310 words for phases 0–4 (written by an earlier pass) and
450–875 for phases 5–7. The 148,000-word figure `stage.py` still prints is
the original plan's estimate and was never met by any phase; it is a target,
not a gate, and nothing fails because of it.

Warm-ups: 177 of the 185 stories have one, median 2 words. The 8 that do not
are stories whose vocabulary is entirely words the learner has been reading for
months — honest blanks. See `reconcile.py` for why that number used to be 95.

---

## The three content jobs — all DONE

### 1. ~~Scenes~~ — DONE. 40 became 95

`content/scenarios/`, `sc41`–`sc95`. Phase-gated and weighted the way the
spine is: 0:8 1:9 2:11 3:11 **4:19** 5:14 6:12 7:11. Four steps, three options,
one `good` per step. They track the stories — the caponera, the Purísima door,
the cuñados' test, the tope, the indirecta about the roof, ni modo, the bus
stop where nobody asks where you are from.

Two things learned while writing them, worth keeping:

- **`screens.js` speaks `step.es` aloud.** A step prompt has to be something a
  person actually says. A bare stage direction gets read out by the voice.
  Where an action matters, put it in a parenthesis in FRONT of a real line.
  Options are only rendered and tapped, never spoken, so a parenthetical
  option (`(no decir nada y esperar)`) is fine and is sometimes the only right
  answer a phase-7 scene has. `sc39` still has one bare direction from the
  original 40; left alone.
- The dialect gate reads scenes as well as lessons, and `stage.py` now loads
  everything in `scenarios/` off disk whether it is in the manifest or not, so
  unpublished scenes are checked exactly like unpublished stories.

**Still out of `manifest.json`**, same as the lessons.

### 2. ~~Patterns~~ — DONE. 5 became 52

47 new ones in `content/patterns/spine.json`, and the original five in
`core.json` repaired. They run from `saludos` and `usted_vos` through the
tenses to `depende`, `indirecta`, `ni modo`, `uno`, `tono_serio` and `citar`.

**A trigger has to be a dictionary LEMMA that the course can actually teach.**
`screens.js` counts how many of a pattern's triggers the learner has an
exposure against, and exposures are recorded against the *resolved lemma* —
`store.recordExposure` is handed `resolve(cleanWord(raw))`. So:

- A conjugated form as a trigger has no vocab entry and **can never be met**.
  The shipped `ser_estar` listed `soy es son estoy está están` with `min: 4`.
  Every one is a form. It could not unlock for anybody, ever. `me_gusta` was
  dead too — one of its three triggers never occurs in the course.
- The lemma does *not* have to appear as itself. `amar` is earnable from every
  `te amo`, because that resolves to `amar`. Check reachability through
  `forms`, not against the raw text.

`stage.py` now enforces both, and `pats.py`-style emitters should validate
before writing. **Do not hand-write a trigger list without running stage.py.**

`spine.json` is deliberately **not** in the manifest yet — see Publishing.

### 3. ~~Verbs~~ — DONE. 45 → 123, and 3 tenses → 6

`content/verbs.json` is generated. Run
`python .github/scripts/verbs_build.py` from the repo root to rebuild it — the
rule tables live at the top of that file, so a missed stem-changer is a
one-line fix there rather than a hand edit to 3,000 lines of JSON. 123 drill
verbs, chosen by how often the course actually uses them, 51 of them with a
full irregular table.

Tenses are now **present, past, imperfect, future, conditional, subjunctive**.
No app change was needed: `engine.js conjugate()` special-cases only `future`,
and conditional builds correctly from stem + ending.

Two things it fixed, both shipping today:

- **`cerrar` and `perder` were in `drill` and in neither table**, so the
  trainer has been teaching Kevin **"cerro"** and **"perdo"**. `engine.js
  conjugate()` falls back to the regular table when a tense is missing, so a
  verb that is irregular and absent produces a wrong form silently. Anything
  added to `drill` MUST be checked against that.
- The whole table is voseo-correct: vos does not diphthongise (`vos pensás`,
  `vos podés`), and the subjunctive is the voseo one (`que vos hablés, comás,
  vivás, tengás`).

**The voseo imperative is stored but NOT drillable.** Each irregular verb has
an `imperative` key with one form, and `forms.py` reads every tense of every
irregular verb when it builds the inflection map, so `hablá`, `tené`, `vení`,
`andá` are all tappable in the reader. It is deliberately **not** in `tenses`,
because `startVerbs()` draws a random subject index 0–4 for whatever tense it
picks and a one-slot tense would hand the drill an `undefined`. Drilling it
needs a change in the **app repo** (`scenicprints/fluidez`): teach
`startVerbs()` that some tenses have one form and no subject. Small job, wrong
repo.

Regenerating: the builder refuses to write unless it reproduces the original 21
irregulars' present/past/future byte-for-byte. That check caught three real
errors while it was being written; do not remove it.

Review, Word Order, Listening and Shadowing need no authoring — they generate
from lesson sentences and grew with every batch.

---

## Open question for Kevin: 95 of 185 warm-ups are empty

This needs a decision before publishing, and it is his, not an agent's.

`reconcile.py` sets each story's `wu` to the words that story genuinely hammers
**and** that genuinely come back. It refuses a word if any earlier story
already claimed it (`claimed`) or if it fails RETURN (6 appearances in the next
25 stories). Across a 185-story course those two rules starve the later
stories: **95 stories end with no warm-up at all, and the median warm-up is
zero words.**

Both rules are individually right and neither should be quietly weakened. But
the warm-up is a feature Kevin specifically asked to have restored, and half
the course now has none. Measured on the finished course:

| variant | empty warm-ups | median | total wu words |
|---|---|---|---|
| today — claimed + return | **95** | 0 | 162 |
| allow a word in more than one warm-up | 36 | 2 | 422 |
| keep claimed, drop the return check | 42 | 2 | 477 |
| drop both | 7 | 4 | 823 |

The cheapest honest fix is the second row: let a word be warmed up again in a
later story that also teaches it hard. That is not a weaker claim — the story
really does hammer it — and re-warming a word 40 stories later is spacing, not
duplication. **Do not change `reconcile.py` without Kevin saying so.**

Related, and the reason RETURN bites hardest in phase 5: a festival noun
(`procesión`, `aserrín`, `chischil`, `gigantona`) cannot honestly appear in six
of the following twenty-five stories. The story teaches it properly and the
gate still refuses the claim.

---

## Two gate false positives found while writing phases 5–7

Both were worked around in the content, not in the gate. Flagged so nobody
re-discovers them:

- **`camión`** is flagged as Mexican. In Nicaragua it is the ordinary word for
  a lorry; the Mexican sense is *bus*. A word list cannot tell those apart.
  Worked around with `rastra`.
- **`vale`** is flagged as Peninsular. It also happens to be the third-person
  of `valer` — `eso vale más que…` is perfectly Nicaraguan. Worked around by
  rewriting with `contar` and `pesar`.

Neither ban should come off casually; both are catching a real thing most of
the time. This is a note for whoever hits them next.

---

## A dictionary trap that costs tappability

`forms.py` drops any inflection two lemmas could both produce. **The
dictionary contains 17 reflexive/plain pairs** — `quedar`/`quedarse`,
`callar`/`callarse`, `perder`/`perderse`, `sentir`/`sentirse`,
`parecer`/`parecerse` and so on. Every shared form of those pairs is dropped
as ambiguous, so `queda`, `parece`, `siente`, `calla` are dead on the page:
not tappable, no exposure, no strength colour. These are among the commonest
verbs in the language.

`forms.py` already computes a `counts` dict to settle collisions and then never
uses it, which suggests the fix was intended and not finished. Leave it alone
until Kevin decides — but **never add a lemma whose ±`se` twin is already an
entry**, or you make things worse. Adding `tragar` beside `tragarse` cost
`traga` its mapping until it was pulled back out.

---

## What already goes live on every push

Most of this work is invisible to Kevin until the manifest flip. **Two things
are not**, because the manifest already lists them, and CI rebuilds
`pack.json` on every push to main:

- **`content/dictionary/*.json`** — every entry added while writing the course
  is live now. That is fine and was always the design: more words become
  tappable, no lesson changes.
- **`content/momo.json`** — the mascot. The sixteen dead lines are live-fixed,
  including the two rewordings.
- **`content/verbs.json`** — the Verb Trainer. The rebuild is live: the
  `cerro`/`perdo` fix, and the three new tenses. Of the 123 drill verbs, 20 are
  not reachable from the 81 lessons he is actually reading, so he will
  occasionally be asked to conjugate an infinitive he has not met. All 45 of
  the original drill verbs are still there; nothing was taken away. If that
  turns out to be unwelcome, reverting is one commit — but the two wrong forms
  should not go back.

Nothing else does. Lessons, scenes and `patterns/spine.json` are all sitting on
disk unlisted.

## THE JOB: fix the tappability, then publish

Kevin decided this on 2026-08-21, after being shown the list below:

> *"We can leave 4 the way it is. For the rest, let's let the next claude agent
> fix them and publish."*

So: do 1, 2 and 3. Then publish. **Item 4 is settled — leave the audio alone.**
Item 5 is in the app repo and is not yours unless you go there.

Items 1, 2 and 3 are the same problem seen from three sides — the reader cannot
look a word up — and they want one pass over `forms.py` and the dictionary, not
three. Do them together and measure with the `lookups` line in `stage.py`,
which is at **93.4%** today. Every point of that is roughly 780 words on the
page that go from dead to tappable.

1. **924 words on the page have no dictionary entry at all** — 6.6% of the
   reader. Not tappable, no exposure, no strength colour. `stage.py` lists them
   in `content/plan/needs-entry.txt` every run. Most are clitic-attached
   infinitives (`acompañarla`, `arreglarlo`) that `forms.py` cannot generate,
   and the rest are genuinely missing lemmas. Two separate fixes: teach
   `forms.py` to strip `-lo -la -le -me -te -se -nos -los -las -les` from an
   infinitive, and add the lemmas that are actually missing.

2. **16 reflexive/plain dictionary pairs cost 485 tokens their tappability.**
   `quedar`/`quedarse`, `callar`/`callarse`, `perder`/`perderse`,
   `sentir`/`sentirse` and twelve more. `forms.py` drops any inflection two
   lemmas could both produce, so `queda`, `parece`, `siente`, `acaba` and
   `levanta` are dead on the page — and these are among the commonest verbs in
   the language. `forms.py` already computes a `counts` dict to settle exactly
   this and then never uses it, which looks like a fix somebody started.
   **Never add a lemma whose ±`se` twin is already an entry** or you make it
   worse.

3. **62 dictionary entries are conjugated forms, not infinitives** — `llega`,
   `entiendo`, `pasa`, `era`, `fue`, `gusta`. HANDOFF says these should not
   exist and 164 have already been merged away; these are what is left.
   Tapping `llega` shows "arrives" instead of opening `llegar`, and the memory
   model treats them as separate words. `reconcile.py` keeps them off warm-up
   cards via `NOT_A_LEMMA`, which is a plaster, not the fix. Careful: the vos
   imperatives the course genuinely teaches as words — `andá`, `mirá`, `vení`,
   `sentate`, `fijate`, `decime` — are NOT in this class and must stay.

4. ~~**Audio is `es-MX`**~~ — **DECIDED 2026-08-21: leave it.** There is no
   Nicaraguan TTS voice on any platform and Kevin has looked at the trade and
   chosen to live with it. Do not reopen this, do not "improve" it, do not swap
   the voice.

5. **The voseo imperative is not drillable** — an **app-repo** change
   (`scenicprints/fluidez`): teach `startVerbs()` that some tenses have one
   form and no subject. Not part of this job.

## Publishing — APPROVED, once 1–3 are done

Kevin gave the go-ahead on 2026-08-21. The stories, scenes and
`patterns/spine.json` have been sitting on disk unlisted the whole time so that
a half-finished course never landed in the middle of the one he uses daily.
That reason has expired: the course is finished.

Do the tappability pass FIRST — publishing locks in whatever the reader can and
cannot look up, and fixing it afterwards means a second pack push.

`manifest.json` needs
**four** edits, not one. Everything written since the rewrite began is sitting
on disk unlisted, and `build-pack.py` only ever loads what the manifest names:

1. Replace the `lessons` list with the spine ids (`p0-01` … `p7-18`).
2. Replace the `scenarios` list with all 95 — each row is
   `{id, title, desc, phase, path}` and `phase` comes from the file's `ph`.
   There is a helper shape to copy in the existing rows.
3. Add `"patterns/spine.json"` to the `patterns` list, beside `core.json`.
4. Delete `content/lessons/s*.json` (the old 81).

Then push. CI rebuilds `content/pack.json` and every app picks it up with **no
app release**.

Run `python .github/scripts/stage.py --root .` first and last. Its `written`,
`scenes` and `patterns` lines each print how many are published versus how many
exist, so the gap tells you what the manifest is still missing.

---

## The loop for one batch of content

1. **Write** the JSON. Emit a batch from one throwaway Python file rather than
   one tool call each.
2. `python .github/scripts/stage.py --root .`
3. **Add the dictionary entries** it lists in `content/plan/needs-entry.txt`
   to `content/dictionary/spine.json`. A word with no entry cannot be counted
   at all, so this clears most DENSITY failures. Skip proper nouns, skip
   inflections, and check the reflexive-twin trap above.
4. `python .github/scripts/reconcile.py`
5. Repeat 2 until no `PROBLEM:` lines. Commit and push.
   **`git pull --rebase` first** — this repo's CI commits the rebuilt pack back
   to main, so a plain push is rejected.

---

## The cast, for anything written from here on

**Roberto** (the neighbour's son, twelve at the start, seventeen by phase 5,
gone to Costa Rica and back by phase 7), **doña Carmen** (his mother, the first
house), **don Beto** (the older neighbour, seventy-two by phase 6, a brother
lost in 1979), **doña Chepa** (the pulpería, the barrio's biggest gossip and
its newspaper), **Marcos** (workmate, then compadre — the one who explains
everything), **Lucía** (wife from phase 4), **doña Elena** (the suegra),
**Julio** and **Chino** (her brothers, the protagonist's cuñados), a son called
**Beto**, and from phase 5 on **Delroy** (costeño from Bluefields), **Wilmer**
(from a Jinotega cafetal), **don Emilio** (sixty-eight in phase 6, the real
hierarchy of the workshop) and **Tom** (the Canadian who arrives in p7-15 and
gets the notebook the protagonist once had). The protagonist's nickname is **el
Perdido**. By p7-18 he has been in the country six years.

---

## Traps that have already cost hours

- **Shell heredocs mangle apostrophes and accents on this machine.** Write
  Python and JSON with a file-writing tool, never `bash <<'EOF'` with accented
  content.
- **Watch apostrophes in Python string literals** — `u'her husband's grave'` is
  a syntax error. Use double quotes for those lines.
- **Console output is cp1252** — accents print as `?`. Write results to a file
  and read the file rather than trusting the terminal.
- **`/tmp` in Python is not the bash `/tmp`** on this machine. Use relative
  paths.
- **Never weaken a gate to make content pass.** If a gate fires, first ask
  whether the content is wrong. It usually is.
- **Never let a conjugated form or a plural be its own dictionary entry.**
  Add lemmas only.

## Kevin's working preferences

Plainest possible output. No option menus for simple asks. Do exactly what he
says and do not generalise to adjacent scope. He does not want progress reports
that read like check-ins — just keep working. **He watches agent usage**, so
work in large batches and lean on the gates rather than re-verifying what they
have already proven.
