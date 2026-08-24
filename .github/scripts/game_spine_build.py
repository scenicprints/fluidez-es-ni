# -*- coding: utf-8 -*-
"""Writes content/plan/game-spine.json — the whole game, planned before any of
it is written, the way plan/spine.json planned the 185 stories."""
import io, json, os, sys

ROOT = sys.argv[1]

# act, place, who, title, goal, teaches (the chunks this mission introduces)
M = [
# ── ACT 1 · LLEGADA — Granada, and you can say nothing ───────────────────
(1,'hostal','El muchacho del hostal','El hostal','Get yourself a room',
 ['Buenas','quiero','un cuarto','tres','noches','está','bien','gracias']),
(1,'calzada','La muchacha del comedor','Desayuno en La Calzada','Order breakfast and pay',
 ['un gallo pinto','por favor','un café','cuánto','le debo']),
(1,'parque','El taxista','Taxi al mercado','Get there without paying the chele price',
 ['al mercado','ochenta','córdobas','cien']),
(1,'mercado','La verdulera','La fruta','Buy fruit for the week',
 ['una libra','de','mango','aguacate','¿a cómo?']),
(1,'mercado','El del cambio','Los reales','Change a hundred dollars',
 ['quiero cambiar','dólares','billetes','pequeños']),
(1,'calzada','Un chavalo','La tarjeta','Buy a phone chip and put credit on it',
 ['un chip','una recarga','de cien','mi teléfono']),
(1,'parque','Doña de los caites','¿Por dónde?','Ask the way to the cathedral',
 ['¿dónde queda?','la catedral','de aquí','arriba','abajo']),
(1,'farmacia','La farmacéutica','La farmacia','Explain what hurts and get something for it',
 ['me duele','la cabeza','el estómago','desde ayer']),
(1,'hostal','La señora del lavado','La ropa sucia','Get your washing done by Friday',
 ['lavar','esta ropa','para el viernes','¿cuánto sale?']),
(1,'lago','El lanchero','Las isletas','Haggle a boat out to the isletas and back',
 ['una vuelta','por las isletas','una hora','ida y vuelta']),
(1,'calzada','El mesero que habla inglés','En español, por favor','Get served in Spanish by somebody who would rather practise English',
 ['en español','estoy aprendiendo','ayúdeme','de nuevo']),
(1,'parque','Don de la banca','El calor','Small talk on a bench about the heat and nothing else',
 ['qué calor','todos los días','así es','ni modo']),

# ── ACT 2 · QUEDARSE — Granada, becoming a regular ───────────────────────
(2,'barrio','Doña Marta','El cuarto de alquiler','Rent a room by the month instead of the night',
 ['por mes','el alquiler','el agua','incluido','¿desde cuándo?']),
(2,'pulperia','Doña Chepa','La pulpería','Become somebody the shop knows by name',
 ['fiado','me apunta','mañana le pago','ideay']),
(2,'barrio','El barbero','La barbería','Get a haircut you actually asked for',
 ['más corto','a los lados','así está bien','déjelo así']),
(2,'barrio','Roberto','El chavalo de al lado','Let the neighbour’s kid teach you the words nobody prints',
 ['chunche','chele','vaya pues','dale']),
(2,'cancha','Los de la cancha','La mejenga','Get picked for a game on the corner pitch',
 ['¿puedo jugar?','de este lado','pásamela','buena esa']),
(2,'barrio','Doña Marta','El agua','Complain that the water has been off for three days',
 ['no hay agua','desde el martes','¿cuándo viene?','avíseme']),
(2,'pulperia','Doña Chepa','El chisme','Hear gossip and pass it on without getting it wrong',
 ['dicen que','fíjese que','no sea así','¿de verdad?']),
(2,'barrio','La vecina','El cumpleaños','Get invited to a birthday and turn up right',
 ['cumple años','¿a qué hora?','llevo algo','felicidades']),
(2,'terminal','El cobrador','El bus a Masaya','Take the bus without ending up in Managua',
 ['¿va para Masaya?','me deja en','la parada','ya voy bajando']),
(2,'masaya','La artesana','El mercado de Masaya','Buy a hammock and get the price down',
 ['una hamaca','está muy caro','¿me lo deja en?','me la llevo']),
(2,'barrio','Don Emilio','El taller','Ask for work and be told what you are actually worth',
 ['busco trabajo','sé un poco','aprendo rápido','pruébeme']),
(2,'barrio','Marcos','El compañero','Make your first real friend at work',
 ['¿qué pasó?','todo bien','vamos','nos vemos']),

# ── ACT 3 · MANAGUA — the barrio, where the course lives ─────────────────
(3,'managua','Marcos','La mudanza','Move to Managua and admit you are lost',
 ['me mudé','no conozco','ando perdido','enséñeme']),
(3,'fritanga','Doña Carmen','La fritanga','Order at the fritanga like somebody who eats there',
 ['un enchilado','con ensalada','para llevar','ya va']),
(3,'managua','Don Beto','El vecino viejo','Sit with an old man and let him talk about 1979',
 ['antes','en aquel tiempo','mi hermano','se lo llevaron']),
(3,'managua','Doña Chepa','Las direcciones','Give somebody your address the Nicaraguan way',
 ['de donde fue','dos cuadras','al lago','casa portón negro']),
(3,'taller','Don Emilio','La jerarquía','Learn who you may and may not contradict at work',
 ['con permiso','usted dirá','como usted diga','no me toca']),
(3,'managua','Marcos','La quincena','Survive the week before payday',
 ['no ando','hasta la quincena','me presta','se lo devuelvo']),
(3,'managua','Delroy','El costeño','Meet somebody from Bluefields whose Spanish is not yours',
 ['de la costa','no le entendí','más despacio','¿cómo dijo?']),
(3,'iglesia','Doña Carmen','La Purísima','Sing at a door on the 7th of December and get sweets for it',
 ['¿quién causa tanta alegría?','la concepción','gorra','vivan las gorras']),
(3,'managua','El vecino','El velorio','Say the right thing at a wake, which is almost nothing',
 ['lo siento mucho','mi pésame','era buena gente','aquí estamos']),
(3,'managua','Doña Chepa','La indirecta','Understand that you are being told off without being told off',
 ['no es por nada','algunos','yo no digo nombres','entienda']),
(3,'managua','Roberto','El que se fue','Hear that the kid next door left for Costa Rica',
 ['se fue','a buscar','manda','vuelve en diciembre']),
(3,'taller','Wilmer','El del norte','Talk to a man from a Jinotega coffee farm about home',
 ['del norte','el corte','frío','allá arriba']),
(3,'managua','Marcos','El compadre','Be asked to be godfather and understand what it costs',
 ['compadre','el bautizo','con mucho gusto','es un honor']),
(3,'managua','Don Beto','La despedida','Say goodbye to a man who is not going to be there next year',
 ['cuídese','que Dios lo guarde','vengo pronto','no diga eso']),

# ── ACT 4 · LA FAMILIA — holding your own ────────────────────────────────
(4,'managua','Lucía','La primera vez','Say something to her that is not about the weather',
 ['te ves bien','¿te puedo?','otro día','cuando quiera']),
(4,'managua','Lucía','El paseo','Ask her out without it sounding like a transaction',
 ['salgamos','el domingo','yo paso','me avisas']),
(4,'suegra','Doña Elena','La suegra','Meet her mother and get out alive',
 ['mucho gusto','señora','permiso','gracias por todo']),
(4,'suegra','Julio y Chino','Los cuñados','Survive being tested by two brothers-in-law',
 ['ideay','no me diga','vos sabés','ya me cayó']),
(4,'suegra','Doña Elena','La cocina','Be taught a recipe and be judged on how you listen',
 ['¿cuánto le echo?','a ojo','así','ya casi']),
(4,'managua','Lucía','El pleito','Have an argument in Spanish and not lose it by accident',
 ['no es eso','me estás','dejame explicar','ya no importa']),
(4,'managua','Lucía','La disculpa','Apologise properly, which is not the same as saying sorry',
 ['me pasé','tenías razón','no vuelve a pasar','perdoname']),
(4,'suegra','Doña Elena','El permiso','Ask her mother for something that matters',
 ['quería hablarle','con respeto','le pido','lo que usted diga']),
(4,'iglesia','Todos','La boda','Get through your own wedding in a language you married into',
 ['sí','acepto','para siempre','gracias a todos']),
(4,'managua','Lucía','El chavalo','Find out you are going to be a father',
 ['estoy','vamos a tener','¿de verdad?','no lo puedo creer']),
(4,'managua','Tom','El nuevo','Give a lost Canadian the notebook somebody once gave you',
 ['ando perdido','yo también estuve','tomá','vas a aprender']),
]

