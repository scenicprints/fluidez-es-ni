# START HERE — what to build next

**You are continuing a course that is 121 stories of 185 written.** Read
`HANDOFF.md` in this same folder for the full context, the gates and the
reasoning behind them. This file is the short version: what to do, right now,
in order.

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

## The next task: phases 5, 6 and 7 — 64 stories

| Phase | | Written | Remaining |
|---|---|---|---|
| 0 | Survival | 16 / 16 | done |
| 1 | Getting Around | 18 / 18 | done |
| 2 | Connecting | 26 / 26 | done |
| 3 | Holding Your Own | 26 / 26 | done |
| 4 | Close to the Heart | 35 / 35 | done |
| **5** | **Fitting In** | **0 / 26** | **`p5-01` … `p5-26`** |
| **6** | **Sounding Local** | **0 / 20** | **`p6-01` … `p6-20`** |
| **7** | **Native-Like** | **0 / 18** | **`p7-01` … `p7-18`** |

Each entry in `content/plan/spine.json` carries `title`, `desc`, and three
planning fields: `spanish` (what language it teaches — **this drives the
order**), `nicaragua` (what it teaches about the country), `beat` (what
happens). Follow them. **Do not rebalance the phase counts** — phase 4 is the
biggest on purpose, and it is already done.

Note: from `p4-23` onward the titles drifted one slot from the spine (I wrote
`La boda` as `p4-23` rather than `p4-24`). The ids are all valid and the gates
pass; the spine is a plan, not a contract. Do not try to renumber.

### Story length ramps

Phase 0 was ~450 words. Phases 5–7 should be **900 → 1,200 words** — longer
sentences, more subordination, fewer explanations. Total target is ~148,000
running words; 38,249 are written.

---

## The loop for one batch (10–13 stories)

1. **Write** `content/lessons/<id>.json` for each story in the batch.
   Emit them from one throwaway Python file rather than one tool call each —
   see the shape below.
2. `python .github/scripts/stage.py --root .`
3. **Add the dictionary entries** it lists in `content/plan/needs-entry.txt`
   to `content/dictionary/spine.json`. This clears most DENSITY failures,
   because a word with no entry cannot be counted at all. Skip proper nouns.
4. `python .github/scripts/reconcile.py` — rewrites every `wu` to the words the
   story actually hammers **and** that actually come back. The warm-up is a
   claim; this makes the claim true.
5. Repeat 2 until no `PROBLEM:` lines. Commit and push.
   **`git pull --rebase` first** — this repo's CI commits the rebuilt pack back
   to main, so a plain push is rejected.

### Story file shape

```json
{
  "id": "p5-01",
  "title": "Qué tuani",
  "desc": "Slang that dates you if you get it wrong",
  "ph": 5,
  "diff": 5,
  "wu": ["tuani", "maje", "..."],
  "sn": [ {"s": "Spanish sentence.", "e": "English translation."} ]
}
```

**Write to the density rule from the start**: pick the 8–12 new words first,
then write so each lands five or six times in different sentences.
Retrofitting repetition costs far more than planning it. Every `sn` entry is
one short standalone sentence — Review, Word Order, Listening and Shadowing
all draw from these, so each must work alone.

### Voice

First person, present tense, plain sentences. The recurring cast is
established and must continue: **Roberto** (the neighbour's son, twelve at the
start, seventeen by phase 4), **doña Carmen** (his mother, the first house),
**don Beto** (the older neighbour), **doña Chepa** (the pulpería), **Marcos**
(workmate, later compadre), **Lucía** (wife by phase 4), **doña Elena** (the
suegra), **Julio** and **Chino** (her brothers), and a baby called **Beto**.
The protagonist's nickname is **el Perdido**. He is married with a small child
by the end of phase 4 — phases 5–7 continue from there.

---

## After the stories: three more content jobs

Do these **after** all 185 stories, in this order.

1. **Scenes** — 40 exist in `content/scenarios/`, grow to ~95. Phase-gated,
   matching the story arc, and heavily weighted to phase 4 material (arguments,
   the suegra, apology). Replies are **Spanish only** — the English is blurred
   behind one reveal control. Never print translations on the option buttons.
2. **Patterns** — only 5 exist in `content/patterns/` for 8 phases. Grow to
   ~50. Same `trigger` + `min` vocabulary gating as the existing ones.
3. **Verbs** — `content/verbs.json` has 45 verbs × 3 tenses × 5 subjects.
   Expand to ~120 verbs and add imperfect, conditional, present subjunctive and
   the **voseo imperative** (`hablá`, `comé`, `vení`, `sentate`).

Review, Word Order, Listening and Shadowing need no authoring — they generate
from lesson sentences and have been growing with every batch.

---

## Publishing — DO NOT DO THIS YET

New stories are deliberately **not** in `content/manifest.json`. They stay out
until all 185 are written, because dropping story three of the new course into
the middle of the old one only confuses Kevin, who uses the app daily.

When all 185 are done and the gates are clean:

1. Replace the `lessons` list in `content/manifest.json` with the spine ids.
2. Delete `content/lessons/s*.json` (the old 81).
3. Push. CI rebuilds `content/pack.json` and every app picks it up with **no
   app release**.

---

## Traps that have already cost hours

- **Shell heredocs mangle apostrophes and accents on this machine.** Write
  Python and JSON with a file-writing tool, never `bash <<'EOF'` with accented
  content. `\n` inside a heredoc becomes a real newline and breaks the file.
- **Console output is cp1252** — accents print as `?`. Write results to a file
  and read the file rather than trusting the terminal.
- **`/tmp` in Python is not the bash `/tmp`** on this machine. Use relative
  paths.
- **Never weaken a gate to make content pass.** Every ban that came off came
  off because it flagged *correct* Spanish — `tío`, `piso`, `ven`, `oye`, `di`,
  `sal`, and every `-ir` verb. If a gate fires, first ask whether the content
  is wrong.
- **Never let a conjugated form or a plural be its own dictionary entry.**
  `sos`, `tenés`, `es`, `frijoles` were all separate entries from `ser`,
  `tener`, `frijol` — 96 of these have been merged. Add lemmas only.

## Kevin's working preferences

Plainest possible output. No option menus for simple asks. Do exactly what he
says and do not generalise to adjacent scope. He does not want progress reports
that read like check-ins — just keep working. **He watches agent usage**, so
work in large batches and lean on the gates rather than re-verifying what they
have already proven.
