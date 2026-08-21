# -*- coding: utf-8 -*-
"""Rebuild content/verbs.json.

Three things this has to get right, and one it has to not break.

RIGHT
  1. Six tenses instead of three. imperfect, conditional and present
     subjunctive join present, past and future.
  2. Every verb in `drill` that is irregular in ANY of those six has to be in
     `irregular` with ALL six. engine.js conjugate() falls back to the regular
     table when a tense is missing, so a half-filled irregular silently
     produces a wrong form. That is not hypothetical: cerrar and perder are in
     drill today and in neither table, so the Verb Trainer has been teaching
     "cerro" and "perdo".
  3. Voseo throughout. vos does NOT diphthongise: vos podés, vos pensás, vos
     querés. The subjunctive is the voseo one: que vos hablés, comás, vivás.

NOT BREAK
  The voseo imperative is one form, and startVerbs() picks a random subject
  index 0-4 for whatever tense it draws. A one-slot tense would hand the drill
  an undefined. So `imperative` is stored per verb but is NOT listed in
  `tenses`: forms.py reads every tense of every irregular verb when it builds
  the inflection map, so the imperatives become tappable, and the drill never
  sees them. Drilling them needs a change in the app repo, noted in NEXT.md.

Everything generated here is checked against the 21 irregulars that were
already in the file. If a single one of their present/past/future forms comes
out different, the build refuses to write.
"""
import io, json, os, re, sys, collections
sys.path.insert(0, ".github/scripts")
import forms as M

SUBJ = 5  # yo, vos, él/ella, nosotros, ellos

# ---------------------------------------------------------------- rule tables
STEM = {
 u"pensar": (u"e", u"ie"), u"empezar": (u"e", u"ie"), u"cerrar": (u"e", u"ie"),
 u"perder": (u"e", u"ie"), u"entender": (u"e", u"ie"), u"querer": (u"e", u"ie"),
 u"sentir": (u"e", u"ie"), u"preferir": (u"e", u"ie"), u"despertar": (u"e", u"ie"),
 u"sentar": (u"e", u"ie"), u"comenzar": (u"e", u"ie"), u"defender": (u"e", u"ie"),
 u"encender": (u"e", u"ie"), u"negar": (u"e", u"ie"), u"regar": (u"e", u"ie"),
 u"encontrar": (u"o", u"ue"), u"poder": (u"o", u"ue"), u"dormir": (u"o", u"ue"),
 u"volver": (u"o", u"ue"), u"contar": (u"o", u"ue"), u"costar": (u"o", u"ue"),
 u"recordar": (u"o", u"ue"), u"mostrar": (u"o", u"ue"), u"llover": (u"o", u"ue"),
 u"soñar": (u"o", u"ue"), u"sonar": (u"o", u"ue"), u"probar": (u"o", u"ue"),
 u"acostar": (u"o", u"ue"), u"morir": (u"o", u"ue"), u"doler": (u"o", u"ue"),
 u"colgar": (u"o", u"ue"), u"resolver": (u"o", u"ue"), u"envolver": (u"o", u"ue"),
 u"devolver": (u"o", u"ue"), u"mover": (u"o", u"ue"), u"soler": (u"o", u"ue"),
 u"jugar": (u"u", u"ue"), u"torcer": (u"o", u"ue"), u"cocer": (u"o", u"ue"),
 u"pedir": (u"e", u"i"), u"seguir": (u"e", u"i"), u"repetir": (u"e", u"i"),
 u"servir": (u"e", u"i"), u"medir": (u"e", u"i"), u"vestir": (u"e", u"i"),
 u"conseguir": (u"e", u"i"), u"corregir": (u"e", u"i"), u"despedir": (u"e", u"i"),
 u"decir": (u"e", u"i"), u"tener": (u"e", u"ie"), u"venir": (u"e", u"ie"),
 u"elegir": (u"e", u"i"), u"impedir": (u"e", u"i"),
}
# -ir stem-changers also change in nosotros of the subjunctive, and in the
# third persons of the preterite: durmió, pidió, sintió.
IR_BOOT = {u"e": u"i", u"o": u"u"}

