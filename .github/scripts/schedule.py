# -*- coding: utf-8 -*-
"""Checks that the course actually recycles its vocabulary.

The old course taught 769 words and let 42% of them appear in exactly one
lesson, ever. Median encounters across the whole thing: two. You cannot learn a
word from two encounters, so the decay model correctly forgot almost all of
them and 81 lessons left you with 187 words.

The fix is not in the app, it is in the writing, and writing recycles by
accident unless something checks. So this is a build gate, like the dialect
one: a story that fails its quota does not ship.

Three rules, all measured at the lemma so that "cosa" and "cosas" are one word:

  COVERAGE   at least 88% of the dictionary words in a story must already have
             been introduced by an earlier story. Extensive reading needs 95%+
             of the running text known; 88% of the *dictionary* words is the
             practical equivalent once names and function words are counted.

  DENSITY    every word a story DECLARES it teaches - its warm-up list - must
             appear at least 5 times in that story. One occurrence is not
             context, it is a sighting, and 71% of the old course was single
             sightings. This also kills an old bug by construction: 46% of
             warm-up words never appeared in the lesson they warmed up for.

             It applies to the declared targets, not to every new word. "a",
             "al" and "bien" turn up new in story one and cannot sensibly be
             said five times each; function words earn their encounters across
             the whole course, not inside one story.

  RETURN     a CONTENT word introduced by a story must reappear in at least 6
             of the next 25 stories. Prepositions, articles and pronouns are
             exempt - they are in every story by their nature. That is what turns 5 encounters into 12 spaced
             ones, and with no SRS scheduler in the app it is the ONLY spacing
             the learner gets.

Only stories on the new spine (ids p0-01 .. p7-18) are checked. The old
lessons are being replaced and would fail every rule.
"""
import io, json, re, collections

TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)
SPINE_ID = re.compile(r"^p[0-7]-\d\d$")

COVERAGE_MIN = 0.88
COVERAGE_START = 0.60   # what story four is held to
RAMP = 25               # stories over which the bar climbs to COVERAGE_MIN
DENSITY_MIN = 5
RETURN_MIN = 6
RETURN_WINDOW = 25

# Parts of speech that are structural rather than vocabulary. They are in
# every story whether anybody planned it or not, so holding them to a
# recycling quota measures nothing and buries the words that matter.
FUNCTION_POS = ("prep", "art", "conj", "contr", "pron", "num")


def is_content(word, dictionary):
    pos = (dictionary.get(word, {}).get("pos") or "").split("/")[0]
    return pos not in FUNCTION_POS


def lemmas(text, dictionary, forms):
    """Every dictionary word in a line, as its lemma, in order."""
    out = []
    for w in TOKEN.findall((text or u"").lower()):
        if w in dictionary:
            out.append(w)
        elif w in forms:
            out.append(forms[w])
    return out


def story_words(lesson, dictionary, forms):
    counts = collections.Counter()
    for sn in lesson.get("sn") or lesson.get("sentences") or []:
        for lem in lemmas(sn.get("s") or sn.get("es") or u"", dictionary, forms):
            counts[lem] += 1
    return counts


