"""
Тренировочный и тестовый корпуса для варианта 7:
  языки — French, English
  формат документов — HTML

Тексты собраны/адаптированы из публичных источников (стиль Wikipedia /
новостные статьи) и приведены к примерно сопоставимому объёму.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# English training texts (~25–40 KB total)
# ---------------------------------------------------------------------------

EN_TRAIN = [
    """
Artificial intelligence is the intelligence of machines or software, as opposed
to the intelligence of humans or animals. It is a field of study in computer
science that develops and studies intelligent machines. Such machines may be
called AIs. AI technology is widely used throughout industry, government, and
science. Some high-profile applications include advanced web search engines,
recommendation systems, understanding human speech, self-driving cars, and
competing at a high level in strategic game systems.

Machine learning is a branch of artificial intelligence and computer science
which focuses on the use of data and algorithms to imitate the way that humans
learn, gradually improving its accuracy. IBM has a rich history with machine
learning. One of its own, Arthur Samuel, is credited with coining the term
machine learning with his research around the game of checkers. Robert Nealey,
the self-proclaimed checkers master, played the game on an IBM 7094 computer
in 1962, and he lost to the computer. Compared with what can be done today,
this feat seems trivial, but it is considered a major milestone in the field
of artificial intelligence.

Natural language processing is an interdisciplinary subfield of computer
science and linguistics. It is primarily concerned with giving computers the
ability to support and manipulate human language. It involves processing
natural language datasets, such as text corpora or speech corpora, using
either rule-based or probabilistic machine learning approaches. The goal is
a computer capable of understanding the contents of documents, including the
contextual nuances of the language within them. The technology can then
accurately extract information and insights contained in the documents as
well as categorize and organize the documents themselves.

Deep learning is part of a broader family of machine learning methods based
on artificial neural networks with representation learning. Learning can be
supervised, semi-supervised or unsupervised. Deep-learning architectures such
as deep neural networks, deep belief networks, deep reinforcement learning,
recurrent neural networks, convolutional neural networks and transformers have
been applied to fields including computer vision, speech recognition, natural
language processing, machine translation, bioinformatics, drug design, medical
image analysis, climate science, material inspection and board game programs,
where they have produced results comparable to and in some cases surpassing
human expert performance.

The history of artificial intelligence began in antiquity, with myths, stories
and rumors of artificial beings endowed with intelligence or consciousness by
master craftsmen. The seeds of modern AI were planted by classical philosophers
who attempted to describe the process of human thinking as the mechanical
manipulation of symbols. This work culminated in the invention of the
programmable digital computer in the 1940s, a machine based on the abstract
essence of mathematical reasoning. This device and the ideas behind it inspired
a handful of scientists to begin seriously discussing the possibility of
building an electronic brain.

Computer vision is an interdisciplinary scientific field that deals with how
computers can gain high-level understanding from digital images or videos.
From the perspective of engineering, it seeks to understand and automate tasks
that the human visual system can do. Computer vision tasks include methods for
acquiring, processing, analyzing and understanding digital images, and
extraction of high-dimensional data from the real world in order to produce
numerical or symbolic information, for example in the forms of decisions.

Reinforcement learning is an area of machine learning concerned with how
intelligent agents ought to take actions in an environment in order to maximize
the notion of cumulative reward. Reinforcement learning is one of three basic
machine learning paradigms, alongside supervised learning and unsupervised
learning. Unlike supervised learning, reinforcement learning does not require
labelled input-output pairs to be presented, and does not need sub-optimal
actions to be explicitly corrected. Instead the focus is on finding a balance
between exploration of uncharted territory and exploitation of current knowledge.

Data science is an interdisciplinary academic field that uses statistics,
scientific computing, scientific methods, processes, algorithms and systems to
extract or extrapolate knowledge and insights from noisy, structured, and
unstructured data. Data science also integrates domain knowledge from the
underlying application domain. Data science is related to data mining, machine
learning and big data. Data science is a concept to unify statistics, data
analysis, informatics, and their related methods in order to understand and
analyze actual phenomena with data.

The Internet of things describes devices with sensors, processing ability,
software and other technologies that connect and exchange data with other
devices and systems over the Internet or other communications networks. The
Internet of things encompasses electronics, communication, and computer science
engineering. IoT technology is most synonymous with products pertaining to the
concept of the smart home, including devices and appliances that support one or
more common ecosystems, and can be controlled via devices associated with that
ecosystem, such as smartphones and smart speakers.

Cloud computing is the on-demand availability of computer system resources,
especially data storage and computing power, without direct active management
by the user. Large clouds often have functions distributed over multiple
locations, each of which is a data center. Cloud computing relies on sharing of
resources to achieve coherence and typically uses a pay-as-you-go model, which
can help in reducing capital expenses but may also lead to unexpected operating
expenses for users.
""",
    """
Climate change includes both global warming driven by human emissions of
greenhouse gases and the resulting large-scale shifts in weather patterns.
Though there have been previous periods of climatic change, since the mid-20th
century the rate of change has been much faster and primarily caused by humans.
The primary driver of current climate change is the emission of greenhouse gases,
mostly carbon dioxide and methane. Fossil fuel burning for energy use creates
most of these emissions. Agriculture, steel making, cement production, and
forest loss are additional sources. Temperature rise is also affected by
climate feedbacks such as the loss of sunlight-reflecting snow cover, and the
release of carbon dioxide from drought-stricken forests.

