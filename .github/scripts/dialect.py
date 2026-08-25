# -*- coding: utf-8 -*-
"""Refuses to publish Spanish that is not Nicaraguan.

The whole point of the course is that somebody finishes it sounding like they
live in Managua. A tu form here, a Mexicanism there, and they finish it
sounding like a telenovela instead -- and none of it is visible by reading a
lesson, because it hides one word at a time across a hundred thousand.

So it is a build gate, exactly like the JSON validation: content that is not
Nicaraguan does not ship.

Only forms that are UNAMBIGUOUSLY tu are listed. Nicaraguan voseo shares
several forms with tu -- "vas", "estas", "das", "ves" are correct with vos --
and flagging those would make the gate cry wolf until somebody switched it off.
"""
import io, json, os, re

# Tu forms voseo replaces. Every one differs from the vos form, usually by the
# accent: comes/comes, hablas/hablas, piensas/pensas.
TU_FORMS = u"""
eres tienes quieres puedes haces dices vienes sabes hablas comes vives
piensas entiendes conoces sientes duermes juegas pides sigues pones sales
traes llegas trabajas necesitas vuelves recuerdas empiezas encuentras debes
crees lees oyes mueres esperas buscas tomas llevas dejas pasas quedas
aprendes escribes abres recibes subes decides respondes miras
caminas compras pagas ayudas cierras pierdes sirves repites eliges
""".split()

# Tu imperatives. "se" and "ve" are left out on purpose: they collide with
# saber and ver, which are everywhere and perfectly correct.
# "ven" is also they-see, "oye" is he-hears, "di" is I-gave, and "sal" is
# salt. All four are ordinary Nicaraguan words far more often than they are
# tu imperatives, and flagging them means flagging correct prose.
TU_IMPERATIVES = u"ten haz pon".split()

# Tu imperatives with the pronoun stuck on the end, which is where they hide.
# The bare forms above are only three words because most tu imperatives collide
# with something ordinary -- but once a pronoun is attached, the stress moves
# and the accent goes on the STEM, and the vos form accents the ending instead:
# tu pasamela / vos pasamela with the accent one syllable later, tu cuentame /
# vos contame, tu fijate / vos fijate. Those pairs never collide, so they are
# safe to ban outright.
#
# This list exists because "pasamela" was sitting in the game spine, accented
# the Madrid way, and the gate could not see it. Anything ambiguous is left
# out: "damelo" and "dame" are identical in both dialects, so they are not here.
TU_IMPERATIVES += u"""
pásame pásamela pásamelo pásalo pásala mírame míralo mírala escúchame
escúchalo tómalo tómala tómate cuéntame cuéntamelo cuéntalo espérame
espérate llévame llévalo déjame déjalo déjame déjate ayúdame búscame
búscalo llámame llámalo cómpralo créeme dilo dime dímelo hazlo hazme
hazlos ponlo ponla ponte sígueme síguelo cállate fíjate levántate
siéntate quédate apúrate acuéstate vuélvete piénsalo ciérralo ábrelo
súbete bájate acércate
""".split()
# NOT "vamonos". It is the nosotros imperative -- let's go -- and it is correct
# in every Spanish there is, Nicaraguan included. It was in this list for one
# run and it flagged two perfectly good lines of the published course.
TU_IMPERATIVES = [w for w in TU_IMPERATIVES if "?" not in w]

# Only the vosotros forms Nicaragua does NOT also use.
#
# Every -ir verb collides: "decis", "venis", "vivis", "salis" are vosotros in
# Madrid and vos in Managua, spelled identically. Banning those would flag the
# course for being written correctly, which is how a gate gets switched off.
# The -ar and -er forms are safe, because vos drops the i: hablas/hablais,
# tenes/teneis, sos/sois.
VOSOTROS = u"""
vosotros vosotras vuestro vuestra vuestros vuestras
hablais teneis sois estais quereis podeis haceis sabeis comeis
llamais trabajais bebeis leeis creeis
""".split()

# Words that put the speaker in the wrong country.
FOREIGN = {
    # No tio/tia here: they are uncle and aunt in every Spanish there is, and
    # only Madrid slang uses them for "bloke". A word list cannot tell those
    # apart, and banning them flags every family in the course.
    "Spain": u"""vale coche movil ordenador guay zumo patata gilipollas
                 hostia currar melocoton cutre flipar majo""".split(),
    "Mexico": u"""orale guey wey chido padrisimo andale chamba lana popote antro
                  chavo chava alberca neta chingon chafa naco fresa mande
                  platicame elote camion""".split(),
    "elsewhere": u"""guagua chevere pana bacano parcero chamo boludo pibe quilombo
                     mae tico cipote pisto guaro? colectivo? pololo curro""".split(),
}
FOREIGN["elsewhere"] = [w for w in FOREIGN["elsewhere"] if "?" not in w]