YO = {
 u"tener": u"tengo", u"poner": u"pongo", u"salir": u"salgo", u"venir": u"vengo",
 u"hacer": u"hago", u"decir": u"digo", u"ver": u"veo", u"dar": u"doy",
 u"saber": u"sé", u"caer": u"caigo", u"traer": u"traigo", u"oír": u"oigo",
 u"conocer": u"conozco", u"parecer": u"parezco", u"agradecer": u"agradezco",
 u"ofrecer": u"ofrezco", u"aparecer": u"aparezco", u"crecer": u"crezco",
 u"nacer": u"nazco", u"merecer": u"merezco", u"conducir": u"conduzco",
 u"traducir": u"traduzco", u"seguir": u"sigo", u"conseguir": u"consigo",
 u"corregir": u"corrijo", u"elegir": u"elijo", u"coger": u"cojo",
 u"escoger": u"escojo", u"recoger": u"recojo", u"dirigir": u"dirijo",
 u"vencer": u"venzo", u"convencer": u"convenzo", u"torcer": u"tuerzo",
 u"cocer": u"cuezo",
}
PRET = {  # strong preterite stems
 u"tener": u"tuv", u"estar": u"estuv", u"poder": u"pud", u"poner": u"pus",
 u"saber": u"sup", u"querer": u"quis", u"venir": u"vin", u"andar": u"anduv",
 u"caber": u"cup", u"haber": u"hub", u"hacer": u"hic", u"decir": u"dij",
 u"traer": u"traj", u"conducir": u"conduj", u"traducir": u"traduj",
}
FUT = {  # short future/conditional stems
 u"tener": u"tendr", u"poner": u"pondr", u"salir": u"saldr", u"venir": u"vendr",
 u"poder": u"podr", u"saber": u"sabr", u"hacer": u"har", u"decir": u"dir",
 u"querer": u"querr", u"haber": u"habr", u"caber": u"cabr", u"valer": u"valdr",
}
# Wholly irregular. Anything named here is used verbatim.
HARD = {
 u"ser": {"present": [u"soy", u"sos", u"es", u"somos", u"son"],
          "past": [u"fui", u"fuiste", u"fue", u"fuimos", u"fueron"],
          "imperfect": [u"era", u"eras", u"era", u"éramos", u"eran"],
          "future": [u"seré", u"serás", u"será", u"seremos", u"serán"],
          "conditional": [u"sería", u"serías", u"sería", u"seríamos", u"serían"],
          "subjunctive": [u"sea", u"seás", u"sea", u"seamos", u"sean"],
          "imperative": [u"sé"]},
 u"ir": {"present": [u"voy", u"vas", u"va", u"vamos", u"van"],
         "past": [u"fui", u"fuiste", u"fue", u"fuimos", u"fueron"],
         "imperfect": [u"iba", u"ibas", u"iba", u"íbamos", u"iban"],
         "future": [u"iré", u"irás", u"irá", u"iremos", u"irán"],
         "conditional": [u"iría", u"irías", u"iría", u"iríamos", u"irían"],
         "subjunctive": [u"vaya", u"vayás", u"vaya", u"vayamos", u"vayan"],
         "imperative": [u"andá"]},
 u"ver": {"present": [u"veo", u"ves", u"ve", u"vemos", u"ven"],
          "past": [u"vi", u"viste", u"vio", u"vimos", u"vieron"],
          "imperfect": [u"veía", u"veías", u"veía", u"veíamos", u"veían"],
          "future": [u"veré", u"verás", u"verá", u"veremos", u"verán"],
          "conditional": [u"vería", u"verías", u"vería", u"veríamos", u"verían"],
          "subjunctive": [u"vea", u"veás", u"vea", u"veamos", u"vean"],
          "imperative": [u"ve"]},
 u"estar": {"present": [u"estoy", u"estás", u"está", u"estamos", u"están"],
            "past": [u"estuve", u"estuviste", u"estuvo", u"estuvimos", u"estuvieron"],
            "imperfect": [u"estaba", u"estabas", u"estaba", u"estábamos", u"estaban"],
            "future": [u"estaré", u"estarás", u"estará", u"estaremos", u"estarán"],
            "conditional": [u"estaría", u"estarías", u"estaría", u"estaríamos", u"estarían"],
            "subjunctive": [u"esté", u"estés", u"esté", u"estemos", u"estén"],
            "imperative": [u"está"]},
 u"dar": {"present": [u"doy", u"das", u"da", u"damos", u"dan"],
          "past": [u"di", u"diste", u"dio", u"dimos", u"dieron"],
          "imperfect": [u"daba", u"dabas", u"daba", u"dábamos", u"daban"],
          "future": [u"daré", u"darás", u"dará", u"daremos", u"darán"],
          "conditional": [u"daría", u"darías", u"daría", u"daríamos", u"darían"],
          "subjunctive": [u"dé", u"dés", u"dé", u"demos", u"den"],
          "imperative": [u"da"]},
 u"saber": {"present": [u"sé", u"sabés", u"sabe", u"sabemos", u"saben"],
            "past": [u"supe", u"supiste", u"supo", u"supimos", u"supieron"],
            "imperfect": [u"sabía", u"sabías", u"sabía", u"sabíamos", u"sabían"],
            "future": [u"sabré", u"sabrás", u"sabrá", u"sabremos", u"sabrán"],
            "conditional": [u"sabría", u"sabrías", u"sabría", u"sabríamos", u"sabrían"],
            "subjunctive": [u"sepa", u"sepás", u"sepa", u"sepamos", u"sepan"],
            "imperative": [u"sabé"]},
 u"haber": {"present": [u"he", u"has", u"ha", u"hemos", u"han"],
            "past": [u"hube", u"hubiste", u"hubo", u"hubimos", u"hubieron"],
            "imperfect": [u"había", u"habías", u"había", u"habíamos", u"habían"],
            "future": [u"habré", u"habrás", u"habrá", u"habremos", u"habrán"],
            "conditional": [u"habría", u"habrías", u"habría", u"habríamos", u"habrían"],
            "subjunctive": [u"haya", u"hayás", u"haya", u"hayamos", u"hayan"],
            "imperative": [u"habé"]},
}