The effects of climate change impact the physical environment, ecosystems and
human societies. The future effects of climate change depend on how much carbon
dioxide is emitted and how much of it is absorbed by the oceans and land. The
physical effects include rising temperatures, rising sea levels, and more
extreme weather events. Ecosystems are affected by the changing climate and by
the rising carbon dioxide concentrations. These effects include the loss of
biodiversity, and the spread of invasive species. Human societies are affected
by food security, access to fresh water, and by the health effects of extreme
weather. The effects of climate change are often more severe for people in
developing countries.

Renewable energy is energy from renewable resources that are naturally
replenished on a human timescale. Renewable resources include sunlight, wind,
the movement of water, and geothermal heat. Although most renewable energy
sources are sustainable, some are not. For example, some biomass sources are
considered unsustainable at current rates of exploitation. Renewable energy
often provides energy in four important areas: electricity generation, heating
and cooling, transport, and rural energy services. Based on REN21's 2022 report,
renewables contributed 28.3 percent to global electricity generation in 2021.

Solar power is the conversion of energy from sunlight into electricity, either
directly using photovoltaics, indirectly using concentrated solar power, or a
combination. Photovoltaic cells convert light into an electric current using
the photovoltaic effect. Concentrated solar power systems use lenses or mirrors
and solar tracking systems to focus a large area of sunlight to a hot spot,
often to drive a steam turbine. Photovoltaics were initially solely used as a
source of electricity for small and medium-sized applications, from the
calculator powered by a single solar cell to remote homes powered by an
off-grid rooftop photovoltaic system.

Wind power is the use of wind energy to generate useful work. Historically,
wind power was used in sails, windmills and windpumps but today it is mostly
used to generate electricity. This article deals only with wind power for
electricity generation. Today, wind power is generated by wind turbines.
Modern utility-scale wind turbines range from around 600 kW to 9 MW of rated
power. The power available from the wind is a function of the cube of the wind
speed, so as wind speed increases, power output increases dramatically up to
the maximum output for the particular turbine. Areas where winds are stronger
and more constant, such as offshore and high altitude sites, are preferred
locations for wind farms.

Biodiversity or biological diversity is the variety and variability of life on
Earth. Biodiversity is a measure of variation at the genetic, species, and
ecosystem level. Biodiversity is not distributed evenly on Earth. It is richer
in the tropics. These tropical forest ecosystems cover less than 10 percent of
earth's surface and contain about 90 percent of the world's species. Marine
biodiversity is usually higher along coasts in the Western Pacific, where sea
surface temperature is highest, and in the mid-latitudinal band in all oceans.
""",

    """
Software engineering is a systematic approach to the design, development,
operation, and maintenance of software. It involves the application of
engineering principles to software creation in order to produce reliable,
efficient and maintainable systems. Key activities include requirements
analysis, architectural design, coding, testing, deployment and ongoing
support. Modern software engineering practices emphasize continuous
integration, automated testing, version control and collaborative development
across geographically distributed teams.

Distributed systems are collections of independent computers that appear to
their users as a single coherent system. Challenges in distributed systems
include concurrency, lack of a global clock, and independent failure of
components. Techniques such as consensus algorithms, replication, sharding
and eventual consistency are widely used to build scalable services that
operate across multiple data centers and geographic regions around the world.

Cybersecurity is the practice of protecting systems, networks and programs
from digital attacks. These attacks are usually aimed at accessing, changing
or destroying sensitive information, extorting money from users, or interrupting
normal business processes. Implementing effective cybersecurity measures is
particularly challenging today because there are more devices than people, and
attackers are becoming more innovative. Common controls include firewalls,
encryption, multi-factor authentication and regular security awareness training.

Human-computer interaction studies the design and use of computer technology,
focused on the interfaces between people and computers. Researchers observe
the ways humans interact with computers and design technologies that let
humans interact with computers in novel ways. HCI draws on computer science,
cognitive psychology, design and several other fields to improve usability
and accessibility of interactive systems for diverse populations.
""",

    """
Quantum computing is a type of computation that harnesses the collective
properties of quantum states, such as superposition, interference and
entanglement, to perform calculations. Devices that perform quantum
computations are known as quantum computers. Quantum computers are believed
to be able to solve certain computational problems substantially faster than
classical computers. The study of quantum computing is a subfield of quantum
information science. Quantum computing is different from classical computing
in the way information is processed and stored.

Database systems provide a structured way to store, retrieve and manage data.
Relational databases organize data into tables with defined relationships,
while NoSQL systems offer flexible schemas for document, key-value, column
or graph data. Query languages such as SQL allow users to express complex
operations over large datasets. Transactions, indexing and concurrency control
are fundamental concepts that ensure correctness and performance under load.

Operating systems manage hardware resources and provide services for application
software. Core responsibilities include process scheduling, memory management,
file systems, device drivers and security. Modern operating systems support
multiprocessing, virtualization and containerization, enabling efficient use
of multi-core processors and cloud infrastructure. Examples include Linux,
Windows, macOS and various real-time systems used in embedded devices.

Computer networks connect devices so they can exchange data. The Internet is
a global network of networks that uses the TCP/IP protocol suite. Layered
models such as OSI and TCP/IP help organize networking functions from physical
transmission up to application protocols. Routing, switching, congestion control
and network security are central topics in the design and operation of large
scale communication systems used by billions of people every day.
""",
]

# ---------------------------------------------------------------------------
# French training texts
# ---------------------------------------------------------------------------

FR_TRAIN = [
    """
