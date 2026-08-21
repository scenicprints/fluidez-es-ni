# -*- coding: utf-8 -*-
"""Maps the inflected words that appear in the course back to their dictionary entry.

Spanish is heavily inflected and the dictionary is keyed on lemmas, so a reader
who taps "hablas", "pregunto" or "palabras" got nothing back: no meaning, no
exposure, no colour. This generates form -> lemma for every form that ACTUALLY
OCCURS in the lessons and scenes, which keeps the pack small and means every
mapping can be checked against real usage rather than trusted.

Three things decide who owns a form, in this order:

  1. **Stated** - verbs.json says so. The irregular tables are facts, not
     guesses, and they beat anything a rule produced. Without this, "dijo" was
     dropped as ambiguous between decir (which states it) and dejar (whose
     speculative e->i stem change happens to spell it), and "dijo" is one of
     the hundred commonest words in the course.
  2. **Ruled** - the regular tables, the plural rules, and clitics attached to
     an infinitive, a gerund or an imperative.
  3. **Weak** - the gerund and participle of an IRREGULAR verb, which the
     regular tables usually get right ("pensando", "pidiendo") and sometimes
     do not ("deciendo"). A weak claim loses every collision, so a wrong guess
     can never take a form away from a lemma that has a real claim on it.

Within a tier a form two lemmas could both produce is dropped rather than
guessed at - except for a plain/reflexive pair (quedar/quedarse), which is
settled from the text: see `resolve_pair`.
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
   imper=["a","a"], ger=["ando"], part=["ado","ada","ados","adas"],
   psubj=[u"ara", u"aras", u"áramos", u"aran"]),
 "er": dict(
   pres=["o","es","es","e","emos","en"], vos_pres=["es"],
   pret=["i","iste","iste","io","imos","ieron"],
   imp=["ia","ias","ias","ia","iamos","ian"],
   subj=["a","as","as","a","amos","an"],
   imper=["e","e"], ger=["iendo"], part=["ido","ida","idos","idas"],
   psubj=[u"iera", u"ieras", u"iéramos", u"ieran"]),
 "ir": dict(
   pres=["o","es","is","e","imos","en"], vos_pres=["is"],
   pret=["i","iste","iste","io","imos","ieron"],
   imp=["ia","ias","ias","ia","iamos","ian"],
   subj=["a","as","as","a","amos","an"],
   imper=["e","i"], ger=["iendo"], part=["ido","ida","idos","idas"],
   psubj=[u"iera", u"ieras", u"iéramos", u"ieran"]),
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


def plain_infinitive(inf):
    """The infinitive with any reflexive -se taken off, or None if it is not one.

    A whole class of extremely common verbs ends in -se - llamarse, sentarse,
    irse, reirse, levantarse - and taking the last two letters of those gives
    "se", which is in no conjugation table, so every one of them produced no
    forms at all and every one of their inflections was dead on the page.
    """
    if inf.endswith("se") and len(inf) > 4 and strip_accent(inf[-4:-2]) in ENDINGS:
        inf = inf[:-2]
    if len(inf) < 2:
        return None
    return inf if strip_accent(inf[-2:]) in ENDINGS else None


def verb_forms(inf):
    """Every regular form of one infinitive, accent variants included."""
    inf = plain_infinitive(inf)
    if not inf:
        return []
    # reir and oir carry an accent on the ending. Their real forms are
    # irregular, so the regular tables produce nonsense for them - but nonsense
    # never occurs in the text and is dropped by the corpus filter, while the
    # forms that ARE regular still land.
    kind = strip_accent(inf[-2:])
    stem, out = inf[:-2], set()
    t = ENDINGS[kind]
    for group in ("pres","pret","imp","subj","imper","ger","part","vos_pres","psubj"):
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


def spelling_classes(inf):
    """conozco, agradezco, ofrezco, dirijo, escojo - and their subjunctives.

    Every -cer/-cir verb with a vowel in front of the c puts a z there in the
    first person and right through the subjunctive, and every -ger/-gir verb
    swaps the g for a j. Neither is an exception anybody learns one verb at a
    time, and without them "agradezco", "reconozco", "pertenezco", "conozcas"
    and "dirijo" were all dead on the page.
    """
    inf = plain_infinitive(inf)
    if not inf or len(inf) < 5:
        return []
    stem, kind = inf[:-2], strip_accent(inf[-2:])
    if kind not in ("er", "ir"):
        return []
    last, before = strip_accent(stem[-1]), strip_accent(stem[-2])
    if last == "c" and before in u"aeiou":
        root = stem[:-1]
        return [root + t for t in (u"zco", u"zca", u"zcas", u"zcás",
                                   u"zcamos", u"zcan")]
    if last == "g":
        root = stem[:-1]
        return [root + t for t in (u"jo", u"ja", u"jas", u"jás",
                                   u"jamos", u"jan")]
    return []


def spelling_changes(inf):
    """llegué, busqué, empecé - and the subjunctives that go with them.

    Spanish respells the last consonant of the stem rather than change its
    sound: -car takes qu before an e, -gar takes gu, -zar takes c. So the one
    form of these verbs a learner writes constantly - "yo llegué", "yo busqué",
    "yo empecé" - is the one no regular table produces.
    """
    inf = plain_infinitive(inf)
    if not inf or len(inf) < 5 or strip_accent(inf[-2:]) != "ar":
        return []
    stem = inf[:-2]
    swap = {"c": u"qu", "g": u"gu", "z": u"c"}.get(strip_accent(stem[-1]))
    if not swap:
        return []
    root = stem[:-1] + swap
    return [root + t for t in (u"é", u"e", u"es", u"és", u"emos", u"en")]


def adverb_forms(word):
    """simplemente, perfectamente, claramente - the -mente adverb of an adjective."""
    if word.endswith("o"):
        return [word[:-1] + u"amente"]
    if word[-1] in u"aeiléí" or word.endswith("z") or word.endswith("r"):
        return [word + u"mente"]
    return []


def hiatus_forms(inf):
    """confía, guío, crían, río - the -iar and -uar verbs that break the diphthong.

    A handful of verbs pull the stress onto the i or the u where the tables put
    it on the ending, so the rules spell "confia" and "guio" and the course
    writes "confía" and "guío". Over-generated on purpose: the ones that do not
    break the diphthong (cambiar, estudiar) never write these spellings, so the
    corpus filter drops them.
    """
    inf = plain_infinitive(inf)
    if not inf or strip_accent(inf[-3:-2]) not in ("i", "u") or strip_accent(inf[-2:]) != "ar":
        return []
    root = inf[:-3] + MARK[strip_accent(inf[-3:-2])]
    return [root + t for t in (u"o", u"a", u"as", u"an", u"e", u"en", u"es")]


def participle_forms(inf):
    """hablado, hablada, hablados, habladas.

    A participle is the verb form that most often stops being a verb: mandado
    is an errand, comida is food, cansado and ocupado and prestado are
    adjectives the course has entries for. So participles are claimed weakly
    and the entry that explains the word keeps it.
    """
    inf = plain_infinitive(inf)
    if not inf:
        return []
    stem = inf[:-2]
    return [stem + e for e in ENDINGS[strip_accent(inf[-2:])]["part"]]


def tu_forms(inf):
    """The tu spellings - hablas, comes, hables - which this course never uses.

    Nicaragua is voseo: it is "vos hablas" written hablas with an accent, "vos
    comes" written comes with one, "que vos hables" written hables with one.
    `dialect.py` fails the build if a tu form is ever written. So the plain
    unaccented 2nd-person endings belong to no word in this course, and all
    they do is collide with real ones: casas is houses, preguntas is questions,
    calles is streets, razones is reasons, puertas is doors. Generated anyway,
    but claimed weakly, so they only ever win when nothing else wants the word.
    """
    inf = plain_infinitive(inf)
    if not inf:
        return []
    stem = inf[:-2]
    return [stem + u"as", stem + u"es", stem + u"is"]


def nonfinite_forms(inf):
    """Just the gerund and the participle, with its four agreements.

    Used for verbs verbs.json calls irregular. Their finite forms must never be
    rule-generated - that is how "esto" ends up pointing at estar - but the
    gerund and the participle are regular for most of them (pensando, pidiendo,
    salido), and without these every one of those words was dead on the page.
    A wrong guess ("deciendo") occurs nowhere and is dropped by the corpus
    filter; a guess that collides with a real word loses, because these are
    claimed in the weak tier.
    """
    inf = plain_infinitive(inf)
    if not inf:
        return []
    kind = strip_accent(inf[-2:])
    stem, t = inf[:-2], ENDINGS[strip_accent(inf[-2:])]
    out = set()
    for group in ("ger", "part"):
        for e in t.get(group, []):
            out.add(stem + e)
    return sorted(out)


# The gerunds and participles no rule can reach. Every one of these is a verb
# the course actually uses; the list is short because it only has to cover the
# irregular ones that occur.
IRREGULAR_NONFINITE = {
    u"decir": [u"diciendo", u"dicho", u"dicha", u"dichos", u"dichas"],
    u"hacer": [u"haciendo"],
    u"ir": [u"yendo", u"ido", u"ida", u"idos", u"idas"],
    u"ser": [u"siendo", u"sido"],
    u"poder": [u"pudiendo"],
    u"venir": [u"viniendo"],
    u"pedir": [u"pidiendo"],
    u"dormir": [u"durmiendo"],
    u"morir": [u"muriendo", u"muerto", u"muerta", u"muertos", u"muertas"],
    u"seguir": [u"siguiendo"],
    u"servir": [u"sirviendo"],
    u"sentir": [u"sintiendo"],
    u"sentirse": [u"sintiendo"],
    u"traer": [u"trayendo", u"traído", u"traída", u"traídos", u"traídas"],
    u"leer": [u"leyendo", u"leído", u"leída", u"leídos", u"leídas"],
    u"creer": [u"creyendo", u"creído"],
    u"caer": [u"cayendo", u"caído", u"caída"],
    u"oír": [u"oyendo", u"oído", u"oída", u"oídos", u"oídas"],
    u"reírse": [u"riendo", u"reído"],
    u"sonreír": [u"sonriendo"],
    u"ver": [u"viendo", u"visto", u"vista", u"vistos", u"vistas"],
    u"poner": [u"puesto", u"puesta", u"puestos", u"puestas"],
    u"componer": [u"compuesto", u"compuesta"],
    u"proponer": [u"propuesto", u"propuesta"],
    u"descomponerse": [u"descompuesto", u"descompuesta"],
    u"volver": [u"vuelto", u"vuelta", u"vueltos", u"vueltas"],
    u"devolver": [u"devuelto", u"devuelta"],
    u"resolver": [u"resuelto", u"resuelta"],
    u"envolver": [u"envuelto", u"envuelta"],
    u"escribir": [u"escrito", u"escrita", u"escritos", u"escritas"],
    u"describir": [u"descrito", u"descrita"],
    u"abrir": [u"abierto", u"abierta", u"abiertos", u"abiertas"],
    u"cubrir": [u"cubierto", u"cubierta"],
    u"descubrir": [u"descubierto", u"descubierta"],
    u"romper": [u"roto", u"rota", u"rotos", u"rotas"],
    u"repetir": [u"repitiendo"],
    u"medir": [u"midiendo"],
    u"corregir": [u"corrigiendo"],
    u"elegir": [u"eligiendo"],
    u"conseguir": [u"consiguiendo"],
    u"despedirse": [u"despidiendo"],
    u"vestirse": [u"vistiendo"],
    u"mentir": [u"mintiendo"],
    u"preferir": [u"prefiriendo"],
    u"advertir": [u"advirtiendo"],
    u"convertirse": [u"convirtiendo"],
    u"arrepentirse": [u"arrepintiendo"],
    u"herir": [u"hiriendo"],
    u"construir": [u"construyendo", u"construido"],
    u"contradecir": [u"contradiciendo", u"contradicho"],
    u"pudrirse": [u"pudriendo", u"podrido", u"podrida", u"podridos", u"podridas"],
    u"freír": [u"friendo", u"frito", u"frita", u"fritos", u"fritas"],
}

# Verbs the course actually inflects that verbs.json does not carry, because
# verbs.json only holds what the Verb Trainer drills. Every form here is
# stated, not guessed, so it wins its collisions the same way the tables do.
# A lemma is only read if the dictionary has an entry for it.
EXTRA_FORMS = {
    u"oír": [u"oigo", u"oís", u"oye", u"oímos", u"oyen", u"oí", u"oíste",
             u"oyó", u"oímos", u"oyeron", u"oía", u"oías", u"oíamos", u"oían",
             u"oiga", u"oigás", u"oigamos", u"oigan", u"oyendo", u"oído", u"oída",
             u"oídos", u"oídas", u"oiré", u"oirá", u"oyera", u"oyeran"],
    u"haber": [u"he", u"has", u"ha", u"hemos", u"han", u"había", u"habías",
               u"habíamos", u"habían", u"hubo", u"hubieron", u"haya", u"hayas",
               u"hayamos", u"hayan", u"habrá", u"habrán", u"habría", u"habrías",
               u"habríamos", u"habrían", u"hubiera", u"hubieras", u"hubiéramos",
               u"hubieran", u"habiendo", u"habido"],
    u"traer": [u"traigo", u"traés", u"trae", u"traemos", u"traen", u"traje",
               u"trajiste", u"trajo", u"trajimos", u"trajeron", u"traía", u"traían",
               u"traiga", u"traigás", u"traigamos", u"traigan", u"trayendo",
               u"traído", u"trajera", u"trajeran"],
    u"reírse": [u"río", u"reís", u"ríe", u"reímos", u"ríen", u"reí", u"reiste",
                u"rió", u"rieron", u"reía", u"reían", u"riendo", u"reído", u"ría",
                u"rían", u"riera", u"rieran"],
    u"sonreír": [u"sonrío", u"sonríe", u"sonríen", u"sonriendo", u"sonrió",
                  u"sonreía", u"sonreían"],
    u"oler": [u"huelo", u"olés", u"huele", u"olemos", u"huelen", u"olía", u"olían",
              u"olió", u"oliendo", u"olido", u"huela", u"huelan"],
    u"morir": [u"muero", u"morís", u"muere", u"morimos", u"mueren", u"murió",
               u"murieron", u"moría", u"muera", u"mueran", u"muriera", u"murieran"],
    u"traducir": [u"traduzco", u"traduce", u"traducen", u"traduje", u"tradujo",
                  u"tradujeron", u"traduzca", u"traduzcan", u"traduciendo"],
    u"producir": [u"produzco", u"produce", u"producen", u"produjo", u"produjeron",
                  u"produzca", u"produciendo"],
    u"conseguir": [u"consigo", u"conseguís", u"consigue", u"conseguimos",
                   u"consiguen", u"conseguí", u"consiguió", u"consiguieron",
                   u"consiga", u"consigan", u"consiguiendo"],
    u"tener": [u"tienes"],
    u"querer": [u"quieres"],
    u"poder": [u"puedes"],
    u"soler": [u"suelo", u"suele", u"solemos", u"suelen", u"solía", u"solían"],
    u"detener": [u"detiene", u"detienen", u"detuvo", u"deteniendo"],
    u"sostener": [u"sostengo", u"sostiene", u"sostienen", u"sostuvo"],
    u"contener": [u"contengo", u"contiene", u"contienen", u"conteniendo"],
    u"convenir": [u"conviene", u"convienen", u"convenía"],
}

# ---- clitics -----------------------------------------------------------
# Spanish glues its pronouns onto the end of an infinitive, a gerund and an
# imperative: acompanarla, arreglarlo, decirme, contame, fijese, haciendolo.
# Nothing in the tables above can produce those, so every one of them was dead
# on the page - and the course is full of them, because that is how people
# actually talk.
OBJECT_CLITICS = [u"lo", u"la", u"le", u"los", u"las", u"les"]
REFLEXIVE_CLITICS = [u"me", u"te", u"se", u"nos"]
# Two pronouns at once: decirmelo, contaselo.
CLITIC_PAIRS = [a + b for a in (u"me", u"te", u"se", u"nos", u"le", u"les")
                for b in (u"lo", u"la", u"los", u"las")]

VOWELS = u"aeiouáéíóú"
MARKED = u"áéíóú"
UNMARK = {u"á": u"a", u"é": u"e", u"í": u"i", u"ó": u"o", u"ú": u"u"}
MARK = {u"a": u"á", u"e": u"é", u"i": u"í", u"o": u"ó", u"u": u"ú"}


def unmark(w):
    return u"".join(UNMARK.get(c, c) for c in w)


def mark_stress(w):
    """`w` with a written accent where the default Spanish stress rule puts it.

    Adding a pronoun makes a word longer without moving its stress, so the
    accent that was not needed before becomes needed: hablando -> hablandome
    is written hablandome with an accent on the -an-, fije -> fijese is
    fijese with one on the -fi-. Marking the base first and then gluing the
    pronoun on gets that right for every shape.
    """
    if any(c in MARKED for c in w):
        return w
    groups, i = [], 0
    while i < len(w):
        if w[i] in VOWELS:
            j = i
            while j < len(w) and w[j] in VOWELS:
                j += 1
            groups.append((i, j))
            i = j
        else:
            i += 1
    if not groups:
        return w
    # Ends in a vowel, n or s: stress the second-last group. Otherwise the last.
    at = groups[-2] if (w[-1] in VOWELS or w[-1] in u"ns") and len(groups) > 1 else groups[-1]
    seg = w[at[0]:at[1]]
    k = len(seg) - 1
    for n, c in enumerate(seg):
        if c in u"aeo":          # the strong vowel of a diphthong carries it
            k = n
    return w[:at[0] + k] + MARK[seg[k]] + w[at[0] + k + 1:]


def clitic_forms(base, clitics):
    """Every spelling of `base` with each of `clitics` glued on.

    All three spellings are emitted - plain, stress-marked and unmarked -
    because which one is correct depends on how many syllables the pronouns
    add (deci + me is "decime", deci + melo is "decimelo" with the accent
    back). The corpus filter throws away the ones nobody wrote.
    """
    out = set()
    for c in clitics:
        for stem in (base, mark_stress(base), unmark(base)):
            out.add(stem + c)
    return out


def verb_bases(lemma, table):
    """The forms a pronoun can be glued to, split by how much they can be trusted.

    Returns (sure, risky). An infinitive or a gerund with a pronoun on it is a
    long, distinctive word that belongs to exactly one verb: acompanarla,
    haciendolo. An imperative is two or three letters, so gluing a pronoun to
    one spells ordinary words - regar gives "regala" and "regalos", ver gives
    "vela" and "velas", comer gives "comete" - and every one of those is a
    different word the course actually uses. So imperatives are claimed weakly
    and lose every argument.
    """
    inf = plain_infinitive(lemma)
    if not inf:
        return [], []
    kind = strip_accent(inf[-2:])
    stem = inf[:-2]
    sure, risky = [inf], []
    for changed in stem_changed(inf):
        stem2 = changed[:-2]
        risky.append(stem2 + ENDINGS[kind]["subj"][0])
        risky.append(stem2 + {"ar": u"a", "er": u"e", "ir": u"e"}[kind])
    if table or lemma in IRREGULAR_NONFINITE:
        for f in ((table or {}).get("imperative") or []):
            if f and " " not in f:
                risky.append(f.strip().lower())
        for f in nonfinite_forms(lemma):
            if f.endswith(u"ndo"):
                sure.append(f)
        subj = (table or {}).get("subjunctive") or []
        for i in (2, 0, 3):
            if len(subj) > i and subj[i] and " " not in subj[i]:
                risky.append(subj[i].strip().lower())   # usted: digame, oigame
        for f in IRREGULAR_NONFINITE.get(lemma, []):
            if f.endswith(u"ndo"):
                sure.append(f)
    else:
        sure.append(stem + ENDINGS[kind]["ger"][0])                       # hablando
        risky.append(stem + {"ar": u"á", "er": u"é", "ir": u"í"}[kind])  # habla
        risky.append(stem + ENDINGS[kind]["subj"][0])                     # hable
        risky.append(stem + ENDINGS[kind]["subj"][4])                     # hablemos
        risky.append(stem + ENDINGS[kind]["subj"][3])                     # hablemos
    # Two letters plus a pronoun is a word, not a form: "ve" + "la" is a candle.
    # The infinitive is exempt - "irse" and "irme" are nothing else.
    return (sure, [b for b in risky if len(b) > 2])


def inflection_of_an_entry(form, dictionary):
    """True when `form` is plainly the plural or the feminine of a real entry.

    abierta, puestos and vueltas are participles of abrir, poner and volver -
    but the course has entries for the adjectives abierto and puesto and the
    noun vuelta, and those own their own inflections. Handing the participle
    to the verb takes the word away from the entry that explains it.
    """
    for cut, tail in ((1, u""), (1, u"o"), (2, u"o"), (3, u"o")):
        if len(form) > cut:
            cand = form[:-cut] + tail
            if cand != form and cand in dictionary:
                return True
    return False


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
    # A word already stressed on its second-last syllable gains a written
    # accent when the plural pushes it further back: joven -> jovenes is
    # written jóvenes, examen -> exámenes, orden -> órdenes. Both spellings
    # are emitted and the corpus filter keeps whichever one is real.
    out = [w + "es"]
    if w[-1] in u"ns":
        marked = mark_stress(w)
        if marked != w:
            out.append(marked + "es")
    return out

def noun_forms(w):
    return plural(w)

def feminine(w):
    """vendedor -> vendedora, peleon -> peleona, espanol -> espanola."""
    for tail, fem in ((u"or", u"ora"), (u"ón", u"ona"), (u"ol", u"ola"),
                      (u"és", u"esa"), (u"ín", u"ina")):
        if w.endswith(tail):
            base = w[:-len(tail)] + fem
            return [base] + plural(base)
    return []


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
# "esta", "esas" and "seria" used to be in here too. They were blocked because
# estar and ser would otherwise claim them - but irregular verbs are never
# rule-generated, so nothing spells them any more except themselves, and the
# demonstratives are among the commonest words on the page.
NEVER = set(u"""do da de del la le lo
los las les se su sus mi mis tu tus un una uno unos unas al a e o y ni que qui como
cuando donde para por sin con sobre tras nos os me te si no ya mas pero sea seas
sean ser ir voy vas van vamos fue fui era eras eran""".split())


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


def derived_irregular(verbs):
    """The imperfect subjunctive of every irregular verb, from its own preterite.

    Spanish builds it off the third-person plural of the preterite with no
    exceptions at all: supieron -> supiera, pudieron -> pudiera, dijeron ->
    dijera, hicieron -> hiciera, estuvieron -> estuviera. verbs.json does not
    carry the tense - the Verb Trainer does not teach it - but the course is
    full of it ("si supiera", "que me explicara", "como si fuera"), and every
    one of those was dead on the page.
    """
    out = {}
    for lemma, tenses in (verbs.get("irregular") or {}).items():
        past = tenses.get("past") or []
        if len(past) < 5 or not past[4]:
            continue
        third = past[4].strip().lower()
        if not third.endswith(u"ron"):
            continue
        base = third[:-3]
        for tail in (u"ra", u"ras", u"ran"):
            out.setdefault(base + tail, set()).add(lemma)
        # supieramos carries an accent: supi + e + ramos.
        nos = base[:-1] + MARK.get(base[-1], base[-1]) + u"ramos"
        out.setdefault(nos, set()).add(lemma)
    return out


def reflexive_twin(lemma, dictionary):
    """The other half of a quedar/quedarse pair, if the dictionary has one."""
    if lemma.endswith("se") and plain_infinitive(lemma) and lemma[:-2] in dictionary:
        return lemma[:-2]
    if not lemma.endswith("se") and lemma + "se" in dictionary:
        return lemma + "se"
    return None


# Which person an ending can belong to. A pronoun in front of a verb is only
# reflexive if it AGREES with it: "me quedo" is quedarse, but "me queda bien"
# is quedar with an indirect object, and so is every "me parece" and "me
# pareció" in the course. Without the agreement test the commonest verb in
# Spanish after ser gets filed under the wrong half of its own pair.
PERSON_ENDINGS = [
    (u"ábamos", "1p"), (u"íamos", "1p"), (u"amos", "1p"), (u"emos", "1p"), (u"imos", "1p"),
    (u"aron", "3p"), (u"ieron", "3p"), (u"aban", "3p"), (u"ían", "3p"),
    (u"aste", "2s"), (u"iste", "2s"), (u"abas", "2s"), (u"ías", "2s"),
    (u"ás", "2s"), (u"és", "2s"), (u"ís", "2s"), (u"as", "2s"), (u"es", "2s"),
    (u"aba", "1s3s"), (u"ía", "1s3s"),
    (u"an", "3p"), (u"en", "3p"),
    (u"ió", "3s"), (u"ó", "3s"), (u"é", "1s"), (u"í", "1s"),
    (u"o", "1s"), (u"a", "3s"), (u"e", "3s"),
]
PRONOUN_PERSON = {u"me": "1s", u"te": "2s", u"nos": "1p", u"se": "3s3p"}


def agrees(pronoun, form):
    """Could `pronoun` be the reflexive of `form`, or is it somebody else's?"""
    # A participle or a gerund says nothing about person, so anything goes.
    if form.endswith(u"ndo") or form.endswith(u"ado") or form.endswith(u"ido")        or form.endswith(u"ada") or form.endswith(u"ida")        or form.endswith(u"ados") or form.endswith(u"idos")        or form.endswith(u"adas") or form.endswith(u"idas"):
        return True
    who = PRONOUN_PERSON.get(pronoun)
    if not who:
        return False
    for tail, person in PERSON_ENDINGS:
        if form.endswith(tail):
            return any(p in person for p in (who[i:i + 2] for i in range(0, len(who), 2)))
    return True


