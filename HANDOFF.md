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
  lessons/p0-01.json …       the 185 stories            <- write here
  scenarios/sc*.json         95 scenes
  patterns/core.json         the original 5
  patterns/spine.json        the 47 the rewrite added
  verbs.json                 123 verbs, 6 tenses (generated)
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
opens `frío` and strengthens `frío`. **97.9% of the words on the page are
tappable**; the rest is the cast, the place names, and a handful of words the
course genuinely uses both ways. Three tiers decide who owns a form and each
one was put there to fix a class rather than a word — the full account is in
`NEXT.md` under *Making a word tappable*. Rules already paid for:

- **Stated beats ruled beats weak.** `verbs.json` is a fact and a rule is a
  guess, so `dijo` is `decir` and not `dejar`'s speculative e→i stem change.
  Tú forms, participles, and pronouns glued to an imperative are weak and lose
  every argument: a voseo course contains no `casas`-the-verb, `mandados` is an
  errand, and `ve` + `la` spells a candle.
- Irregular verbs are **never** rule-generated for their finite tenses (the
  tables turn `estar` into `esto` and `dar` into `do`, which are real words
  with other meanings). Their gerund and participle are guessed weakly, and
  the ones no rule can reach — `diciendo`, `visto`, `puesto`, `muerto` — are
  written out in `IRREGULAR_NONFINITE`.
- A form two lemmas could both produce is **dropped, not guessed** — with one
  exception. A plain/reflexive pair (`quedar`/`quedarse`) is settled from the
  text: the pronoun in front says which, **as long as it agrees with the
  verb**. Without the agreement test "me parece" reads as a reflexive.
- **Pronouns glue onto the end of a verb** and no table can spell that:
  `acompañarla`, `decírmelo`, `contame`, `fíjese`, `hagámoslo`. The stress is
  marked on the base before the pronoun goes on, which is what makes
  `hablando` → `hablándome` and `fije` → `fíjese` come out right.
- Spanish drops the written accent in the plural: `razón`→`razones`,
  `inglés`→`ingleses`, and every `-ción` noun — and gains one going the other
  way: `joven`→`jóvenes`, `examen`→`exámenes`.
- Reflexive infinitives strip `-se` before generating, or `llamarse`,
  `sentarse`, `irse` produce nothing at all. A `-se`-only entry also owns the
  plain infinitive (`soltar` → `soltarse`) — do not add a second entry.
- Anything ending in `-o` agrees like an adjective whatever its `pos` says
  (`todo` is tagged `pron`, `mucho` is tagged `adv`), and a noun that names a
  person has a feminine (`maestro`/`maestra`, `vendedor`/`vendedora`).
- **Stem changes are generated speculatively** (o→ue, e→ie, e→i):
  `costar`→`cuesta`, `pensar`→`piensa`, `volver`→`vuelve`. Over-generating
  is safe because anything not actually written is thrown away by the
  corpus filter. Voseo does not stem-change (`vos podés`), and those come
  from the plain stem, so both spellings are covered.
- **Never let a plural or a conjugated form be its own entry** when the lemma
  exists. `frijol` and `frijoles` were both entries, so every plural counted
  towards a different memory; 62 conjugated forms were entries too and 42 have
  been merged away. What is deliberately kept is listed in `reconcile.py`.
- `forms-overrides.json` pins what no rule can settle and a `null` blocks a
  form outright. **stage.py, reconcile.py and build-pack.py all apply it** —
  they used to disagree. Keys starting with `_` are notes, not forms.

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

**Published 2026-08-21.** `manifest.json` lists all 185 stories in spine order,
all 95 scenes, both pattern files and both dictionary files; the old
`lessons/s*.json` are gone. CI rebuilds `content/pack.json` on every push to
main and every app picks it up with **no app release**.

Publishing was four edits, and it is worth knowing it was four in case a
future language repo needs the same: the `lessons` list, the 95 `scenarios`
rows (`{id, title, desc, phase, path}`), adding `patterns/spine.json`, and
deleting the old story files. `build-pack.py` only ever loads what the
manifest names, so a file on disk that nobody lists does not exist.

The pack went from 420 KB to 1.5 MB. It still stores in `localStorage` — that
was checked in the real app, not assumed — and `cacheWrite` already swallows a
quota failure and refetches, so the worst case is slow, not broken.

**The lesson ids changed**, from `s00`–`s710` to `p0-01`–`p7-18`. Vocabulary,
streak and fluency are keyed on words and survive; "read" is keyed on lesson
id and does not. Anybody using the old course starts the Path at zero with
everything past phase 0 locked, because `openPhases()` opens a phase only once
every story in the one before it is read.

Three independent update lanes, all working:
1. App code → push to `fluidez` main → CI stamps a version → Pages.
2. Lessons → push JSON here → CI rebuilds the pack. **No app release.**
3. New language → new repo + a line in the registry. **No app release.**

---

## 7. Still to do

- [x] **Stories** — 185 of 185 written and published. 77,544 running words,
      1,963 words taught, median six encounters. See `plan/PROGRESS.md`.
- [x] **Warm-ups** — 95 of 185 used to end up empty, because `reconcile.py`
      would not let two stories claim the same word. Five changes and no gate
      weakened: 5 empty, median 3, 609 warm-up words.
- [x] **Tappability** — 93.4% → **97.9%**. 363 lemmas added, 42 conjugated
      entries merged into their infinitives, pronouns-glued-to-a-verb
      generated, and the sixteen `quedar`/`quedarse` pairs settled from the
      text instead of dropped. Ambiguous forms went from 153 to 22. The
      three tiers and the trade-offs are in `NEXT.md`.
- [x] **Scenes** — 95, weighted 0:8 1:9 2:11 3:11 4:19 5:14 6:12 7:11. Replies
      are Spanish-only. NOTE: `screens.js` speaks `step.es` aloud, so a step
      prompt must be a line somebody says; options are only tapped.
- [x] **Patterns** — 52. A trigger must be a dictionary LEMMA the course can
      teach: exposures are keyed on the resolved lemma, so a conjugated form
      can never be met. Two of the original five were dead for that reason.
- [x] **Verbs** — 123 verbs × 6 tenses. `cerrar` and `perder` were producing
      "cerro" and "perdo". Rebuild with
      `python .github/scripts/verbs_build.py`. The voseo imperative is stored
      per verb but kept out of `tenses`, because a one-form tense would break
      `startVerbs()` — drilling it needs an app-repo change.
- [x] **Momo lines** — 59, and **16 of them could never fire**. Same bug as
      the patterns: triggers on inflected forms (`vamos`, `sos`, `hacés`) or on
      words the course never uses (`tranqui`, `platicar`, `ánimo`).
      `build-pack.py` only checks `min <= len(trigger)`, so none of it showed.
      Two lines were reworded and are flagged in NEXT.md: *Vamos a platicar* →
      *Vamos a conversar* (platicar is Mexican and on dialect.py's own ban
      list), and *¡Ánimo!* → *¡Seguí!* (nothing teaches ánimo, so that line was
      unreachable by construction). `stage.py` checks this now.
- [x] **Audio** — **DECIDED 2026-08-21: leave it as `es-MX`.** There is no
      Nicaraguan TTS voice on any platform. Kevin has seen the trade and chosen
      to live with the Mexican voice rather than lose audio. Closed. Do not
      reopen it, do not swap the voice, do not add a warning label.

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
