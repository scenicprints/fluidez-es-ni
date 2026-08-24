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
    districts = plan["districts"]
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

    # Nothing on the map is signposted, so the crowd IS the quest system: a
    # mission nobody in the street points at is a mission nobody can find.
    hints = {}
    hint_dir = os.path.join(content, "game", "crowd")
    if os.path.isdir(hint_dir):
        for name in sorted(os.listdir(hint_dir)):
            if not name.endswith(".json"):
                continue
            for row in read(os.path.join(hint_dir, name)) or []:
                for mid in row.get("points_at") or []:
                    hints.setdefault(mid, []).append(row)
    unfindable = [m["id"] for m in missions
                  if m["id"] in written and not hints.get(m["id"])]

    # A chunk taught once and never met again strands the player on rung one,
    # because the help ladder only fades when a phrase comes back.
    met = {}
    for m in missions:
        for c in m.get("teaches", []) + m.get("reuses", []):
            met[c] = met.get(c, 0) + 1
    cold = [c for c in plan.get("core", []) if met.get(c, 0) < 3]

    print("planned    %d missions across %d districts, %d chunks"
          % (len(missions), len(districts), len(met)))
    print("written    %d of %d missions, %d beats"
          % (len(written), len(missions), beats_total))
    for d in sorted(districts, key=lambda k: -sum(1 for m in missions if m["district"] == k)):
        ms = [m for m in missions if m["district"] == d]
        done = sum(1 for m in ms if m["id"] in written)
        print("%-11s%d of %d  %s" % (d, done, len(ms), districts[d]["name"]))
    print("tiers      %s" % u"  ".join(
        u"t%d %d/%d" % (t, sum(1 for m in missions if m["tier"] == t and m["id"] in written),
                        sum(1 for m in missions if m["tier"] == t)) for t in (1, 2, 3, 4, 5)))
    print("crowd      %d mission(s) nobody in the street points at" % len(unfindable))
    print("recycling  %d everyday phrase(s) that do not come back often enough"
          % len(cold))
    if cold:
        print("           %s" % u", ".join(cold[:12]))
    for s_ in stray:
        print("PROBLEM: %s is not on the game spine" % s_)
    for u_ in unfindable[:10]:
        print("PROBLEM: %s is written but unfindable - no crowd hint points at it" % u_)
    for p_ in problems[:25]:
        print("PROBLEM: %s" % p_)
    if len(problems) > 25:
        print("PROBLEM: ... and %d more" % (len(problems) - 25))

    lines = [u"# Game progress", u"",
             u"Written by `game_stage.py`. Do not edit by hand.", u"",
             u"> %s" % plan.get("premise", u""), u"",
             u"**%d of %d missions written.**" % (len(written), len(missions)), u""]
    for d in districts:
        ms = [m for m in missions if m["district"] == d]
        if not ms:
            continue
        done = sum(1 for m in ms if m["id"] in written)
        lines += [u"## %s (%d/%d)" % (districts[d]["name"], done, len(ms)),
                  u"*%s*" % districts[d]["desc"], u"",
                  u"| | tier | mission | who | what you are doing |",
                  u"|---|---|---|---|---|"]
        for m in sorted(ms, key=lambda x: (x["tier"], x["id"])):
            lines.append(u"| %s | %d | `%s` **%s** | %s | %s |"
                         % (u"x" if m["id"] in written else u" ", m["tier"],
                            m["id"], m["title"], m["who"], m["goal"]))
        lines.append(u"")
    with io.open(os.path.join(content, "plan", "GAME-PROGRESS.md"),
                 "w", encoding="utf-8") as f:
        f.write(NEWLINE.join(lines) + NEWLINE)

    return len(problems) + len(stray) + len(unfindable)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
