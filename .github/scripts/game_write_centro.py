# -*- coding: utf-8 -*-
"""Emits the first real missions into content/game/, plus the crowd who point
at them. One throwaway file per batch — never one tool call per mission."""
import io, json, os, sys

ROOT = sys.argv[1]
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
 'id': 'centro-01', 'district': 'centro', 'tier': 1,
 'who': u'El muchacho del hostal', 'title': u'La primera noche',
 'goal': u'Get a room for your first three nights',
 'culture': u'Cuarto, not habitación. Habitación is what a Spaniard says, and everyone will hear it.',
 'beats': [
  beat(u'Buenas. ¿En qué le ayudo?', u'Ask for a room', u'Buenas',
       u'Buenas. Quiero un cuarto.', u'Hello. I want a room.',
       [u'Buenas', u'quiero', u'un cuarto'],
       [u'mañana', u'no', u'gracias', u'tres noches'],
       [u'buenas quiero un cuarto', u'quiero un cuarto',
        u'buenas quiero un cuarto gracias', u'quiero un cuarto gracias'],
       [u'Buenas', u'quiero', u'un cuarto'],
       u'Buenas on its own is the whole greeting here. Nobody says buenos días after about nine.'),
  beat(u'¿Para cuántas noches?', u'Three nights', u'tres noches',
       u'Tres noches.', u'Three nights.',
       [u'tres', u'noches'],
       [u'córdobas', u'cinco', u'un cuarto', u'mañana'],
       [u'tres noches', u'tres'],
       [u'tres noches'],
       u'Short is normal. Nobody builds a sentence for this.'),
  beat(u'Son quince dólares la noche. ¿Está bien?', u'Agree', u'está bien',
       u'Está bien.', u'That’s fine.',
       [u'está', u'bien'],
       [u'no', u'muy', u'caro', u'gracias'],
       [u'esta bien', u'esta bien gracias', u'muy bien'],
       [u'está bien'],
       u'Está bien is the whole language for yes, agreed, fine, alright.'),
 ]},
{
 'id': 'centro-02', 'district': 'centro', 'tier': 1,
 'who': u'La muchacha del comedor', 'title': u'El desayuno',
 'goal': u'Order breakfast and ask what you owe',
 'culture': u'Gallo pinto is rice and beans fried together, and it is breakfast. There is no other option and nobody is apologising for that.',
 'beats': [
  beat(u'Buenas, ¿qué le doy?', u'Order gallo pinto', u'por favor',
       u'Buenas. Un gallo pinto, por favor.', u'Hello. A gallo pinto, please.',
       [u'Buenas', u'un gallo pinto', u'por favor'],
       [u'un café', u'no', u'la cuenta', u'mañana'],
       [u'buenas un gallo pinto por favor', u'un gallo pinto por favor',
        u'buenas un gallo pinto', u'un gallo pinto'],
       [u'un gallo pinto', u'por favor'],
       u'¿Qué le doy? is what you get instead of a menu. Answer with the thing, not a sentence.'),
  beat(u'¿Y de tomar?', u'A coffee', u'por favor',
       u'Un café, por favor.', u'A coffee, please.',
       [u'un café', u'por favor'],
       [u'un gallo pinto', u'agua', u'no', u'Buenas'],
       [u'un cafe por favor', u'un cafe', u'buenas un cafe por favor'],
       [u'un café'],
       u'De tomar covers anything you drink, not just alcohol.'),
  beat(u'Ahí le va, pues.', u'Ask what you owe', u'cuánto le debo',
       u'¿Cuánto le debo?', u'How much do I owe you?',
       [u'cuánto', u'le debo'],
       [u'la cuenta', u'por favor', u'está bien', u'gracias'],
       [u'cuanto le debo', u'cuanto le debo por favor',
        u'la cuenta por favor', u'la cuenta'],
       [u'cuánto le debo'],
       u'¿Cuánto le debo? is warmer than la cuenta. It assumes you are staying.'),
 ]},
{
 'id': 'centro-03', 'district': 'centro', 'tier': 1,
 'who': u'El mesero', 'title': u'En español',
 'goal': u'Get served in Spanish by somebody who would rather practise English',
 'culture': u'He is being friendly, not rude — English is worth money on this street. Asking in Spanish is how you turn it round without embarrassing him.',
 'beats': [
  beat(u'Hello my friend! Where you from?', u'Answer, and ask to speak Spanish', u'en español',
       u'Buenas. ¿Podemos hablar en español?', u'Hello. Can we speak in Spanish?',
       [u'Buenas', u'¿podemos hablar', u'en español?'],
       [u'no entiendo', u'gracias', u'otro día', u'está bien'],
       [u'buenas podemos hablar en espanol', u'podemos hablar en espanol'],
       [u'en español'],
       u'Asking is better than just answering in Spanish and hoping. He will switch, and he will be pleased.'),
  beat(u'¡Ah! ¿Está aprendiendo? Muy bien. ¿Qué va a querer?', u'Say you are learning, and ask for his help', u'estoy aprendiendo',
       u'Estoy aprendiendo. Ayúdeme, por favor.', u'I am learning. Help me, please.',
       [u'estoy aprendiendo', u'ayúdeme', u'por favor'],
       [u'no sé', u'gracias', u'de nuevo', u'está bien'],
       [u'estoy aprendiendo ayudeme por favor', u'estoy aprendiendo ayudeme',
        u'estoy aprendiendo'],
       [u'estoy aprendiendo', u'ayúdeme'],
       u'Say it once and people will slow down for the rest of the conversation. It is the most useful sentence you own.'),
  beat(u'Perfecto. Entonces le traigo el menú y me dice, ¿va?', u'You missed that — ask again', u'de nuevo',
       u'De nuevo, por favor.', u'Again, please.',
       [u'de nuevo', u'por favor'],
       [u'gracias', u'está bien', u'ya va', u'no'],
       [u'de nuevo por favor', u'de nuevo'],
       [u'de nuevo'],
       u'Asking twice is normal and costs you nothing. Nodding at something you did not catch costs you the rest of the conversation.'),
 ]},
{
 'id': 'centro-05', 'district': 'centro', 'tier': 2,
 'who': u'El cuidacarros', 'title': u'El cuidacarros',
 'goal': u'Understand that the man watching your moto has a job, not a racket',
 'culture': u'This is not a shakedown and refusing marks you instantly. Ten córdobas, and your moto is still there when you come back. Everybody pays it.',
 'beats': [
  beat(u'¿Se lo cuido, jefe?', u'Leave it with him', u'ahí se lo dejo',
       u'Ahí se lo dejo.', u'I’ll leave it with you.',
       [u'ahí', u'se lo dejo'],
       [u'no gracias', u'yo lo cuido', u'no es mío', u'está bien'],
       [u'ahi se lo dejo', u'se lo dejo'],
       [u'ahí se lo dejo'],
       u'Jefe is not sarcasm. It is what he calls everybody, and it costs nothing to be called it.'),
  beat(u'Ahí está, jefe. Nadie lo tocó.', u'Pay him', u'diez pesos',
       u'Aquí tiene. Diez pesos.', u'Here you go. Ten córdobas.',
       [u'aquí tiene', u'diez pesos'],
       [u'cien pesos', u'no tengo', u'está caro', u'mañana'],
       [u'aqui tiene diez pesos', u'diez pesos', u'aqui tiene'],
       [u'diez pesos'],
       u'Pesos, not córdobas, in the street. The note says córdoba and nobody says it.'),
  beat(u'Gracias, jefe. Aquí lo espero.', u'Thank him properly', u'gracias',
       u'Gracias, muy amable.', u'Thank you, that’s very kind.',
       [u'gracias', u'muy amable'],
       [u'adiós', u'por favor', u'está bien', u'otro día'],
       [u'gracias muy amable', u'muy amable', u'gracias'],
       [u'gracias', u'muy amable'],
       u'Muy amable is the everyday sign-off after somebody does you a small service.'),
 ]},
]

