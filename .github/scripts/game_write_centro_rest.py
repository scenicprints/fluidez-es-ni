# -*- coding: utf-8 -*-
"""Finishes El Centro: centro-04 and centro-06 through centro-12, plus the
crowd lines that make them findable at all.

Copied from game_write_centro.py, which wrote the first four. One throwaway
file per batch -- never one tool call per mission.

The crowd file is MERGED, not overwritten: the six lines that point at
centro-01..05 are already in it and are still the only way to find those.

Self-checks at the bottom repeat what game_stage.py enforces (winnable in
written order, every accepted answer buildable) plus two the mockup needs and
the stage script does not know about:

  * no chunk text appears in both tiles and extra, because granada.html finds
    a tray tile by its text when it lays the answer out for you after two
    misses, and two tiles reading the same thing make that pick the wrong one;
  * every chunk the spine says a mission teaches is actually taught by one of
    its beats, or the spine and the content have quietly drifted apart.
"""
import io, json, os, sys, unicodedata

ROOT = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else None
GAME = os.path.join(ROOT, 'content', 'game')
CROWD = os.path.join(GAME, 'crowd')
for d in (GAME, CROWD):
    if not os.path.isdir(d):
        os.makedirs(d)


def beat(es, objective, key, say, en, tiles, extra, ok, teaches, good):
    return {'es': es, 'objective': objective, 'key': key, 'say': say, 'en': en,
            'tiles': tiles, 'extra': extra, 'ok': ok, 'teaches': teaches, 'good': good}