PLACES = {
 'hostal':'Hostal, Calle La Libertad','calzada':'Calle La Calzada','parque':'Parque Central',
 'mercado':'Mercado de Granada','farmacia':'La farmacia','lago':'The dock on Cocibolca',
 'barrio':'Your street in Granada','pulperia':'The pulpería on the corner',
 'cancha':'The corner pitch','terminal':'The bus terminal','masaya':'Masaya',
 'managua':'The barrio, Managua','fritanga':'Doña Carmen’s fritanga','taller':'The workshop',
 'iglesia':'The church','suegra':'Doña Elena’s house',
}
ACTS = {
 1:('Llegada','Granada, and you can say nothing'),
 2:('Quedarse','Granada, becoming a regular'),
 3:('Managua','The barrio, where the course lives'),
 4:('La familia','Holding your own'),
}

# The phrases a person says every day, and which therefore have to COME BACK.
# The help ladder is driven by how many times you have met a phrase, so a chunk
# taught once and never seen again leaves the player on rung one forever. This
# is the same problem the course's RETURN rule exists to catch.
#
# Everything else is exempt on purpose, exactly like the course's one-scene
# words: 'aserrin' and 'gigantona' cannot honestly recur, and neither can
# '¿quién causa tanta alegría?'. They are taught properly once and that is the
# honest answer.
CORE = ['Buenas','por favor','gracias','está','bien','quiero','cuánto','vaya pues',
        'ideay','ni modo','así es','me deja en','con permiso','fíjese que','dale',
        'cuídese','más despacio','ya va','todo bien','vamos','nos vemos','así']

