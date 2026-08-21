# -*- coding: utf-8 -*-
"""Bundles a language's whole course into one file.

Downloading 123 separate JSON files took over two minutes on a good
connection, which is not a first run anybody should have on Nicaraguan
mobile data. This flattens the lot into content/pack.json, so the app makes
one request instead, and writes a tiny content/version.json so checking for
updates does not mean pulling the whole pack down again.

Run inside a language content repo:

    python build-pack.py --root . --language es-ni --version 2026-08-17+abc1234

It is what the repo's GitHub Action runs on every push, so publishing a
lesson stays "edit the JSON, commit" and nothing else.
"""
import argparse, io, json, os, sys

import forms as morphology

NEWLINE = chr(10)

def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


# When Momo opens his beak. Every one of these needs at least one line the
# learner has already earned on day one, or a beginner meets a silent bird.
MOMO_WHEN = ("welcome", "back", "poke", "great", "ok", "poor", "goal", "pattern", "sleep")
MOMO_STATE = ("happy", "cheer", "speak", "wrong", "sleep")


def check_momo(doc, problems):
    """Validate content/momo.json and return the cleaned list of lines."""
    lines = doc.get("lines") if isinstance(doc, dict) else doc
    if not isinstance(lines, list) or not lines:
        problems.append("momo: expected a non-empty 'lines' list")
        return None

    seen, starters, said = set(), set(), {}
    for i, ln in enumerate(lines):
        where = "momo line %d" % (i + 1)
        if not isinstance(ln, dict):
            problems.append("%s: should be an object" % where)
            continue

        lid = ln.get("id")
        if not lid:
            problems.append("%s: has no id" % where)
        elif lid in seen:
            problems.append("%s: duplicate id %s" % (where, lid))
        else:
            seen.add(lid)
        where = "momo line %s" % (lid or i + 1)

        when = ln.get("when")
        if when not in MOMO_WHEN:
            problems.append("%s: 'when' must be one of %s, got %r"
                            % (where, ", ".join(MOMO_WHEN), when))
        if ln.get("state") not in MOMO_STATE:
            problems.append("%s: 'state' must be one of %s, got %r"
                            % (where, ", ".join(MOMO_STATE), ln.get("state")))
        say = (ln.get("say") or "").strip()
        if not say:
            problems.append("%s: 'say' is empty" % where)
        elif say in said:
            # Two moments sharing wording reads as a bug on screen: a bad score
            # followed by the daily goal said "¡Qué tuani!" twice in a row and
            # looked like he was praising the score he had just marked down.
            problems.append("%s: says the same as %s — %r" % (where, said[say], say))
        else:
            said[say] = lid or i + 1

        trigger = ln.get("trigger") or []
        if not isinstance(trigger, list) or any(not isinstance(w, str) for w in trigger):
            problems.append("%s: 'trigger' must be a list of words" % where)
            trigger = []
        mn = ln.get("min", 1 if trigger else 0)
        if not isinstance(mn, int) or mn < 0:
            problems.append("%s: 'min' must be a whole number" % where)
        elif mn > len(trigger):
            problems.append("%s: needs %d of %d trigger words — unreachable"
                            % (where, mn, len(trigger)))

        if not trigger:
            starters.add(when)

    missing = [w for w in MOMO_WHEN if w not in starters]
    if missing:
        problems.append("momo: no ungated line for %s — a brand new learner "
                        "would get silence there" % ", ".join(missing))

    return lines

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--language", required=True)
    ap.add_argument("--version", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    content_dir = os.path.join(args.root, "content")
    manifest_path = os.path.join(content_dir, "manifest.json")
    if not os.path.exists(manifest_path):
        sys.exit("no content/manifest.json in %s" % os.path.abspath(args.root))
    manifest = read(manifest_path)

    problems = []

    def load(rel, what):
        p = os.path.join(content_dir, rel)
        if not os.path.exists(p):
            problems.append("%s: missing file %s" % (what, rel))
            return None
        try:
            return read(p)
        except ValueError as e:
            problems.append("%s: %s is not valid JSON (%s)" % (what, rel, e))
            return None

    # dictionary — several files merged into one map
    dictionary = {}
    for rel in manifest.get("dictionary", []):
        part = load(rel, "dictionary")
        if isinstance(part, dict):
            dictionary.update(part)
        elif part is not None:
            problems.append("dictionary: %s should be an object" % rel)

    # patterns
    patterns = []
    for rel in manifest.get("patterns", []):
        part = load(rel, "patterns")
        if isinstance(part, list):
            patterns.extend(part)
        elif isinstance(part, dict):
            patterns.append(part)

    def collect(key):
        out = []
        for entry in manifest.get(key, []):
            rel = entry.get("path")
            if not rel:
                problems.append("%s: entry %s has no path" % (key, entry.get("id")))
                continue
            body = load(rel, key)
            if body is None:
                continue
            merged = dict(entry)
            merged.pop("path", None)
            merged.update(body)
            out.append(merged)
        return out

    lessons = collect("lessons")
    scenarios = collect("scenarios")

    verbs = load(manifest["verbs"], "verbs") if manifest.get("verbs") else None
    emergency = load(manifest["emergency"], "emergency") if manifest.get("emergency") else None

    # What the mascot is allowed to say, and when he has earned the right to
    # say it. Each line is gated on vocabulary the learner has actually met,
    # using the same trigger/min shape as patterns, so he only ever speaks
    # words you would understand — and he grows more idiomatic as you do.
    momo = load(manifest["momo"], "momo") if manifest.get("momo") else None
    if momo is not None:
        momo = check_momo(momo, problems)

    # Sanity checks worth failing a push over — a broken pack breaks the app
    # for everyone at once, and it is far cheaper to catch it here.
    ids = {}
    for kind, items in (("lesson", lessons), ("scenario", scenarios)):
        for item in items:
            i = item.get("id")
            if not i:
                problems.append("%s with no id" % kind)
            elif (kind, i) in ids:
                problems.append("duplicate %s id: %s" % (kind, i))
            ids[(kind, i)] = True
            if kind == "lesson" and not item.get("sn"):
                problems.append("lesson %s has no sentences" % i)
            if kind == "scenario" and not item.get("steps"):
                problems.append("scenario %s has no steps" % i)

    features = manifest.get("features")
    if not features:
        features = ["words"]
        if lessons: features += ["reader", "review", "order"]
        if scenarios: features.append("scenes")
        if patterns: features.append("patterns")
        if verbs: features.append("verbs")
        # Audio is opt-in: several languages have no speech voice at all.

    # Inflected forms -> the dictionary entry they belong to.
    #
    # Spanish inflects hard and the dictionary is keyed on lemmas, so a reader
    # who tapped "hablas", "pregunto" or "palabras" got nothing back: no
    # meaning, no exposure, no colour on the word. Worse, the memory model
    # treated "cosa" and "cosas" as two unrelated words that each decayed on
    # their own, so knowing one earned you nothing for the other.
    #
    # Only forms that actually occur in this course's own text are emitted, so
    # every mapping can be checked against real usage and the pack does not
    # carry a conjugation table nobody can reach. Anything two lemmas could
    # both produce is dropped rather than guessed at.
    corpus = []
    for lesson in lessons:
        for sn in lesson.get("sn") or lesson.get("sentences") or []:
            corpus.append(sn.get("s") or sn.get("es") or "")
    for scene in scenarios:
        for st in scene.get("steps") or []:
            corpus.append(st.get("es") or "")
            for o in st.get("options") or []:
                corpus.append(o.get("es") or "")

    word_forms, ambiguous, seen_words = morphology.build(dictionary, corpus, verbs or {})

    # A hand-written escape hatch, because no rule set is ever right about
    # every word. {"form": "lemma"} pins one; {"form": null} blocks one.
    overrides = {}
    ov_path = os.path.join(content_dir, "dictionary", "forms-overrides.json")
    if os.path.exists(ov_path):
        try:
            overrides = read(ov_path) or {}
        except ValueError as e:
            problems.append("forms-overrides.json is not valid JSON (%s)" % e)
    for form, lemma in overrides.items():
        form = form.lower()
        if lemma is None:
            word_forms.pop(form, None)
        elif lemma in dictionary:
            word_forms[form] = lemma
        else:
            problems.append("forms-overrides: %r points at %r, which is not a "
                            "dictionary entry" % (form, lemma))

    pack = {
        "version": args.version,
        "language": args.language,
        "name": manifest.get("name"),
        "speech": manifest.get("speech"),
        "features": features,
        "dictionary": dictionary,
        "forms": word_forms,
        "patterns": patterns,
        "lessons": lessons,
        "scenarios": scenarios,
        "verbs": verbs,
        "emergency": emergency,
        "momo": momo,
    }

    if problems:
        for p in problems:
            print("ERROR: %s" % p)
        sys.exit("refusing to build a broken pack (%d problem(s))" % len(problems))

    out_dir = args.out or content_dir
    pack_path = os.path.join(out_dir, "pack.json")
    with io.open(pack_path, "w", encoding="utf-8") as f:
        json.dump(pack, f, ensure_ascii=False, separators=(",", ":"))

    # Tiny sidecar so "is there anything new?" is a 60-byte request.
    with io.open(os.path.join(out_dir, "version.json"), "w", encoding="utf-8") as f:
        json.dump({"version": args.version, "lessons": len(lessons),
                   "scenarios": len(scenarios), "words": len(dictionary)},
                  f, ensure_ascii=False)

    size = os.path.getsize(pack_path)
    print("pack.json  %d lessons, %d scenarios, %d words, %d patterns%s" %
          (len(lessons), len(scenarios), len(dictionary), len(patterns),
           ", verbs" if verbs else ""))
    print("features   %s" % ", ".join(features))

    # What the reader can and cannot look up. A word with no entry and no form
    # is a word the learner taps and nothing happens, so the number is worth
    # having in front of you on every build.
    tappable = sum(1 for w in seen_words if w in dictionary or w in word_forms)
    # Counted by running word, because that is what the reader actually meets:
    # the distinct-word figure is dragged down by a long tail of names and
    # one-off forms nobody taps twice.
    hits = total = 0
    for line in corpus:
        for w in morphology.tokens(line):
            total += 1
            if w in dictionary or w in word_forms:
                hits += 1
    print("forms      %d inflections mapped, %d dropped as ambiguous"
          % (len(word_forms), len(ambiguous)))
    print("lookups    %.1f%% of words on the page can be tapped (%d of %d distinct)"
          % (100.0 * hits / max(1, total), tappable, len(seen_words)))
    unresolved = sorted(w for w in seen_words
                        if w not in dictionary and w not in word_forms)
    if unresolved:
        with io.open(os.path.join(out_dir, "unresolved.txt"), "w", encoding="utf-8") as f:
            f.write(NEWLINE.join(unresolved))
        print("           %d have no entry at all - see unresolved.txt"
              % len(unresolved))
    if momo:
        print("momo       %d lines" % len(momo))
    print("size       %.1f KB" % (size / 1024.0))
    print("version    %s" % args.version)


if __name__ == "__main__":
    main()
