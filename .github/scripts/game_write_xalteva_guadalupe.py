# -*- coding: utf-8 -*-
"""Writes Xalteva and Guadalupe -- twenty missions -- and their crowd.

Xalteva is the old quarter west of the centre: churches, quiet streets, and
people with time. The Spanish is slower and older, and half of it is listening
rather than transacting.

Guadalupe slopes east towards the water: families, workshops, kids in the
street. This is the district where the game finally uses VOS -- the kid on the
bike and the chavalos on the pitch are the first people in Granada you would
never address as usted, and voseo is what the whole course is for.

Same self-checks as the other batches: winnable in written order, every
accepted answer buildable from the tray, no chunk twice in one tray, every
chunk the spine promises actually taught, nobody unfindable.
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
# ── Xalteva ─────────────────────────────────────────────────────────────
{
 'id': 'xalteva-01', 'district': 'xalteva', 'tier': 1,
 'who': u'Doña de los caites', 'title': u'¿Por dónde?',
 'goal': u'Ask the way and get an answer with no street names in it',
 'culture': u'Nobody here navigates by street names, even the ones that have '
            u'them. Directions are blocks, and the two fixed points are the '
            u'lake and the mountain: al lago is east and arriba is west, '
            u'towards Mombacho. Learn those two words and the city becomes '
            u'legible.',
 'beats': [
  beat(u'Buenas tardes, mi hijo. ¿Anda perdido?',
       u'Ask where the church is', u'¿dónde queda?',
       u'Buenas. ¿Dónde queda la iglesia?', u'Hello. Where’s the church?',
       [u'Buenas', u'¿dónde queda', u'la iglesia?'],
       [u'gracias', u'al lago', u'cuídese', u'no ando'],
       [u'buenas donde queda la iglesia', u'donde queda la iglesia',
        u'donde queda'],
       [u'¿dónde queda?'],
       u'¿Dónde queda? is where something is located, and it is the question you will ask most often in your first month.'),
  beat(u'Ahí nomás. Dos cuadras al lago y ya la ve.',
       u'Say it back to be sure', u'dos cuadras',
       u'¿Dos cuadras al lago?', u'Two blocks towards the lake?',
       [u'¿dos cuadras', u'al lago?'],
       [u'arriba', u'gracias', u'cuídese', u'no ando'],
       [u'dos cuadras al lago', u'dos cuadras'],
       [u'dos cuadras', u'al lago'],
       u'Al lago means east, because the lake is east of everything in this city. Repeating the direction back is how you avoid walking twenty minutes the wrong way.'),
  beat(u'Al lago, sí. Y si se pasa, se devuelve para arriba.',
       u'Check the other direction too', u'arriba',
       u'¿Y arriba es para allá?', u'And arriba is that way?',
       [u'¿y arriba', u'es para allá?'],
       [u'al lago', u'dos cuadras', u'gracias', u'cuídese'],
       [u'y arriba es para alla', u'arriba es para alla'],
       [u'arriba'],
       u'Arriba is west, towards Mombacho, and it has nothing to do with up. Al lago and arriba are the whole compass here.'),
  beat(u'Así es, mi hijo. Vaya con cuidado.',
       u'Thank her and go', u'cuídese',
       u'Gracias. Cuídese.', u'Thank you. Take care.',
       [u'gracias', u'cuídese'],
       [u'otro día', u'al lago', u'no ando', u'arriba'],
       [u'gracias cuidese', u'cuidese', u'gracias'],
       [u'cuídese'],
       u'Cuídese back at somebody who has just looked after you is the whole of good manners here, and it costs one word.'),
 ]},
{
 'id': 'xalteva-02', 'district': 'xalteva', 'tier': 2,
 'who': u'El sacristán', 'title': u'La iglesia',
 'goal': u'Get into a church that is shut, and be told why',
 'culture': u'The old churches are locked between services because they have '
            u'been robbed. The sacristán is not turning you away — he is '
            u'telling you the hour to come back, and if you take it he will '
            u'let you in and tell you what you are looking at.',
 'beats': [
  beat(u'No, no. Está cerrado, joven.',
       u'Ask when it opens', u'está cerrado',
       u'¿Está cerrado? ¿A qué hora abre?', u'It’s closed? What time does it open?',
       [u'¿está cerrado?', u'¿a qué hora abre?'],
       [u'con permiso', u'gracias', u'otro día', u'venga después'],
       [u'esta cerrado a que hora abre', u'a que hora abre', u'esta cerrado'],
       [u'está cerrado'],
       u'Está cerrado is a fact, not a refusal. The next question is always the hour, and he is expecting you to ask it.'),
  beat(u'A las cinco, para la misa. Antes no.',
       u'Say it back — five', u'a las cinco',
       u'A las cinco, entonces.', u'At five, then.',
       [u'a las cinco', u'entonces'],
       [u'a las tres', u'gracias', u'otro día', u'venga después'],
       [u'a las cinco entonces', u'a las cinco'],
       [u'a las cinco'],
       u'Hours here are said plainly and meant loosely, except for mass, which starts when it says it will.'),
  beat(u'Venga después de la misa y se la enseño toda.',
       u'Accept the offer', u'venga después',
       u'Vengo después. Muy amable.', u'I’ll come afterwards. That’s very kind.',
       [u'vengo después', u'muy amable'],
       [u'otro día', u'gracias', u'con permiso', u'a las cinco'],
       [u'vengo despues muy amable', u'vengo despues'],
       [u'venga después', u'muy amable'],
       u'He says venga, you say vengo — the same trip from the two ends of it. Turning his invitation into your plan is what gets you the tour.'),
  beat(u'Ahí lo espero, pues. Con permiso.',
       u'Excuse yourself properly', u'con permiso',
       u'Con permiso. Gracias.', u'Excuse me. Thank you.',
       [u'con permiso', u'gracias'],
       [u'otro día', u'cuídese', u'a las cinco', u'muy amable'],
       [u'con permiso gracias', u'con permiso'],
       [u'con permiso'],
       u'Con permiso is how you leave, how you pass somebody in a doorway and how you interrupt. Not saying it is the rudest thing a quiet person can do here.'),
 ]},
{
 'id': 'xalteva-03', 'district': 'xalteva', 'tier': 2,
 'who': u'La beata', 'title': u'La misa',
 'goal': u'Talk about mass without pretending to be devout',
 'culture': u'She will ask, and lying is worse than saying no. The honest '
            u'answer given respectfully is completely acceptable here — what '
            u'is not acceptable is being dismissive about it. Primero Dios is '
            u'said by believers and non-believers alike; it means we will see.',
 'beats': [
  beat(u'¿Y usted no viene a misa, joven? No lo he visto.',
       u'Say you are not from here', u'no soy de aquí',
       u'No soy de aquí, doña.', u'I’m not from here, doña.',
       [u'no soy de aquí', u'doña'],
       [u'primero Dios', u'gracias', u'algún día', u'cuídese'],
       [u'no soy de aqui dona', u'no soy de aqui'],
       [u'no soy de aquí'],
       u'It is the true answer and it is not a brush-off. Doña on the end is what makes it courteous rather than defensive.'),
  beat(u'Ah, pero Dios está en todas partes, mi hijo.',
       u'Say you respect it', u'respeto mucho',
       u'Lo respeto mucho.', u'I have a lot of respect for it.',
       [u'lo respeto mucho'],
       [u'no soy de aquí', u'algún día', u'gracias', u'primero Dios'],
       [u'lo respeto mucho'],
       [u'respeto mucho'],
       u'Respect without agreement, said plainly. She will accept it, because it is the answer she was actually asking for.'),
  beat(u'Bueno. Ahí lo espero un domingo.',
       u'Leave it open — some day', u'algún día',
       u'Algún día, doña.', u'One of these days, doña.',
       [u'algún día', u'doña'],
       [u'nunca', u'primero Dios', u'gracias', u'cuídese'],
       [u'algun dia dona', u'algun dia'],
       [u'algún día'],
       u'Algún día is a soft maybe that neither of you will hold the other to. Saying never would be answering a question she did not ask.'),
  beat(u'Primero Dios, mi hijo. Primero Dios.',
       u'Answer it the way it is meant', u'primero Dios',
       u'Primero Dios. Cuídese.', u'God willing. Take care.',
       [u'primero Dios', u'cuídese'],
       [u'algún día', u'gracias', u'no soy de aquí', u'otro día'],
       [u'primero dios cuidese', u'primero dios'],
       [u'primero Dios'],
       u'Primero Dios is said by everybody here, devout or not. It means we will see, and answering it back closes the conversation warmly and commits you to nothing.'),
 ]},
{
 'id': 'xalteva-04', 'district': 'xalteva', 'tier': 3,
 'who': u'Don Chombo', 'title': u'El viejo de la esquina',
 'goal': u'Let an old man tell you what this street used to be',
 'culture': u'He has all afternoon and the only thing being asked of you is '
            u'that you stay for it. There is nothing to win here and no '
            u'transaction — this is the mission that teaches you that '
            u'listening is a thing you do in Spanish too.',
 'beats': [
  beat(u'¿Usted vive aquí ahora? Esta calle antes era otra cosa.',
       u'Ask what it was like before', u'antes',
       u'¿Cómo era antes?', u'What was it like before?',
       [u'¿cómo era', u'antes?'],
       [u'ya no es igual', u'gracias', u'otro día', u'en aquel tiempo'],
       [u'como era antes', u'antes'],
       [u'antes'],
       u'Antes does the work of a whole tense here. Ask it once and you have twenty minutes of answer.'),
  beat(u'Uy. En aquel tiempo esto era todo de tierra. No pasaba un carro.',
       u'Say it back with wonder', u'en aquel tiempo',
       u'¿En aquel tiempo no había carros?', u'Back then there were no cars?',
       [u'¿en aquel tiempo', u'no había carros?'],
       [u'antes', u'ya no es igual', u'gracias', u'usted no vio eso'],
       [u'en aquel tiempo no habia carros', u'en aquel tiempo'],
       [u'en aquel tiempo'],
       u'En aquel tiempo is his phrase, not yours yet. Using it back tells him you are following, and he will keep going.'),
  beat(u'Ni uno. Y la gente se sentaba afuera. Ahora ya no es igual.',
       u'Agree that it has changed', u'ya no es igual',
       u'Ya no es igual, dice usted.', u'It’s not the same any more, you say.',
       [u'ya no es igual', u'dice usted'],
       [u'antes', u'en aquel tiempo', u'gracias', u'otro día'],
       [u'ya no es igual dice usted', u'ya no es igual'],
       [u'ya no es igual'],
       u'Agreeing with the complaint is the correct move and it is free. He is not asking you to fix anything.'),
  beat(u'Usted no vio eso. Usted no lo vio.',
       u'Admit it — you did not', u'usted no vio eso',
       u'No, yo no vi eso.', u'No, I didn’t see that.',
       [u'no', u'yo no vi eso'],
       [u'ya no es igual', u'antes', u'gracias', u'en aquel tiempo'],
       [u'no yo no vi eso', u'yo no vi eso'],
       [u'usted no vio eso'],
       u'Usted no vio eso from him, yo no vi eso from you. He is not scoring a point — he is telling you that you had to be there, and agreeing is the whole of your part.'),
 ]},
{
 'id': 'xalteva-05', 'district': 'xalteva', 'tier': 3,
 'who': u'La costurera', 'title': u'El pantalón',
 'goal': u'Get trousers taken up and agree when they are ready',
 'culture': u'Everything gets mended here rather than replaced, and there is '
            u'a costurera on nearly every block doing it for the price of a '
            u'coffee. Point at the length you want and name a day: both of '
            u'those are more reliable than any measurement.',
 'beats': [
  beat(u'Buenas. ¿Qué se le ofrece?',
       u'Ask her to take them up', u'me lo arregla',
       u'Buenas. ¿Me lo arregla?', u'Hello. Could you alter this for me?',
       [u'Buenas', u'¿me lo arregla?'],
       [u'gracias', u'por favor', u'el jueves', u'aquí'],
       [u'buenas me lo arregla', u'me lo arregla'],
       [u'me lo arregla'],
       u'Me lo arregla covers taking up, letting out, patching and mending. Show her the garment and the verb does the rest.'),
  beat(u'¿De dónde? ¿Del ruedo?',
       u'Point — here', u'aquí',
       u'Aquí, por favor.', u'Here, please.',
       [u'aquí', u'por favor'],
       [u'el jueves', u'gracias', u'me lo arregla', u'más'],
       [u'aqui por favor', u'aqui'],
       [u'aquí'],
       u'Aquí with a finger on the cloth beats any number of centimetres, and it is what she would rather you did.'),
  beat(u'Va pues. Se lo dejo bien.',
       u'Ask when it will be ready', u'¿para cuándo?',
       u'¿Para cuándo?', u'When for?',
       [u'¿para cuándo?'],
       [u'gracias', u'el jueves', u'por favor', u'aquí'],
       [u'para cuando'],
       [u'¿para cuándo?'],
       u'¿Para cuándo? asks the day it will be done. Ask now, because ahorita is not a time and you will be told ahorita.'),
  beat(u'Véngase el jueves, después de las tres.',
       u'Fix the day', u'el jueves',
       u'El jueves, entonces. Gracias.', u'Thursday, then. Thank you.',
       [u'el jueves', u'entonces', u'gracias'],
       [u'mañana', u'aquí', u'por favor', u'¿para cuándo?'],
       [u'el jueves entonces gracias', u'el jueves entonces', u'el jueves'],
       [u'el jueves'],
       u'Name the day back and it becomes an appointment. Leave it vague and it becomes Thursday anyway, but you will have walked there twice.'),
 ]},
{
 'id': 'xalteva-06', 'district': 'xalteva', 'tier': 3,
 'who': u'El niño de la bici', 'title': u'El mandado',
 'goal': u'Send a kid on an errand and get the change back',
 'culture': u'Sending a chavalo to the pulpería is completely normal and he '
            u'expects a few córdobas for going. This is also the first person '
            u'in Granada you address as VOS instead of usted: a child, and '
            u'later a friend. Getting that switch right is most of sounding '
            u'Nicaraguan.',
 'beats': [
  beat(u'¿Le hago mandado, señor? Ando en la bici.',
       u'Ask him to run an errand', u'me hace un mandado',
       u'¿Me hace un mandado?', u'Would you run an errand for me?',
       [u'¿me hace un mandado?'],
       [u'aquí está', u'gracias', u'para vos', u'me trae el vuelto'],
       [u'me hace un mandado'],
       [u'me hace un mandado'],
       u'Un mandado is an errand and the whole arrangement is in the word. He will already know which pulpería.'),
  beat(u'Sí pues. ¿Qué le traigo?',
       u'Hand him the money', u'aquí está',
       u'Aquí está. Cien pesos.', u'Here you go. A hundred córdobas.',
       [u'aquí está', u'cien pesos'],
       [u'para vos', u'gracias', u'me trae el vuelto', u'está bien'],
       [u'aqui esta cien pesos', u'aqui esta'],
       [u'aquí está'],
       u'Aquí está hands something over. Pesos in the street, córdobas on the note, and everybody says pesos.'),
  beat(u'Va. Ya vengo.',
       u'Ask for the change back', u'me trae el vuelto',
       u'Y me trae el vuelto.', u'And bring me the change.',
       [u'y', u'me trae el vuelto'],
       [u'para vos', u'aquí está', u'gracias', u'está bien'],
       [u'y me trae el vuelto', u'me trae el vuelto'],
       [u'me trae el vuelto'],
       u'El vuelto is the change. Say it lightly and it is not an accusation — it is the arrangement, and it is why he gets tipped rather than skimming.'),
  beat(u'Aquí está todo, señor. Conté bien.',
       u'Give him something for going', u'para vos',
       u'Diez para vos.', u'Ten for you.',
       [u'diez', u'para vos'],
       [u'para usted', u'gracias', u'el vuelto', u'está bien'],
       [u'diez para vos', u'para vos'],
       [u'para vos'],
       u'Para VOS, not para usted. He is a child, so he gets vos — and this is the first time in the whole game you use it. Getting that switch right matters more than any verb ending you will study.'),
 ]},
{
 'id': 'xalteva-07', 'district': 'xalteva', 'tier': 4,
 'who': u'La maestra', 'title': u'La escuela',
 'goal': u'Be asked to say hello to a class in English',
 'culture': u'A foreigner walking past a school is a free English lesson and '
            u'she will ask. Saying yes costs five minutes and buys you the '
            u'whole street; saying no is fine too, but say it as a no to '
            u'today rather than a no to her.',
 'beats': [
  beat(u'¡Joven! Disculpe. ¿Usted habla inglés? ¿Es maestro?',
       u'You are not a teacher', u'no soy maestro',
       u'No soy maestro, pero sí hablo inglés.', u'I’m not a teacher, but I do speak English.',
       [u'no soy maestro', u'pero sí hablo inglés'],
       [u'con mucho gusto', u'una vez nada más', u'gracias', u'con permiso'],
       [u'no soy maestro pero si hablo ingles', u'no soy maestro'],
       [u'no soy maestro'],
       u'Correct the assumption and answer the real question in the same breath. She is not asking for your credentials.'),
  beat(u'¿Y no me les habla tantito a los chavalos? Cinco minutos.',
       u'Say yes, gladly', u'con mucho gusto',
       u'Con mucho gusto.', u'Gladly.',
       [u'con mucho gusto'],
       [u'no puedo', u'una vez nada más', u'gracias', u'con permiso'],
       [u'con mucho gusto'],
       [u'con mucho gusto'],
       u'Con mucho gusto is a warm yes and it is used constantly here — for favours, for introductions, for handing somebody the salt.'),
  beat(u'¡Ay, gracias! Pase, pase.',
       u'Ask what to say to them', u'¿qué les digo?',
       u'¿Y qué les digo?', u'And what should I say to them?',
       [u'¿y qué', u'les digo?'],
       [u'con mucho gusto', u'gracias', u'una vez nada más', u'con permiso'],
       [u'y que les digo', u'que les digo'],
       [u'¿qué les digo?'],
       u'Ask before you are in front of thirty children. She has a plan and she will tell you in four words.'),
  beat(u'Cualquier cosa. Salúdelos y que le oigan el acento.',
       u'Agree — but just the once', u'una vez nada más',
       u'Está bien. Una vez nada más.', u'Alright. Just this once.',
       [u'está bien', u'una vez nada más'],
       [u'con mucho gusto', u'gracias', u'otro día', u'con permiso'],
       [u'esta bien una vez nada mas', u'una vez nada mas'],
       [u'una vez nada más'],
       u'Una vez nada más sets the limit while still saying yes. Without it you are the English teacher of Xalteva by Friday.'),
 ]},
{
 'id': 'xalteva-08', 'district': 'xalteva', 'tier': 4,
 'who': u'El del cementerio', 'title': u'El cementerio',
 'goal': u'Walk a cemetery with the man who looks after it',
 'culture': u'The municipal cemetery is full of marble brought from Italy by '
            u'families that no longer exist, and one man cuts the grass round '
            u'all of it. He is proud of it and almost nobody asks him about '
            u'it. This is a mission with nothing to buy and nothing to win.',
 'beats': [
  beat(u'Buenas. ¿Busca a alguien?',
       u'No — ask how long he has worked here', u'toda mi vida',
       u'No. ¿Usted trabaja aquí?', u'No. Do you work here?',
       [u'no', u'¿usted trabaja aquí?'],
       [u'toda mi vida', u'gracias', u'no ando', u'ya va'],
       [u'no usted trabaja aqui', u'usted trabaja aqui'],
       [u'toda mi vida'],
       u'Ask the man his work and you get his life. He has been waiting years for somebody to ask.'),
  beat(u'Toda mi vida, joven. Desde chavalo con mi papá.',
       u'His whole life — say it back', u'aquí están',
       u'¿Y aquí están todos?', u'And they’re all here?',
       [u'¿y aquí están', u'todos?'],
       [u'toda mi vida', u'los cuido', u'gracias', u'nadie viene'],
       [u'y aqui estan todos', u'aqui estan todos', u'aqui estan'],
       [u'aquí están'],
       u'Toda mi vida from him, aquí están from you: he is talking about the families, and the right thing to do is keep him talking.'),
  beat(u'Todititos. Los grandes de Granada están aquí, mire ese mármol.',
       u'Ask whether he looks after them all', u'los cuido',
       u'¿Y usted los cuida?', u'And you look after them?',
       [u'¿y usted', u'los cuida?'],
       [u'los cuido', u'nadie viene', u'gracias', u'ya va'],
       [u'y usted los cuida', u'usted los cuida'],
       [u'los cuido'],
       u'Los cuido is what he will answer, and it is the sentence the whole mission is for. Cuidar is minding, watching, tending — the cuidacarros does it to a moto and he does it to the dead.'),
  beat(u'Yo los cuido. Corto el monte, limpio. Pero ya nadie viene.',
       u'Nobody comes — say something true', u'nadie viene',
       u'¿Nadie viene? Qué lástima.', u'Nobody comes? That’s a shame.',
       [u'¿nadie viene?', u'qué lástima'],
       [u'los cuido', u'gracias', u'otro día', u'toda mi vida'],
       [u'nadie viene que lastima', u'nadie viene'],
       [u'nadie viene'],
       u'Qué lástima is the right size of answer. Anything bigger would be about you, and this is not about you.'),
 ]},
{
 'id': 'xalteva-09', 'district': 'xalteva', 'tier': 5,
 'who': u'Doña Rosa', 'title': u'La rezadora',
 'goal': u'Be invited to a novena and know what is expected',
 'culture': u'A novena is nine nights of prayer for somebody who died, and '
            u'the rezadora leads it. Going is a kindness to the family and '
            u'nobody will test your faith at the door. Do not turn up with '
            u'flowers or wine — there is coffee and bread and that is the '
            u'form.',
 'beats': [
  beat(u'Buenas noches. ¿Usted es el vecino nuevo? Estamos rezando aquí al lado.',
       u'Ask how many nights', u'nueve noches',
       u'¿Son nueve noches?', u'Is it nine nights?',
       [u'¿son nueve noches?'],
       [u'a las siete', u'gracias', u'no hace falta', u'otro día'],
       [u'son nueve noches', u'nueve noches'],
       [u'nueve noches'],
       u'Nine nights, one for each, ending on the ninth with the biggest one. Knowing that is knowing what you are being invited to.'),
  beat(u'Nueve, sí. Desde que se nos fue don Ramón.',
       u'Ask what time', u'a las siete',
       u'¿Y a qué hora? ¿A las siete?', u'And what time? Seven?',
       [u'¿y a qué hora?', u'¿a las siete?'],
       [u'nueve noches', u'gracias', u'no hace falta', u'otro día'],
       [u'y a que hora a las siete', u'a que hora a las siete', u'a las siete'],
       [u'a las siete'],
       u'Seven, after work and before the heat drops. It will start at ten past and nobody minds.'),
  beat(u'A las siete. Y véngase, aunque sea un ratito.',
       u'Ask whether to bring anything', u'no hace falta',
       u'¿Llevo algo?', u'Should I bring something?',
       [u'¿llevo algo?'],
       [u'no hace falta', u'con eso basta', u'gracias', u'a las siete'],
       [u'llevo algo'],
       [u'no hace falta'],
       u'Ask, and the answer will be no hace falta — there is no need. Ask anyway: not asking is what would be rude.'),
  beat(u'No hace falta nada, mi hijo. Con que venga, con eso basta.',
       u'Accept it as given', u'con eso basta',
       u'Con eso basta. Ahí llego.', u'That’s enough, then. I’ll be there.',
       [u'con eso basta', u'ahí llego'],
       [u'no hace falta', u'otro día', u'gracias', u'a las siete'],
       [u'con eso basta ahi llego', u'con eso basta', u'ahi llego'],
       [u'con eso basta'],
       u'Con eso basta — that is enough. Turning up IS the gift, and ahí llego is a promise you should keep.'),
 ]},
{
 'id': 'xalteva-10', 'district': 'xalteva', 'tier': 5,
 'who': u'El historiador', 'title': u'Las murallas',
 'goal': u'Hear why this quarter is called Xalteva',
 'culture': u'Xalteva was the indigenous town, and the Spanish built their '
            u'city beside it rather than on it. The low walls along the '
            u'street are what is left of the boundary between the two, and '
            u'people walk past them every day without knowing that is what '
            u'they are.',
 'beats': [
  beat(u'¿Ve esa pared baja? Eso no es de ahora, joven.',
       u'Ask who was here before', u'los indios',
       u'¿Aquí vivían los indios?', u'Did the indigenous people live here?',
       [u'¿aquí vivían', u'los indios?'],
       [u'la muralla', u'antes de', u'gracias', u'lo que queda'],
       [u'aqui vivian los indios', u'vivian los indios'],
       [u'los indios'],
       u'Los indios is the ordinary word here and carries no sting in this sentence. He will use it himself and so does the history he is about to give you.'),
  beat(u'Aquí era el pueblo de ellos. Xalteva se llamaba, antes de que llegaran los españoles.',
       u'Before the Spanish, then', u'antes de',
       u'¿Antes de los españoles?', u'Before the Spanish?',
       [u'¿antes de', u'los españoles?'],
       [u'los indios', u'la muralla', u'gracias', u'lo que queda'],
       [u'antes de los espanoles', u'antes de'],
       [u'antes de'],
       u'Antes de puts a date on something without needing one, which is how this history is told: before the Spanish, before the earthquake, before the war.'),
  beat(u'Antes. Y los españoles levantaron su ciudad al lado, y una muralla en medio.',
       u'Ask about the wall', u'la muralla',
       u'¿Y esta es la muralla?', u'And this is the wall?',
       [u'¿y esta es', u'la muralla?'],
       [u'antes de', u'los indios', u'gracias', u'lo que queda'],
       [u'y esta es la muralla', u'esta es la muralla'],
       [u'la muralla'],
       u'La muralla divided the two towns. What is standing is a fraction of it and nobody has signposted a metre of it.'),
  beat(u'Un pedazo. Es lo que queda, joven. Lo demás se lo llevaron para hacer casas.',
       u'That is what is left', u'lo que queda',
       u'Lo que queda. Gracias por contarme.', u'What’s left. Thank you for telling me.',
       [u'lo que queda', u'gracias por contarme'],
       [u'la muralla', u'antes de', u'otro día', u'por favor'],
       [u'lo que queda gracias por contarme', u'lo que queda'],
       [u'lo que queda'],
       u'Lo que queda — what is left. Thanking him for the telling rather than for the wall is the difference between a tourist and a neighbour.'),
 ]},
# ── Guadalupe ───────────────────────────────────────────────────────────
{
 'id': 'guadalupe-01', 'district': 'guadalupe', 'tier': 1,
 'who': u'El pulpero', 'title': u'La pulpería',
 'goal': u'Buy the small things at the shop on the corner',
 'culture': u'A pulpería is a front room with a grille, and it sells one of '
            u'everything: soap, eggs, a single cigarette, rice by the pound. '
            u'You do not go in — you stand at the window and say me da.',
 'beats': [
  beat(u'Buenas. ¿Qué va a llevar?',
       u'Ask for a bar of soap', u'me da',
       u'Me da un jabón.', u'Give me a bar of soap.',
       [u'me da', u'un jabón'],
       [u'y una gaseosa', u'nada más', u'por favor', u'quiero'],
       [u'me da un jabon', u'me da un jabon por favor'],
       [u'me da', u'un jabón'],
       u'Me da is how you ask for things across a counter — softer than quiero and shorter than everything else. It is the single most useful phrase in this district.'),
  beat(u'¿Cuál? ¿De bañarse o de lavar?',
       u'Add a fizzy drink', u'y una gaseosa',
       u'De bañarse. Y una gaseosa.', u'For washing myself. And a fizzy drink.',
       [u'de bañarse', u'y una gaseosa'],
       [u'de lavar', u'nada más', u'gracias', u'me da'],
       [u'de banarse y una gaseosa', u'y una gaseosa'],
       [u'y una gaseosa'],
       u'Two kinds of soap and he will always ask which. Gaseosa is any fizzy drink; if you want a Coca-Cola you say Coca and he will not be surprised.'),
  beat(u'¿Fría o del tiempo?',
       u'Cold, and that is all', u'nada más',
       u'Fría. Nada más, gracias.', u'Cold. That’s all, thanks.',
       [u'fría', u'nada más', u'gracias'],
       [u'del tiempo', u'y una gaseosa', u'me da', u'por favor'],
       [u'fria nada mas gracias', u'nada mas gracias', u'nada mas'],
       [u'nada más'],
       u'Nada más closes the order. Del tiempo means room temperature and is what you get if you do not say fría.'),
 ]},
{
 'id': 'guadalupe-02', 'district': 'guadalupe', 'tier': 2,
 'who': u'El de las motos', 'title': u'El taller de motos',
 'goal': u'Describe a noise without knowing the word for it',
 'culture': u'The workshop is half the pavement and he will look at it now, '
            u'not on Tuesday. You do not need the vocabulary for the part — '
            u'you need where it is and when it happens, and he does the rest.',
 'beats': [
  beat(u'Buenas. ¿Qué le pasa a la moto?',
       u'It is making a noise', u'hace un ruido',
       u'Buenas. Hace un ruido.', u'Hello. It’s making a noise.',
       [u'Buenas', u'hace un ruido'],
       [u'aquí atrás', u'cuando freno', u'gracias', u'por favor'],
       [u'buenas hace un ruido', u'hace un ruido'],
       [u'hace un ruido'],
       u'Hace un ruido is enough to start with. You do not need the word for the part and you are not expected to have it.'),
  beat(u'¿Un ruido de qué tipo? ¿Dónde?',
       u'Point — back here', u'aquí atrás',
       u'Aquí atrás.', u'Back here.',
       [u'aquí atrás'],
       [u'aquí adelante', u'cuando freno', u'gracias', u'por favor'],
       [u'aqui atras'],
       [u'aquí atrás'],
       u'Where it comes from is worth more than what it sounds like. Put your hand on the place and say aquí atrás.'),
  beat(u'¿Y suena siempre, o cuándo?',
       u'When you brake', u'cuando freno',
       u'Cuando freno.', u'When I brake.',
       [u'cuando freno'],
       [u'cuando acelero', u'aquí atrás', u'gracias', u'por favor'],
       [u'cuando freno'],
       [u'cuando freno'],
       u'When it happens is the diagnosis. Cuando freno and aquí atrás together have already told him what it is.'),
  beat(u'Ah, son las balatas. Se las cambio ahorita.',
       u'Ask if it is serious', u'¿es grave?',
       u'¿Es grave?', u'Is it serious?',
       [u'¿es grave?'],
       [u'gracias', u'cuando freno', u'por favor', u'aquí atrás'],
       [u'es grave'],
       [u'¿es grave?'],
       u'¿Es grave? works for a moto, a tooth and a relative. Ask it and you get a straight answer, because he wants the work either way and there is plenty of it.'),
 ]},
{
 'id': 'guadalupe-03', 'district': 'guadalupe', 'tier': 2,
 'who': u'Los chavalos', 'title': u'La mejenga',
 'goal': u'Get picked for a game on the corner pitch',
 'culture': u'A mejenga is a pick-up game and anybody can ask. These are the '
            u'other people you address as VOS — kids, and now teammates. '
            u'Pasámela is the vos imperative; pásamela with the accent early '
            u'is Mexican television, and they will hear it.',
 'beats': [
  beat(u'¡Ey! ¿Juega o solo mira?',
       u'Ask to join', u'¿puedo jugar?',
       u'¿Puedo jugar?', u'Can I play?',
       [u'¿puedo jugar?'],
       [u'de este lado', u'buena esa', u'gracias', u'está bien'],
       [u'puedo jugar'],
       [u'¿puedo jugar?'],
       u'Just ask. Nobody is picking teams by ability and there is always room for one more.'),
  beat(u'Dale pues. ¿De qué lado se pone?',
       u'This side', u'de este lado',
       u'De este lado.', u'On this side.',
       [u'de este lado'],
       [u'de aquel lado', u'¿puedo jugar?', u'gracias', u'está bien'],
       [u'de este lado'],
       [u'de este lado'],
       u'Dale is yes, go on, alright, get on with it. You will hear it forty times an hour in this district.'),
  beat(u'¡Va! Estás con nosotros.',
       u'Call for the ball', u'pasámela',
       u'¡Pasámela!', u'Pass it to me!',
       [u'¡pasámela!'],
       [u'de este lado', u'buena esa', u'está bien', u'aquí'],
       [u'pasamela'],
       [u'pasámela'],
       u'Pasámela, with the stress on the MA — that is the vos imperative and it is what they say. Pásamela, stressed early, is Mexican television and they will hear it instantly.'),
  beat(u'¡Ahí va! ¡Ahí va!',
       u'Somebody scores — say so', u'buena esa',
       u'¡Buena esa!', u'Nice one!',
       [u'¡buena esa!'],
       [u'pasámela', u'de este lado', u'gracias', u'está bien'],
       [u'buena esa'],
       [u'buena esa'],
       u'Buena esa is what you shout when somebody does something good, on a pitch or anywhere else. Two words, and it makes you one of them for the afternoon.'),
 ]},
{
 'id': 'guadalupe-04', 'district': 'guadalupe', 'tier': 3,
 'who': u'La vecina', 'title': u'El cumpleaños',
 'goal': u'Be invited to a birthday and turn up with the right thing',
 'culture': u'The invitation is real, not a formality, and not turning up is '
            u'noticed. Ask what to bring and you will be told nothing, so '
            u'bring a bottle of something fizzy for the table, which is what '
            u'everybody else does while saying they brought nothing.',
 'beats': [
  beat(u'Vecino, buenas. Fíjese que la niña cumple años el sábado.',
       u'Ask whose birthday and say congratulations', u'cumple años',
       u'¿Cumple años? ¡Felicidades!', u'It’s her birthday? Congratulations!',
       [u'¿cumple años?', u'¡felicidades!'],
       [u'¿a qué hora?', u'¿llevo algo?', u'gracias', u'así es'],
       [u'cumple anos felicidades', u'cumple anos', u'felicidades'],
       [u'cumple años', u'felicidades'],
       u'Cumplir años is to complete years, which is a better way of putting it. Felicidades goes to the family as much as to the child.'),
  beat(u'Gracias, vecino. Ahí lo esperamos, pues.',
       u'Ask what time', u'¿a qué hora?',
       u'¿A qué hora?', u'What time?',
       [u'¿a qué hora?'],
       [u'¿llevo algo?', u'gracias', u'así es', u'con permiso'],
       [u'a que hora'],
       [u'¿a qué hora?'],
       u'Ask, and take the answer as the earliest possible moment rather than the time. Nobody arrives at three.'),
  beat(u'Como a las tres. Pero llegue cuando pueda.',
       u'Ask whether to bring something', u'¿llevo algo?',
       u'¿Llevo algo?', u'Should I bring anything?',
       [u'¿llevo algo?'],
       [u'¿a qué hora?', u'gracias', u'con permiso', u'ni modo'],
       [u'llevo algo'],
       [u'¿llevo algo?'],
       u'You will be told no. Ask anyway — asking is the courtesy, and then bring a big bottle of gaseosa for the table like everybody else.'),
  beat(u'Nada, vecino. Usted venga nomás.',
       u'Accept, and confirm you will be there', u'así es',
       u'Está bien. Ahí llego, vecina.', u'Alright. I’ll be there, vecina.',
       [u'está bien', u'ahí llego', u'vecina'],
       [u'ni modo', u'otro día', u'gracias', u'con permiso'],
       [u'esta bien ahi llego vecina', u'ahi llego vecina', u'ahi llego'],
       [u'así es'],
       u'Vecino and vecina are what neighbours call each other instead of names, sometimes for years. Ahí llego means you are going, so go.'),
 ]},
{
 'id': 'guadalupe-05', 'district': 'guadalupe', 'tier': 3,
 'who': u'El carpintero', 'title': u'La mesa',
 'goal': u'Order a table and describe the size with your hands',
 'culture': u'He will build it from what he has and he will not write '
            u'anything down. Hands are an accepted unit of measurement here '
            u'and sin prisa is a real instruction — say it and mean it, '
            u'because saying it and then chasing him is worse than not '
            u'saying it.',
 'beats': [
  beat(u'Buenas. ¿En qué le sirvo?',
       u'You want a table made', u'¿me la hace?',
       u'Quiero una mesa. ¿Me la hace?', u'I want a table. Could you make me one?',
       [u'quiero una mesa', u'¿me la hace?'],
       [u'así de grande', u'de madera', u'gracias', u'sin prisa'],
       [u'quiero una mesa me la hace', u'me la hace'],
       [u'¿me la hace?'],
       u'¿Me la hace? asks him to make you one. There is no catalogue and no price list, and that is not a problem to be solved.'),
  beat(u'¿De qué tamaño la quiere?',
       u'Show him with your hands', u'así de grande',
       u'Así de grande.', u'About this big.',
       [u'así de grande'],
       [u'de madera', u'sin prisa', u'gracias', u'por favor'],
       [u'asi de grande'],
       [u'así de grande'],
       u'Hands are a unit here and he would rather have them than a number. Así de grande with your arms out is a specification.'),
  beat(u'¿Y de qué material? Tengo pino y tengo cedro.',
       u'Wood — the cedar', u'de madera',
       u'De madera. De cedro.', u'Wood. Cedar.',
       [u'de madera', u'de cedro'],
       [u'de pino', u'así de grande', u'gracias', u'sin prisa'],
       [u'de madera de cedro', u'de madera', u'de cedro'],
       [u'de madera'],
       u'Cedro is the good one and he asked because it costs more. Saying which is how you avoid finding out in a fortnight.'),
  beat(u'Va pues. Démela en quince días, ¿le corre prisa?',
       u'No rush — and mean it', u'sin prisa',
       u'Sin prisa. Cuando pueda.', u'No hurry. Whenever you can.',
       [u'sin prisa', u'cuando pueda'],
       [u'para mañana', u'gracias', u'de madera', u'por favor'],
       [u'sin prisa cuando pueda', u'sin prisa'],
       [u'sin prisa'],
       u'Sin prisa is a real instruction and he will take it at face value. Say it and then chase him and you have taught him you did not mean it.'),
 ]},
{
 'id': 'guadalupe-06', 'district': 'guadalupe', 'tier': 3,
 'who': u'La señora del perro', 'title': u'El perro',
 'goal': u'Deal with a dog that has decided your gate is its gate',
 'culture': u'Street dogs here belong to the street rather than to nobody, '
            u'and several houses feed the same one. Asking whose it is gets '
            u'you a shrug: it is aquí anda — it is around. It is also almost '
            u'certainly harmless.',
 'beats': [
  beat(u'¿Le está molestando ese perro?',
       u'Ask whether it is hers', u'ese perro',
       u'¿Ese perro es suyo?', u'Is that dog yours?',
       [u'¿ese perro', u'es suyo?'],
       [u'no es mío', u'aquí anda', u'gracias', u'no muerde'],
       [u'ese perro es suyo', u'ese perro'],
       [u'ese perro'],
       u'Ese perro, said with a nod at it. Whose it is turns out to be a harder question than you expect.'),
  beat(u'No, no es mío. De nadie es.',
       u'So whose is it?', u'no es mío',
       u'¿No es suyo? ¿Y de quién es?', u'Not yours? Then whose is it?',
       [u'¿no es suyo?', u'¿y de quién es?'],
       [u'aquí anda', u'no muerde', u'gracias', u'ese perro'],
       [u'no es suyo y de quien es', u'y de quien es', u'no es suyo'],
       [u'no es mío'],
       u'No es mío from her, no es suyo from you. The dog is fed by four houses and belongs to none of them, which is a normal arrangement.'),
  beat(u'De nadie, pues. Aquí anda desde chiquito.',
       u'It is just around, then', u'aquí anda',
       u'Aquí anda nomás.', u'It just hangs around here.',
       [u'aquí anda', u'nomás'],
       [u'no es mío', u'no muerde', u'gracias', u'ese perro'],
       [u'aqui anda nomas', u'aqui anda'],
       [u'aquí anda'],
       u'Aquí anda — it is around. Andar is doing a great deal of work in this country and almost none of it is walking.'),
  beat(u'No le haga caso. No muerde ese, es bien manso.',
       u'Check that — it does not bite?', u'no muerde',
       u'¿No muerde?', u'It doesn’t bite?',
       [u'¿no muerde?'],
       [u'aquí anda', u'gracias', u'otro día', u'no es mío'],
       [u'no muerde'],
       [u'no muerde'],
       u'No muerde is the reassurance you will be given about every dog in Nicaragua, and it is nearly always true.'),
 ]},
{
 'id': 'guadalupe-07', 'district': 'guadalupe', 'tier': 4,
 'who': u'El evangélico', 'title': u'El culto',
 'goal': u'Decline an invitation to church without giving offence',
 'culture': u'He is inviting you because he thinks it would be good for you, '
            u'which is a kindness by his lights. Thank him for the invitation '
            u'rather than arguing with the premise, and you will keep a '
            u'neighbour who genuinely knows the barrio.',
 'beats': [
  beat(u'Hermano, buenas. Lo invito al culto el domingo. Es aquí cerquita.',
       u'Thank him for the invitation', u'le agradezco',
       u'Le agradezco, hermano.', u'I appreciate it, brother.',
       [u'le agradezco', u'hermano'],
       [u'no soy de esa', u'quizás otro día', u'gracias', u'respeto'],
       [u'le agradezco hermano', u'le agradezco'],
       [u'le agradezco'],
       u'Le agradezco thanks him for the thought before you answer it. It buys the rest of the conversation a friendly tone.'),
  beat(u'¿Y viene, pues? Cantamos, hay predicación.',
       u'Say it is not your church', u'no soy de esa',
       u'No soy de esa iglesia.', u'I’m not of that church.',
       [u'no soy de esa', u'iglesia'],
       [u'respeto', u'quizás otro día', u'gracias', u'le agradezco'],
       [u'no soy de esa iglesia', u'no soy de esa'],
       [u'no soy de esa'],
       u'A fact about you rather than a judgement about him. Arguing the theology is the one move that turns a neighbour into a project.'),
  beat(u'Ah. ¿Y usted es católico?',
       u'Say you respect it either way', u'respeto',
       u'Lo respeto igual.', u'I respect it all the same.',
       [u'lo respeto', u'igual'],
       [u'no soy de esa', u'quizás otro día', u'gracias', u'hermano'],
       [u'lo respeto igual', u'lo respeto'],
       [u'respeto'],
       u'Respect without joining. It is the same move as with the beata in Xalteva, and it works for the same reason.'),
  beat(u'Bueno, hermano. Ahí queda la invitación.',
       u'Leave the door open', u'quizás otro día',
       u'Quizás otro día. Gracias.', u'Maybe another day. Thank you.',
       [u'quizás otro día', u'gracias'],
       [u'nunca', u'le agradezco', u'respeto', u'hermano'],
       [u'quizas otro dia gracias', u'quizas otro dia'],
       [u'quizás otro día'],
       u'Quizás otro día is a no that leaves everybody their dignity. He will ask again in a month and that is fine.'),
 ]},
{
 'id': 'guadalupe-08', 'district': 'guadalupe', 'tier': 4,
 'who': u'Doña Chepa', 'title': u'El chisme',
 'goal': u'Hear gossip and pass it on without getting it wrong',
 'culture': u'Chisme is how a barrio keeps track of itself and being told any '
            u'is a sign you are inside it. The grammar of it matters: dicen '
            u'que and fíjese que mark what you heard rather than what you '
            u'know, and using them is the difference between passing on news '
            u'and starting a rumour.',
 'beats': [
  beat(u'Vecino, ¿supo lo de la casa de la esquina?',
       u'No — ask what they are saying', u'dicen que',
       u'No. ¿Qué dicen?', u'No. What are they saying?',
       [u'no', u'¿qué dicen?'],
       [u'dicen que', u'fíjese que', u'¿de verdad?', u'no sea así'],
       [u'no que dicen', u'que dicen'],
       [u'dicen que'],
       u'Dicen que — they say that. The whole of this mission is learning to mark where a thing came from.'),
  beat(u'Fíjese que la vendieron. Y dicen que fue a un extranjero.',
       u'Show you are listening', u'fíjese que',
       u'¿Fíjese? ¿De verdad?', u'Really? Truly?',
       [u'¿fíjese?', u'¿de verdad?'],
       [u'dicen que', u'no sea así', u'gracias', u'está bien'],
       [u'fijese de verdad', u'de verdad'],
       [u'fíjese que', u'¿de verdad?'],
       u'Fíjese que opens a piece of news and is one of the most Nicaraguan phrases there is. Note the accent: fíjese is usted. To a friend it is fijate, with no accent at all.'),
  beat(u'De verdad. Y la doña se fue sin decirle a nadie, imagínese.',
       u'Do not join in the unkind part', u'no sea así',
       u'Ay, no sea así, doña.', u'Oh, don’t be like that, doña.',
       [u'ay', u'no sea así', u'doña'],
       [u'dicen que', u'¿de verdad?', u'gracias', u'fíjese que'],
       [u'ay no sea asi dona', u'no sea asi dona', u'no sea asi'],
       [u'no sea así'],
       u'No sea así is a smiling reproach — do not be like that. It lets you decline the cruel half of the gossip without declining the gossip.'),
  beat(u'Ay, vecino, usted es muy bueno. Pero es la verdad, pues.',
       u'Pass it on carefully — mark it as hearsay', u'dicen que',
       u'Bueno. Dicen que la vendieron.', u'Well. They say it was sold.',
       [u'bueno', u'dicen que', u'la vendieron'],
       [u'fíjese que', u'¿de verdad?', u'gracias', u'no sea así'],
       [u'bueno dicen que la vendieron', u'dicen que la vendieron'],
       [u'dicen que'],
       u'Dicen que in front of it is what keeps you out of trouble. Drop those two words and the story becomes yours, and so does the row when it turns out to be wrong.'),
 ]},
{
 'id': 'guadalupe-09', 'district': 'guadalupe', 'tier': 5,
 'who': u'El vecino bravo', 'title': u'El pleito',
 'goal': u'Get between two neighbours arguing over a wall',
 'culture': u'A shouting match on the street is public and everybody watches, '
            u'which is also what settles it: nobody wants to be the one who '
            u'would not calm down. A third person saying no es para tanto is '
            u'a recognised role, and it is not interfering.',
 'beats': [
  beat(u'¡Esa pared es mía! ¡Yo la levanté con mi plata!',
       u'Calm him down', u'cálmese',
       u'Cálmese, vecino.', u'Calm down, neighbour.',
       [u'cálmese', u'vecino'],
       [u'no es para tanto', u'ya estuvo', u'Buenas', u'otro día'],
       [u'calmese vecino', u'calmese'],
       [u'cálmese'],
       u'Cálmese, usted, and with vecino after it. The word alone can sound like an order; with vecino it is somebody on his side.'),
  beat(u'¡Es que me corrió la cerca! ¡Medio metro me quitó!',
       u'Say it is not that big a thing', u'no es para tanto',
       u'No es para tanto, hombre.', u'It’s not such a big deal, man.',
       [u'no es para tanto', u'hombre'],
       [u'cálmese', u'ya estuvo', u'gracias', u'otro día'],
       [u'no es para tanto hombre', u'no es para tanto'],
       [u'no es para tanto'],
       u'No es para tanto shrinks it, and shrinking it is the entire job. You are not judging who is right and nobody has asked you to.'),
  beat(u'¡Es que usted no sabe! ¡Toda la vida hemos vivido aquí!',
       u'Say it can be talked out', u'hablando se arregla',
       u'Hablando se arregla, vecino.', u'It can be sorted out by talking, neighbour.',
       [u'hablando se arregla', u'vecino'],
       [u'no es para tanto', u'cálmese', u'gracias', u'ya estuvo'],
       [u'hablando se arregla vecino', u'hablando se arregla'],
       [u'hablando se arregla'],
       u'Hablando se arregla — talking sorts it out. It is a proverb and it works because it hands both of them a way to stop without losing.'),
  beat(u'...Bueno. Bueno pues. Que venga y hablamos.',
       u'Close it off', u'ya estuvo',
       u'Ya estuvo, pues.', u'That’s that, then.',
       [u'ya estuvo', u'pues'],
       [u'cálmese', u'no es para tanto', u'gracias', u'otro día'],
       [u'ya estuvo pues', u'ya estuvo'],
       [u'ya estuvo'],
       u'Ya estuvo ends it: that is enough, it is over, done. Said at the right moment it lets everybody walk away having agreed to stop rather than having given in.'),
 ]},
{
 'id': 'guadalupe-10', 'district': 'guadalupe', 'tier': 5,
 'who': u'La partera', 'title': u'La partera',
 'goal': u'Talk to a midwife who has delivered half the street',
 'culture': u'The parteras delivered most people over forty in this barrio, '
            u'at home, without a doctor, and they are respected accordingly. '
            u'She is not a folk curiosity and this is not a mission about '
            u'quaintness — she did a hard job well for fifty years and she '
            u'is the right person to ask about it.',
 'beats': [
  beat(u'Siéntese, mi hijo. ¿Usted es el que anda preguntando por el barrio?',
       u'Ask how long she has been doing it', u'¿cuántos años?',
       u'Sí. ¿Cuántos años tiene de partera?', u'Yes. How many years have you been a midwife?',
       [u'sí', u'¿cuántos años', u'tiene de partera?'],
       [u'aquí nacieron', u'sin doctor', u'gracias', u'está bien'],
       [u'si cuantos anos tiene de partera', u'cuantos anos tiene de partera',
        u'cuantos anos'],
       [u'¿cuántos años?'],
       u'¿Cuántos años? asks the number and gets you the life. It is the same question you ask about a house, a job or a marriage here.'),
  beat(u'Cincuenta y dos años, mi hijo. Desde los diecinueve.',
       u'Ask about the children of this street', u'aquí nacieron',
       u'¿Y aquí nacieron todos?', u'And they were all born here?',
       [u'¿y aquí nacieron', u'todos?'],
       [u'sin doctor', u'gracias', u'está bien', u'por favor'],
       [u'y aqui nacieron todos', u'aqui nacieron todos', u'aqui nacieron'],
       [u'aquí nacieron'],
       u'Aquí nacieron — they were born here, in these rooms, on this street. Half the people you have met in this district came through her hands.'),
  beat(u'Aquí mismo. En sus casas, en su cama.',
       u'Without a doctor?', u'sin doctor',
       u'¿Sin doctor?', u'Without a doctor?',
       [u'¿sin doctor?'],
       [u'aquí nacieron', u'gracias', u'está bien', u'por favor'],
       [u'sin doctor'],
       [u'sin doctor'],
       u'Ask it plainly. It is not a challenge and she will not take it as one — the hospital was far and there was petrol money to find.'),
  beat(u'Sin doctor. Y nunca se me murió ninguno, gracias a Dios. Ninguno.',
       u'Say something equal to that', u'nunca se me murió',
       u'Nunca se le murió ninguno. Qué grande.', u'You never lost one. That’s something.',
       [u'nunca se le murió ninguno', u'qué grande'],
       [u'sin doctor', u'gracias', u'está bien', u'aquí nacieron'],
       [u'nunca se le murio ninguno que grande', u'nunca se le murio ninguno'],
       [u'nunca se me murió'],
       u'Nunca se me murió from her, nunca se le murió from you — the same fact, and the little pronoun carries the whole weight of it. Qué grande is admiration, not size.'),
 ]},
]

HINTS = [
 # Xalteva
 {'kind': u'doña en la puerta', 'district': 'xalteva',
  'says': u'¿Anda buscando algo? Pregúntele a la doña de la esquina, ella sabe dónde queda todo.',
  'en': u'Looking for something? Ask the lady on the corner, she knows where everything is.',
  'points_at': ['xalteva-01']},
 {'kind': u'chavalo en bici', 'district': 'xalteva',
  'says': u'La iglesia la abren a las cinco, para la misa. Antes está cerrada.',
  'en': u'They open the church at five, for mass. Before that it is shut.',
  'points_at': ['xalteva-02']},
 {'kind': u'viejo de la esquina', 'district': 'xalteva',
  'says': u'A la doña Rosa no le diga que no cree. Ella pregunta, pero no juzga.',
  'en': u'Do not tell doña Rosa you are not a believer. She asks, but she does not judge.',
  'points_at': ['xalteva-03', 'xalteva-09']},
 {'kind': u'obrero', 'district': 'xalteva',
  'says': u'Don Chombo está en la esquina desde las seis. Si tiene tiempo, siéntese con él.',
  'en': u'Don Chombo has been on the corner since six. If you have time, sit with him.',
  'points_at': ['xalteva-04']},
 {'kind': u'vendedora', 'district': 'xalteva',
  'says': u'¿Le queda largo el pantalón? La costurera está a media cuadra, cobra poquito.',
  'en': u'Are your trousers too long? The seamstress is half a block away, she charges very little.',
  'points_at': ['xalteva-05']},
 {'kind': u'doña en la puerta', 'district': 'xalteva',
  # Not "Mande al chavalo": the dialect gate bans `mande` because Mexico says
  # it for "pardon?", and it cannot tell that apart from the usted imperative
  # of mandar. Rewording is better than widening the gate, and this version
  # uses the mission's own phrase anyway.
  'says': u'Si necesita algo de la pulpería, el chavalo de la bici le hace el mandado. Es honrado.',
  'en': u'If you need something from the shop, the lad on the bike will run the errand for you. He is honest.',
  'points_at': ['xalteva-06']},
 {'kind': u'caponero', 'district': 'xalteva',
  'says': u'La maestra anda buscando quién le hable inglés a los chavalos. Ahí en la escuela.',
  'en': u'The teacher is looking for somebody to speak English to the kids. There at the school.',
  'points_at': ['xalteva-07']},
 {'kind': u'viejo de la esquina', 'district': 'xalteva',
  'says': u'En el cementerio hay un señor que lo cuida todo solo. Ese sabe quién es quién.',
  'en': u'There is a man at the cemetery who looks after all of it alone. He knows who is who.',
  'points_at': ['xalteva-08']},
 {'kind': u'evangélico', 'district': 'xalteva',
  'says': u'Están rezando la novena de don Ramón, nueve noches. Puede llegar aunque no sea de aquí.',
  'en': u'They are praying don Ramón’s novena, nine nights. You can go even if you are not from here.',
  'points_at': ['xalteva-09']},
 {'kind': u'obrero', 'district': 'xalteva',
  'says': u'¿Ve esas paredes bajas? Pregúntele al señor de los libros qué son. Le va a encantar.',
  'en': u'See those low walls? Ask the man with the books what they are. He will love it.',
  'points_at': ['xalteva-10']},
 # Guadalupe
 {'kind': u'chavalo en bici', 'district': 'guadalupe',
  'says': u'Todo lo chiquito lo hay en la pulpería de la esquina. Jabón, huevos, lo que sea.',
  'en': u'Everything small is at the corner shop. Soap, eggs, whatever you need.',
  'points_at': ['guadalupe-01']},
 {'kind': u'cuidacarros', 'district': 'guadalupe',
  'says': u'¿Le suena raro la moto? Ahí abajo está el taller. Ese hombre la oye y ya sabe.',
  'en': u'Is your moto making a strange noise? The workshop is down there. That man hears it and he knows.',
  'points_at': ['guadalupe-02']},
 {'kind': u'chavalo en bici', 'district': 'guadalupe',
  'says': u'A las cuatro armamos mejenga en la esquina. Caiga, si quiere jugar.',
  'en': u'At four we get a game going on the corner. Come by if you want to play.',
  'points_at': ['guadalupe-03']},
 {'kind': u'doña en la puerta', 'district': 'guadalupe',
  'says': u'La niña de la vecina cumple años el sábado. Van a invitar a toda la cuadra.',
  'en': u'The neighbour’s little girl has her birthday on Saturday. They are inviting the whole block.',
  'points_at': ['guadalupe-04']},
 {'kind': u'obrero', 'district': 'guadalupe',
  'says': u'Si necesita un mueble, el carpintero se lo hace. Pero no lo apure, que es despacio.',
  'en': u'If you need furniture, the carpenter will make it. But do not rush him, he is slow.',
  'points_at': ['guadalupe-05']},
 {'kind': u'vendedora', 'district': 'guadalupe',
  'says': u'Ese perro no es de nadie, aquí anda desde chiquito. No muerde, no le tenga miedo.',
  'en': u'That dog belongs to nobody, it has been around since it was small. It does not bite, do not be afraid of it.',
  'points_at': ['guadalupe-06']},
 {'kind': u'evangélico', 'district': 'guadalupe',
  'says': u'Hermano, lo invito al culto. Y si no puede, ahí queda la invitación, sin compromiso.',
  'en': u'Brother, I invite you to the service. And if you cannot, the invitation stands, no obligation.',
  'points_at': ['guadalupe-07']},
 {'kind': u'doña en la puerta', 'district': 'guadalupe',
  'says': u'Doña Chepa sabe todo lo que pasa en esta cuadra. Todo, todo.',
  'en': u'Doña Chepa knows everything that happens on this block. Everything.',
  'points_at': ['guadalupe-08']},
 {'kind': u'policía', 'district': 'guadalupe',
  'says': u'Ahí están otra vez peleando por la pared. Si pasa, dígales que se calmen.',
  'en': u'They are arguing about that wall again. If you go past, tell them to calm down.',
  'points_at': ['guadalupe-09']},
 {'kind': u'viejo de la esquina', 'district': 'guadalupe',
  'says': u'La partera de esta cuadra trajo al mundo a medio barrio. A mí también.',
  'en': u'The midwife on this block brought half the barrio into the world. Me as well.',
  'points_at': ['guadalupe-10']},
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