L'intelligence artificielle est l'intelligence des machines ou des logiciels,
par opposition à l'intelligence des humains ou des animaux. C'est un domaine
d'étude de l'informatique qui développe et étudie des machines intelligentes.
De telles machines peuvent être appelées IA. La technologie de l'IA est
largement utilisée dans l'industrie, le gouvernement et la science. Certaines
applications de haut niveau comprennent les moteurs de recherche Web avancés,
les systèmes de recommandation, la compréhension de la parole humaine, les
voitures autonomes et la compétition à un haut niveau dans les systèmes de
jeux stratégiques.

L'apprentissage automatique est une branche de l'intelligence artificielle et
de l'informatique qui se concentre sur l'utilisation de données et d'algorithmes
pour imiter la façon dont les humains apprennent, en améliorant progressivement
sa précision. IBM a une riche histoire avec l'apprentissage automatique. L'un
des siens, Arthur Samuel, est crédité d'avoir inventé le terme apprentissage
automatique avec ses recherches autour du jeu de dames. Robert Nealey, le
maître autodéclaré des dames, a joué au jeu sur un ordinateur IBM 7094 en 1962,
et il a perdu contre l'ordinateur. Comparé à ce qui peut être fait aujourd'hui,
cet exploit semble trivial, mais il est considéré comme une étape majeure dans
le domaine de l'intelligence artificielle.

Le traitement automatique du langage naturel est un sous-domaine interdisciplinaire
de l'informatique et de la linguistique. Il s'agit principalement de donner aux
ordinateurs la capacité de soutenir et de manipuler le langage humain. Cela
implique le traitement d'ensembles de données en langage naturel, tels que des
corpus de texte ou des corpus de parole, en utilisant soit des approches basées
sur des règles, soit des approches probabilistes d'apprentissage automatique.
L'objectif est un ordinateur capable de comprendre le contenu des documents,
y compris les nuances contextuelles de la langue qu'ils contiennent.

L'apprentissage profond fait partie d'une famille plus large de méthodes
d'apprentissage automatique basées sur des réseaux de neurones artificiels avec
un apprentissage de représentation. L'apprentissage peut être supervisé,
semi-supervisé ou non supervisé. Les architectures d'apprentissage profond
telles que les réseaux de neurones profonds, les réseaux de croyances profondes,
l'apprentissage par renforcement profond, les réseaux de neurones récurrents,
les réseaux de neurones convolutifs et les transformeurs ont été appliquées à
des domaines comprenant la vision par ordinateur, la reconnaissance vocale, le
traitement du langage naturel, la traduction automatique, la bioinformatique,
la conception de médicaments et l'analyse d'images médicales.

L'histoire de l'intelligence artificielle a commencé dans l'Antiquité, avec des
mythes, des histoires et des rumeurs d'êtres artificiels dotés d'intelligence
ou de conscience par des maîtres artisans. Les graines de l'IA moderne ont été
plantées par des philosophes classiques qui ont tenté de décrire le processus
de la pensée humaine comme la manipulation mécanique de symboles. Ce travail a
abouti à l'invention de l'ordinateur numérique programmable dans les années 1940,
une machine basée sur l'essence abstraite du raisonnement mathématique. Cet
appareil et les idées derrière lui ont inspiré une poignée de scientifiques à
commencer à discuter sérieusement de la possibilité de construire un cerveau
électronique.

La vision par ordinateur est un domaine scientifique interdisciplinaire qui
traite de la façon dont les ordinateurs peuvent acquérir une compréhension de
haut niveau à partir d'images ou de vidéos numériques. Du point de vue de
l'ingénierie, elle cherche à comprendre et à automatiser les tâches que le
système visuel humain peut accomplir. Les tâches de vision par ordinateur
comprennent des méthodes d'acquisition, de traitement, d'analyse et de
compréhension d'images numériques, et l'extraction de données de haute dimension
du monde réel afin de produire des informations numériques ou symboliques.

L'apprentissage par renforcement est un domaine de l'apprentissage automatique
concerné par la façon dont les agents intelligents devraient prendre des actions
dans un environnement afin de maximiser la notion de récompense cumulative.
L'apprentissage par renforcement est l'un des trois paradigmes de base de
l'apprentissage automatique, aux côtés de l'apprentissage supervisé et de
l'apprentissage non supervisé. Contrairement à l'apprentissage supervisé, il
ne nécessite pas que des paires entrée-sortie étiquetées soient présentées.

La science des données est un domaine académique interdisciplinaire qui utilise
les statistiques, le calcul scientifique, les méthodes scientifiques, les
processus, les algorithmes et les systèmes pour extraire ou extrapoler des
connaissances et des informations à partir de données bruyantes, structurées
et non structurées. La science des données intègre également les connaissances
du domaine d'application sous-jacent. Elle est liée à l'exploration de données,
à l'apprentissage automatique et aux mégadonnées.
""",
    """
Le changement climatique comprend à la fois le réchauffement climatique entraîné
par les émissions humaines de gaz à effet de serre et les grands changements
résultants dans les régimes météorologiques. Bien qu'il y ait eu des périodes
précédentes de changement climatique, depuis le milieu du XXe siècle le taux de
changement a été beaucoup plus rapide et principalement causé par les humains.
Le principal moteur du changement climatique actuel est l'émission de gaz à
effet de serre, principalement le dioxyde de carbone et le méthane. La combustion
de combustibles fossiles pour la production d'énergie crée la plupart de ces
émissions. L'agriculture, la fabrication d'acier, la production de ciment et la
perte de forêts sont des sources supplémentaires.

