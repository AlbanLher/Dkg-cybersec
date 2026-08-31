Le projet DKG-CyberSec  vise a proposer un Framework de développement d'agent IA basé sur les Graphes de Connaissance dynamiques (DKG). Il est mise en oeuvre sur un cas d'usage Cybersecurité pour l'illustrer et le guider.

> **Une approche Spec-Driven, modulaire et hautement gouvernée pour construire des Graphes de Connaissances Cyber souverains et conformes aux standards du W3C.**.  Un dossier de spécifications de développement constitue un des principaux objectifs du dossier framework du projet .

##  1.    Vision & Ambition du Projet

Nous avons tous fait l'expérience de mal-entendus entre nous et un tiers ou en tant qu'observateur dans un échange entre deux tiers, et nous avons tous passé beaucoup de temps pour s'assurer que les équipes comprennent bien les objectifs a atteindre. 
Combien de fois les réunion de retour d'expérience intègrent : "Il faut améliorer la communication" ?
Les enjeux d’efficacité opérationnelle et de niveau de qualité des produits et services semblent très importants.

Les technologies nous permettent enfin grâce aux agents IA basés sur les Graph de connaissance d'améliorer le partage des connaissance tout en gardant les niveaux de confidentialité. 

Mais ce n'est pas de la magie, ces technologies restent sous la gouvernance des équipes. Mais elles permettent une dynamique de capitalisation et d'amélioration continue difficilement imaginable auparavant.

Ce projet vise a faire un petit démonstrateur trés simple qui permette de percevoir les concepts mis en oeuvre mais aussi d'appréhender  les enjeux et promesse présentés dans cette vision.

En cybersécurité, les données d'intelligence sur les menaces (CTI), les inventaires d'actifs et les vulnérabilités sont souvent cloisonnés dans des silos hétérogènes.
Le projet **DKG-CyberSec** répond à ce défi en proposant :

1. **Un Framework d'Ingénierie Ontologique Rigoureux** : Une méthodologie réutilisable axée sur le développement piloté par les spécifications (_Spec-Driven Development_), la validation automatisée par SHACL/Pytest et une traçabilité stricte par phase.
    
2. **Une Application Concrète au Domaine Cyber / SOC** : Un modèle opérationnel permettant de relier en temps réel la connaissance théorique des menaces aux réalités du terrain d'un Centre d'Opérations de Sécurité (SOC).

3. **Econome en ressource** : pour le POC usecase tourner en inférence en local sur PC sans GPU avec 16Go RAM. Recours au cloud GPU pour fine tuning si besoin. 
4. **co-developement avec LLM cadré** : Methodologie de dévelopement avec IA , intégrant l'amélioration continue ([SPEC & PROMPT](./00-Projet/PROJECT_CONTEXT_PROMPT.md) )

##  2.   Le Cas d'Usage Métier pour illustrer les principes  : L'Ecosystème Cyber & SOC

Le projet illustre la puissance des Semantic Web Technologies en modélisant l'intégralité de la chaîne d'impact opérationnelle d'un SOC :
Commence petit puis grandi au cours des phases

```
┌──────────────┐       ┌───────────────────┐       ┌─────────────────┐
│  dkg:Asset   │──────>│ dkg:SoftwareComp  │──────>│dkg:Vulnerability│
│  (Serveur)   │       │  (Bibliothèque)   │       │  (CVE-2023-x)   │
└──────────────┘       └───────────────────┘       └────────┬────────┘
       │                                                    │
       ▼                                                    ▼
┌──────────────┐                                   ┌─────────────────┐
│dkg:TLPMarking│                                   │  dkg:Weakness   │
│ (TLP:AMBER)  │                                   │  (CWE-89 SQLi)  │
└──────────────┘                                   └─────────────────┘
```

### Principes & Fonctionnalités Clés du Framework :

