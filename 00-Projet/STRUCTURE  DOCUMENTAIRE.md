
```
dkg-cybersec/
├── 00-Projet/
│   ├── README.md
│   ├── ROADMAP.md
│   ├── LEXIQUE.md                # <-- Lexique ci-dessus
│   └── CHANGELOG.md
│
├── 01-CasUsage/
│   ├── DESCRIPTION.md
│   └── Donnees/
│       ├── PUBLIQUES.md           # Sources publiques (CVE, MITRE)
│       └── PRIVEES.md             # Schéma des données privées
│
├── 02-Architecture/
│   ├── ONTOLOGIE/
│   │   ├── ontologie-publique.ttl # Classes/propriétés génériques
|   |   ├── ontologie-pseudo-privee.ttl    #  Ontologie "pseudo-privée" (POC uniquement)
│   │   ├── ontologie-regles.ttl  # Règles publiques (ex: liens CVE → Device)
│   │   └── SCHEMA.md              # Schéma visuel (Mermaid)
│   ├── DECISIONS.md               # Choix architecturaux
│   └── NEO4J.md                   # Configuration Neo4j/n10s
│
├── 03-Implementation/
│   ├── Phase0-Cadrage/
│   │   ├── scripts/
│   │   │   ├── generate_inventory.py
│   │   │   ├── load_cve_feed.py
│   │   │   └── migrate_ontology.py # Nouveau : Migration entre versions
│   │   └── tests/                # Tests unitaires
│   └── Phase1-Infrastructure/
│       └── scripts/
│           └── load_all.py        # Charge ontologie + données
│
└── .private/
    ├── ontologie-privee.ttl       # Extensions spécifiques
    ├── regles-internes.ttl        # Règles internes (ex: RGPD)
    ├── donnees/
    │   ├── inventory-reel.json    # Inventaire réel
    │   └── cve_data.ttl           # CVE privées (si applicable)
    └── config/
        └── neo4j.conf             # Config locale
```