# The crowd. Nothing is signposted and Granada has no usable street names, so
# these are how a mission is found at all. Kept short and easy on purpose:
# being lost should be a nudge, not a puzzle.
HINTS = [
 {'kind': u'doña en la puerta', 'district': 'centro',
  'says': u'¿Anda buscando dónde quedarse? Ahí nomás, en la esquina, hay hospedaje.',
  'en': u'Looking for somewhere to stay? Just there, on the corner, there is a guesthouse.',
  'points_at': ['centro-01']},
 {'kind': u'chavalo en bici', 'district': 'centro',
  'says': u'¿Tiene hambre? El comedor de la Calzada abre temprano.',
  'en': u'Hungry? The comedor on La Calzada opens early.',
  'points_at': ['centro-02']},
 {'kind': u'caponero', 'district': 'centro',
  'says': u'Si quiere desayunar, La Calzada. Ahí desayunan todos.',
  'en': u'If you want breakfast, La Calzada. Everybody eats there.',
  'points_at': ['centro-02', 'centro-03']},
 {'kind': u'viejo de la esquina', 'district': 'centro',
  'says': u'A ese mesero no le hable en inglés, que después no lo suelta.',
  'en': u'Do not speak English to that waiter, or he will never let you go.',
  'points_at': ['centro-03']},
 {'kind': u'vendedora', 'district': 'centro',
  'says': u'Deje la moto con el muchacho, él se la cuida. Es su trabajo, pues.',
  'en': u'Leave the moto with the lad, he will watch it. It is his job.',
  'points_at': ['centro-05']},
 {'kind': u'cuidacarros', 'district': 'centro',
  'says': u'Aquí le cuido cualquier cosa, jefe. Nada le pasa.',
  'en': u'I will watch anything for you here, boss. Nothing happens to it.',
  'points_at': ['centro-05']},
]

for m in MISSIONS:
    with io.open(os.path.join(GAME, m['id'] + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(m, ensure_ascii=False, indent=1) + u'\n')
with io.open(os.path.join(CROWD, 'centro.json'), 'w', encoding='utf-8') as f:
    f.write(json.dumps(HINTS, ensure_ascii=False, indent=1) + u'\n')

print('wrote %d missions, %d beats, %d crowd lines'
      % (len(MISSIONS), sum(len(m['beats']) for m in MISSIONS), len(HINTS)))
