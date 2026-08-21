# START HERE — where the course stands

**The course is written and PUBLISHED.** 185 stories, 95 scenes, 52 patterns,
123 verbs and a dictionary of 2,428 words are all in `manifest.json`, so CI
rebuilds `content/pack.json` on every push and every app picks it up with no
app release. Read `HANDOFF.md` beside this file for the gates and the
reasoning behind them. This file is the short version.

| | | |
|---|---|---|
| Stories | **185** | 77,544 running words |
| Scenes | **95** | four steps, three options, phase-gated |
| Patterns | **52** | every trigger a lemma the course can teach |
| Verbs | **123 verbs, 6 tenses** | voseo-correct |
| Lookups | **97.9%** | of the words on the page can be tapped |

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
It never publishes anything. Commit only when it prints no `PROBLEM:` lines,
and **`git pull --rebase` before pushing** — CI commits the rebuilt pack back
to main, so a plain push is rejected.

---

## What is left

1. **The voseo imperative is not drillable.** Every irregular verb carries an
   `imperative` key with one form, and `forms.py` reads it, so `hablá`, `tené`,
   `vení` and `andá` are tappable in the reader. It is deliberately not in
   `tenses`, because `startVerbs()` draws a random subject index 0–4 for
   whatever tense it picks and a one-slot tense would hand the drill an
   `undefined`. Drilling it is a change in the **app repo**
   (`scenicprints/fluidez`): teach `startVerbs()` that some tenses have one
   form and no subject. Small job, wrong repo.

2. **Kevin's Path resets to zero.** The old 81 stories were `s00`–`s710` and
   the new ones are `p0-01`–`p7-18`, so the ids he has read no longer exist.
   His vocabulary, streak and fluency score are keyed on WORDS and survive
   untouched — but "5 of 185 read" starts at nought, and `openPhases()` opens
   a phase only once every story in the one before it is read, so everything
   past phase 0 shows locked until he reads through it. That is inherent in
   replacing the course and there is nothing to do about it in this repo. He
   should be told rather than left to find it.

3. **The pack is 1.5 MB**, up from 420 KB, because it now carries 185 stories
   instead of 81. Checked in the real app: it stores in `localStorage`
   without complaint. If a device ever does hit its quota, `cacheWrite`
   already swallows the error and the app simply refetches on next launch —
   slower and useless offline, never broken.

4. **Audio is `es-MX`. DECIDED 2026-08-21: leave it.** There is no Nicaraguan
   TTS voice on any platform and Kevin has looked at the trade and chosen to
   live with it. Do not reopen this, do not swap the voice.

---

## Making a word tappable — how it works now

`forms.py` maps every inflected word that ACTUALLY OCCURS back to its
dictionary entry, which is what makes it tappable, colour it by memory
strength, and record an exposure against the right lemma. Three tiers decide
who owns a form, and they exist because each one fixed a whole class:

1. **Stated** — `verbs.json`'s irregular tables, the imperfect subjunctive
   built off each verb's own preterite, and `EXTRA_FORMS` for the verbs the
   Trainer does not drill (oír, haber, traer, oler, morir…). Facts, not
   guesses, so they beat the rules: `dijo` is `decir`, not `dejar`'s
   speculative e→i stem change.
2. **Ruled** — the regular tables, plurals, the -zco/-jo and -qué/-gué/-cé
   spelling classes, -mente adverbs, and pronouns glued onto an infinitive or
   a gerund (`acompañarla`, `haciéndolo`).
3. **Weak** — claims that lose every argument: the tú forms (a voseo course
   contains none, so `casas` is houses and `calles` is streets), participles
   (`mandados` is an errand, `comidas` is food), pronouns glued onto an
   imperative (`ve` + `la` spells a candle), the gerund and participle guessed
   for an irregular verb, and anything the rules spell for a verb whose forms
   are hand-written.

A form two lemmas can both spell is **dropped, not guessed at** — except a
plain/reflexive pair, which the text settles. "Se queda en la casa" is
`quedarse` and "queda lejos" is `quedar`, and the pronoun in front says which
— but only if it **agrees** with the verb. Without that test "me parece" and
"me pareció" read as reflexives and `parecer` lands under `parecerse`.

`content/dictionary/forms-overrides.json` pins what no rule can settle, and a
`null` blocks a form outright. `siento` is blocked on purpose: it is
`sentarse` 19 times and `sentir`/`sentirse` 17, so either answer would be
wrong half the time. **stage.py, reconcile.py and build-pack.py all apply it**
— they used to disagree, and a warm-up card turned on which one was right.

