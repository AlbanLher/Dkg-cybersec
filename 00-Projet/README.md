# 🚀 Démo : Dynamic Knowledge Graph (DKG) Cybersécurité

---
## 📌 Table des Matières
1. [🎯 Objectifs](#objectifs)
2. [📖 Histoire du Use Case](#histoire-du-use-case)
3. [🏗 Architecture](#architecture)
4. [🔒 Confidentialité : POC vs Production](#confidentialité)
5. [💻 Hypothèses Matérielles](#hypothèses-matérielles)
6. [📊 Données](#données)
7. [📁 Structure du Projet](#structure-du-projet)

---

## 🎯 Objectifs
Créer un démonstrateur de mise en oeuvre d'un **assistant IA** utilisant un Graphe de connaissance dynamique. (**Dynamic Knowledge Graph**)

**→ Le graphe de connaissances** se base sur une **ontologie** (cœur de la structure de connaissance).
-> Il est associé à un **lexique**  **[Lexique](./LEXIQUE.md)** pour une compréhension commune des termes (ontologie, KG, règles, etc.).
**→ L’aspect dynamique** est crucial : le graphe évolue continûment avec pour socle une ontologie et un lexique contrôlés.


Cette ontologie et ce lexique sont des références pour le système agentique, tant pour l'agent que pour les humains. . 
Il existent dans un version humaine (.md) et dans une version machine (.ttl)
Les modification du lexique( .md)  vont se répercuter sur la version (.ttl)
pour l'ontologie seule la version ttl fait reference, le md en est extrait.

Ce projet a aussi un objectif didactique, il tente de développer les principes sur un cas d'usage cyber individuel puis de petite structure :  
pour :
- **Détecter** les vulnérabilités (CVE) sur des devices/logiciels.
- **Appliquer** des règles de sécurité adaptées (ex: RGPD, NIS2).
- **Évoluer** dynamiquement avec l’ajout de nouveaux devices ou menaces.

Mais les principes et l'architecture peuvent d'adapter à d'autres contextes et cas d'usage


---

## 📖 Développement du cas d'usage

Le use case présente des phase qui permettent d'illustrer comment l'ensemble évolue. Ces phases nécessitent la préparation de données générées sur la base de l'histoire du cas d'usage. 

Ces évolutions peuvent être de simple ajout d'instance au graph de connaissance existant, mais elles peuvent aussi impacter le cadre semantique/lexical et  ontologique, jusqu'a nécessiter un mise a niveau des outils de l'agent ( NER , embeddings...)

Pour comprendre **pourquoi et comment** ce projet a évolué, lisez :
→ [📖 Histoire d'Alban et la Gestion des Vulnérabilités](../01-CasUsage/DESCRIPTION.md)

**Résumé des 3 phases** :

| Phase       | Contexte                | Enjeu                         | Objectif Pédagogique                       |
| ----------- | ----------------------- | ----------------------------- | ------------------------------------------ |
| **Phase 0** | 1 PC, 1 routeur         | Découverte des vulnérabilités | Présenter l’architecture de base.          |
| **Phase 1** | +2 employés, +1 serveur | Gestion des règles internes   | Comprendre le sens de l’ontologie.         |
| **Phase 2** | +1 client externe       | Contradiction apparente       | Résoudre via l’enrichissement du contexte. |

> 💡 **L’enjeu** : Illustrer une évolution maitrisée d'un graphe de connaissance sous le controle d'une ontologie et d'un lexique, permettand de **développer les nuances du contexte**.

---

## 🏗 Principes et Architecture
un répertoire est dédié aux principes et Architecture afin de les développer dans le cadre du projet

**Principes clés** :
- **Ontologie** : Schéma du graphe (classes, propriétés, relations) accessible aux profils non technique garant de l'explicabilité
- **Lexique** : cadre sémantique du projet, intégré au fine tuning des outils de l'agent
- **Données** : Instances concrètes (devices, CVE, règles).
- **Agents** : Série de fonctionnalité comme l'ajout de donnée la fourniture de rapport , sous controle humain quand nécessaire.

---
## 🔒 Confidentialité : POC vs Production
Le developpement de graph de connaissance interessent beaucoup d'organisation pour lesquels ces connaissance représente un savoir faire a protéger. Ce projet est publique et simule des données privie appelée pseudo-private, pour avoir une architecture qui puisse facilement adresser ce besoin de confidentiaité.

| Type                        | Statut dans le POC | Statut en Production  | Exemple                              |
| --------------------------- | ------------------ | --------------------- | ------------------------------------ |
| **Ontologie publique**      | ✅ Public           | ✅ Public              | `:Device`, `:Vulnerability`          |
| **Ontologie pseudo-privée** | 🟡 Public (POC)    | ❌ Privé (`.private/`) | `:InternalDevice`, `:ComplianceRule` |
| **Données publiques**       | ✅ Public           | ✅ Public              | CVE (MITRE), OWASP                   |
| **Données pseudo-privées**  | 🟡 Public (POC)    | ❌ Privé (`.private/`) | Inventaire fictif, règles internes   |
> ⚠️ **Note** : Dans ce POC, les données **pseudo-privées** sont publiques pour faciliter la collaboration.
> **En production**, elles seraient déplacées dans `.private/` et exclues de Git.

---
## 💻 Hypothèses Matérielles

| Ressource                                    | Usage                      | Exemple                                   |
| -------------------------------------------- | -------------------------- | ----------------------------------------- |
| **PC local** (ACER ASPIRE A515-40, 16Go RAM) | Développement, inférences  | Exécution de Neo4j, scripts Python        |
| **Cloud GPU** (si besoin)                    | Fine-tuning de modèles NLP | Entraînement de modèles de classification |

**Objectif** : Pouvoir effectuer les **inférences sur le PC local**.

---
## 📊 Données

| Source              | Type          | Format | Fréquence   | Script Associé          | Exemple                          |
| ------------------- | ------------- | ------ | ----------- | ----------------------- | -------------------------------- |
| **CVE**             | Publique      | TTL    | Quotidienne | `load_cve_feed.py`      | CVE-2023-1234                    |
| **MITRE ATT&CK**    | Publique      | JSON   | Mensuelle   | -                       | T1059 (Command-Line Interface)   |
| **OWASP Top 10**    | Publique      | CSV    | Annuelle    | -                       | A01:2021 (Broken Access Control) |
| **Inventaire**      | Pseudo-privée | JSON   | Ponctuelle  | `generate_inventory.py` | PC-Alban-POC                     |
| **Règles internes** | Pseudo-privée | TTL    | Ponctuelle  | -                       | `Compliance-CVSS-Low`            |

---
## 📁 Structure du Projet
```
dkg-cybersec/
├── 00-Projet/               # Documentation globale
│   ├── README.md           # 👈 Vous êtes ici
│   ├── LEXIQUE.md          # Définitions techniques
│   └── ROADMAP.md          # Feuille de route
│
├── 01-CasUsage/            # Histoire et cas d'usage
│   ├── DESCRIPTION.md      # Histoire d'Alban (3 phases)
│   ├── ONTOLOGIE..md      # Histoire d'Alban (3 phases)
│   └── LEXIQUE.md      # Histoire d'Alban (3 phases)

│
├── 02-Architecture/        # Conception
│   ├── ONTOLOGIE/          # Ontologies (TTL)
│   │   ├── ontologie.ttl   # Ontologie publique
│   │   └── ontologie-schema.md # Schéma Mermaid
│   │
│   ├── DESIGN.md           # Choix architecturaux
│   └── NEO4J.md            # Configuration Neo4j
│
└── 03-Implementation/      # Implémentation
└── Phase0-Cadrage/     # Phase 0 : POC basique
├── ONTOLOGIE/      # Ontologie spécifique
├── donnees/         # Données (public/pseudo-private)
├── scripts/        # Scripts Python
└── migrations/     # Scripts de migration (vide pour Phase 0)
```
