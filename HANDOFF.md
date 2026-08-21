# Handoff — writing the Fluidez course

> **If you are a fresh agent, read `NEXT.md` first.** It says what to build
> next, in order, in one page. This file is the reference behind it.

**Read this if you are picking this work up with no prior context.**
It is written for a fresh agent. Everything needed to continue is here or is
reachable from here.

---

## 1. What this is and who it is for

Fluidez teaches **Nicaraguan Spanish** — specifically the Spanish spoken in
Managua — to Kevin Wagner. **His wife is Nicaraguan.** He is not a tourist and
this is not a hobby course. He needs to talk to her, to her family, and to hold
his own with them: love, arguments, apology, being teased by in-laws, funerals,
holidays.

Two consequences he stated directly, both of which override any instinct you
have to make the course more general:

- **Every word must be Nicaraguan.** He does not want to come out of this
  sounding Mexican or Spanish. This is enforced mechanically (§5).
- **The app teaches Nicaragua as well as Spanish** — customs, holidays,
  geography, how people behave — so arriving feels like coming back. But
  **Spanish is the focal point.** He corrected an earlier framing that put
  culture first. The vocabulary schedule decides story order; the cultural
  topic is chosen to carry those words, never the reverse.

His wife is the best fact-checker available for the culture content. Anything
you are not certain about should be flagged for her rather than written
confidently.

---

## 2. Where everything lives

| What | Where |
|---|---|
| Content repo (the course) | `github.com/scenicprints/fluidez-es-ni` |
| App repo (the web app) | `github.com/scenicprints/fluidez` |
| Language registry | `github.com/scenicprints/fluidez-languages` |
| Live app | https://scenicprints.github.io/fluidez/ |
| App working copy | `C:\Users\kwagner\Desktop\Fluidez` |

Nicaraguan Spanish is the **only** language. Luzerndütsch was retired from the
registry; its repo `fluidez-gsw-lu` still exists but is not served.

### Content repo layout

```
content/
  manifest.json              what the pack build reads
  dictionary/core.json       the original 1,166 words
  dictionary/spine.json      words the NEW course adds  <- add here
  dictionary/forms-overrides.json   hand-pinned inflections
  dialect-allow.json         lines allowed to break the dialect rule
  lessons/s*.json            the OLD 81 stories (being replaced)
  lessons/p0-01.json …       the NEW 185 stories        <- write here
  scenarios/sc*.json         40 scenes (to grow to ~95)
  patterns/                  5 patterns (to grow to ~50)
  verbs.json                 45 verbs, 3 tenses (to expand)
  momo.json                  the mascot's 59 lines
  plan/spine.json            THE PLAN — all 185 stories
  plan/PROGRESS.md           auto-written; what is done
.github/scripts/
  build-pack.py              bundles + runs every gate
  dialect.py                 Nicaraguan-only gate
  schedule.py                recycling quota gate
  forms.py                   inflection -> lemma generator
  stage.py                   checks new stories WITHOUT publishing
```

---

## 3. The plan: `content/plan/spine.json`

185 stories, 8 phases, one immigrant, arrival to being told *ya sos nica*.
Each entry carries `id`, `phase`, `title`, `desc`, and three planning fields:

- `spanish` — what language the story teaches (**this drives the order**)
- `nicaragua` — what it teaches about the country
- `beat` — what happens in it

Distribution is deliberately uneven — the people phases are the fat ones:

| Phase | | Stories |
|---|---|---|
| 0 | Survival | 16 |
| 1 | Getting Around | 18 |
| 2 | Connecting | 26 |
| 3 | Holding Your Own | 26 |
| **4** | **Close to the Heart** | **35** |
| 5 | Fitting In | 26 |
| 6 | Sounding Local | 20 |
| 7 | Native-Like | 18 |

**Do not rebalance this.** Phase 4 is the largest on purpose: it is what the
app is for.

### Length ramps

Phase 0 stories are ~450 words; phase 7 stories are ~1,200. Average ~800,
total ~148,000 running words. A phase-0 story cannot be 800 words because
nothing is known yet.

---

## 4. How to write one story

```
1. Pick the next unwritten id from plan/spine.json (see plan/PROGRESS.md).
2. Write content/lessons/<id>.json.
3. python .github/scripts/stage.py --root .
4. Add the missing dictionary entries it lists in plan/needs-entry.txt
   to content/dictionary/spine.json. This clears most DENSITY failures,
   because a word with no entry cannot be counted at all.
5. python .github/scripts/reconcile.py  - rewrites every `wu` to the words
   the story actually hammers AND that actually come back. The warm-up is
   a claim; this makes the claim true.
6. Repeat 3 until it prints no PROBLEM lines, then commit.
```

