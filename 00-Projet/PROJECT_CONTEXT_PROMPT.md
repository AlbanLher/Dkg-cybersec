
Ce document constitue la **source unique de vérité (SSOT)** pour les consignes système, les principes d'architecture et la méthode de travail applicables par l'agent IA et l'équipe de développement.


##  Prompt de Contexte & Guide de Gouvernance

* **Rôle** : Architecte IA et co-développeur d'un framework  pour développer un Agent IA basé sur un Knowledge Graph  Dynamique, appliqué au cas d'usage Cybersécurité décrit dans le [UseCase](./00-Projet/Use_Case.md).
* L'ensemble des concepts et fonctionnalités du dévelopement itératif de ce Framework sont présentés dans  : [./00-Projet/PhasesProjet.md](PhasesProjet.md)] associés aux phases quant il ont étés développés ou dans la liste backlog. 
* **Chaque Phase comporte 5 étapes  :**
	1. **Cadrage & Contexte (`00-Projet/Phase_X/Phase_Context.md`)** : Rappel des concepts, périmètre et livrables cibles.
	2. **Spécifications (`01-Principes_Architecture_Specifications/`)** : Formalisation des exigences fonctionnelles et techniques.
	3. **Sourcing des Données (`02-Donnees/`)** : Identification des sources, caches externes ou snapshots nécessaires.
	4. **Développement & Nommage (`03-Application/`)** : Écriture des scripts selon le nommage explicite de la phase.
	5. **Qualification & Recette (`03-Application/` ou `tests/`)** : Implémentation de la suite de tests (`test_*.py`) adossée aux exigences.

- Le contenu de chaque Phase est détallé dans **../00-Projet/Phase#/Phase_Content.md**
- **Knowledge confidentielle associées au données publique avec la gouvernance TLP** : 
	- `TLP:AMBER` : Modèle de données canonique, règles métier et validation SHACL. 
	- `TLP:RED` : Données de cartographie interne de l'infrastructure et du SI. 
	- `TLP:CLEAR` : Référentiels publics externes (CVE, CWE, CAPEC, NVD). 
- **Collaboration Homme - Machine** : Tout composant Master doit être décliné en triple format : Turtle (`.ttl`), JSON-LD (`.json`) et Documentation Markdown (`.md`). 
- **Spec driven** 
	- la spec projet a impérativement appliquer sont : [spec projet](./Specifications/ExigencesProjet)
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