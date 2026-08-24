# -*- coding: utf-8 -*-
"""Checks the new course while it is being written, without publishing it.

The 185 spine stories land one batch at a time. They must not go into the
manifest until the whole course is there -- dropping story three of the new
course into the middle of the old one would just confuse anybody using the app
today. But they still need checking as they are written, or problems pile up
185 stories deep.

So this assembles a pack from the spine plus whatever p*-NN.json files exist
so far, and runs exactly the gates the real build runs: Nicaraguan dialect,
inflection coverage, and the recycling quota.

    python .github/scripts/stage.py --root .
"""
import argparse, io, json, os, re, sys

import dialect as nica
import forms as morphology
import schedule as recycling

SPINE_FILE = re.compile(r"^p[0-7]-\d\d\.json$")
NEWLINE = chr(10)


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    content = os.path.join(args.root, "content")
    spine = read(os.path.join(content, "plan", "spine.json"))
    order = [s["id"] for s in spine]
    planned = set(order)

    lessons_dir = os.path.join(content, "lessons")
    written = {}
    for name in sorted(os.listdir(lessons_dir)):
        if not SPINE_FILE.match(name):
            continue
        body = read(os.path.join(lessons_dir, name))
        written[body.get("id") or name[:-5]] = body

    stray = sorted(set(written) - planned)
    for s in stray:
        print("PROBLEM: %s is not on the spine" % s)

    dictionary = {}
    for rel in read(os.path.join(content, "manifest.json")).get("dictionary", []):
        part = read(os.path.join(content, rel))
        if isinstance(part, dict):
            dictionary.update(part)

    verbs_path = os.path.join(content, "verbs.json")
    verbs = read(verbs_path) if os.path.exists(verbs_path) else {}

    lessons = [written[i] for i in order if i in written]
    corpus = []
    for l in lessons:
        for sn in l.get("sn") or []:
            corpus.append(sn.get("s") or "")

    # Scenes are checked here too, and for the same reason the lessons are:
    # they are written a batch at a time and stay out of the manifest until the
    # whole set is ready, so nothing else would ever look at them. Everything
    # in scenarios/ is read straight off disk, published or not.
    scene_dir = os.path.join(content, "scenarios")
    scenes, scene_problems = [], []
    if os.path.isdir(scene_dir):
        for name in sorted(os.listdir(scene_dir)):
            if not name.endswith(".json"):
                continue
            sc = read(os.path.join(scene_dir, name))
            scenes.append(sc)
            if not sc.get("id"):
                scene_problems.append("%s has no id" % name)
            if sc.get("ph") is None:
                scene_problems.append("scene %s has no phase" % sc.get("id", name))
            steps = sc.get("steps") or []
            if not steps:
                scene_problems.append("scene %s has no steps" % sc.get("id", name))
            for k, st in enumerate(steps, 1):
                opts = st.get("options") or []
                if not st.get("es"):
                    scene_problems.append("scene %s step %d says nothing" % (sc.get("id"), k))
                if len(opts) < 2:
                    scene_problems.append("scene %s step %d has %d option(s)"
                                          % (sc.get("id"), k, len(opts)))
                verdicts = [o.get("verdict") for o in opts]
                if "good" not in verdicts:
                    scene_problems.append("scene %s step %d has no good answer"
                                          % (sc.get("id"), k))
                for o in opts:
                    if not (o.get("es") and o.get("en") and o.get("feedback")):
                        scene_problems.append("scene %s step %d has a half-written option"
                                              % (sc.get("id"), k))
                    if o.get("verdict") not in ("good", "ok", "bad"):
                        scene_problems.append("scene %s step %d verdict %r"
                                              % (sc.get("id"), k, o.get("verdict")))
    dup = set()
    for sc in scenes:
        i = sc.get("id")
        if i in dup:
            scene_problems.append("duplicate scene id: %s" % i)
        dup.add(i)
    # Scene text joins the corpus so the inflection map covers it, but the
    # volume and lookup numbers below are about the COURSE, so they keep
    # counting lessons only.
    lesson_corpus = list(corpus)
    for sc in scenes:
        for st in sc.get("steps") or []:
            corpus.append(st.get("es") or "")
            for o in st.get("options") or []:
                corpus.append(o.get("es") or "")

    word_forms, ambiguous, seen = morphology.build(dictionary, corpus, verbs)

    # build-pack.py lets forms-overrides.json pin or block a mapping by hand,
    # so this has to apply them too or the lookup number below is measuring a
    # pack nobody ships.
    ov_path = os.path.join(content, "dictionary", "forms-overrides.json")
    override_problems = []
    if os.path.exists(ov_path):
        for form, lemma in (read(ov_path) or {}).items():
            if form.startswith("_"):
                continue
            form = form.lower()
            if lemma is None:
                word_forms.pop(form, None)
            elif lemma in dictionary:
                word_forms[form] = lemma
            else:
                override_problems.append(
                    "forms-overrides: %r points at %r, which is not a dictionary "
                    "entry" % (form, lemma))

    pack = {"dictionary": dictionary, "forms": word_forms,
            "lessons": lessons, "scenarios": scenes, "momo": []}

    allow = {}
    allow_path = os.path.join(content, "dialect-allow.json")
    if os.path.exists(allow_path):
        allow = read(allow_path)

    print("written    %d of %d stories" % (len(lessons), len(order)))
    if not lessons:
        return 0

    words = sum(len(morphology.tokens(c)) for c in lesson_corpus)
    print("volume     %s running words so far (target ~148,000)" % format(words, ","))

    # Words with no entry at all cannot be tapped, so they teach nothing.
    missing = sorted(w for w in seen if w not in dictionary and w not in word_forms)
    tappable = words - sum(
        1 for c in lesson_corpus for w in morphology.tokens(c)
        if w not in dictionary and w not in word_forms)
    print("lookups    %.1f%% of words on the page can be tapped" % (100.0 * tappable / max(1, words)))
    for p_ in override_problems:
        print("PROBLEM: %s" % p_)

    off, voseo = nica.check(pack, allow)
    print("dialect    %d voseo forms, %d off-dialect" % (voseo, len(off)))
    for where, word, why, text in off[:25]:
        print("PROBLEM: %s says %r - %s" % (where, word, why))

    problems, stats = recycling.check(pack, order)
    print("recycling  %d words taught, median %d encounters, %d reach ten"
          % (stats.get("vocabulary", 0), stats.get("median_encounters", 0),
             stats.get("reach_ten", 0)))
    print("one-scene  %d word(s) exempt from RETURN, taught hard in one story"
          % stats.get("one_scene", 0))
    # Patterns are gated on vocabulary: screens.js counts how many of a
    # pattern's trigger words the learner has an exposure against, and shows it
    # once that reaches `min`. Exposures are recorded against the RESOLVED
    # LEMMA -- store.recordExposure is handed resolve(cleanWord(raw)) -- so a
    # trigger that is a conjugated form has no vocab entry and can never be
    # met. That is not theoretical: the shipped ser_estar pattern listed soy,
    # es, son, estoy, esta and estan with min 4, every one of them a form, and
    # could not unlock for anybody, ever.
    #
    # So a trigger has to be a dictionary key, and it has to occur somewhere in
    # the course, or nobody can earn it.
    pattern_problems = []
    # Which lemmas the reader can actually land an exposure on. Exposures go
    # against the resolved lemma, so 'amar' is earnable from every 'te amo'
    # even though the string 'amar' never appears in the course.
    earned = set()
    for w in seen:
        if w in dictionary:
            earned.add(w)
        elif w in word_forms:
            earned.add(word_forms[w])
    patterns, core_ids, listed = [], set(), set()
    for rel in read(os.path.join(content, "manifest.json")).get("patterns", []):
        rows = read(os.path.join(content, rel))
        rows = rows if isinstance(rows, list) else [rows]
        patterns.extend(rows)
        core_ids.update(x.get("id") for x in rows)
        listed.add(os.path.basename(rel))
    pat_dir = os.path.join(content, "patterns")
    if os.path.isdir(pat_dir):
        for name in sorted(os.listdir(pat_dir)):
            if name.endswith(".json") and name not in listed:
                rows = read(os.path.join(pat_dir, name))
                patterns.extend(rows if isinstance(rows, list) else [rows])
    seen_ids = set()
    for pat in patterns:
        pid = pat.get("id") or "?"
        if pid in seen_ids:
            pattern_problems.append("duplicate pattern id: %s" % pid)
        seen_ids.add(pid)
        if not pat.get("title") or not pat.get("text"):
            pattern_problems.append("pattern %s is half written" % pid)
        trig = pat.get("trigger") or []
        if not trig:
            pattern_problems.append("pattern %s has no trigger" % pid)
            continue
        earnable = []
        for t in trig:
            if t not in dictionary:
                pattern_problems.append(
                    "pattern %s triggers on %r, which is not a dictionary entry - "
                    "exposures are keyed on the lemma, so it can never be met"
                    % (pid, t))
            elif t not in earned:
                pattern_problems.append(
                    "pattern %s triggers on %r, which never occurs in the course"
                    % (pid, t))
            else:
                earnable.append(t)
        need = pat.get("min", 3)
        if need > len(earnable):
            pattern_problems.append(
                "pattern %s needs %d triggers and only %d can ever be earned"
                % (pid, need, len(earnable)))

    # Momo is gated the same way patterns are, and had the same bug: sixteen of
    # his fifty-nine lines triggered on an inflected form (vamos, sos, hacés)
    # or on a word the course never uses (tranqui, platicar, ánimo), so they
    # could never fire. build-pack.py checks only that `min` is not larger than
    # the trigger list, which none of those failed.
    momo_problems = []
    momo_path = os.path.join(content, "momo.json")
    momo = []
    if os.path.exists(momo_path):
        doc = read(momo_path)
        momo = doc if isinstance(doc, list) else (doc.get("lines") or [])
    momo_dead_weight = 0
    for ln in momo:
        lid = ln.get("id") or "?"
        trig = ln.get("trigger") or []
        ok = [t for t in trig if t in dictionary and t in earned]
        # A trigger nobody can earn is only a PROBLEM when it takes the line
        # below its `min`. w-ideay lists both ideay and diay with min 1: diay
        # is never used in the course, and the line fires perfectly well on
        # ideay. That is dead weight, not breakage, so it is counted and not
        # shouted about.
        momo_dead_weight += len(trig) - len(ok)
        if ln.get("min", 1 if trig else 0) > len(ok):
            momo_problems.append(
                "momo %s can never fire: needs %d trigger(s), only %d earnable"
                " (%s)" % (lid, ln.get("min", 1), len(ok),
                           ", ".join(repr(t) for t in trig if t not in ok)))

    by_phase = {}
    for sc in scenes:
        by_phase[sc.get("ph")] = by_phase.get(sc.get("ph"), 0) + 1
    published = set()
    for row in read(os.path.join(content, "manifest.json")).get("scenarios", []):
        published.add(row.get("id"))
    print("scenes     %d written (%d published), by phase %s"
          % (len(scenes), sum(1 for sc in scenes if sc.get("id") in published),
             " ".join("%s:%d" % (k, by_phase[k]) for k in sorted(by_phase))))
    for p_ in scene_problems[:25]:
        print("PROBLEM: %s" % p_)

    # A scene is the payoff of the phase it sits in, so it may only use words a
    # lesson at or before that phase has taught. Nothing else checks this: the
    # block above checks a scene's SHAPE and dialect.py checks its Spanish, and
    # neither looks at the schedule. That is how forty scenes carried over from
    # the old 78-lesson course sat in the new phases for months with 7.5% of
    # their words unteachable at the point you meet them.
    first_phase = {}
    for lesson in lessons:
        ph = lesson.get("ph")
        raw = list(lesson.get("wu") or [])
        for sn in lesson.get("sn") or lesson.get("sentences") or []:
            raw.extend(morphology.tokens(sn.get("s") or sn.get("es") or ""))
        for w in raw:
            w = w.lower()
            lem = w if w in dictionary else word_forms.get(w)
            if lem is not None and lem not in first_phase:
                first_phase[lem] = ph
    ahead = []
    for sc in scenes:
        ph = sc.get("ph")
        for st in sc.get("steps") or []:
            texts = [st.get("es") or ""]
            texts.extend(o.get("es") or "" for o in st.get("options") or [])
            for text in texts:
                for w in morphology.tokens(text):
                    w = w.lower()
                    lem = w if w in dictionary else word_forms.get(w)
                    if lem is None:
                        continue
                    if first_phase.get(lem) is not None and first_phase[lem] > ph:
                        ahead.append((sc.get("id"), ph, w, lem, first_phase[lem]))
    print("scene words %d used before the course teaches them" % len(ahead))
    for sid, ph, w, lem, fp in sorted(set(ahead))[:25]:
        print("           %s (phase %d) says %r, and %s is first taught in phase %d"
              % (sid, ph, w, lem, fp))
    print("patterns   %d written (%d published)"
          % (len(patterns), sum(1 for x in patterns if x.get("id") in core_ids)))
    for p_ in pattern_problems[:25]:
        print("PROBLEM: %s" % p_)
    print("momo       %d lines, %d gated on vocabulary, %d unearnable trigger(s)"
          % (len(momo), sum(1 for x in momo if x.get("trigger")),
             momo_dead_weight))
    for p_ in momo_problems[:25]:
        print("PROBLEM: %s" % p_)
    for p in problems[:25]:
        print("PROBLEM: %s" % p)
    if len(problems) > 25:
        print("PROBLEM: ... and %d more" % (len(problems) - 25))

    # A progress file that cannot go stale, because nobody writes it by hand.
    # If this work is picked up by a fresh agent with no context, this and
    # HANDOFF.md are what tell it where things stand.
    done = [s for s in spine if s["id"] in written]
    todo = [s for s in spine if s["id"] not in written]
    lines = [u"# Progress", u"",
             u"Written by `stage.py`. Do not edit by hand.", u"",
             u"**%d of %d stories written** - %s of ~148,000 running words."
             % (len(done), len(spine), format(words, ",")), u""]
    by_phase = {}
    for sp in spine:
        d = by_phase.setdefault(sp["phase"], [0, 0])
        d[1] += 1
        if sp["id"] in written:
            d[0] += 1
    lines += [u"| Phase | Written | Total |", u"|---|---|---|"]
    for ph in sorted(by_phase):
        lines.append(u"| %d | %d | %d |" % (ph, by_phase[ph][0], by_phase[ph][1]))
    lines += [u"", u"## Next to write", u""]
    for sp in todo[:20]:
        lines.append(u"- `%s` **%s** - %s" % (sp["id"], sp["title"], sp["desc"]))
    if len(todo) > 20:
        lines.append(u"- ... and %d more in `plan/spine.json`" % (len(todo) - 20))
    with io.open(os.path.join(content, "plan", "PROGRESS.md"), "w", encoding="utf-8") as f:
        f.write(NEWLINE.join(lines) + NEWLINE)

    if missing:
        out = os.path.join(content, "plan", "needs-entry.txt")
        with io.open(out, "w", encoding="utf-8") as f:
            f.write(u"\n".join(missing))
        print("entries    %d words used but not in the dictionary "
              "(plan/needs-entry.txt)" % len(missing))

    return (len(off) + len(problems) + len(stray) + len(scene_problems)
            + len(pattern_problems) + len(momo_problems) + len(override_problems))


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