- **Déduction & Raisonnement (OWL 2)** : Calcul automatique des relations inverses (ex: si un actif possède un composant, le composant est automatiquement rattaché à l'actif).
    
- **Alignement Lexical & Multilingue (SKOS)** : Normalisation des synonymes et jargons métiers (ex: lier _CVE_, _Faille de sécurité_ et _Vulnerability_ sur le même concept).
    
- **Gouvernance & Qualité Stricte (SHACL)** : Validation sous _Closed World Assumption_ (CWA) pour interdire les données corrompues (ex: rejet automatique d'un score CVSS supérieur à 10.0 ou mal typé).
    
- **Souveraineté & Classification (TLP)** : Marquage natif du niveau de confidentialité de l'information (`TLP:CLEAR`, `TLP:AMBER`, `TLP:RED`).
    


## 3. Méthodologie Itérative & Phase Projet & Architecture IA Hybride

Le projet **DKG-CyberSec** ne se limite pas à un graphe statique : il constitue le **cerveau opérationnel d'un Agent IA collaborateur** conçu pour épauler les équipes Cyber dans la gestion intégrale de leur SOC (à la manière d'une "micro-entreprise" de défense numérique).

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                   AGENT IA COLLABORATEUR (Assistant SOC)                 │
 └────────────────────────────────────┬────────────────────────────────────┘
                                      │
         ┌────────────────────────────┴────────────────────────────┐
         ▼                                                         ▼
┌───────────────────────────────┐                         ┌─────────────────┐
│     Couche Exploratoire &     │                         │ Couche Formelle │
│          Nuancée              │                         │   & Déterministe│
├───────────────────────────────┤                         ├─────────────────┤
│ • Ingestion Textuelle (NER)   │───(Enrichissement)─────>│ • Knowledge     │
│ • Vectorisation & Graph RAG   │                         │   Graph OWL/SKOS│
│ • Fine-Tuning de LLM Cyber    │<──(Rétro-Ingestion)─────│ • Base Neo4j    │
│ • Capture des subtilités      │                         │ • Rules SHACL   │
└───────────────────────────────┘                         └─────────────────┘
```

#### A. Le Triptyque Technique Cible

1. **Graphe Property Graph & SPARQL (Neo4j)** : Projection opérationnelle des données TBox/ABox pour offrir des requêtes de cheminement ultra-rapides (_graph traversal_) et des analyses d'impact visuelles en temps réel pour l'analyste SOC.
    
2. **Pipelines NLP / NER & Vectorisation (Graph RAG)** : Extraction d'entités nommées (_Named Entity Recognition_) à partir de flux non structurés (bulletins CTI, rapports d'incidents, advisories de sécurité) pour mapper automatiquement les concepts textuels vers le DKG.
    
3. **Fine-Tuning Continu du LLM** : Ré-entraînement régulier des modèles de langage locaux sur les données qualifiées du graphe. Cela permet à l'IA d'assimiler les nuances, le jargon métier et la terminologie spécifique à l'organisation.
    

#### B. La Boucle de Feedback & Rétro-Ingestion

L'IA ne se contente pas de lire le graphe : elle formule des hypothèses, identifie des incohérences ou propose des raffinements. En cas de doute ou lors de l'arrivée de nouvelles menaces ambiguës, l'Agent IA déclenche un processus de **re-digestion des données d'entrée** pour réévaluer et affiner la base de connaissances.

#### C. Une Rigueur Formelle & Explicable

Malgré la flexibilité apportée par le LLM et la vectorisation, **la décision finale reste 100 % déterministe et explicable**. C'est le Knowledge Graph ontologique (OWL + SHACL) qui sert de "garde-fou" (_Ground Truth_) : aucune assertion générée par l'IA ne peut être intégrée dans le SOC Master sans valider les contraintes formelles SHACL.

#### D. Cycle de Vie des Phases Projet

Le projet est a ses début. L'organisation par étape contribue aussi a consolider l'aspect "Dynamique" nécessaire à l'évolution du Graphe de Connaissance
```
┌─────────────────┐     Gate 1     ┌─────────────────┐     Gate 2     ┌─────────────────┐                    ┌──────────────────┐
│     PHASE 1     │───────────────>│     PHASE 2     │───────────────>│     PHASE 3     │───............───> │     PHASE XX     │
│ Socle TBox/SKOS │   (Pytest /    │Instanciation des│   (Validation  │ Données Externes│  maturation des    │     A VENIR      │
│  & Rules SHACL  │  Checklist)    │  données ABox   │   Qualité)     │  principe TLP   │ concepts&fonctions │neo4j, NER, ..    │
└─────────────────┘                └─────────────────┘                └─────────────────┘                    └──────────────────┘
     🟢 CLOSE                           🟡 EN COURS                       ⚪ PLANIFIÉ
```


[Phase Projet](./00-Projet/PhasesProjet.md)




##  4. Structure du Référentiel

Le dépôt est organisé selon une hiérarchie stricte facilitant la séparation entre gouvernance, données et outillage :

Plaintext

```
DKG-CYBERSEC/
├── 00-Projet/                          # Gouvernance, Checklists de Cadrage et suivi des Phases
│   ├── SPEC-00_Exigences.md            # Matrice globale des exigences projet (EXG-*)
│   ├── PhasesProjet.md                 # Tableau de bord d'avancement global
│   └── Cadrage_Checklist.md            # Gatekeeper d'évaluation inter-phases
├── 01-Principes_Spécification/         # Spécifications fonctionnelles et techniques (SPEC-XX)
├── 02-Donnees/                         # Graphes RDF Turtle, Datasets Master et Snapshots figés
└── 03-Application/                     # Outillage Python, scripts de génération et tests CI/CD
```

##  5. Rejoindre la Communauté & Réutiliser le Framework

### Vous souhaitez réutiliser le Framework sur votre propre Use Case ?

Ce Framework n'est pas limité à la cybersécurité ! Sa structure (OWL + SKOS + SHACL + Spec-Driven) est conçue pour être appliquée à tout domaine exigeant une gouvernance de données stricte (Santé, Finance, Aéronautique, Logistique) :
1. Adoptez la matrice d'exigences **`SPEC-00`** comme socle de qualité.
2. Modélisez votre domaine dans `01-Exigences/`.
3. Exploitez notre chaîne de scripts d'automatisation et de validation SHACL.
    

### Vous souhaitez contribuer au DKG-CyberSec ?
Les contributions sont les bienvenues ! Que ce soit pour :
- Enrichir l'ontologie Cyber (intégration de STIX 2.1, ATT&CK, TAXII).
- Ajouter de nouvelles Shapes SHACL de validation.
- Proposer des connecteurs d'ingestion d'ABox.
    

Consultez nos [Spécifications Projets (`SPEC-00`)](https://www.google.com/search?q=./00-Projet/SPEC-00_Exigences_Projet.md) pour comprendre nos règles de contribution et lancez-vous !