# -*- coding: utf-8 -*-
"""Writes content/plan/game-spine.json — the whole game, planned before any of
it is written, the way plan/spine.json planned the 185 stories.

You moved to Granada and you live there. There is no plot: there are districts,
and there is everything that happens to somebody living in a Nicaraguan city.
Winning is doing all of it.

Organised by DISTRICT (where) and TIER (how hard), not by act, because a
sandbox has no acts. Tier gates on how much Spanish you have, so the city opens
up as you get better rather than as a story advances.
"""
import io, json, os, sys

ROOT = sys.argv[1]

DISTRICTS = {
 'centro':    (u'El Centro', u'Parque Central, la catedral, La Calzada. Where the tourists are, and where people would rather practise their English on you.'),
 'mercado':   (u'El Mercado', u'The municipal market and the streets around it. Loud, cheap, and where you learn what things actually cost.'),
 'xalteva':   (u'Xalteva', u'The old quarter west of the centre. Churches, quiet streets, old people with time to talk.'),
 'guadalupe': (u'Guadalupe', u'East, sloping toward the water. Families, workshops, kids in the street.'),
 'pantanal':  (u'Pantanal', u'Down by the lake. Poorer, wetter, the part of Granada no postcard shows.'),
 'malecon':   (u'El Malecón', u'The lakefront. Boats, fried fish, Sunday crowds.'),
 'terminal':  (u'La Terminal', u'Buses in and out. Everyone here is going somewhere or has just arrived.'),
 'barrio':    (u'Tu barrio', u'Your own street. The landlady, the pulpería on the corner, neighbours who hear everything.'),
 'trabajo':   (u'El trabajo', u'The workshop and the errands that pay. Where your Spanish stops being polite and starts being useful.'),
 'tramites':  (u'Trámites y salud', u'Offices, clinics, queues. The Spanish nobody teaches and everybody needs.'),
 'fiestas':   (u'Las fiestas', u'The calendar. Some come round once a year and you will miss one.'),
 'afuera':    (u'Afuera', u'Masaya, Catarina, la Laguna, Mombacho. You need wheels and a reason.'),
}

