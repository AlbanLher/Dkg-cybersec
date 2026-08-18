

```
dkg-cybersec/

dkg-cybersec/
├── 00-Projet/
│   ├── README.md
│   ├── ROADMAP.md
│   ├── LEXIQUE.md                         # <-- Lexique ci-dessus
│   └── CHANGELOG.md
│
├── 01-CasUsage/
│   ├── DESCRIPTION.md
│   └── Donnees/
│       ├── PUBLIQUES.md                   # Sources publiques (CVE, MITRE)
│       └── PRIVEES.md                     # Schéma des données privées
│
├── 02-Architecture/
│   ├── ONTOLOGIE/
│   │   ├── ontologie-publique.ttl         # Classes/propriétés génériques
|   |   ├── ontologie-pseudo-privee.ttl    #  Ontologie "pseudo-privée" (POC uniquement)
│   │   ├── ontologie-regles.ttl           # Règles publiques (ex: liens CVE → Device)
│   │   └── SCHEMA.md                      # Schéma visuel (Mermaid)
│   ├── DECISIONS.md                       # Choix architecturaux
│   └── NEO4J.md                           # Configuration Neo4j/n10s
│
├── 03-Implementation/
│   ├── Phase0-Cadrage/                    # POC : 1 individu
│   │   ├── ONTOLOGIE/
│   │   │   └── ontologie.ttl              # Ontologie de base (Device, Software, Vulnerability)
│   │   ├── DESIGN.md                      # Design initial
│   │   ├── data/
│   │   │   ├── public/
│   │   │   │   ├── inventory.json
│   │   │   │   └── cve_data.ttl
│   │   │   └── pseudo-private/
│   │   │       └── rules.ttl
│   │   └── migrations/                    # Vide (pas de migration avant Phase0)
│   │
│   ├── Phase1-Infrastructure/             # Micro-entreprise
│   │   ├── ONTOLOGIE/
│   │   │   └── ontologie.ttl              # +InternalDevice, +ComplianceRule
│   │   ├── DESIGN.md                      # Design avec règles internes
│   │   ├── data/
│   │   │   ├── public/
│   │   │   │   ├── inventory-v2.json
│   │   │   │   └── cve_data-v2.ttl
│   │   │   └── pseudo-private/
│   │   │       └── rules-v2.ttl
│   │   └── migrations/
│   │       └── to_phase1.cypher           # Migration depuis Phase0
│   │
│   └── Phase2-Reglementaire/              # Startup + RGPD
│       ├── ONTOLOGIE/
│       │   └── ontologie.ttl              # +ExternalDevice, +Context, +Waiver
│       ├── DESIGN.md                      # Design avec contradictions résolues
│       ├── data/
│       │   ├── public/
│       │   │   ├── inventory-v3.json
│       │   │   └── cve_data-v3.ttl
│       │   └── pseudo-private/
│       │       └── rules-v3.ttl
│       └── migrations/
│           ├── to_phase2.cypher           # Migration depuis Phase1
│           └── resolve_conflict.cypher    # Résolution de la contradiction
│
└── data/                                  # Données centralisées
│   ├── current/                           # Liens vers la phase ACTUELLE (Phase0)
│   │   ├── public/         -> Phase0-Cadrage/data/public
│   │   └── pseudo-private/ -> Phase0-Cadrage/data/pseudo-private
│   └── Phase0-Cadrage/                    # Données de Phase0
│       ├── public/
│       │   ├── inventory.json
│       │   └── cve_data.ttl
│       └── pseudo-private/
│           └── rules.ttl
│           
│
└── .private/                             # non utilisée dans la premiere partie de ce POC
    ├── ontologie-privee.ttl              # Extensions spécifiques
    ├── regles-internes.ttl               # Règles internes (ex: RGPD)
    ├── donnees/
    │   ├── inventory-reel.json           # Inventaire réel
    │   └── cve_data.ttl                  # CVE privées (si applicable):w
    └── config/
        └── neo4j.conf                    # Config locale
```