### Rules that still hold

- **Never let a conjugated form or a plural be its own dictionary entry.**
  62 were, and 42 have been merged into their infinitives. Three are kept on
  purpose and are listed in `reconcile.py`'s `NOT_A_LEMMA`: `hay`, and `fue`
  and `fui`, which are ir AND ser at once — the gloss "was/went" is the honest
  answer, and dropping them would take 119 words off the page. The vos and
  usted imperatives the course teaches AS words — `andá`, `vení`, `sentate`,
  `fijate`, `decime`, `deme`, `disculpe` — are lemmas in their own right.
- **Never add a lemma whose ±`se` twin is already an entry.** Adding `tragar`
  beside `tragarse` cost `traga` its mapping until it was pulled back out. If
  the course uses the plain infinitive of a `-se`-only entry, `forms.py` maps
  it (`soltar` → `soltarse`) — no second entry needed.
- **Skip proper nouns.** The cast and the place names are 1.9% of the page and
  they are why the lookup number is 97.9% and not 99%. The remaining 0.2% is
  words that genuinely go both ways — `llena`, `dura`, `corta`, `seca` — and
  the ir/ser preterite.

### The trade-off worth knowing about

`queda` is `quedarse` in 74 of the 126 places the course writes it, so it maps
there — which means "el cuarto queda oscuro" opens a card reading "to stay".
The same goes for the other fifteen pairs. One card for a verb the learner
meets 126 times beats no card at all, but it is a choice, not a certainty.

---

## Two gate false positives — do not re-discover these

- **`camión`** is flagged as Mexican. In Nicaragua it is the ordinary word for
  a lorry; the Mexican sense is *bus*. Worked around with `rastra`.
- **`vale`** is flagged as Peninsular. It is also the third person of `valer`.
  Worked around by rewriting with `contar` and `pesar`.

Neither ban should come off casually; both catch a real thing most of the time.

---

## The loop for changing content

1. **Write** the JSON. Emit a batch from one throwaway Python file rather than
   one tool call each.
2. `python .github/scripts/stage.py --root .`
3. **Add the dictionary entries** it lists in `content/plan/needs-entry.txt`.
   Lemmas only. Skip proper nouns. Check the reflexive-twin trap above.
4. `python .github/scripts/reconcile.py` — rewrites every warm-up from the
   text, so a warm-up can never claim a word the story does not teach.
5. Repeat 2 until there are no `PROBLEM:` lines, then commit and push.

---

## The cast

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
- **Console output is cp1252** — accents print as `?`. Write results to a file
  and read the file rather than trusting the terminal.
- **`/tmp` in Python is not the bash `/tmp`** on this machine. Use relative
  paths.
- **`screens.js` speaks `step.es` aloud.** A scene step prompt has to be
  something a person actually says; put an action in a parenthesis in FRONT of
  a real line. Options are only tapped, so a parenthetical option is fine.
- **A pattern trigger must be a dictionary LEMMA the course can teach.**
  Exposures are keyed on `resolve(cleanWord(raw))`, so a conjugated trigger has
  no vocab entry and can never be met. `ser_estar` and `me_gusta` both shipped
  dead for exactly this.
- **`engine.js conjugate()` falls back to the regular table** when an irregular
  verb lacks a tense, so a verb that is in `drill` and in neither table is
  taught wrong and silently — that is how the Trainer taught "cerro" and
  "perdo" for years. Rebuild with `python .github/scripts/verbs_build.py`; it
  refuses to write unless it reproduces the original 21 irregulars byte for
  byte.
- **Never weaken a gate to make content pass.** If a gate fires, first ask
  whether the content is wrong. It usually is.
- **To check a change in the real app**, seed `localStorage` and reload: the
  cached pack lives at `fl:c:pack:es-ni` and is stored in `applyPack` shape,
  not the shape `pack.json` ships — `dictionary` becomes `dict`, lessons get
  `sentences` (from `sn`) and `warmup` (from `wu`), scenes get mapped steps.
  Seed it raw and nothing is tappable and no story will open. Writes to
  Firestore are already blocked on localhost. Browser-pane screenshots always
  fail; read `innerText` instead.

## Kevin's working preferences

Plainest possible output. No option menus for simple asks. Do exactly what he
says and do not generalise to adjacent scope. He does not want progress reports
that read like check-ins — just keep working. **He watches agent usage**, so
work in large batches and lean on the gates rather than re-verifying what they
have already proven.