# district, tier, who, title, goal, teaches
M = [
# ── EL CENTRO ────────────────────────────────────────────────────────────
('centro',1,u'El muchacho del hostal',u'La primera noche',u'Get a room for your first three nights',[u'Buenas',u'quiero',u'un cuarto',u'tres noches',u'está bien']),
('centro',1,u'La muchacha del comedor',u'El desayuno',u'Order breakfast and ask what you owe',[u'un gallo pinto',u'por favor',u'un café',u'cuánto le debo']),
('centro',1,u'El mesero',u'En español',u'Get served in Spanish by somebody who would rather practise English',[u'en español',u'estoy aprendiendo',u'ayúdeme',u'de nuevo']),
('centro',2,u'Doña de la banca',u'El calor',u'Sit on a bench and talk about the weather and nothing else',[u'qué calor',u'todos los días',u'así es',u'ni modo']),
('centro',2,u'El cuidacarros',u'El cuidacarros',u'Understand that the man watching your moto has a job, not a racket',[u'se lo cuido',u'diez pesos',u'ahí se lo dejo',u'gracias']),
('centro',2,u'El guía',u'La catedral',u'Get the story of the cathedral out of somebody who wants paying for it',[u'¿me cuenta?',u'no ando',u'otro día',u'muy amable']),
('centro',3,u'El fotógrafo',u'La foto',u'Get a photo taken for a document, not for a postcard',[u'para un documento',u'fondo blanco',u'sin lentes',u'¿cuándo salen?']),
('centro',3,u'El del kiosco',u'El periódico',u'Buy a paper and get told the news before you read it',[u'el periódico',u'¿qué dice?',u'lo de siempre',u'nada bueno']),
('centro',3,u'La turista perdida',u'La gringa perdida',u'Translate for a lost tourist, and feel your accent get worse',[u'ella pregunta',u'dice que',u'no es aquí',u'yo le explico']),
('centro',4,u'El poeta',u'Darío',u'Be told about Rubén Darío by a man who will not stop',[u'el poeta',u'de aquí',u'me lo aprendí',u'de memoria']),
('centro',4,u'El transitero',u'La multa',u'Talk your way out of a ticket, or find out what not doing so costs',[u'jefe',u'no me di cuenta',u'ando sin',u'disculpe la molestia']),
('centro',5,u'El borracho amable',u'El del parque',u'Get away from a friendly drunk without insulting him',[u'ya me voy',u'otro día conversamos',u'cuídese',u'que le vaya bien']),

# ── EL MERCADO ───────────────────────────────────────────────────────────
('mercado',1,u'La verdulera',u'La fruta',u'Buy fruit for the week without paying the chele price',[u'una libra',u'de mango',u'¿a cómo?',u'está caro']),
('mercado',1,u'El del cambio',u'Los reales',u'Change dollars and insist on small notes',[u'quiero cambiar',u'dólares',u'billetes pequeños',u'¿a cómo está?']),
('mercado',2,u'La carnicera',u'La carne',u'Buy meat by weight and get the cut you meant',[u'media libra',u'sin hueso',u'para sopa',u'así está bien']),
('mercado',2,u'El de los granos',u'Los frijoles',u'Buy beans and be told how to cook them',[u'una libra de frijoles',u'rojos',u'¿cómo los hago?',u'con todo']),
('mercado',2,u'Doña de la fritanga',u'La fritanga',u'Order from a fritanga like somebody who eats there',[u'un enchilado',u'con ensalada',u'para llevar',u'ya va']),
('mercado',3,u'El cargador',u'Las bolsas',u'Pay somebody to carry your shopping, agreed first',[u'me ayuda',u'hasta la esquina',u'¿cuánto me cobra?',u'quedamos así']),
('mercado',3,u'La de las tortillas',u'Las tortillas',u'Buy tortillas at the right hour, because later there are none',[u'¿todavía hay?',u'ya se acabaron',u'mañana temprano',u'guárdeme']),
('mercado',3,u'El vendedor insistente',u'El insistente',u'Say no four times to somebody who ignores the first three',[u'no gracias',u'ya tengo',u'de verdad no',u'que le vaya bien']),
('mercado',4,u'La de las hierbas',u'El remedio',u'Be sold a remedy for something you did not know you had',[u'para el estómago',u'lo hierve',u'en ayunas',u'no cuesta nada']),
('mercado',4,u'El pescadero',u'El pescado',u'Buy fish and be able to tell whether it is fresh',[u'está fresco',u'de hoy',u'me lo limpia',u'entero']),
('mercado',4,u'La comadre',u'La comadre',u'Be recognised, and become somebody who comes here',[u'ya lo conozco',u'lo de siempre',u'le guardé',u'así me gusta']),
('mercado',5,u'El regateador',u'El regateo',u'Haggle properly, which is neither arguing nor accepting',[u'me lo deja en',u'ni para usted ni para mí',u'ya pues',u'trato hecho']),

# ── XALTEVA ──────────────────────────────────────────────────────────────
('xalteva',1,u'Doña de los caites',u'¿Por dónde?',u'Ask the way and get an answer with no street names in it',[u'¿dónde queda?',u'dos cuadras',u'al lago',u'arriba']),
('xalteva',2,u'El sacristán',u'La iglesia',u'Get into a church that is shut, and be told why',[u'está cerrado',u'a las cinco',u'venga después',u'con permiso']),
('xalteva',2,u'La beata',u'La misa',u'Talk about mass without pretending to be devout',[u'no soy de aquí',u'respeto mucho',u'algún día',u'primero Dios']),
('xalteva',3,u'Don Chombo',u'El viejo de la esquina',u'Let an old man tell you what this street used to be',[u'antes',u'en aquel tiempo',u'ya no es igual',u'usted no vio eso']),
('xalteva',3,u'La costurera',u'El pantalón',u'Get trousers taken up and agree when they are ready',[u'me lo arregla',u'aquí',u'¿para cuándo?',u'el jueves']),
('xalteva',3,u'El niño de la bici',u'El mandado',u'Send a kid on an errand and get the change back',[u'me hace un mandado',u'aquí está',u'me trae el vuelto',u'para vos']),
('xalteva',4,u'La maestra',u'La escuela',u'Be asked to say hello to a class in English',[u'no soy maestro',u'con mucho gusto',u'¿qué les digo?',u'una vez nada más']),
('xalteva',4,u'El del cementerio',u'El cementerio',u'Walk a cemetery with the man who looks after it',[u'toda mi vida',u'aquí están',u'los cuido',u'nadie viene']),
('xalteva',5,u'Doña Rosa',u'La rezadora',u'Be invited to a novena and know what is expected',[u'nueve noches',u'a las siete',u'no hace falta',u'con eso basta']),
('xalteva',5,u'El historiador',u'Las murallas',u'Hear why this quarter is called Xalteva',[u'los indios',u'antes de',u'la muralla',u'lo que queda']),

# ── GUADALUPE ────────────────────────────────────────────────────────────
('guadalupe',1,u'El pulpero',u'La pulpería',u'Buy the small things at the shop on the corner',[u'me da',u'un jabón',u'y una gaseosa',u'nada más']),
('guadalupe',2,u'El de las motos',u'El taller de motos',u'Describe a noise without knowing the word for it',[u'hace un ruido',u'aquí atrás',u'cuando freno',u'¿es grave?']),
('guadalupe',2,u'Los chavalos',u'La mejenga',u'Get picked for a game on the corner pitch',[u'¿puedo jugar?',u'de este lado',u'pásamela',u'buena esa']),
('guadalupe',3,u'La vecina',u'El cumpleaños',u'Be invited to a birthday and turn up with the right thing',[u'cumple años',u'¿a qué hora?',u'¿llevo algo?',u'felicidades']),
('guadalupe',3,u'El carpintero',u'La mesa',u'Order a table and describe the size with your hands',[u'así de grande',u'de madera',u'¿me la hace?',u'sin prisa']),
('guadalupe',3,u'La señora del perro',u'El perro',u'Deal with a dog that has decided your gate is its gate',[u'ese perro',u'no es mío',u'aquí anda',u'no muerde']),
('guadalupe',4,u'El evangélico',u'El culto',u'Decline an invitation to church without giving offence',[u'le agradezco',u'no soy de esa',u'respeto',u'quizás otro día']),
('guadalupe',4,u'Doña Chepa',u'El chisme',u'Hear gossip and pass it on without getting it wrong',[u'dicen que',u'fíjese que',u'no sea así',u'¿de verdad?']),
('guadalupe',5,u'El vecino bravo',u'El pleito',u'Get between two neighbours arguing over a wall',[u'cálmese',u'no es para tanto',u'hablando se arregla',u'ya estuvo']),
('guadalupe',5,u'La partera',u'La partera',u'Talk to a midwife who has delivered half the street',[u'¿cuántos años?',u'aquí nacieron',u'sin doctor',u'nunca se me murió']),

# ── PANTANAL ─────────────────────────────────────────────────────────────
('pantanal',2,u'El pescador',u'La lancha',u'Get taken out on the lake by somebody who works it',[u'me lleva',u'una hora',u'ida y vuelta',u'temprano']),
('pantanal',2,u'La lavandera',u'El lavado',u'Get your washing done and agree a day',[u'lavar esta ropa',u'para el viernes',u'¿cuánto sale?',u'sin apuro']),
('pantanal',3,u'El del agua',u'No hay agua',u'Find out when the water is coming back',[u'no hay agua',u'desde el martes',u'¿cuándo viene?',u'avíseme']),
('pantanal',3,u'La señora del fogón',u'La leña',u'Buy firewood and carry it further than you expected',[u'un tercio',u'de leña',u'seca',u'ahí se la dejo']),
('pantanal',3,u'El chavalo descalzo',u'El chavalo',u'Be asked for money by a kid, and work out what you think',[u'no tengo',u'te compro algo',u'¿comiste?',u'andá con cuidado']),
('pantanal',4,u'Doña Julia',u'La inundación',u'Help bail out a house after the rain and be fed for it',[u'se metió el agua',u'toda la noche',u'échele',u'coma algo']),
('pantanal',4,u'El albañil',u'El techo',u'Help patch a roof with a man who explains nothing',[u'súbase',u'páseme',u'aquí',u'quieto']),
('pantanal',4,u'La curandera',u'El mal de ojo',u'Be treated for something you do not believe in',[u'le hicieron ojo',u'un huevo',u'no se ría',u'ya verá']),
('pantanal',5,u'El que volvió',u'El que volvió',u'Talk to a man who went south for work and came back with nothing',[u'me fui',u'allá',u'no es como dicen',u'aquí estoy mejor']),
('pantanal',5,u'La abuela',u'El terremoto',u'Hear about 1972 from somebody who was in it',[u'yo tenía',u'esa noche',u'se cayó todo',u'no lo olvido']),

# ── EL MALECÓN ───────────────────────────────────────────────────────────
('malecon',1,u'La del quesillo',u'El quesillo',u'Eat a quesillo and survive the bag it comes in',[u'un quesillo',u'con todo',u'sin cebolla',u'está rico']),
('malecon',2,u'El lanchero',u'Las isletas',u'Haggle a boat around the isletas',[u'una vuelta',u'por las isletas',u'¿cuánto por todos?',u'ida y vuelta']),
('malecon',2,u'El de la pesca',u'El guapote',u'Order fried fish and be told which one is worth it',[u'guapote',u'frito',u'con tajadas',u'el de allá']),
('malecon',3,u'La familia del domingo',u'El domingo',u'Be pulled into somebody’s Sunday on the shore',[u'siéntese',u'hay bastante',u'no sea pena',u'sírvase']),
('malecon',3,u'El del caballo',u'El caballo',u'Turn down a horse ride without making it awkward',[u'no gracias',u'nunca he montado',u'otro día',u'está bonito']),
('malecon',4,u'El músico',u'El son nica',u'Get a musician to explain what he is playing',[u'¿qué es eso?',u'de aquí',u'toque otra',u'me gustó']),
('malecon',4,u'El vigilante',u'La noche',u'Be told, politely, that this is not a good place after dark',[u'ya es tarde',u'mejor váyase',u'por ahí no',u'se lo digo yo']),
('malecon',5,u'El capitán',u'A Ometepe',u'Buy a ferry ticket and understand the schedule',[u'¿a qué hora sale?',u'un pasaje',u'de ida',u'si el lago deja']),

# ── LA TERMINAL ──────────────────────────────────────────────────────────
('terminal',1,u'El cobrador',u'La ruta',u'Take a bus without ending up somewhere else',[u'¿va para?',u'me deja en',u'la parada',u'ya voy bajando']),
('terminal',2,u'El taxista',u'El taxi',u'Agree the fare before you get in, not after',[u'¿cuánto me cobra?',u'al mercado',u'está bien',u'antes de subir']),
('terminal',2,u'El del colectivo',u'El colectivo',u'Understand that a taxi stopping for others is not a scam',[u'va lleno',u'yo voy primero',u'no importa',u'así es aquí']),
('terminal',3,u'La de los boletos',u'El expreso',u'Buy a ticket to Managua and pick the right bus',[u'un boleto',u'el expreso',u'¿a qué hora?',u'el próximo']),
('terminal',3,u'El vendedor del bus',u'El que vende en el bus',u'Buy something from somebody selling in the aisle at speed',[u'¿qué lleva?',u'deme uno',u'aquí tiene',u'gracias joven']),
('terminal',4,u'El de las encomiendas',u'La encomienda',u'Send a package to somebody in another town',[u'mandar esto',u'a Masaya',u'¿llega hoy?',u'¿quién lo recibe?']),
('terminal',4,u'El estafador',u'El que te quiere ver la cara',u'Spot the one who actually is trying it on',[u'no hay cambio',u'espere',u'yo le doy',u'no me venga']),
('terminal',4,u'La señora con maletas',u'Las maletas',u'Help somebody with bags and refuse the money',[u'yo le ayudo',u'no es nada',u'no se preocupe',u'que le vaya bien']),
('terminal',5,u'El chofer',u'El chofer',u'Sit up front and get a driver talking for forty minutes',[u'¿cuántos años maneja?',u'toda la ruta',u'me gusta',u'uno se acostumbra']),
('terminal',5,u'El que se va',u'El migrante',u'Say goodbye to somebody leaving for good',[u'se va',u'¿cuándo vuelve?',u'no sé',u'que Dios lo acompañe']),

# ── TU BARRIO ────────────────────────────────────────────────────────────
('barrio',1,u'Doña Marta',u'El cuarto',u'Rent a room by the month instead of the night',[u'por mes',u'el alquiler',u'¿el agua va incluida?',u'¿desde cuándo?']),
('barrio',1,u'Doña Marta',u'El depósito',u'Understand the deposit and when you get it back',[u'el depósito',u'un mes',u'cuando me vaya',u'quedamos']),
('barrio',2,u'El pulpero',u'Fiado',u'Be given credit at the shop, which means being trusted',[u'fiado',u'me lo apunta',u'mañana le pago',u'ideay']),
('barrio',2,u'El barbero',u'La barbería',u'Get the haircut you actually asked for',[u'más corto',u'a los lados',u'así está bien',u'déjelo así']),
('barrio',2,u'La vecina de al lado',u'La música',u'Ask a neighbour to turn it down at one in the morning',[u'disculpe',u'es muy tarde',u'un favor',u'se lo agradezco']),
('barrio',3,u'El electricista',u'Se fue la luz',u'Get the power back, and learn it is not just your house',[u'se fue la luz',u'en toda la cuadra',u'¿ya llamó?',u'ya viene']),
('barrio',3,u'Roberto',u'El chavalo de al lado',u'Let a kid teach you the words nobody prints',[u'chunche',u'chele',u'vaya pues',u'dale']),
('barrio',3,u'Doña Marta',u'La gotera',u'Report a leak and get it fixed before the rains',[u'hay una gotera',u'en el cuarto',u'cuando llueve',u'¿lo puede ver?']),
('barrio',3,u'El del gas',u'El cilindro',u'Order a gas cylinder and be in when it comes',[u'un cilindro',u'de veinticinco',u'¿a qué hora?',u'aquí estoy']),
('barrio',4,u'La vecina',u'El velorio',u'Say the right thing at a wake, which is almost nothing',[u'lo siento mucho',u'mi pésame',u'era buena gente',u'aquí estamos']),
('barrio',4,u'Doña Chepa',u'La indirecta',u'Realise you are being told off without being told off',[u'no es por nada',u'algunos',u'yo no digo nombres',u'entienda']),
('barrio',4,u'El vecino',u'El favor',u'Be asked a favour you would rather not do',[u'fíjese que',u'es que',u'déjeme ver',u'no le prometo']),
('barrio',5,u'Doña Marta',u'El aumento',u'Be told the rent is going up, and negotiate',[u'va a subir',u'¿desde cuándo?',u'es mucho',u'quedemos en']),
('barrio',5,u'Todos',u'La cuadra',u'Be greeted first, by everybody, on your own street',[u'adiós',u'buenas',u'¿cómo amaneció?',u'ahí vamos']),

# ── EL TRABAJO ───────────────────────────────────────────────────────────
('trabajo',1,u'Doña Chepa',u'El mandado',u'Earn your first córdobas carrying somebody else’s shopping',[u'yo se lo llevo',u'¿cuánto me da?',u'está bien',u'cuando quiera']),
('trabajo',2,u'Don Emilio',u'El taller',u'Ask for work and be told what you are actually worth',[u'busco trabajo',u'sé un poco',u'aprendo rápido',u'pruébeme']),
('trabajo',2,u'Marcos',u'El compañero',u'Make your first real friend at work',[u'¿qué pasó?',u'todo bien',u'vamos',u'nos vemos']),
('trabajo',3,u'Don Emilio',u'La jerarquía',u'Learn who you may and may not contradict',[u'con permiso',u'usted dirá',u'como usted diga',u'no me toca']),
('trabajo',3,u'Marcos',u'La quincena',u'Survive the week before payday',[u'no ando',u'hasta la quincena',u'me presta',u'se lo devuelvo']),
('trabajo',3,u'El cliente',u'El cliente',u'Explain a delay to somebody who does not want to hear it',[u'no está listo',u'para el lunes',u'le aviso',u'una disculpa']),
('trabajo',4,u'Don Emilio',u'El error',u'Own a mistake that cost money',[u'fue mío',u'yo lo hice',u'lo arreglo',u'no vuelve a pasar']),
('trabajo',4,u'Marcos',u'La cerveza del viernes',u'Drink with workmates and keep up with the joking',[u'una fría',u'yo invito',u'no seás así',u'ya va la última']),
('trabajo',5,u'Don Emilio',u'El aumento del sueldo',u'Ask for more money without insulting anybody',[u'quería hablarle',u'ya llevo',u'lo que usted crea',u'le agradezco']),
('trabajo',5,u'El nuevo',u'El nuevo',u'Teach somebody newer than you, in Spanish',[u'ponete aquí',u'así no',u'mirá',u'vas bien']),

# ── TRÁMITES Y SALUD ─────────────────────────────────────────────────────
('tramites',2,u'La farmacéutica',u'La farmacia',u'Explain what hurts and get something for it',[u'me duele',u'la cabeza',u'desde ayer',u'algo suave']),
('tramites',2,u'La de la ventanilla',u'La fila',u'Queue, and find out you are in the wrong one',[u'¿es aquí?',u'la otra ventanilla',u'¿quién es el último?',u'yo sigo']),
('tramites',3,u'El del banco',u'El banco',u'Open an account with documents you do not have',[u'quiero abrir',u'no tengo',u'¿qué necesito?',u'vuelvo mañana']),
('tramites',3,u'La enfermera',u'El centro de salud',u'Get seen at a clinic and describe symptoms properly',[u'tengo fiebre',u'tres días',u'me duele aquí',u'¿es grave?']),
('tramites',3,u'El de migración',u'La prórroga',u'Extend a visa and be sent away twice first',[u'la prórroga',u'treinta días',u'¿qué más?',u'ya vengo']),
('tramites',4,u'El dentista',u'La muela',u'Get a tooth dealt with while explaining the pain',[u'esta muela',u'cuando como',u'con el frío',u'sáquemela']),
('tramites',4,u'El policía',u'La denuncia',u'Report a stolen phone and manage your expectations',[u'me robaron',u'anoche',u'poner una denuncia',u'¿sirve de algo?']),
('tramites',4,u'La abogada',u'El papel',u'Get a document notarised without understanding it',[u'necesito',u'un papel',u'¿usted me lo hace?',u'¿cuánto cobra?']),
('tramites',5,u'El doctor',u'El dengue',u'Have dengue explained to you while you have it',[u'mucho suero',u'no se levante',u'si empeora',u'una semana']),
('tramites',5,u'La de la ventanilla',u'La cédula',u'Sit through the whole bureaucracy for one piece of card',[u'vengo por',u'ya entregué',u'me dijeron',u'¿cuál es el mío?']),

# ── LAS FIESTAS (date-gated) ─────────────────────────────────────────────
('fiestas',2,u'Doña Marta',u'La Purísima',u'Sing at a door on the 7th of December and get sweets for it',[u'¿quién causa tanta alegría?',u'la concepción',u'gorra',u'vivan las gorras']),
('fiestas',3,u'El vecino',u'La Gritería',u'Go door to door and keep up with the responses',[u'gritería',u'ya empezó',u'vamos',u'aquí dan bueno']),
('fiestas',3,u'La de la alfombra',u'Semana Santa',u'Help make a sawdust carpet before the procession walks over it',[u'aserrín',u'la alfombra',u'no lo pise',u'toda la noche']),
('fiestas',3,u'El jinete',u'La Hípica',u'Watch the horse parade and understand what is being shown off',[u'los caballos',u'ese es de',u'qué bonito',u'todos los años']),
('fiestas',4,u'El enmascarado',u'El Torovenado',u'Work out that the costumes are mocking somebody specific',[u'se están burlando',u'¿de quién?',u'del alcalde',u'nadie se salva']),
('fiestas',4,u'La bailarina',u'El Palo de Mayo',u'Be dragged into dancing something you cannot dance',[u'no sé bailar',u'nadie sabe',u'movete',u'ya vas']),
('fiestas',4,u'Doña Marta',u'La Nochebuena',u'Get through Christmas Eve with somebody else’s family',[u'nochebuena',u'a las doce',u'feliz navidad',u'que se repita']),
('fiestas',5,u'Todos',u'El año viejo',u'Burn an old year, which is a doll, in the street at midnight',[u'el año viejo',u'quemarlo',u'que se vaya',u'feliz año']),

# ── AFUERA ───────────────────────────────────────────────────────────────
('afuera',3,u'La artesana',u'Masaya',u'Buy a hammock and get the price down',[u'una hamaca',u'está muy caro',u'¿me lo deja en?',u'me la llevo']),
('afuera',3,u'El alfarero',u'San Juan de Oriente',u'Watch pottery being made and ask how long it took to learn',[u'¿cuánto tardó?',u'desde chavalo',u'mi papá',u'está lindo']),
('afuera',4,u'El del mirador',u'Catarina',u'Look down at the laguna and be told what you are seeing',[u'ahí está',u'la laguna',u'aquel es',u'se ve todo']),
('afuera',4,u'El guía de Mombacho',u'Mombacho',u'Climb a volcano with a guide who talks the whole way',[u'el volcán',u'ahí arriba',u'despacio',u'ya casi']),
('afuera',4,u'El de la laguna',u'La Laguna de Apoyo',u'Swim in a crater and be warned about the current',[u'está honda',u'no vaya lejos',u'el agua es',u'salga ya']),
('afuera',5,u'El caficultor',u'El cafetal',u'Pick coffee for a day and be judged on your speed',[u'el corte',u'sólo las rojas',u'con las dos manos',u'va aprendiendo']),
('afuera',5,u'El de Nandaime',u'La carretera',u'Break down between towns and get help from strangers',[u'se me quedó',u'no arranca',u'¿me da un jalón?',u'Dios se lo pague']),
('afuera',5,u'Los de Masatepe',u'La sopa',u'Eat sopa de mondongo and be watched while you do it',[u'mondongo',u'primera vez',u'está fuerte',u'me gustó']),
]