def check(pack, spine_order=None):
    """Returns (problems, stats). A problem is a hard build failure."""
    dictionary = pack.get("dictionary") or {}
    forms = pack.get("forms") or {}
    lessons = [l for l in (pack.get("lessons") or []) if SPINE_ID.match(str(l.get("id") or ""))]
    if not lessons:
        return [], {"stories": 0}

    # Course order is the spine's order, not whatever the manifest happens to
    # list, because "already introduced" only means anything in reading order.
    if spine_order:
        rank = {sid: i for i, sid in enumerate(spine_order)}
        lessons.sort(key=lambda l: rank.get(l.get("id"), 10 ** 6))
    else:
        lessons.sort(key=lambda l: str(l.get("id")))

    counts = [story_words(l, dictionary, forms) for l in lessons]

    problems = []
    introduced = {}          # lemma -> index of the story that introduced it
    known = set()
    thin, weak = [], []

    for i, (lesson, c) in enumerate(zip(lessons, counts)):
        sid = lesson.get("id")
        if not c:
            problems.append(u"%s has no dictionary words in it at all" % sid)
            continue

        fresh = [w for w in c if w not in known]
        seen_before = len(c) - len(fresh)
        coverage = seen_before / float(len(c))

        # Coverage has to ramp. Story four cannot have 88% of its words already
        # known, because there are three stories' worth of Spanish in
        # existence. A real graded course introduces heavily at the start and
        # then lives off what it built. So the bar climbs from 60% to the full
        # 88% over the first RAMP stories and holds there for the rest.
        need = COVERAGE_MIN
        if i < RAMP:
            need = COVERAGE_START + (COVERAGE_MIN - COVERAGE_START) * (i / float(RAMP))
        if i >= 3 and coverage < need:
            problems.append(
                u"%s: only %.0f%% of its words were introduced earlier (need %.0f%%). "
                u"%d new words in one story is too many to infer."
                % (sid, 100 * coverage, 100 * need, len(fresh)))

        for w in fresh:
            introduced[w] = i
        known.update(fresh)

        # The story's own claim about what it teaches, held to the density
        # rule. A warm-up word that is not in the story at all is the worst
        # case and shows up here as 0 uses.
        for raw in lesson.get("wu") or lesson.get("warmup") or []:
            w = raw.lower()
            if " " in w:
                # "gallo pinto" is one dictionary entry and two tokens, so a
                # word counter can never see it. Count the phrase in the raw
                # text instead. Nicaraguan speech is full of these - dale pues,
                # va pues, por favor - so this is not a special case for one
                # breakfast.
                hits = sum(
                    (sn.get("s") or sn.get("es") or u"").lower().count(w)
                    for sn in lesson.get("sn") or lesson.get("sentences") or [])
                if hits < DENSITY_MIN:
                    thin.append((sid, raw, hits))
                continue
            w = w if w in dictionary else forms.get(w, w)
            if c.get(w, 0) < DENSITY_MIN:
                thin.append((sid, raw, c.get(w, 0)))

    # DENSITY is reported in one place so a story with eight thin words is one
    # readable failure rather than eight.
    by_story = collections.defaultdict(list)
    for sid, w, n in thin:
        by_story[sid].append(u"%s(%dx)" % (w, n))
    for sid, ws in by_story.items():
        problems.append(
            u"%s introduces %d word(s) it barely uses: %s. A new word needs %d "
            u"uses in the story that teaches it, or there is no context to work "
            u"it out from." % (sid, len(ws), u", ".join(sorted(ws)[:10]), DENSITY_MIN))

    # RETURN: does the word ever come back?
    last = len(lessons) - 1
    for w, at in introduced.items():
        if not is_content(w, dictionary):
            continue
        window = list(range(at + 1, min(at + 1 + RETURN_WINDOW, last + 1)))
        # Judge a word only once its whole window exists. While the course is
        # being written the last stories always have a short tail, and scaling
        # the requirement down for them ends up demanding that EVERY remaining
        # story contain EVERY word - which flagged 109 words in story one when
        # six stories existed.
        if len(window) < RETURN_WINDOW:
            continue
        came_back = sum(1 for j in window if counts[j].get(w))
        if came_back < RETURN_MIN:
            weak.append((lessons[at].get("id"), w, came_back, needed))

    if weak:
        per_story = collections.defaultdict(list)
        for sid, w, got, need in weak:
            per_story[sid].append(w)
        for sid in sorted(per_story):
            ws = per_story[sid]
            problems.append(
                u"%s introduces %d word(s) that never come back: %s. Every new "
                u"word has to reappear in %d of the next %d stories or it is "
                u"taught once and forgotten."
                % (sid, len(ws), u", ".join(sorted(ws)[:10]), RETURN_MIN, RETURN_WINDOW))

    total = sum(sum(c.values()) for c in counts)
    encounters = collections.Counter()
    for c in counts:
        for w, n in c.items():
            encounters[w] += n
    med = 0
    if encounters:
        vals = sorted(encounters.values())
        med = vals[len(vals) // 2]
    stats = {
        "stories": len(lessons),
        "running_words": total,
        "vocabulary": len(encounters),
        "median_encounters": med,
        "reach_ten": sum(1 for v in encounters.values() if v >= 10),
    }
    return problems, stats


def main(pack_path, spine_path=None):
    pack = json.load(io.open(pack_path, encoding="utf-8"))
    order = None
    if spine_path:
        try:
            order = [s["id"] for s in json.load(io.open(spine_path, encoding="utf-8"))]
        except (IOError, ValueError, KeyError):
            order = None
    problems, stats = check(pack, order)
    print(u"stories %d, %s running words, %d words taught, median %d encounters, "
          u"%d reach ten"
          % (stats.get("stories", 0), format(stats.get("running_words", 0), ","),
             stats.get("vocabulary", 0), stats.get("median_encounters", 0),
             stats.get("reach_ten", 0)))
    for p in problems:
        print(u"PROBLEM: %s" % p)
    return len(problems)


if __name__ == "__main__":
    import sys
    sys.exit(1 if main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None) else 0)
