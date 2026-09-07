# 📜 SPEC-SOCLE-00 — Gouvernance du Cadre Spécifications & Exigences DKG

> **Classification** : `TLP:AMBER`
> **Statut** : 🟢 Approuvé
> **Niveau d'Abstraction** : 🟢 SOCLE_TRANSVERSAL
> **Public Cible** : Tous Rôles (Architectes Sémantiques, Analystes SOC, Développeurs DevSecOps)
> **Domaine Principal** : Méta-Framework DKG (`OR`, `HW`, `SE`, `TB`, `QU`, `SH`)
> **Matrice de Rattachabilité** : `EXG-OR-01` à `06`, `EXG-HW-01`, `EXG-SE-01` à `03`, `EXG-TB-01` à `05`, `EXG-QU-01` à `04`, `EXG-SH-01`

## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif

La présente spécification établit le cadre de gouvernance documentaire, organisationnel et technique pour le Dynamic Knowledge Graph (DKG) CyberSec. Elle définit le cycle de vie des exigences (`EXG-`), le découpage tripartite des spécifications et fixe les contraintes de sobriété hardware, d'isolation TLP et de qualité sémantique automatisée.

### 1.2 Glossaire Métier & Technique

|**Acronyme / Terme**|**Définition Complète**|**Contextualisation DKG**|
|---|---|---|
|**DKG**|Dynamic Knowledge Graph|Graphe de connaissances dynamique unifiant cartographie SI et CTI.|
|**SSOT**|Single Source of Truth|Centralisation des configurations et URIs dans un fichier unique.|
|**Air-Gapped**|Environnement Isolé|Exécution 100 % hors-ligne, sans aucun accès au réseau externe.|
|**CWA**|Closed World Assumption|Hypothèse du monde clos utilisée pour la validation SHACL stricte.|
|**TBox / ABox**|Terminology / Assertion Box|Schéma ontologique master (`dkg:`) vs Graphe d'instances réelles.|
|**TLP**|Traffic Light Protocol|Protocole de partage et de restriction de l'information (CLEAR/AMBER/RED).|

## 🎯 2. Périmètre & Principes Directeurs

Cette spécification s'applique de manière **transversale à toutes les phases du projet**. Aucun code Python, graphe Turtle ou pipeline CI/CD ne peut déroger aux principes ci-dessous.

### 2.1 Principes Fondamentaux

1. **Spec-Driven First** : La spécification précède systématiquement le code et l'ontologie (`EXG-OR-01`).
    
2. **Accessibilité & Alignement Métier** : Le découpage documentaire permet au SOC de valider les règles métier (`SPEC-METIER`) sans barrière technique OWL/RDF (`SPEC-TECH`).
    
3. **Souveraineté & Sobriété Hardware** : Exécution locale sur machine standard (16 Go RAM) en mode strictement hermétique (`EXG-HW-01`).
    

## 📐 3. Architecture Documentaire Tripartite

Pour garantir la lisibilité par toutes les parties prenantes, la documentation est structurée selon trois niveaux d'abstraction stricts :

Plaintext

```
docs/specs/
├── 01_TRANSVERSAL/
│   ├── SPEC-SOCLE-00_Gouvernance_Cadre_Ontologique.md
│   ├── SPEC-SOCLE-01_Framework_TBox_RBox_SHACL.md
│   └── SPEC-SOCLE-02_ABox_Validation_Constraints.md
├── 02_USECASE_METIER/
│   └── SPEC-METIER-UC02_Scenario_Silent_Cascade.md
└── 03_USECASE_TECHNIQUE/
    ├── SPEC-TECH-UC01_Instanciation_ABox_Cyber.md
    └── SPEC-TECH-UC03_Raisonnement_Propagation_Silent_Cascade.md
```

- **Niveau 1 — Socle Transversal (`SPEC-SOCLE-[NUM]`)** : Invariants applicables à tous les cas d'usage (Règles d'organisation, TBox Master, contraintes SHACL globales et politiques TLP).
    
- **Niveau 2 — Cas d'Usage Métier (`SPEC-METIER-[UC]`)** : Déclinaison fonctionnelle dédiée aux analystes SOC et CTI (Kill Chains, scénarios d'attaque, requêtes SPARQL de détection).
    
- **Niveau 3 — Cas d'Usage Technique (`SPEC-TECH-[UC]`)** : Spécification d'implémentation pour l'équipe DevSecOps (triplets RDF, règles SWRL/Inférence, scripts Python et assertions Pytest).
    