# The phrases a person says every day, which therefore have to COME BACK. The
# help ladder is driven by how many times you have met a phrase, so a chunk
# taught once and never seen again strands the player on rung one forever. The
# course's RETURN rule exists to catch exactly this.
#
# Everything else is exempt on purpose, the same way the course exempts
# one-scene words: '¿quién causa tanta alegría?' cannot honestly recur, and
# pretending otherwise is worse than teaching it once and well.
CORE = [u'Buenas',u'por favor',u'gracias',u'está bien',u'quiero',u'me da',u'vaya pues',
        u'ideay',u'ni modo',u'así es',u'me deja en',u'con permiso',u'fíjese que',
        u'dale',u'cuídese',u'no ando',u'ya va',u'todo bien',u'vamos',u'nos vemos',
        u'que le vaya bien',u'disculpe',u'¿a cómo?',u'otro día']

spine, per = [], {}
for n, (dist, tier, who, title, goal, teaches) in enumerate(M):
    per[dist] = per.get(dist, 0) + 1
    earlier = set(c for m in spine for c in m['teaches'] + m['reuses'] if c in CORE)
    pool = [c for c in CORE if c in earlier]
    reuses = sorted(set(pool[(n * 3 + i) % len(pool)] for i in range(3)) - set(teaches)) if pool else []
    spine.append({
        'id': '%s-%02d' % (dist, per[dist]),
        'district': dist, 'tier': tier, 'who': who,
        'title': title, 'goal': goal,
        'teaches': teaches, 'reuses': reuses,
    })

