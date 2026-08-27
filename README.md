# 🚀 Démo : Dynamic Knowledge Graph (DKG) Cybersécurité

---

## 🎯 Objectifs

Objectif du projet : Mettre en place un "Framework" de développement d'un Agent IA basé sur le "Dynamique Knowledge Graph" qui soit didactique.  
L'idée de base est la conviction du potentiel de ces concept mais aussi la difficulté a bien percevoir et implémenter tous les concepts qui la supportent, surtout dans un domaine ou il faut combiner le benefice que l'on peut attendre dees Standards et bien communs, mais aussi tous les enjeux de confidentialité qui s'imposent.

Le projet présenter les concepts et les étapes pour pouvoir être adapté a d'autres cas d'usages et contextes.  

Cette notion de framework sera développée grâce a un ensemble de spécification de développement, ainsi q'un certain nombre d'étapes reprises dans les phases du projet.
- Les spécifications sont capitalisées dans l'arborescence dans des repertoires sommés Specification*  { [Spec projet](./10-Projet/Specifications/ExigencesProjet.md), [Spec_Architecture](./11-Principes_Architecture/Specifications/SpecificationNormativeSortiesFormatsTBox.md), ....}
- Les étapes sont reprises dans les phases du projet  { [Phases](./10-Projet/PhasesProjet.md) }
  Dans chaque phase un petit résumé est présenté sous forme de md dans **./Eléments de la phase**

Une illustration de ce développement sera faite sur un cas d'usage  : un **assistant IA** utilisant un Graphe de connaissance dynamique. (**Dynamic Knowledge Graph**)



---

## 📖 Cas d'usage

Le use case présente une histoire qui permet d'illustrer la démarche. 
Cette histoire sert de base à la génération de données synthètiques permettant la mise en ouvre.
Elle se développer aux fur et a mesure des phases pour accompagner le développement progressif et didactique.

Elle doit aussi être continuement revue et adapter pour garantir une cohérence et 
Elle est détaillée → [ Détail du cas d'usage](../10-Projet/Use_Case.md)

## Phases :
[Workflow](../10-Projet/PhasesProjet.md)


> 💡 **L’enjeu** : Illustrer une évolution maitrisée d'un graphe de connaissance sous le controle d'une ontologie et d'un lexique, permettand de **développer les nuances du contexte**.

---

##   Principes et Architecture
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
## 🔒 Confidentialité : POC vs Production  -- A consolider
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

## 📁 Exigences_Projet