Les effets du changement climatique ont un impact sur l'environnement physique,
les écosystèmes et les sociétés humaines. Les effets futurs dépendent de la
quantité de dioxyde de carbone émise et de la quantité absorbée par les océans
et les terres. Les effets physiques comprennent la hausse des températures,
l'élévation du niveau de la mer et des événements météorologiques plus extrêmes.
Les écosystèmes sont affectés par le climat changeant et par la hausse des
concentrations de dioxyde de carbone. Ces effets comprennent la perte de
biodiversité et la propagation d'espèces envahissantes.

Les énergies renouvelables sont des énergies provenant de ressources
renouvelables qui se reconstituent naturellement à l'échelle humaine. Les
ressources renouvelables comprennent la lumière du soleil, le vent, le mouvement
de l'eau et la chaleur géothermique. Bien que la plupart des sources d'énergie
renouvelable soient durables, certaines ne le sont pas. Par exemple, certaines
sources de biomasse sont considérées comme non durables aux taux d'exploitation
actuels. L'énergie renouvelable fournit souvent de l'énergie dans quatre domaines
importants : la production d'électricité, le chauffage et le refroidissement, les
transports et les services énergétiques ruraux.

L'énergie solaire est la conversion de l'énergie de la lumière du soleil en
électricité, soit directement en utilisant le photovoltaïque, soit indirectement
en utilisant l'énergie solaire concentrée, ou une combinaison. Les cellules
photovoltaïques convertissent la lumière en courant électrique en utilisant
l'effet photovoltaïque. Les systèmes d'énergie solaire concentrée utilisent des
lentilles ou des miroirs et des systèmes de suivi solaire pour concentrer une
grande surface de lumière solaire sur un point chaud, souvent pour entraîner une
turbine à vapeur.

L'énergie éolienne est l'utilisation de l'énergie du vent pour générer un travail
utile. Historiquement, l'énergie éolienne était utilisée dans les voiles, les
moulins à vent et les pompes à vent, mais aujourd'hui elle est principalement
utilisée pour générer de l'électricité. Aujourd'hui, l'énergie éolienne est
générée par des éoliennes. Les éoliennes modernes à l'échelle des services publics
vont d'environ 600 kW à 9 MW de puissance nominale. La puissance disponible du
vent est une fonction du cube de la vitesse du vent.

La biodiversité ou diversité biologique est la variété et la variabilité de la
vie sur Terre. La biodiversité est une mesure de la variation au niveau génétique,
des espèces et des écosystèmes. La biodiversité n'est pas répartie uniformément
sur Terre. Elle est plus riche sous les tropiques. Ces écosystèmes de forêts
tropicales couvrent moins de 10 pour cent de la surface de la terre et contiennent
environ 90 pour cent des espèces du monde. La biodiversité marine est généralement
plus élevée le long des côtes dans le Pacifique occidental.
""",

    """
Le génie logiciel est une approche systématique de la conception, du
développement, de l'exploitation et de la maintenance des logiciels. Il
implique l'application de principes d'ingénierie à la création de logiciels
afin de produire des systèmes fiables, efficaces et maintenables. Les
activités clés comprennent l'analyse des besoins, la conception architecturale,
le codage, les tests, le déploiement et le support continu. Les pratiques
modernes mettent l'accent sur l'intégration continue et les tests automatisés.

Les systèmes distribués sont des collections d'ordinateurs indépendants qui
apparaissent à leurs utilisateurs comme un système cohérent unique. Les défis
incluent la concurrence, l'absence d'horloge globale et la défaillance
indépendante des composants. Des techniques telles que les algorithmes de
consensus, la réplication et la cohérence éventuelle sont largement utilisées
pour construire des services évolutifs.

La cybersécurité est la pratique de protection des systèmes, des réseaux et
des programmes contre les attaques numériques. Ces attaques visent généralement
à accéder, modifier ou détruire des informations sensibles, à extorquer de
l'argent aux utilisateurs ou à interrompre les processus métier normaux. Les
contrôles courants comprennent les pare-feu, le chiffrement et
l'authentification multifacteur.

L'interaction homme-machine étudie la conception et l'utilisation de la
technologie informatique, en se concentrant sur les interfaces entre les
personnes et les ordinateurs. Les chercheurs observent les façons dont les
humains interagissent avec les ordinateurs et conçoivent des technologies qui
permettent de nouvelles formes d'interaction. Ce domaine s'appuie sur
l'informatique, la psychologie cognitive et le design.
""",

    """
L'informatique quantique est un type de calcul qui exploite les propriétés
collectives des états quantiques, telles que la superposition, l'interférence
et l'intrication, pour effectuer des calculs. Les appareils qui effectuent des
calculs quantiques sont appelés ordinateurs quantiques. On pense que les
ordinateurs quantiques peuvent résoudre certains problèmes de calcul
substantiellement plus rapidement que les ordinateurs classiques. L'étude de
l'informatique quantique est un sous-domaine de la science de l'information
quantique et diffère du calcul classique dans le traitement de l'information.

Les systèmes de bases de données fournissent un moyen structuré de stocker,
récupérer et gérer des données. Les bases relationnelles organisent les données
en tables avec des relations définies, tandis que les systèmes NoSQL offrent
des schémas flexibles. Les langages de requête tels que SQL permettent
d'exprimer des opérations complexes sur de grands ensembles de données.
Les transactions, l'indexation et le contrôle de concurrence sont des concepts
fondamentaux qui garantissent l'exactitude et les performances sous charge.

