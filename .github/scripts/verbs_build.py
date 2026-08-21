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
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import forms as M

# Run from the repo root:  python .github/scripts/verbs_build.py

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

# The drill list, frozen. It was picked once from how often the course
# actually uses each verb, and it is written down rather than recomputed
# so that this script is a pure function of its own tables: running it
# twice gives the same file. Reflexives are absent on purpose - engine.js
# conjugate() does verb.slice(0, -2), so "enojarse" would come out
# "enojarso". Add one only when the app knows how to strip the pronoun.
DRILL = [
 u"decir", u"ser", u"estar", u"ir", u"hacer", u"tener",
 u"preguntar", u"saber", u"hablar", u"dar", u"querer", u"contar",
 u"poder", u"salir", u"poner", u"llevar", u"pedir", u"ver",
 u"pasar", u"venir", u"explicar", u"empezar", u"volver", u"esperar",
 u"aprender", u"contestar", u"pensar", u"medir", u"seguir", u"dejar",
 u"sonar", u"mirar", u"cambiar", u"llegar", u"servir", u"mandar",
 u"entrar", u"gritar", u"usar", u"faltar", u"enseñar", u"pagar",
 u"terminar", u"comprar", u"avisar", u"costar", u"sacar", u"entender",
 u"caminar", u"tomar", u"cerrar", u"tocar", u"dormir", u"conocer",
 u"trabajar", u"comer", u"escuchar", u"importar", u"saludar", u"discutir",
 u"subir", u"repetir", u"caer", u"significar", u"abrir", u"vender",
 u"perder", u"escribir", u"invitar", u"buscar", u"deber", u"lavar",
 u"bailar", u"depender", u"arreglar", u"parar", u"tratar", u"meter",
 u"llamar", u"corregir", u"llorar", u"leer", u"existir", u"aguantar",
 u"devolver", u"sorprender", u"quitar", u"olvidar", u"ayudar", u"vivir",
 u"jugar", u"creer", u"cocinar", u"nacer", u"reclamar", u"probar",
 u"presentar", u"mencionar", u"recitar", u"funcionar", u"estudiar", u"doler",
 u"guardar", u"alcanzar", u"insistir", u"aceptar", u"correr", u"escoger",
 u"cantar", u"recibir", u"cargar", u"apuntar", u"cobrar", u"prender",
 u"cuidar", u"cumplir", u"encontrar", u"armar", u"vacilar", u"pesar",
 u"sentir", u"necesitar", u"ganar",
]

