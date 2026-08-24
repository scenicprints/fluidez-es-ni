# -*- coding: utf-8 -*-
"""Writes El Mercado: mercado-01 through mercado-12, and the crowd who point
at them.

Same shape as game_write_centro_rest.py, and the same self-checks at the
bottom -- winnable in written order, every accepted answer buildable, no chunk
twice in one tray, every chunk the spine promises actually taught, and nobody
unfindable.

The district is the municipal market and the streets round it, which is where
a learner finds out what things really cost. Almost every mission here is a
transaction, so the Spanish is the Spanish of buying: ask the price, say it is
dear, name a weight, say what you are cooking, close the deal.
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
 'id': 'mercado-01', 'district': 'mercado', 'tier': 1,
 'who': u'La verdulera', 'title': u'La fruta',
 'goal': u'Buy fruit for the week without paying the chele price',
 'culture': u'Nothing has a price on it. You ask ¿a cómo?, the first number '
            u'you are given is the one for a foreigner, and saying está caro '
            u'is not rudeness — it is the second line of a conversation you '
            u'are both expected to have.',
 'beats': [
  beat(u'¡Adelante, mi amor! ¿Qué le doy? Hay mango, papaya, jocote.',
       u'Ask the price of the mango', u'¿a cómo?',
       u'¿A cómo el mango?', u'How much is the mango?',
       [u'¿a cómo', u'el mango?'],
       [u'una libra', u'está caro', u'gracias', u'mañana'],
       [u'a como el mango', u'a como'],
       [u'¿a cómo?'],
       u'¿A cómo? is the whole question and you will use it every day. Asking is not haggling yet — it is finding out where the haggling starts.'),
  beat(u'A veinte la libra, fresquito, del día.',
       u'Say that is dear', u'está caro',
       u'Está caro.', u'That’s expensive.',
       [u'está caro'],
       [u'muy', u'está bien', u'ni modo', u'una libra'],
       [u'esta caro', u'esta muy caro'],
       [u'está caro'],
       u'Está caro is neither an insult nor a refusal. It is the line that gets you the real price, and she is waiting for it.'),
  beat(u'Uy. Bueno, se lo dejo a quince. Ni modo.',
       u'Ask for a pound of it', u'una libra',
       u'Una libra de mango.', u'A pound of mango.',
       [u'una libra', u'de mango'],
       [u'media libra', u'está caro', u'gracias', u'por favor'],
       [u'una libra de mango', u'una libra de mango por favor'],
       [u'una libra', u'de mango'],
       u'Everything on this floor is sold by the libra, and a libra is a pound. The market here never went metric and never will.'),
  beat(u'Ahí le va. ¿Algo más, mi amor?',
       u'That is all', u'está bien',
       u'Está bien. Gracias.', u'That’s everything. Thank you.',
       [u'está bien', u'gracias'],
       [u'una libra', u'otro día', u'por favor', u'ni modo'],
       [u'esta bien gracias', u'esta bien', u'gracias'],
       [u'está bien'],
       u'Está bien closes the sale without cutting her off. Mi amor is not flirting — it is what she calls everybody who stops at the stall.'),
 ]},
{
 'id': 'mercado-02', 'district': 'mercado', 'tier': 1,
 'who': u'El del cambio', 'title': u'Los reales',
 'goal': u'Change dollars and insist on small notes',
 'culture': u'The money changers work the street outside the market with a '
            u'calculator and a fold of notes, everybody uses them, and they '
            u'beat the bank. Ask the rate first and ask for small notes: a '
            u'thousand-córdoba note is no use to a pulpería or a bus.',
 'beats': [
  beat(u'¿Cambia, amigo? Dólares, córdobas.',
       u'Ask today’s rate', u'¿a cómo está?',
       u'¿A cómo está hoy?', u'What’s the rate today?',
       [u'¿a cómo está', u'hoy?'],
       [u'dólares', u'está bien', u'gracias', u'mañana'],
       [u'a como esta hoy', u'a como esta'],
       [u'¿a cómo está?'],
       u'¿A cómo está? asks today’s rate. It moves, everybody knows roughly what it should be, and asking says that you do too.'),
  beat(u'A treinta y seis con cincuenta.',
       u'Change a hundred dollars', u'quiero cambiar',
       u'Quiero cambiar cien dólares.', u'I want to change a hundred dollars.',
       [u'quiero cambiar', u'cien', u'dólares'],
       [u'billetes pequeños', u'está bien', u'gracias', u'mañana'],
       [u'quiero cambiar cien dolares', u'quiero cambiar cien'],
       [u'quiero cambiar', u'dólares'],
       u'Quiero cambiar is the entire transaction. He counts it into your hand and you are expected to watch him do it.'),
  beat(u'Listo. ¿Se los doy en billetes de mil?',
       u'Ask for small notes', u'billetes pequeños',
       u'Billetes pequeños, por favor.', u'Small notes, please.',
       [u'billetes pequeños', u'por favor'],
       [u'de mil', u'está bien', u'gracias', u'dólares'],
       [u'billetes pequenos por favor', u'billetes pequenos'],
       [u'billetes pequeños'],
       u'A thousand-córdoba note is nearly useless: the pulpería cannot change it and neither can the bus. Ask for small ones every single time.'),
  beat(u'Ahí está. Cuéntelos, pues.',
       u'Count them and agree', u'está bien',
       u'Está bien. Gracias.', u'That’s right. Thank you.',
       [u'está bien', u'gracias'],
       [u'ni modo', u'otro día', u'por favor', u'dólares'],
       [u'esta bien gracias', u'esta bien'],
       [u'está bien'],
       u'Cuéntelos is not a challenge. Counting it in front of him is normal, he expects it, and not counting is the odd thing to do.'),
 ]},
{
 'id': 'mercado-03', 'district': 'mercado', 'tier': 2,
 'who': u'La carnicera', 'title': u'La carne',
 'goal': u'Buy meat by weight and get the cut you meant',
 'culture': u'There is no case to point at and no label to read. You say a '
            u'weight and what you are cooking, and she cuts for it — that is '
            u'the service, it is free, and it works better than choosing '
            u'would.',
 'beats': [
  beat(u'Buenas. ¿Qué le doy hoy?',
       u'Half a pound', u'media libra',
       u'Media libra, por favor.', u'Half a pound, please.',
       [u'media libra', u'por favor'],
       [u'una libra', u'para sopa', u'gracias', u'sin hueso'],
       [u'media libra por favor', u'media libra'],
       [u'media libra'],
       u'Media libra. It is asked for out loud, by weight, and there is nothing behind the glass to point at.'),
  beat(u'¿Y para qué la quiere? ¿Para sopa o para asar?',
       u'For soup', u'para sopa',
       u'Para sopa.', u'For soup.',
       [u'para sopa'],
       [u'para asar', u'sin hueso', u'gracias', u'mañana'],
       [u'para sopa'],
       [u'para sopa'],
       u'Tell her the dish and she picks the cut. You have to know what you are cooking; you do not have to know any butchery.'),
  beat(u'¿Con hueso o sin hueso?',
       u'Without the bone', u'sin hueso',
       u'Sin hueso.', u'Without bone.',
       [u'sin hueso'],
       [u'con hueso', u'para sopa', u'gracias', u'por favor'],
       [u'sin hueso', u'sin hueso por favor'],
       [u'sin hueso'],
       u'The bone is where the flavour is and she may well say so, but sin hueso is an ordinary thing to ask for and she will not argue twice.'),
  beat(u'¿Así está bien, o le pongo un poquito más?',
       u'That is the right amount', u'así está bien',
       u'Así está bien. Gracias.', u'That’s just right. Thank you.',
       [u'así está bien', u'gracias'],
       [u'más', u'sin hueso', u'por favor', u'otro día'],
       [u'asi esta bien gracias', u'asi esta bien'],
       [u'así está bien'],
       u'Así está bien stops the scale where it is. It is the polite enough, and it works for rice, for beans and for how much they are pouring you.'),
 ]},
{
 'id': 'mercado-04', 'district': 'mercado', 'tier': 2,
 'who': u'El de los granos', 'title': u'Los frijoles',
 'goal': u'Buy beans and be told how to cook them',
 'culture': u'Red beans, not black — black is Guatemala and Costa Rica, and '
            u'gallo pinto is made with rojos. Ask how to cook them and you '
            u'get the whole recipe twice over, which is included in the '
            u'price and is worth more than the beans.',
 'beats': [
  beat(u'Buenas, ¿qué anda llevando?',
       u'A pound of beans', u'una libra de frijoles',
       u'Una libra de frijoles.', u'A pound of beans.',
       [u'una libra de frijoles'],
       [u'rojos', u'negros', u'gracias', u'por favor'],
       [u'una libra de frijoles', u'una libra de frijoles por favor'],
       [u'una libra de frijoles'],
       u'Out of the sack, into the scale, weighed in front of you. Nothing here comes in a packet.'),
  beat(u'¿Rojos o negros?',
       u'Red', u'rojos',
       u'Rojos.', u'Red ones.',
       [u'rojos'],
       [u'negros', u'una libra de frijoles', u'gracias', u'por favor'],
       [u'rojos', u'rojos por favor'],
       [u'rojos'],
       u'Red. Black beans are Guatemala and Costa Rica; a Nicaraguan kitchen runs on rojos and so does gallo pinto.'),
  beat(u'Ahí le van, fresquitos, de Nueva Guinea.',
       u'Ask how to cook them', u'¿cómo los hago?',
       u'¿Y cómo los hago?', u'And how do I cook them?',
       [u'¿y cómo', u'los hago?'],
       [u'gracias', u'mañana', u'con todo', u'por favor'],
       [u'y como los hago', u'como los hago'],
       [u'¿cómo los hago?'],
       u'Ask, and you get the recipe, then the recipe again, then the answer to a question you did not ask. All of it is free and most of it is right.'),
  beat(u'Los deja en agua desde anoche. Y les echa cebolla, chiltoma, ajo...',
       u'With the lot, then', u'con todo',
       u'Con todo. Está bien.', u'With everything. Got it.',
       [u'con todo', u'está bien'],
       [u'sin cebolla', u'gracias', u'otro día', u'por favor'],
       [u'con todo esta bien', u'con todo'],
       [u'con todo'],
       u'Con todo is the lot — onion, chiltoma, garlic. Chiltoma, not pimiento: the pepper has a different name here and this is where you learn it.'),
 ]},
{
 'id': 'mercado-05', 'district': 'mercado', 'tier': 2,
 'who': u'Doña de la fritanga', 'title': u'La fritanga',
 'goal': u'Order from a fritanga like somebody who eats there',
 'culture': u'The fritanga is the evening grill on the pavement, and it is '
            u'where most people actually eat. An enchilado here is a fried '
            u'stuffed tortilla off that grill and has nothing to do with the '
            u'Mexican dish that shares the name.',
 'beats': [
  beat(u'Buenas noches. ¿Qué le sirvo?',
       u'One enchilado', u'un enchilado',
       u'Un enchilado, por favor.', u'One enchilado, please.',
       [u'un enchilado', u'por favor'],
       [u'dos', u'con ensalada', u'gracias', u'para llevar'],
       [u'un enchilado por favor', u'un enchilado'],
       [u'un enchilado'],
       u'A fried, stuffed tortilla straight off the grill. Order it by name and nobody will ask you anything else about it.'),
  beat(u'¿Con ensalada y maduro?',
       u'Yes, with salad', u'con ensalada',
       u'Con ensalada, sí.', u'With salad, yes.',
       [u'con ensalada', u'sí'],
       [u'sin ensalada', u'no', u'gracias', u'para llevar'],
       [u'con ensalada si', u'con ensalada'],
       [u'con ensalada'],
       u'The ensalada is shredded cabbage in vinegar and it goes on the plate, not beside it. Maduro is fried sweet plantain and you want that too.'),
  beat(u'¿Se lo sirvo aquí o se lo empaco?',
       u'To take away', u'para llevar',
       u'Para llevar, por favor.', u'To take away, please.',
       [u'para llevar', u'por favor'],
       [u'aquí', u'con ensalada', u'gracias', u'mañana'],
       [u'para llevar por favor', u'para llevar'],
       [u'para llevar'],
       u'Para llevar gets it in a bag with the salad in a bag of its own. Aquí gets you a plastic chair on the pavement, which is the better answer.'),
  beat(u'Se lo hago fresquito. Espéreme un poquito, pues.',
       u'Tell her you will wait', u'ya va',
       u'Ya va. Aquí espero.', u'Alright. I’ll wait here.',
       [u'ya va', u'aquí espero'],
       [u'para llevar', u'otro día', u'gracias', u'no'],
       [u'ya va aqui espero', u'ya va'],
       [u'ya va'],
       u'Ya va is the most useful two words in the country: coming right up, hang on, alright, I heard you. The tone does all the work.'),
 ]},
{
 'id': 'mercado-06', 'district': 'mercado', 'tier': 3,
 'who': u'El cargador', 'title': u'Las bolsas',
 'goal': u'Pay somebody to carry your shopping, agreed first',
 'culture': u'The cargadores carry loads on their backs and by handcart, and '
            u'it is a job like any other. Agreeing the price before he picks '
            u'anything up is the whole etiquette and it protects both of you '
            u'— afterwards it is an argument, beforehand it is a price.',
 'beats': [
  beat(u'¿Le ayudo con eso, jefe? Está pesado.',
       u'Yes — ask him to help', u'me ayuda',
       u'Sí, me ayuda, por favor.', u'Yes, give me a hand, please.',
       [u'sí', u'me ayuda', u'por favor'],
       [u'no gracias', u'hasta la esquina', u'ya tengo', u'otro día'],
       [u'si me ayuda por favor', u'me ayuda por favor', u'me ayuda'],
       [u'me ayuda'],
       u'Me ayuda asks for a hand rather than hiring a servant, which is how both of you want it framed.'),
  beat(u'¿Hasta dónde se lo llevo?',
       u'As far as the corner', u'hasta la esquina',
       u'Hasta la esquina.', u'As far as the corner.',
       [u'hasta la esquina'],
       [u'hasta el hotel', u'me ayuda', u'gracias', u'por favor'],
       [u'hasta la esquina', u'hasta la esquina por favor'],
       [u'hasta la esquina'],
       u'Distance here is corners and blocks. Nobody measures anything in metres and nobody uses a street name.'),
  beat(u'Va pues. Ahorita se lo dejo ahí.',
       u'Ask the price before he lifts it', u'¿cuánto me cobra?',
       u'¿Y cuánto me cobra?', u'And what will you charge me?',
       [u'¿y cuánto', u'me cobra?'],
       [u'gracias', u'está bien', u'otro día', u'por favor'],
       [u'y cuanto me cobra', u'cuanto me cobra'],
       [u'¿cuánto me cobra?'],
       u'Before he picks it up, every time. Ask afterwards and you are having an argument; ask now and you are agreeing a price.'),
  beat(u'Deme veinte pesos y estamos bien.',
       u'Agree, and shake on it', u'quedamos así',
       u'Quedamos así. Gracias.', u'Agreed. Thank you.',
       [u'quedamos así', u'gracias'],
       [u'muy caro', u'ni modo', u'otro día', u'por favor'],
       [u'quedamos asi gracias', u'quedamos asi'],
       [u'quedamos así'],
       u'Quedamos así seals it: we are agreed. It closes every small deal in this country and it is worth more than a handshake.'),
 ]},
{
 'id': 'mercado-07', 'district': 'mercado', 'tier': 3,
 'who': u'La de las tortillas', 'title': u'Las tortillas',
 'goal': u'Buy tortillas at the right hour, because later there are none',
 'culture': u'Tortillas are made in the morning and they run out. Turn up at '
            u'eleven and the answer is ya se acabaron, and the fix is not to '
            u'complain but to ask her to put some aside for you tomorrow.',
 'beats': [
  beat(u'Buenas.',
       u'Ask whether there are any left', u'¿todavía hay?',
       u'Buenas. ¿Todavía hay tortillas?', u'Hello. Are there still tortillas?',
       [u'Buenas', u'¿todavía hay', u'tortillas?'],
       [u'gracias', u'mañana', u'por favor', u'está bien'],
       [u'buenas todavia hay tortillas', u'todavia hay tortillas', u'todavia hay'],
       [u'¿todavía hay?'],
       u'¿Todavía hay? asks whether any are left, which is a different question from whether she sells them. Here it is the one that matters.'),
  beat(u'Uy, no. Ya se acabaron, mi amor. Desde las diez.',
       u'Say it back to be sure you understood', u'ya se acabaron',
       u'¿Ya se acabaron?', u'They’ve run out already?',
       [u'¿ya se acabaron?'],
       [u'mañana temprano', u'gracias', u'está bien', u'guárdeme'],
       [u'ya se acabaron'],
       [u'ya se acabaron'],
       u'Se acabaron — they are finished. Repeating it back as a question is how you check you heard it, and she will tell you when to come instead.'),
  beat(u'Sí pues. Venga mañana temprano, como a las seis.',
       u'Early tomorrow, then', u'mañana temprano',
       u'Mañana temprano, entonces.', u'Early tomorrow, then.',
       [u'mañana temprano', u'entonces'],
       [u'otro día', u'gracias', u'está bien', u'guárdeme'],
       [u'manana temprano entonces', u'manana temprano'],
       [u'mañana temprano'],
       u'Temprano at a tortillería means six. Anything in this market worth queueing for is gone by ten and nobody thinks that is early.'),
  beat(u'Ahí la espero, pues.',
       u'Ask her to put some aside', u'guárdeme',
       u'Guárdeme unas, por favor.', u'Keep me some, please.',
       [u'guárdeme', u'unas', u'por favor'],
       [u'mañana temprano', u'gracias', u'otro día', u'no'],
       [u'guardeme unas por favor', u'guardeme unas'],
       [u'guárdeme'],
       u'Guárdeme asks her to put some by for you, and asking is the whole difference between a customer and a regular.'),
 ]},
{
 'id': 'mercado-08', 'district': 'mercado', 'tier': 3,
 'who': u'El vendedor insistente', 'title': u'El insistente',
 'goal': u'Say no four times to somebody who ignores the first three',
 'culture': u'He is not being rude and neither are you. The escalation is the '
            u'ritual: nobody expects the first no to work, and four polite '
            u'ones are normal. Walking off in silence is the only move here '
            u'that actually reads as contempt.',
 'beats': [
  beat(u'¡Amigo! Hamacas, hamacas. Le hago precio especial.',
       u'No thank you', u'no gracias',
       u'No, gracias.', u'No, thank you.',
       [u'no', u'gracias'],
       [u'ya tengo', u'de verdad no', u'está bien', u'por favor'],
       [u'no gracias', u'gracias no'],
       [u'no gracias'],
       u'The first no, and nobody expects it to work — including him. It is not ignored so much as noted.'),
  beat(u'Mire nomás, sin compromiso. ¿De qué color la quiere?',
       u'Say you have one already', u'ya tengo',
       u'Ya tengo, gracias.', u'I’ve already got one, thanks.',
       [u'ya tengo', u'gracias'],
       [u'no', u'de verdad no', u'otro día', u'por favor'],
       [u'ya tengo gracias', u'ya tengo'],
       [u'ya tengo'],
       u'Ya tengo hands him a reason instead of a wall, and it works about half the time. It is the only one of the four that is a fact.'),
  beat(u'¿Y una para la esposa? ¿Para la mamá? Le dejo dos por el precio de una.',
       u'Really, no', u'de verdad no',
       u'De verdad no, gracias.', u'Really, no thank you.',
       [u'de verdad no', u'gracias'],
       [u'ya tengo', u'otro día', u'está bien', u'no'],
       [u'de verdad no gracias', u'de verdad no'],
       [u'de verdad no'],
       u'De verdad no is firm without being cross. Getting cross is what would be rude; a third no is not.'),
  beat(u'Bueno, bueno. Ahí cuando quiera, amigo.',
       u'Leave it well', u'que le vaya bien',
       u'Que le vaya bien.', u'All the best to you.',
       [u'que le vaya bien'],
       [u'ya tengo', u'de verdad no', u'gracias', u'otro día'],
       [u'que le vaya bien', u'que le vaya bien gracias'],
       [u'que le vaya bien'],
       u'Wishing him well on the way out is what turns four noes into a conversation. He will remember you kindly and try again tomorrow, and that is fine.'),
 ]},
{
 'id': 'mercado-09', 'district': 'mercado', 'tier': 4,
 'who': u'La de las hierbas', 'title': u'El remedio',
 'goal': u'Be sold a remedy for something you did not know you had',
 'culture': u'The herb stall is where a great many people get their medicine, '
            u'and a fair amount of it works. You are not being taken in. Say '
            u'which part of you hurts, take the instructions seriously, and '
            u'when she says no cuesta nada she is giving you something.',
 'beats': [
  beat(u'¿Qué anda buscando, mi hijo? Aquí hay para todo.',
       u'Something for your stomach', u'para el estómago',
       u'Algo para el estómago.', u'Something for my stomach.',
       [u'algo', u'para el estómago'],
       [u'para la gripe', u'gracias', u'por favor', u'no ando'],
       [u'algo para el estomago', u'para el estomago'],
       [u'para el estómago'],
       u'Name the part of you that hurts. That is the whole consultation, and she will put the plant for it in your hand.'),
  beat(u'Ah, eso es el hombre grande. Amarguísimo, pero le quita todo.',
       u'Ask how you take it', u'lo hierve',
       u'¿Lo hierve?', u'Do you boil it?',
       [u'¿lo hierve?'],
       [u'en ayunas', u'gracias', u'por favor', u'no ando'],
       [u'lo hierve'],
       [u'lo hierve'],
       u'Nearly everything on this stall is a tea, and asking is how you avoid a week of chewing bark. Hombre grande really is that bitter.'),
  beat(u'Lo hierve y se lo toma en ayunas, tres días.',
       u'Say it back so you have it', u'en ayunas',
       u'En ayunas. Tres días.', u'On an empty stomach. Three days.',
       [u'en ayunas', u'tres días'],
       [u'lo hierve', u'gracias', u'otro día', u'por favor'],
       [u'en ayunas tres dias', u'en ayunas'],
       [u'en ayunas'],
       u'En ayunas is before you have eaten anything at all. Repeating the instruction back matters more here than it does at a pharmacy, because there is no label.'),
  beat(u'Y llévese esta ramita también. No cuesta nada.',
       u'Check you heard that right', u'no cuesta nada',
       u'¿No cuesta nada?', u'It doesn’t cost anything?',
       [u'¿no cuesta nada?'],
       [u'gracias', u'muy amable', u'no ando', u'en ayunas'],
       [u'no cuesta nada', u'no cuesta nada gracias'],
       [u'no cuesta nada'],
       u'She is giving it to you. No cuesta nada ends the sale as a kindness, and the only right answer is to take it and say muy amable.'),
 ]},
{
 'id': 'mercado-10', 'district': 'mercado', 'tier': 4,
 'who': u'El pescadero', 'title': u'El pescado',
 'goal': u'Buy fish and be able to tell whether it is fresh',
 'culture': u'Guapote and mojarra come out of Cocibolca and they come in at '
            u'dawn. Asking whether it is from today is expected rather than '
            u'insulting, and he will tell you the truth, because you live '
            u'here now and he will see you next week.',
 'beats': [
  beat(u'Guapote, mojarra, tilapia. ¿Qué le gusta?',
       u'Ask if it is fresh', u'está fresco',
       u'¿Está fresco?', u'Is it fresh?',
       [u'¿está fresco?'],
       [u'de hoy', u'gracias', u'entero', u'por favor'],
       [u'esta fresco'],
       [u'está fresco'],
       u'Asking is expected. What would be strange, and what would mark you as somebody passing through, is not asking.'),
  beat(u'Fresquísimo. Mírele los ojos, mire.',
       u'Ask whether it came in today', u'de hoy',
       u'¿Es de hoy?', u'Did it come in today?',
       [u'¿es de hoy?'],
       [u'de ayer', u'está fresco', u'gracias', u'por favor'],
       [u'es de hoy', u'de hoy'],
       [u'de hoy'],
       u'Fresco is an opinion; de hoy is a fact. This is the question behind the question and he will answer it straight.'),
  beat(u'De hoy, de la madrugada. ¿Se lo limpio?',
       u'Yes, have him clean it', u'me lo limpia',
       u'Sí, me lo limpia, por favor.', u'Yes, clean it for me, please.',
       [u'sí', u'me lo limpia', u'por favor'],
       [u'no', u'entero', u'gracias', u'de hoy'],
       [u'si me lo limpia por favor', u'me lo limpia por favor', u'me lo limpia'],
       [u'me lo limpia'],
       u'He guts and scales it on the spot and does not charge for it. Saying no to that is a decision, not a saving.'),
  beat(u'¿Y se lo corto en filete?',
       u'Whole, please', u'entero',
       u'Entero, por favor.', u'Whole, please.',
       [u'entero', u'por favor'],
       [u'en filete', u'me lo limpia', u'gracias', u'de hoy'],
       [u'entero por favor', u'entero'],
       [u'entero'],
       u'Entero — whole. A guapote is fried whole here, head and all, and asking for fillets marks you out more than your accent does.'),
 ]},
{
 'id': 'mercado-11', 'district': 'mercado', 'tier': 4,
 'who': u'La comadre', 'title': u'La comadre',
 'goal': u'Be recognised, and become somebody who comes here',
 'culture': u'This is what all the other market missions were for. Going to '
            u'the same stall until she knows you is not a trick for better '
            u'prices — though it is that too. It is the difference between '
            u'shopping in a place and living in it.',
 'beats': [
  beat(u'¡Ideay! Usted otra vez. Ya lo conozco a usted.',
       u'Tell her you know your way around now', u'ya lo conozco',
       u'Ya lo conozco todo aquí.', u'I know my way around here now.',
       [u'ya lo conozco', u'todo aquí'],
       [u'otro día', u'no ando', u'gracias', u'así es'],
       [u'ya lo conozco todo aqui', u'ya lo conozco'],
       [u'ya lo conozco'],
       u'Ideay is the most Nicaraguan noise there is — surprise, greeting, disbelief, all of it. Ya lo conozco claims the place a little, and she will let you.'),
  beat(u'Le guardé los mejores, mire. Desde temprano se los aparté.',
       u'She put them aside for you — check', u'le guardé',
       u'¿Me los guardó? Muy amable.', u'You kept them for me? That’s very kind.',
       [u'¿me los guardó?', u'muy amable'],
       [u'gracias', u'otro día', u'no ando', u'así es'],
       [u'me los guardo muy amable', u'me los guardo'],
       [u'le guardé', u'muy amable'],
       u'Le guardé from her, me los guardó from you: the same act from the two ends of it. Hearing one and being able to say the other is most of what fluency is.'),
  beat(u'¿Y qué va a llevar hoy?',
       u'The usual', u'lo de siempre',
       u'Lo de siempre, pues.', u'The usual, then.',
       [u'lo de siempre', u'pues'],
       [u'una libra', u'otro día', u'gracias', u'así es'],
       [u'lo de siempre pues', u'lo de siempre'],
       [u'lo de siempre'],
       u'This is the sentence you have been working towards since your first morning here. It means she knows what you buy, and you only get it by coming back.'),
  beat(u'¿Se los doy bien maduros, como la vez pasada?',
       u'Yes — that is how you like them', u'así me gusta',
       u'Así me gusta. Gracias.', u'That’s how I like them. Thank you.',
       [u'así me gusta', u'gracias'],
       [u'no', u'otro día', u'por favor', u'lo de siempre'],
       [u'asi me gusta gracias', u'asi me gusta'],
       [u'así me gusta'],
       u'She asked because she remembered. Answering it is the entire point of going to the same stall, and it is worth more than the córdobas it saves.'),
 ]},
{
 'id': 'mercado-12', 'district': 'mercado', 'tier': 5,
 'who': u'El regateador', 'title': u'El regateo',
 'goal': u'Haggle properly, which is neither arguing nor accepting',
 'culture': u'Haggling has a shape: ask, be told, counter once, meet in the '
            u'middle, close, and never reopen it. Grinding somebody down is '
            u'not winning and paying the first number is not manners — the '
            u'ritual is the point, and both of you are meant to enjoy it.',
 'beats': [
  beat(u'Ese bolso de cuero le sale en mil quinientos. De Masaya, hecho a mano.',
       u'Counter, once', u'me lo deja en',
       u'¿Me lo deja en mil?', u'Would you let me have it for a thousand?',
       [u'¿me lo deja en', u'mil?'],
       [u'está caro', u'ni modo', u'gracias', u'trato hecho'],
       [u'me lo deja en mil'],
       [u'me lo deja en'],
       u'One counter, said as a question. Me lo deja en... is not an argument — it is the next line of a script you are both reading from.'),
  beat(u'¿Mil? Uy, no. En mil doscientos, y le juro que no gano nada.',
       u'Split it — say it suits neither of you', u'ni para usted ni para mí',
       u'Mil cien. Ni para usted ni para mí.', u'Eleven hundred. Good for neither of us.',
       [u'mil cien', u'ni para usted ni para mí'],
       [u'mil quinientos', u'está caro', u'gracias', u'trato hecho'],
       [u'mil cien ni para usted ni para mi', u'ni para usted ni para mi'],
       [u'ni para usted ni para mí'],
       u'Ni para usted ni para mí closes the gap by making the split the fair thing rather than the concession. It lets him agree without losing.'),
  beat(u'Ay, hombre. Mil ciento cincuenta y se lo llevo hasta la esquina.',
       u'Hold where you are', u'ya pues',
       u'Ya pues, mil cien.', u'Come on now, eleven hundred.',
       [u'ya pues', u'mil cien'],
       [u'mil quinientos', u'trato hecho', u'gracias', u'está caro'],
       [u'ya pues mil cien', u'ya pues'],
       [u'ya pues'],
       u'Ya pues is come on, alright, enough — a nudge and not a demand. Said with a smile it ends the haggling your way and costs him nothing he minds.'),
  beat(u'¡Bueno! Mil cien pues. Se lo dejo porque usted me cae bien.',
       u'Close it', u'trato hecho',
       u'Trato hecho. Gracias.', u'Done deal. Thank you.',
       [u'trato hecho', u'gracias'],
       [u'ya pues', u'está caro', u'otro día', u'por favor'],
       [u'trato hecho gracias', u'trato hecho'],
       [u'trato hecho'],
       u'Trato hecho — done. Say it, pay it, and never go back to the price: reopening a closed deal is the one genuinely rude move in the whole exchange.'),
 ]},
]

# The crowd of El Mercado. Louder and more specific than El Centro's, because
# in a market being pointed at the right stall IS the direction.
HINTS = [
 {'kind': u'caponero', 'district': 'mercado',
  'says': u'¿Va al mercado? La fruta está más barata al fondo, donde la verdulera.',
  'en': u'Going to the market? The fruit is cheaper at the back, at the vegetable woman’s stall.',
  'points_at': ['mercado-01']},
 {'kind': u'vendedora', 'district': 'mercado',
  'says': u'Si anda dólares, cámbielos con el muchacho de la esquina. Ese le da mejor que el banco.',
  'en': u'If you have dollars, change them with the lad on the corner. He gives you better than the bank.',
  'points_at': ['mercado-02']},
 {'kind': u'policía', 'district': 'mercado',
  'says': u'Aquí es tranquilo, pero cuide la bolsa. Y no cambie dinero con cualquiera.',
  'en': u'It is quiet here, but mind your bag. And do not change money with just anybody.',
  'points_at': ['mercado-02']},
 {'kind': u'doña en la puerta', 'district': 'mercado',
  'says': u'La carnicería está entrando a mano derecha. Dígale qué va a cocinar y ella le corta.',
  'en': u'The butcher is on the right as you go in. Tell her what you are cooking and she cuts it for you.',
  'points_at': ['mercado-03']},
 {'kind': u'obrero', 'district': 'mercado',
  'says': u'Los frijoles cómprelos por libra donde el de los granos. Y pregúntele cómo se hacen.',
  'en': u'Buy the beans by the pound at the grain seller. And ask him how they are cooked.',
  'points_at': ['mercado-04']},
 {'kind': u'chavalo en bici', 'district': 'mercado',
  'says': u'De noche ponen la fritanga en la esquina. El enchilado de esa doña es el mejor.',
  'en': u'At night they set the fritanga up on the corner. That lady’s enchilado is the best there is.',
  'points_at': ['mercado-05']},
 {'kind': u'cuidacarros', 'district': 'mercado',
  'says': u'Si lleva mucha bolsa, ahí andan los cargadores. Arregle el precio antes, jefe.',
  'en': u'If you are carrying a lot of bags, the porters are about. Agree the price first, boss.',
  'points_at': ['mercado-06']},
 {'kind': u'doña en la puerta', 'district': 'mercado',
  'says': u'Las tortillas se acaban temprano. Si va después de las diez, ya no hay.',
  'en': u'The tortillas run out early. If you go after ten, there are none left.',
  'points_at': ['mercado-07']},
 {'kind': u'viejo de la esquina', 'district': 'mercado',
  'says': u'Al de las hamacas no le diga que sí por lástima. Dígale que no cuatro veces y ya.',
  'en': u'Do not say yes to the hammock man out of pity. Tell him no four times and that is that.',
  'points_at': ['mercado-08']},
 {'kind': u'evangélico', 'district': 'mercado',
  'says': u'¿Anda malo del estómago, hermano? La señora de las hierbas, al fondo. Le da el remedio.',
  'en': u'Is your stomach bad, brother? The herb lady, at the back. She will give you the remedy.',
  'points_at': ['mercado-09']},
 {'kind': u'caponero', 'district': 'mercado',
  'says': u'El pescado del lago lo venden en la mañana. Pregunte si es de hoy, no tenga pena.',
  'en': u'They sell the lake fish in the morning. Ask if it came in today, do not be shy.',
  'points_at': ['mercado-10']},
 {'kind': u'vendedora', 'district': 'mercado',
  'says': u'Vaya siempre donde la misma. A los tres días ya le guarda lo mejor.',
  'en': u'Always go to the same woman. Within three days she is keeping the best for you.',
  'points_at': ['mercado-11']},
 {'kind': u'chavalo en bici', 'district': 'mercado',
  'says': u'El de los bolsos de cuero pide el doble. Ofrezca la mitad y quédense en medio.',
  'en': u'The leather bag man asks double. Offer half and settle in the middle.',
  'points_at': ['mercado-12']},
 {'kind': u'turista', 'district': 'mercado',
  'says': u'Do they take dollars here? Everyone keeps saying a number and I can’t tell if it’s good.',
  'en': u'(She wants the money changer, and she is about to accept a terrible rate.)',
  'points_at': ['mercado-02', 'mercado-12']},
]

# ---------------------------------------------------------------- write

for m in MISSIONS:
    with io.open(os.path.join(GAME, m['id'] + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(m, ensure_ascii=False, indent=1) + u'\n')

crowd_path = os.path.join(CROWD, 'mercado.json')
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
    if m['id'] not in planned:
        bad.append(u'%s is not on the spine' % m['id'])
        continue
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
            bad.append(u'%s has only %d distractors' % (w, len(b['extra'])))
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
