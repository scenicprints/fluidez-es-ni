# -*- coding: utf-8 -*-
import io, json, os, sys, re
sys.path.insert(0,".github/scripts")
import forms as M, schedule as SCH
dictionary={}
for p in ["content/dictionary/core.json","content/dictionary/spine.json"]:
    dictionary.update(json.load(io.open(p,encoding="utf-8")))
verbs=json.load(io.open("content/verbs.json",encoding="utf-8"))
spine=[s["id"] for s in json.load(io.open("content/plan/spine.json",encoding="utf-8"))]
lessons={}
for n in sorted(os.listdir("content/lessons")):
    if re.match(r"^p[0-7]-\d\d\.json$", n):
        b=json.load(io.open("content/lessons/"+n,encoding="utf-8")); lessons[b["id"]]=b
corpus=[sn["s"] for b in lessons.values() for sn in b["sn"]]
forms,_,_=M.build(dictionary,corpus,verbs)
counts={sid:SCH.story_words(b,dictionary,forms) for sid,b in lessons.items()}
order=[s for s in spine if s in lessons]
BORING=set(u"su no ir venir poner ser estar haber tener hacer decir dar ver uno una todo "
           u"mucho poco mas muy ya tambien aqui alli este ese otro hay dos tres sin ella el la "
           u"que como cuando donde porque pero si mi tu nos les lo se".split())
claimed=set()
for i,sid in enumerate(order):
    b=lessons[sid]; c=counts[sid]
    later=order[i+1:i+1+SCH.RETURN_WINDOW]
    def returns(w):
        if len(later)<SCH.RETURN_WINDOW: return True
        return sum(1 for j in later if counts[j].get(w))>=SCH.RETURN_MIN
    ok=[w for w,n in c.items() if n>=SCH.DENSITY_MIN and SCH.is_content(w,dictionary)
        and w not in claimed and w in dictionary and w.lower() not in BORING and returns(w)]
    keep=[]
    for raw in b["wu"]:
        w=raw.lower()
        if " " in w: continue
        w=w if w in dictionary else forms.get(w,w)
        if w in ok and w not in keep: keep.append(w)
    rest=sorted((w for w in ok if w not in keep), key=lambda w:-c[w])
    b["wu"]=(keep+rest)[:12]; claimed.update(b["wu"])
    io.open("content/lessons/%s.json"%sid,"w",encoding="utf-8").write(
        json.dumps(b,ensure_ascii=False,indent=1)+u"\n")