## 📐 4. Spécifications Formelles & Règles Métier

### 4.1 Organisation, Architecture & Sobriété Hardware

- **Spec-Driven First [`EXG-OR-01`]** : Aucun code, script ou fichier ontologique ne peut être produit ou modifié sans une spécification formelle préalable (`SPEC-SOCLE`, `SPEC-METIER` ou `SPEC-TECH`).
    
- **Parité Binaire Master/Snapshot [`EXG-OR-02`]** : Les données maîtres dans `02-Donnees/Master_Transversal/` doivent posséder une empreinte identique aux snapshots figés dans `02-Donnees/Snapshots_Phases/`.
    
- **Traçabilité par Phase [`EXG-OR-03`]** : Chaque phase dispose de son dossier dédié avec traçabilité complète à travers 4 briques (Framework, Instanciation, Data, Scripts).
    
- **Gatekeeper Inter-Phase [`EXG-OR-04`]** : L'ouverture d'une Phase N est conditionnée par la validation du formulaire de cadrage et le contrôle de clôture de la Phase N-1.
    
- **Source Unique de Vérité (SSOT) [`EXG-OR-05`]** : L'intégralité des chemins, namespaces RDF et seuils applicatifs doivent être importés exclusivement depuis `03-Application/config.py`. Aucun chemin _hardcodé_ n'est toléré.
    
- **Double Export Safe Sync [`EXG-OR-06`]** : Chaque pipeline produit d'abord son livrable dans `Snapshots_Phases/`, puis le synchronise vers `Master_Transversal/` en vérifiant l'impossibilité de conflit (`if snapshot.resolve() != master.resolve():`).
    
- **Inférence Économe & Air-Gapped [`EXG-HW-01`]** : L'inférence du POC (graphe, règles, NER, agent vectoriel) doit s'exécuter localement sur un PC standard (16 Go RAM, sans GPU dédié). Les accès externes au runtime sont strictement interdits.
    

### 4.2 Sécurité & Cloisonnement TLP

- **Marquage TLP Obligatoire [`EXG-SE-01`]** : Tout artefact (document Markdown, graphe Turtle) doit arborer son tag TLP explicite (`TLP:CLEAR`, `TLP:AMBER`, `TLP:RED`).
    
- **Isolation des Snapshots [`EXG-SE-02`]** : Les snapshots de jalons validés sont figés et conservés de façon immuable.
    
- **Souveraineté & Modèles Locaux [`EXG-SE-03`]** : Les modèles d'embeddings et de NER s'exécutent entièrement hors-ligne via le cache local `03-Application/models/cache/`.
    

### 4.3 Normes Sémantiques, TBox & Qualité

- **Namespace & Séparateur [`EXG-TB-01`]** : Espace de noms racine unique avec séparateur `#` pour la TBox.
    
- **Typage OWL Strict [`EXG-TB-02`]** : Typage formel obligatoire (`owl:Class`, `owl:ObjectProperty`, etc.).
    
- **Domaine & Portée Explicites [`EXG-TB-03`]** : Interdiction de déclarer une propriété sans `rdfs:domain` ni `rdfs:range`.
    
- **Inverses RBox [`EXG-TB-04`]** : Déclaration obligatoire de la propriété inverse via `owl:inverseOf`.
    
- **Couche Lexicale SKOS [`EXG-TB-05`]** : Présence obligatoire de `skos:prefLabel` (FR/EN) et `skos:definition`.
    
- **Couverture SHACL [`EXG-QU-01`]** : Validation SHACL couvrante sur l'ensemble du schéma.
    
- **Conformité Données CWA [`EXG-QU-02`]** : Validation des datatypes, longueurs et plages sous Closed World Assumption.
    
- **Sanity Check Automatisé [`EXG-QU-03`]** : Absence totale de violation de sévérité `sh:Violation`.
    
- **Vocabulaire TBox First [`EXG-QU-04`]** : Zéro prédicat ou classe hors-TBox Master utilisé dans le projet (contrôlé par `test_00`).
    
- **Shapes Structurales [`EXG-SH-01`]** : Méta-shapes de validation intégrées au schéma.
    

## 📊 5. Matrice Synthétique des Exigences (Index de Traçabilité)