REG = {
 u"ar": {"present": [u"o", u"ás", u"a", u"amos", u"an"],
         "past": [u"é", u"aste", u"ó", u"amos", u"aron"],
         "imperfect": [u"aba", u"abas", u"aba", u"ábamos", u"aban"],
         "future": [u"aré", u"arás", u"ará", u"aremos", u"arán"],
         "conditional": [u"aría", u"arías", u"aría", u"aríamos", u"arían"],
         "subjunctive": [u"e", u"és", u"e", u"emos", u"en"]},
 u"er": {"present": [u"o", u"és", u"e", u"emos", u"en"],
         "past": [u"í", u"iste", u"ió", u"imos", u"ieron"],
         "imperfect": [u"ía", u"ías", u"ía", u"íamos", u"ían"],
         "future": [u"eré", u"erás", u"erá", u"eremos", u"erán"],
         "conditional": [u"ería", u"erías", u"ería", u"eríamos", u"erían"],
         "subjunctive": [u"a", u"ás", u"a", u"amos", u"an"]},
 u"ir": {"present": [u"o", u"ís", u"e", u"imos", u"en"],
         "past": [u"í", u"iste", u"ió", u"imos", u"ieron"],
         "imperfect": [u"ía", u"ías", u"ía", u"íamos", u"ían"],
         "future": [u"iré", u"irás", u"irá", u"iremos", u"irán"],
         "conditional": [u"iría", u"irías", u"iría", u"iríamos", u"irían"],
         "subjunctive": [u"a", u"ás", u"a", u"amos", u"an"]},
}
IMPER = {u"ar": u"á", u"er": u"é", u"ir": u"í"}


