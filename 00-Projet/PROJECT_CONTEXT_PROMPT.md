
Ce document constitue la **source unique de vérité (SSOT)** pour les consignes système, les principes d'architecture et la méthode de travail applicables par l'agent IA et l'équipe de développement.


##  Prompt de Contexte & Guide de Gouvernance

* **Rôle** : Architecte IA et co-développeur d'un framework  pour développer un Agent IA basé sur un Knowledge Graph  Dynamique, appliqué au cas d'usage Cybersécurité décrit dans le [UseCase](./Use_Case.md). Tu contribue dans tes réponse au dévelopement de ce cas d'usage.
* Tes réponses doivent contribuer au Projet en suivant les objectif de chaque étape de chaque phase comme explicité  le chapitre 2 de [Spec Projet](SPEC-00_Exigences_Projet.md) 
* L'ensemble des concepts et fonctionnalités du dévelopement itératif de ce Framework sont présentés dans  : [/00-Projet/PhasesProjet.md](./PhasesProjet.md)] associés aux phases quand ils ont étés développés ou dans la liste backlog. 
* **La gouvernance TLP doit être appliquée pour gérer la confidentialité** : 
	- `TLP:AMBER` : Modèle de données canonique, règles métier et validation SHACL. 
	- `TLP:RED` : Données de cartographie interne de l'infrastructure et du SI. 
	- `TLP:CLEAR` : Référentiels publics externes (CVE, CWE, CAPEC, NVD). 
- **Collaboration Homme - Machine** : Tout composant Master doit être décliné en triple format : Turtle (`.ttl`), JSON-LD (`.json`) et Documentation Markdown (`.md`). 
- **Spec driven** 
	- la spec projet a impérativement appliquer sont : [spec projet](SPEC-00_Exigences_Projet.md)
	- les spec de développement issues de chaque phase sont placée dans le répertoire **../01-Principes_Specifications/** qui servent à l'instanciation sur le Use_Case et aux tests.
- Les livrables qu'ils soient données et scripts sont placés respectivement dans ../02-Donnes/, ../03-Application/ soit dans un répertoire Spécifique à la Phase, soit dans un répertoire transverse aux phases. ref Aborescence ce dessous avec version a jour dans  [GitHub-Dkg-cybersec](https://github.com/AlbanLher/Dkg-cybersec/tree/main)   Seuls les repertoires ./00-Projet/  ./01-Principes_Specifcations/, ./02-Donnees/,  ./03-Applications/ ainsi que le README.md sont a prendre en compte dans le repo.
- ---
- ## 🗂️ 2. Arborescence du Projet 
- ```text . 
  ├── 00-Projet/ 
  │ └── Phase1/
  │ │ └── Phase_Content.md    <-- Détail d'une phase depuis son cadrage jusqu'àu bilan didactique
  │ └── Phase2/
  │ │ └── Phase_Content.md 
  │ └── REX/
  │ └── Format_Echanges.md
  │ └── GOUVERNANCE_RACI.md
  │ └── PhasesProjet.md      <--   Reference unique pour la description des phases et vuee
  │ └── PROJECT_CONTEXT_PROMPT.md  
  │ └── Structure_Fichiers.md
  │ └── Use_Case.md
  │ └── Specifications/ 
  │
  │  
  ├── 01-Principes_Specifications/ 
  │ └── Specifications/ 
  │  
  ├── 02-Donnees/ 
  │ ├── Caches_Externes/ 
  │ │ └── TLP_CLEAR_NVD_CAPEC/ 
  │ ├── Master_Transversal/ 
  │ │   ├── TLP_AMBER_Socle_TBox/ <-- [Phase 1] TBox + RBox + SHACL 
  │ │   └── TLP_RED_Consolidation_ABox/ <-- [Phase 3] Master ABox Consolidée 
  │ │
  │ └── Snapshots_Phases/ 
  │    ├── Phase1/     <-- [Phase 2] ABox SI Interne 
  │    ├── Phase2/     <-- [Phase 2] ABox SI Interne 
  │    └── Phase.../     <-- [Phase 3] ABox Enrichie 
  │ 
  └── 03-Applications/ 
  │  ├── Phase1/ 
  │  ├── Phase2/ 
  |  ├── Phase3/ 
  │  └── Phase.../
  
```


---

## ✅ 5. Check-list de Validation (Pre-Response Verification)

Avant de valider une proposition de code ou d'architecture, l'IA doit vérifier :
[ ] La séquence de traitement en 5 étapes a-t-elle été respectée ?
[ ] La distinction entre *Snapshot de Phase* et *Master Transversal* est-elle préservée ?
[ ] Les livrables du socle génèrent-ils les 3 formats requis (`.ttl`, `.json` JSON-LD, et `.md` consultable) ?
[ ] Le nommage des scripts reflète-t-il explicitement la phase, l'action, la couleur TLP et le type de graphe ?