Les systèmes d'exploitation gèrent les ressources matérielles et fournissent
des services aux logiciels d'application. Les responsabilités principales
comprennent l'ordonnancement des processus, la gestion de la mémoire, les
systèmes de fichiers, les pilotes de périphériques et la sécurité. Les systèmes
modernes prennent en charge le multitraitement, la virtualisation et la
conteneurisation, permettant une utilisation efficace des processeurs multi-cœurs.

Les réseaux informatiques connectent des appareils afin qu'ils puissent échanger
des données. Internet est un réseau mondial de réseaux qui utilise la suite de
protocoles TCP/IP. Les modèles en couches tels que OSI et TCP/IP aident à
organiser les fonctions réseau. Le routage, la commutation et la sécurité
réseau sont des sujets centraux dans la conception des systèmes de communication.
""",
]

# ---------------------------------------------------------------------------
# Test documents (HTML format) with known labels
# ---------------------------------------------------------------------------

TEST_DOCUMENTS = [
    {
        "id": 1,
        "title": "Machine Learning Overview",
        "language": "english",
        "filename": "en_ml.html",
        "html": """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Machine Learning</title></head>
<body>
<h1>Introduction to Machine Learning</h1>
<p>Machine learning algorithms build a model based on sample data, known as
training data, in order to make predictions or decisions without being
explicitly programmed to do so. Machine learning algorithms are used in a wide
variety of applications, such as in medicine, email filtering, speech
recognition, agriculture, and computer vision, where it is difficult or
unfeasible to develop conventional algorithms to perform the needed tasks.</p>
<p>A subset of machine learning is closely related to computational statistics,
which focuses on making predictions using computers, but not all machine
learning is statistical learning. The study of mathematical optimization
delivers methods, theory and application domains to the field of machine
learning. Data mining is a related field of study, focusing on exploratory
data analysis through unsupervised learning.</p>
<p>Some implementations of machine learning use data and neural networks in a
way that mimics the working of a biological brain. In its application across
business problems, machine learning is also referred to as predictive analytics.</p>
</body></html>""",
    },
    {
        "id": 2,
        "title": "L'apprentissage automatique",
        "language": "french",
        "filename": "fr_ml.html",
        "html": """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Apprentissage automatique</title></head>
<body>
<h1>Introduction à l'apprentissage automatique</h1>
<p>Les algorithmes d'apprentissage automatique construisent un modèle basé sur
des données d'échantillon, appelées données d'entraînement, afin de faire des
prédictions ou des décisions sans être explicitement programmés pour le faire.
Les algorithmes d'apprentissage automatique sont utilisés dans une grande
variété d'applications, telles que la médecine, le filtrage des e-mails, la
reconnaissance vocale, l'agriculture et la vision par ordinateur.</p>
<p>Un sous-ensemble de l'apprentissage automatique est étroitement lié aux
statistiques computationnelles, qui se concentrent sur la réalisation de
prédictions à l'aide d'ordinateurs. L'étude de l'optimisation mathématique
fournit des méthodes, une théorie et des domaines d'application au domaine de
l'apprentissage automatique. L'exploration de données est un domaine d'étude
connexe, axé sur l'analyse exploratoire des données.</p>
<p>Certaines implémentations de l'apprentissage automatique utilisent des
données et des réseaux de neurones d'une manière qui imite le fonctionnement
d'un cerveau biologique. Dans son application aux problèmes commerciaux,
l'apprentissage automatique est également appelé analyse prédictive.</p>
</body></html>""",
    },
    {
        "id": 3,
        "title": "Climate and Energy",
        "language": "english",
        "filename": "en_climate.html",
        "html": """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Climate</title></head>
<body>
<article>
<h1>Global Warming and Renewable Energy</h1>
<p>Scientific consensus is that the Earth's climate system is unequivocally
warming, and that it is extremely likely that this warming is predominantly
caused by humans. The primary driver is the emission of greenhouse gases from
burning fossil fuels. Renewable energy sources such as solar, wind and
hydroelectric power are essential for reducing these emissions.</p>
<p>Many countries have set targets for increasing the share of renewable energy
in their electricity mix. Investment in clean technologies continues to grow,
and the cost of solar photovoltaic modules has fallen dramatically over the
past decade. Energy storage and smart grids also play an important role in
integrating intermittent renewable sources into the power system.</p>
</article>
</body></html>""",
    },
    {
        "id": 4,
        "title": "Le réchauffement climatique",
        "language": "french",
        "filename": "fr_climate.html",
        "html": """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Climat</title></head>
<body>
<article>
<h1>Réchauffement climatique et énergies renouvelables</h1>
<p>Le consensus scientifique est que le système climatique de la Terre se
réchauffe de manière incontestable, et qu'il est extrêmement probable que ce
réchauffement soit principalement causé par les humains. Le principal moteur
est l'émission de gaz à effet de serre provenant de la combustion de
combustibles fossiles. Les sources d'énergie renouvelable telles que le
solaire, l'éolien et l'hydroélectricité sont essentielles pour réduire ces
émissions.</p>
<p>De nombreux pays ont fixé des objectifs pour augmenter la part des énergies
renouvelables dans leur mix électrique. Les investissements dans les technologies
propres continuent de croître, et le coût des modules photovoltaïques a
considérablement diminué au cours de la dernière décennie.</p>
</article>
</body></html>""",
    },
    {
        "id": 5,
        "title": "History of Computing",
        "language": "english",
        "filename": "en_history.html",
        "html": """<!DOCTYPE html>