MISSIONS = [
{
 'id': 'centro-04', 'district': 'centro', 'tier': 2,
 'who': u'Doña de la banca', 'title': u'El calor',
 'goal': u'Sit on a bench and talk about the weather and nothing else',
 'culture': u'The heat is not small talk you have to get past — it is the '
            u'conversation. A doña on a shaded bench expects nothing from you '
            u'but agreement, and agreeing well is how a stranger turns into '
            u'somebody she recognises tomorrow.',
 'beats': [
  beat(u'Buenas tardes. Siéntese aquí, mijo, que hay sombra.',
       u'Sit down and say how hot it is', u'qué calor',
       u'Gracias. ¡Qué calor!', u'Thank you. It’s so hot!',
       [u'Gracias', u'qué calor'],
       [u'ni modo', u'está bien', u'mañana', u'por favor'],
       [u'gracias que calor', u'que calor', u'que calor gracias'],
       [u'qué calor', u'gracias'],
       u'¡Qué calor! is closer to a greeting than a complaint. Say it and you have said exactly the right thing.'),
  beat(u'Uh, y así es todo el año. En abril es peor, fíjese.',
       u'Agree with her', u'así es',
       u'Así es. Todos los días.', u'That’s how it is. Every day.',
       [u'así es', u'todos los días'],
       [u'ni modo', u'no sé', u'otro día', u'está bien'],
       [u'asi es todos los dias', u'asi es', u'asi es todos los dias ni modo'],
       [u'así es', u'todos los días'],
       u'Así es is the whole agreement. It sits where English puts "you’re telling me", and it never sounds like flattery.'),
  beat(u'Y no llueve. Se secó todo el patio, mire.',
       u'Shrug it off with her', u'ni modo',
       u'Ni modo. Así es.', u'Nothing to be done. That’s how it is.',
       [u'ni modo', u'así es'],
       [u'qué calor', u'está bien', u'por favor', u'otro día'],
       [u'ni modo asi es', u'ni modo', u'asi es ni modo'],
       [u'ni modo', u'así es'],
       u'Ni modo closes a complaint without arguing with it. Offering a solution here would be the odd thing to do.'),
 ]},
{
 'id': 'centro-06', 'district': 'centro', 'tier': 2,
 'who': u'El guía', 'title': u'La catedral',
 'goal': u'Get the story of the cathedral out of somebody who wants paying for it',
 'culture': u'He sells the tower climb, but the history he tells for free, '
            u'because telling it is the part he likes. Saying you have no '
            u'money on you today is not a refusal here — it is a fact about '
            u'today, and it leaves him his dignity and you the story.',
 'beats': [
  beat(u'¿Tour de la catedral, amigo? Cinco dólares y subimos a la torre.',
       u'Say you have no money on you', u'no ando',
       u'No ando con dinero.', u'I haven’t got any money on me.',
       [u'no ando', u'con dinero'],
       [u'otro día', u'está bien', u'muy amable', u'gracias'],
       [u'no ando con dinero', u'no ando', u'no ando con dinero gracias'],
       [u'no ando'],
       u'No ando con... is what you have not got on you right now, which is softer than no tengo. It closes nothing.'),
  beat(u'Ah, qué lástima. Y yo me sé toda la historia, desde que la quemaron.',
       u'Ask him to tell it anyway', u'¿me cuenta?',
       u'¿Me cuenta? Por favor.', u'Will you tell me? Please.',
       [u'¿me cuenta?', u'por favor'],
       [u'otro día', u'no ando', u'está bien', u'gracias'],
       [u'me cuenta por favor', u'me cuenta', u'por favor me cuenta'],
       [u'¿me cuenta?', u'por favor'],
       u'¿Me cuenta? asks for the story and not the tour, so there is nothing for him to charge for and no reason to say no.'),
  beat(u'Pues mire: la quemaron los filibusteros y la levantaron tres veces. '
       u'Esa torre es del quince.',
       u'Thank him for something he gave you free', u'muy amable',
       u'Muy amable. Gracias.', u'Very kind of you. Thank you.',
       [u'muy amable', u'gracias'],
       [u'otro día', u'está bien', u'por favor', u'no ando'],
       [u'muy amable gracias', u'muy amable', u'gracias muy amable'],
       [u'muy amable', u'gracias'],
       u'Muy amable pays for a favour that had no price on it. It is the nearest thing to a tip you can hand over in words.'),
  beat(u'Y para la torre aquí ando todos los días, desde temprano.',
       u'Leave the tower for another day', u'otro día',
       u'Otro día. Está bien.', u'Another day. Alright.',
       [u'otro día', u'está bien'],
       [u'muy amable', u'gracias', u'no ando', u'por favor'],
       [u'otro dia esta bien', u'otro dia', u'esta bien otro dia'],
       [u'otro día', u'está bien'],
       u'Otro día is a real later, not a polite no. It keeps him friendly and keeps the tower on offer.'),
 ]},
{
 'id': 'centro-07', 'district': 'centro', 'tier': 3,
 'who': u'El fotógrafo', 'title': u'La foto',
 'goal': u'Get a photo taken for a document, not for a postcard',
 'culture': u'Every trámite in Nicaragua wants photos, and the studio knows '
            u'the format better than the office that asks for it. Say para un '
            u'documento and he will get the size, the background and the crop '
            u'right without you knowing any of the numbers.',
 'beats': [
  beat(u'Buenas. ¿Una foto con la catedral atrás?',
       u'No — a photo for paperwork', u'para un documento',
       u'Buenas. Una foto para un documento.', u'Hello. A photo for a document.',
       [u'Buenas', u'una foto', u'para un documento'],
       [u'con la catedral', u'por favor', u'gracias', u'mañana'],
       [u'buenas una foto para un documento', u'una foto para un documento',
        u'una foto para un documento por favor'],
       [u'para un documento'],
       u'Para un documento is the entire instruction. He knows the sizes every office wants; you do not have to.'),
  beat(u'Ah, para trámite. ¿Y con qué fondo se la hago?',
       u'White background', u'fondo blanco',
       u'Fondo blanco, por favor.', u'White background, please.',
       [u'fondo blanco', u'por favor'],
       [u'fondo azul', u'sin lentes', u'gracias', u'mañana'],
       [u'fondo blanco por favor', u'fondo blanco'],
       [u'fondo blanco'],
       u'Fondo blanco is what the offices here take. Asking for it now saves you the second trip.'),
  beat(u'Listo. ¿Se quita los lentes o se los deja?',
       u'Without glasses', u'sin lentes',
       u'Sin lentes.', u'Without glasses.',
       [u'sin lentes'],
       [u'con lentes', u'fondo blanco', u'por favor', u'gracias'],
       [u'sin lentes', u'sin lentes por favor'],
       [u'sin lentes'],
       u'Lentes, not gafas and not anteojos. Gafas is Spain, anteojos is further south, and both get you a look.'),
  beat(u'Ya está. Le quedaron bien, mire.',
       u'Ask when they will be ready', u'¿cuándo salen?',
       u'¿Cuándo salen?', u'When will they be ready?',
       [u'¿cuándo', u'salen?'],
       [u'gracias', u'mañana', u'por favor', u'está bien'],
       [u'cuando salen', u'cuando salen por favor'],
       [u'¿cuándo salen?'],
       u'Photos salen, papers salen, results salen. Nobody here says estarán listas.'),
 ]},
{
 'id': 'centro-08', 'district': 'centro', 'tier': 3,
 'who': u'El del kiosco', 'title': u'El periódico',
 'goal': u'Buy a paper and get told the news before you read it',
 'culture': u'The man at the kiosk reads every paper he sells and will tell '
            u'you what is in it whether you ask or not. That summary is the '
            u'better half of what you are buying, and asking for it out loud '
            u'is what turns a sale into a conversation.',
 'beats': [
  beat(u'Buenas, ¿qué anda buscando?',
       u'Ask for the paper', u'el periódico',
       u'Quiero el periódico.', u'I want the paper.',
       [u'quiero', u'el periódico'],
       [u'una revista', u'por favor', u'gracias', u'está bien'],
       [u'quiero el periodico', u'el periodico', u'quiero el periodico por favor'],
       [u'el periódico', u'quiero'],
       u'Periódico, and on this corner it means La Prensa unless you say otherwise.'),
  beat(u'Aquí tiene. Quince pesos.',
       u'Ask what the news is today', u'¿qué dice?',
       u'¿Y qué dice hoy?', u'And what does it say today?',
       [u'¿y qué dice', u'hoy?'],
       [u'mañana', u'nada bueno', u'está bien', u'gracias'],
       [u'y que dice hoy', u'que dice hoy', u'y que dice'],
       [u'¿qué dice?'],
       u'¿Qué dice? asks the paper and the man at once, and he will answer for both. It is the cheapest conversation in Granada.'),
  beat(u'Uh. Lo de siempre, pues: que suben los precios, que no hay luz en Xalteva.',
       u'Agree that the news is never good', u'nada bueno',
       u'Nada bueno. Ni modo.', u'Nothing good. Oh well.',
       [u'nada bueno', u'ni modo'],
       [u'lo de siempre', u'está bien', u'gracias', u'mañana'],
       [u'nada bueno ni modo', u'nada bueno', u'ni modo nada bueno'],
       [u'nada bueno', u'ni modo'],
       u'Ni modo after bad news is agreement, not despair. It is how a complaint gets put down here.'),
  beat(u'¿Y mañana le guardo uno?',
       u'Yes — the usual', u'lo de siempre',
       u'Sí, lo de siempre.', u'Yes, the usual.',
       [u'sí', u'lo de siempre'],
       [u'nada bueno', u'está bien', u'gracias', u'mañana'],
       [u'si lo de siempre', u'lo de siempre', u'lo de siempre esta bien'],
       [u'lo de siempre'],
       u'Lo de siempre makes you a regular in three words, and it works the same at the comedor and the pulpería.'),
 ]},
{
 'id': 'centro-09', 'district': 'centro', 'tier': 3,
 'who': u'La turista perdida', 'title': u'La gringa perdida',
 'goal': u'Translate for a lost tourist, and feel your accent get worse',
 'culture': u'Standing between two people is the fastest Spanish you will '
            u'ever be made to do, and it is also the moment you stop being '
            u'the foreigner in the conversation. Nobody expects it to be '
            u'elegant — ella pregunta and dice que carry the whole job.',
 'beats': [
  beat(u'Excuse me — do you speak English? I’m looking for the boats to the '
       u'islands and nobody understands me.',
       u'Tell the vendedora what she is asking', u'ella pregunta',
       u'Ella pregunta por los botes.', u'She’s asking about the boats.',
       [u'ella pregunta', u'por los botes'],
       [u'yo le explico', u'no es aquí', u'otro día', u'así es'],
       [u'ella pregunta por los botes', u'ella pregunta'],
       [u'ella pregunta'],
       u'Ella pregunta... hands somebody else’s question over without you having to act it out or own it.'),
  beat(u'Wait — is it far? Can I walk there?',
       u'Pass that question on too', u'dice que',
       u'Dice que si puede ir caminando.', u'She’s asking whether she can walk there.',
       [u'dice que', u'si puede', u'ir caminando'],
       [u'no es aquí', u'yo le explico', u'otro día', u'así es'],
       [u'dice que si puede ir caminando', u'dice que si puede', u'dice que'],
       [u'dice que'],
       u'Dice que carries other people’s words for you. You will use it more than any tense you ever study.'),
  beat(u'Caminando son diez minutos, derechito por la Calzada. Pero de aquí no '
       u'salen, dígale.',
       u'Check you understood — this is not the place', u'no es aquí',
       u'Entonces no es aquí.', u'So it isn’t here.',
       [u'entonces', u'no es aquí'],
       [u'así es', u'yo le explico', u'otro día', u'dice que'],
       [u'entonces no es aqui', u'no es aqui', u'no es aqui entonces'],
       [u'no es aquí'],
       u'Saying it back as a flat statement is how you check you got it. She answers así es and the matter is settled.'),
  beat(u'Así es. Al final de la Calzada, donde está el muelle. ¿Le digo yo?',
       u'Take the job — you will explain it', u'yo le explico',
       u'No, yo le explico. Gracias.', u'No, I’ll explain it to her. Thank you.',
       [u'no', u'yo le explico', u'gracias'],
       [u'dice que', u'así es', u'otro día', u'por favor'],
       [u'no yo le explico gracias', u'yo le explico', u'yo le explico gracias'],
       [u'yo le explico'],
       u'Yo le explico takes the job off her. Le is the tourist — one small word does all the naming.'),
 ]},
{
 'id': 'centro-10', 'district': 'centro', 'tier': 4,
 'who': u'El poeta', 'title': u'Darío',
 'goal': u'Be told about Rubén Darío by a man who will not stop',
 'culture': u'Darío was born in Metapa and grew up in León, but when a '
            u'Nicaraguan says he is de aquí he means the country, and he is '
            u'right. Every schoolchild here has a poem by heart, which is why '
            u'the man in the park assumes you will learn one too.',
 'beats': [
  beat(u'Buenas. ¿Y usted sabe quién fue Rubén Darío?',
       u'Say who he was', u'el poeta',
       u'Buenas. Él es el poeta, ¿verdad?', u'Hello. He’s the poet, isn’t he?',
       [u'Buenas', u'él es el poeta', u'¿verdad?'],
       [u'de aquí', u'de memoria', u'gracias', u'por favor'],
       [u'buenas el es el poeta verdad', u'el es el poeta verdad',
        u'el es el poeta'],
       [u'el poeta'],
       u'El poeta with nothing after it is Darío. There is only one, and everybody knows which one you mean.'),
  beat(u'¡El poeta! Padre del modernismo. Y es nuestro, ¿oyó? Nuestro.',
       u'Agree that he belongs here', u'de aquí',
       u'Así es. Es de aquí.', u'That’s right. He’s from here.',
       [u'así es', u'es de aquí'],
       [u'de memoria', u'el poeta', u'gracias', u'por favor'],
       [u'asi es es de aqui', u'es de aqui', u'es de aqui asi es'],
       [u'de aquí', u'así es'],
       u'De aquí means Nicaragua, not Granada. Agreeing is the right answer; the geography lesson is not.'),
  beat(u'Repita conmigo, pues: «Margarita, está linda la mar». Apréndaselo.',
       u'Tell him you have got it', u'me lo aprendí',
       u'Ya me lo aprendí.', u'I’ve learned it now.',
       [u'ya', u'me lo aprendí'],
       [u'de memoria', u'otro día', u'gracias', u'por favor'],
       [u'ya me lo aprendi', u'me lo aprendi', u'ya me lo aprendi gracias'],
       [u'me lo aprendí'],
       u'Me lo aprendí, with the me in it, is learning something for yourself. Aprendí on its own sounds like a school report.'),
  beat(u'¿De memoria? A ver, sin leerlo.',
       u'By heart, and thank him', u'de memoria',
       u'De memoria. Gracias.', u'By heart. Thank you.',
       [u'de memoria', u'gracias'],
       [u'me lo aprendí', u'otro día', u'por favor', u'así es'],
       [u'de memoria gracias', u'de memoria', u'gracias de memoria'],
       [u'de memoria'],
       u'De memoria is by heart, and it is the only way anybody here has ever learned a poem. Saying it tells him you did it his way.'),
 ]},
{
 'id': 'centro-11', 'district': 'centro', 'tier': 4,
 'who': u'El transitero', 'title': u'La multa',
 'goal': u'Talk your way out of a ticket, or find out what not doing so costs',
 'culture': u'The transitero keeps your licence and you pay the ticket at a '
            u'bank, not to him. Offering him money instead is a crime and a '
            u'worse afternoon. Politeness is the only lever you actually '
            u'have, and jefe plus an admission is most of it.',
 'beats': [
  beat(u'Buenas. Su licencia, por favor. Se pasó el alto.',
       u'Greet him properly and admit it', u'no me di cuenta',
       u'Buenas, jefe. No me di cuenta.', u'Hello, boss. I didn’t notice.',
       [u'Buenas', u'jefe', u'no me di cuenta'],
       [u'está bien', u'ni modo', u'otro día', u'disculpe'],
       [u'buenas jefe no me di cuenta', u'no me di cuenta',
        u'buenas jefe no me di cuenta disculpe'],
       [u'jefe', u'no me di cuenta'],
       u'Jefe is respect without grovelling and no me di cuenta admits it without arguing. Both make the next minute cheaper.'),
  beat(u'Es infracción, pues. Enséñeme la licencia y la circulación.',
       u'You have not got the licence on you', u'ando sin',
       u'Ando sin licencia, jefe.', u'I haven’t got my licence on me, boss.',
       [u'ando sin licencia', u'jefe'],
       [u'no me di cuenta', u'está bien', u'ni modo', u'disculpe'],
       [u'ando sin licencia jefe', u'ando sin licencia'],
       [u'ando sin'],
       u'Ando sin... is not having it on you today, which is a smaller thing than no tengo. Andar is how Nicaragua says what you are carrying.'),
  beat(u'Uh, peor. Entonces son quinientos, y los paga en el banco.',
       u'Take it without arguing', u'ni modo',
       u'Ni modo. Está bien, jefe.', u'Oh well. Alright, boss.',
       [u'ni modo', u'está bien', u'jefe'],
       [u'no me di cuenta', u'ando sin', u'otro día', u'disculpe'],
       [u'ni modo esta bien jefe', u'ni modo esta bien', u'esta bien jefe'],
       [u'ni modo'],
       u'Taking it is what keeps it at five hundred. There is no version of this conversation where arguing costs you less.'),
  beat(u'Aquí le va el papel. Tiene ocho días para pagarlo.',
       u'Apologise for taking up his time', u'disculpe la molestia',
       u'Disculpe la molestia, jefe.', u'Sorry for the trouble, boss.',
       [u'disculpe la molestia', u'jefe'],
       [u'ni modo', u'está bien', u'ando sin', u'otro día'],
       [u'disculpe la molestia jefe', u'disculpe la molestia'],
       [u'disculpe la molestia'],
       u'Disculpe la molestia ends it on your terms. It is what you say to anybody whose day you took up, and it costs nothing.'),
 ]},
{
 'id': 'centro-12', 'district': 'centro', 'tier': 5,
 'who': u'El borracho amable', 'title': u'El del parque',
 'goal': u'Get away from a friendly drunk without insulting him',
 'culture': u'He is harmless and the whole park knows him. Walking off '
            u'mid-sentence is what a chele does, and the doñas on the benches '
            u'will see you do it. Leaving properly is a set of fixed phrases '
            u'and it costs you thirty seconds.',
 'beats': [
  beat(u'¡Amigo! ¡Amigo, venga! Yo trabajé ocho años en Miami. Allá sí se gana bien, ¿oyó?',
       u'Agree, and stay standing', u'así es',
       u'Así es. Ocho años.', u'Is that right. Eight years.',
       [u'así es', u'ocho años'],
       [u'ya me voy', u'no ando', u'cuídese', u'otro día'],
       [u'asi es ocho años', u'asi es'],
       [u'así es'],
       u'Así es agrees with the claim without joining the story, and echoing his number back shows you were listening. Contradicting a drunk is the long way home.'),
  beat(u'Regáleme veinte pesos, hermano, para un fresco. Nada más veinte.',
       u'Say you have nothing on you', u'no ando',
       u'No ando con nada, hermano.', u'I haven’t got anything on me, brother.',
       [u'no ando con nada', u'hermano'],
       [u'ya me voy', u'otro día', u'cuídese', u'así es'],
       [u'no ando con nada hermano', u'no ando con nada'],
       [u'no ando'],
       u'No ando con nada is honest and unarguable. No tengo invites a discussion about your shoes.'),
  beat(u'Ah, ni modo. Pero óigame esta otra, una historia buenísima...',
       u'Leave, but leave the door open', u'ya me voy',
       u'Ya me voy. Otro día conversamos.', u'I’m off now. We’ll talk another day.',
       [u'ya me voy', u'otro día conversamos'],
       [u'cuídese', u'que le vaya bien', u'no ando', u'así es'],
       [u'ya me voy otro dia conversamos', u'ya me voy', u'otro dia conversamos'],
       [u'ya me voy', u'otro día conversamos'],
       u'Ya me voy on its own is abrupt. Otro día conversamos turns leaving into a plan, and he will hold you to it.'),
  beat(u'¡Vaya pues! Es usted buena gente, hermano.',
       u'Say goodbye the whole way', u'cuídese',
       u'Cuídese. Que le vaya bien.', u'Take care. All the best.',
       [u'cuídese', u'que le vaya bien'],
       [u'otro día', u'ya me voy', u'así es', u'gracias'],
       [u'cuidese que le vaya bien', u'cuidese', u'que le vaya bien'],
       [u'cuídese', u'que le vaya bien'],
       u'Both at once is the full goodbye: cuídese looks after him, que le vaya bien wishes the rest of his day well. It is what stops leaving reading as escaping.'),
 ]},
]