|**Identifiant**|**Domaine**|**Intitulé de l'Exigence**|**Description & Critères d'Acceptation**|**Mode de Validation**|
|---|---|---|---|---|
|**EXG-OR-01**|`OR`|Spec-Driven Development|Mise à jour SPEC obligatoire avant toute modification de code.|Revue Git / Audit|
|**EXG-OR-02**|`OR`|Parité Master / Snapshot|Empreinte binaire identique entre Master et Snapshot.|Control Hash / CI|
|**EXG-OR-03**|`OR`|Standard Traçabilité Phase|Découpage strict des livrables selon les 4 briques projet.|Inspection Dossiers|
|**EXG-OR-04**|`OR`|Gatekeeper Inter-Phase|Validation préalable du formulaire de cadrage inter-phase.|Validation Cadrage|
|**EXG-OR-05**|`OR`|Architecture SSOT (`config.py`)|Centralisation stricte des répertoires et URIs dans `config.py`.|Test Python / AST|
|**EXG-OR-06**|`OR`|Double Export Anti-Collision|Synchronisation Snapshot -> Master sans erreur `SameFileError`.|Execution Script|
|**EXG-HW-01**|`HW`|Inférence Local Économe|Exécution PC 16 Go RAM sans GPU dédié, Air-Gapped strict.|Benchmark Resource|
|**EXG-SE-01**|`SE`|Marquage TLP Obligatoire|Tag TLP présent sur tout document ou graphe Turtle.|Linter / Pytest|
|**EXG-SE-02**|`SE`|Isolation des Snapshots|Immuabilité des snapshots de jalons validés.|Droits Fichiers|
|**EXG-SE-03**|`SE`|Air-Gapped & Modèles Locaux|Exécution MLOps/NLP 100% locale sans accès Internet runtime.|Check Réseau / Cache|
|**EXG-TB-01**|`TB`|Espace de Noms & Séparateur URI|Namespace TBox unique avec séparateur `#`.|Parsing RDF|
|**EXG-TB-02**|`TB`|Typage OWL Strict|Typage formel obligatoire (`owl:Class`, `owl:ObjectProperty`).|Parsing OWL / SPARQL|
|**EXG-TB-03**|`TB`|Déclaration Domaine & Portée|`rdfs:domain` et `rdfs:range` obligatoires sur toute propriété.|Requête SPARQL TBox|
|**EXG-TB-04**|`TB`|Sémantique RBox & Inverses|Rôles inverses obligatoires via `owl:inverseOf`.|Check Inverses SPARQL|
|**EXG-TB-05**|`TB`|Couche Lexicale SKOS|Labels multilingues (FR/EN) et définitions SKOS.|Validation SKOS|
|**EXG-QU-01**|`QU`|Couverture SHACL|Validation SHACL couvrante sur l'ensemble du schéma.|Execution pySHACL|
|**EXG-QU-02**|`QU`|Contrôle Conformité Données|Datatypes, plages et formats validés sous CWA.|pySHACL CWA|
|**EXG-QU-03**|`QU`|Sanity Check Automatisé|0 violation `sh:Violation` au contrôle pySHACL.|Pytest / SHACL|
|**EXG-QU-04**|`QU`|Vocabulaire TBox First|0 prédicat hors-TBox Master utilisé dans le projet.|Pytest (`test_00`)|
|**EXG-SH-01**|`SH`|Shapes Structurales Abstraites|Méta-shapes de validation intégrées au schéma.|Execution SHACL|

## 🛡️ 6. Outillage, CI/CD & Traçabilité Pytest

L'ensemble des exigences est vérifié automatiquement à chaque commit via la suite de tests unitaires et d'intégration :

- **Centralisation de Configuration** : `03-Application/config.py`
    
- **Moteur de Validation SHACL** : Executé via `pyshacl` sur la TBox Master et les ABox d'instances.
    
- **Suites de Tests Pytest** :
    
    - `tests/test_00_governance_and_tbox.py` (Vérifie `EXG-OR-*`, `EXG-TB-*`, `EXG-QU-04`)
        
    - `tests/test_01_shacl_and_quality.py` (Vérifie `EXG-QU-01` à `03`, `EXG-SH-01`)
        
    - `tests/test_02_security_and_tlp.py` (Vérifie `EXG-SE-01` à `03`)
        

## 📚 7. Documents Liés & Références

- **[TEMPLATE_SPECIFICATION]** : Modèle unifié de rédaction des spécifications du projet.
    
- **[SPEC-SOCLE-01]** : Spécification du Framework TBox, RBox et Contraintes SHACL Globale.
    
- **[SPEC-METIER-UC02]** : Scénario d'Attaque Silent Cascade (Description Métier SOC).
    
- **[SPEC-TECH-UC03]** : Instanciation & Raisonnement (Propagation Silent Cascade).