# The crowd. Most people on the street are not a mission — they point you at
# one. That IS the quest system, because there are no map markers and Granada
# has no usable street names.
CROWD = [
 (u'vendedora', 12, u'Sells something from a doorway. Knows who buys what.'),
 (u'chavalo en bici', 10, u'Kids on bikes. Know where everyone is, and are wrong about a third of the time.'),
 (u'doña en la puerta', 14, u'Out in a rocking chair. Sees everything on the street.'),
 (u'caponero', 8, u'Waiting for a fare. Knows every address in town.'),
 (u'obrero', 8, u'Working on something. Short answers, useful ones.'),
 (u'viejo de la esquina', 6, u'Has time. Tells you more than you asked.'),
 (u'turista', 6, u'Lost, and speaks English at you. Talking to them raises your chele.'),
 (u'cuidacarros', 5, u'Watching parked motos. Sees who comes and goes.'),
 (u'evangélico', 4, u'Wants to invite you somewhere, and genuinely knows the barrio.'),
 (u'borracho amable', 3, u'Unreliable, friendly, occasionally right.'),
 (u'policía', 4, u'Answers what you ask and nothing more.'),
 (u'perro', 10, u'Not a source of hints.'),
]

out = os.path.join(ROOT, 'content', 'plan', 'game-spine.json')
with io.open(out, 'w', encoding='utf-8') as f:
    f.write(json.dumps({
        'premise': (u'You moved to Granada and you live there. There is no plot. '
                    u'There are districts, and everything that happens to somebody '
                    u'living in a Nicaraguan city. Winning is doing all of it.'),
        'districts': {k: {'name': v[0], 'desc': v[1]} for k, v in DISTRICTS.items()},
        'crowd': [{'kind': k, 'count': n, 'note': d} for k, n, d in CROWD],
        'core': CORE,
        'missions': spine,
    }, ensure_ascii=False, indent=1) + u'\n')

met = {}
for m in spine:
    for c in m['teaches'] + m['reuses']:
        met[c] = met.get(c, 0) + 1
cold = [c for c in CORE if met.get(c, 0) < 3]
print('missions:', len(spine))
print('by district:', ' '.join('%s:%d' % (k, per[k]) for k in DISTRICTS if k in per))
print('by tier:', ' '.join('%d:%d' % (t, sum(1 for m in spine if m['tier'] == t)) for t in (1,2,3,4,5)))
print('chunks taught:', sum(len(m['teaches']) for m in spine), ' distinct:', len(met))
print('core phrases:', len(CORE), ' reaching rung three:', len(CORE) - len(cold))
if cold:
    print('  NOT recurring enough:', ', '.join(cold).encode('ascii', 'replace').decode())
print('crowd NPCs planned:', sum(n for _, n, _ in CROWD))
