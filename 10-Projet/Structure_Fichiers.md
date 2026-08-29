10-Projet
├── 1-TBox_initialisation
│     ├── Phase_Content                                   <---  initié lors du cadrage de la phase, il sert aussi de synthèse lorsque la phase est terminée
├── 2-ABox
│     ├── Phase_Content
├── 3-EnrichissementExterne
│     ├── Phase_Content
├── 4- ....
├── REX                          <--- Dossier dans lequel sont capitalisé les retours d'expérience de ce dévelopement itératif.
│     ├── REX-01_rigueur_attendue_RDF-OWL
├── Specification.md                                        <--- Exigence de gestion du projet
├── PhasesProjet.md                                        <--- Liste des Phase effectuée et en vues ainsi que le backlog des Concept et fonctions restant a implémenter dans les phases a venir
├── UseCase.md                                               <--- description de l'histoire correspondant au use case servant de base à la construction des data synthetiques en debut de phase
├── PROJECT_CONTEXT_PROMPT.md



11-Principes_Architecture
├── Spécifications                   <--- Contient les spécifcation relatives aux concept/fonction développés dans les phase et servant de référence aux test
│     ├── SPEC-01_Norme_TBox_RBox
│     ├── SPEC-02_Norme_ ...



12-Donnees/
├──  Master_Transversal/                      <--- Source UNIQUE de vérité (Cible Apps/Neo4j)
│   ├── TLP_AMBER_Socle_TBox/                   <--- Ontologie Canonique (TTL, JSON-LD, MD)
│   │   ├── DKG_TBox_Master.ttl
│   │   └── DKG_TBox_Master.md
│   └── TLP_RED_Consolidation_ABox/             <--- Graphe d'Attaque Consolidé (TTL, JSON-LD, MD)
│       ├── DKG_ABox_Master.ttl
│       └── DKG_ABox_Master.md
│
├──  Snapshots_Phases/                         <--- Historique figé / Auditabilité
│   ├── Phase_1_TBox_init/
│   ├── Phase_2_ABox_init/
│   └── Phase_3_ABox_enriched/
│
└──  Caches_Externes/                          <--- Référentiels publics
    └── TLP_CLEAR_NVD_CAPEC/    exemple




13-Application/
├──  Common/                                  <--- Utilitaires transversaux (Connecteurs RDF, Parsers)
│   ├── scrip-xx.py
├──  Phase_1_TBox/                             <--- Scripts historiques Phase 1
├──  Phase_2_ABox/                             <--- Scripts historiques Phase 2
├──  Phase_3_Enrichment/                 <--- Scripts d'enrichissement & consolidation
├──  Phase_4_ ...../                               <--- Scripts d'enrichissement & consolidation
