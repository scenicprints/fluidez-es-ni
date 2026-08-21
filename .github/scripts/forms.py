# -*- coding: utf-8 -*-
"""Maps the inflected words that appear in the course back to their dictionary entry.

Spanish is heavily inflected and the dictionary is keyed on lemmas, so a reader
who taps "hablas", "pregunto" or "palabras" got nothing back: no meaning, no
exposure, no colour. This generates form -> lemma for every form that ACTUALLY
OCCURS in the lessons and scenes, which keeps the pack small and means every
mapping can be checked against real usage rather than trusted.
"""
import io, json, re, unicodedata

TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)
def tokens(text):
    return [t.lower() for t in TOKEN.findall(text or "")]

def strip_accent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))

# ---- verbs -------------------------------------------------------------
# Regular endings, including the Nicaraguan voseo forms the course is built on.
ENDINGS = {
 "ar": dict(
   pres=["o","as","as","a","amos","an"], vos_pres=["as"],
   pret=["e","aste","aste","o","amos","aron"],
   imp=["aba","abas","abas","aba","abamos","aban"],
   subj=["e","es","es","e","emos","en"],
   imper=["a","a"], ger=["ando"], part=["ado","ada","ados","adas"]),
 "er": dict(
   pres=["o","es","es","e","emos","en"], vos_pres=["es"],
   pret=["i","iste","iste","io","imos","ieron"],
   imp=["ia","ias","ias","ia","iamos","ian"],
   subj=["a","as","as","a","amos","an"],
   imper=["e","e"], ger=["iendo"], part=["ido","ida","idos","idas"]),
 "ir": dict(
   pres=["o","es","is","e","imos","en"], vos_pres=["is"],
   pret=["i","iste","iste","io","imos","ieron"],
   imp=["ia","ias","ias","ia","iamos","ian"],
   subj=["a","as","as","a","amos","an"],
   imper=["e","i"], ger=["iendo"], part=["ido","ida","idos","idas"]),
}
# Accented spellings the plain tables above cannot carry.
ACCENTED = {
 "ar": ["as","e","o","abamos","emos"], "er": ["es","i","io","ia","ias","iamos","ian"],
 "ir": ["is","i","io","ia","ias","iamos","ian"],
}
ACCENT_MAP = {"as":u"ás","es":u"és","is":u"í s".replace(" ",""),
              "e":u"é","o":u"ó","i":u"í","io":u"ió",
              "ia":u"ía","ias":u"ías","iamos":u"íamos","ian":u"ían",
              "abamos":u"ábamos","emos":u"émos"}

def stem_changed(inf):
    """Speculative o->ue / e->ie / e->i variants of the stem.

    Spanish changes the stem vowel wherever the stress lands on it: costar ->
    cuesta, poder -> puede, pensar -> piensa, pedir -> pide. Without this,
    "cuesta" resolved to nothing at all, and this is one of the largest verb
    classes in the language.

    Nicaraguan voseo does NOT stem-change - it is "vos podes", never "vos
    puedes" - and those forms are generated from the plain stem anyway, so
    both spellings are covered.

    Over-generating is safe here: anything that is not actually written in the
    course is thrown away by the corpus filter, and anything two lemmas could
    both produce is dropped as ambiguous. So a wrong guess costs nothing while
    a right one rescues a whole verb.
    """
    stem, tail = inf[:-2], inf[-2:]
    out = []
    for old, new in ((u"o", u"ue"), (u"e", u"ie"), (u"e", u"i"), (u"u", u"ue")):
        at = stem.rfind(old)
        if at < 0:
            continue
        out.append(stem[:at] + new + stem[at + 1:] + tail)
    return out


def verb_forms(inf):
    """Every regular form of one infinitive, accent variants included.

    Reflexive infinitives are handled by dropping the pronoun first. A whole
    class of extremely common verbs ends in -se - llamarse, sentarse, irse,
    reirse, levantarse - and taking the last two letters of those gives "se",
    which is in no conjugation table, so every one of them produced no forms
    at all and every one of their inflections was dead on the page.
    """
    if inf.endswith("se") and len(inf) > 4 and strip_accent(inf[-4:-2]) in ENDINGS:
        inf = inf[:-2]
    if len(inf) < 3: return []
    # reir and oir carry an accent on the ending. Their real forms are
    # irregular, so the regular tables produce nonsense for them - but nonsense
    # never occurs in the text and is dropped by the corpus filter, while the
    # forms that ARE regular still land.
    kind = strip_accent(inf[-2:])
    if kind not in ENDINGS: return []
    stem, out = inf[:-2], set()
    t = ENDINGS[kind]
    for group in ("pres","pret","imp","subj","imper","ger","part","vos_pres"):
        for e in t.get(group, []):
            out.add(stem + e)
            if e in ACCENT_MAP:
                out.add(stem + ACCENT_MAP[e])
    # future and conditional build on the whole infinitive
    for e in [u"é",u"ás",u"á",u"emos",u"án",
              u"ía",u"ías",u"íamos",u"ían"]:
        out.add(inf + e)
    # voseo imperative: hablá, comé, viví
    out.add(stem + {"ar":u"á","er":u"é","ir":u"í"}[kind])
    return [f for f in out if f != inf]

