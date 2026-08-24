# -*- coding: utf-8 -*-
"""Checks the game while it is being written, and says where it stands.

Same job as stage.py does for the course, and it exists for the same reason:
the missions land a few at a time across many sessions, and without one command
that reports the truth, the plan and the content drift apart until nobody knows
what is left.

    python .github/scripts/game_stage.py --root .

It never publishes anything. It rewrites content/plan/GAME-PROGRESS.md on every
run, so that file can never be stale — nobody writes it by hand.

The two invariants below are what make a mission PLAYABLE, and both have
already caught a real defect:

  * the chunks laid down in their written order must be one of the accepted
    answers, or the beat cannot be won at all;
  * every accepted answer must be buildable from the chunks the tray offers,
    or it is dead data pretending to be a second right answer.
"""
import argparse, io, json, os, re, sys, unicodedata

NEWLINE = chr(10)
PUNCT = set(u"¿?¡!.,;:\"'")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def norm(t):
    """Same normalisation the game grades with: caseless, accentless, bare."""
    t = (t or u"").lower()
    t = u"".join(c for c in unicodedata.normalize("NFD", t)
                 if not unicodedata.combining(c))
    t = u"".join(u" " if c in PUNCT else c for c in t)
    return u" ".join(t.split())


def check_mission(body, problems):
    mid = body.get("id") or "?"
    beats = body.get("beats") or []
    if not beats:
        problems.append(u"%s has no beats" % mid)
    for i, b in enumerate(beats, 1):
        where = u"%s beat %d" % (mid, i)
        for key in ("es", "objective", "key", "say", "en", "good"):
            if not b.get(key):
                problems.append(u"%s has no %s" % (where, key))
        tiles = b.get("tiles") or []
        extra = b.get("extra") or []
        ok = b.get("ok") or []
        if not tiles:
            problems.append(u"%s has no chunks to build with" % where)
            continue
        if not ok:
            problems.append(u"%s accepts nothing" % where)
            continue
        accepted = set(norm(x) for x in ok)
        if norm(u" ".join(tiles)) not in accepted:
            problems.append(
                u"%s cannot be won: the chunks in their written order (%s) are "
                u"not an accepted answer" % (where, norm(u" ".join(tiles))))
        pool = set(norm(u" ".join(tiles + extra)).split())
        for a in ok:
            if not set(norm(a).split()) <= pool:
                problems.append(
                    u"%s accepts %r, which cannot be built from the chunks on "
                    u"offer" % (where, a))
        if not b.get("teaches"):
            problems.append(u"%s teaches nothing, so it feeds no vocabulary" % where)
    return beats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    content = os.path.join(args.root, "content")

    plan = read(os.path.join(content, "plan", "game-spine.json"))
    missions = plan["missions"]
    acts = plan["acts"]
    planned = dict((m["id"], m) for m in missions)

    written, beats_total = {}, 0
    problems, stray = [], []
    game_dir = os.path.join(content, "game")
    if os.path.isdir(game_dir):
        for name in sorted(os.listdir(game_dir)):
            if not name.endswith(".json"):
                continue
            body = read(os.path.join(game_dir, name))
            mid = body.get("id") or name[:-5]
            if mid not in planned:
                stray.append(mid)
            written[mid] = body
            beats_total += len(check_mission(body, problems))

    # Which chunks are taught, and which are re-used later — the fade ladder
    # only works if a phrase comes back, so a chunk taught once and never seen
    # again is a phrase the player meets on rung one forever.
    taught, reused = {}, {}
    for m in missions:
        for c in m.get("teaches", []):
            taught.setdefault(c, []).append(m["id"])
    once = sorted(c for c, ids in taught.items() if len(ids) == 1)

    print("planned    %d missions across %d acts, %d chunks"
          % (len(missions), len(acts), len(taught)))
    print("written    %d of %d missions, %d beats"
          % (len(written), len(missions), beats_total))
    for a in sorted(acts, key=int):
        ms = [m for m in missions if str(m["act"]) == a]
        done = sum(1 for m in ms if m["id"] in written)
        print("act %s      %d of %d  %s" % (a, done, len(ms), acts[a]["name"]))
    print("recycling  %d chunk(s) taught in only one mission" % len(once))
    if once:
        print("           %s" % u", ".join(once[:12]))
    for s in stray:
        print("PROBLEM: %s is not on the game spine" % s)
    for p in problems[:25]:
        print("PROBLEM: %s" % p)
    if len(problems) > 25:
        print("PROBLEM: ... and %d more" % (len(problems) - 25))

    lines = [u"# Game progress", u"",
             u"Written by `game_stage.py`. Do not edit by hand.", u"",
             u"**%d of %d missions written.**" % (len(written), len(missions)), u""]
    for a in sorted(acts, key=int):
        ms = [m for m in missions if str(m["act"]) == a]
        done = sum(1 for m in ms if m["id"] in written)
        lines += [u"## Act %s — %s (%d/%d)" % (a, acts[a]["name"], done, len(ms)),
                  u"*%s*" % acts[a]["desc"], u"",
                  u"| | mission | who | what you are doing |",
                  u"|---|---|---|---|"]
        for m in ms:
            lines.append(u"| %s | `%s` **%s** | %s | %s |"
                         % (u"x" if m["id"] in written else u" ",
                            m["id"], m["title"], m["who"], m["goal"]))
        lines.append(u"")
    with io.open(os.path.join(content, "plan", "GAME-PROGRESS.md"),
                 "w", encoding="utf-8") as f:
        f.write(NEWLINE.join(lines) + NEWLINE)

    return len(problems) + len(stray)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
