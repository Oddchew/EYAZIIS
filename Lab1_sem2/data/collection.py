"""Тестовая коллекция документов и экспертные оценки релевантности."""

DOCUMENTS = {
    1: {
        "title": "Introduction to Artificial Intelligence",
        "text": "Artificial intelligence is a branch of computer science that aims to create intelligent machines. AI systems can perform tasks that typically require human intelligence such as visual perception speech recognition decision making and language translation. Machine learning is a subset of AI that enables systems to learn from data.",
        "date": "2025-03-12",
    },
    2: {
        "title": "Machine Learning Fundamentals",
        "text": "Machine learning algorithms build a model based on sample data known as training data in order to make predictions or decisions without being explicitly programmed. Supervised learning unsupervised learning and reinforcement learning are the main types of machine learning. Neural networks are widely used in deep learning.",
        "date": "2025-04-01",
    },
    3: {
        "title": "Natural Language Processing",
        "text": "Natural language processing NLP is a field of artificial intelligence that focuses on the interaction between computers and humans through natural language. The ultimate objective of NLP is to read decipher understand and make sense of human languages in a valuable way. Sentiment analysis and machine translation are common NLP applications.",
        "date": "2025-05-18",
    },
    4: {
        "title": "Computer Networks and Protocols",
        "text": "A computer network is a set of computers sharing resources located on or provided by network nodes. Computers use common communication protocols over digital interconnections to communicate with each other. Local area networks LAN and wide area networks WAN are common types. TCP IP is the fundamental protocol suite of the internet.",
        "date": "2025-02-20",
    },
    5: {
        "title": "Database Management Systems",
        "text": "A database management system DBMS is software that interacts with end users applications and the database itself to capture and analyze data. A general purpose DBMS is designed to allow the definition creation querying update and administration of databases. SQL is the standard language for relational databases.",
        "date": "2025-06-07",
    },
    6: {
        "title": "Information Retrieval Systems",
        "text": "Information retrieval is the process of obtaining information system resources relevant to an information need from a collection of information resources. Searches can be based on full text or other content based indexing. Boolean retrieval is a classical model using logical operators AND OR and NOT.",
        "date": "2025-07-14",
    },
    7: {
        "title": "Deep Learning and Neural Networks",
        "text": "Deep learning is part of a broader family of machine learning methods based on artificial neural networks with representation learning. Learning can be supervised semi supervised or unsupervised. Deep neural networks have been applied to computer vision speech recognition and natural language processing with great success.",
        "date": "2025-08-22",
    },
    8: {
        "title": "Cybersecurity Basics",
        "text": "Cybersecurity is the practice of protecting systems networks and programs from digital attacks. These cyber attacks are usually aimed at accessing changing or destroying sensitive information. Firewalls encryption and intrusion detection systems are essential tools in cybersecurity. Authentication and authorization are critical components.",
        "date": "2025-09-03",
    },
    9: {
        "title": "Cloud Computing",
        "text": "Cloud computing is the on demand availability of computer system resources especially data storage and computing power without direct active management by the user. Large clouds often have functions distributed over multiple locations from central servers. Public private and hybrid clouds are the main deployment models.",
        "date": "2025-10-11",
    },
    10: {
        "title": "Software Engineering Principles",
        "text": "Software engineering is a systematic engineering approach to software development. A software engineer applies engineering principles to design develop maintain test and evaluate computer software. Agile methodology and DevOps practices are widely adopted in modern software engineering projects.",
        "date": "2025-11-05",
    },
}

# экспертные оценки: query -> set of relevant doc ids
RELEVANCE_JUDGMENTS = {
    "artificial intelligence OR machine learning": {1, 2, 3, 7},
    "network AND protocol": {4},
    "database OR sql": {5},
    "natural language processing": {3, 7},
    "cybersecurity AND encryption": {8},
    "cloud computing": {9},
    "deep learning AND neural": {2, 7},
    "software engineering": {10},
    "information retrieval OR boolean": {6},
    "ai AND learning NOT network": {1, 2, 7},
}