def reflexive_context(token_lists, wanted):
    """For each form, how often it is written with a reflexive pronoun in front.

    This is what settles quedar vs quedarse. Both spell "queda", so the map
    cannot have both - but the text knows: "se queda en la casa" is quedarse
    and "queda lejos" is quedar, and one of those is most of the times the
    course writes the word. Counting them is a better answer than picking the
    commoner lemma, and a far better one than dropping the word.
    """
    out = {}
    for tl in token_lists:
        for i, t in enumerate(tl):
            if t not in wanted:
                continue
            box = out.setdefault(t, [0, 0])
            near = [x for x in tl[max(0, i - 2):i] if x in REFLEXIVE_CLITICS]
            box[0 if any(agrees(x, t) for x in near) else 1] += 1
    return out


def build(dictionary, texts, verbs=None):
    """form -> lemma, for forms that occur in `texts` and are not entries themselves."""
    token_lists = [tokens(t) for t in texts]
    used = set()
    for tl in token_lists:
        used.update(tl)

    verbs = verbs or {}
    tables = verbs.get("irregular") or {}
    irregular = set(tables)

    # Three tiers: what verbs.json states, what the rules produce, and the
    # gerund/participle guesses that lose every argument. See the module note.
    stated, ruled, weak = {}, {}, {}

    def claim(bucket, form, lemma):
        if form in dictionary or form not in used or form == lemma:
            return
        if bucket is not stated and (form in NEVER or strip_accent(form) in NEVER):
            return
        bucket.setdefault(form, set()).add(lemma)

    for f, lemmas in irregular_forms(verbs).items():
        for l in lemmas:
            claim(stated, f, l)
    for f, lemmas in derived_irregular(verbs).items():
        for l in lemmas:
            claim(stated, f, l)
    for lemma, extra in EXTRA_FORMS.items():
        if lemma in dictionary:
            for f in extra:
                claim(stated, f, lemma)

    for lemma, entry in dictionary.items():
        pos = (entry.get("pos") or "").split("/")[0]
        if " " in lemma:            # multi-word phrases do not inflect here
            continue
        if pos == "v":
            table = tables.get(lemma)
            hand_written = lemma in EXTRA_FORMS
            if table or lemma in irregular:
                for f in nonfinite_forms(lemma):
                    claim(weak, f, lemma)
                for f in spelling_classes(lemma) + spelling_changes(lemma):
                    claim(weak, f, lemma)
            else:
                variants = stem_changed(plain_infinitive(lemma) or lemma)
                soft = set(tu_forms(lemma)) | set(participle_forms(lemma))
                for variant in variants:
                    soft.update(tu_forms(variant))
                    soft.update(participle_forms(variant))
                for source in [lemma] + variants:
                    for f in verb_forms(source):
                        claim(weak if (hand_written or f in soft) else ruled, f, lemma)
                for f in spelling_classes(lemma) + spelling_changes(lemma):
                    claim(ruled, f, lemma)
                for f in hiatus_forms(lemma):
                    claim(weak, f, lemma)
            # A hand-written gerund or participle is a fact like verbs.json is,
            # so it outranks anything a rule spelled the same way: "viendo" is
            # ver, not vender's speculative e->ie stem change.
            for f in IRREGULAR_NONFINITE.get(lemma, []):
                claim(weak if inflection_of_an_entry(f, dictionary) else stated,
                      f, lemma)

            # Pronouns glued on the end. A verb whose ±se twin is also an entry
            # splits them: "callarlo" can only be callar and "callarme" can
            # only be callarse, so those two never collide.
            twin = reflexive_twin(lemma, dictionary)
            reflexive = lemma.endswith("se") and plain_infinitive(lemma)
            if reflexive and twin:
                mine = list(REFLEXIVE_CLITICS)
            elif twin:
                mine = OBJECT_CLITICS + CLITIC_PAIRS
            else:
                mine = OBJECT_CLITICS + REFLEXIVE_CLITICS + CLITIC_PAIRS
            if reflexive and not twin:
                # soltarse is the only entry, but the course also writes plain
                # "soltar" and "soltarlo". Both are the same verb and there is
                # nothing else they could be.
                claim(ruled, plain_infinitive(lemma), lemma)
            sure, risky = verb_bases(lemma, tables.get(lemma))
            for base in sure:
                for f in clitic_forms(base, mine):
                    claim(ruled, f, lemma)
            for base in risky:
                for f in clitic_forms(base, mine):
                    claim(weak, f, lemma)
            continue
        if pos == "n":
            gen = noun_forms(lemma)
            # Half the nouns in Spanish are adjectives too, and the ones that
            # name a person always have a feminine: maestro/maestra,
            # companero/companera, vendedor/vendedora, peleon/peleona. Claimed
            # weakly, because a real entry must always outrank a guess.
            for f in adj_forms(lemma) + feminine(lemma):
                claim(weak, f, lemma)
        elif pos == "adj":
            gen = adj_forms(lemma) + feminine(lemma)
        # Anything ending in -o agrees like an adjective whatever it is tagged.
        # "todo" is filed as a pronoun and "mucho" as an adverb, so toda,
        # todas, muchos and mucha resolved to nothing - and those are among the
        # commonest words in the language.
        elif lemma.endswith("o"): gen = adj_forms(lemma)
        else: gen = []
        if pos in ("adj", "adv"):
            gen = list(gen) + adverb_forms(lemma)
        for f in gen:
            claim(ruled, f, lemma)

    # Count how often each lemma is itself written out, to settle collisions.
    counts = {}
    for tl in token_lists:
        for w in tl:
            if w in dictionary:
                counts[w] = counts.get(w, 0) + 1

    candidates = {}
    for f in set(stated) | set(ruled) | set(weak):
        candidates[f] = stated.get(f) or ruled.get(f) or weak.get(f)

    pairs = dict((f, s) for f, s in candidates.items() if len(s) > 1)
    context = reflexive_context(token_lists, set(pairs))

    def resolve_pair(f, lemmas):
        """quedar or quedarse, decided by the text rather than by a coin."""
        bases = set()
        for l in lemmas:
            bases.add(l[:-2] if (l.endswith("se") and l[:-2] in dictionary) else l)
        if len(bases) != 1:
            return None
        plain = bases.pop()
        refl = plain + "se"
        if plain not in dictionary or refl not in dictionary:
            return None
        with_pronoun, without = context.get(f, (0, 0))
        if with_pronoun != without:
            return refl if with_pronoun > without else plain
        # Nothing to go on in this form's own sentences: fall back to which
        # half of the pair the course writes out more often as an infinitive.
        if counts.get(refl, 0) != counts.get(plain, 0):
            return refl if counts.get(refl, 0) > counts.get(plain, 0) else plain
        return plain

    # A form two lemmas can both produce is dropped, not guessed at. "decido"
    # is decidir far more often than decir, and picking the commoner lemma got
    # it wrong; a word that shows nothing is recoverable, a word that shows the
    # wrong meaning is not. The one exception is a plain/reflexive pair, where
    # both answers name the same verb and the text says which one it is.
    forms, ambiguous = {}, []
    for f, lemmas in candidates.items():
        if len(lemmas) == 1:
            forms[f] = next(iter(lemmas))
            continue
        pick = resolve_pair(f, lemmas)
        if pick:
            forms[f] = pick
        else:
            ambiguous.append((f, sorted(lemmas)))
    return forms, ambiguous, used
