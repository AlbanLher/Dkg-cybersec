# DKG Cybersécurité - Démonstrateur

**Objectif** : Créer un Dynamic Knowledge Graph pour la gestion des vulnérabilités et règles de sécurité, évoluant d'un individu à une micro-entreprise.

**Les fonctionnalités  principales :**
- **Détecter** les vulnérabilités (CVE) sur des devices/logiciels.
- **Appliquer** des règles de sécurité adaptées (ex: RGPD, NIS2).
- **Évoluer** dynamiquement avec l’ajout de nouveaux devices ou menaces.


# Cas d'Usage
Détection et correction de vulnérabilités (CVE, MITRE ATT&CK).

# Données :
  - Publiques : CVE, MITRE, OWASP.
  - Privées : Inventaire des devices/logiciels (générés).

| Type          | Source                                     | Format    | Exemple                                  |
| ------------- | ------------------------------------------ | --------- | ---------------------------------------- |
| **Publiques** | [CVE CIRCL API](https://cve.circl.lu/api/) | JSON/RDF  | `cve:CVE-2023-1234`                      |
| **Publiques** | [MITRE ATT&CK](https://attack.mitre.org/)  | STIX/JSON | `mitre:TA0001`                           |
| **Privées**   | Générées localement                        | JSON/RDF  | `inventory-reel.json` (dans `.private/`) |


| Source       | Type     | Fréquence   | Script Associé          |
| ------------ | -------- | ----------- | ----------------------- |
| CVE (CIRCL)  | Publique | Quotidienne | `load_cve_feed.py`      |
| MITRE ATT&CK | Publique | Mensuelle   | À développer            |
| Inventaire   | Privé    | Ponctuelle  | `generate_inventory.py` |

# Outils :

| Outil                     | Usage                          | Lien                                                      | commentaire          |
| ------------------------- | ------------------------------ | --------------------------------------------------------- | -------------------- |
| **Neo4j**                 | Base de données de graphe      | [neo4j.com](https://neo4j.com/)                           | en local pour le POC |
| **RDFLib**                | Manipulation RDF en Python     | [rdflib.readthedocs.io](https://rdflib.readthedocs.io/)   |                      |
| **Sentence Transformers** | Vectorisation                  | [sbert.net](https://www.sbert.net/) ,  `all-MiniLM-L6-v2` |                      |
| **spaCy**                 | NER (Reconnaissance d’entités) | [spacy.io](https://spacy.io/)                             |                      |
| **Faker**                 | Génération de données fictives | [faker.readthedocs.io](https://faker.readthedocs.io/)     |                      |
| Ontologie                 | OWL/TTL + Protégé              |                                                           |                      |
| NER                       | SpaCy (modèle personalisé)     |                                                           |                      |




## 🔗 Liens Utiles
- [Dépôt GitHub](https://github.com/alban-lhermine/dkg-cybersec)
- [Neo4j Docs](https://neo4j.com/docs/)
- [MITRE ATT&CK](https://attack.mitre.org/)


# structure

```text

Dkg-cybersec/
├── .gitignore                  # Exclut .private/, fichiers temporaires
├── 00-Projet/                  # Documentation globale
│   ├── README.md               # Ce fichier
│   ├── ROADMAP.md              # Feuille de route
│   └── CHANGELOG.md            # Historique des changements
├── 01-CasUsage/                # Cas d'usage et données
│   ├── DESCRIPTION.md          # Détail du cas cybersécurité
│   └── Donnees/
│       ├── PUBLIQUES.md        # Sources publiques (CVE, MITRE)
│       └── PRIVEES.md          # Schéma des données privées
├── 02-Architecture/            # Architecture technique
│   ├── SCHEMA.md               # Schémas (Mermaid)
│   ├── ONTOLOGIE/
│   │   └── ontologie-v1.0.ttl  # Ontologie RDF/OWL
│   └── PIPELINE.md             # Flux de données
└── 03-Implementation/          # Code et scripts
    └── Phase0-Cadrage/
        └── scripts/
            ├── generate_inventory.py  # Génère un inventaire fictif
            └── load_cve_feed.py        # Charge les CVE depuis CIRCL API

```