spine, per = [], {}
for n, (act, place, who, title, goal, teaches) in enumerate(M):
    per[act] = per.get(act, 0) + 1
    # Bring back core phrases already taught, three missions apart, so every one
    # of them reaches rung three — noise, no English — before the game ends.
    earlier = [c for m in spine for c in m['teaches'] + m['reuses'] if c in CORE]
    pool = [c for c in CORE if c in earlier]
    reuses = [pool[(n * 3 + i) % len(pool)] for i in range(3)] if pool else []
    reuses = sorted(set(reuses) - set(teaches))
    spine.append({
        'id': 'g%d-%02d' % (act, per[act]),
        'act': act, 'place': place, 'who': who,
        'title': title, 'goal': goal,
        'teaches': teaches, 'reuses': reuses,
    })

out = os.path.join(ROOT, 'content', 'plan', 'game-spine.json')
with io.open(out, 'w', encoding='utf-8') as f:
    f.write(json.dumps({'acts': {str(k): {'name': v[0], 'desc': v[1]} for k, v in ACTS.items()},
                        'places': PLACES, 'missions': spine},
                       ensure_ascii=False, indent=1) + u'\n')
print('missions:', len(spine), ' by act:', {k: per[k] for k in sorted(per)})
met = {}
for m in spine:
    for c in m['teaches'] + m['reuses']:
        met[c] = met.get(c, 0) + 1
cold = sorted(c for c in CORE if met.get(c, 0) < 3)
print('chunks taught:', sum(len(m['teaches']) for m in spine))
print('core phrases:', len(CORE), ' reaching rung three:', len(CORE) - len(cold))
if cold:
    print('  NOT recurring enough:', ', '.join(cold))
print('distinct places:', len(set(m['place'] for m in spine)))
print('wrote', out)
