# -*- coding: utf-8 -*-
"""Writes Trámites y salud (10) and El Malecón (8).

Trámites is the Spanish nobody teaches and everybody needs: what hurts, how
long, which window, what else do I need, and come back tomorrow without
getting cross. Half of it is repeating an instruction back so you actually
have it, because none of it is written down anywhere.

El Malecón is the lakefront on a Sunday: quesillo, fried guapote, a boat round
the isletas, a family who will feed you, and a night watchman telling you
kindly that it is time to go.

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
{
 'id': 'tramites-01', 'district': 'tramites', 'tier': 2,
 'who': u'La farmacéutica', 'title': u'La farmacia',
 'goal': u'Explain what hurts and get something for it',
 'culture': u'The pharmacist is the first line of medicine here, not the '
            u'doctor. You describe the symptom across the counter and she '
            u'hands you something out of a drawer, often without a '
            u'prescription — which is why saying algo suave matters.',
 'beats': [
  beat(u'Buenas. ¿Qué necesita?',
       u'Say what hurts', u'me duele',
       u'Me duele la cabeza.', u'I have a headache.',
       [u'me duele', u'la cabeza'],
       [u'desde ayer', u'algo suave', u'gracias', u'por favor'],
       [u'me duele la cabeza', u'me duele'],
       [u'me duele', u'la cabeza'],
       u'Me duele plus the part of you. It is the sentence that gets you seen anywhere in this country, and she is where you start, not the clinic.'),
  beat(u'¿Y desde cuándo?',
       u'Since yesterday', u'desde ayer',
       u'Desde ayer.', u'Since yesterday.',
       [u'desde ayer'],
       [u'desde hoy', u'me duele', u'gracias', u'por favor'],
       [u'desde ayer'],
       [u'desde ayer'],
       u'How long is the second half of every diagnosis here, and she will ask it before she reaches for anything.'),
  beat(u'¿Le doy algo fuerte?',
       u'Ask for something mild', u'algo suave',
       u'Deme algo suave.', u'Give me something mild.',
       [u'deme', u'algo suave'],
       [u'algo fuerte', u'desde ayer', u'gracias', u'por favor'],
       [u'deme algo suave', u'algo suave'],
       [u'algo suave'],
       u'Algo suave — something mild. Say it, or you may be handed something a good deal stronger than you wanted, over the counter, no questions asked.'),
  beat(u'Tome esto. Cada ocho horas, con comida.',
       u'Repeat the dose back', u'cada ocho horas',
       u'Cada ocho horas. Gracias.', u'Every eight hours. Thank you.',
       [u'cada ocho horas', u'gracias'],
       [u'algo suave', u'desde ayer', u'por favor', u'Buenas'],
       [u'cada ocho horas gracias', u'cada ocho horas'],
       [u'cada ocho horas'],
       u'Say the dose back. There is no printed label on what she has just tipped into a little paper bag for you.'),
 ]},
{
 'id': 'tramites-02', 'district': 'tramites', 'tier': 2,
 'who': u'La de la ventanilla', 'title': u'La fila',
 'goal': u'Queue, and find out you are in the wrong one',
 'culture': u'A queue here is not a line, it is an order that everybody in '
            u'the room is holding in their head. You ask who is last, you '
            u'tell the next person that you follow them, and then you can go '
            u'and sit down.',
 'beats': [
  beat(u'(Hay tres filas y ninguna tiene rótulo.)',
       u'Ask whether this is the right one', u'¿es aquí?',
       u'¿Es aquí la fila?', u'Is this the right queue?',
       [u'¿es aquí', u'la fila?'],
       [u'la otra ventanilla', u'yo sigo', u'está bien', u'me da'],
       [u'es aqui la fila', u'es aqui'],
       [u'¿es aquí?'],
       u'Ask before you stand in it for forty minutes. Nothing in the building is labelled and nobody thinks that is strange.'),
  beat(u'No, aquí no. Es en la otra ventanilla.',
       u'Say it back', u'la otra ventanilla',
       u'¿En la otra ventanilla?', u'At the other window?',
       [u'¿en la otra ventanilla?'],
       [u'¿es aquí?', u'yo sigo', u'quiero', u'está bien'],
       [u'en la otra ventanilla'],
       [u'la otra ventanilla'],
       u'There is always another ventanilla. Being sent to it once is normal; being sent back is Tuesday.'),
  beat(u'(La otra fila no tiene principio ni fin.)',
       u'Ask who is last', u'¿quién es el último?',
       u'¿Quién es el último?', u'Who’s last?',
       [u'¿quién es', u'el último?'],
       [u'yo sigo', u'la otra ventanilla', u'me da', u'quiero'],
       [u'quien es el ultimo', u'quien es'],
       [u'¿quién es el último?'],
       u'This question is how you enter the queue. Somebody puts a hand up, you remember their face, and the order exists.'),
  beat(u'(Llega alguien detrás de usted y pregunta lo mismo.)',
       u'Claim your place', u'yo sigo',
       u'Yo sigo. Usted va después.', u'I’m next. You’re after me.',
       [u'yo sigo', u'usted va después'],
       [u'¿quién es el último?', u'la otra ventanilla', u'está bien', u'me da'],
       [u'yo sigo usted va despues', u'yo sigo'],
       [u'yo sigo'],
       u'Yo sigo — I follow. Say it and you can go and sit down, because the room will hold your place for you.'),
 ]},
{
 'id': 'tramites-03', 'district': 'tramites', 'tier': 3,
 'who': u'El del banco', 'title': u'El banco',
 'goal': u'Open an account with documents you do not have',
 'culture': u'Nobody has all of it on the first visit and the list on the '
            u'wall is longer than the real one. Ask for the real one out '
            u'loud, write it down, and come back without irritation: getting '
            u'cross at a ventanilla has never moved a document forward.',
 'beats': [
  beat(u'Buenas, ¿en qué le ayudo?',
       u'Say what you want', u'quiero abrir',
       u'Quiero abrir una cuenta.', u'I want to open an account.',
       [u'quiero abrir', u'una cuenta'],
       [u'no tengo', u'vuelvo mañana', u'ideay', u'ni modo'],
       [u'quiero abrir una cuenta', u'quiero abrir'],
       [u'quiero abrir'],
       u'Simple to say. As it turns out, not simple to do.'),
  beat(u'¿Trae cédula, constancia salarial y recibo de luz?',
       u'Say you have not got them', u'no tengo',
       u'No tengo todo eso.', u'I don’t have all that.',
       [u'no tengo', u'todo eso'],
       [u'¿qué necesito?', u'vuelvo mañana', u'vaya pues', u'ni modo'],
       [u'no tengo todo eso', u'no tengo'],
       [u'no tengo'],
       u'No tengo, plainly, without apologising for it. Nobody has all of it the first time and he knows that better than you do.'),
  beat(u'Hm. Sin eso no se puede.',
       u'Ask for the real list', u'¿qué necesito?',
       u'¿Y qué necesito exactamente?', u'And what exactly do I need?',
       [u'¿y qué necesito', u'exactamente?'],
       [u'no tengo', u'vuelvo mañana', u'ideay', u'vaya pues'],
       [u'y que necesito exactamente', u'que necesito'],
       [u'¿qué necesito?'],
       u'Ask for it out loud and write it down. It will be shorter than the list on the wall, and it is the one that counts.'),
  beat(u'Con eso ya le abrimos la cuenta.',
       u'Say you will come back', u'vuelvo mañana',
       u'Está bien. Vuelvo mañana.', u'Alright. I’ll come back tomorrow.',
       [u'está bien', u'vuelvo mañana'],
       [u'¿qué necesito?', u'no tengo', u'ni modo', u'ideay'],
       [u'esta bien vuelvo manana', u'vuelvo manana'],
       [u'vuelvo mañana'],
       u'Vuelvo mañana, without irritation. Getting cross at a window has never once moved a piece of paper forward in this country.'),
 ]},
{
 'id': 'tramites-04', 'district': 'tramites', 'tier': 3,
 'who': u'La enfermera', 'title': u'El centro de salud',
 'goal': u'Get seen at a clinic and describe symptoms properly',
 'culture': u'Public clinics are free and busy. She is triaging thirty people '
            u'this morning, so the symptom comes first, the number of days '
            u'second and the location third — in that order, in as few words '
            u'as you can manage.',
 'beats': [
  beat(u'Pase. ¿Qué le pasa?',
       u'Symptom first', u'tengo fiebre',
       u'Tengo fiebre.', u'I have a fever.',
       [u'tengo fiebre'],
       [u'tres días', u'me duele aquí', u'así es', u'con permiso'],
       [u'tengo fiebre'],
       [u'tengo fiebre'],
       u'Two words, first. She is seeing thirty people this morning and she is sorting them, not chatting.'),
  beat(u'¿Desde cuándo?',
       u'Three days', u'tres días',
       u'Tres días.', u'Three days.',
       [u'tres días'],
       [u'tres horas', u'tengo fiebre', u'así es', u'me deja en'],
       [u'tres dias'],
       [u'tres días'],
       u'Three days with a fever, in this country, is the number that gets you a blood test — because of what it might be.'),
  beat(u'¿Y le duele algo?',
       u'Point, and be specific', u'me duele aquí',
       u'Me duele aquí, atrás de los ojos.', u'It hurts here, behind the eyes.',
       [u'me duele aquí', u'atrás de los ojos'],
       [u'tengo fiebre', u'tres días', u'con permiso', u'así es'],
       [u'me duele aqui atras de los ojos', u'me duele aqui'],
       [u'me duele aquí'],
       u'Behind the eyes, with a fever, means one thing here. She will say the word before you do.'),
  beat(u'Le voy a mandar un examen de sangre.',
       u'Ask whether it is serious', u'¿es grave?',
       u'¿Es grave?', u'Is it serious?',
       [u'¿es grave?'],
       [u'tres días', u'tengo fiebre', u'me deja en', u'así es'],
       [u'es grave'],
       [u'¿es grave?'],
       u'The same two words you used on the moto in Guadalupe. They work on an engine and they work on a person.'),
 ]},
{
 'id': 'tramites-05', 'district': 'tramites', 'tier': 3,
 'who': u'El de migración', 'title': u'La prórroga',
 'goal': u'Extend a visa and be sent away twice first',
 'culture': u'Thirty days at a time, and never all of the requirements at '
            u'once. Ask ¿qué más? until the answer is nada, or you will find '
            u'out about the third item on your second trip.',
 'beats': [
  beat(u'Buenas. ¿Qué necesita?',
       u'Name the thing', u'la prórroga',
       u'Vengo por la prórroga.', u'I’ve come about the extension.',
       [u'vengo por', u'la prórroga'],
       [u'treinta días', u'¿qué más?', u'cuídese', u'dale'],
       [u'vengo por la prorroga', u'la prorroga'],
       [u'la prórroga'],
       u'La prórroga is the extension. Say the word for the thing and you skip ten minutes of explaining what you mean.'),
  beat(u'¿Por cuánto tiempo la quiere?',
       u'Thirty days', u'treinta días',
       u'Treinta días.', u'Thirty days.',
       [u'treinta días'],
       [u'noventa días', u'la prórroga', u'cuídese', u'fíjese que'],
       [u'treinta dias'],
       [u'treinta días'],
       u'Thirty at a time is what they give, so thirty is what you ask for.'),
  beat(u'Necesito copia del pasaporte y dos fotos.',
       u'Ask what else', u'¿qué más?',
       u'¿Y qué más?', u'And what else?',
       [u'¿y qué más?'],
       [u'la prórroga', u'treinta días', u'dale', u'cuídese'],
       [u'y que mas', u'que mas'],
       [u'¿qué más?'],
       u'Ask it until the answer is nada. Otherwise the third requirement turns up on your second trip, which is how it is designed.'),
  beat(u'Y el comprobante del pago. Nada más.',
       u'Say you will be straight back', u'ya vengo',
       u'Ya vengo con las fotos.', u'I’ll be back with the photos.',
       [u'ya vengo', u'con las fotos'],
       [u'¿qué más?', u'treinta días', u'fíjese que', u'dale'],
       [u'ya vengo con las fotos', u'ya vengo'],
       [u'ya vengo'],
       u'Ya vengo — back in a moment, said about anything from a minute to an afternoon. The photo place is the one you already used in El Centro.'),
 ]},
{
 'id': 'tramites-06', 'district': 'tramites', 'tier': 4,
 'who': u'El dentista', 'title': u'La muela',
 'goal': u'Get a tooth dealt with while explaining the pain',
 'culture': u'Same diagnostic shape as the moto workshop: where it is, and '
            u'when it happens. Between cuando como and con el frío he already '
            u'knows what he will find, and he will do it today.',
 'beats': [
  beat(u'Abra. ¿Cuál le duele?',
       u'Point at it', u'esta muela',
       u'Esta muela.', u'This tooth.',
       [u'esta muela'],
       [u'cuando como', u'con el frío', u'no ando', u'ya va'],
       [u'esta muela'],
       [u'esta muela'],
       u'Muela is a molar and diente is a front tooth. Pointing is allowed and expected.'),
  beat(u'¿Y cuándo le duele?',
       u'When you eat', u'cuando como',
       u'Cuando como.', u'When I eat.',
       [u'cuando como'],
       [u'cuando duermo', u'esta muela', u'todo bien', u'ya va'],
       [u'cuando como'],
       [u'cuando como'],
       u'When it hurts is the diagnosis, exactly as it was with the noise on the moto: aquí atrás, cuando freno.'),
  beat(u'¿Y con lo frío?',
       u'With cold as well', u'con el frío',
       u'Con el frío también.', u'With cold things too.',
       [u'con el frío', u'también'],
       [u'cuando como', u'esta muela', u'no ando', u'todo bien'],
       [u'con el frio tambien', u'con el frio'],
       [u'con el frío'],
       u'Between that and cuando como he already knows what he is going to find when he gets in there.'),
  beat(u'Se puede salvar... pero le va a doler un tiempo.',
       u'Tell him to take it out', u'sáquemela',
       u'Sáquemela, mejor.', u'Better take it out.',
       [u'sáquemela', u'mejor'],
       [u'no', u'esta muela', u'ya va', u'todo bien'],
       [u'saquemela mejor', u'saquemela'],
       [u'sáquemela'],
       u'Sáquemela — take it out. It is your decision and he will do it this afternoon, which is either reassuring or not depending on the day you are having.'),
 ]},
{
 'id': 'tramites-07', 'district': 'tramites', 'tier': 4,
 'who': u'El policía', 'title': u'La denuncia',
 'goal': u'Report a stolen phone and manage your expectations',
 'culture': u'You will get a piece of paper, not the phone. The paper is for '
            u'the phone company. Asking the officer whether it is worth '
            u'anything is a completely normal question and he will answer it '
            u'honestly, which is worth more than the paper.',
 'beats': [
  beat(u'Buenas. Dígame.',
       u'Say what happened', u'me robaron',
       u'Me robaron el teléfono.', u'My phone was stolen.',
       [u'me robaron', u'el teléfono'],
       [u'anoche', u'poner una denuncia', u'vamos', u'nos vemos'],
       [u'me robaron el telefono', u'me robaron'],
       [u'me robaron'],
       u'Me robaron — they robbed me, with no particular they. Spanish puts it this way round and it is the normal way to say it.'),
  beat(u'¿Cuándo fue?',
       u'Last night, and where', u'anoche',
       u'Anoche, en la Calzada.', u'Last night, on La Calzada.',
       [u'anoche', u'en la Calzada'],
       [u'me robaron', u'poner una denuncia', u'vamos', u'que le vaya bien'],
       [u'anoche en la calzada', u'anoche'],
       [u'anoche'],
       u'Anoche is last night in one word. Where matters more than you would think — he already knows which corner.'),
  beat(u'¿Y qué quiere hacer?',
       u'Say you want to file it', u'poner una denuncia',
       u'Quiero poner una denuncia.', u'I want to file a report.',
       [u'quiero', u'poner una denuncia'],
       [u'anoche', u'me robaron', u'nos vemos', u'vamos'],
       [u'quiero poner una denuncia', u'poner una denuncia'],
       [u'poner una denuncia'],
       u'Poner una denuncia — to file a report. The verb is poner, which is worth knowing before you are standing at the desk.'),
  beat(u'Le doy el papel. Pero el teléfono ya no aparece, se lo digo de una vez.',
       u'Ask whether it is worth anything', u'¿sirve de algo?',
       u'¿Y sirve de algo?', u'And is it any use?',
       [u'¿y sirve de algo?'],
       [u'poner una denuncia', u'anoche', u'vamos', u'que le vaya bien'],
       [u'y sirve de algo', u'sirve de algo'],
       [u'¿sirve de algo?'],
       u'Ask it. He will tell you the truth — the paper is for the phone company, not for getting the phone back — and you are both better for the honesty.'),
 ]},
{
 'id': 'tramites-08', 'district': 'tramites', 'tier': 4,
 'who': u'La abogada', 'title': u'El papel',
 'goal': u'Get a document notarised without understanding it',
 'culture': u'Un papel is any document at all, and admitting you do not know '
            u'which one you need is the fastest route to the right one. She '
            u'has read the letter you were given and she knows exactly what '
            u'it is asking for.',
 'beats': [
  beat(u'Buenas, adelante. ¿En qué le ayudo?',
       u'Say what you need', u'necesito',
       u'Necesito un papel.', u'I need a document.',
       [u'necesito', u'un papel'],
       [u'¿usted me lo hace?', u'¿cuánto cobra?', u'disculpe', u'otro día'],
       [u'necesito un papel', u'necesito'],
       [u'necesito', u'un papel'],
       u'Un papel is any document there is. Say it and she will work out which one you mean rather better than you can.'),
  beat(u'¿Qué tipo de papel? ¿Un poder, una constancia?',
       u'Admit you do not know', u'¿usted me lo hace?',
       u'No sé. ¿Usted me lo hace?', u'I don’t know. Could you do it for me?',
       [u'no sé', u'¿usted me lo hace?'],
       [u'necesito', u'¿cuánto cobra?', u'otro día', u'¿a cómo?'],
       [u'no se usted me lo hace', u'usted me lo hace'],
       [u'¿usted me lo hace?'],
       u'Admitting it is the fastest route to the right document. She has read the letter you were handed and she knows what it wants.'),
  beat(u'Sí, se lo hago y se lo notarizo.',
       u'Ask the price before she starts', u'¿cuánto cobra?',
       u'¿Cuánto cobra usted?', u'What do you charge?',
       [u'¿cuánto cobra', u'usted?'],
       [u'necesito', u'un papel', u'disculpe', u'otro día'],
       [u'cuanto cobra usted', u'cuanto cobra'],
       [u'¿cuánto cobra?'],
       u'Ask before she starts typing. A notarised page has a price and it is not written down anywhere in the room.'),
 ]},
{
 'id': 'tramites-09', 'district': 'tramites', 'tier': 5,
 'who': u'El doctor', 'title': u'El dengue',
 'goal': u'Have dengue explained to you while you have it',
 'culture': u'There is no medicine for it. The treatment is fluid and lying '
            u'down, and the dangerous part is the day the fever drops and you '
            u'feel better. Every instruction here is one to repeat back, '
            u'because none of it comes on a piece of paper.',
 'beats': [
  beat(u'Es dengue. Tiene que tomar mucho suero.',
       u'Repeat the instruction', u'mucho suero',
       u'Mucho suero. Entendido.', u'Plenty of fluids. Understood.',
       [u'mucho suero', u'entendido'],
       [u'no se levante', u'si empeora', u'gracias', u'por favor'],
       [u'mucho suero entendido', u'mucho suero'],
       [u'mucho suero'],
       u'Suero is rehydration salts, sold in every pulpería. There is no medicine for this and the fluid IS the treatment.'),
  beat(u'Y no se levante. Reposo, joven.',
       u'Check what he means', u'no se levante',
       u'¿No me levanto nada?', u'I’m not to get up at all?',
       [u'¿no me levanto', u'nada?'],
       [u'mucho suero', u'si empeora', u'gracias', u'Buenas'],
       [u'no me levanto nada', u'no me levanto'],
       [u'no se levante'],
       u'No se levante from him, no me levanto from you. He means it: people get up on day four and end up straight back in here.'),
  beat(u'Si empeora, se viene de una vez.',
       u'Ask what worse looks like', u'si empeora',
       u'¿Si empeora cómo?', u'Worse how?',
       [u'¿si empeora', u'cómo?'],
       [u'mucho suero', u'no se levante', u'gracias', u'por favor'],
       [u'si empeora como', u'si empeora'],
       [u'si empeora'],
       u'Ask, because the dangerous part of dengue is the day the fever drops and you feel better. He will tell you the signs and you should write them down.'),
  beat(u'Una semana, más o menos, y va a andar bien.',
       u'A week, then', u'una semana',
       u'Una semana. Está bien.', u'A week. Alright.',
       [u'una semana', u'está bien'],
       [u'un día', u'si empeora', u'gracias', u'Buenas'],
       [u'una semana esta bien', u'una semana'],
       [u'una semana'],
       u'A week flat on your back, and everybody you tell afterwards will say they had it worse. They probably did.'),
 ]},
{
 'id': 'tramites-10', 'district': 'tramites', 'tier': 5,
 'who': u'La de la ventanilla', 'title': u'La cédula',
 'goal': u'Sit through the whole bureaucracy for one piece of card',
 'culture': u'Five weeks, four visits and a shoebox of laminated cards with '
            u'no order to them. The Spanish that gets you through it is four '
            u'phrases long and every one of them is a way of saying: I have '
            u'already done my part.',
 'beats': [
  beat(u'¿Sí?',
       u'Say what you came for', u'vengo por',
       u'Vengo por mi cédula.', u'I’ve come for my ID card.',
       [u'vengo por', u'mi cédula'],
       [u'ya entregué', u'me dijeron', u'está bien', u'me da'],
       [u'vengo por mi cedula', u'vengo por'],
       [u'vengo por'],
       u'Vengo por — I have come for. The single most useful opening sentence in any office in the country.'),
  beat(u'¿Ya entregó los papeles?',
       u'Yes, already', u'ya entregué',
       u'Ya entregué todo.', u'I handed everything in already.',
       [u'ya entregué', u'todo'],
       [u'vengo por', u'me dijeron', u'quiero', u'está bien'],
       [u'ya entregue todo', u'ya entregue'],
       [u'ya entregué'],
       u'Ya entregué — I already handed them in. Say it before she asks you to do it again, because she will.'),
  beat(u'¿Y quién le dijo que viniera hoy?',
       u'Say who told you', u'me dijeron',
       u'Me dijeron que hoy.', u'I was told today.',
       [u'me dijeron', u'que hoy'],
       [u'ya entregué', u'vengo por', u'me da', u'quiero'],
       [u'me dijeron que hoy', u'me dijeron'],
       [u'me dijeron'],
       u'Me dijeron, with no particular they, is both true and unarguable. Naming whoever told you would only get them into trouble.'),
  beat(u'(Pone una caja de cartón llena de cédulas en el mostrador.)',
       u'Ask which one is yours', u'¿cuál es el mío?',
       u'¿Cuál es el mío?', u'Which one is mine?',
       [u'¿cuál es el mío?'],
       [u'me dijeron', u'ya entregué', u'está bien', u'me da'],
       [u'cual es el mio'],
       [u'¿cuál es el mío?'],
       u'A shoebox of laminated cards in no order at all. This is the last sentence of a process that took five weeks and it is worth every one of them.'),
 ]},
{
 'id': 'malecon-01', 'district': 'malecon', 'tier': 1,
 'who': u'La del quesillo', 'title': u'El quesillo',
 'goal': u'Eat a quesillo and survive the bag it comes in',
 'culture': u'Cheese, cream, pickled onion and salt in a tortilla, served in '
            u'a plastic bag. The bag is not a mistake — you drink the cream '
            u'out of the corner of it when the tortilla is gone, and everybody '
            u'watching will be pleased that you knew to.',
 'beats': [
  beat(u'¿Le doy quesillo, joven?',
       u'Order one', u'un quesillo',
       u'Un quesillo, por favor.', u'One quesillo, please.',
       [u'un quesillo', u'por favor'],
       [u'con todo', u'sin cebolla', u'está bien', u'quiero'],
       [u'un quesillo por favor', u'un quesillo'],
       [u'un quesillo'],
       u'Cheese, cream, pickled onion and salt, in a tortilla, in a bag. La Paz Centro and Nagarote argue about who does it best and neither of them is here.'),
  beat(u'¿Con todo?',
       u'With everything', u'con todo',
       u'Con todo.', u'With everything.',
       [u'con todo'],
       [u'sin nada', u'un quesillo', u'gracias', u'está bien'],
       [u'con todo'],
       [u'con todo'],
       u'Con todo again — the same answer you gave about the beans. It is the default reply to every ¿con qué? in this country.'),
  beat(u'¿Todo todo? ¿Con la cebolla?',
       u'Except the onion', u'sin cebolla',
       u'Pero sin cebolla.', u'But without the onion.',
       [u'pero', u'sin cebolla'],
       [u'con todo', u'un quesillo', u'gracias', u'quiero'],
       [u'pero sin cebolla', u'sin cebolla'],
       [u'sin cebolla'],
       u'The pickled onion is the strongest thing in there and asking for it without offends nobody.'),
  beat(u'(Se lo pasa en la bolsa, goteando.)',
       u'Tell her it is good', u'está rico',
       u'Está rico. De verdad.', u'It’s good. Really.',
       [u'está rico', u'de verdad'],
       [u'con todo', u'sin cebolla', u'está bien', u'gracias'],
       [u'esta rico de verdad', u'esta rico'],
       [u'está rico'],
       u'Está rico is what you say with your mouth full and it is expected. Saying nothing at all reads as not liking it.'),
 ]},
{
 'id': 'malecon-02', 'district': 'malecon', 'tier': 2,
 'who': u'El lanchero', 'title': u'Las isletas',
 'goal': u'Haggle a boat around the isletas',
 'culture': u'Per person is the tourist unit. Ask for the boat rather than '
            u'the seat and the number changes, and settle the return before '
            u'you push off — the same lesson the fisherman in Pantanal taught '
            u'you, at Malecón prices.',
 'beats': [
  beat(u'¡Paseo por las isletas! ¿Van?',
       u'Ask for a trip round', u'una vuelta',
       u'¿Nos da una vuelta?', u'Would you take us round?',
       [u'¿nos da', u'una vuelta?'],
       [u'por las isletas', u'ida y vuelta', u'así es', u'me da'],
       [u'nos da una vuelta', u'una vuelta'],
       [u'una vuelta'],
       u'Una vuelta is a spin, a lap, a trip round. It is the word for this and it costs less than the thing called a tour.'),
  beat(u'¿Por dónde quieren ir?',
       u'Round the isletas', u'por las isletas',
       u'Por las isletas.', u'Round the isletas.',
       [u'por las isletas'],
       [u'una vuelta', u'ida y vuelta', u'ni modo', u'así es'],
       [u'por las isletas'],
       [u'por las isletas'],
       u'The same islands the fisherman took you to, at the price the Malecón charges. Which is why this mission is a haggle and that one was not.'),
  beat(u'Quince dólares por persona.',
       u'Ask for the boat, not the seat', u'¿cuánto por todos?',
       u'¿Y cuánto por todos?', u'And how much for all of us?',
       [u'¿y cuánto', u'por todos?'],
       [u'una vuelta', u'por las isletas', u'ni modo', u'me da'],
       [u'y cuanto por todos', u'cuanto por todos'],
       [u'¿cuánto por todos?'],
       u'Per person is the tourist unit. Ask for the whole boat and the arithmetic changes in your favour immediately.'),
  beat(u'Cuarenta por todos y los traigo de vuelta.',
       u'Confirm the return', u'ida y vuelta',
       u'Ida y vuelta, ¿verdad?', u'There and back, right?',
       [u'ida y vuelta', u'¿verdad?'],
       [u'una vuelta', u'por todos', u'así es', u'ni modo'],
       [u'ida y vuelta verdad', u'ida y vuelta'],
       [u'ida y vuelta'],
       u'You learned this from the fisherman. Ask it again anyway — a boat is the one place where the return really is negotiable.'),
 ]},
{
 'id': 'malecon-03', 'district': 'malecon', 'tier': 2,
 'who': u'El de la pesca', 'title': u'El guapote',
 'goal': u'Order fried fish and be told which one is worth it',
 'culture': u'It comes whole, head and all, with fried plantain. Tajadas are '
            u'the savoury green ones and maduro is the sweet ripe one, and '
            u'that is the only real decision. Choosing your fish by pointing '
            u'at the tray is normal.',
 'beats': [
  beat(u'¿Pescado, joven? Fresquito del lago.',
       u'Ask for guapote', u'guapote',
       u'Un guapote.', u'A guapote.',
       [u'un guapote'],
       [u'frito', u'con tajadas', u'con permiso', u'cuídese'],
       [u'un guapote'],
       [u'guapote'],
       u'Guapote is the lake fish worth ordering. You met it on the fishmonger’s slab in the market; here it arrives on a plate.'),
  beat(u'¿Frito o al vapor?',
       u'Fried', u'frito',
       u'Frito.', u'Fried.',
       [u'frito'],
       [u'al vapor', u'un guapote', u'gracias', u'fíjese que'],
       [u'frito'],
       [u'frito'],
       u'Frito, whole, head and all. Al vapor exists on the sign and nobody has ever ordered it.'),
  beat(u'¿Y con qué se lo pongo?',
       u'With plantain', u'con tajadas',
       u'Con tajadas.', u'With plantain chips.',
       [u'con tajadas'],
       [u'con arroz', u'frito', u'gracias', u'cuídese'],
       [u'con tajadas'],
       [u'con tajadas'],
       u'Tajadas are fried green plantain. Maduro is the sweet ripe one, and this is the fork in the road at every plate in the country.'),
  beat(u'(Le enseña la bandeja.) ¿Cuál quiere?',
       u'Point at one', u'el de allá',
       u'El de allá, el grande.', u'That one over there, the big one.',
       [u'el de allá', u'el grande'],
       [u'este', u'con tajadas', u'frito', u'fíjese que'],
       [u'el de alla el grande', u'el de alla'],
       [u'el de allá'],
       u'El de allá — that one over there. Fish is chosen by pointing everywhere on earth and nobody minds you doing it here.'),
 ]},
{
 'id': 'malecon-04', 'district': 'malecon', 'tier': 3,
 'who': u'La familia del domingo', 'title': u'El domingo',
 'goal': u'Be pulled into somebody’s Sunday on the shore',
 'culture': u'Sunday on the lakefront is families with pots of food, and they '
            u'will feed you. Hesitating for one beat is polite; refusing '
            u'outright is the only wrong answer on that beach. No sea pena '
            u'means stop being shy and it is said to everybody.',
 'beats': [
  beat(u'¡Venga, siéntese con nosotros!',
       u'Check they mean it', u'siéntese',
       u'¿Yo? ¿Me siento?', u'Me? Should I sit?',
       [u'¿yo?', u'¿me siento?'],
       [u'hay bastante', u'sírvase', u'no ando', u'ya va'],
       [u'yo me siento', u'me siento'],
       [u'siéntese'],
       u'Siéntese from them, me siento from you. They do mean it, and hesitating for exactly one beat before accepting is the polite amount.'),
  beat(u'¡Sí, hombre! Hay bastante.',
       u'Check there is enough', u'hay bastante',
       u'¿Hay bastante?', u'Is there enough?',
       [u'¿hay bastante?'],
       [u'siéntese', u'sírvase', u'ya va', u'que le vaya bien'],
       [u'hay bastante'],
       [u'hay bastante'],
       u'Hay bastante — there is plenty. There is never quite as much as they say and you are eating some of it regardless; that is the arrangement.'),
  beat(u'No sea pena, pues. Coma.',
       u'Say you are not being shy', u'no sea pena',
       u'No, no es pena.', u'No, I’m not being shy.',
       [u'no', u'no es pena'],
       [u'hay bastante', u'sírvase', u'no ando', u'ya va'],
       [u'no no es pena', u'no es pena'],
       [u'no sea pena'],
       u'Pena is shyness and embarrassment at once. No sea pena is said to everybody who hesitates, and the correct response is to stop hesitating.'),
  beat(u'Sírvase, pues. Agarre de ahí.',
       u'Help yourself', u'sírvase',
       u'Gracias. Me sirvo.', u'Thank you. I’ll help myself.',
       [u'gracias', u'me sirvo'],
       [u'sírvase', u'hay bastante', u'ya va', u'no ando'],
       [u'gracias me sirvo', u'me sirvo'],
       [u'sírvase'],
       u'Sírvase — help yourself. Take a modest amount and say so out loud; taking nothing is the one move that would hurt somebody’s feelings.'),
 ]},
{
 'id': 'malecon-05', 'district': 'malecon', 'tier': 3,
 'who': u'El del caballo', 'title': u'El caballo',
 'goal': u'Turn down a horse ride without making it awkward',
 'culture': u'Reasons work better than refusals, and praising the animal '
            u'costs nothing and is probably true. You have done the four-noes '
            u'version of this at the hammock stall; this is the gentler one.',
 'beats': [
  beat(u'¿Un paseo a caballo, amigo? Barato.',
       u'No thank you', u'no gracias',
       u'No, gracias.', u'No, thank you.',
       [u'no', u'gracias'],
       [u'nunca he montado', u'otro día', u'está bonito', u'Buenas'],
       [u'no gracias'],
       [u'no gracias'],
       u'The first no. You have done this at the hammock stall and it works the same way here.'),
  beat(u'¡Es manso! Suba, no le pasa nada.',
       u'Give him a reason', u'nunca he montado',
       u'Nunca he montado.', u'I’ve never ridden.',
       [u'nunca he montado'],
       [u'no gracias', u'otro día', u'está bonito', u'¿a cómo?'],
       [u'nunca he montado'],
       [u'nunca he montado'],
       u'A reason he cannot argue with, and it happens to be true. Reasons work far better than refusals in this country.'),
  beat(u'Por eso mismo. Yo lo llevo despacio.',
       u'Praise the horse', u'está bonito',
       u'Pero está bonito el caballo.', u'He is a fine-looking horse, though.',
       [u'pero', u'está bonito', u'el caballo'],
       [u'no gracias', u'otro día', u'nunca he montado', u'Buenas'],
       [u'pero esta bonito el caballo', u'esta bonito'],
       [u'está bonito'],
       u'Praise the animal. It costs nothing, it is probably true, and it turns a refusal into a conversation he can walk away from happily.'),
  beat(u'¿Verdad que sí? Es mío desde potrillo.',
       u'Leave it open', u'otro día',
       u'Otro día, tal vez.', u'Another day, maybe.',
       [u'otro día', u'tal vez'],
       [u'está bonito', u'nunca he montado', u'no gracias', u'¿a cómo?'],
       [u'otro dia tal vez', u'otro dia'],
       [u'otro día'],
       u'Otro día, one more time. By now you know it is a real maybe rather than a brush-off, which is exactly why it works.'),
 ]},
{
 'id': 'malecon-06', 'district': 'malecon', 'tier': 4,
 'who': u'El músico', 'title': u'El son nica',
 'goal': u'Get a musician to explain what he is playing',
 'culture': u'Musicians here are asked to play and almost never asked what it '
            u'is. Asking is worth more to him than the coins, and toque otra '
            u'is the best thing you can say to anybody holding a guitar.',
 'beats': [
  beat(u'(Está tocando algo que usted no reconoce.)',
       u'Ask what it is', u'¿qué es eso?',
       u'¿Qué es eso que toca?', u'What’s that you’re playing?',
       [u'¿qué es eso', u'que toca?'],
       [u'de aquí', u'toque otra', u'gracias', u'está bien'],
       [u'que es eso que toca', u'que es eso'],
       [u'¿qué es eso?'],
       u'Ask. He is asked to play constantly and asked what it is almost never.'),
  beat(u'Es son nica, pues. De aquí.',
       u'From here?', u'de aquí',
       u'¿De aquí, de Nicaragua?', u'From here, from Nicaragua?',
       [u'¿de aquí,', u'de Nicaragua?'],
       [u'¿qué es eso?', u'toque otra', u'gracias', u'por favor'],
       [u'de aqui de nicaragua', u'de aqui'],
       [u'de aquí'],
       u'De aquí again — the same two words the poet used about Darío in Parque Central, and meaning the same thing: the country, not the street.'),
  beat(u'De aquí mismo. Mi papá tocaba esto.',
       u'Ask for another', u'toque otra',
       u'Toque otra, por favor.', u'Play another, please.',
       [u'toque otra', u'por favor'],
       [u'de aquí', u'¿qué es eso?', u'gracias', u'está bien'],
       [u'toque otra por favor', u'toque otra'],
       [u'toque otra'],
       u'Toque otra — play another one. It is the best thing you can say to somebody with a guitar and it is worth more to him than the coins are.'),
  beat(u'(Toca otra, más larga.)',
       u'Tell him you liked it', u'me gustó',
       u'Me gustó mucho. Gracias.', u'I liked that a lot. Thank you.',
       [u'me gustó mucho', u'gracias'],
       [u'toque otra', u'de aquí', u'por favor', u'está bien'],
       [u'me gusto mucho gracias', u'me gusto mucho'],
       [u'me gustó'],
       u'Me gustó, in the past, because it is finished. Saying so out loud is the payment that is not money.'),
 ]},
{
 'id': 'malecon-07', 'district': 'malecon', 'tier': 4,
 'who': u'El vigilante', 'title': u'La noche',
 'goal': u'Be told, politely, that this is not a good place after dark',
 'culture': u'He is a night watchman being kind, and the whole warning is '
            u'delivered in softeners: ya es tarde, mejor váyase, por ahí no. '
            u'Recognising it as advice rather than conversation is the '
            u'mission, and the correct answer is to take it.',
 'beats': [
  beat(u'Buenas noches, joven. Ya es tarde.',
       u'Register that this is advice', u'ya es tarde',
       u'¿Ya es tarde?', u'Is it late?',
       [u'¿ya es tarde?'],
       [u'mejor váyase', u'por ahí no', u'me da', u'quiero'],
       [u'ya es tarde'],
       [u'ya es tarde'],
       u'He is not making conversation. Ya es tarde from a watchman is the opening line of a piece of advice.'),
  beat(u'Sí. Mejor váyase para el centro.',
       u'Say it back', u'mejor váyase',
       u'¿Mejor me voy?', u'I should go, then?',
       [u'¿mejor me voy?'],
       [u'ya es tarde', u'por ahí no', u'ni modo', u'me da'],
       [u'mejor me voy'],
       [u'mejor váyase'],
       u'Mejor váyase from him, mejor me voy from you. Mejor here means it would be better if — the gentlest possible way to tell somebody to leave.'),
  beat(u'Sí. Y por ahí no, por la orilla no vaya.',
       u'Ask which way instead', u'por ahí no',
       u'¿Por ahí no? ¿Por dónde entonces?', u'Not that way? Which way, then?',
       [u'¿por ahí no?', u'¿por dónde entonces?'],
       [u'mejor váyase', u'ya es tarde', u'quiero', u'ni modo'],
       [u'por ahi no por donde entonces', u'por ahi no'],
       [u'por ahí no'],
       u'Ask for the alternative. He is telling you about one specific stretch of shore after dark, not about the country.'),
  beat(u'Por la calle, derechito. Se lo digo yo.',
       u'Take the advice', u'se lo digo yo',
       u'Le hago caso. Gracias.', u'I’ll do as you say. Thank you.',
       [u'le hago caso', u'gracias'],
       [u'ya es tarde', u'por ahí no', u'me da', u'ni modo'],
       [u'le hago caso gracias', u'le hago caso'],
       [u'se lo digo yo'],
       u'Se lo digo yo — take it from me. That is the weight he is putting behind it, and le hago caso, I’ll do as you say, is the right answer.'),
 ]},
{
 'id': 'malecon-08', 'district': 'malecon', 'tier': 5,
 'who': u'El capitán', 'title': u'A Ometepe',
 'goal': u'Buy a ferry ticket and understand the schedule',
 'culture': u'A pasaje on a boat, a boleto on a bus. And the timetable has a '
            u'condition attached to it that no printed schedule anywhere else '
            u'has: si el lago deja — if the lake lets us. Cocibolca gets '
            u'rough enough to cancel the crossing and everybody who works it '
            u'talks about the lake as something that decides.',
 'beats': [
  beat(u'Buenas. ¿Para Ometepe?',
       u'Ask the time', u'¿a qué hora sale?',
       u'¿A qué hora sale el ferry?', u'What time does the ferry leave?',
       [u'¿a qué hora sale', u'el ferry?'],
       [u'un pasaje', u'de ida', u'así es', u'con permiso'],
       [u'a que hora sale el ferry', u'a que hora sale'],
       [u'¿a qué hora sale?'],
       u'The same question you asked at the bus terminal. Sale is what everything does here — buses, photographs, ferries.'),
  beat(u'A las dos y media. Si el lago deja.',
       u'Buy the ticket', u'un pasaje',
       u'Un pasaje, por favor.', u'One ticket, please.',
       [u'un pasaje', u'por favor'],
       [u'un boleto', u'de ida', u'fíjese que', u'así es'],
       [u'un pasaje por favor', u'un pasaje'],
       [u'un pasaje'],
       u'A pasaje on a boat and a boleto on a bus. Nobody will correct you, and he will notice that you got it right.'),
  beat(u'¿De ida o ida y vuelta?',
       u'One way', u'de ida',
       u'De ida nada más.', u'One way only.',
       [u'de ida', u'nada más'],
       [u'ida y vuelta', u'un pasaje', u'con permiso', u'así es'],
       [u'de ida nada mas', u'de ida'],
       [u'de ida'],
       u'De ida — one way. You are staying on the island a while, which is the correct decision and he will approve of it.'),
  beat(u'Listo. A las dos y media, si el lago deja.',
       u'Ask what he means by that', u'si el lago deja',
       u'¿Si el lago deja?', u'If the lake lets us?',
       [u'¿si el lago deja?'],
       [u'de ida', u'un pasaje', u'fíjese que', u'con permiso'],
       [u'si el lago deja'],
       [u'si el lago deja'],
       u'Cocibolca gets rough enough to cancel the crossing. Everybody who works this water talks about the lake as something that makes decisions.'),
 ]},
]

HINTS = [
 {'kind': u'vendedora', 'district': 'tramites',
  'says': u'Si le duele algo, primero a la farmacia. Ahí le dan sin receta y le sale más barato.',
  'en': u'If something hurts, go to the pharmacy first. They give it to you without a prescription and it is cheaper.',
  'points_at': ['tramites-01']},
 {'kind': u'viejo de la esquina', 'district': 'tramites',
  'says': u'En esas oficinas pregunte quién es el último antes de pararse en la fila.',
  'en': u'In those offices, ask who is last before you stand in the queue.',
  'points_at': ['tramites-02', 'tramites-10']},
 {'kind': u'obrero', 'district': 'tramites',
  'says': u'Para abrir cuenta le piden mil papeles. Pregunte bien la lista antes de ir.',
  'en': u'To open an account they ask for a thousand documents. Ask for the exact list before you go.',
  'points_at': ['tramites-03']},
 {'kind': u'doña en la puerta', 'district': 'tramites',
  'says': u'Con fiebre de tres días vaya al centro de salud, no se quede en la casa.',
  'en': u'With a three-day fever go to the clinic, do not stay at home.',
  'points_at': ['tramites-04', 'tramites-09']},
 {'kind': u'caponero', 'district': 'tramites',
  'says': u'Lo de la prórroga es en migración, y llévese las fotos desde ya.',
  'en': u'The visa extension is at immigration, and take the photos with you from the start.',
  'points_at': ['tramites-05']},
 {'kind': u'chavalo en bici', 'district': 'tramites',
  'says': u'¿Le duele la muela? El dentista de la esquina se la saca el mismo día.',
  'en': u'Toothache? The dentist on the corner takes it out the same day.',
  'points_at': ['tramites-06']},
 {'kind': u'policía', 'district': 'tramites',
  'says': u'Si le robaron, ponga la denuncia. No le va a aparecer, pero el papel le sirve.',
  'en': u'If you were robbed, file the report. It will not turn up, but the paper is useful.',
  'points_at': ['tramites-07']},
 {'kind': u'vendedora', 'district': 'tramites',
  'says': u'Para papeles, la abogada de enfrente. Ella se los hace y se los notariza.',
  'en': u'For documents, the lawyer across the way. She writes them and notarises them.',
  'points_at': ['tramites-08']},
 {'kind': u'doña en la puerta', 'district': 'malecon',
  'says': u'Baje al malecón el domingo. Ahí venden quesillo y la gente lleva las ollas.',
  'en': u'Go down to the lakefront on Sunday. They sell quesillo and people bring their pots.',
  'points_at': ['malecon-01', 'malecon-04']},
 {'kind': u'caponero', 'district': 'malecon',
  'says': u'Los lancheros piden por persona. Pregúnteles cuánto por el bote completo.',
  'en': u'The boatmen charge per person. Ask them how much for the whole boat.',
  'points_at': ['malecon-02']},
 {'kind': u'vendedora', 'district': 'malecon',
  'says': u'El guapote frito con tajadas, ahí en los ranchos de la orilla. Pida el más grande.',
  'en': u'Fried guapote with plantain, in the shacks along the shore. Ask for the biggest one.',
  'points_at': ['malecon-03']},
 {'kind': u'chavalo en bici', 'district': 'malecon',
  'says': u'Ahí anda el señor de los caballos. Si no quiere, dígale que nunca ha montado.',
  'en': u'The horse man is about. If you do not want to, tell him you have never ridden.',
  'points_at': ['malecon-05']},
 {'kind': u'viejo de la esquina', 'district': 'malecon',
  'says': u'Ese que toca ahí sabe son nica del bueno. Pregúntele qué es lo que toca.',
  'en': u'That man playing there knows the real son nica. Ask him what it is he is playing.',
  'points_at': ['malecon-06']},
 {'kind': u'cuidacarros', 'district': 'malecon',
  'says': u'De noche por la orilla no ande, jefe. Hágale caso al vigilante.',
  'en': u'Do not walk along the shore at night, boss. Do as the watchman says.',
  'points_at': ['malecon-07']},
 {'kind': u'obrero', 'district': 'malecon',
  'says': u'El ferry a Ometepe sale de aquí. Pero si el lago está bravo, no sale.',
  'en': u'The ferry to Ometepe leaves from here. But if the lake is rough, it does not go.',
  'points_at': ['malecon-08']},
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
