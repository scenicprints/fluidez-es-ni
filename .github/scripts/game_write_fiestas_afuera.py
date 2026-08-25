# -*- coding: utf-8 -*-
"""Writes Las fiestas (8) and Afuera (8) — the last sixteen missions.

Las fiestas is the calendar, and most of it comes round once a year, so a
player will meet these out of order and will miss some. That is the point of
the district: they are written so that being told about one is worth as much
as being at it.

The Purísima call and response is the real one. On the seventh of December
somebody shouts ¿Quién causa tanta alegría? at a door and everybody within
earshot shouts back ¡La Concepción de María! It is the single most Nicaraguan
night of the year and it is not optional.

Afuera is Masaya, San Juan de Oriente, Catarina, Mombacho and the Laguna — all
of it outside the map, so these people are met on the road out of town, which
is where you would really meet them.
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
 'id': 'fiestas-01', 'district': 'fiestas', 'tier': 2,
 'who': u'Doña Marta', 'title': u'La Purísima',
 'goal': u'Sing at a door on the 7th of December and get sweets for it',
 'culture': u'The seventh of December. Somebody shouts the question at a '
            u'door, everybody within earshot shouts the answer, and the house '
            u'hands out la gorra — sweets, sugar cane, fruit, a whistle. It '
            u'is the most Nicaraguan night of the year and you do it with '
            u'somebody who knows the houses.',
 'beats': [
  beat(u'El siete gritamos en las puertas. Yo pregunto y usted contesta. '
       u'¿Quién causa tanta alegría?',
       u'Give the answer everybody gives', u'la concepción',
       u'¡La Concepción de María!', u'The Conception of Mary!',
       [u'¡la Concepción', u'de María!'],
       [u'gorra', u'vivan las gorras', u'ideay', u'ni modo'],
       [u'la concepcion de maria', u'la concepcion'],
       [u'¿quién causa tanta alegría?', u'la concepción'],
       u'One question, one answer, at every door in the country on the same night. It is the one call and response you cannot afford not to know.'),
  beat(u'¡Eso! Y entonces le dan la gorra.',
       u'Ask what a gorra is', u'gorra',
       u'¿Qué es la gorra?', u'What’s a gorra?',
       [u'¿qué es', u'la gorra?'],
       [u'vivan las gorras', u'la concepción', u'vaya pues', u'ni modo'],
       [u'que es la gorra', u'la gorra'],
       [u'gorra'],
       u'La gorra is what the house hands you at the door: sweets, fruit, a stick of sugar cane, a plastic whistle. Everybody goes home with a bagful.'),
  beat(u'Dulces, caña, un pito. Y usted grita otra cosa cuando se la dan.',
       u'Shout the thanks', u'vivan las gorras',
       u'¡Vivan las gorras!', u'Long live the gift bags!',
       [u'¡vivan las gorras!'],
       [u'la concepción', u'la gorra', u'ideay', u'vaya pues'],
       [u'vivan las gorras'],
       [u'vivan las gorras'],
       u'Shouted, on somebody’s doorstep, by grown adults. It is not a joke and by the fourth house you will be shouting it too.'),
  beat(u'¿Y viene conmigo el siete, pues?',
       u'Say yes', u'vaya pues',
       u'Vaya pues. Voy con usted.', u'Alright then. I’ll come with you.',
       [u'vaya pues', u'voy con usted'],
       [u'otro día', u'ni modo', u'la gorra', u'ideay'],
       [u'vaya pues voy con usted', u'vaya pues'],
       [u'vaya pues'],
       u'Going with somebody who knows which houses give what is the only way to do your first Gritería. Going alone is carol singing without the carols.'),
 ]},
{
 'id': 'fiestas-02', 'district': 'fiestas', 'tier': 3,
 'who': u'El vecino', 'title': u'La Gritería',
 'goal': u'Go door to door and keep up with the responses',
 'culture': u'Six in the evening, the bells go and the fireworks start, and '
            u'the entire city walks out of its houses at once. You will do '
            u'thirty houses, the good ones run out, and every barrio knows '
            u'which house does the big gorras.',
 'beats': [
  beat(u'(Suenan las campanas y empiezan los cohetes. Son las seis.)',
       u'Ask whether it has started', u'ya empezó',
       u'¿Ya empezó?', u'Has it started?',
       [u'¿ya empezó?'],
       [u'la gritería', u'vamos', u'aquí dan bueno', u'así es'],
       [u'ya empezo'],
       [u'ya empezó'],
       u'Six in the evening, bells and rockets, and the whole city out of doors within about four minutes. Ya empezó is what everybody says.'),
  beat(u'¡Ya empezó! ¡Vámonos, vecino!',
       u'Name the night', u'gritería',
       u'¡La gritería! Vamos.', u'The Gritería! Let’s go.',
       [u'¡la gritería!', u'vamos'],
       [u'ya empezó', u'aquí dan bueno', u'con permiso', u'me deja en'],
       [u'la griteria vamos', u'la griteria'],
       [u'gritería'],
       u'La Gritería — the shouting. That is genuinely its name and it is a completely accurate description of the evening.'),
  beat(u'(Ya llevan cuatro casas. La bolsa va pesando.)',
       u'Move him on to the next one', u'vamos',
       u'Vamos a la otra.', u'On to the next one.',
       [u'vamos', u'a la otra'],
       [u'aquí dan bueno', u'ya empezó', u'así es', u'con permiso'],
       [u'vamos a la otra', u'vamos'],
       [u'vamos'],
       u'You are doing thirty houses tonight and the good ones run out. Vamos is said constantly and always slightly urgently.'),
  beat(u'Espere, espere. Aquí dan bueno.',
       u'Agree to queue at this one', u'aquí dan bueno',
       u'¿Aquí dan bueno? Entonces esperamos.', u'They give good stuff here? Then we’ll wait.',
       [u'¿aquí dan bueno?', u'entonces esperamos'],
       [u'vamos', u'la gritería', u'me deja en', u'así es'],
       [u'aqui dan bueno entonces esperamos', u'aqui dan bueno'],
       [u'aquí dan bueno'],
       u'Dan bueno — they give good stuff. Every barrio knows which house does the big gorras, and there will be a queue outside it.'),
 ]},
{
 'id': 'fiestas-03', 'district': 'fiestas', 'tier': 3,
 'who': u'La de la alfombra', 'title': u'Semana Santa',
 'goal': u'Help make a sawdust carpet before the procession walks over it',
 'culture': u'Dyed sawdust laid on the road overnight by a whole family, so '
            u'that the procession can walk straight over it at seven in the '
            u'morning. The destruction is the point, which does not stop '
            u'everybody shouting at you not to step on it.',
 'beats': [
  beat(u'(Hay costales de aserrín de colores en media calle.)',
       u'Ask what the sawdust is for', u'aserrín',
       u'¿Y ese aserrín?', u'What’s all the sawdust for?',
       [u'¿y ese aserrín?'],
       [u'la alfombra', u'no lo pise', u'toda la noche', u'cuídese'],
       [u'y ese aserrin', u'ese aserrin'],
       [u'aserrín'],
       u'Aserrín is sawdust, dyed in buckets, and there is a lorry-load of it in the middle of the road.'),
  beat(u'Es para la alfombra. Para la procesión de mañana.',
       u'Say it back', u'la alfombra',
       u'¿La alfombra? ¿En la calle?', u'A carpet? On the road?',
       [u'¿la alfombra?', u'¿en la calle?'],
       [u'aserrín', u'no lo pise', u'toda la noche', u'dale'],
       [u'la alfombra en la calle', u'la alfombra'],
       [u'la alfombra'],
       u'A carpet, made of coloured sawdust, laid on the road surface. In the morning the procession walks over it, and that is what it was made for.'),
  beat(u'¡Cuidado! No lo pise, por favor.',
       u'Apologise and step back', u'no lo pise',
       u'Disculpe. No lo piso.', u'Sorry. I won’t step on it.',
       [u'disculpe', u'no lo piso'],
       [u'no lo pise', u'aserrín', u'cuídese', u'fíjese que'],
       [u'disculpe no lo piso', u'no lo piso'],
       [u'no lo pise'],
       u'No lo pise from her, no lo piso from you. Everybody says it to everybody all night and it is the first thing you will hear when you arrive.'),
  beat(u'Vamos a estar aquí hasta que amanezca.',
       u'All night?', u'toda la noche',
       u'¿Toda la noche?', u'All night?',
       [u'¿toda la noche?'],
       [u'la alfombra', u'aserrín', u'dale', u'fíjese que'],
       [u'toda la noche'],
       [u'toda la noche'],
       u'All night, by a whole family, to be walked over at seven in the morning. Saying it back is how you find out that the destruction is the whole idea.'),
 ]},
{
 'id': 'fiestas-04', 'district': 'fiestas', 'tier': 3,
 'who': u'El jinete', 'title': u'La Hípica',
 'goal': u'Watch the horse parade and understand what is being shown off',
 'culture': u'The Hípica is a parade of horses, and every horse in it belongs '
            u'to somebody the crowd can name. Whose it is and where it is '
            u'from is half the conversation and all of the point.',
 'beats': [
  beat(u'(Van pasando los caballos, uno detrás de otro, brillando.)',
       u'Ask whose they are', u'los caballos',
       u'¿De quién son los caballos?', u'Whose are the horses?',
       [u'¿de quién son', u'los caballos?'],
       [u'ese es de', u'qué bonito', u'todo bien', u'ya va'],
       [u'de quien son los caballos', u'los caballos'],
       [u'los caballos'],
       u'The horses are the point and whose they are is the second question everybody in the crowd is asking.'),
  beat(u'De las fincas. Ese es de don Alberto, el de Nandaime.',
       u'Say it back', u'ese es de',
       u'¿Ese es de Nandaime?', u'That one’s from Nandaime?',
       [u'¿ese es de', u'Nandaime?'],
       [u'los caballos', u'qué bonito', u'no ando', u'todo bien'],
       [u'ese es de nandaime', u'ese es de'],
       [u'ese es de'],
       u'Ese es de — that one belongs to. Every horse in the parade belongs to a name, and half the pleasure of watching is knowing them.'),
  beat(u'(Pasa uno blanco, bailando de lado.)',
       u'Say the right thing', u'qué bonito',
       u'Qué bonito.', u'Beautiful.',
       [u'qué bonito'],
       [u'ese es de', u'los caballos', u'ya va', u'todo bien'],
       [u'que bonito'],
       [u'qué bonito'],
       u'Qué bonito, on its own, about a horse. It is the complete and correct thing to say and nothing more is needed.'),
  beat(u'Todos los años igual. Nunca falla.',
       u'Every year?', u'todos los años',
       u'¿Todos los años?', u'Every year?',
       [u'¿todos los años?'],
       [u'qué bonito', u'los caballos', u'no ando', u'ya va'],
       [u'todos los anos'],
       [u'todos los años'],
       u'Todos los años — every year. The calendar here is fixed and heavy, and this is the parade that closes the patron saint’s fiestas.'),
 ]},
{
 'id': 'fiestas-05', 'district': 'fiestas', 'tier': 4,
 'who': u'El enmascarado', 'title': u'El Torovenado',
 'goal': u'Work out that the costumes are mocking somebody specific',
 'culture': u'Torovenado is satire in costume, and every mask in it is '
            u'somebody in particular — the mayor, the priest, the police, the '
            u'crowd itself. It is a protected licence to say out loud what is '
            u'not otherwise said, and the even-handedness is what protects '
            u'it.',
 'beats': [
  beat(u'(Pasa un hombre disfrazado de algo que le resulta muy familiar.)',
       u'Ask what is going on', u'se están burlando',
       u'¿Se están burlando?', u'Are they making fun of someone?',
       [u'¿se están burlando?'],
       [u'¿de quién?', u'del alcalde', u'vamos', u'nos vemos'],
       [u'se estan burlando'],
       [u'se están burlando'],
       u'Burlarse is to mock. The costumes are not decoration — every one of them is a person, and the crowd knows which.'),
  beat(u'¡Claro que sí! ¿No lo ve?',
       u'Ask who of', u'¿de quién?',
       u'¿De quién?', u'Of whom?',
       [u'¿de quién?'],
       [u'se están burlando', u'del alcalde', u'vamos', u'que le vaya bien'],
       [u'de quien'],
       [u'¿de quién?'],
       u'Two words, and the answer will be a name you now recognise, because you live here.'),
  beat(u'De ese de ahí, el gordo... del alcalde, pues.',
       u'Say it back', u'del alcalde',
       u'¿Del alcalde? Ideay.', u'The mayor? Well I never.',
       [u'¿del alcalde?', u'ideay'],
       [u'se están burlando', u'nadie se salva', u'vamos', u'nos vemos'],
       [u'del alcalde ideay', u'del alcalde'],
       [u'del alcalde'],
       u'The mayor, in a mask, in a parade, in front of the whole town. This is a protected tradition of saying out loud what is not said the rest of the year.'),
  beat(u'Aquí nadie se salva. Ni el cura, ni la policía, ni nosotros.',
       u'Agree', u'nadie se salva',
       u'Nadie se salva, entonces.', u'Nobody gets off, then.',
       [u'nadie se salva', u'entonces'],
       [u'del alcalde', u'se están burlando', u'vamos', u'nos vemos'],
       [u'nadie se salva entonces', u'nadie se salva'],
       [u'nadie se salva'],
       u'Nadie se salva — nobody is spared. Not the mayor, not the priest, not the people watching, and that even-handedness is the entire licence the day runs on.'),
 ]},
{
 'id': 'fiestas-06', 'district': 'fiestas', 'tier': 4,
 'who': u'La bailarina', 'title': u'El Palo de Mayo',
 'goal': u'Be dragged into dancing something you cannot dance',
 'culture': u'Palo de Mayo comes from the Caribbean coast and is danced '
            u'everywhere in May. You cannot dance it, which will not save '
            u'you, and nadie sabe is what everybody says to everybody who '
            u'tries to get out of it.',
 'beats': [
  beat(u'(Lo agarra de la mano y lo jala hacia la rueda.)',
       u'Say you cannot dance', u'no sé bailar',
       u'¡No sé bailar!', u'I can’t dance!',
       [u'¡no sé bailar!'],
       [u'nadie sabe', u'movete', u'otro día', u'disculpe'],
       [u'no se bailar'],
       [u'no sé bailar'],
       u'True, and it will not save you. Say it anyway — it is the required opening move and she has an answer ready.'),
  beat(u'¡Nadie sabe! Igual bailamos.',
       u'Check that', u'nadie sabe',
       u'¿Nadie sabe?', u'Nobody knows how?',
       [u'¿nadie sabe?'],
       [u'no sé bailar', u'movete', u'disculpe', u'¿a cómo?'],
       [u'nadie sabe'],
       [u'nadie sabe'],
       u'Nadie sabe — nobody knows how. It is not true, and it is exactly the right thing to say to somebody who is about to refuse.'),
  beat(u'¡Movete! Así, con las caderas.',
       u'Repeat the instruction back', u'movete',
       u'¿Así? ¿Me muevo así?', u'Like this? Do I move like this?',
       [u'¿así?', u'¿me muevo así?'],
       [u'movete', u'nadie sabe', u'otro día', u'disculpe'],
       [u'asi me muevo asi', u'me muevo asi'],
       [u'movete'],
       u'Movete — vos, and no accent on the o. She is your age and dancing with you, so there is no usted anywhere in this.'),
  beat(u'¡Ya vas! ¡Eso, eso!',
       u'Take the compliment', u'ya vas',
       u'¿Ya voy? ¡Ideay!', u'I’m getting it? Well!',
       [u'¿ya voy?', u'¡ideay!'],
       [u'ya vas', u'movete', u'disculpe', u'otro día'],
       [u'ya voy ideay', u'ya voy'],
       [u'ya vas'],
       u'Ya vas — you are getting it. Vas is the same in vos and tú, which is why it slips past unnoticed. The point is that she said it, and you should believe her.'),
 ]},
{
 'id': 'fiestas-07', 'district': 'fiestas', 'tier': 4,
 'who': u'Doña Marta', 'title': u'La Nochebuena',
 'goal': u'Get through Christmas Eve with somebody else’s family',
 'culture': u'The 24th is the night that matters and the 25th is for '
            u'sleeping. Nothing happens until midnight, and then everybody in '
            u'the room hugs everybody else in the room, one at a time, '
            u'including the people they met an hour ago.',
 'beats': [
  beat(u'Vecino, ¿y usted qué va a hacer el veinticuatro?',
       u'Say you have nothing on', u'nochebuena',
       u'¿La Nochebuena? Nada.', u'Christmas Eve? Nothing.',
       [u'¿la Nochebuena?', u'nada'],
       [u'a las doce', u'feliz navidad', u'gracias', u'por favor'],
       [u'la nochebuena nada', u'la nochebuena'],
       [u'nochebuena'],
       u'Nochebuena, the 24th, is the night here; the 25th is for sleeping. Saying you have nothing planned is an invitation, and she asked for that reason.'),
  beat(u'¡Entonces venga! Comemos a las doce.',
       u'Check the hour', u'a las doce',
       u'¿A las doce de la noche?', u'At midnight?',
       [u'¿a las doce', u'de la noche?'],
       [u'nochebuena', u'feliz navidad', u'gracias', u'Buenas'],
       [u'a las doce de la noche', u'a las doce'],
       [u'a las doce'],
       u'Midnight, and not a minute before. The whole meal happens after the fireworks and the children are awake for every bit of it.'),
  beat(u'(Dan las doce. Todo el mundo se abraza, uno por uno.)',
       u'Say the thing', u'feliz navidad',
       u'¡Feliz Navidad!', u'Merry Christmas!',
       [u'¡feliz Navidad!'],
       [u'a las doce', u'que se repita', u'gracias', u'por favor'],
       [u'feliz navidad'],
       [u'feliz navidad'],
       u'Said while hugging every single person in the room, one at a time, including the ones you met an hour ago.'),
  beat(u'¡Feliz Navidad, mi hijo! Y que se repita.',
       u'Answer it', u'que se repita',
       u'Que se repita, doña.', u'May it come round again, doña.',
       [u'que se repita', u'doña'],
       [u'feliz navidad', u'a las doce', u'gracias', u'Buenas'],
       [u'que se repita dona', u'que se repita'],
       [u'que se repita'],
       u'Que se repita — may it happen again. It is what you say at the end of anything good, and it is the nearest thing to a blessing that gets used casually.'),
 ]},
{
 'id': 'fiestas-08', 'district': 'fiestas', 'tier': 5,
 'who': u'Todos', 'title': u'El año viejo',
 'goal': u'Burn an old year, which is a doll, in the street at midnight',
 'culture': u'A stuffed dummy in old clothes, sitting in a chair on the '
            u'pavement all day, often dressed as somebody who annoyed '
            u'everybody that year. At midnight it is burned in the middle of '
            u'the street with fireworks inside it.',
 'beats': [
  beat(u'(Hay un muñeco de ropa vieja sentado en una silla en la acera.)',
       u'Ask what it is', u'el año viejo',
       u'¿Y ese es el año viejo?', u'Is that the old year?',
       [u'¿y ese es', u'el año viejo?'],
       [u'quemarlo', u'que se vaya', u'está bien', u'me da'],
       [u'y ese es el ano viejo', u'el ano viejo'],
       [u'el año viejo'],
       u'A stuffed dummy in old clothes, sat in a chair on the pavement. It is the old year, and it is very often dressed as somebody in particular.'),
  beat(u'Ese mismo. A las doce lo quemamos.',
       u'Ask about the burning', u'quemarlo',
       u'¿Van a quemarlo?', u'You’re going to burn it?',
       [u'¿van a quemarlo?'],
       [u'el año viejo', u'que se vaya', u'quiero', u'está bien'],
       [u'van a quemarlo', u'quemarlo'],
       [u'quemarlo'],
       u'Quemarlo — burn it. In the middle of the street, with fireworks stuffed inside it, while the whole block watches.'),
  beat(u'¡Que se vaya el año viejo! ¡Que se vaya!',
       u'Shout it with them', u'que se vaya',
       u'¡Que se vaya!', u'Let it go!',
       [u'¡que se vaya!'],
       [u'quemarlo', u'feliz año', u'me da', u'quiero'],
       [u'que se vaya'],
       [u'que se vaya'],
       u'Que se vaya — let it go. Everybody shouts it and every single person shouting means a different year.'),
  beat(u'(Dan las doce. Arde el muñeco y truenan los cohetes.)',
       u'Say it', u'feliz año',
       u'¡Feliz año!', u'Happy new year!',
       [u'¡feliz año!'],
       [u'que se vaya', u'el año viejo', u'está bien', u'me da'],
       [u'feliz ano'],
       [u'feliz año'],
       u'Feliz año, not feliz año nuevo — everybody drops the nuevo. And then you hug thirty people, again.'),
 ]},
{
 'id': 'afuera-01', 'district': 'afuera', 'tier': 3,
 'who': u'La artesana', 'title': u'Masaya',
 'goal': u'Buy a hammock and get the price down',
 'culture': u'Masaya hammocks are the good ones and everybody knows it, which '
            u'is reflected in the first number you are given. The haggle has '
            u'the same shape as the leather bag in El Centro, one letter '
            u'different: una hamaca is feminine, so it is me la deja en.',
 'beats': [
  beat(u'Adelante. Hamacas de Masaya, hechas a mano.',
       u'Ask the price', u'una hamaca',
       u'¿A cómo una hamaca?', u'How much is a hammock?',
       [u'¿a cómo', u'una hamaca?'],
       [u'está muy caro', u'me la llevo', u'ideay', u'ni modo'],
       [u'a como una hamaca', u'una hamaca'],
       [u'una hamaca'],
       u'¿A cómo? one last time. It has worked on a mango, a bundle of firewood and now a hammock.'),
  beat(u'Mil ochocientos, y es de las buenas.',
       u'Say it is too dear', u'está muy caro',
       u'Uy, está muy caro.', u'Oof, that’s very dear.',
       [u'uy', u'está muy caro'],
       [u'una hamaca', u'me la llevo', u'vaya pues', u'ni modo'],
       [u'uy esta muy caro', u'esta muy caro'],
       [u'está muy caro'],
       u'You have done this in the market. The uy in front is free and it does half the work for you.'),
  beat(u'Es que lleva tres días de trabajo, mire el tejido.',
       u'Make the counter', u'¿me lo deja en?',
       u'¿Me la deja en mil doscientos?', u'Would you let me have it for twelve hundred?',
       [u'¿me la deja en', u'mil doscientos?'],
       [u'está muy caro', u'me la llevo', u'ideay', u'vaya pues'],
       [u'me la deja en mil doscientos', u'me la deja en'],
       [u'¿me lo deja en?'],
       u'Me lo deja en, me la deja en — the lo or the la follows the thing, and a hamaca is feminine. Same move as the leather bag, one letter different.'),
  beat(u'Mil cuatrocientos y es suya. Ya no gano nada.',
       u'Take it', u'me la llevo',
       u'Me la llevo. Trato hecho.', u'I’ll take it. Done deal.',
       [u'me la llevo', u'trato hecho'],
       [u'está muy caro', u'otro día', u'ni modo', u'ideay'],
       [u'me la llevo trato hecho', u'me la llevo'],
       [u'me la llevo'],
       u'Me la llevo — I’ll take it. Say it, pay it, and do not reopen the price. You learned that from the man with the leather bags.'),
 ]},
{
 'id': 'afuera-02', 'district': 'afuera', 'tier': 3,
 'who': u'El alfarero', 'title': u'San Juan de Oriente',
 'goal': u'Watch pottery being made and ask how long it took to learn',
 'culture': u'In this village the pottery goes four or five generations deep '
            u'in most houses. Ask about the years rather than the technique — '
            u'the years are the answer he wants to give you.',
 'beats': [
  beat(u'(Está centrando el barro con el pie en el torno.)',
       u'Ask how long it took to learn', u'¿cuánto tardó?',
       u'¿Cuánto tardó en aprender?', u'How long did it take you to learn?',
       [u'¿cuánto tardó', u'en aprender?'],
       [u'desde chavalo', u'mi papá', u'así es', u'con permiso'],
       [u'cuanto tardo en aprender', u'cuanto tardo'],
       [u'¿cuánto tardó?'],
       u'Ask the years, not the technique. The years are the answer he would rather give.'),
  beat(u'Uf. Desde chavalo ando en esto.',
       u'Since he was a kid?', u'desde chavalo',
       u'¿Desde chavalo?', u'Since you were a boy?',
       [u'¿desde chavalo?'],
       [u'¿cuánto tardó?', u'mi papá', u'me deja en', u'así es'],
       [u'desde chavalo'],
       [u'desde chavalo'],
       u'Desde chavalo — since I was a kid. The same word Roberto taught you next door, now describing a whole working life.'),
  beat(u'Mi papá me enseñó. Y a él le enseñó el suyo.',
       u'Ask about his father', u'mi papá',
       u'¿Su papá también?', u'Your father as well?',
       [u'¿su papá', u'también?'],
       [u'desde chavalo', u'está lindo', u'con permiso', u'así es'],
       [u'su papa tambien', u'su papa'],
       [u'mi papá'],
       u'Mi papá from him, su papá from you. In this village the wheel goes four or five generations deep in most houses on the street.'),
  beat(u'(Levanta la pieza terminada y se la enseña.)',
       u'Say the right thing about it', u'está lindo',
       u'Está lindo. De verdad.', u'That’s lovely. Really.',
       [u'está lindo', u'de verdad'],
       [u'desde chavalo', u'mi papá', u'me deja en', u'con permiso'],
       [u'esta lindo de verdad', u'esta lindo'],
       [u'está lindo'],
       u'Lindo rather than bonito, for something somebody made with their hands. It is a small choice and he will hear it.'),
 ]},
{
 'id': 'afuera-03', 'district': 'afuera', 'tier': 4,
 'who': u'El del mirador', 'title': u'Catarina',
 'goal': u'Look down at the laguna and be told what you are seeing',
 'culture': u'From the mirador at Catarina you can see the crater lake, '
            u'Mombacho, and the town you live in. It is also where Spanish '
            u'finally makes you use its third distance: este, ese and aquel, '
            u'that last one for things far enough away to point at.',
 'beats': [
  beat(u'(Doscientos metros abajo hay agua, redonda y quieta.)',
       u'Ask what it is', u'la laguna',
       u'¿Esa es la laguna?', u'Is that the lagoon?',
       [u'¿esa es', u'la laguna?'],
       [u'ahí está', u'aquel es', u'cuídese', u'dale'],
       [u'esa es la laguna', u'la laguna'],
       [u'la laguna'],
       u'The Laguna de Apoyo: a crater full of water, two hundred metres below you and about the same again deep.'),
  beat(u'Ahí está. La Laguna de Apoyo.',
       u'Say it back', u'ahí está',
       u'Ahí está. Qué grande.', u'There it is. It’s huge.',
       [u'ahí está', u'qué grande'],
       [u'la laguna', u'aquel es', u'fíjese que', u'dale'],
       [u'ahi esta que grande', u'ahi esta'],
       [u'ahí está'],
       u'Ahí está — there it is. Two words that hand something over, and you last heard them from the cuidacarros about your moto.'),
  beat(u'Y aquel es el Mombacho. Y aquel de allá, Granada.',
       u'Ask which is which', u'aquel es',
       u'¿Y aquel es Granada?', u'And that far one is Granada?',
       [u'¿y aquel es', u'Granada?'],
       [u'la laguna', u'ahí está', u'cuídese', u'dale'],
       [u'y aquel es granada', u'aquel es'],
       [u'aquel es'],
       u'Aquel is that one over there, further off than ese. Spanish has three distances and this viewpoint is where you finally need the third.'),
  beat(u'Desde aquí se ve todo, joven. Todo.',
       u'Agree', u'se ve todo',
       u'Se ve todo desde aquí.', u'You can see everything from here.',
       [u'se ve todo', u'desde aquí'],
       [u'aquel es', u'ahí está', u'fíjese que', u'cuídese'],
       [u'se ve todo desde aqui', u'se ve todo'],
       [u'se ve todo'],
       u'From up here you can see the town you live in. It is a strange feeling and a good one, and it is worth the trip on its own.'),
 ]},
{
 'id': 'afuera-04', 'district': 'afuera', 'tier': 4,
 'who': u'El guía de Mombacho', 'title': u'Mombacho',
 'goal': u'Climb a volcano with a guide who talks the whole way',
 'culture': u'Mombacho is the volcano you have been looking at from the plaza '
            u'since your first morning. Going slowly up it is not a failure, '
            u'it is the method, and ya casi is a kindness rather than a '
            u'measurement.',
 'beats': [
  beat(u'Buenas. ¿Sube hoy?',
       u'Ask about the climb', u'el volcán',
       u'¿Subimos el volcán?', u'Are we going up the volcano?',
       [u'¿subimos', u'el volcán?'],
       [u'ahí arriba', u'despacio', u'todo bien', u'ya va'],
       [u'subimos el volcan', u'el volcan'],
       [u'el volcán'],
       u'Mombacho is the shape on the horizon you have been looking at from Parque Central since your first morning. Today you are on it.'),
  beat(u'Ahí arriba está el cráter. Hora y media.',
       u'Up there?', u'ahí arriba',
       u'¿Ahí arriba, hasta el cráter?', u'Up there, all the way to the crater?',
       [u'¿ahí arriba,', u'hasta el cráter?'],
       [u'el volcán', u'despacio', u'no ando', u'todo bien'],
       [u'ahi arriba hasta el crater', u'ahi arriba'],
       [u'ahí arriba'],
       u'Ahí arriba — up there. He will point at cloud, because the top of it is in cloud most days of the year.'),
  beat(u'Despacio, despacio. No hay prisa, joven.',
       u'Agree to go slowly', u'despacio',
       u'Despacio, sí. Voy despacio.', u'Slowly, yes. I’m going slowly.',
       [u'despacio', u'sí', u'voy despacio'],
       [u'ya casi', u'el volcán', u'ya va', u'todo bien'],
       [u'despacio si voy despacio', u'voy despacio', u'despacio'],
       [u'despacio'],
       u'Despacio is the whole technique and he says it to everybody. Going slowly up a volcano is not failing at it, it is how it is done.'),
  beat(u'Ya casi, ya casi. Ahí está.',
       u'Ask whether that is true', u'ya casi',
       u'¿Ya casi de verdad?', u'Really almost there?',
       [u'¿ya casi', u'de verdad?'],
       [u'despacio', u'ahí arriba', u'no ando', u'ya va'],
       [u'ya casi de verdad', u'ya casi'],
       [u'ya casi'],
       u'Ya casi means almost there and it is said from about the halfway point onwards. It is a kindness rather than a measurement.'),
 ]},
{
 'id': 'afuera-05', 'district': 'afuera', 'tier': 4,
 'who': u'El de la laguna', 'title': u'La Laguna de Apoyo',
 'goal': u'Swim in a crater and be warned about the current',
 'culture': u'The water is warm because there is a volcano underneath it, '
            u'which is not a metaphor. The afternoon wind on that crater is '
            u'the reason there are rules, and salga ya is not a suggestion '
            u'even though it is delivered like one.',
 'beats': [
  beat(u'Puede meterse. Está buena hoy.',
       u'Ask if it is deep', u'está honda',
       u'¿Está honda?', u'Is it deep?',
       [u'¿está honda?'],
       [u'no vaya lejos', u'el agua es', u'vamos', u'nos vemos'],
       [u'esta honda'],
       [u'está honda'],
       u'Honda, not profunda — the everyday word. The answer is about two hundred metres and nobody has ever touched the bottom of it.'),
  beat(u'Bien honda. No vaya lejos, ¿oyó?',
       u'Say it back', u'no vaya lejos',
       u'¿No voy lejos?', u'Not far out?',
       [u'¿no voy lejos?'],
       [u'está honda', u'el agua es', u'que le vaya bien', u'vamos'],
       [u'no voy lejos'],
       [u'no vaya lejos'],
       u'No vaya from him, no voy from you. It is a real warning delivered gently: the far side is a very long way back.'),
  beat(u'Y el agua es tibia, fíjese. Meta la mano.',
       u'Ask about that', u'el agua es',
       u'¿El agua es caliente?', u'The water is warm?',
       [u'¿el agua es', u'caliente?'],
       [u'está honda', u'no vaya lejos', u'nos vemos', u'vamos'],
       [u'el agua es caliente', u'el agua es'],
       [u'el agua es'],
       u'It is warm because there is a volcano underneath it. That is not a figure of speech.'),
  beat(u'¡Salga ya! ¡Ya viene el viento!',
       u'Get out', u'salga ya',
       u'Ya salgo. Ya voy.', u'Coming out. On my way.',
       [u'ya salgo', u'ya voy'],
       [u'salga ya', u'no vaya lejos', u'vamos', u'nos vemos'],
       [u'ya salgo ya voy', u'ya salgo'],
       [u'salga ya'],
       u'Salga ya from him, ya salgo from you, and do not argue about it. The afternoon wind on that crater is the reason there are rules at all.'),
 ]},
{
 'id': 'afuera-06', 'district': 'afuera', 'tier': 5,
 'who': u'El caficultor', 'title': u'El cafetal',
 'goal': u'Pick coffee for a day and be judged on your speed',
 'culture': u'El corte is the coffee harvest and it is the axis a third of '
            u'the country’s year turns on. You are paid by weight, green '
            u'beans ruin the batch, and the people who do this for a living '
            u'will be four times faster than you by lunchtime.',
 'beats': [
  beat(u'Buenas. ¿Viene a ver el cafetal?',
       u'Ask about the harvest', u'el corte',
       u'¿Cuándo es el corte?', u'When is the harvest?',
       [u'¿cuándo es', u'el corte?'],
       [u'sólo las rojas', u'con las dos manos', u'disculpe', u'otro día'],
       [u'cuando es el corte', u'el corte'],
       [u'el corte'],
       u'El corte is the picking. For a third of this country it is the axis the whole year turns on.'),
  beat(u'Ahorita mismo. Agarre un canasto, pues. Pero sólo las rojas.',
       u'Check the rule', u'sólo las rojas',
       u'¿Sólo las rojas?', u'Only the red ones?',
       [u'¿sólo las rojas?'],
       [u'el corte', u'con las dos manos', u'¿a cómo?', u'otro día'],
       [u'solo las rojas'],
       [u'sólo las rojas'],
       u'Only the red ones. Green ones ruin the batch, and you are paid by weight — so the temptation is real and so is the rule.'),
  beat(u'Y con las dos manos, si no, no avanza.',
       u'Say it back', u'con las dos manos',
       u'¿Con las dos manos?', u'With both hands?',
       [u'¿con las dos manos?'],
       [u'sólo las rojas', u'el corte', u'disculpe', u'¿a cómo?'],
       [u'con las dos manos'],
       [u'con las dos manos'],
       u'Both hands, both sides of the branch, all day. The people doing this for a living will be four times faster than you by lunchtime.'),
  beat(u'Va aprendiendo, joven. Va aprendiendo.',
       u'Take the compliment', u'va aprendiendo',
       u'Voy aprendiendo, pues.', u'I’m getting there.',
       [u'voy aprendiendo', u'pues'],
       [u'va aprendiendo', u'el corte', u'otro día', u'disculpe'],
       [u'voy aprendiendo pues', u'voy aprendiendo'],
       [u'va aprendiendo'],
       u'Va aprendiendo from him, voy aprendiendo from you. It is the highest praise you will get on your first day and it is meant kindly.'),
 ]},
{
 'id': 'afuera-07', 'district': 'afuera', 'tier': 5,
 'who': u'El de Nandaime', 'title': u'La carretera',
 'goal': u'Break down between towns and get help from strangers',
 'culture': u'Somebody will stop. Asking a stranger on the road for a tow is '
            u'completely ordinary, and Dios se lo pague — the biggest '
            u'thank-you there is — is exactly what this situation is for. '
            u'You last heard it from the woman with the suitcases.',
 'beats': [
  beat(u'(Un carro se orilla detrás de usted.) ¿Qué pasó, amigo?',
       u'Say what happened', u'se me quedó',
       u'Se me quedó el carro.', u'The car died on me.',
       [u'se me quedó', u'el carro'],
       [u'no arranca', u'¿me da un jalón?', u'gracias', u'Buenas'],
       [u'se me quedo el carro', u'se me quedo'],
       [u'se me quedó'],
       u'Se me quedó — it stopped on me. The me puts it on you without making it your fault, which is exactly the right amount of blame.'),
  beat(u'¿Y no arranca?',
       u'Confirm', u'no arranca',
       u'No arranca nada.', u'It won’t start at all.',
       [u'no arranca', u'nada'],
       [u'se me quedó', u'¿me da un jalón?', u'gracias', u'por favor'],
       [u'no arranca nada', u'no arranca'],
       [u'no arranca'],
       u'No arranca — it will not start. Two words that will get somebody’s head under your bonnet within a minute on any road in this country.'),
  beat(u'(Se asoma al motor un rato.) Uy. Eso es taller.',
       u'Ask for a tow', u'¿me da un jalón?',
       u'¿Me da un jalón?', u'Could you give me a tow?',
       [u'¿me da un jalón?'],
       [u'no arranca', u'se me quedó', u'Buenas', u'por favor'],
       [u'me da un jalon'],
       [u'¿me da un jalón?'],
       u'Un jalón is a tow or a lift. Asking a stranger on the road for one is completely ordinary, and he had already stopped before you asked.'),
  beat(u'Va pues. Amarre ahí y vamos despacio hasta Nandaime.',
       u'Thank him the big way', u'Dios se lo pague',
       u'Dios se lo pague.', u'God repay you.',
       [u'Dios se lo pague'],
       [u'gracias', u'no arranca', u'Buenas', u'por favor'],
       [u'dios se lo pague', u'dios se lo pague gracias'],
       [u'Dios se lo pague'],
       u'The largest thank-you there is, and the one the woman with the suitcases used on you at the terminal. This is the situation it exists for.'),
 ]},
{
 'id': 'afuera-08', 'district': 'afuera', 'tier': 5,
 'who': u'Los de Masatepe', 'title': u'La sopa',
 'goal': u'Eat sopa de mondongo and be watched while you do it',
 'culture': u'Masatepe is where people drive to eat mondongo, which is tripe '
            u'soup. The whole table will watch your first spoonful. Honesty '
            u'is completely fine — está fuerte is accurate and acceptable — '
            u'and pulling a face is the only thing that is not.',
 'beats': [
  beat(u'¿Ya probó el mondongo, joven?',
       u'Ask what is in it, before', u'mondongo',
       u'¿Qué lleva el mondongo?', u'What’s in the mondongo?',
       [u'¿qué lleva', u'el mondongo?'],
       [u'primera vez', u'está fuerte', u'me da', u'está bien'],
       [u'que lleva el mondongo', u'el mondongo'],
       [u'mondongo'],
       u'Ask before, not after. Mondongo is tripe, and Masatepe is where people drive from other departments to eat it.'),
  beat(u'Panza de res, yuca, chayote... ¿nunca ha comido?',
       u'Say it is your first', u'primera vez',
       u'Es mi primera vez.', u'It’s my first time.',
       [u'es mi', u'primera vez'],
       [u'mondongo', u'está fuerte', u'quiero', u'me da'],
       [u'es mi primera vez', u'primera vez'],
       [u'primera vez'],
       u'Say it. Everybody at that table wants to watch a first spoonful, and you may as well let them enjoy it.'),
  beat(u'(Toda la mesa lo está viendo. Pruebe.)',
       u'Be honest', u'está fuerte',
       u'Está fuerte.', u'It’s strong.',
       [u'está fuerte'],
       [u'primera vez', u'me gustó', u'está bien', u'me da'],
       [u'esta fuerte'],
       [u'está fuerte'],
       u'Está fuerte — it is strong. Honest, accurate and completely acceptable. Pulling a face is the thing that would not be.'),
  beat(u'(Se termina el plato. Siguen viéndolo.)',
       u'Say the thing they are waiting for', u'me gustó',
       u'Pero me gustó.', u'But I liked it.',
       [u'pero', u'me gustó'],
       [u'está fuerte', u'primera vez', u'quiero', u'está bien'],
       [u'pero me gusto', u'me gusto'],
       [u'me gustó'],
       u'Pero me gustó — but I liked it. If it is true, this is the sentence the whole table was waiting for, and you will immediately be given more.'),
 ]},
]

HINTS = [
 {'kind': u'doña en la puerta', 'district': 'fiestas',
  'says': u'El siete de diciembre es la Purísima. Váyase conmigo y aprende a gritar en las puertas.',
  'en': u'The seventh of December is the Purísima. Come with me and learn to shout at the doors.',
  'points_at': ['fiestas-01', 'fiestas-02']},
 {'kind': u'chavalo en bici', 'district': 'fiestas',
  'says': u'A las seis suenan las campanas y sale todo el mundo. Ahí empieza la gritería.',
  'en': u'At six the bells go and everybody comes out. That is when the Gritería starts.',
  'points_at': ['fiestas-02']},
 {'kind': u'vendedora', 'district': 'fiestas',
  'says': u'En Semana Santa hacen las alfombras de aserrín en la calle. No las vaya a pisar.',
  'en': u'In Holy Week they make the sawdust carpets in the street. Mind you do not step on them.',
  'points_at': ['fiestas-03']},
 {'kind': u'viejo de la esquina', 'district': 'fiestas',
  'says': u'La Hípica es de los caballos. Cada uno es de una finca y todos saben de cuál.',
  'en': u'The Hípica is the horses. Each one belongs to an estate and everybody knows which.',
  'points_at': ['fiestas-04']},
 {'kind': u'obrero', 'district': 'fiestas',
  'says': u'En el Torovenado se disfrazan del alcalde, del cura, de todos. Nadie se salva.',
  'en': u'At the Torovenado they dress up as the mayor, the priest, everybody. Nobody is spared.',
  'points_at': ['fiestas-05']},
 {'kind': u'chavalo en bici', 'district': 'fiestas',
  'says': u'En mayo bailan el Palo de Mayo en la calle. Y lo van a jalar a usted, no se salva.',
  'en': u'In May they dance the Palo de Mayo in the street. And they will drag you in, you will not escape.',
  'points_at': ['fiestas-06']},
 {'kind': u'doña en la puerta', 'district': 'fiestas',
  'says': u'En Nochebuena se come a las doce de la noche, no antes. Y se abraza a todo el mundo.',
  'en': u'On Christmas Eve you eat at midnight, not before. And you hug everybody.',
  'points_at': ['fiestas-07']},
 {'kind': u'viejo de la esquina', 'district': 'fiestas',
  'says': u'El treinta y uno queman el año viejo en la calle. Un muñeco de ropa vieja, con cohetes.',
  'en': u'On the thirty-first they burn the old year in the street. A dummy in old clothes, with fireworks.',
  'points_at': ['fiestas-08']},
 {'kind': u'caponero', 'district': 'afuera',
  'says': u'¿Va para Masaya? Las hamacas allá son las buenas, pero pida rebaja.',
  'en': u'Going to Masaya? The hammocks there are the good ones, but ask for a discount.',
  'points_at': ['afuera-01']},
 {'kind': u'vendedora', 'district': 'afuera',
  'says': u'En San Juan de Oriente hacen la cerámica. Pregúntele al alfarero desde cuándo trabaja.',
  'en': u'In San Juan de Oriente they make the pottery. Ask the potter how long he has been at it.',
  'points_at': ['afuera-02']},
 {'kind': u'obrero', 'district': 'afuera',
  'says': u'Del mirador de Catarina se ve la laguna, el Mombacho y hasta Granada.',
  'en': u'From the viewpoint at Catarina you can see the lagoon, Mombacho and even Granada.',
  'points_at': ['afuera-03']},
 {'kind': u'chavalo en bici', 'district': 'afuera',
  'says': u'Al Mombacho se sube con guía. Hora y media, pero despacio se llega.',
  'en': u'You go up Mombacho with a guide. An hour and a half, but slowly you get there.',
  'points_at': ['afuera-04']},
 {'kind': u'doña en la puerta', 'district': 'afuera',
  'says': u'En la laguna se puede nadar, pero no vaya lejos. Por la tarde entra el viento.',
  'en': u'You can swim in the lagoon, but do not go far out. The wind comes up in the afternoon.',
  'points_at': ['afuera-05']},
 {'kind': u'viejo de la esquina', 'district': 'afuera',
  'says': u'En el corte pagan por peso. Pero si corta las verdes, le echan a perder el saco.',
  'en': u'On the harvest they pay by weight. But if you pick the green ones you ruin the sack.',
  'points_at': ['afuera-06']},
 {'kind': u'cuidacarros', 'district': 'afuera',
  'says': u'Si se le queda el carro en la carretera, alguien para. Aquí siempre para alguien, jefe.',
  'en': u'If your car dies on the highway, somebody stops. Somebody always stops here, boss.',
  'points_at': ['afuera-07']},
 {'kind': u'vendedora', 'district': 'afuera',
  'says': u'En Masatepe está la sopa de mondongo. Fuerte, pero hay que probarla una vez.',
  'en': u'The mondongo soup is in Masatepe. Strong, but you have to try it once.',
  'points_at': ['afuera-08']},
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