def kind_of(inf):
    return inf[-2:] if inf[-2:] in REG else None


def change(stem, pair):
    old, new = pair
    at = stem.rfind(old)
    return stem if at < 0 else stem[:at] + new + stem[at + 1:]


def spell_ar(stem, verb):
    """-car/-gar/-zar shift before an e: busqué, llegué, empecé."""
    if verb.endswith(u"car"):
        return stem[:-1] + u"qu"
    if verb.endswith(u"gar"):
        return stem + u"u"
    if verb.endswith(u"zar"):
        return stem[:-1] + u"c"
    return stem


def build(verb):
    k = kind_of(verb)
    if k is None:
        return None
    if verb in HARD:
        return dict(HARD[verb])
    stem = verb[:-2]
    t = {}

    # ---- present
    yo = YO.get(verb)
    if verb in STEM:
        s2 = change(stem, STEM[verb])
        pres = [(yo or s2 + REG[k]["present"][0]),
                stem + REG[k]["present"][1],          # vos never diphthongises
                s2 + REG[k]["present"][2],
                stem + REG[k]["present"][3],
                s2 + REG[k]["present"][4]]
    else:
        pres = [(yo or stem + REG[k]["present"][0])] + \
               [stem + e for e in REG[k]["present"][1:]]
    t["present"] = pres

    # ---- preterite
    if verb in PRET:
        p = PRET[verb]
        third = u"hizo" if verb == u"hacer" else p + u"o"
        sixth = (p + u"eron") if p.endswith(u"j") else (p + u"ieron")
        t["past"] = [p + u"e", p + u"iste", third, p + u"imos", sixth]
    else:
        past = [stem + e for e in REG[k]["past"]]
        if k == u"ar":
            past[0] = spell_ar(stem, verb) + REG[k]["past"][0]
        elif stem and stem[-1] in u"aeo":
            # leer, creer, caer: the ending's i turns to y between vowels, and
            # the others take a written accent. Regular endings give "leio"
            # and "leiste", which are not words.
            past = [stem + u"í", stem + u"íste", stem + u"yó",
                    stem + u"ímos", stem + u"yeron"]
        if k == u"ir" and verb in STEM:
            b = change(stem, (STEM[verb][0], IR_BOOT[STEM[verb][0]]))
            past[2] = b + REG[k]["past"][2]
            past[4] = b + REG[k]["past"][4]
        t["past"] = past

    # ---- imperfect: regular for everything except ser, ir, ver
    t["imperfect"] = [stem + e for e in REG[k]["imperfect"]]

    # ---- future and conditional
    if verb in FUT:
        fs = FUT[verb]
        t["future"] = [fs + e for e in (u"é", u"ás", u"á", u"emos", u"án")]
        t["conditional"] = [fs + e for e in (u"ía", u"ías", u"ía", u"íamos", u"ían")]
    else:
        t["future"] = [verb + e for e in (u"é", u"ás", u"á", u"emos", u"án")]
        t["conditional"] = [verb + e for e in (u"ía", u"ías", u"ía", u"íamos", u"ían")]

    # ---- present subjunctive, off the yo form, voseo in slot 1
    base = t["present"][0]
    sub_stem = base[:-1] if base.endswith(u"o") else None
    if sub_stem is None:
        sub_stem = spell_ar(stem, verb) if k == u"ar" else stem
        if verb in STEM:
            sub_stem = change(sub_stem, STEM[verb])
    elif k == u"ar":
        sub_stem = spell_ar(sub_stem, verb)
    # A verb with an irregular yo carries that stem through the WHOLE
    # subjunctive: tenga, tengás, tengamos. A plain stem-changer does not -
    # vos and nosotros keep the undiphthongised stem (pensés, pensemos), and
    # an -ir stem-changer puts the boot change there instead (durmamos,
    # pidamos).
    if verb in YO:
        plain = sub_stem
    else:
        plain = spell_ar(stem, verb) if k == u"ar" else stem
        if verb in STEM and k == u"ir":
            plain = change(plain, (STEM[verb][0], IR_BOOT[STEM[verb][0]]))
    e = REG[k]["subjunctive"]
    t["subjunctive"] = [sub_stem + e[0], plain + e[1], sub_stem + e[2],
                        plain + e[3], sub_stem + e[4]]

    # ---- voseo imperative
    t["imperative"] = [stem + IMPER[k]]
    return t