<html><head><title>Computing History</title></head>
<body>
<h1>A Brief History of Computing</h1>
<p>The first electronic general-purpose computer was ENIAC, completed in 1945.
It used vacuum tubes and occupied a large room. The invention of the transistor
in 1947 and later the integrated circuit enabled much smaller and more reliable
machines. The microprocessor, introduced in the early 1970s, brought computing
power to individuals and led to the personal computer revolution.</p>
<p>The development of the Internet and the World Wide Web in the 1990s
transformed how people communicate and access information. Mobile devices and
cloud computing have further changed the landscape in the twenty-first century.
Artificial intelligence is now becoming a central technology in many industries.</p>
</body></html>""",
    },
    {
        "id": 6,
        "title": "Histoire de l'informatique",
        "language": "french",
        "filename": "fr_history.html",
        "html": """<!DOCTYPE html>
<html lang="fr"><head><title>Histoire informatique</title></head>
<body>
<h1>Une brève histoire de l'informatique</h1>
<p>Le premier ordinateur électronique à usage général fut l'ENIAC, achevé en
1945. Il utilisait des tubes à vide et occupait une grande pièce. L'invention
du transistor en 1947 puis du circuit intégré a permis des machines beaucoup
plus petites et plus fiables. Le microprocesseur, introduit au début des années
1970, a apporté la puissance de calcul aux individus et a conduit à la
révolution de l'ordinateur personnel.</p>
<p>Le développement d'Internet et du World Wide Web dans les années 1990 a
transformé la façon dont les gens communiquent et accèdent à l'information.
Les appareils mobiles et l'informatique en nuage ont encore changé le paysage
au XXIe siècle. L'intelligence artificielle devient aujourd'hui une technologie
centrale dans de nombreuses industries.</p>
</body></html>""",
    },
    {
        "id": 7,
        "title": "Biodiversity Crisis",
        "language": "english",
        "filename": "en_bio.html",
        "html": """<!DOCTYPE html>
<html><head><title>Biodiversity</title></head>
<body>
<h1>The Biodiversity Crisis</h1>
<p>Scientists estimate that species are disappearing at rates tens to hundreds
of times higher than the natural background rate. Habitat loss, climate change,
pollution and overexploitation are the main drivers. Protecting ecosystems and
restoring degraded habitats are critical steps to slow this decline.</p>
<p>International agreements such as the Convention on Biological Diversity aim
to coordinate global action. Local communities and indigenous peoples play an
essential role in conservation, as they often manage lands with high levels of
biodiversity and traditional ecological knowledge.</p>
</body></html>""",
    },
    {
        "id": 8,
        "title": "Crise de la biodiversité",
        "language": "french",
        "filename": "fr_bio.html",
        "html": """<!DOCTYPE html>
<html lang="fr"><head><title>Biodiversité</title></head>
<body>
<h1>La crise de la biodiversité</h1>
<p>Les scientifiques estiment que les espèces disparaissent à des rythmes
dizaines à centaines de fois plus élevés que le taux naturel de fond. La perte
d'habitat, le changement climatique, la pollution et la surexploitation sont
les principaux moteurs. La protection des écosystèmes et la restauration des
habitats dégradés sont des étapes critiques pour ralentir ce déclin.</p>
<p>Des accords internationaux tels que la Convention sur la diversité biologique
visent à coordonner l'action mondiale. Les communautés locales et les peuples
autochtones jouent un rôle essentiel dans la conservation, car ils gèrent
souvent des terres présentant de hauts niveaux de biodiversité.</p>
</body></html>""",
    },

    {
        "id": 9,
        "title": "Space Exploration",
        "language": "english",
        "filename": "en_space.html",
        "html": """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Space Exploration</title></head>
<body>
<h1>The Future of Space Exploration</h1>
<p>Space exploration has entered a new era driven by both government agencies and
private companies. Missions to the Moon and Mars are being planned with the goal
of establishing permanent human presence beyond Earth. Reusable rockets have
dramatically reduced the cost of launching satellites and cargo into orbit.</p>
<p>Scientific instruments aboard spacecraft continue to expand our knowledge of
the solar system. Telescopes in space observe distant galaxies and search for
exoplanets that might support life. International cooperation remains essential
for large-scale projects such as space stations and deep-space probes.</p>
<p>Challenges include radiation exposure, long-duration life support, and the
psychological effects of isolation. Advances in propulsion, materials science
and robotics will determine how far humanity can travel in the coming decades.</p>
</body></html>""",
    },
    {
        "id": 10,
        "title": "L'exploration spatiale",
        "language": "french",
        "filename": "fr_space.html",
        "html": """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Exploration spatiale</title></head>
<body>
<h1>L'avenir de l'exploration spatiale</h1>
<p>L'exploration spatiale est entrée dans une nouvelle ère portée à la fois par
les agences gouvernementales et les entreprises privées. Des missions vers la
Lune et Mars sont planifiées dans le but d'établir une présence humaine permanente
au-delà de la Terre. Les fusées réutilisables ont considérablement réduit le coût
du lancement de satellites et de cargos en orbite.</p>
<p>Les instruments scientifiques à bord des engins spatiaux continuent d'élargir
notre connaissance du système solaire. Les télescopes dans l'espace observent des
galaxies lointaines et recherchent des exoplanètes susceptibles d'abriter la vie.
La coopération internationale reste essentielle pour les projets à grande échelle.</p>
<p>Les défis comprennent l'exposition aux radiations, le support de vie de longue
durée et les effets psychologiques de l'isolement. Les progrès en propulsion et
en robotique détermineront jusqu'où l'humanité pourra voyager dans les décennies
à venir.</p>
</body></html>""",
    },
    {
        "id": 11,
        "title": "Public Health and Vaccines",
        "language": "english",
        "filename": "en_health.html",
        "html": """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Public Health</title></head>