# The crowd. Nothing is signposted and Granada has no usable street names, so
# these are how a mission is found at all. Kept short and easy on purpose:
# being lost should be a nudge, not a puzzle.
HINTS = [
 {'kind': u'doña en la puerta', 'district': 'centro',
  'says': u'Con este calor nadie camina. En el parque, en la banca de la sombra, siempre hay doñas conversando.',
  'en': u'Nobody walks in this heat. In the park, on the shaded bench, there are always ladies talking.',
  'points_at': ['centro-04']},
 {'kind': u'obrero', 'district': 'centro',
  'says': u'Si le pega el sol, siéntese en el parque. Ahí la doña le conversa todo el día.',
  'en': u'If the sun gets you, sit in the park. The doña there will talk to you all day.',
  'points_at': ['centro-04']},
 {'kind': u'chavalo en bici', 'district': 'centro',
  'says': u'¿Va a la catedral? En la puerta anda un señor que se sabe toda la historia. Le va a pedir plata, pero se la sabe.',
  'en': u'Going to the cathedral? There is a man at the door who knows the whole history. He will ask you for money, but he knows it.',
  'points_at': ['centro-06']},
 {'kind': u'vendedora', 'district': 'centro',
  'says': u'¿Necesita foto para un trámite? El estudio está a media cuadra, con el señor de los lentes.',
  'en': u'Need a photo for paperwork? The studio is half a block away, the man with the glasses.',
  'points_at': ['centro-07']},
 {'kind': u'policía', 'district': 'centro',
  'says': u'Foto para documento la hacen aquí en el centro. Y la multa se paga en el banco, no aquí.',
  'en': u'They do document photos here in the centre. And a fine is paid at the bank, not here.',
  'points_at': ['centro-07', 'centro-11']},
 {'kind': u'viejo de la esquina', 'district': 'centro',
  'says': u'El periódico lo venden en el kiosco de la esquina del parque. Y ahí mismo le cuentan lo que dice.',
  'en': u'They sell the paper at the kiosk on the corner of the park. And right there they tell you what it says.',
  'points_at': ['centro-08']},
 {'kind': u'caponero', 'district': 'centro',
  'says': u'Ahí en la esquina anda una gringa perdida con un mapa. Nadie le entiende, pues.',
  'en': u'There is a lost gringa on the corner with a map. Nobody understands her.',
  'points_at': ['centro-09']},
 {'kind': u'turista', 'district': 'centro',
  'says': u'Do you speak English? I can’t find the boats and everyone points a different way.',
  'en': u'(She is asking about the boats to the isletas, and somebody has to tell the vendedora what she wants.)',
  'points_at': ['centro-09']},
 {'kind': u'evangélico', 'district': 'centro',
  'says': u'Vaya a la catedral, hermano. Y si le habla el poeta del sombrero, óigalo, que es buena gente.',
  'en': u'Go to the cathedral, brother. And if the poet in the hat speaks to you, hear him out, he is a good sort.',
  'points_at': ['centro-06', 'centro-10']},
 {'kind': u'chavalo en bici', 'district': 'centro',
  'says': u'Al señor del sombrero no le pregunte por Darío. Le recita el poema completo, se lo digo yo.',
  'en': u'Do not ask the man in the hat about Darío. He will recite you the whole poem, I am telling you.',
  'points_at': ['centro-10']},
 {'kind': u'cuidacarros', 'district': 'centro',
  'says': u'Cuidado con el alto de la esquina, jefe. Ahí se para el transitero todos los días.',
  'en': u'Watch the stop sign on the corner, boss. The traffic officer stands there every day.',
  'points_at': ['centro-11']},
 {'kind': u'doña en la puerta', 'district': 'centro',
  'says': u'En el parque anda el pobre Chepe, tomado desde temprano. No le crea nada, pero salúdelo.',
  'en': u'Poor Chepe is in the park, drinking since early. Believe nothing he says, but greet him.',
  'points_at': ['centro-12']},
 {'kind': u'borracho amable', 'district': 'centro',
  'says': u'¡Hermano! Venga que le cuento de Miami. Ocho años estuve allá, ocho.',
  'en': u'Brother! Come here and I will tell you about Miami. I was there eight years, eight.',
  'points_at': ['centro-12']},
]

