# -*- coding: utf-8 -*-
"""Rewrites every warm-up to the words its story actually teaches.

A warm-up is a CLAIM: these are the words this lesson is going to hammer.
Written by hand the claim drifts - 46% of the old course's warm-up words never
appeared in the lesson they warmed up for. So it is not written by hand. This
derives it from the text, and the text is the only thing that can be wrong.

A word is warmed up when all of this is true:

  * the story uses it at least DENSITY_MIN times, so there is context to work
    it out from;
  * it is a content word, not a preposition or an article;
  * it is a dictionary lemma, or nothing can be shown on the card;
  * it is not one of the few dozen words in BORING - "hacer", "todo", "muy" -
    which every story is full of and which nobody needs a card for;
  * it comes back later in the course per schedule.py's RETURN rule, OR it is
    a one-scene word that this story is most of - mango, gigantona, nacatamal;
  * and no story in the last GAP stories has already warmed it up.

That last rule used to be "no story has EVER warmed it up". It was the single
biggest cause of a defect worth writing down: 95 of the 185 stories ended with
NO warm-up at all, median zero words. First-come-first-served meant the early
stories claimed every common word and everything after them starved. Letting a
word be warmed up again twenty-five stories later is not a duplicate claim -
the later story really does hammer it, and re-teaching a word a month later is
spacing, which is the whole point.

The other half of the fix was that RETURN was picking the cards. "Semana
Santa" came out warming up "calle gente pasar" while procesion, alfombra and
aserrin were refused for not coming back. See ONE_SCENE in schedule.py.

Together - the gap, the widened RETURN window, the one-scene exemption, a
content pass recycling ten stranded words, and dropping the conjugated-form
entries from the candidates - 95 empty warm-ups became 8, the median went
from zero words to two, and the whole course went from 162 warm-up words to
558.

The stories that still have none are stories whose vocabulary is entirely
words the learner has been reading for months. Those are honest blanks: there
is nothing to pre-teach, and the app shows no warm-up rather than a card for
"hacer".
"""
import io, json, os, sys, re
sys.path.insert(0, ".github/scripts")
import forms as M, schedule as SCH

# How many stories must pass before a word may be warmed up a second time.
GAP = 25
# Most a single warm-up may show.
CAP = 12

dictionary = {}
for p in ["content/dictionary/core.json", "content/dictionary/spine.json"]:
    dictionary.update(json.load(io.open(p, encoding="utf-8")))
verbs = json.load(io.open("content/verbs.json", encoding="utf-8"))
spine = [s["id"] for s in json.load(io.open("content/plan/spine.json", encoding="utf-8"))]
lessons = {}
for n in sorted(os.listdir("content/lessons")):
    if re.match(r"^p[0-7]-\d\d\.json$", n):
        b = json.load(io.open("content/lessons/" + n, encoding="utf-8"))
        lessons[b["id"]] = b
corpus = [sn["s"] for b in lessons.values() for sn in b["sn"]]
forms, _, _ = M.build(dictionary, corpus, verbs)
counts = {sid: SCH.story_words(b, dictionary, forms) for sid, b in lessons.items()}
order = [s for s in spine if s in lessons]

# Words every story is full of. A card for "hacer" in story 140 teaches nobody
# anything and pushes out the word the story is actually about.
BORING = set(u"su no ir venir poner ser estar haber tener hacer decir dar ver uno una todo "
             u"mucho poco mas muy ya tambien aqui alli este ese otro hay dos tres sin ella el la "
             u"que como cuando donde porque pero si mi tu nos les lo se".split())

# Dictionary entries that are a conjugated form of a verb that is ALSO an
# entry: "llega" beside "llegar", "entiendo" beside "entender". HANDOFF.md
# says these should not exist and 164 of them have already been merged away;
# these are what is left, and merging them is a data job nobody has done yet.
# Until somebody does they must not be offered as vocabulary cards - a card
# reading "llega: arrives" teaches nothing and costs the story a real word.
# The vos imperatives the course genuinely teaches as words - anda, mira,
# veni, sentate, fijate, decime - are deliberately NOT in here.
NOT_A_LEMMA = set(
    u"busco cabe come comemos compro comí conocen conozco creo entendés "
    u"entiende entiendo era fue fui gusta gustan habla hablamos hablo hablé "
    u"habría hubiera huele jugaba llama llamo llega llego llegué necesito pago "
    u"parece pasa podría tomo trae tuviera vaya venden vive vivimos vivo viví"
    .split())

# How much of everything the course ever says with a word is said in this one
# story. Ordering the warm-up by this puts what the lesson is ABOUT first:
# "Semana Santa" leads with aserrin and procesion, not with calle and gente.
total_uses = {}
for _c in counts.values():
    for _w, _n in _c.items():
        total_uses[_w] = total_uses.get(_w, 0) + _n

last_claim = {}
for i, sid in enumerate(order):
    b = lessons[sid]
    c = counts[sid]
    later = order[i + 1:]

    def returns(w):
        # Same rule schedule.py enforces, including both its exemptions: a word
        # is judged only once enough course exists after it, and a one-scene
        # word - most of everything the course says with it is said right here -
        # is exempt, because a festival noun comes back when the country gives
        # it a reason to and not before.
        if len(later) < SCH.RETURN_WINDOW:
            return True
        if sum(1 for j in later if counts[j].get(w)) >= SCH.RETURN_MIN:
            return True
        return SCH.one_scene(w, c.get(w, 0), sum(x.get(w, 0) for x in counts.values()))

    def qualifies(w, n, gap):
        return (n >= SCH.DENSITY_MIN
                and SCH.is_content(w, dictionary)
                and w in dictionary
                and w.lower() not in BORING
                and w.lower() not in NOT_A_LEMMA
                and (not gap or w not in last_claim or i - last_claim[w] >= GAP)
                and returns(w))

    ok = [w for w, n in c.items() if qualifies(w, n, True)]
    if not ok:
        # The gap is there to stop a word being warmed up twice in quick
        # succession, not to leave a lesson with nothing to pre-teach. The
        # story called Perdón should be allowed to warm up perdón.
        ok = [w for w, n in c.items() if qualifies(w, n, False)]

    # Ordered by how much of the word belongs to this story, then by how hard
    # the story leans on it. A hand-written warm-up is not preserved for its
    # own sake - if the word still earns its place it comes back anyway.
    def own(w):
        return c[w] / float(total_uses.get(w, c[w]))
    b["wu"] = sorted(ok, key=lambda w: (-own(w), -c[w], w))[:CAP]
    for w in b["wu"]:
        last_claim[w] = i
    io.open("content/lessons/%s.json" % sid, "w", encoding="utf-8").write(
        json.dumps(b, ensure_ascii=False, indent=1) + u"\n")

sizes = [len(lessons[s]["wu"]) for s in order]
print("warm-ups  %d stories, %d words, median %d, %d with none"
      % (len(sizes), sum(sizes), sorted(sizes)[len(sizes) // 2],
         sum(1 for x in sizes if x == 0)))