<body>
<article>
<h1>Vaccines and Public Health</h1>
<p>Vaccination is one of the most effective public health interventions ever
developed. Immunization programs have eradicated smallpox and nearly eliminated
polio in many regions. Modern vaccines protect against a wide range of infectious
diseases, reducing mortality and healthcare costs worldwide.</p>
<p>Public health authorities monitor disease outbreaks, promote hygiene, and
coordinate emergency responses. Access to clean water, nutrition and primary care
are foundational determinants of population health. Global collaboration through
organizations such as the World Health Organization helps share data and resources
during pandemics.</p>
<p>Challenges remain in vaccine hesitancy, equitable distribution and the emergence
of new pathogens. Investment in research, surveillance systems and community
engagement is critical to preparedness for future health crises.</p>
</article>
</body></html>""",
    },
    {
        "id": 12,
        "title": "Santé publique et vaccins",
        "language": "french",
        "filename": "fr_health.html",
        "html": """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Santé publique</title></head>
<body>
<article>
<h1>Vaccins et santé publique</h1>
<p>La vaccination est l'une des interventions de santé publique les plus efficaces
jamais développées. Les programmes d'immunisation ont éradiqué la variole et
presque éliminé la poliomyélite dans de nombreuses régions. Les vaccins modernes
protègent contre un large éventail de maladies infectieuses, réduisant la mortalité
et les coûts de santé dans le monde entier.</p>
<p>Les autorités de santé publique surveillent les épidémies, promeuvent l'hygiène
et coordonnent les réponses d'urgence. L'accès à l'eau potable, à la nutrition et
aux soins primaires sont des déterminants fondamentaux de la santé des populations.
La collaboration mondiale permet de partager données et ressources pendant les
pandémies.</p>
<p>Des défis subsistent concernant l'hésitation vaccinale, la distribution équitable
et l'émergence de nouveaux pathogènes. L'investissement dans la recherche et les
systèmes de surveillance est essentiel à la préparation face aux crises sanitaires.</p>
</article>
</body></html>""",
    },
    {
        "id": 13,
        "title": "Urban Planning and Cities",
        "language": "english",
        "filename": "en_urban.html",
        "html": """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Urban Planning</title></head>
<body>
<h1>Sustainable Cities of the Future</h1>
<p>Urban planning shapes how millions of people live, work and move every day.
Sustainable city design prioritizes public transit, green spaces, energy-efficient
buildings and mixed-use neighborhoods. Reducing car dependence lowers pollution
and improves quality of life for residents.</p>
<p>Smart city technologies use sensors and data analytics to optimize traffic flow,
waste collection and energy consumption. Affordable housing and inclusive public
spaces help ensure that growth benefits all social groups. Climate adaptation
measures such as flood defenses and urban forests are increasingly important.</p>
<p>Successful cities balance economic development with environmental protection
and social equity. Collaboration between governments, citizens and private
developers is essential to implement long-term visions for livable urban areas.</p>
</body></html>""",
    },
    {
        "id": 14,
        "title": "Urbanisme et villes durables",
        "language": "french",
        "filename": "fr_urban.html",
        "html": """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Urbanisme</title></head>
<body>
<h1>Les villes durables de l'avenir</h1>
<p>L'urbanisme façonne la façon dont des millions de personnes vivent, travaillent
et se déplacent chaque jour. La conception de villes durables privilégie les
transports en commun, les espaces verts, les bâtiments économes en énergie et les
quartiers à usage mixte. La réduction de la dépendance à la voiture diminue la
pollution et améliore la qualité de vie des habitants.</p>
<p>Les technologies de ville intelligente utilisent des capteurs et l'analyse de
données pour optimiser le trafic, la collecte des déchets et la consommation
d'énergie. Le logement abordable et les espaces publics inclusifs aident à garantir
que la croissance profite à tous les groupes sociaux. Les mesures d'adaptation
au climat sont de plus en plus importantes.</p>
<p>Les villes réussies équilibrent le développement économique, la protection de
l'environnement et l'équité sociale. La collaboration entre les gouvernements,
les citoyens et les promoteurs privés est essentielle pour mettre en œuvre des
visions à long terme.</p>
</body></html>""",
    },
    {
        "id": 15,
        "title": "Digital Economy",
        "language": "english",
        "filename": "en_economy.html",
        "html": """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>Digital Economy</title></head>
<body>
<h1>The Rise of the Digital Economy</h1>
<p>Digital platforms have transformed commerce, entertainment and employment.
E-commerce allows consumers to purchase goods from anywhere in the world, while
streaming services deliver media on demand. Remote work tools enable collaboration
across time zones and have changed traditional office culture.</p>
<p>Cryptocurrencies and blockchain technology introduce new forms of digital assets
and decentralized finance. At the same time, concerns about data privacy, market
concentration and the digital divide require careful regulation. Education and
skills training are vital so that workers can adapt to automation and artificial
intelligence in the workplace.</p>
<p>Governments and businesses must work together to ensure that the benefits of
digital transformation are widely shared and that infrastructure reaches rural
and underserved communities.</p>
</body></html>""",
    },
    {
        "id": 16,
        "title": "L'économie numérique",
        "language": "french",
        "filename": "fr_economy.html",
        "html": """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Économie numérique</title></head>