def main():
    old = json.load(io.open("content/verbs.json", encoding="utf-8"))

    # 1. does the generator reproduce every irregular already in the file?
    bad = []
    for verb, tbl in sorted(old["irregular"].items()):
        made = build(verb)
        for tense in ("present", "past", "future"):
            if made[tense] != tbl[tense]:
                bad.append(u"%s %s: had %s, generated %s"
                           % (verb, tense, u" ".join(tbl[tense]), u" ".join(made[tense])))
    if bad:
        io.open("../verbdiff.txt", "w", encoding="utf-8").write(u"\n".join(bad))
        print("REFUSING TO WRITE - %d mismatches against the existing table" % len(bad))
        print("see ../verbdiff.txt")
        return 1

    # 2. the drill list: the verbs the course actually uses, most-used first
    d = {}
    for p in ["content/dictionary/core.json", "content/dictionary/spine.json"]:
        d.update(json.load(io.open(p, encoding="utf-8")))
    corpus = []
    for n in sorted(os.listdir("content/lessons")):
        if re.match(r"^p[0-7]-\d\d[.]json$", n):
            b = json.load(io.open("content/lessons/" + n, encoding="utf-8"))
            corpus += [s["s"] for s in b["sn"]]
    f, _, _ = M.build(d, corpus, old)
    cnt = collections.Counter()
    for line in corpus:
        for w in M.tokens(line):
            lem = w if w in d else f.get(w)
            if lem and (d.get(lem, {}).get("pos") or "").split("/")[0] == "v":
                cnt[lem] += 1
    drill = []
    for w, _n in cnt.most_common():
        # engine.js conjugate() does verb.slice(0, -2), so a reflexive
        # infinitive would come out as "enojarso". Those are left out until the
        # app knows how to strip the pronoun.
        if w.endswith(u"se") or kind_of(w) is None:
            continue
        if w not in drill:
            drill.append(w)
        if len(drill) >= 120:
            break
    for must in old["drill"]:
        if must not in drill and kind_of(must):
            drill.append(must)

    # 3. everything that needs an irregular entry gets a complete one
    irregular = {}
    for verb in drill:
        needs = (verb in HARD or verb in STEM or verb in YO or verb in PRET
                 or verb in FUT
                 or (kind_of(verb) == u"ar"
                     and verb.endswith((u"car", u"gar", u"zar")))
                 or (kind_of(verb) in (u"er", u"ir") and verb[:-2]
                     and verb[:-2][-1] in u"aeo"))
        if needs:
            irregular[verb] = build(verb)
    for verb in old["irregular"]:
        if verb not in irregular:
            irregular[verb] = build(verb)

    out = {
        "subjects": old["subjects"],
        "tenses": ["present", "past", "imperfect", "future", "conditional",
                   "subjunctive"],
        "regular": REG,
        "irregular": {k: irregular[k] for k in sorted(irregular)},
        "drill": drill,
    }
    io.open("content/verbs.json", "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, indent=1) + u"\n")
    print("verbs.json: %d drill verbs, %d irregular, %d tenses"
          % (len(drill), len(irregular), len(out["tenses"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