# ---------------------------------------------------------------- write

for m in MISSIONS:
    with io.open(os.path.join(GAME, m['id'] + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(m, ensure_ascii=False, indent=1) + u'\n')

crowd_path = os.path.join(CROWD, 'centro.json')
existing = []
if os.path.exists(crowd_path):
    with io.open(crowd_path, encoding='utf-8') as f:
        existing = json.load(f)
have = set((r.get('kind'), r.get('says')) for r in existing)
merged = existing + [h for h in HINTS if (h['kind'], h['says']) not in have]
with io.open(crowd_path, 'w', encoding='utf-8') as f:
    f.write(json.dumps(merged, ensure_ascii=False, indent=1) + u'\n')

# ---------------------------------------------------------------- check

PUNCT = set(u"¿?¡!.,;:\"'«»")


def norm(t):
    t = (t or u"").lower()
    t = u"".join(c for c in unicodedata.normalize("NFD", t)
                 if not unicodedata.combining(c))
    t = u"".join(u" " if c in PUNCT else c for c in t)
    return u" ".join(t.split())


spine = json.load(io.open(os.path.join(ROOT, 'content', 'plan',
                                       'game-spine.json'), encoding='utf-8'))
planned = dict((m['id'], m) for m in spine['missions'])

bad = []
for m in MISSIONS:
    for i, b in enumerate(m['beats'], 1):
        w = u'%s beat %d' % (m['id'], i)
        accepted = set(norm(x) for x in b['ok'])
        if norm(u' '.join(b['tiles'])) not in accepted:
            bad.append(u'%s unwinnable: %r' % (w, norm(u' '.join(b['tiles']))))
        pool = set(norm(u' '.join(b['tiles'] + b['extra'])).split())
        for a in b['ok']:
            if not set(norm(a).split()) <= pool:
                bad.append(u'%s accepts unbuildable %r' % (w, a))
        dupes = set(norm(t) for t in b['tiles']) & set(norm(e) for e in b['extra'])
        if dupes:
            bad.append(u'%s has the same chunk in tiles and extra: %s'
                       % (w, u', '.join(sorted(dupes))))
        if len(b['extra']) < 4:
            bad.append(u'%s has only %d distractors, and the top help rung '
                       u'asks for 4' % (w, len(b['extra'])))
    taught = set()
    for b in m['beats']:
        taught |= set(b['teaches'])
    missing = [c for c in planned[m['id']]['teaches'] if c not in taught]
    if missing:
        bad.append(u'%s never teaches %s' % (m['id'], u', '.join(missing)))

pointed = set()
for h in merged:
    pointed |= set(h['points_at'])
for m in MISSIONS:
    if m['id'] not in pointed:
        bad.append(u'%s is unfindable: nobody in the street points at it' % m['id'])

lines = [u'wrote %d missions, %d beats, %d new crowd lines (%d in the file)'
         % (len(MISSIONS), sum(len(m['beats']) for m in MISSIONS),
            len(merged) - len(existing), len(merged))]
lines += bad or [u'checks clean']
report = u'\n'.join(lines) + u'\n'
if OUT:
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write(report)
print(report.encode('ascii', 'replace').decode('ascii'))