# ---- nouns and adjectives ---------------------------------------------
# Spanish loses the written accent when the stress stops needing marking:
# razón -> razones, inglés -> ingleses, jardín -> jardines. Without this the
# rule produced "razónes", which occurs nowhere, and then "razones" got picked
# up by the verb razonar instead — wrong meaning, confidently shown. Every
# -ción noun in the language is in this class.
FINAL_ACCENT = {u"ón": "on", u"án": "an", u"én": "en", u"ín": "in",
                u"ún": "un", u"és": "es"}

def plural(w):
    if not w: return []
    if w.endswith("z"): return [w[:-1] + "ces"]
    for tail, plain in FINAL_ACCENT.items():
        if w.endswith(tail):
            return [w[:-2] + plain + "es"]
    if w[-1] in u"aeiouáéíóú": return [w + "s"]
    return [w + "es"]

def noun_forms(w):
    return plural(w)

def adj_forms(w):
    out = set(plural(w))
    if w.endswith("o"):
        fem = w[:-1] + "a"
        out.add(fem); out.update(plural(fem)); out.update(plural(w))
    return [f for f in out if f != w]

# Words that must never be produced by a rule. Every one of these is a real
# Spanish word in its own right that the regular tables also happen to spell:
# "esto" falls out of estar, "do" out of dar, "sea" out of ser. Mapping any of
# them shows a confidently wrong definition, which teaches worse than showing
# nothing at all.
NEVER = set(u"""esto esta estas este estos eso esa esas ese esos do da de del la le lo
los las les se su sus mi mis tu tus un una uno unos unas al a e o y ni que qui como
cuando donde para por sin con sobre tras nos os me te si no ya mas pero sea seas
sean seria serias ser ir voy vas van vamos fue fui era eras eran""".split())


def irregular_forms(verbs):
    """The real forms of the irregular verbs, straight from verbs.json.

    Rules cannot produce these: estar's first person is "estoy", not "esto".
    Generating regular forms for an irregular verb is exactly how "esto" ends
    up pointing at estar, so irregulars are never rule-generated at all.
    """
    out = {}
    for lemma, tenses in (verbs.get("irregular") or {}).items():
        for forms in tenses.values():
            for f in forms or []:
                f = (f or "").strip().lower()
                if f and " " not in f:
                    out.setdefault(f, set()).add(lemma)
    return out


def build(dictionary, texts, verbs=None):
    """form -> lemma, for forms that occur in `texts` and are not entries themselves."""
    used = set()
    for t in texts: used.update(tokens(t))

    verbs = verbs or {}
    irregular = set((verbs.get("irregular") or {}).keys())

    candidates = {}   # form -> set(lemma)
    for f, lemmas in irregular_forms(verbs).items():
        if f in dictionary or f not in used:
            continue
        candidates.setdefault(f, set()).update(lemmas)

    for lemma, entry in dictionary.items():
        pos = (entry.get("pos") or "").split("/")[0]
        if " " in lemma:            # multi-word phrases do not inflect here
            continue
        if pos == "v" and lemma in irregular: gen = []   # verbs.json already said
        elif pos == "v":
            gen = verb_forms(lemma)
            for variant in stem_changed(lemma):
                gen.extend(verb_forms(variant))
        elif pos == "n": gen = noun_forms(lemma)
        elif pos == "adj": gen = adj_forms(lemma)
        # Anything ending in -o agrees like an adjective whatever it is tagged.
        # "todo" is filed as a pronoun and "mucho" as an adverb, so toda,
        # todas, muchos and mucha resolved to nothing - and those are among the
        # commonest words in the language.
        elif lemma.endswith("o"): gen = adj_forms(lemma)
        else: gen = []
        for f in gen:
            if f in dictionary:     # a real entry always wins over a guess
                continue
            if f not in used:       # nobody can ever tap it, so do not ship it
                continue
            if f in NEVER or strip_accent(f) in NEVER:
                continue
            candidates.setdefault(f, set()).add(lemma)

    # Count how often each lemma is itself written out, to settle collisions.
    counts = {}
    for t in texts:
        for w in tokens(t):
            if w in dictionary: counts[w] = counts.get(w, 0) + 1

    # A form two lemmas can both produce is dropped, not guessed at. "decido"
    # is decidir far more often than decir, and picking the commoner lemma got
    # it wrong; a word that shows nothing is recoverable, a word that shows the
    # wrong meaning is not.
    forms, ambiguous = {}, []
    for f, lemmas in candidates.items():
        if len(lemmas) == 1:
            forms[f] = next(iter(lemmas))
        else:
            ambiguous.append((f, sorted(lemmas)))
    return forms, ambiguous, used
