# -*- coding: utf-8 -*-
"""Runs the dialect gate over the game, which dialect.py cannot reach.

    python .github/scripts/dialect_game.py --root .

dialect.py refuses to publish Spanish that is not Nicaraguan, but its
collect() only knows about lessons, scenes and momo lines -- the game did not
exist when it was written. This feeds it the game instead, and it is the same
word lists doing the judging.

ONLY THE SPANISH FIELDS GO IN, and that is the whole subtlety. A beat carries
English as well as Spanish: `objective` and `en` are instructions to the
player, and `good` and `culture` are notes about the language written in
English. Feed those to the gate and it flags "nothing here comes in a packet"
for the tu form `comes`, and "gone by ten" for the tu imperative `ten`. Three
of those turned up the first time this ran, all of them nonsense, and a gate
that cries wolf is a gate somebody switches off.
"""
import argparse, io, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dialect

# The fields that are actually Spanish. Everything else in a beat is English
# on purpose.
SPANISH = ('es', 'say')
CHUNKS = ('tiles', 'extra', 'ok')


def rows_of(root):
    rows = []
    gdir = os.path.join(root, 'content', 'game')
    if not os.path.isdir(gdir):
        return rows
    for name in sorted(os.listdir(gdir)):
        if not name.endswith('.json'):
            continue
        m = json.load(io.open(os.path.join(gdir, name), encoding='utf-8'))
        for i, b in enumerate(m.get('beats') or [], 1):
            for k in SPANISH:
                rows.append({'id': u'%s beat %d %s' % (m['id'], i, k),
                             'say': b.get(k) or u''})
            for k in CHUNKS:
                for t in b.get(k) or []:
                    rows.append({'id': u'%s beat %d %s' % (m['id'], i, k),
                                 'say': t})
    cdir = os.path.join(gdir, 'crowd')
    if os.path.isdir(cdir):
        for name in sorted(os.listdir(cdir)):
            if not name.endswith('.json'):
                continue
            for j, h in enumerate(json.load(io.open(os.path.join(cdir, name),
                                                    encoding='utf-8')), 1):
                rows.append({'id': u'crowd %s %d' % (name[:-5], j),
                             'say': h.get('says') or u''})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--report')
    a = ap.parse_args()

    rows = rows_of(a.root)
    allow_path = os.path.join(a.root, 'content', 'dialect-allow.json')
    allow = {}
    if os.path.exists(allow_path):
        allow = json.load(io.open(allow_path, encoding='utf-8'))
    violations, voseo = dialect.check({'momo': rows}, allow)

    L = [u'checked  %d Spanish strings in the game' % len(rows),
         u'voseo    %d occurrences' % voseo]
    if violations:
        L.append(u'dialect  %d line(s) are not Nicaraguan:' % len(violations))
        for where, word, why, text in violations[:40]:
            L.append(u'PROBLEM: %s  %s  %s' % (where, word, why))
            L.append(u'         %s' % text[:96])
    else:
        L.append(u'dialect  clean -- every line is Nicaraguan')
    out = u'\n'.join(L) + u'\n'
    if a.report:
        io.open(a.report, 'w', encoding='utf-8').write(out)
    print(out.encode('ascii', 'replace').decode('ascii'))
    return len(violations)


if __name__ == '__main__':
    sys.exit(1 if main() else 0)