# The 21 irregulars this file inherited, exactly as they were. The build
# refuses to write unless it reproduces every one of these. That check
# caught real errors in decir, tener and venir; do not remove it.
BASELINE = {
 u"dar": {"present": [u"doy", u"das", u"da", u"damos", u"dan"], "past": [u"di", u"diste", u"dio", u"dimos", u"dieron"], "future": [u"daré", u"darás", u"dará", u"daremos", u"darán"]},
 u"decir": {"present": [u"digo", u"decís", u"dice", u"decimos", u"dicen"], "past": [u"dije", u"dijiste", u"dijo", u"dijimos", u"dijeron"], "future": [u"diré", u"dirás", u"dirá", u"diremos", u"dirán"]},
 u"dormir": {"present": [u"duermo", u"dormís", u"duerme", u"dormimos", u"duermen"], "past": [u"dormí", u"dormiste", u"durmió", u"dormimos", u"durmieron"], "future": [u"dormiré", u"dormirás", u"dormirá", u"dormiremos", u"dormirán"]},
 u"empezar": {"present": [u"empiezo", u"empezás", u"empieza", u"empezamos", u"empiezan"], "past": [u"empecé", u"empezaste", u"empezó", u"empezamos", u"empezaron"], "future": [u"empezaré", u"empezarás", u"empezará", u"empezaremos", u"empezarán"]},
 u"encontrar": {"present": [u"encuentro", u"encontrás", u"encuentra", u"encontramos", u"encuentran"], "past": [u"encontré", u"encontraste", u"encontró", u"encontramos", u"encontraron"], "future": [u"encontraré", u"encontrarás", u"encontrará", u"encontraremos", u"encontrarán"]},
 u"estar": {"present": [u"estoy", u"estás", u"está", u"estamos", u"están"], "past": [u"estuve", u"estuviste", u"estuvo", u"estuvimos", u"estuvieron"], "future": [u"estaré", u"estarás", u"estará", u"estaremos", u"estarán"]},
 u"hacer": {"present": [u"hago", u"hacés", u"hace", u"hacemos", u"hacen"], "past": [u"hice", u"hiciste", u"hizo", u"hicimos", u"hicieron"], "future": [u"haré", u"harás", u"hará", u"haremos", u"harán"]},
 u"ir": {"present": [u"voy", u"vas", u"va", u"vamos", u"van"], "past": [u"fui", u"fuiste", u"fue", u"fuimos", u"fueron"], "future": [u"iré", u"irás", u"irá", u"iremos", u"irán"]},
 u"pedir": {"present": [u"pido", u"pedís", u"pide", u"pedimos", u"piden"], "past": [u"pedí", u"pediste", u"pidió", u"pedimos", u"pidieron"], "future": [u"pediré", u"pedirás", u"pedirá", u"pediremos", u"pedirán"]},
 u"pensar": {"present": [u"pienso", u"pensás", u"piensa", u"pensamos", u"piensan"], "past": [u"pensé", u"pensaste", u"pensó", u"pensamos", u"pensaron"], "future": [u"pensaré", u"pensarás", u"pensará", u"pensaremos", u"pensarán"]},
 u"poder": {"present": [u"puedo", u"podés", u"puede", u"podemos", u"pueden"], "past": [u"pude", u"pudiste", u"pudo", u"pudimos", u"pudieron"], "future": [u"podré", u"podrás", u"podrá", u"podremos", u"podrán"]},
 u"poner": {"present": [u"pongo", u"ponés", u"pone", u"ponemos", u"ponen"], "past": [u"puse", u"pusiste", u"puso", u"pusimos", u"pusieron"], "future": [u"pondré", u"pondrás", u"pondrá", u"pondremos", u"pondrán"]},
 u"querer": {"present": [u"quiero", u"querés", u"quiere", u"queremos", u"quieren"], "past": [u"quise", u"quisiste", u"quiso", u"quisimos", u"quisieron"], "future": [u"querré", u"querrás", u"querrá", u"querremos", u"querrán"]},
 u"saber": {"present": [u"sé", u"sabés", u"sabe", u"sabemos", u"saben"], "past": [u"supe", u"supiste", u"supo", u"supimos", u"supieron"], "future": [u"sabré", u"sabrás", u"sabrá", u"sabremos", u"sabrán"]},
 u"salir": {"present": [u"salgo", u"salís", u"sale", u"salimos", u"salen"], "past": [u"salí", u"saliste", u"salió", u"salimos", u"salieron"], "future": [u"saldré", u"saldrás", u"saldrá", u"saldremos", u"saldrán"]},
 u"seguir": {"present": [u"sigo", u"seguís", u"sigue", u"seguimos", u"siguen"], "past": [u"seguí", u"seguiste", u"siguió", u"seguimos", u"siguieron"], "future": [u"seguiré", u"seguirás", u"seguirá", u"seguiremos", u"seguirán"]},
 u"sentir": {"present": [u"siento", u"sentís", u"siente", u"sentimos", u"sienten"], "past": [u"sentí", u"sentiste", u"sintió", u"sentimos", u"sintieron"], "future": [u"sentiré", u"sentirás", u"sentirá", u"sentiremos", u"sentirán"]},
 u"ser": {"present": [u"soy", u"sos", u"es", u"somos", u"son"], "past": [u"fui", u"fuiste", u"fue", u"fuimos", u"fueron"], "future": [u"seré", u"serás", u"será", u"seremos", u"serán"]},
 u"tener": {"present": [u"tengo", u"tenés", u"tiene", u"tenemos", u"tienen"], "past": [u"tuve", u"tuviste", u"tuvo", u"tuvimos", u"tuvieron"], "future": [u"tendré", u"tendrás", u"tendrá", u"tendremos", u"tendrán"]},
 u"venir": {"present": [u"vengo", u"venís", u"viene", u"venimos", u"vienen"], "past": [u"vine", u"viniste", u"vino", u"vinimos", u"vinieron"], "future": [u"vendré", u"vendrás", u"vendrá", u"vendremos", u"vendrán"]},
 u"ver": {"present": [u"veo", u"ves", u"ve", u"vemos", u"ven"], "past": [u"vi", u"viste", u"vio", u"vimos", u"vieron"], "future": [u"veré", u"verás", u"verá", u"veremos", u"verán"]},
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
    # 1. does the generator still reproduce the table this file inherited?
    bad = []
    for verb, tbl in sorted(BASELINE.items()):
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

    # 2. the drill list is frozen data, not recomputed - see DRILL above
    drill = [w for w in DRILL if kind_of(w) and not w.endswith(u"se")]
    if len(drill) != len(DRILL):
        print("dropped %d unconjugatable entries from DRILL"
              % (len(DRILL) - len(drill)))

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
    for verb in BASELINE:
        if verb not in irregular:
            irregular[verb] = build(verb)

    out = {
        "subjects": [u"yo", u"vos", u"él/ella", u"nosotros", u"ellos"],
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