# What Managua actually sounds like. Not a gate, a temperature reading: content
# with no voseo in it at all is a warning sign whatever else it gets right.
VOSEO = u"""
sos tenes queres podes haces? decis venis sabes? hablas? vos andate anda
mira vení decí hace poné salí tené sentate fijate pasa dale come oi trae
espera vos
""".split()
VOSEO = [w for w in VOSEO if "?" not in w]

PUNCT = re.compile(u"[.,;:!?¿¡\"'()«»“”—–]")


def strip_accents(s):
    import unicodedata
    return u"".join(c for c in unicodedata.normalize("NFD", s)
                    if not unicodedata.combining(c))


def words_of(text):
    """Lower-cased words, accents kept AND stripped, so both spellings match."""
    clean = PUNCT.sub(u" ", (text or u"").lower())
    return clean.split()


def collect(pack):
    """Every line of target-language text in the pack, with where it came from."""
    out = []
    for l in pack.get("lessons") or []:
        for sn in l.get("sn") or l.get("sentences") or []:
            out.append((u"lesson %s" % l.get("id"), sn.get("s") or sn.get("es") or u""))
    for s in pack.get("scenarios") or []:
        for st in s.get("steps") or []:
            out.append((u"scene %s" % s.get("id"), st.get("es") or u""))
            for o in st.get("options") or []:
                out.append((u"scene %s reply" % s.get("id"), o.get("es") or u""))
    for m in pack.get("momo") or []:
        out.append((u"momo %s" % m.get("id"), m.get("say") or u""))
    # The interface is target-language text too, and it is the text a learner
    # sees most often — every screen, every day. It used to be skipped here
    # simply because it did not exist when this was written, which is exactly
    # how the game ended up needing a gate of its own.
    for key, value in sorted((pack.get("ui") or {}).items()):
        if isinstance(value, str):
            out.append((u"ui %s" % key, value))
    for i, phase in enumerate(pack.get("phases") or []):
        pair = phase if isinstance(phase, list) else [phase.get("name"), phase.get("desc")]
        for part in pair:
            if isinstance(part, str):
                out.append((u"phase %d" % i, part))
    return out


def check(pack, allow=None):
    """Returns (violations, voseo_count). A violation is a hard build failure."""
    allow = allow or {}
    # A lesson that TEACHES the difference has to be able to write the wrong
    # form: "No es 'tu tienes', sino 'vos tenes'." Those lines are listed by id
    # in dialect-allow.json and skipped.
    skip_ids = set(allow.get("lines") or [])
    skip_words = set(w.lower() for w in (allow.get("words") or []))

    # Two kinds of ban, matched differently.
    #
    # A tu form is matched on its EXACT spelling, because the accent is the
    # whole difference: "comes" is tu, "comes" with the accent on the end is
    # vos and perfectly correct. Stripping accents here would flag every
    # correct Nicaraguan verb in the course.
    exact = {}
    for w in TU_FORMS: exact[w] = u"tu form -- Nicaragua uses vos"
    for w in TU_IMPERATIVES: exact[w] = u"tu imperative -- Nicaragua uses the vos imperative"

    # Foreign vocabulary and vosotros are matched with accents stripped, so
    # "orale", "guey" and "sabeis" are caught however they are typed. These do
    # not collide with anything Nicaraguan, so there is nothing to protect.
    loose = {}
    for w in VOSOTROS: loose[strip_accents(w)] = u"vosotros -- Spain only"
    for country, ws in FOREIGN.items():
        for w in ws: loose[strip_accents(w)] = u"%s, not Nicaragua" % country

    violations, voseo = [], 0
    vos_set = set(VOSEO)
    for where, text in collect(pack):
        if where in skip_ids:
            continue
        for w in words_of(text):
            plain = strip_accents(w)
            if w in vos_set or plain in vos_set:
                voseo += 1
            if w in skip_words or plain in skip_words:
                continue
            why = exact.get(w) or loose.get(plain)
            if why:
                violations.append((where, w, why, text))
    return violations, voseo


def main(pack_path, allow_path=None):
    pack = json.load(io.open(pack_path, encoding="utf-8"))
    allow = {}
    if allow_path and os.path.exists(allow_path):
        allow = json.load(io.open(allow_path, encoding="utf-8"))
    violations, voseo = check(pack, allow)
    print(u"voseo    %d occurrences" % voseo)
    if not violations:
        print(u"dialect  clean -- every line is Nicaraguan")
        return 0
    print(u"dialect  %d line(s) are not Nicaraguan Spanish:" % len(violations))
    for where, word, why, text in violations[:40]:
        print(u"   %-22s %-12s %s" % (where, word, why))
        print(u"      %s" % text[:96])
    if len(violations) > 40:
        print(u"   ... and %d more" % (len(violations) - 40))
    return len(violations)


if __name__ == "__main__":
    import sys
    sys.exit(1 if main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None) else 0)
