"""
Тестовая коллекция, вариант 7:
  языки — English, French
  области — computer science, literature essays
"""

from __future__ import annotations

DOCUMENTS = [
    {
        "id": "en_cs_1",
        "title": "Neural Networks and Deep Learning",
        "language": "english",
        "domain": "computer science",
        "text": """
Neural networks are computing systems inspired by biological neural networks.
A neural network consists of layers of interconnected nodes called neurons.
Each connection has a weight that is adjusted during learning. Deep learning
refers to neural networks with many hidden layers. These models have achieved
remarkable results in computer vision, speech recognition and natural language
processing.

Training a neural network typically relies on backpropagation and gradient
descent. The loss function measures the difference between predicted and true
outputs. Optimization algorithms such as stochastic gradient descent update
weights iteratively. Regularization techniques including dropout and weight
decay help prevent overfitting on limited training data.

Convolutional neural networks are particularly effective for image analysis.
They apply learnable filters across spatial dimensions. Pooling layers reduce
spatial resolution while retaining important features. Residual connections
allow very deep architectures to be trained successfully. Transfer learning
enables reuse of pretrained models on new tasks with smaller datasets.

Recurrent neural networks process sequential data by maintaining a hidden state.
Long short-term memory units address the vanishing gradient problem. Attention
mechanisms and transformers have largely replaced recurrent models for many
sequence tasks. Large language models based on transformers demonstrate strong
generalization across diverse language understanding problems.

Practical deployment of deep learning systems requires careful consideration of
computational cost, data quality and ethical implications. Model compression and
quantization reduce inference latency on edge devices. Continual learning remains
an open research challenge when data distributions shift over time.
""",
    },
    {
        "id": "fr_cs_1",
        "title": "Réseaux de neurones et apprentissage profond",
        "language": "french",
        "domain": "computer science",
        "text": """
Les réseaux de neurones sont des systèmes de calcul inspirés des réseaux
neuronaux biologiques. Un réseau de neurones est composé de couches de nœuds
interconnectés appelés neurones. Chaque connexion possède un poids ajusté
pendant l'apprentissage. L'apprentissage profond désigne les réseaux de neurones
comportant de nombreuses couches cachées. Ces modèles ont obtenu des résultats
remarquables en vision par ordinateur, en reconnaissance vocale et en traitement
du langage naturel.

L'entraînement d'un réseau de neurones s'appuie généralement sur la rétropropagation
et la descente de gradient. La fonction de perte mesure l'écart entre les sorties
prédites et les sorties réelles. Les algorithmes d'optimisation tels que la
descente de gradient stochastique mettent à jour les poids de manière itérative.
Les techniques de régularisation, notamment le dropout, aident à éviter le
surapprentissage sur des données limitées.

Les réseaux de neurones convolutifs sont particulièrement efficaces pour l'analyse
d'images. Ils appliquent des filtres apprenables sur les dimensions spatiales.
Les couches de pooling réduisent la résolution tout en conservant les
caractéristiques importantes. Les connexions résiduelles permettent d'entraîner
des architectures très profondes. L'apprentissage par transfert réutilise des
modèles préentraînés sur de nouvelles tâches.

Les réseaux de neurones récurrents traitent des données séquentielles en
maintenant un état caché. Les mécanismes d'attention et les transformeurs ont
largement remplacé les modèles récurrents pour de nombreuses tâches. Les grands
modèles de langage fondés sur les transformeurs montrent une forte capacité de
généralisation. Le déploiement pratique exige de prendre en compte le coût de
calcul, la qualité des données et les implications éthiques.
""",
    },
    {
        "id": "en_cs_2",
        "title": "Distributed Systems Overview",
        "language": "english",
        "domain": "computer science",
        "text": """
A distributed system is a collection of independent computers that appears to
its users as a single coherent system. Nodes communicate by exchanging messages
over a network. Key challenges include concurrency, partial failures and the
absence of a global clock. Designers must reason carefully about consistency,
availability and partition tolerance.

Replication improves fault tolerance and read scalability. Consistency models
range from strong linearizability to eventual consistency. Consensus protocols
such as Paxos and Raft allow a group of nodes to agree on a shared state despite
failures. Leader election and log replication are central building blocks of
modern coordination services.

Sharding partitions data across machines to handle large volumes. Load balancing
distributes requests to avoid hotspots. Caching reduces latency for frequently
accessed objects. Observability through metrics, logs and traces is essential
for operating large production systems. Security considerations include mutual
authentication, encryption in transit and access control.

Cloud platforms provide elastic resources for distributed applications. Microservices
architectures decompose systems into independently deployable components. Service
meshes manage traffic routing and policy enforcement. Understanding fundamental
distributed systems principles remains critical even as tooling evolves rapidly.
""",
    },
    {
        "id": "fr_cs_2",
        "title": "Systèmes distribués",
        "language": "french",
        "domain": "computer science",
        "text": """
Un système distribué est un ensemble d'ordinateurs indépendants qui apparaît à
ses utilisateurs comme un système cohérent unique. Les nœuds communiquent en
échangeant des messages sur un réseau. Les défis principaux comprennent la
concurrence, les défaillances partielles et l'absence d'horloge globale. Les
concepteurs doivent raisonner sur la cohérence, la disponibilité et la tolérance
aux partitions.

La réplication améliore la tolérance aux pannes et la scalabilité en lecture.
Les modèles de cohérence vont de la linéarisabilité forte à la cohérence à terme.
Les protocoles de consensus tels que Paxos et Raft permettent à un groupe de nœuds
de s'accorder sur un état partagé malgré les défaillances. L'élection d'un leader
et la réplication de journaux sont des éléments centraux des services de
coordination modernes.

Le partitionnement répartit les données sur plusieurs machines pour traiter de
grands volumes. l'équilibrage de charge évite les points chauds. La mise en cache
réduit la latence pour les objets fréquemment consultés. L'observabilité par
métriques, journaux et traces est essentielle pour l'exploitation. Les plateformes
cloud fournissent des ressources élastiques pour les applications distribuées.
Les architectures en microservices décomposent les systèmes en composants
déployables indépendamment.
""",
    },
    {
        "id": "en_lit_1",
        "title": "Essay: The Role of Memory in Literature",
        "language": "english",
        "domain": "literature",
        "text": """
Memory shapes the way stories are told and understood. Authors often rely on
recollected experience to construct narrative voice. The reliability of memory
becomes a central theme when narrators revise the past. In many modern novels,
fragmented recollection mirrors the uncertainty of identity.

Classical literature already treated memory as a moral and philosophical force.
Epic poetry preserved collective history through oral performance. Later prose
fiction explored private recollection and its distortions. The tension between
what happened and what is remembered drives dramatic irony. Readers participate
by filling gaps left by incomplete testimony.

Contemporary writers experiment with nonlinear chronology. Scenes return with
altered emphasis, suggesting that memory is creative rather than archival.
Trauma narratives in particular show how recollection resists simple chronology.
Literary form itself becomes a metaphor for the workings of the mind. Through
such devices, fiction investigates how individuals and communities sustain a
sense of continuity across time.
""",
    },
    {
        "id": "fr_lit_1",
        "title": "Essai : la mémoire dans la littérature",
        "language": "french",
        "domain": "literature",
        "text": """
La mémoire façonne la manière dont les récits sont racontés et compris. Les
auteurs s'appuient souvent sur l'expérience ressouvenue pour construire une voix
narrative. La fiabilité de la mémoire devient un thème central lorsque les
narrateurs revisent le passé. Dans de nombreux romans modernes, le souvenir
fragmenté reflète l'incertitude de l'identité.

La littérature classique traitait déjà la mémoire comme une force morale et
philosophique. La poésie épique préservait l'histoire collective par la
performance orale. La prose fictionnelle a ensuite exploré le souvenir privé et
ses distorsions. La tension entre ce qui s'est produit et ce qui est rappelé
alimente l'ironie dramatique. Les lecteurs participent en comblant les lacunes
laissées par un témoignage incomplet.

Les écrivains contemporains expérimentent une chronologie non linéaire. Les
scènes reviennent avec une emphase modifiée, suggérant que la mémoire est
créative plutôt qu'archivistique. Les récits de traumatisme montrent comment le
souvenir résiste à une chronologie simple. La forme littéraire devient elle-même
une métaphore du fonctionnement de l'esprit. Par ces procédés, la fiction examine
comment les individus et les communautés maintiennent un sentiment de continuité.
""",
    },
    {
        "id": "en_lit_2",
        "title": "Essay: Landscape and Character",
        "language": "english",
        "domain": "literature",
        "text": """
Landscape in fiction is rarely a neutral backdrop. Setting influences character
motivation and symbolic meaning. Harsh environments may externalize internal
conflict. Pastoral scenes often encode ideals of harmony or loss. Writers select
details of place to guide the reader's emotional response.

In realist traditions, precise description anchors social critique. Industrial
cities become emblems of alienation. Rural spaces can represent either refuge or
stagnation depending on narrative perspective. Travel narratives turn geography
into a structure for personal transformation. The journey motif links spatial
movement with moral development.

Modernist and postcolonial texts further complicate the politics of place.
Maps, borders and names carry histories of power. Characters negotiate belonging
in contested spaces. Landscape description thus participates in broader arguments
about culture and identity. Careful attention to setting reveals how literature
imagines the relationship between people and the worlds they inhabit.
""",
    },
    {
        "id": "fr_lit_2",
        "title": "Essai : paysage et personnage",
        "language": "french",
        "domain": "literature",
        "text": """
Le paysage dans la fiction n'est presque jamais un décor neutre. Le cadre
influence la motivation des personnages et le sens symbolique. Les environnements
hostiles peuvent extérioriser un conflit intérieur. Les scènes pastorales
encodent souvent des idéaux d'harmonie ou de perte. Les écrivains choisissent
les détails du lieu pour orienter la réponse émotionnelle du lecteur.

Dans les traditions réalistes, la description précise ancre la critique sociale.
Les villes industrielles deviennent des emblèmes de l'aliénation. Les espaces
ruraux peuvent représenter un refuge ou une stagnation selon la perspective
narrative. Les récits de voyage font de la géographie une structure de
transformation personnelle. Le motif du voyage relie le déplacement spatial au
développement moral.

Les textes modernistes et postcoloniaux compliquent la politique du lieu. Les
cartes, les frontières et les noms portent des histoires de pouvoir. Les
personnages négocient l'appartenance dans des espaces contestés. La description
du paysage participe ainsi à des débats plus larges sur la culture et l'identité.
Une attention attentive au cadre révèle comment la littérature imagine le lien
entre les personnes et les mondes qu'elles habitent.
""",
    },
]


def get_documents():
    return DOCUMENTS


def get_document(doc_id: str):
    for d in DOCUMENTS:
        if d["id"] == doc_id:
            return d
    return None