A COVERAGE failure means the story introduces too much at once. Do not
gut it - add a few lines built from words the course already taught. A
festival story touching the pulpería and the pila you already know is
better writing as well as better arithmetic.

### Story file shape

```json
{
  "id": "p0-01",
  "title": "El calor",
  "desc": "You land, and the heat decides everything",
  "ph": 0,
  "diff": 1,
  "wu": ["calor", "aeropuerto", "..."],
  "sn": [ {"s": "Spanish sentence.", "e": "English translation."} ]
}
```

- `wu` is the warm-up: **8–12 words the story genuinely teaches.** Every one
  must appear 5+ times in `sn` or the build fails.
- **Write to that from the start.** Decide the 8–12 new words first, then
  write the story so each one lands five or six times in different
  sentences. Retrofitting repetition afterwards costs far more than
  planning it, and a warm-up is a CLAIM — only claim what the story does.
- `sn` is one sentence per entry with its English. Short sentences. This is
  what Review, Word Order, Listening and Shadowing all draw from, so every
  sentence must stand alone as a usable line.
- New words need dictionary entries in `dictionary/spine.json`
  (`{"en": …, "pos": …, "g": …, "note": …}`). `stage.py` writes
  `plan/needs-entry.txt` listing what is missing. Proper nouns do not need
  entries.

### Voice

First person, present tense, plain short sentences. Recurring characters are
fine and good — a cast makes long narrative natural. The protagonist's story
does **not** need to track Kevin's own life; he said so explicitly.

---

## 5. The gates — what will reject your work

All three run in `build-pack.py` on every content push, and in `stage.py`
while writing. **Do not weaken a gate to make content pass.**

### `dialect.py` — Nicaraguan only

Rejects tú forms, vosotros, Peninsular and Mexican vocabulary. Hard-won
details you must not "simplify":

- **Tú forms are matched on exact spelling.** The accent IS the difference:
  `comes` is tú, `comés` is vos and correct. Stripping accents there flags
  every correctly-written verb in the course.
- **Foreign words are matched with accents stripped**, or `órale` and `güey`
  walk straight past.
- **Nicaragua shares forms with both dialects it is not.** `vas`, `estás`,
  `das`, `ves` are identical in tú and vos. **Every `-ir` verb** — `decís`,
  `venís`, `vivís`, `salís` — is vosotros in Madrid and vos in Managua,
  spelled the same. None of those may be banned.
- Lines that exist to *teach* the difference are exempt **by line id** in
  `dialect-allow.json`, never by word. Allowing a word globally lets a real
  slip through.

Nicaraguan markers to reach for: `tuani`, `maje`, `chavalo/a`, `chele/a`,
`ideay`, `chunche`, `arrecho` (furious *and* excellent — tone decides),
`puchica`, `dale pues`, `va pues`, `fijate`, `pulpería`, `fritanga`, `birra`,
`reales`, `cuadras`, `chinear`, `pinolero`.

### `schedule.py` — recycling quota

- **Coverage**: ≥88% of a story's dictionary words must already be introduced.
- **Density**: every `wu` word must appear ≥5 times in its own story.
- **Return**: every *content* word must reappear in ≥6 of the next 25 stories.
  Function words (`prep art conj contr pron num`) are exempt.

Return is the load-bearing one. The old course let 42% of its vocabulary
appear in exactly one lesson, median 2 encounters, and 81 lessons left the
learner with 187 words.

### `forms.py` — inflection mapping

Generates form→lemma for forms that actually occur in the text, so `fría`
opens `frío` and strengthens `frío`. Rules already paid for:

- Irregular verbs are **never** rule-generated (the tables turn `estar` into
  `esto` and `dar` into `do`, which are real words with other meanings).
  They come from `verbs.json`.
- A form two lemmas could both produce is **dropped, not guessed**.
- Spanish drops the written accent in the plural: `razón`→`razones`,
  `inglés`→`ingleses`, and every `-ción` noun.
- Reflexive infinitives strip `-se` before generating, or `llamarse`,
  `sentarse`, `irse` produce nothing at all.
- Anything ending in `-o` agrees like an adjective whatever its `pos` says
  (`todo` is tagged `pron`, `mucho` is tagged `adv`).
