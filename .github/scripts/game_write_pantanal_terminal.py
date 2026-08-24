# -*- coding: utf-8 -*-
"""Writes Pantanal and La Terminal -- twenty missions.

Pantanal is the lakeside barrio, poorer and wetter, and it is where the game
stops being about buying things. Half of these have nothing to transact: a
flooded house, a roof, a man who went south for work and came back with
nothing, a woman who was nineteen in Managua in 1972. The Spanish is easier
than El Mercado's and the missions are harder, which is the right way round.

La Terminal is buses. Six of these happen at or on a vehicle, which is what
the vehicle hook in game_bake.py is for.

A note on the two that could go wrong. pantanal-05 is a barefoot child asking
for money and pantanal-08 is a curandera treating you for something you do not
believe in; both are written as they actually happen and neither is played for
pity or for laughs. The culture note carries the weight in both.

Same self-checks as every other batch.
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
# ── Pantanal ────────────────────────────────────────────────────────────
{
 'id': 'pantanal-01', 'district': 'pantanal', 'tier': 2,
 'who': u'El pescador', 'title': u'La lancha',
 'goal': u'Get taken out on the lake by somebody who works it',
 'culture': u'The isletas are three hundred and sixty-odd islands left by '
            u'Mombacho falling into the lake. The tour boats leave from the '
            u'Centro Turístico and charge in dollars; a fisherman at the '
            u'shore will take you for córdobas and show you where he actually '
            u'works. Agree the return before you go, or you will be '
            u'negotiating it standing on an island.',
 'beats': [
  beat(u'Buenas. ¿Anda viendo las isletas?',
       u'Ask him to take you out', u'me lleva',
       u'¿Me lleva a las isletas?', u'Would you take me out to the isletas?',
       [u'¿me lleva', u'a las isletas?'],
       [u'una hora', u'ida y vuelta', u'gracias', u'temprano'],
       [u'me lleva a las isletas', u'me lleva'],
       [u'me lleva'],
       u'Me lleva asks for the ride. He is not a tour operator and there is no ticket — there is a boat, a price and the two of you.'),
  beat(u'Puedo. ¿Por cuánto tiempo quiere andar?',
       u'An hour', u'una hora',
       u'Una hora está bien.', u'An hour would be fine.',
       [u'una hora', u'está bien'],
       [u'ida y vuelta', u'temprano', u'gracias', u'ni modo'],
       [u'una hora esta bien', u'una hora'],
       [u'una hora'],
       u'An hour gets you round the near islands and back. Settle the time before the price and the price will make sense.'),
  beat(u'Va. ¿Y lo dejo allá o lo traigo de vuelta?',
       u'There and back', u'ida y vuelta',
       u'Ida y vuelta, por favor.', u'There and back, please.',
       [u'ida y vuelta', u'por favor'],
       [u'solo ida', u'una hora', u'gracias', u'temprano'],
       [u'ida y vuelta por favor', u'ida y vuelta'],
       [u'ida y vuelta'],
       u'Ida y vuelta — out and back. Agree it now. Agreeing it later means agreeing it while standing on an island.'),
  beat(u'¿Y a qué hora salimos, pues?',
       u'Early', u'temprano',
       u'Temprano. A las seis.', u'Early. Six o’clock.',
       [u'temprano', u'a las seis'],
       [u'a las doce', u'ida y vuelta', u'gracias', u'ni modo'],
       [u'temprano a las seis', u'temprano'],
       [u'temprano'],
       u'Temprano, before the wind gets up on the lake in the afternoon. He will be there at six and so should you.'),
 ]},
{
 'id': 'pantanal-02', 'district': 'pantanal', 'tier': 2,
 'who': u'La lavandera', 'title': u'El lavado',
 'goal': u'Get your washing done and agree a day',
 'culture': u'She washes by hand at a pila for a small weekly sum, and it is '
            u'real work. Name the day, ask what it comes to, pay it and do '
            u'not haggle — this is the one price in Granada that nobody who '
            u'lives here would try to push down.',
 'beats': [
  beat(u'Buenas, vecino. ¿Qué se le ofrece?',
       u'Ask her to wash these clothes', u'lavar esta ropa',
       u'¿Me puede lavar esta ropa?', u'Could you wash these clothes for me?',
       [u'¿me puede', u'lavar esta ropa?'],
       [u'para el viernes', u'¿cuánto sale?', u'gracias', u'con permiso'],
       [u'me puede lavar esta ropa', u'lavar esta ropa'],
       [u'lavar esta ropa'],
       u'Said with the bag held up. She will want to see what it is before she says yes, and that is not suspicion, it is arithmetic.'),
  beat(u'Claro que sí. ¿Para cuándo la ocupa?',
       u'For Friday', u'para el viernes',
       u'Para el viernes.', u'For Friday.',
       [u'para el viernes'],
       [u'para mañana', u'sin apuro', u'gracias', u'así es'],
       [u'para el viernes'],
       [u'para el viernes'],
       u'Ocupar is to need here, not to occupy — ¿la ocupa? is do you need it. Naming the day is the whole arrangement.'),
  beat(u'Va pues, para el viernes se la tengo.',
       u'Ask what it comes to', u'¿cuánto sale?',
       u'¿Y cuánto sale?', u'And what does it come to?',
       [u'¿y cuánto', u'sale?'],
       [u'gracias', u'sin apuro', u'con permiso', u'así es'],
       [u'y cuanto sale', u'cuanto sale'],
       [u'¿cuánto sale?'],
       u'¿Cuánto sale? asks the total. Ask it, pay it, and do not haggle: this is hand-washing and the price is already low.'),
  beat(u'Doscientos. Y si me atraso un día, fíjese que a veces llueve.',
       u'Tell her there is no rush', u'sin apuro',
       u'Está bien. Sin apuro.', u'That’s fine. No rush.',
       [u'está bien', u'sin apuro'],
       [u'para el viernes', u'gracias', u'así es', u'con permiso'],
       [u'esta bien sin apuro', u'sin apuro'],
       [u'sin apuro'],
       u'Everything dries outside, so rain is a real reason. Sin apuro costs you nothing and she will remember which neighbour said it.'),
 ]},
{
 'id': 'pantanal-03', 'district': 'pantanal', 'tier': 3,
 'who': u'El del agua', 'title': u'No hay agua',
 'goal': u'Find out when the water is coming back',
 'culture': u'The mains go off down here for days at a time and everybody '
            u'stores water in barrels. Nobody announces anything, so the '
            u'neighbour who listens to the pipes IS the information system. '
            u'Getting yourself onto that list is what this mission is for.',
 'beats': [
  beat(u'¿Y usted también anda sin agua?',
       u'Say there is none at your house', u'no hay agua',
       u'No hay agua en mi casa.', u'There’s no water at my house.',
       [u'no hay agua', u'en mi casa'],
       [u'desde el martes', u'¿cuándo viene?', u'gracias', u'ya va'],
       [u'no hay agua en mi casa', u'no hay agua'],
       [u'no hay agua'],
       u'No hay agua is a sentence you will say and hear constantly down here. It is not a complaint, it is the weather report.'),
  beat(u'Aquí tampoco. Desde el martes, fíjese.',
       u'Since Tuesday?', u'desde el martes',
       u'¿Desde el martes?', u'Since Tuesday?',
       [u'¿desde el martes?'],
       [u'no hay agua', u'¿cuándo viene?', u'gracias', u'cuídese'],
       [u'desde el martes'],
       [u'desde el martes'],
       u'Three days already. Repeating the day back is how you find out whether this is bad or normal, and down here it is normal.'),
  beat(u'Desde el martes, sí. Yo tengo dos barriles llenos, gracias a Dios.',
       u'Ask when it is coming back', u'¿cuándo viene?',
       u'¿Y cuándo viene?', u'And when is it coming back?',
       [u'¿y cuándo', u'viene?'],
       [u'no hay agua', u'gracias', u'ya va', u'cuídese'],
       [u'y cuando viene', u'cuando viene'],
       [u'¿cuándo viene?'],
       u'Nobody from the company will tell you, so asking a neighbour is not a workaround — it is the system, and he will know before they do.'),
  beat(u'Quién sabe. Pero yo oigo el ruido en los tubos y aviso a todos.',
       u'Ask him to let you know', u'avíseme',
       u'Avíseme, por favor.', u'Let me know, please.',
       [u'avíseme', u'por favor'],
       [u'gracias', u'ya va', u'no ando', u'cuídese'],
       [u'aviseme por favor', u'aviseme'],
       [u'avíseme'],
       u'Avíseme — let me know. Asking to be told is how you get plugged into a barrio that runs entirely on being told things.'),
 ]},
{
 'id': 'pantanal-04', 'district': 'pantanal', 'tier': 3,
 'who': u'La señora del fogón', 'title': u'La leña',
 'goal': u'Buy firewood and carry it further than you expected',
 'culture': u'A great many kitchens here still cook on wood, and wood is sold '
            u'by the tercio — a bundle, never weighed. Green wood smokes and '
            u'will not light, so asking for seca is the entire skill, and '
            u'delivery means as far as the corner.',
 'beats': [
  beat(u'¿Qué anda buscando, joven?',
       u'A bundle of firewood', u'un tercio',
       u'Un tercio de leña.', u'A bundle of firewood.',
       [u'un tercio', u'de leña'],
       [u'seca', u'gracias', u'otro día', u'¿a cómo?'],
       [u'un tercio de lena', u'un tercio'],
       [u'un tercio', u'de leña'],
       u'Un tercio is the bundle firewood comes in. Nobody weighs it and nobody ever has.'),
  beat(u'¿Y para qué la quiere? ¿Para cocinar?',
       u'Yes — and ask for dry', u'seca',
       u'Sí. Que sea seca.', u'Yes. Dry, if you have it.',
       [u'sí', u'que sea seca'],
       [u'verde', u'un tercio', u'gracias', u'otro día'],
       [u'si que sea seca', u'que sea seca'],
       [u'seca'],
       u'Seca — dry. Green wood smokes, will not catch, and is exactly what you get if you do not ask for the other kind.'),
  beat(u'Toda mi leña es seca, mire, tóquela.',
       u'Ask the price', u'¿a cómo?',
       u'¿A cómo el tercio?', u'How much is the bundle?',
       [u'¿a cómo', u'el tercio?'],
       [u'seca', u'de leña', u'gracias', u'otro día'],
       [u'a como el tercio', u'a como'],
       [u'¿a cómo?'],
       u'The same three words you used on the mango and the hammock. ¿A cómo? works on everything sold in this country.'),
  beat(u'Cincuenta. Yo se lo llevo hasta la esquina y ahí se lo dejo.',
       u'So you carry it from the corner', u'ahí se la dejo',
       u'¿Ahí me lo deja?', u'You’ll leave it there for me?',
       [u'¿ahí me lo deja?'],
       [u'un tercio', u'seca', u'gracias', u'otro día'],
       [u'ahi me lo deja'],
       [u'ahí se la dejo'],
       u'Ahí se lo dejo from her, ahí me lo deja from you. She carries it to the corner and the rest is yours, which is further than it sounds with fifty pounds of wood.'),
 ]},
{
 'id': 'pantanal-05', 'district': 'pantanal', 'tier': 3,
 'who': u'El chavalo descalzo', 'title': u'El chavalo',
 'goal': u'Be asked for money by a kid, and work out what you think',
 'culture': u'Handing cash to a child is complicated here — it can keep him '
            u'out of school and there is often somebody older collecting it. '
            u'Buying him something to eat is unambiguous, ordinary, and '
            u'nobody will look at you twice for doing it. He gets VOS, '
            u'because he is a child, and getting that right matters more than '
            u'the money does.',
 'beats': [
  beat(u'Regáleme diez pesos, chele. Para comer.',
       u'Say you have not got it', u'no tengo',
       u'No tengo, chavalo.', u'I haven’t got it, kid.',
       [u'no tengo', u'chavalo'],
       [u'te compro algo', u'¿comiste?', u'gracias', u'por favor'],
       [u'no tengo chavalo', u'no tengo'],
       [u'no tengo'],
       u'The plain truth, said to him rather than past him. Chavalo on the end is friendly — it is what everybody calls him.'),
  beat(u'Ideay. Aunque sea cinco, chele.',
       u'Offer to buy him food instead', u'te compro algo',
       u'Te compro algo de comer.', u'I’ll buy you something to eat.',
       [u'te compro algo', u'de comer'],
       [u'no tengo', u'¿comiste?', u'gracias', u'por favor'],
       [u'te compro algo de comer', u'te compro algo'],
       [u'te compro algo'],
       u'TE compro — vos, because he is a child. Food instead of cash is the ordinary thing to do here and nobody will think it mean.'),
  beat(u'¿De verdad? Va pues, chele.',
       u'Ask whether he has eaten today', u'¿comiste?',
       u'¿Comiste hoy?', u'Have you eaten today?',
       [u'¿comiste', u'hoy?'],
       [u'te compro algo', u'no tengo', u'gracias', u'por favor'],
       [u'comiste hoy', u'comiste'],
       [u'¿comiste?'],
       u'¿Comiste? is spelled the same in vos and in tú, which is why it slips past learners. Asking is not charity; it is what any adult here would ask him.'),
  beat(u'Hoy no todavía. Gracias, chele.',
       u'Send him off', u'andá con cuidado',
       u'Andá con cuidado.', u'Mind how you go.',
       [u'andá con cuidado'],
       [u'cuídese', u'gracias', u'por favor', u'no tengo'],
       [u'anda con cuidado'],
       [u'andá con cuidado'],
       u'Andá, not vaya. He is nine and he gets vos — cuídese to a child would be as odd as calling him sir.'),
 ]},
{
 'id': 'pantanal-06', 'district': 'pantanal', 'tier': 4,
 'who': u'Doña Julia', 'title': u'La inundación',
 'goal': u'Help bail out a house after the rain and be fed for it',
 'culture': u'When it rains hard the water comes into the houses down here, '
            u'and helping bail is what a neighbour does rather than a '
            u'kindness worth mentioning. Being fed for it is not optional: '
            u'refusing the food is the insult, not the eating.',
 'beats': [
  beat(u'¡Ay, vecino! Mire cómo quedó esto.',
       u'Ask whether the water got in', u'se metió el agua',
       u'¿Se metió el agua?', u'Did the water get in?',
       [u'¿se metió el agua?'],
       [u'toda la noche', u'échele', u'gracias', u'está bien'],
       [u'se metio el agua'],
       [u'se metió el agua'],
       u'Se metió el agua — the water got in. It is the sentence of the whole rainy season in this barrio.'),
  beat(u'Toda la noche estuvo entrando. Desde las dos.',
       u'All night — say it back', u'toda la noche',
       u'¿Toda la noche?', u'All night?',
       [u'¿toda la noche?'],
       [u'se metió el agua', u'échele', u'gracias', u'me da'],
       [u'toda la noche'],
       [u'toda la noche'],
       u'Saying it back is doing something. She has been awake with a bucket since two and somebody noticing is not nothing.'),
  beat(u'Agarre esa cubeta, vecino. Échele para afuera.',
       u'Get on with it, and say so', u'échele',
       u'Échele, pues. Yo le ayudo.', u'Keep at it. I’ll give you a hand.',
       [u'échele', u'yo le ayudo'],
       [u'toda la noche', u'se metió el agua', u'gracias', u'está bien'],
       [u'echele yo le ayudo', u'yo le ayudo'],
       [u'échele'],
       u'Échele is go on, keep at it, throw it out. It is a verb of encouragement that means almost anything, and here it means both of you keep bailing.'),
  beat(u'Ya, ya. Siéntese. Coma algo, aunque sea un poquito.',
       u'Accept — and turn it round on her', u'coma algo',
       u'Coma algo usted también, doña.', u'You eat something too, doña.',
       [u'coma algo', u'usted también', u'doña'],
       [u'gracias', u'está bien', u'me da', u'no'],
       [u'coma algo usted tambien dona', u'coma algo usted tambien'],
       [u'coma algo'],
       u'She will feed you for helping and refusing is the insult. Telling her to eat too is the right answer, because she has not since it started.'),
 ]},
{
 'id': 'pantanal-07', 'district': 'pantanal', 'tier': 4,
 'who': u'El albañil', 'title': u'El techo',
 'goal': u'Help patch a roof with a man who explains nothing',
 'culture': u'He does not explain because the job explains itself and because '
            u'he is on a roof. Every line he says to you is an imperative, '
            u'and your whole part is understanding them fast and saying so. '
            u'This is the listening mission of the district.',
 'beats': [
  beat(u'¿Me ayuda tantito, joven? Súbase, pues.',
       u'Check he means you should come up', u'súbase',
       u'¿Que me suba?', u'You want me to come up?',
       [u'¿que me suba?'],
       [u'páseme', u'aquí', u'quieto', u'con permiso'],
       [u'que me suba'],
       [u'súbase'],
       u'Súbase from him, que me suba from you. Repeating an instruction back as a question is how you work with somebody who explains nothing.'),
  beat(u'Sí pues. Ahora páseme esa lámina.',
       u'This one — and say it is coming', u'páseme',
       u'¿Esta? Ya se la paso.', u'This one? Coming up.',
       [u'¿esta?', u'ya se la paso'],
       [u'páseme', u'quieto', u'aquí', u'así es'],
       [u'esta ya se la paso', u'ya se la paso'],
       [u'páseme'],
       u'Páseme — pass me. Ya se la paso is the answer, and ya does the whole tense on its own: I am doing it now.'),
  beat(u'Póngala aquí. Aquí, aquí.',
       u'One word, with your hand on the spot', u'aquí',
       u'¿Aquí?', u'Here?',
       [u'¿aquí?'],
       [u'páseme', u'quieto', u'allá', u'así es'],
       [u'aqui'],
       [u'aquí'],
       u'One word said as a question, with your hand where you think he means. On a roof that is worth more than a sentence.'),
  beat(u'Ahí. Quieto, quieto... ya. Ya quedó.',
       u'Tell him you have it', u'quieto',
       u'Quieto. Ya lo tengo.', u'Holding. I’ve got it.',
       [u'quieto', u'ya lo tengo'],
       [u'páseme', u'aquí', u'con permiso', u'ni modo'],
       [u'quieto ya lo tengo', u'ya lo tengo'],
       [u'quieto'],
       u'Quieto is hold still and there is nothing rude in it. Ya lo tengo is the only thing he needs to hear, because it means he can let go.'),
 ]},
{
 'id': 'pantanal-08', 'district': 'pantanal', 'tier': 4,
 'who': u'La curandera', 'title': u'El mal de ojo',
 'goal': u'Be treated for something you do not believe in',
 'culture': u'Mal de ojo is taken seriously by a great many people here, and '
            u'the egg is a real, common remedy done for fussing babies all '
            u'over the country. You are not obliged to believe any of it. You '
            u'are obliged not to laugh, and that is the whole difference '
            u'between a guest and a tourist.',
 'beats': [
  beat(u'Usted anda ojeado, mi hijo. Se le ve en la cara.',
       u'Ask what she means', u'le hicieron ojo',
       u'¿Me hicieron ojo?', u'Someone gave me the evil eye?',
       [u'¿me hicieron ojo?'],
       [u'un huevo', u'no se ría', u'gracias', u'no ando'],
       [u'me hicieron ojo'],
       [u'le hicieron ojo'],
       u'Le hicieron ojo from her, me hicieron ojo from you. Somebody looked at you with envy, is the idea, and it is not a small matter to her.'),
  beat(u'Se lo quito con un huevo. Aquí mismo, no se mueva.',
       u'An egg?', u'un huevo',
       u'¿Con un huevo?', u'With an egg?',
       [u'¿con un huevo?'],
       [u'le hicieron ojo', u'no se ría', u'gracias', u'ya verá'],
       [u'con un huevo'],
       [u'un huevo'],
       u'A raw egg passed over you and then broken into a glass of water. It is done for babies who will not settle, everywhere, and it is not a trick got up for foreigners.'),
  beat(u'No se ría. Se lo digo en serio, mi hijo.',
       u'Tell her you are not laughing', u'no se ría',
       u'No me río. En serio.', u'I’m not laughing. Honestly.',
       [u'no me río', u'en serio'],
       [u'no se ría', u'gracias', u'cuídese', u'ya verá'],
       [u'no me rio en serio', u'no me rio'],
       [u'no se ría'],
       u'You do not have to believe it. You do have to not laugh at it, and she asked because plenty of people have.'),
  beat(u'Ya verá que amanece mejor mañana.',
       u'Leave it open', u'ya verá',
       u'Ya veré. Gracias, doña.', u'We’ll see. Thank you, doña.',
       [u'ya veré', u'gracias', u'doña'],
       [u'no me río', u'ya verá', u'cuídese', u'no ando'],
       [u'ya vere gracias dona', u'ya vere'],
       [u'ya verá'],
       u'Ya verá — you will see. Answering ya veré is neither agreeing nor arguing, and it is exactly the right amount of commitment to make.'),
 ]},
{
 'id': 'pantanal-09', 'district': 'pantanal', 'tier': 5,
 'who': u'El que volvió', 'title': u'El que volvió',
 'goal': u'Talk to a man who went south for work and came back with nothing',
 'culture': u'Half this barrio has somebody in Costa Rica or Panama. Some '
            u'came back with a house and some came back with nothing, and he '
            u'is neither a success story nor a warning — he made a decision, '
            u'it went how it went, and he would like to tell somebody about '
            u'it without being pitied for it.',
 'beats': [
  beat(u'Yo estuve fuera, ¿sabe? Cinco años estuve.',
       u'Ask where he went', u'me fui',
       u'¿A dónde se fue?', u'Where did you go?',
       [u'¿a dónde', u'se fue?'],
       [u'allá', u'no es como dicen', u'gracias', u'ya va'],
       [u'a donde se fue', u'a donde'],
       [u'me fui'],
       u'He will answer me fui a Costa Rica. Se fue from you, me fui from him — the same trip from the two ends of it, which is the pattern this whole game runs on.'),
  beat(u'Me fui a Costa Rica. A cortar café primero, después construcción.',
       u'Ask what it was like there', u'allá',
       u'¿Y cómo era allá?', u'And what was it like over there?',
       [u'¿y cómo era', u'allá?'],
       [u'me fui', u'aquí estoy mejor', u'gracias', u'¿a cómo?'],
       [u'y como era alla', u'como era alla'],
       [u'allá'],
       u'Allá is over there, wherever there is. In this barrio it means Costa Rica or Panama and nobody has to say which.'),
  beat(u'Uy. No es como dicen, le voy a ser sincero.',
       u'Ask him what he means', u'no es como dicen',
       u'¿No es como dicen?', u'It isn’t how they say?',
       [u'¿no es como dicen?'],
       [u'allá', u'aquí estoy mejor', u'gracias', u'ya va'],
       [u'no es como dicen'],
       [u'no es como dicen'],
       u'No es como dicen — it is not how they tell it. He is not warning you off; he is correcting a story the whole street believes.'),
  beat(u'Trabajé bien duro cinco años y volví igual que me fui. Pero aquí estoy mejor.',
       u'Take him at his word', u'aquí estoy mejor',
       u'Aquí está mejor, entonces.', u'You’re better off here, then.',
       [u'aquí está mejor', u'entonces'],
       [u'aquí estoy mejor', u'allá', u'gracias', u'que le vaya bien'],
       [u'aqui esta mejor entonces', u'aqui esta mejor'],
       [u'aquí estoy mejor'],
       u'Agreement, not sympathy. He did not tell you this to be pitied and aquí estoy mejor is the sentence he came home with — he means it.'),
 ]},
{
 'id': 'pantanal-10', 'district': 'pantanal', 'tier': 5,
 'who': u'La abuela', 'title': u'El terremoto',
 'goal': u'Hear about 1972 from somebody who was in it',
 'culture': u'The Managua earthquake struck two days before Christmas in '
            u'1972, killed something like ten thousand people and flattened '
            u'the centre of the capital, which was never rebuilt. Anybody '
            u'over sixty in this country has a version of that night. This '
            u'mission is four questions and then listening; there is nothing '
            u'to say at the end except that you heard her.',
 'beats': [
  beat(u'Buenas, mi hijo. ¿Usted es el que anda preguntando cosas viejas?',
       u'Ask how old she was in ’72', u'yo tenía',
       u'¿Cuántos años tenía usted en el setenta y dos?', u'How old were you in ’72?',
       [u'¿cuántos años tenía usted', u'en el setenta y dos?'],
       [u'esa noche', u'no lo olvido', u'gracias', u'otro día'],
       [u'cuantos anos tenia usted en el setenta y dos',
        u'cuantos anos tenia usted'],
       [u'yo tenía'],
       u'She will answer yo tenía diecinueve. Tenía is the tense for how things were, and this entire conversation happens in it.'),
  beat(u'Yo tenía diecinueve. Estaba en Managua, en casa de mi tía.',
       u'Ask about that night', u'esa noche',
       u'¿Y esa noche?', u'And that night?',
       [u'¿y esa noche?'],
       [u'yo tenía', u'se cayó todo', u'gracias', u'por favor'],
       [u'y esa noche', u'esa noche'],
       [u'esa noche'],
       u'Esa noche — that night. You do not have to name the earthquake and she will not need you to.'),
  beat(u'Esa noche se cayó todo. Todo, mi hijo. A las doce y media de la noche.',
       u'Say it back', u'se cayó todo',
       u'¿Se cayó todo?', u'Everything came down?',
       [u'¿se cayó todo?'],
       [u'esa noche', u'no lo olvido', u'gracias', u'otro día'],
       [u'se cayo todo'],
       [u'se cayó todo'],
       u'Ten thousand people, two days before Christmas, and the centre of Managua still has holes in it. Se cayó todo is not an exaggeration.'),
  beat(u'Todo. Yo no lo olvido. Nunca lo he olvidado.',
       u'Say the small right thing', u'no lo olvido',
       u'No lo olvida usted. Gracias por contarme.', u'You don’t forget it. Thank you for telling me.',
       [u'no lo olvida usted', u'gracias por contarme'],
       [u'no lo olvido', u'esa noche', u'otro día', u'por favor'],
       [u'no lo olvida usted gracias por contarme', u'gracias por contarme'],
       [u'no lo olvido'],
       u'There is nothing to say to this and you should not reach for something. Her own words back, and thanks for the telling, is the whole of your part.'),
 ]},
# ── La Terminal ─────────────────────────────────────────────────────────
{
 'id': 'terminal-01', 'district': 'terminal', 'tier': 1,
 'who': u'El cobrador', 'title': u'La ruta',
 'goal': u'Take a bus without ending up somewhere else',
 'culture': u'The cobrador hangs out of the door shouting the destination and '
            u'he is the one you pay, not the driver. There are no printed '
            u'stops: you tell him where you are getting off and he remembers, '
            u'and you shout before you get there or you see the next town.',
 'beats': [
  beat(u'¡Managua, Managua! ¡Masaya, Masaya!',
       u'Check where it is going', u'¿va para?',
       u'¿Va para Masaya?', u'Are you going to Masaya?',
       [u'¿va para', u'Masaya?'],
       [u'la parada', u'me deja en', u'gracias', u'cuídese'],
       [u'va para masaya', u'va para'],
       [u'¿va para?'],
       u'Ask from the pavement, before you get on. He is shouting a destination and so is the bus in front of him, which is going somewhere else.'),
  beat(u'¡Sí, Masaya! Súbase, súbase, ya nos vamos.',
       u'Tell him where to drop you', u'me deja en',
       u'Me deja en el mercado.', u'Drop me at the market.',
       [u'me deja en', u'el mercado'],
       [u'la parada', u'ya voy bajando', u'gracias', u'no ando'],
       [u'me deja en el mercado', u'me deja en'],
       [u'me deja en'],
       u'Me deja en... names your stop. There is no bell and no list — you tell him once and he keeps it in his head along with everybody else’s.'),
  beat(u'Va pues. Son veinte pesos.',
       u'Ask where the stop actually is', u'la parada',
       u'¿Dónde queda la parada?', u'Where’s the stop?',
       [u'¿dónde queda', u'la parada?'],
       [u'me deja en', u'ya voy bajando', u'gracias', u'cuídese'],
       [u'donde queda la parada', u'la parada'],
       [u'la parada'],
       u'La parada is wherever people are standing. Asking is faster than looking for a sign, because there is no sign.'),
  beat(u'Ya casi, joven. Ahí adelantito.',
       u'Call out that you are getting off', u'ya voy bajando',
       u'¡Ya voy bajando!', u'I’m getting off!',
       [u'¡ya voy bajando!'],
       [u'la parada', u'me deja en', u'gracias', u'ya va'],
       [u'ya voy bajando'],
       [u'ya voy bajando'],
       u'Shout it, and shout it early. Ya voy bajando is the difference between your stop and a long walk back from the next one.'),
 ]},
{
 'id': 'terminal-02', 'district': 'terminal', 'tier': 2,
 'who': u'El taxista', 'title': u'El taxi',
 'goal': u'Agree the fare before you get in, not after',
 'culture': u'There is no meter in any taxi in this country and there never '
            u'has been. The fare is agreed through the window before you '
            u'open the door, and asking afterwards is a different and much '
            u'worse conversation with your bags already inside.',
 'beats': [
  beat(u'¿Taxi, joven? ¿Para dónde va?',
       u'To the market', u'al mercado',
       u'Al mercado.', u'To the market.',
       [u'al mercado'],
       [u'al parque', u'¿cuánto me cobra?', u'gracias', u'está bien'],
       [u'al mercado'],
       [u'al mercado'],
       u'Name the place, never the street. Al mercado is a complete address in this town.'),
  beat(u'Súbase pues, ahí lo llevo.',
       u'Ask the fare — through the window', u'¿cuánto me cobra?',
       u'¿Cuánto me cobra?', u'What will you charge me?',
       [u'¿cuánto me cobra?'],
       [u'al mercado', u'está bien', u'gracias', u'quiero'],
       [u'cuanto me cobra'],
       [u'¿cuánto me cobra?'],
       u'You asked the cargador this in the market and it is the same question here. No meter, so the number happens now or it happens badly later.'),
  beat(u'Cincuenta pesos.',
       u'Agree', u'está bien',
       u'Está bien. Cincuenta.', u'Alright. Fifty.',
       [u'está bien', u'cincuenta'],
       [u'cien', u'¿cuánto me cobra?', u'gracias', u'al mercado'],
       [u'esta bien cincuenta', u'esta bien'],
       [u'está bien'],
       u'Fifty is a fair town fare. Haggling a taxi here is not the ritual it is in a market — agree it and get in.'),
  beat(u'Así me gusta, que pregunte antes de subir. Muchos no.',
       u'Say the rule out loud', u'antes de subir',
       u'Antes de subir, siempre.', u'Before getting in, always.',
       [u'antes de subir', u'siempre'],
       [u'está bien', u'al mercado', u'gracias', u'quiero'],
       [u'antes de subir siempre', u'antes de subir'],
       [u'antes de subir'],
       u'Antes de subir — before getting in. He approves because the ones who ask afterwards are the ones who end up arguing on the pavement.'),
 ]},
{
 'id': 'terminal-03', 'district': 'terminal', 'tier': 2,
 'who': u'El del colectivo', 'title': u'El colectivo',
 'goal': u'Understand that a taxi stopping for others is not a scam',
 'culture': u'A colectivo picks up other passengers along the way and that is '
            u'why it costs a third of what a private ride would. It is not '
            u'your taxi and nothing has gone wrong. The only thing worth '
            u'negotiating is the order of the drop-offs.',
 'beats': [
  beat(u'Súbase, pero voy juntando gente, ¿va?',
       u'Ask if it is full', u'va lleno',
       u'¿Va lleno?', u'Is it full?',
       [u'¿va lleno?'],
       [u'yo voy primero', u'no importa', u'gracias', u'así es'],
       [u'va lleno'],
       [u'va lleno'],
       u'Juntando means he is collecting passengers. ¿Va lleno? is really asking how many more he plans to fit, and the answer is always one more.'),
  beat(u'Vamos cuatro. Pero usted va primero, no se preocupe.',
       u'Check that — you first?', u'yo voy primero',
       u'¿Yo voy primero?', u'I get dropped first?',
       [u'¿yo voy primero?'],
       [u'va lleno', u'no importa', u'gracias', u'ni modo'],
       [u'yo voy primero'],
       [u'yo voy primero'],
       u'The order of the drop-offs is the entire negotiation in a colectivo, and it goes to whoever thinks to ask.'),
  beat(u'Ahí voy a recoger a dos más, en la esquina nomás.',
       u'Say it does not matter', u'no importa',
       u'No importa. Está bien.', u'It doesn’t matter. That’s fine.',
       [u'no importa', u'está bien'],
       [u'va lleno', u'yo voy primero', u'gracias', u'me da'],
       [u'no importa esta bien', u'no importa'],
       [u'no importa'],
       u'It is not your taxi and the fare is a third of what it would be. No importa is both true and the right thing to say.'),
  beat(u'Así es aquí, joven. Todos vamos llegando.',
       u'Agree with him', u'así es aquí',
       u'Así es aquí. Así es.', u'That’s how it is here. That’s right.',
       [u'así es aquí', u'así es'],
       [u'no importa', u'va lleno', u'gracias', u'ni modo'],
       [u'asi es aqui asi es', u'asi es aqui'],
       [u'así es aquí'],
       u'Así es aquí — that is how it is here. Said with a shrug, it explains a great deal of the country and excuses none of it.'),
 ]},
{
 'id': 'terminal-04', 'district': 'terminal', 'tier': 3,
 'who': u'La de los boletos', 'title': u'El expreso',
 'goal': u'Buy a ticket to Managua and pick the right bus',
 'culture': u'The expreso does not stop; the ordinario stops for anybody who '
            u'waves and takes twice as long to save you about a dollar. The '
            u'timetable on the wall is from another year, so ask the woman '
            u'and not the wall.',
 'beats': [
  beat(u'Buenas. ¿Para dónde le doy?',
       u'A ticket to Managua', u'un boleto',
       u'Un boleto para Managua.', u'One ticket to Managua.',
       [u'un boleto', u'para Managua'],
       [u'el expreso', u'el próximo', u'gracias', u'con permiso'],
       [u'un boleto para managua', u'un boleto'],
       [u'un boleto'],
       u'Un boleto — one ticket. In a bus terminal it is very nearly the only sentence you strictly need.'),
  beat(u'¿Ordinario o expreso?',
       u'The express', u'el expreso',
       u'El expreso, por favor.', u'The express, please.',
       [u'el expreso', u'por favor'],
       [u'el ordinario', u'un boleto', u'gracias', u'con permiso'],
       [u'el expreso por favor', u'el expreso'],
       [u'el expreso'],
       u'El expreso does not stop. El ordinario stops for everybody who waves at it and takes twice as long to save you about a dollar.'),
  beat(u'Va. Ochenta córdobas el expreso.',
       u'Ask what time it leaves', u'¿a qué hora?',
       u'¿A qué hora sale?', u'What time does it leave?',
       [u'¿a qué hora', u'sale?'],
       [u'el próximo', u'gracias', u'con permiso', u'fíjese que'],
       [u'a que hora sale', u'a que hora'],
       [u'¿a qué hora?'],
       u'Sale is what buses, papers and photographs all do here. Ask her, because the timetable pinned to the wall is from another year.'),
  beat(u'Ese ya se fue, fíjese. El próximo a las dos.',
       u'Take the next one', u'el próximo',
       u'El próximo, entonces. Está bien.', u'The next one, then. That’s fine.',
       [u'el próximo', u'entonces', u'está bien'],
       [u'el expreso', u'gracias', u'con permiso', u'un boleto'],
       [u'el proximo entonces esta bien', u'el proximo entonces', u'el proximo'],
       [u'el próximo'],
       u'El próximo — the next one. There is always a next one, and it leaves when it is full whatever the ticket says.'),
 ]},
{
 'id': 'terminal-05', 'district': 'terminal', 'tier': 3,
 'who': u'El vendedor del bus', 'title': u'El que vende en el bus',
 'goal': u'Buy something from somebody selling in the aisle at speed',
 'culture': u'Vendors board at every stop, work the aisle and jump off before '
            u'the bus is properly moving. You have about twenty seconds, so '
            u'the Spanish is short and the money should already be in your '
            u'hand.',
 'beats': [
  beat(u'¡Agua, gaseosa, rosquillas! ¡Rosquillas calientitas!',
       u'Ask what he has', u'¿qué lleva?',
       u'¿Qué lleva?', u'What have you got?',
       [u'¿qué lleva?'],
       [u'deme uno', u'aquí tiene', u'gracias', u'cuídese'],
       [u'que lleva'],
       [u'¿qué lleva?'],
       u'¿Qué lleva? is what are you carrying, and it is the fastest possible question — which matters, because he is leaving.'),
  beat(u'Rosquillas, agua fría, gaseosa.',
       u'Ask for one', u'deme uno',
       u'Deme uno.', u'Give me one.',
       [u'deme uno'],
       [u'¿qué lleva?', u'aquí tiene', u'no ando', u'gracias'],
       [u'deme uno'],
       [u'deme uno'],
       u'Deme uno — give me one. Shorter than me da and right for the speed this is happening at.'),
  beat(u'Diez pesos, joven.',
       u'Pay him', u'aquí tiene',
       u'Aquí tiene. Diez.', u'Here you go. Ten.',
       [u'aquí tiene', u'diez'],
       [u'deme uno', u'no ando', u'gracias', u'ya va'],
       [u'aqui tiene diez', u'aqui tiene'],
       [u'aquí tiene'],
       u'Have the note ready before you ask. He is getting off at the next corner whether the transaction is finished or not.'),
  beat(u'Ahí tiene. ¡Buen viaje, pues!',
       u'Thank him as he jumps off', u'gracias joven',
       u'Gracias, joven.', u'Thanks, lad.',
       [u'gracias', u'joven'],
       [u'aquí tiene', u'deme uno', u'cuídese', u'ya va'],
       [u'gracias joven', u'gracias'],
       [u'gracias joven'],
       u'Joven is what you call any young man you are not going to name. He is fourteen and he has three more buses to work before dark.'),
 ]},
{
 'id': 'terminal-06', 'district': 'terminal', 'tier': 4,
 'who': u'El de las encomiendas', 'title': u'La encomienda',
 'goal': u'Send a package to somebody in another town',
 'culture': u'Parcels travel by bus. You hand it over, pay a little, it rides '
            u'in the same hold as everybody’s shopping, and somebody collects '
            u'it at the other terminal. There is no tracking of any kind and '
            u'it works, but only if a real person knows to be there.',
 'beats': [
  beat(u'¿Encomienda, joven?',
       u'Yes — you want to send this', u'mandar esto',
       u'Quiero mandar esto.', u'I want to send this.',
       [u'quiero', u'mandar esto'],
       [u'a Masaya', u'¿llega hoy?', u'gracias', u'otro día'],
       [u'quiero mandar esto', u'mandar esto'],
       [u'mandar esto'],
       u'Mandar esto, with the parcel held out. The whole system is a man, a bus and somebody waiting at the other end.'),
  beat(u'¿Y para dónde va?',
       u'To Masaya', u'a Masaya',
       u'A Masaya.', u'To Masaya.',
       [u'a Masaya'],
       [u'a Managua', u'mandar esto', u'gracias', u'¿a cómo?'],
       [u'a masaya'],
       [u'a Masaya'],
       u'The destination is a town, and every town has one terminal. That is the entire address.'),
  beat(u'Va. Sale en el de las tres.',
       u'Ask whether it gets there today', u'¿llega hoy?',
       u'¿Llega hoy?', u'Will it get there today?',
       [u'¿llega hoy?'],
       [u'a Masaya', u'mandar esto', u'gracias', u'otro día'],
       [u'llega hoy'],
       [u'¿llega hoy?'],
       u'It will. The bus takes an hour and your parcel is going in the hold with everybody’s shopping.'),
  beat(u'Llega hoy mismo, como a las cuatro.',
       u'Ask who collects it', u'¿quién lo recibe?',
       u'¿Y quién lo recibe?', u'And who picks it up?',
       [u'¿y quién', u'lo recibe?'],
       [u'¿llega hoy?', u'a Masaya', u'gracias', u'que le vaya bien'],
       [u'y quien lo recibe', u'quien lo recibe'],
       [u'¿quién lo recibe?'],
       u'Ask, because the answer is a person and not an office. Somebody has to be standing at that terminal when the bus pulls in.'),
 ]},
{
 'id': 'terminal-07', 'district': 'terminal', 'tier': 4,
 'who': u'El estafador', 'title': u'El que te quiere ver la cara',
 'goal': u'Spot the one who actually is trying it on',
 'culture': u'This is the only person in the whole game who is genuinely at '
            u'it, and that is the point: almost nobody is, which is exactly '
            u'why it works when somebody tries. No hay cambio, said after he '
            u'has your note, is the oldest one at any terminal. The move is '
            u'to be pleasant and not to move.',
 'beats': [
  beat(u'Le cambio los dólares aquí mismo, mejor precio que el banco. ...Uy, fíjese que no hay cambio.',
       u'Do not accept that', u'no hay cambio',
       u'¿No hay cambio?', u'No change?',
       [u'¿no hay cambio?'],
       [u'espere', u'yo le doy', u'gracias', u'Buenas'],
       [u'no hay cambio'],
       [u'no hay cambio'],
       u'He has your note in his hand and no change in the other. Said as a flat question rather than an accusation, this is where it starts going wrong for him.'),
  beat(u'Ahorita consigo, deme un minutito. Espéreme aquí.',
       u'Tell HIM to wait', u'espere',
       u'Espere. Yo no me muevo.', u'Wait. I’m not moving.',
       [u'espere', u'yo no me muevo'],
       [u'no hay cambio', u'yo le doy', u'gracias', u'por favor'],
       [u'espere yo no me muevo', u'espere'],
       [u'espere'],
       u'Do not follow him and do not leave. Espere, said calmly, standing exactly where you are, ends most of these inside a minute.'),
  beat(u'Bueno, bueno. Deme los otros cien y yo le doy todo junto ahorita.',
       u'Turn it round', u'yo le doy',
       u'Yo le doy cuando tenga el cambio.', u'I’ll hand it over when you have the change.',
       [u'yo le doy', u'cuando tenga el cambio'],
       [u'no hay cambio', u'espere', u'gracias', u'por favor'],
       [u'yo le doy cuando tenga el cambio', u'yo le doy'],
       [u'yo le doy'],
       u'You hand yours over when he has the change in his hand. Said pleasantly it is not an accusation, and there is nothing in it for him to argue with.'),
  beat(u'Ya pues, hombre, tenga. No sea así conmigo.',
       u'Close it', u'no me venga',
       u'No me venga con eso.', u'Don’t come at me with that.',
       [u'no me venga', u'con eso'],
       [u'espere', u'gracias', u'Buenas', u'por favor'],
       [u'no me venga con eso', u'no me venga'],
       [u'no me venga'],
       u'No me venga con eso is the firmest thing in this entire game, and it is the right amount of firm for exactly one person in it.'),
 ]},
{
 'id': 'terminal-08', 'district': 'terminal', 'tier': 4,
 'who': u'La señora con maletas', 'title': u'Las maletas',
 'goal': u'Help somebody with bags and refuse the money',
 'culture': u'The mirror of the cargador in the market: there, you paid '
            u'somebody to carry, and agreeing the price first was the whole '
            u'etiquette. Here you are the one carrying, and refusing the '
            u'money is. She will offer, because everybody who lifts a bag in '
            u'that terminal is paid for it.',
 'beats': [
  beat(u'Ay, Dios... perdón, joven, es que son muchas.',
       u'Offer before she asks', u'yo le ayudo',
       u'Yo le ayudo, doña.', u'Let me help you, doña.',
       [u'yo le ayudo', u'doña'],
       [u'no es nada', u'no se preocupe', u'gracias', u'está bien'],
       [u'yo le ayudo dona', u'yo le ayudo'],
       [u'yo le ayudo'],
       u'Offer first. There is no version of this where she asks you, and the offer is the whole of the kindness.'),
  beat(u'¡Ay, mi hijo, gracias! ¿Y cuánto le doy?',
       u'Refuse the money', u'no es nada',
       u'Nada, doña. No es nada.', u'Nothing, doña. It’s nothing.',
       [u'nada', u'doña', u'no es nada'],
       [u'yo le ayudo', u'no se preocupe', u'gracias', u'me da'],
       [u'nada dona no es nada', u'no es nada'],
       [u'no es nada'],
       u'She offers because everybody who lifts a bag in this terminal is paid for it. No es nada declines without leaving her owing you.'),
  beat(u'Pero es que usted se molestó por mí...',
       u'Tell her not to worry', u'no se preocupe',
       u'No se preocupe.', u'Don’t worry about it.',
       [u'no se preocupe'],
       [u'no es nada', u'yo le ayudo', u'gracias', u'está bien'],
       [u'no se preocupe'],
       [u'no se preocupe'],
       u'No se preocupe closes it. A third refusal after this would start making it about you.'),
  beat(u'Que Dios se lo pague, mi hijo. De verdad.',
       u'Say goodbye properly', u'que le vaya bien',
       u'Que le vaya bien, doña.', u'All the best to you, doña.',
       [u'que le vaya bien', u'doña'],
       [u'no es nada', u'gracias', u'está bien', u'me da'],
       [u'que le vaya bien dona', u'que le vaya bien'],
       [u'que le vaya bien'],
       u'Que Dios se lo pague is the largest thank-you there is here and it is not answered in kind. Que le vaya bien is the right size.'),
 ]},
{
 'id': 'terminal-09', 'district': 'terminal', 'tier': 5,
 'who': u'El chofer', 'title': u'El chofer',
 'goal': u'Sit up front and get a driver talking for forty minutes',
 'culture': u'The seat beside the driver is not off limits and it is cooler. '
            u'Four questions is all it takes; after that your part is '
            u'listening, and you will learn more Spanish in forty minutes of '
            u'it than in a week of anything else.',
 'beats': [
  beat(u'Súbase adelante si quiere, joven. Ahí va más fresco.',
       u'Ask how long he has been driving', u'¿cuántos años maneja?',
       u'¿Cuántos años maneja usted?', u'How many years have you been driving?',
       [u'¿cuántos años', u'maneja usted?'],
       [u'toda la ruta', u'me gusta', u'así es', u'ni modo'],
       [u'cuantos anos maneja usted', u'cuantos anos maneja'],
       [u'¿cuántos años maneja?'],
       u'Manejar is to drive; conducir is what a textbook says and nobody here. Ask a driver his years and you have bought yourself the whole journey.'),
  beat(u'Veintidós años. Toda la ruta me la sé de memoria.',
       u'The whole route?', u'toda la ruta',
       u'¿Toda la ruta?', u'The whole route?',
       [u'¿toda la ruta?'],
       [u'me gusta', u'uno se acostumbra', u'así es', u'me deja en'],
       [u'toda la ruta'],
       [u'toda la ruta'],
       u'De memoria again — the same phrase the poet used about Darío. He means every curve, every tope and every place the police stand.'),
  beat(u'Toda. Y me gusta, fíjese. No lo cambio.',
       u'Ask whether he really likes it', u'me gusta',
       u'¿Le gusta manejar?', u'You like driving?',
       [u'¿le gusta', u'manejar?'],
       [u'toda la ruta', u'uno se acostumbra', u'así es', u'ni modo'],
       [u'le gusta manejar', u'le gusta'],
       [u'me gusta'],
       u'Me gusta from him, le gusta from you. He said it first and unprompted, which in a job like his is worth noticing out loud.'),
  beat(u'Cansa, eso sí. Pero uno se acostumbra.',
       u'Agree the way he means it', u'uno se acostumbra',
       u'Uno se acostumbra. Así es.', u'You get used to it. That’s right.',
       [u'uno se acostumbra', u'así es'],
       [u'me gusta', u'toda la ruta', u'ni modo', u'me deja en'],
       [u'uno se acostumbra asi es', u'uno se acostumbra'],
       [u'uno se acostumbra'],
       u'Uno for I, which turns it into something general — it is how people here say the hard part out loud without it counting as a complaint.'),
 ]},
{
 'id': 'terminal-10', 'district': 'terminal', 'tier': 5,
 'who': u'El que se va', 'title': u'El migrante',
 'goal': u'Say goodbye to somebody leaving for good',
 'culture': u'The bus goes to the border and after that nobody at this '
            u'terminal knows anything. Everybody has somebody on one of '
            u'these. Nobody says how long, because nobody knows, and the '
            u'honest no sé is allowed to sit there without being filled in.',
 'beats': [
  beat(u'Me voy, pues. Ya está el bus ahí.',
       u'Check — today?', u'se va',
       u'¿Se va hoy?', u'You’re going today?',
       [u'¿se va', u'hoy?'],
       [u'¿cuándo vuelve?', u'no sé', u'cuídese', u'con permiso'],
       [u'se va hoy', u'se va'],
       [u'se va'],
       u'Se va — he is going. That bus goes to the border, and after the border nobody standing here knows anything.'),
  beat(u'Hoy mismo. A las tres sale.',
       u'Ask when he is coming back', u'¿cuándo vuelve?',
       u'¿Y cuándo vuelve?', u'And when will you be back?',
       [u'¿y cuándo', u'vuelve?'],
       [u'se va', u'no sé', u'cuídese', u'fíjese que'],
       [u'y cuando vuelve', u'cuando vuelve'],
       [u'¿cuándo vuelve?'],
       u'Ask it. Everybody standing at that gate is thinking it and somebody has to be the one who says it out loud.'),
  beat(u'No sé. De verdad no sé, hermano.',
       u'Let the answer stand', u'no sé',
       u'No sabe. Está bien.', u'You don’t know. That’s alright.',
       [u'no sabe', u'está bien'],
       [u'no sé', u'se va', u'cuídese', u'con permiso'],
       [u'no sabe esta bien', u'no sabe'],
       [u'no sé'],
       u'No sé is the honest answer and the temptation is to fill the silence after it with something hopeful. Do not. Letting it stand is the respect.'),
  beat(u'Cuídese usted, pues. Cuide la casa.',
       u'Say the thing there is to say', u'que Dios lo acompañe',
       u'Que Dios lo acompañe.', u'May God go with you.',
       [u'que Dios lo acompañe'],
       [u'cuídese', u'no sé', u'con permiso', u'fíjese que'],
       [u'que dios lo acompane', u'que dios lo acompane cuidese'],
       [u'que Dios lo acompañe'],
       u'Said to people leaving whether anybody believes it or not, because it is what there is and nothing smaller would do.'),
 ]},
]

HINTS = [
 # Pantanal
 {'kind': u'chavalo en bici', 'district': 'pantanal',
  'says': u'Si quiere ir a las isletas, no pague el tour. Ahí en la orilla hay pescadores que lo llevan.',
  'en': u'If you want to go to the isletas, do not pay for the tour. There are fishermen on the shore who will take you.',
  'points_at': ['pantanal-01']},
 {'kind': u'doña en la puerta', 'district': 'pantanal',
  'says': u'¿Anda con ropa sucia? La lavandera de la otra cuadra lava bien y cobra poco.',
  'en': u'Got dirty washing? The laundress a block over washes well and charges little.',
  'points_at': ['pantanal-02']},
 {'kind': u'obrero', 'district': 'pantanal',
  'says': u'Aquí no hay agua desde el martes. Pregúntele al señor de la esquina, él avisa cuando viene.',
  'en': u'There has been no water here since Tuesday. Ask the man on the corner, he lets everyone know when it comes back.',
  'points_at': ['pantanal-03']},
 {'kind': u'vendedora', 'district': 'pantanal',
  'says': u'¿Cocina con leña? La señora del fogón la vende por tercio, y seca.',
  'en': u'Do you cook with wood? The woman with the stove sells it by the bundle, and dry.',
  'points_at': ['pantanal-04']},
 {'kind': u'viejo de la esquina', 'district': 'pantanal',
  # `pisto` IS Nicaraguan for money, but dialect.py bans it with the
  # Guatemalan and Salvadoran slang and it is not worth loosening the
  # gate over one crowd line. Kevin may want it allowed later.
  'says': u'Ese chavalo anda pidiendo todo el día. No le dé dinero: cómprele de comer, es mejor.',
  'en': u'That kid begs all day. Do not give him money: buy him something to eat, it is better.',
  'points_at': ['pantanal-05']},
 {'kind': u'doña en la puerta', 'district': 'pantanal',
  'says': u'A doña Julia se le metió el agua otra vez anoche. Está sacándola sola, la pobre.',
  'en': u'Doña Julia’s house flooded again last night. She is bailing it out on her own, poor thing.',
  'points_at': ['pantanal-06']},
 {'kind': u'obrero', 'district': 'pantanal',
  'says': u'El albañil anda en aquel techo y está solo. Si le ayuda, no le va a explicar nada.',
  'en': u'The builder is up on that roof on his own. If you help him, he will not explain a thing.',
  'points_at': ['pantanal-07']},
 {'kind': u'evangélico', 'district': 'pantanal',
  'says': u'La curandera vive al final. Yo no creo en eso, pero la gente le tiene fe.',
  'en': u'The healer lives at the end of the street. I do not believe in it, but people have faith in her.',
  'points_at': ['pantanal-08']},
 {'kind': u'caponero', 'district': 'pantanal',
  'says': u'Ese hombre estuvo cinco años en Costa Rica y volvió igual. Pregúntele, le gusta contarlo.',
  'en': u'That man spent five years in Costa Rica and came back the same. Ask him, he likes telling it.',
  'points_at': ['pantanal-09']},
 {'kind': u'viejo de la esquina', 'district': 'pantanal',
  'says': u'La abuela de esa casa estaba en Managua en el setenta y dos. Ella sí se acuerda.',
  'en': u'The grandmother in that house was in Managua in ’72. She remembers all of it.',
  'points_at': ['pantanal-10']},
 # La Terminal
 {'kind': u'caponero', 'district': 'terminal',
  'says': u'Pregunte al cobrador para dónde va antes de subirse. Los buses no dicen nada afuera.',
  'en': u'Ask the conductor where it is going before you get on. The buses say nothing on the outside.',
  'points_at': ['terminal-01']},
 {'kind': u'cuidacarros', 'district': 'terminal',
  'says': u'Los taxis no tienen taxímetro, jefe. Pregunte el precio por la ventana, antes de subir.',
  'en': u'The taxis have no meter, boss. Ask the price through the window, before you get in.',
  'points_at': ['terminal-02', 'terminal-03']},
 {'kind': u'policía', 'district': 'terminal',
  'says': u'Si el taxi recoge a otros no es engaño, es colectivo. Por eso le sale más barato.',
  'en': u'If the taxi picks up other people it is not a trick, it is a colectivo. That is why it costs you less.',
  'points_at': ['terminal-03']},
 {'kind': u'vendedora', 'district': 'terminal',
  'says': u'Los boletos para Managua los venden ahí. Pida el expreso, que el ordinario no llega nunca.',
  'en': u'They sell the Managua tickets there. Ask for the express, the ordinary one never gets there.',
  'points_at': ['terminal-04']},
 {'kind': u'chavalo en bici', 'district': 'terminal',
  'says': u'En el bus se sube gente vendiendo rosquillas. Tenga el billete listo, que se bajan rápido.',
  'en': u'People get on the bus selling rosquillas. Have your money ready, they get off fast.',
  'points_at': ['terminal-05']},
 {'kind': u'obrero', 'district': 'terminal',
  'says': u'¿Va a mandar algo a otro pueblo? Se manda en el bus, ahí donde las encomiendas.',
  'en': u'Sending something to another town? It goes by bus, over there where the parcels are.',
  'points_at': ['terminal-06']},
 {'kind': u'policía', 'district': 'terminal',
  'says': u'Cuidado con el que cambia dólares en la terminal. Ese sí le quiere ver la cara.',
  'en': u'Watch out for the man changing dollars in the terminal. That one really is trying it on.',
  'points_at': ['terminal-07']},
 {'kind': u'doña en la puerta', 'district': 'terminal',
  'says': u'Ahí anda una señora con cuatro maletas y nadie la ayuda. Es que aquí todo se cobra.',
  'en': u'There is a woman there with four suitcases and nobody helping her. Everything gets charged for here.',
  'points_at': ['terminal-08']},
 {'kind': u'caponero', 'district': 'terminal',
  'says': u'Súbase adelante con el chofer. Ese hombre lleva veintidós años en la misma ruta.',
  'en': u'Sit up front with the driver. That man has done the same route for twenty-two years.',
  'points_at': ['terminal-09']},
 {'kind': u'viejo de la esquina', 'district': 'terminal',
  'says': u'Ese muchacho se va hoy para el sur. La mamá está ahí y no le dice nada.',
  'en': u'That lad is leaving for the south today. His mother is right there and she is not saying anything.',
  'points_at': ['terminal-10']},
]

# ---------------------------------------------------------------- write

for m in MISSIONS:
    with io.open(os.path.join(GAME, m['id'] + '.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(m, ensure_ascii=False, indent=1) + u'\n')

by_district = {}
for h in HINTS:
    by_district.setdefault(h['district'], []).append(h)
crowd_counts = {}
for district, rows in by_district.items():
    path = os.path.join(CROWD, district + '.json')
    existing = []
    if os.path.exists(path):
        with io.open(path, encoding='utf-8') as f:
            existing = json.load(f)
    have = set((r.get('kind'), r.get('says')) for r in existing)
    merged = existing + [h for h in rows if (h['kind'], h['says']) not in have]
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(merged, ensure_ascii=False, indent=1) + u'\n')
    crowd_counts[district] = (len(merged) - len(existing), len(merged))

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
for district in by_district:
    path = os.path.join(CROWD, district + '.json')
    for h in json.load(io.open(path, encoding='utf-8')):
        pointed |= set(h['points_at'])
for m in MISSIONS:
    if m['id'] not in pointed:
        bad.append(u'%s is unfindable: nobody in the street points at it' % m['id'])

lines = [u'wrote %d missions, %d beats'
         % (len(MISSIONS), sum(len(m['beats']) for m in MISSIONS))]
for d in sorted(crowd_counts):
    lines.append(u'crowd %-10s %d new (%d in the file)'
                 % (d, crowd_counts[d][0], crowd_counts[d][1]))
lines += bad or [u'checks clean']
report = u'\n'.join(lines) + u'\n'
if OUT:
    with io.open(OUT, 'w', encoding='utf-8') as f:
        f.write(report)
print(report.encode('ascii', 'replace').decode('ascii'))
