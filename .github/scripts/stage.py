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

    return len(off) + len(problems) + len(stray) + len(scene_problems)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
