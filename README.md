# 🚀 Démo : Dynamic Knowledge Graph (DKG) Cybersécurité

---

## 🎯 Objectifs

Objectif du projet : Mettre en place un "Framework" de développement d'un Agent IA basé sur le "Dynamique Knowledge Graph" qui soit didactique.  
Pour cela il doit présenter les concepts et les étapes pour pouvoir être adapté a d'autres cas d'usages et contextes.  
Il faut pouvoir développer une liste d'exigences de ce projets que nous partagions comme :  
- Identifier et mettre en oeuvre les données publique comme les standards et les communs pour être pertinent et efficace
- Assurer la confidentialité des données internes privée (avec différents niveaux de confidentialité). 
  Ce projet (POC ) simule les données privées avec l'étiquette "pseudo-confidentielle" pour satisfaire le besoin didactique. Mais explicite ajustement a faire pour accéder a cette confidentialité.  
- l'agent doit pouvoir tourner en local sur une machine ACER Aspire 515-40 avec 16Go RAM et peut faire a ppel a des ressource cloud pour le fine tuning de modèle si nécessaire.
Générer des spécification qui permettent de façiliter la maintenance et l'adaptation a d'autre contexte et cas d'usages

Créer un démonstrateur de mise en oeuvre d'un **assistant IA** utilisant un Graphe de connaissance dynamique. (**Dynamic Knowledge Graph**)

**→ Le graphe de connaissances** se base sur une **ontologie** (cœur de la structure de connaissance).
-> Il est associé à un **lexique**  **[Lexique](./LEXIQUE.md)** pour une compréhension commune des termes (ontologie, KG, règles, etc.).
**→ L’aspect dynamique** est crucial : le graphe évolue continûment avec pour socle une ontologie et un lexique contrôlés.


Cette ontologie et ce lexique sont des références pour le système agentique, tant pour l'agent que pour les humains. . 
Il existent dans un version humaine (.md) et dans une version machine (.ttl)
Les modification du lexique( .md)  vont se répercuter sur la version (.ttl)
pour l'ontologie seule la version ttl fait reference, le md en est extrait.

Ce projet a aussi un objectif didactique, il tente de développer les principes sur un cas d'usage cybersecurité dans un cas individuel dans un premier temps, puis étendu a une petite entreprise pour illustrer l'aspect dynamique :  



---

## 📖 Développement du cas d'usage

Le use case présente des phase qui permettent d'illustrer comment l'ensemble évolue. Ces phases nécessitent la préparation de données générées sur la base de l'histoire du cas d'usage. 

Ces évolutions peuvent être de simple ajout d'instance au graph de connaissance existant, mais elles peuvent aussi impacter le cadre semantique/lexical et  ontologique, jusqu'a nécessiter un mise a niveau des outils de l'agent ( NER , embeddings...)

Pour comprendre **pourquoi et comment** ce projet a évolué, lisez :
→ [📖 Histoire d'Alban et la Gestion des Vulnérabilités](../01-CasUsage/DESCRIPTION.md)

## Phases :
[Workflow](../10-Projet/PhasesProjet.md)


> 💡 **L’enjeu** : Illustrer une évolution maitrisée d'un graphe de connaissance sous le controle d'une ontologie et d'un lexique, permettand de **développer les nuances du contexte**.

---

## 🏗 Principes et Architecture
un répertoire est dédié aux principes et Architecture afin de les développer dans le cadre du projet

**Principes clés** :
- **TBoxe**  _(Terminological Box)_ : Ontologies + Lexiques : 
  Schéma formel du domaine définissant le vocabulaire, les concepts (Classes), leurs hiérarchies (Sous-classes) et les règles d'association (Propriétés/Relations). C'est le contrat de structure immuable du graphe.
	- **Ontologie** : Schéma du graphe (classes, propriétés, relations) accessible aux profils non technique garant de l'explicabilité
	- **Lexique** : cadre sémantique du projet, intégré au fine tuning des outils de l'agent
- **ABox**  _(Assertional Box)_ : Données réelles / Instances 
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

## 💻 Hypothèses Matérielles

| Ressource                                    | Usage                      | Exemple                                   |
| -------------------------------------------- | -------------------------- | ----------------------------------------- |
| **PC local** (ACER ASPIRE A515-40, 16Go RAM) | Développement, inférences  | Exécution de Neo4j, scripts Python        |
| **Cloud GPU** (si besoin)                    | Fine-tuning de modèles NLP | Entraînement de modèles de classification |

**Objectif** : Pouvoir effectuer les **inférences sur le PC local**.

Preserver l'espace des repertoires racine => créer un répertoire pour HF dans l'espace /data/

```
# 1. Créer le dossier sur votre partition de données
mkdir -p /data/SyncData/Projets/T2C_1/hf_cache

# 2. Exporter la variable d'environnement (valable pour la session courante)
export HF_HOME=/data/SyncData/Projets/T2C_1/hf_cache
```

## 📁 Structure du Projet