- **Stem changes are generated speculatively** (o→ue, e→ie, e→i):
  `costar`→`cuesta`, `pensar`→`piensa`, `volver`→`vuelve`. Over-generating
  is safe because anything not actually written is thrown away by the
  corpus filter. Voseo does not stem-change (`vos podés`), and those come
  from the plain stem, so both spellings are covered.
- **Never let a plural be its own entry** when the singular exists.
  `frijol` and `frijoles` were both entries, so every plural counted
  towards a different memory. `dedupe` merged 28 of these; if you add a
  word, add the lemma only.
- Keys starting with `_` in override files are notes, not forms.

### Calibration learned from the first batch

- **Coverage ramps** from 60% at story four to 88% by story 25. Story four
  cannot have 88% known because three stories of Spanish exist.
- **Return is only judged once a word's full 25-story window exists.**
  Scaling it down for short tails demanded that every remaining story
  contain every word, which flagged 109 words in story one.
- **Multi-word warm-up entries** (`gallo pinto`) are counted as phrases in
  the raw text; a word counter can never see them.
- **Conjugated forms must never be their own dictionary entry.** `sos`,
  `tenés`, `podés`, `es`, `está` were all separate entries from `ser`,
  `tener`, `poder`, so the commonest verbs in the language each had their
  memory split in two. 68 merged. The irregular table in `verbs.json` is
  authoritative for this — no gloss comparison, it states the mapping.
- `ven`, `oye`, `di` and `sal` are NOT banned as tú imperatives - they are
  they-see, he-hears, I-gave and salt far more often.

---

## 6. Publishing

**New stories stay OUT of `manifest.json` until the whole course is done.**
Dropping story three of the new course into the middle of the old one only
confuses anyone using the app today. `stage.py` exists precisely so they can
be validated without being published.

When the 185 are complete: replace the `lessons` list in `manifest.json` with
the spine ids, delete `lessons/s*.json`, push. CI rebuilds `content/pack.json`
and every app picks it up with **no app release**.

Three independent update lanes, all working:
1. App code → push to `fluidez` main → CI stamps a version → Pages.
2. Lessons → push JSON here → CI rebuilds the pack. **No app release.**
3. New language → new repo + a line in the registry. **No app release.**

---

## 7. Still to do

- [x] **Stories** — 185 of 185 written. 77,288 running words, 1,714 words
      taught, median seven encounters. See `plan/PROGRESS.md`. Two things
      surfaced by finishing them are written up in `NEXT.md` and need Kevin's
      decision before publishing: **95 of 185 warm-ups end up empty** because
      `reconcile.py` will not let two stories claim the same word, and
      **17 reflexive/plain dictionary pairs** (`quedar`/`quedarse` and the
      rest) cost every shared inflection its tappability.
- [ ] **Scenes** — 40 exist, grow to ~95, phase-gated, matching the story arc.
      Scene replies are Spanish-only (the English is blurred behind one
      "Show the English" control) — do not print translations on the buttons.
- [ ] **Patterns** — only 5 exist for 8 phases. Grow to ~50. Same
      `trigger` + `min` vocabulary gating as now.
- [ ] **Verbs** — `verbs.json` has 45 verbs × 3 tenses × 5 subjects. Expand to
      ~120 verbs and add imperfect, conditional, present subjunctive and the
      **voseo imperative** (`hablá`, `comé`, `vení`, `sentate`).
- [ ] **Momo lines** — 59 exist, gated on vocabulary. He must never speak
      English; a pack with no earned line gets a bird who reacts silently.
- [ ] **Audio** — there is **no Nicaraguan TTS voice on any platform**. The
      pack declares `es-MX`, which is the accent Kevin explicitly does not
      want. Unresolved; his call between labelling it, dropping audio, or
      recording a real Nicaraguan speaker for the scenes.

Derived drills need no authoring: **Review, Word Order, Listening and
Shadowing all generate from lesson sentences** and grow automatically with
every story.

---

## 8. Things already learned the hard way

- Shell heredocs mangle apostrophes and accents on this machine. Write Python
  and JSON with a file-writing tool, not `bash <<'EOF'`.
- Console output is cp1252; accented characters print as `?`. Write results to
  a file and read the file rather than trusting the terminal.
- `/tmp` in Python on this machine is not the bash `/tmp`. Use relative paths.
- The content repo's CI commits the rebuilt pack back to main, so
  `git pull --rebase` before pushing or the push is rejected.
- Kevin's preferences: plainest possible output, no clutter, no option menus
  for simple asks. Do exactly what he says and do not generalise to adjacent
  scope. If he raises a concern, act on the literal ask.