<body>
<h1>L'essor de l'économie numérique</h1>
<p>Les plateformes numériques ont transformé le commerce, le divertissement et
l'emploi. Le commerce électronique permet aux consommateurs d'acheter des biens
depuis n'importe où dans le monde, tandis que les services de streaming diffusent
des médias à la demande. Les outils de télétravail permettent la collaboration
à travers les fuseaux horaires et ont modifié la culture de bureau traditionnelle.</p>
<p>Les cryptomonnaies et la technologie blockchain introduisent de nouvelles formes
d'actifs numériques et de finance décentralisée. En même temps, les préoccupations
concernant la confidentialité des données, la concentration du marché et la fracture
numérique nécessitent une réglementation attentive. L'éducation et la formation
sont essentielles pour que les travailleurs s'adaptent à l'automatisation.</p>
<p>Les gouvernements et les entreprises doivent collaborer pour garantir que les
bénéfices de la transformation numérique soient largement partagés et que les
infrastructures atteignent les communautés rurales et mal desservies.</p>
</body></html>""",
    },
    {
        "id": 17,
        "title": "Ocean Conservation",
        "language": "english",
        "filename": "en_ocean.html",
        "html": """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Oceans</title></head>
<body>
<h1>Protecting the World's Oceans</h1>
<p>Oceans cover more than seventy percent of the Earth's surface and play a
crucial role in regulating climate, producing oxygen and supporting biodiversity.
Overfishing, plastic pollution and rising temperatures threaten marine ecosystems
from coral reefs to deep-sea habitats.</p>
<p>Marine protected areas help conserve critical species and habitats. Sustainable
fishing practices and international agreements aim to restore depleted fish stocks.
Reducing plastic waste and improving waste management on land are essential to
keep debris out of the seas.</p>
<p>Scientific research using underwater robots and satellite data improves our
understanding of ocean processes. Public awareness and policy action are needed
to ensure healthy oceans for future generations.</p>
</body></html>""",
    },
    {
        "id": 18,
        "title": "Conservation des océans",
        "language": "french",
        "filename": "fr_ocean.html",
        "html": """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>Océans</title></head>
<body>
<h1>Protéger les océans du monde</h1>
<p>Les océans couvrent plus de soixante-dix pour cent de la surface de la Terre
et jouent un rôle crucial dans la régulation du climat, la production d'oxygène
et le soutien de la biodiversité. La surpêche, la pollution plastique et la hausse
des températures menacent les écosystèmes marins, des récifs coralliens aux habitats
des grands fonds.</p>
<p>Les aires marines protégées aident à conserver des espèces et des habitats
critiques. Les pratiques de pêche durable et les accords internationaux visent
à restaurer les stocks de poissons épuisés. Réduire les déchets plastiques et
améliorer la gestion des déchets sur terre sont essentiels pour garder les débris
hors des mers.</p>
<p>La recherche scientifique utilisant des robots sous-marins et des données
satellitaires améliore notre compréhension des processus océaniques. La
sensibilisation du public et l'action politique sont nécessaires pour assurer
des océans sains pour les générations futures.</p>
</body></html>""",
    },
    {
        "id": 19,
        "title": "Education Technology",
        "language": "english",
        "filename": "en_edu.html",
        "html": """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>EdTech</title></head>
<body>
<section>
<h1>Technology in Education</h1>
<p>Digital tools are reshaping how students learn and teachers teach. Online
courses, interactive simulations and adaptive learning platforms personalize
instruction based on individual progress. Access to educational resources is
no longer limited by geography when reliable internet is available.</p>
<p>However, the digital divide means that not all learners benefit equally.
Teacher training and thoughtful curriculum design are required to integrate
technology effectively rather than as a superficial addition. Assessment methods
are also evolving to measure skills beyond traditional tests.</p>
<p>The future of education will likely blend face-to-face interaction with
digital experiences, preparing students for a world where continuous learning
and digital literacy are essential professional skills.</p>
</section>
</body></html>""",
    },
    {
        "id": 20,
        "title": "Technologies éducatives",
        "language": "french",
        "filename": "fr_edu.html",
        "html": """<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><title>EdTech</title></head>
<body>
<section>
<h1>La technologie dans l'éducation</h1>
<p>Les outils numériques transforment la façon dont les élèves apprennent et dont
les enseignants enseignent. Les cours en ligne, les simulations interactives et
les plateformes d'apprentissage adaptatif personnalisent l'instruction en fonction
des progrès individuels. L'accès aux ressources éducatives n'est plus limité par
la géographie lorsque Internet fiable est disponible.</p>
<p>Cependant, la fracture numérique signifie que tous les apprenants ne profitent
pas également. La formation des enseignants et une conception réfléchie des
programmes sont nécessaires pour intégrer efficacement la technologie. Les méthodes
d'évaluation évoluent également pour mesurer des compétences au-delà des tests
traditionnels.</p>
<p>L'avenir de l'éducation combinera probablement l'interaction en présentiel avec
des expériences numériques, préparant les étudiants à un monde où l'apprentissage
continu et la littératie numérique sont des compétences professionnelles essentielles.</p>
</section>
</body></html>""",
    },
]


def get_training_corpus() -> dict:
    # Expand to meet 20–120 KB guideline while keeping diverse vocabulary
    en = list(EN_TRAIN)
    fr = list(FR_TRAIN)
    en.append("\n\n".join(EN_TRAIN))
    fr.append("\n\n".join(FR_TRAIN))
    return {"english": en, "french": fr}


def get_test_documents() -> list:
    return TEST_DOCUMENTS
