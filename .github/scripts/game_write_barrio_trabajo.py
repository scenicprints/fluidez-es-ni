# -*- coding: utf-8 -*-
"""Writes Tu barrio (14) and El trabajo (10).

Tu barrio is your own street, and it is the district the whole game has been
walking towards: renting a room by the month instead of the night, being given
credit at the pulpería because you are now somebody who comes back, a wake, a
telling-off delivered so carefully that nobody is told off, and finally being
greeted first by everybody on your own block.

El trabajo is where the Spanish stops being polite and starts being useful,
and where VOS takes over: Marcos is a workmate your own age and the new lad is
newer than you, so the imperatives go ponete, mirá, seguí. The one place it
snaps back to usted is asking a friend for money, which is real and worth
noticing.

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
# ── Tu barrio ───────────────────────────────────────────────────────────
{
 'id': 'barrio-01', 'district': 'barrio', 'tier': 1,
 'who': u'Doña Marta', 'title': u'El cuarto',
 'goal': u'Rent a room by the month instead of the night',
 'culture': u'You rent from a woman who lives in the same house. There is no '
            u'agency, no contract and nothing to sign — the agreement is the '
            u'two of you saying the numbers out loud. Which is why the water '
            u'and the light have to be asked about now, by you.',
 'beats': [
  beat(u'Buenas. Sí, tengo un cuarto desocupado. ¿Lo quiere ver?',
       u'Ask to take it by the month', u'por mes',
       u'¿Me lo alquila por mes?', u'Would you rent it to me by the month?',
       [u'¿me lo alquila', u'por mes?'],
       [u'el alquiler', u'¿desde cuándo?', u'gracias', u'no ando'],
       [u'me lo alquila por mes', u'por mes'],
       [u'por mes'],
       u'Por mes, not por noche. The hostel was fifteen dollars a night; this is a different arrangement and this is the sentence that opens it.'),
  beat(u'Claro. Son cien dólares el mes.',
       u'Say the number back', u'el alquiler',
       u'Cien dólares de alquiler.', u'A hundred dollars rent.',
       [u'cien dólares', u'de alquiler'],
       [u'por mes', u'¿desde cuándo?', u'gracias', u'ya va'],
       [u'cien dolares de alquiler', u'de alquiler'],
       [u'el alquiler'],
       u'El alquiler is the rent. Say the number back out loud: there is nothing to sign, so the two of you agreeing out loud IS the agreement.'),
  beat(u'Ajá. Cien al mes, adelantado.',
       u'Ask whether the water is included', u'¿el agua va incluida?',
       u'¿El agua va incluida?', u'Is the water included?',
       [u'¿el agua', u'va incluida?'],
       [u'el alquiler', u'por mes', u'gracias', u'no ando'],
       [u'el agua va incluida', u'va incluida'],
       [u'¿el agua va incluida?'],
       u'Ask, because often it is not, and the water and the light are what turn a cheap room into an expensive one.'),
  beat(u'El agua sí. La luz la paga usted aparte.',
       u'Ask from when', u'¿desde cuándo?',
       u'¿Y desde cuándo?', u'And from when?',
       [u'¿y desde cuándo?'],
       [u'por mes', u'el alquiler', u'gracias', u'que le vaya bien'],
       [u'y desde cuando', u'desde cuando'],
       [u'¿desde cuándo?'],
       u'¿Desde cuándo? asks when it starts. Everything here is agreed by talking, so the date has to be said out loud as well.'),
 ]},
{
 'id': 'barrio-02', 'district': 'barrio', 'tier': 1,
 'who': u'Doña Marta', 'title': u'El depósito',
 'goal': u'Understand the deposit and when you get it back',
 'culture': u'A month held as a deposit, in cash, with nothing written down. '
            u'It comes back if the room does, and the time to settle what '
            u'that means is now — pleasantly, while everybody still likes '
            u'each other.',
 'beats': [
  beat(u'Ah, y me deja el depósito.',
       u'Ask what deposit', u'el depósito',
       u'¿El depósito? ¿De cuánto?', u'A deposit? How much?',
       [u'¿el depósito?', u'¿de cuánto?'],
       [u'un mes', u'cuando me vaya', u'gracias', u'otro día'],
       [u'el deposito de cuanto', u'el deposito'],
       [u'el depósito'],
       u'El depósito. Nothing is written down, so what it is and when it comes back are things you settle out loud, now.'),
  beat(u'Un mes. Igual que el alquiler.',
       u'One month — say it back', u'un mes',
       u'Un mes, entonces.', u'A month, then.',
       [u'un mes', u'entonces'],
       [u'dos meses', u'el depósito', u'gracias', u'¿a cómo?'],
       [u'un mes entonces', u'un mes'],
       [u'un mes'],
       u'One month’s rent, held in a drawer. Repeating the number is how a spoken agreement gets made in a country that does not sign much.'),
  beat(u'Ajá. Así se hace aquí.',
       u'Ask when you get it back', u'cuando me vaya',
       u'¿Me lo devuelve cuando me vaya?', u'Do I get it back when I leave?',
       [u'¿me lo devuelve', u'cuando me vaya?'],
       [u'un mes', u'el depósito', u'gracias', u'otro día'],
       [u'me lo devuelve cuando me vaya', u'cuando me vaya'],
       [u'cuando me vaya'],
       u'Cuando me vaya — when I go. Ask it now, kindly, while the two of you are still pleased with each other.'),
  beat(u'Cuando se vaya, sí. Si me deja el cuarto bien.',
       u'Close the agreement', u'quedamos',
       u'Quedamos así, doña.', u'Agreed, then, doña.',
       [u'quedamos así', u'doña'],
       [u'un mes', u'el depósito', u'gracias', u'Buenas'],
       [u'quedamos asi dona', u'quedamos asi'],
       [u'quedamos'],
       u'Quedamos así — the same two words that closed the deal with the porter in the market. It is how every agreement in this country gets signed.'),
 ]},
{
 'id': 'barrio-03', 'district': 'barrio', 'tier': 2,
 'who': u'El pulpero', 'title': u'Fiado',
 'goal': u'Be given credit at the shop, which means being trusted',
 'culture': u'Fiado is credit in a school exercise book behind the counter, '
            u'with no interest and no paperwork. Being given it is not a '
            u'financial event, it is a social one: it says you are somebody '
            u'who lives here and will be walking past tomorrow.',
 'beats': [
  beat(u'Son sesenta pesos. ...¿No le alcanza?',
       u'Ask for credit', u'fiado',
       u'¿Me lo da fiado?', u'Could you put it on credit?',
       [u'¿me lo da', u'fiado?'],
       [u'me lo apunta', u'mañana le pago', u'gracias', u'está bien'],
       [u'me lo da fiado', u'fiado'],
       [u'fiado'],
       u'Fiado is credit, in a notebook, with nothing signed. Asking for it is asking to be counted as a neighbour rather than a customer.'),
  beat(u'Va pues. Se lo fío.',
       u'He said yes — react', u'ideay',
       u'¡Ideay! Gracias.', u'Well! Thank you.',
       [u'¡ideay!', u'gracias'],
       [u'fiado', u'me lo apunta', u'está bien', u'por favor'],
       [u'ideay gracias', u'ideay'],
       [u'ideay'],
       u'Ideay is the most Nicaraguan noise there is — surprise, greeting, disbelief, delight — and the tone does all of the work. Here it means: really? Thanks.'),
  beat(u'Le apunto aquí en el cuaderno, ¿va?',
       u'Yes — write it down', u'me lo apunta',
       u'Sí, me lo apunta.', u'Yes, put it down for me.',
       [u'sí', u'me lo apunta'],
       [u'ideay', u'fiado', u'gracias', u'por favor'],
       [u'si me lo apunta', u'me lo apunta'],
       [u'me lo apunta'],
       u'Me lo apunta — put it down for me. That exercise book is the entire credit system of the barrio and it works better than most.'),
  beat(u'¿Y cuándo me paga?',
       u'Name the day', u'mañana le pago',
       u'Mañana le pago. Palabra.', u'I’ll pay you tomorrow. My word.',
       [u'mañana le pago', u'palabra'],
       [u'otro día', u'fiado', u'gracias', u'está bien'],
       [u'manana le pago palabra', u'manana le pago'],
       [u'mañana le pago'],
       u'Say the day and then keep it. The thing that ends fiado is never being poor — it is not turning up.'),
 ]},
{
 'id': 'barrio-04', 'district': 'barrio', 'tier': 2,
 'who': u'El barbero', 'title': u'La barbería',
 'goal': u'Get the haircut you actually asked for',
 'culture': u'No numbers, no guards and no photographs. He asks as he goes '
            u'and you answer in two-word instructions, which is why this is '
            u'a listening mission disguised as a haircut.',
 'beats': [
  beat(u'Buenas. Siéntese. ¿Cómo se lo hago?',
       u'Shorter', u'más corto',
       u'Más corto, por favor.', u'Shorter, please.',
       [u'más corto', u'por favor'],
       [u'a los lados', u'así está bien', u'gracias', u'con permiso'],
       [u'mas corto por favor', u'mas corto'],
       [u'más corto'],
       u'Más corto is the whole instruction, and he will ask about the rest as he goes. There is no number and no attachment on the clippers.'),
  beat(u'¿Y de arriba? ¿También?',
       u'At the sides only', u'a los lados',
       u'A los lados nada más.', u'At the sides only.',
       [u'a los lados', u'nada más'],
       [u'más corto', u'de arriba', u'gracias', u'fíjese que'],
       [u'a los lados nada mas', u'a los lados'],
       [u'a los lados'],
       u'The two words that stop a haircut from turning into a different haircut. Say them before he starts, not after.'),
  beat(u'¿Así, mire? ¿Le gusta?',
       u'That’s right', u'así está bien',
       u'Así está bien.', u'That’s just right.',
       [u'así está bien'],
       [u'más corto', u'a los lados', u'gracias', u'con permiso'],
       [u'asi esta bien'],
       [u'así está bien'],
       u'Así está bien again — the same phrase that stops the butcher’s scale. It stops anything, anywhere, without giving offence.'),
  beat(u'¿Le arreglo la barba también?',
       u'Leave it as it is', u'déjelo así',
       u'Déjelo así. Gracias.', u'Leave it as it is. Thank you.',
       [u'déjelo así', u'gracias'],
       [u'más corto', u'a los lados', u'con permiso', u'fíjese que'],
       [u'dejelo asi gracias', u'dejelo asi'],
       [u'déjelo así'],
       u'Déjelo así — leave it. Useful in a barbershop and in every other situation where somebody is about to improve something of yours.'),
 ]},
{
 'id': 'barrio-05', 'district': 'barrio', 'tier': 2,
 'who': u'La vecina de al lado', 'title': u'La música',
 'goal': u'Ask a neighbour to turn it down at one in the morning',
 'culture': u'Music at volume is normal and complaining about it is not, so '
            u'the entire thing is done as a favour asked rather than a right '
            u'asserted. Politeness gets it turned down. A complaint gets it '
            u'turned up, and then you live next door to that for a year.',
 'beats': [
  beat(u'(La música se oye desde la calle. Es la una de la mañana.)',
       u'Open by apologising', u'disculpe',
       u'Disculpe, vecina.', u'Excuse me, neighbour.',
       [u'disculpe', u'vecina'],
       [u'un favor', u'es muy tarde', u'gracias', u'cuídese'],
       [u'disculpe vecina', u'disculpe'],
       [u'disculpe'],
       u'You open by apologising for existing. That is not weakness here — it is the move that decides how the next thirty seconds go.'),
  beat(u'¿Sí? Dígame, vecino.',
       u'Ask for a favour', u'un favor',
       u'¿Me hace un favor?', u'Would you do me a favour?',
       [u'¿me hace', u'un favor?'],
       [u'disculpe', u'es muy tarde', u'gracias', u'ya va'],
       [u'me hace un favor', u'un favor'],
       [u'un favor'],
       u'Ask for a favour rather than assert a right. The music is not illegal and you are not owed silence — you are asking a neighbour for something.'),
  beat(u'Claro, ¿qué pasó?',
       u'State the fact and stop', u'es muy tarde',
       u'Es muy tarde. La música.', u'It’s very late. The music.',
       [u'es muy tarde', u'la música'],
       [u'un favor', u'disculpe', u'gracias', u'no ando'],
       [u'es muy tarde la musica', u'es muy tarde'],
       [u'es muy tarde'],
       u'Say the fact and stop talking. Add what you want after it and you are complaining; leave it there and she will say it for you.'),
  beat(u'Ay, sí pues. Ya la bajo, no se preocupe.',
       u'Thank her properly', u'se lo agradezco',
       u'Se lo agradezco, vecina.', u'I really appreciate it, neighbour.',
       [u'se lo agradezco', u'vecina'],
       [u'disculpe', u'un favor', u'cuídese', u'ya va'],
       [u'se lo agradezco vecina', u'se lo agradezco'],
       [u'se lo agradezco'],
       u'Se lo agradezco is a size up from gracias, and it is the right size for somebody who did what you asked at one in the morning.'),
 ]},
{
 'id': 'barrio-06', 'district': 'barrio', 'tier': 3,
 'who': u'El electricista', 'title': u'Se fue la luz',
 'goal': u'Get the power back, and learn it is not just your house',
 'culture': u'The first question is never how to fix it, it is how far it '
            u'goes. Your house alone is your problem; the whole block is the '
            u'company’s. And somebody has to ring it in, which everybody '
            u'assumes somebody else has already done.',
 'beats': [
  beat(u'Buenas, joven. ¿También sin luz?',
       u'Say the power has gone', u'se fue la luz',
       u'Se fue la luz.', u'The power’s gone.',
       [u'se fue la luz'],
       [u'en toda la cuadra', u'¿ya llamó?', u'está bien', u'me da'],
       [u'se fue la luz'],
       [u'se fue la luz'],
       u'Se fue la luz — the light went. The verb is irse, as though it had walked out, which after the third time in a week is how it feels.'),
  beat(u'A mí también, desde hace rato.',
       u'Ask how far it goes', u'en toda la cuadra',
       u'¿En toda la cuadra?', u'The whole block?',
       [u'¿en toda la cuadra?'],
       [u'se fue la luz', u'¿ya llamó?', u'está bien', u'quiero'],
       [u'en toda la cuadra'],
       [u'en toda la cuadra'],
       u'This is the diagnostic question and it changes what happens next. Your house is your problem; the block is somebody else’s.'),
  beat(u'En toda. Hasta la esquina está oscuro.',
       u'Ask whether anybody has rung it in', u'¿ya llamó?',
       u'¿Ya llamó alguien?', u'Has anyone called it in?',
       [u'¿ya llamó', u'alguien?'],
       [u'en toda la cuadra', u'se fue la luz', u'gracias', u'me da'],
       [u'ya llamo alguien', u'ya llamo'],
       [u'¿ya llamó?'],
       u'Somebody has to report it and everybody assumes somebody else did. Asking is how you find out that nobody has.'),
  beat(u'Sí, ya llamaron. Ya viene la cuadrilla.',
       u'Accept that', u'ya viene',
       u'Ya viene, entonces. Está bien.', u'It’s coming, then. Alright.',
       [u'ya viene', u'entonces', u'está bien'],
       [u'se fue la luz', u'¿ya llamó?', u'me da', u'quiero'],
       [u'ya viene entonces esta bien', u'ya viene entonces', u'ya viene'],
       [u'ya viene'],
       u'Ya viene means it is on its way and commits nobody to a time. You will hear it about the bus, the plumber, the rain and the light.'),
 ]},
{
 'id': 'barrio-07', 'district': 'barrio', 'tier': 3,
 'who': u'Roberto', 'title': u'El chavalo de al lado',
 'goal': u'Let a kid teach you the words nobody prints',
 'culture': u'None of these four words are in a textbook and all four are in '
            u'every conversation. A nine-year-old will teach them to you '
            u'faster and more accurately than anybody else, because he has '
            u'no idea which ones are supposed to be difficult.',
 'beats': [
  beat(u'¡Chele! ¿Y usted cómo se llama?',
       u'Ask what chele means', u'chele',
       u'¿Qué es chele?', u'What’s a chele?',
       [u'¿qué es', u'chele?'],
       [u'chunche', u'vaya pues', u'dale', u'así es'],
       [u'que es chele', u'chele'],
       [u'chele'],
       u'Chele is what you are: fair, foreign, or both. It is not an insult, it is not going to stop, and the only useful response is to know it.'),
  beat(u'Chele es usted, pues. Blanquito. Pasame ese chunche.',
       u'Ask what a chunche is', u'chunche',
       u'¿Y qué es un chunche?', u'And what’s a chunche?',
       [u'¿y qué es', u'un chunche?'],
       [u'chele', u'vaya pues', u'dale', u'ni modo'],
       [u'y que es un chunche', u'que es un chunche'],
       [u'chunche'],
       u'A chunche is a thing whose name you do not need: the thingy, the whatsit, that. It will cover about a fifth of everything you cannot yet name.'),
  beat(u'El chunche es... cualquier cosa. Eso. Aquello. ¿Entendiste?',
       u'Tell him you have it', u'dale',
       u'Dale, entendí.', u'Right, got it.',
       [u'dale', u'entendí'],
       [u'vaya pues', u'chunche', u'así es', u'ideay'],
       [u'dale entendi', u'dale'],
       [u'dale'],
       u'Dale is go on, alright, yes, do it. It is the most-used word in the country after pues and on its own it means almost nothing.'),
  beat(u'¡Va! Ya aprendió. Vaya pues, chele.',
       u'Sign off the way he did', u'vaya pues',
       u'Vaya pues, Roberto.', u'See you, then, Roberto.',
       [u'vaya pues', u'Roberto'],
       [u'dale', u'chunche', u'chele', u'ni modo'],
       [u'vaya pues roberto', u'vaya pues'],
       [u'vaya pues'],
       u'Vaya pues closes a conversation without ending it. Half the goodbyes in this country are these two words and nothing else.'),
 ]},
{
 'id': 'barrio-08', 'district': 'barrio', 'tier': 3,
 'who': u'Doña Marta', 'title': u'La gotera',
 'goal': u'Report a leak and get it fixed before the rains',
 'culture': u'The rains start in May and after that it is every afternoon, so '
            u'a drip in March is a small favour and a drip in June is an '
            u'emergency for everybody at once. The deadline is the useful '
            u'part of the report.',
 'beats': [
  beat(u'Buenas, mi hijo. ¿Qué pasó?',
       u'Report the leak', u'hay una gotera',
       u'Hay una gotera.', u'There’s a leak.',
       [u'hay una gotera'],
       [u'en el cuarto', u'cuando llueve', u'ideay', u'ni modo'],
       [u'hay una gotera'],
       [u'hay una gotera'],
       u'Una gotera is a drip through the roof and every house here has had one. Naming it is the whole report.'),
  beat(u'¿Dónde, pues?',
       u'In the room', u'en el cuarto',
       u'En el cuarto, arriba.', u'In the room, up there.',
       [u'en el cuarto', u'arriba'],
       [u'hay una gotera', u'cuando llueve', u'vaya pues', u'ni modo'],
       [u'en el cuarto arriba', u'en el cuarto'],
       [u'en el cuarto'],
       u'Cuarto again — the same word as your first night in the hostel. Arriba here means up there, not west: context does that work.'),
  beat(u'¿Y gotea siempre o qué?',
       u'Only when it rains', u'cuando llueve',
       u'Solo cuando llueve.', u'Only when it rains.',
       [u'solo', u'cuando llueve'],
       [u'en el cuarto', u'hay una gotera', u'ideay', u'vaya pues'],
       [u'solo cuando llueve', u'cuando llueve'],
       [u'cuando llueve'],
       u'Which is the important half of the report, because in May it will be raining every afternoon and so will the roof.'),
  beat(u'Ah, ya. Le digo a mi hijo que suba a verlo.',
       u'Ask for it before the rains', u'¿lo puede ver?',
       u'¿Lo puede ver antes de las lluvias?', u'Could he look at it before the rains?',
       [u'¿lo puede ver', u'antes de las lluvias?'],
       [u'cuando llueve', u'en el cuarto', u'ni modo', u'vaya pues'],
       [u'lo puede ver antes de las lluvias', u'lo puede ver'],
       [u'¿lo puede ver?'],
       u'Ask for the timing as well as the fix. Antes de las lluvias is a real deadline here and everybody understands exactly how much time it means.'),
 ]},
{
 'id': 'barrio-09', 'district': 'barrio', 'tier': 3,
 'who': u'El del gas', 'title': u'El cilindro',
 'goal': u'Order a gas cylinder and be in when it comes',
 'culture': u'Cooking gas comes in a cylinder you swap, delivered off the '
            u'back of a truck. There is no pipe and no account, and delivery '
            u'is simply two people agreeing to be in the same place at the '
            u'same time.',
 'beats': [
  beat(u'¡Gaaas! ¿Gas, joven?',
       u'Order one', u'un cilindro',
       u'Un cilindro, por favor.', u'One cylinder, please.',
       [u'un cilindro', u'por favor'],
       [u'de veinticinco', u'¿a qué hora?', u'así es', u'con permiso'],
       [u'un cilindro por favor', u'un cilindro'],
       [u'un cilindro'],
       u'Gas arrives on a truck with a loudspeaker and you buy it by shouting back. There is no pipe to any house on this street.'),
  beat(u'¿De veinticinco o de cien libras?',
       u'The twenty-five', u'de veinticinco',
       u'De veinticinco.', u'The twenty-five.',
       [u'de veinticinco'],
       [u'de cien', u'un cilindro', u'gracias', u'así es'],
       [u'de veinticinco'],
       [u'de veinticinco'],
       u'Twenty-five pounds is the household one and one person can carry it. The hundred is for a comedor.'),
  beat(u'Se lo mando hoy mismo.',
       u'Ask what time', u'¿a qué hora?',
       u'¿A qué hora me lo trae?', u'What time will you bring it?',
       [u'¿a qué hora', u'me lo trae?'],
       [u'un cilindro', u'de veinticinco', u'con permiso', u'me deja en'],
       [u'a que hora me lo trae', u'a que hora'],
       [u'¿a qué hora?'],
       u'Ask, because somebody has to open the door and hand over the empty one, and that somebody is you.'),
  beat(u'Como a las tres de la tarde.',
       u'Say you will be in', u'aquí estoy',
       u'A las tres aquí estoy.', u'I’ll be here at three.',
       [u'a las tres', u'aquí estoy'],
       [u'¿a qué hora?', u'un cilindro', u'así es', u'con permiso'],
       [u'a las tres aqui estoy', u'aqui estoy'],
       [u'aquí estoy'],
       u'Aquí estoy — I will be here. That is the whole of the delivery contract and both halves of it are spoken.'),
 ]},
{
 'id': 'barrio-10', 'district': 'barrio', 'tier': 4,
 'who': u'La vecina', 'title': u'El velorio',
 'goal': u'Say the right thing at a wake, which is almost nothing',
 'culture': u'The wake is in the house, all night, door open, chairs out in '
            u'the street and coffee going. You go in, you say four words, you '
            u'sit down for twenty minutes. Saying too much is the mistake. '
            u'Not going at all is the bigger one, and it will be noticed.',
 'beats': [
  beat(u'(La puerta está abierta. Hay sillas en la calle y café.)',
       u'Say you are sorry', u'lo siento mucho',
       u'Lo siento mucho.', u'I’m very sorry.',
       [u'lo siento mucho'],
       [u'mi pésame', u'era buena gente', u'cuídese', u'dale'],
       [u'lo siento mucho'],
       [u'lo siento mucho'],
       u'Four syllables, and then stop. The mistake at a wake is never saying too little.'),
  beat(u'Gracias, vecino. Pase, pase adelante.',
       u'Offer your condolences properly', u'mi pésame',
       u'Mi pésame, doña.', u'My condolences, doña.',
       [u'mi pésame', u'doña'],
       [u'lo siento mucho', u'era buena gente', u'fíjese que', u'dale'],
       [u'mi pesame dona', u'mi pesame'],
       [u'mi pésame'],
       u'Mi pésame is the fixed phrase, and using it says you know what to do — which at that door is worth a great deal more than sincerity you cannot express yet.'),
  beat(u'Setenta y ocho años tenía. Se fue tranquilo, gracias a Dios.',
       u'Say something about him', u'era buena gente',
       u'Era buena gente.', u'He was a good sort.',
       [u'era buena gente'],
       [u'mi pésame', u'lo siento mucho', u'cuídese', u'fíjese que'],
       [u'era buena gente'],
       [u'era buena gente'],
       u'Buena gente is the highest ordinary praise there is here, and it is exactly what you say about somebody you did not know well. It is not a lie; it is the form.'),
  beat(u'Aquí estamos, pues. Toda la noche vamos a estar.',
       u'Say you will stay a while', u'aquí estamos',
       u'Aquí estamos. Me quedo un rato.', u'We’re here. I’ll stay a while.',
       [u'aquí estamos', u'me quedo un rato'],
       [u'mi pésame', u'cuídese', u'dale', u'fíjese que'],
       [u'aqui estamos me quedo un rato', u'aqui estamos'],
       [u'aquí estamos'],
       u'Aquí estamos — we are here. It means what it says: nobody is going anywhere, and for the next twenty minutes neither are you.'),
 ]},
{
 'id': 'barrio-11', 'district': 'barrio', 'tier': 4,
 'who': u'Doña Chepa', 'title': u'La indirecta',
 'goal': u'Realise you are being told off without being told off',
 'culture': u'The indirecta is a whole grammar of complaint and the point of '
            u'it is that nobody has to be embarrassed. Recognising it is the '
            u'skill. Answering it directly — naming yourself, apologising '
            u'outright — is a bigger breach than whatever you did.',
 'beats': [
  beat(u'No es por nada, vecino, pero...',
       u'You know what is coming — let it come', u'no es por nada',
       u'¿No es por nada?', u'It’s nothing, is it?',
       [u'¿no es por nada?'],
       [u'algunos', u'yo no digo nombres', u'no ando', u'ya va'],
       [u'no es por nada'],
       [u'no es por nada'],
       u'No es por nada means it is very much about something. When a sentence opens like this, what follows is about you.'),
  beat(u'...algunos sacan la basura el día que no toca, fíjese.',
       u'Acknowledge the some people', u'algunos',
       u'Ah. Algunos.', u'Ah. Some people.',
       [u'ah', u'algunos'],
       [u'no es por nada', u'yo no digo nombres', u'ya va', u'que le vaya bien'],
       [u'ah algunos', u'algunos'],
       [u'algunos'],
       u'Algunos — some people. There is exactly one person in the algunos and both of you know which one.'),
  beat(u'Yo no digo nombres, ¿va? Yo no soy así.',
       u'Play it perfectly straight', u'yo no digo nombres',
       u'Usted no dice nombres.', u'You don’t name names.',
       [u'usted no dice nombres'],
       [u'algunos', u'no es por nada', u'ya va', u'no ando'],
       [u'usted no dice nombres'],
       [u'yo no digo nombres'],
       u'Naming yourself would embarrass her, and the entire architecture of the indirecta exists so that nobody has to be embarrassed. Play it straight.'),
  beat(u'Usted entienda, pues.',
       u'Answer with what you will do', u'entienda',
       u'Ya entendí, doña. Mañana la saco.', u'I understand, doña. I’ll put it out tomorrow.',
       [u'ya entendí', u'doña', u'mañana la saco'],
       [u'algunos', u'no es por nada', u'que le vaya bien', u'ya va'],
       [u'ya entendi dona manana la saco', u'ya entendi dona', u'ya entendi'],
       [u'entienda'],
       u'Answer with the action and never with an admission. Say what you will do differently and the whole thing closes with neither of you having said it out loud.'),
 ]},
{
 'id': 'barrio-12', 'district': 'barrio', 'tier': 4,
 'who': u'El vecino', 'title': u'El favor',
 'goal': u'Be asked a favour you would rather not do',
 'culture': u'A flat no is expensive between neighbours, so the language does '
            u'the work instead. Fíjese que and es que buy you room, déjeme '
            u'ver is a real answer, and no le prometo is the honest end of '
            u'it. Saying yes and not turning up would cost far more.',
 'beats': [
  beat(u'Vecino, fíjese que necesito que me cuide la casa el fin de semana.',
       u'Buy yourself some room', u'fíjese que',
       u'Fíjese que... no sé.', u'Well now... I’m not sure.',
       [u'fíjese que', u'no sé'],
       [u'es que', u'déjeme ver', u'no le prometo', u'disculpe'],
       [u'fijese que no se', u'fijese que'],
       [u'fíjese que'],
       u'Fíjese que back at him is a stall and a softener at once. It signals that a but is coming without committing you to it yet.'),
  beat(u'Es un ratito nomás. ¿Puede o no puede?',
       u'Start the reason', u'es que',
       u'Es que voy a estar fuera.', u'It’s just that I’ll be away.',
       [u'es que', u'voy a estar fuera'],
       [u'fíjese que', u'déjeme ver', u'no le prometo', u'otro día'],
       [u'es que voy a estar fuera', u'es que'],
       [u'es que'],
       u'Es que introduces a reason, and half the time the reason never arrives. It is the most useful two words for declining anything in this country.'),
  beat(u'Ah. ¿Y no puede aunque sea el sábado?',
       u'Do not commit', u'déjeme ver',
       u'Déjeme ver.', u'Let me see.',
       [u'déjeme ver'],
       [u'es que', u'fíjese que', u'no le prometo', u'disculpe'],
       [u'dejeme ver'],
       [u'déjeme ver'],
       u'Déjeme ver — let me see. It is a real answer here rather than a brush-off, and it is understood as one by both sides.'),
  beat(u'Va pues. Me avisa, entonces.',
       u'Be honest about the odds', u'no le prometo',
       u'Le aviso, pero no le prometo.', u'I’ll let you know, but I’m not promising.',
       [u'le aviso', u'pero no le prometo'],
       [u'déjeme ver', u'es que', u'disculpe', u'otro día'],
       [u'le aviso pero no le prometo', u'no le prometo'],
       [u'no le prometo'],
       u'No le prometo is the honest end of it. Saying yes and then not turning up would cost you the street, and this costs you nothing.'),
 ]},
{
 'id': 'barrio-13', 'district': 'barrio', 'tier': 5,
 'who': u'Doña Marta', 'title': u'El aumento',
 'goal': u'Be told the rent is going up, and negotiate',
 'culture': u'She is not a company and there is no contract to point at, '
            u'which cuts both ways: she can raise it whenever she likes and '
            u'she can also just decide not to. Es mucho said plainly, and a '
            u'number in the middle, is the whole of the negotiation.',
 'beats': [
  beat(u'Mi hijo, fíjese que el alquiler va a subir.',
       u'Get the number first', u'va a subir',
       u'¿Va a subir? ¿Cuánto?', u'It’s going up? By how much?',
       [u'¿va a subir?', u'¿cuánto?'],
       [u'¿desde cuándo?', u'es mucho', u'gracias', u'Buenas'],
       [u'va a subir cuanto', u'va a subir'],
       [u'va a subir'],
       u'Va a subir — it is going up. Ask the number before you say anything else, because the number is the only part that is negotiable.'),
  beat(u'A ciento treinta, mi hijo.',
       u'Ask from when', u'¿desde cuándo?',
       u'¿Y desde cuándo?', u'And from when?',
       [u'¿y desde cuándo?'],
       [u'va a subir', u'es mucho', u'gracias', u'por favor'],
       [u'y desde cuando', u'desde cuando'],
       [u'¿desde cuándo?'],
       u'The date is worth as much as the number. A rise next month and a rise today are two different conversations.'),
  beat(u'Desde el mes que viene.',
       u'Say it is a lot — and stop', u'es mucho',
       u'Es mucho, doña. De verdad.', u'That’s a lot, doña. Honestly.',
       [u'es mucho', u'doña', u'de verdad'],
       [u'va a subir', u'¿desde cuándo?', u'gracias', u'por favor'],
       [u'es mucho dona de verdad', u'es mucho dona', u'es mucho'],
       [u'es mucho'],
       u'Es mucho, said flatly and then nothing. She is not a company, and she may not have thought about it from your side until you said it out loud.'),
  beat(u'Bueno... ¿y usted qué dice, pues?',
       u'Propose the middle', u'quedemos en',
       u'Quedemos en ciento quince.', u'Let’s settle on a hundred and fifteen.',
       [u'quedemos en', u'ciento quince'],
       [u'es mucho', u'va a subir', u'gracias', u'Buenas'],
       [u'quedemos en ciento quince', u'quedemos en'],
       [u'quedemos en'],
       u'Quedemos en — let’s settle on. The same move as the leather bag in the market, and it works here for exactly the same reason.'),
 ]},
{
 'id': 'barrio-14', 'district': 'barrio', 'tier': 5,
 'who': u'Todos', 'title': u'La cuadra',
 'goal': u'Be greeted first, by everybody, on your own street',
 'culture': u'This is what all of it was for. Nobody on this block greets a '
            u'stranger first; they greet you now. And adiós shouted at '
            u'somebody you are walking past means hello, not goodbye, which '
            u'is the single most confusing thing in Nicaraguan Spanish and '
            u'stops being confusing here.',
 'beats': [
  beat(u'(Una señora pasa en la acera de enfrente.) ¡Adiós!',
       u'Answer it', u'adiós',
       u'¡Adiós!', u'Hello!',
       [u'¡adiós!'],
       [u'buenas', u'¿cómo amaneció?', u'ahí vamos', u'está bien'],
       [u'adios'],
       [u'adiós'],
       u'Adiós, shouted at somebody you are walking past, means hello. Not goodbye. This is the moment it stops confusing you.'),
  beat(u'(Don Chombo, en su silla, levanta la mano.) Buenas.',
       u'Greet him back, by name', u'buenas',
       u'Buenas, don Chombo.', u'Morning, don Chombo.',
       [u'buenas', u'don Chombo'],
       [u'adiós', u'ahí vamos', u'me da', u'quiero'],
       [u'buenas don chombo', u'buenas'],
       [u'buenas'],
       u'The same word you learned on your first night at the hostel, said now to a man whose name you know and who was expecting you.'),
  beat(u'¿Y cómo amaneció, vecino?',
       u'Ask it back', u'¿cómo amaneció?',
       u'Bien, ¿y usted? ¿Cómo amaneció?', u'Well, and you? How did you wake up?',
       [u'bien', u'¿y usted?', u'¿cómo amaneció?'],
       [u'adiós', u'ahí vamos', u'está bien', u'me da'],
       [u'bien y usted como amanecio', u'como amanecio'],
       [u'¿cómo amaneció?'],
       u'¿Cómo amaneció? is how did you wake up, and it is the morning greeting between people who live on the same street. It is being asked OF you.'),
  beat(u'Ahí vamos, gracias a Dios. Ahí vamos.',
       u'Say it yourself', u'ahí vamos',
       u'Ahí vamos.', u'Getting along.',
       [u'ahí vamos'],
       [u'adiós', u'buenas', u'está bien', u'quiero'],
       [u'ahi vamos'],
       [u'ahí vamos'],
       u'Ahí vamos — we are getting along. Not good, not bad, still going. It is the answer everybody gives, and now it is yours, on your own street.'),
 ]},
# ── El trabajo ──────────────────────────────────────────────────────────
{
 'id': 'trabajo-01', 'district': 'trabajo', 'tier': 1,
 'who': u'Doña Chepa', 'title': u'El mandado',
 'goal': u'Earn your first córdobas carrying somebody else’s shopping',
 'culture': u'The mirror of the cargador in the market: there you paid, and '
            u'agreeing the price first was the etiquette. Here you are the '
            u'one carrying, and letting her name the figure is the move — '
            u'the work is small and she is a neighbour.',
 'beats': [
  beat(u'(Va cargada con cuatro bolsas y le falta media cuadra.)',
       u'Offer to carry it', u'yo se lo llevo',
       u'Yo se lo llevo, doña.', u'I’ll carry it for you, doña.',
       [u'yo se lo llevo', u'doña'],
       [u'¿cuánto me da?', u'cuando quiera', u'ideay', u'ni modo'],
       [u'yo se lo llevo dona', u'yo se lo llevo'],
       [u'yo se lo llevo'],
       u'The same sentence the porter used on you in the market, now coming out of your mouth. That is the whole arc of this district in one line.'),
  beat(u'¡Ay, sí, mi hijo! ¿Y cuánto me cobra?',
       u'Let her name it', u'¿cuánto me da?',
       u'¿Cuánto me da usted?', u'What will you give me?',
       [u'¿cuánto me da', u'usted?'],
       [u'yo se lo llevo', u'cuando quiera', u'vaya pues', u'ni modo'],
       [u'cuanto me da usted', u'cuanto me da'],
       [u'¿cuánto me da?'],
       u'¿Cuánto me da? lets her set it, which is right when the work is small and the person is a neighbour. ¿Cuánto me cobra? was for when you were the one buying.'),
  beat(u'Le doy veinte, ¿le parece?',
       u'Take it', u'está bien',
       u'Está bien. Vamos.', u'That’s fine. Let’s go.',
       [u'está bien', u'vamos'],
       [u'¿cuánto me da?', u'ideay', u'ni modo', u'vaya pues'],
       [u'esta bien vamos', u'esta bien'],
       [u'está bien'],
       u'Twenty córdobas for three blocks. It is not much and it is the first money you have earned in Spanish, which is a different thing.'),
  beat(u'Gracias, mi hijo. Cuando quiera, ahí me busca.',
       u'Say the same back', u'cuando quiera',
       u'Cuando quiera, doña.', u'Any time, doña.',
       [u'cuando quiera', u'doña'],
       [u'está bien', u'vaya pues', u'ni modo', u'ideay'],
       [u'cuando quiera dona', u'cuando quiera'],
       [u'cuando quiera'],
       u'Cuando quiera — whenever you like. It is an offer of more work, and the correct answer is the same two words straight back.'),
 ]},
{
 'id': 'trabajo-02', 'district': 'trabajo', 'tier': 2,
 'who': u'Don Emilio', 'title': u'El taller',
 'goal': u'Ask for work and be told what you are actually worth',
 'culture': u'Busco trabajo is not an embarrassing thing to say here and he '
            u'has been asked it a hundred times. He is not deciding whether '
            u'you are a mechanic; he is deciding whether you are worth a '
            u'week, and overselling yourself is the fastest way back onto the '
            u'street.',
 'beats': [
  beat(u'Buenas. ¿Qué se le ofrece, joven?',
       u'Say it straight out', u'busco trabajo',
       u'Busco trabajo, don Emilio.', u'I’m looking for work, don Emilio.',
       [u'busco trabajo', u'don Emilio'],
       [u'sé un poco', u'aprendo rápido', u'así es', u'con permiso'],
       [u'busco trabajo don emilio', u'busco trabajo'],
       [u'busco trabajo'],
       u'No preamble. Busco trabajo is not embarrassing to say in this country and he has heard it a hundred times without thinking less of anybody.'),
  beat(u'¿Y usted sabe de esto o no sabe nada?',
       u'Be honest', u'sé un poco',
       u'Sé un poco. No mucho.', u'I know a little. Not much.',
       [u'sé un poco', u'no mucho'],
       [u'busco trabajo', u'aprendo rápido', u'así es', u'me deja en'],
       [u'se un poco no mucho', u'se un poco'],
       [u'sé un poco'],
       u'Sé un poco is the answer that survives the first hour. Claiming more than you have is the fastest way out of a workshop.'),
  beat(u'Hm.',
       u'Give him the reason to try', u'aprendo rápido',
       u'Pero aprendo rápido.', u'But I learn fast.',
       [u'pero', u'aprendo rápido'],
       [u'sé un poco', u'busco trabajo', u'con permiso', u'así es'],
       [u'pero aprendo rapido', u'aprendo rapido'],
       [u'aprendo rápido'],
       u'The pero does all the work. He is weighing a week of his time, not your qualifications.'),
  beat(u'¿Y por qué le voy a dar chance a usted?',
       u'Ask him to try you', u'pruébeme',
       u'Pruébeme una semana.', u'Give me a week’s trial.',
       [u'pruébeme', u'una semana'],
       [u'aprendo rápido', u'sé un poco', u'así es', u'me deja en'],
       [u'pruebeme una semana', u'pruebeme'],
       [u'pruébeme'],
       u'Pruébeme — try me. It costs him almost nothing to agree to and it is the one argument he has no answer for.'),
 ]},
{
 'id': 'trabajo-03', 'district': 'trabajo', 'tier': 2,
 'who': u'Marcos', 'title': u'El compañero',
 'goal': u'Make your first real friend at work',
 'culture': u'¿Qué pasó? is hello between men who work together. Nothing has '
            u'happened and he does not want to know what has. This is also '
            u'where you switch to vos for good with somebody your own age, '
            u'and getting that switch right is worth more than any verb '
            u'table.',
 'beats': [
  beat(u'¿Qué pasó, pues?',
       u'Answer the greeting', u'¿qué pasó?',
       u'¿Qué pasó, Marcos?', u'How’s it going, Marcos?',
       [u'¿qué pasó', u'Marcos?'],
       [u'todo bien', u'vamos', u'nos vemos', u'cuídese'],
       [u'que paso marcos', u'que paso'],
       [u'¿qué pasó?'],
       u'¿Qué pasó? is hello, not a question. Nothing has happened, and answering it as though something had is the mistake every learner makes once.'),
  beat(u'¿Todo bien?',
       u'All good — and ask him back', u'todo bien',
       u'Todo bien. ¿Y vos?', u'All good. And you?',
       [u'todo bien', u'¿y vos?'],
       [u'¿qué pasó?', u'vamos', u'nos vemos', u'dale'],
       [u'todo bien y vos', u'todo bien'],
       [u'todo bien'],
       u'¿Y vos? He is a workmate your own age, so it is vos from here on, permanently. That switch is worth more than any verb table you will ever learn.'),
  beat(u'Todo bien. ¿Vamos a almorzar?',
       u'Go with him', u'vamos',
       u'Vamos. Dale.', u'Let’s go. Right.',
       [u'vamos', u'dale'],
       [u'todo bien', u'nos vemos', u'fíjese que', u'cuídese'],
       [u'vamos dale', u'vamos'],
       [u'vamos'],
       u'Vamos is let’s go and dale is alright. Between them they arrange nearly everything that happens after work.'),
  beat(u'Bueno, ya me voy. Nos vemos mañana.',
       u'Say goodbye like a workmate', u'nos vemos',
       u'Nos vemos, Marcos.', u'See you, Marcos.',
       [u'nos vemos', u'Marcos'],
       [u'vamos', u'todo bien', u'cuídese', u'dale'],
       [u'nos vemos marcos', u'nos vemos'],
       [u'nos vemos'],
       u'Nos vemos — see you. Cuídese is for the doña on the corner; between the two of you it is this, and using the wrong one is audible.'),
 ]},
{
 'id': 'trabajo-04', 'district': 'trabajo', 'tier': 3,
 'who': u'Don Emilio', 'title': u'La jerarquía',
 'goal': u'Learn who you may and may not contradict',
 'culture': u'The workshop has an order to it and none of it is written down. '
            u'You do not walk up and start talking, you do not argue in front '
            u'of a customer, and you do not decide anything that is not '
            u'yours to decide. None of that is servility; it is how the place '
            u'runs and everybody in it is protected by it.',
 'beats': [
  beat(u'(Don Emilio está con un cliente. Usted necesita preguntarle algo.)',
       u'Knock, so to speak', u'con permiso',
       u'Con permiso, don Emilio.', u'Excuse me, don Emilio.',
       [u'con permiso', u'don Emilio'],
       [u'usted dirá', u'como usted diga', u'está bien', u'me da'],
       [u'con permiso don emilio', u'con permiso'],
       [u'con permiso'],
       u'You do not walk up and start talking. Con permiso is the knock on the door, and skipping it is the loudest thing you can do in a quiet workshop.'),
  beat(u'Usted dirá, joven.',
       u'He has given you the floor — be brief', u'usted dirá',
       u'Es sobre el trabajo del lunes.', u'It’s about Monday’s job.',
       [u'es sobre', u'el trabajo del lunes'],
       [u'como usted diga', u'no me toca', u'está bien', u'quiero'],
       [u'es sobre el trabajo del lunes', u'es sobre'],
       [u'usted dirá'],
       u'Usted dirá means go on, I am listening. It is a small formality that tells you he is the one granting the turn — so take it and be short.'),
  beat(u'Eso lo hacemos como siempre. No me lo cambie.',
       u'Accept the decision', u'como usted diga',
       u'Como usted diga.', u'As you say.',
       [u'como usted diga'],
       [u'no me toca', u'usted dirá', u'está bien', u'me da'],
       [u'como usted diga'],
       [u'como usted diga'],
       u'Como usted diga is not servility. It closes a decision that was never yours, it costs nothing, and it is why he will listen next time you do have something.'),
  beat(u'(Un cliente le pregunta a USTED si puede rebajarle el precio.)',
       u'Say it is not yours to decide', u'no me toca',
       u'No me toca a mí. Pregúntele a don Emilio.', u'That’s not mine to decide. Ask don Emilio.',
       [u'no me toca a mí', u'pregúntele a don Emilio'],
       [u'como usted diga', u'usted dirá', u'quiero', u'me da'],
       [u'no me toca a mi preguntele a don emilio', u'no me toca a mi',
        u'no me toca'],
       [u'no me toca'],
       u'No me toca — it is not mine to decide. It protects you and it points the customer at the one person who can actually answer him.'),
 ]},
{
 'id': 'trabajo-05', 'district': 'trabajo', 'tier': 3,
 'who': u'Marcos', 'title': u'La quincena',
 'goal': u'Survive the week before payday',
 'culture': u'La quincena is the fifteenth and the last day of the month, and '
            u'the whole country is broke for the three days before each one. '
            u'Being skint is not embarrassing because everybody is skint on '
            u'exactly the same day.',
 'beats': [
  beat(u'¿Vamos por una fría?',
       u'Say you are skint', u'no ando',
       u'No ando con nada.', u'I haven’t got a thing.',
       [u'no ando con nada'],
       [u'hasta la quincena', u'me presta', u'ideay', u'ni modo'],
       [u'no ando con nada'],
       [u'no ando'],
       u'The same phrase you used on the friendly drunk in the park, now said to a friend. It carries no shame here at all.'),
  beat(u'Ideay, ¿y eso?',
       u'Until payday', u'hasta la quincena',
       u'Hasta la quincena.', u'Not till payday.',
       [u'hasta la quincena'],
       [u'no ando con nada', u'me presta', u'vaya pues', u'ni modo'],
       [u'hasta la quincena'],
       [u'hasta la quincena'],
       u'La quincena is the fifteenth and the thirtieth. Everybody in the country is broke on the same three days and everybody knows it.'),
  beat(u'Yo tampoco ando... bueno, algo tengo.',
       u'Ask for the loan', u'me presta',
       u'¿Me presta cien?', u'Could you lend me a hundred?',
       [u'¿me presta', u'cien?'],
       [u'hasta la quincena', u'se lo devuelvo', u'ideay', u'vaya pues'],
       [u'me presta cien', u'me presta'],
       [u'me presta'],
       u'Me presta — usted, even to a friend you call vos. Asking for money is the one place people go formal with somebody close, and copying that is worth noticing.'),
  beat(u'Va pues. Tenga.',
       u'Promise the day back', u'se lo devuelvo',
       u'Se lo devuelvo el viernes.', u'I’ll give it back on Friday.',
       [u'se lo devuelvo', u'el viernes'],
       [u'me presta', u'hasta la quincena', u'ni modo', u'ideay'],
       [u'se lo devuelvo el viernes', u'se lo devuelvo'],
       [u'se lo devuelvo'],
       u'Name the day. The lending was easy; the giving back is what decides whether there is ever a second time.'),
 ]},
{
 'id': 'trabajo-06', 'district': 'trabajo', 'tier': 3,
 'who': u'El cliente', 'title': u'El cliente',
 'goal': u'Explain a delay to somebody who does not want to hear it',
 'culture': u'Bad news first and in four words. Then a real day — not '
            u'ahorita and not mañana, both of which mean neither. Then one '
            u'apology, once: apologising three times makes it sound like it '
            u'is going to happen again.',
 'beats': [
  beat(u'Vengo por lo mío. ¿Ya está listo?',
       u'Say it plainly', u'no está listo',
       u'Todavía no está listo.', u'It’s not ready yet.',
       [u'todavía', u'no está listo'],
       [u'para el lunes', u'le aviso', u'así es', u'con permiso'],
       [u'todavia no esta listo', u'no esta listo'],
       [u'no está listo'],
       u'Say it first and plainly. Everything after this is easier once the bad news is out of the way in four words.'),
  beat(u'¿Y para cuándo, pues?',
       u'Give a real day', u'para el lunes',
       u'Para el lunes.', u'By Monday.',
       [u'para el lunes'],
       [u'para mañana', u'le aviso', u'así es', u'me deja en'],
       [u'para el lunes'],
       [u'para el lunes'],
       u'A day you can keep. Ahorita and mañana are what people say when they mean neither, and he has heard both already this week.'),
  beat(u'Uy. Bueno, ni modo.',
       u'Promise to tell him', u'le aviso',
       u'Le aviso cuando esté.', u'I’ll let you know when it’s done.',
       [u'le aviso', u'cuando esté'],
       [u'para el lunes', u'no está listo', u'con permiso', u'así es'],
       [u'le aviso cuando este', u'le aviso'],
       [u'le aviso'],
       u'Le aviso — I will let you know. The same word the neighbour used about the water coming back, and it carries the same obligation.'),
  beat(u'Está bien, joven. Aquí lo espero.',
       u'Apologise once', u'una disculpa',
       u'Una disculpa, de verdad.', u'My apologies, truly.',
       [u'una disculpa', u'de verdad'],
       [u'le aviso', u'para el lunes', u'así es', u'me deja en'],
       [u'una disculpa de verdad', u'una disculpa'],
       [u'una disculpa'],
       u'Once, and then stop. Apologising three times makes it sound like it is going to happen again.'),
 ]},
{
 'id': 'trabajo-07', 'district': 'trabajo', 'tier': 4,
 'who': u'Don Emilio', 'title': u'El error',
 'goal': u'Own a mistake that cost money',
 'culture': u'Say it before anybody looks around. He forgives the mistake and '
            u'not the lie, and the whole ritual is four short sentences — own '
            u'it, confirm it, fix it, promise once. Tomorrow nobody will '
            u'mention it again.',
 'beats': [
  beat(u'¿Y esto? ¿Quién hizo esto?',
       u'Own it immediately', u'fue mío',
       u'Fue mío, don Emilio.', u'That was me, don Emilio.',
       [u'fue mío', u'don Emilio'],
       [u'yo lo hice', u'lo arreglo', u'cuídese', u'dale'],
       [u'fue mio don emilio', u'fue mio'],
       [u'fue mío'],
       u'Immediately, before anybody starts looking around. Fue mío is two words and it is the difference between a mistake and a problem.'),
  beat(u'¿Usted?',
       u'Confirm it', u'yo lo hice',
       u'Yo lo hice. Sí.', u'I did it. Yes.',
       [u'yo lo hice', u'sí'],
       [u'fue mío', u'lo arreglo', u'fíjese que', u'dale'],
       [u'yo lo hice si', u'yo lo hice'],
       [u'yo lo hice'],
       u'No explanation yet. He asked a yes-or-no question and the only thing that helps you is the yes.'),
  beat(u'¿Y ahora qué hacemos?',
       u'Move to the fix', u'lo arreglo',
       u'Lo arreglo hoy mismo.', u'I’ll fix it today.',
       [u'lo arreglo', u'hoy mismo'],
       [u'fue mío', u'no vuelve a pasar', u'cuídese', u'dale'],
       [u'lo arreglo hoy mismo', u'lo arreglo'],
       [u'lo arreglo'],
       u'Get to the fix as fast as you can. He is not interested in how you feel about it, and telling him would make it about you.'),
  beat(u'Le va a costar a usted, ¿oyó?',
       u'Take it and promise once', u'no vuelve a pasar',
       u'Está bien. No vuelve a pasar.', u'Alright. It won’t happen again.',
       [u'está bien', u'no vuelve a pasar'],
       [u'lo arreglo', u'fue mío', u'fíjese que', u'dale'],
       [u'esta bien no vuelve a pasar', u'no vuelve a pasar'],
       [u'no vuelve a pasar'],
       u'Take the cost without arguing and promise exactly once. That is the whole ritual, and tomorrow nobody mentions it again.'),
 ]},
{
 'id': 'trabajo-08', 'district': 'trabajo', 'tier': 4,
 'who': u'Marcos', 'title': u'La cerveza del viernes',
 'goal': u'Drink with workmates and keep up with the joking',
 'culture': u'Paying is fought over rather than negotiated, and losing '
            u'gracefully is part of it. Ya va la última is said about the '
            u'third of six and everybody knows it is not true, which is why '
            u'saying it is joining in rather than lying.',
 'beats': [
  beat(u'¡Viernes! ¿Nos tomamos algo?',
       u'Order a cold one', u'una fría',
       u'Una fría.', u'A cold one.',
       [u'una fría'],
       [u'yo invito', u'no seás así', u'no ando', u'todo bien'],
       [u'una fria'],
       [u'una fría'],
       u'Una fría — a cold one. Nobody orders beer by its name; the temperature is the part that matters.'),
  beat(u'Yo pago, dale.',
       u'Fight him for it', u'yo invito',
       u'No, yo invito.', u'No, it’s on me.',
       [u'no', u'yo invito'],
       [u'una fría', u'no seás así', u'ya va', u'todo bien'],
       [u'no yo invito', u'yo invito'],
       [u'yo invito'],
       u'Yo invito — my treat. It is fought over rather than negotiated, and losing the fight gracefully is part of the ritual.'),
  beat(u'¡No! Vos pagaste la vez pasada.',
       u'Push back the way he would', u'no seás así',
       u'No seás así.', u'Don’t be like that.',
       [u'no seás así'],
       [u'yo invito', u'una fría', u'ya va', u'no ando'],
       [u'no seas asi'],
       [u'no seás así'],
       u'No seás así — don’t be like that. VOS: seás, not seas. It is the same phrase doña Chepa used about the gossip, in the vos form because he is your friend.'),
  beat(u'Bueno, bueno. Ya va la última, ¿va?',
       u'Agree it is the last one', u'ya va la última',
       u'Ya va la última. Dale.', u'Last one, then. Right.',
       [u'ya va la última', u'dale'],
       [u'yo invito', u'una fría', u'no ando', u'todo bien'],
       [u'ya va la ultima dale', u'ya va la ultima'],
       [u'ya va la última'],
       u'Ya va la última is said about the third of six and everybody at the table knows it. Saying it is joining in, not lying.'),
 ]},
{
 'id': 'trabajo-09', 'district': 'trabajo', 'tier': 5,
 'who': u'Don Emilio', 'title': u'El aumento del sueldo',
 'goal': u'Ask for more money without insulting anybody',
 'culture': u'Alone, early, and never in front of anybody. The imperfect does '
            u'the softening — quería, I was wanting to — and naming your own '
            u'number invites a no. Hand him the decision and he has to live '
            u'up to it.',
 'beats': [
  beat(u'¿Qué pasó, joven? ¿Todo bien?',
       u'Open it softly', u'quería hablarle',
       u'Quería hablarle un momento.', u'I wanted to have a word.',
       [u'quería hablarle', u'un momento'],
       [u'ya llevo', u'lo que usted crea', u'nos vemos', u'vamos'],
       [u'queria hablarle un momento', u'queria hablarle'],
       [u'quería hablarle'],
       u'The imperfect softens it: quería, I was wanting to. Quiero hablarle would be a confrontation, and this is not one.'),
  beat(u'Dígame, pues.',
       u'State the fact, not the demand', u'ya llevo',
       u'Ya llevo ocho meses aquí.', u'I’ve been here eight months now.',
       [u'ya llevo', u'ocho meses aquí'],
       [u'quería hablarle', u'lo que usted crea', u'vamos', u'que le vaya bien'],
       [u'ya llevo ocho meses aqui', u'ya llevo'],
       [u'ya llevo'],
       u'Ya llevo — I have been here this long already. A fact rather than a demand, and he can do the arithmetic himself without being asked to.'),
  beat(u'Ajá. ¿Y cuánto quiere usted?',
       u'Hand him the decision', u'lo que usted crea',
       u'Lo que usted crea justo.', u'Whatever you think is fair.',
       [u'lo que usted crea', u'justo'],
       [u'ya llevo', u'quería hablarle', u'nos vemos', u'vamos'],
       [u'lo que usted crea justo', u'lo que usted crea'],
       [u'lo que usted crea'],
       u'Naming a number invites a no. Lo que usted crea makes it about what is fair, and then he has to be fair in front of himself.'),
  beat(u'Le subo quinientos desde la quincena.',
       u'Thank him and go', u'le agradezco',
       u'Le agradezco, don Emilio.', u'I’m grateful, don Emilio.',
       [u'le agradezco', u'don Emilio'],
       [u'lo que usted crea', u'ya llevo', u'vamos', u'nos vemos'],
       [u'le agradezco don emilio', u'le agradezco'],
       [u'le agradezco'],
       u'Le agradezco, not gracias — a size up, for something that cost him a decision. And then leave: staying to talk about it would undo it.'),
 ]},
{
 'id': 'trabajo-10', 'district': 'trabajo', 'tier': 5,
 'who': u'El nuevo', 'title': u'El nuevo',
 'goal': u'Teach somebody newer than you, in Spanish',
 'culture': u'The last mission of the district, and the first time you are '
            u'the one who knows. He is newer than you, so he gets vos — '
            u'ponete, mirá, seguí — and you teach the way don Emilio taught '
            u'you, which is two words and then showing him.',
 'beats': [
  beat(u'Buenas... me dijeron que le preguntara a usted.',
       u'Put him where he should be', u'ponete aquí',
       u'Ponete aquí, a la par mía.', u'Stand here, next to me.',
       [u'ponete aquí', u'a la par mía'],
       [u'así no', u'mirá', u'vas bien', u'disculpe'],
       [u'ponete aqui a la par mia', u'ponete aqui'],
       [u'ponete aquí'],
       u'Ponete — vos. He is newer than you, so he gets vos and you get to be the one who knows. A la par is beside; al lado is what a book would say.'),
  beat(u'(Lo agarra al revés.) ¿Así?',
       u'Stop him', u'así no',
       u'Así no. Mirá.', u'Not like that. Look.',
       [u'así no', u'mirá'],
       [u'ponete aquí', u'vas bien', u'otro día', u'disculpe'],
       [u'asi no mira', u'asi no'],
       [u'así no'],
       u'Así no — not like that. Two words, no explanation, and then you show him, which is exactly how don Emilio taught you in your first week.'),
  beat(u'Ah. ¿Y entonces cómo?',
       u'Show him', u'mirá',
       u'Mirá. Así, despacio.', u'Look. Like this, slowly.',
       [u'mirá', u'así', u'despacio'],
       [u'así no', u'ponete aquí', u'vas bien', u'¿a cómo?'],
       [u'mira asi despacio', u'mira asi', u'mira'],
       [u'mirá'],
       u'Mirá, not mira — the accent is the entire difference and it is the vos imperative. You have been hearing it since Guadalupe.'),
  beat(u'(Lo hace bien.) ¿Así está?',
       u'Tell him he is doing fine', u'vas bien',
       u'Vas bien. Seguí así.', u'You’re doing fine. Keep going.',
       [u'vas bien', u'seguí así'],
       [u'así no', u'mirá', u'ponete aquí', u'otro día'],
       [u'vas bien segui asi', u'vas bien'],
       [u'vas bien'],
       u'Vas bien — you’re doing fine. Seguí is vos again. This is the last mission of the district and you are the one saying it, which is the whole point of it.'),
 ]},
]

HINTS = [
 # Tu barrio
 {'kind': u'doña en la puerta', 'district': 'barrio',
  'says': u'¿Anda buscando cuarto? Doña Marta alquila por mes, ahí en la casa azul.',
  'en': u'Looking for a room? Doña Marta rents by the month, there in the blue house.',
  'points_at': ['barrio-01', 'barrio-02']},
 {'kind': u'chavalo en bici', 'district': 'barrio',
  'says': u'En la pulpería le fían si ya lo conocen. Pregúntele al pulpero, no tenga pena.',
  'en': u'The shop gives you credit once they know you. Ask the shopkeeper, do not be shy.',
  'points_at': ['barrio-03']},
 {'kind': u'obrero', 'district': 'barrio',
  'says': u'El barbero abre hasta las siete. Dígale bien cortito o le deja lo mismo.',
  'en': u'The barber is open till seven. Tell him nice and short or he leaves it the same.',
  'points_at': ['barrio-04']},
 {'kind': u'viejo de la esquina', 'district': 'barrio',
  'says': u'Esa vecina pone música hasta la madrugada. Pídale el favor, no se enoje, y la baja.',
  'en': u'That neighbour plays music till dawn. Ask her the favour, do not get cross, and she turns it down.',
  'points_at': ['barrio-05']},
 {'kind': u'vendedora', 'district': 'barrio',
  'says': u'Se fue la luz en toda la cuadra. El electricista anda por ahí, pregúntele a él.',
  'en': u'The power is out on the whole block. The electrician is about, ask him.',
  'points_at': ['barrio-06']},
 {'kind': u'doña en la puerta', 'district': 'barrio',
  'says': u'El chavalo Roberto le enseña más palabras que cualquier libro. Y unas que no debería.',
  'en': u'Young Roberto will teach you more words than any book. And a few he should not.',
  'points_at': ['barrio-07']},
 {'kind': u'obrero', 'district': 'barrio',
  'says': u'Si le gotea el techo, dígale a la dueña antes de mayo. Después no hay quien suba.',
  'en': u'If your roof leaks, tell the landlady before May. After that nobody will go up there.',
  'points_at': ['barrio-08']},
 {'kind': u'chavalo en bici', 'district': 'barrio',
  'says': u'El del gas pasa como a las tres. Encárguele el cilindro y espérelo en la casa.',
  'en': u'The gas man comes past about three. Order the cylinder and wait in for him.',
  'points_at': ['barrio-09']},
 {'kind': u'doña en la puerta', 'district': 'barrio',
  'says': u'Murió don Ramón. Están velando ahí al lado, toda la noche. Pase aunque sea un rato.',
  'en': u'Don Ramón has died. They are holding the wake next door, all night. Go in even for a while.',
  'points_at': ['barrio-10']},
 {'kind': u'viejo de la esquina', 'district': 'barrio',
  'says': u'Cuando doña Chepa dice "algunos", está hablando de usted. Fíjese bien.',
  'en': u'When doña Chepa says "some people", she means you. Pay attention.',
  'points_at': ['barrio-11']},
 {'kind': u'vendedora', 'district': 'barrio',
  'says': u'El vecino anda pidiendo que le cuiden la casa. Ya nos preguntó a todos.',
  'en': u'The neighbour is going round asking somebody to watch his house. He has asked all of us already.',
  'points_at': ['barrio-12']},
 {'kind': u'doña en la puerta', 'district': 'barrio',
  'says': u'Fíjese que a todos nos subió el alquiler este mes. Hable con ella, sí se puede.',
  'en': u'She has put all our rents up this month. Talk to her, it can be done.',
  'points_at': ['barrio-13']},
 {'kind': u'caponero', 'district': 'barrio',
  'says': u'Aquí lo saludan a uno primero. Si no contesta, al mes ya nadie lo saluda.',
  'en': u'Round here people greet you first. If you do not answer, in a month nobody greets you at all.',
  'points_at': ['barrio-14']},
 # El trabajo
 {'kind': u'doña en la puerta', 'district': 'trabajo',
  'says': u'Doña Chepa siempre viene cargada del mercado. Ofrézcase, que ella paga.',
  'en': u'Doña Chepa always comes back loaded from the market. Offer to help, she pays.',
  'points_at': ['trabajo-01']},
 {'kind': u'obrero', 'district': 'trabajo',
  'says': u'Don Emilio necesita quien le ayude en el taller. Vaya temprano y pregúntele.',
  'en': u'Don Emilio needs somebody to help in the workshop. Go early and ask him.',
  'points_at': ['trabajo-02']},
 {'kind': u'chavalo en bici', 'district': 'trabajo',
  'says': u'En el taller está Marcos, el más alegre de todos. Con ese se hace amigo rápido.',
  'en': u'Marcos is at the workshop, the cheeriest of the lot. You will be friends with him fast.',
  'points_at': ['trabajo-03', 'trabajo-08']},
 {'kind': u'obrero', 'district': 'trabajo',
  'says': u'En el taller no le lleve la contraria a don Emilio delante de la gente.',
  'en': u'In that workshop, do not contradict don Emilio in front of people.',
  'points_at': ['trabajo-04']},
 {'kind': u'viejo de la esquina', 'district': 'trabajo',
  'says': u'Antes de la quincena aquí nadie anda con nada. Ni pregunte.',
  'en': u'Before payday nobody round here has anything. Do not even ask.',
  'points_at': ['trabajo-05']},
 {'kind': u'vendedora', 'district': 'trabajo',
  'says': u'Ahí viene el cliente por su trabajo. Dígale la verdad de una vez, es peor después.',
  'en': u'Here comes the customer for his job. Tell him the truth straight away, it is worse later.',
  'points_at': ['trabajo-06']},
 {'kind': u'obrero', 'district': 'trabajo',
  'says': u'Si se equivoca, dígalo usted primero. Don Emilio perdona el error, no la mentira.',
  'en': u'If you make a mistake, say so first. Don Emilio forgives the mistake, not the lie.',
  'points_at': ['trabajo-07']},
 {'kind': u'obrero', 'district': 'trabajo',
  'says': u'Si va a pedir aumento, hable con él solo y temprano. Nunca delante de otros.',
  'en': u'If you are going to ask for a rise, talk to him alone and early. Never in front of others.',
  'points_at': ['trabajo-09']},
 {'kind': u'vendedora', 'district': 'trabajo',
  'says': u'Entró un muchacho nuevo al taller. Enséñele usted, que ya sabe cómo es.',
  'en': u'A new lad has started at the workshop. You teach him, you know how it goes now.',
  'points_at': ['trabajo-10']},
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

PUNCT = set(u"¿?¡!.,;:\"'«»()")


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
