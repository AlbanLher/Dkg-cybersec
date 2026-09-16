---
type: spec
reference: SPC-TEC-P5-CONSO_01
revision: 1
titre: "Agent MITM, Consolidation SKOS & Réconciliation Sémantique"
titre_court: agent_mitm_conso_01
description: "Définit le cadre technique de l'Agent MITM et du Moteur de Consolidation SKOS pour la réconciliation sémantique déterministe."
phase_code: P5
phase_nom: "Agent MITM & Reasoning Base"
statut: "🟢 PASSED"
portee: USECASE_TECHNIQUE
public_vise:
  - "Architectes Ontologues"
  - "Développeurs DevSecOps"
exigences:
  - id: EXG-MITM-01
    domaine: IA
    titre: "Interception & Calcul Similitude"
    description: "L'Agent MITM doit vectoriser les entités via all-MiniLM-L6-v2 et calculer la similarité cosinus avec la TBox/ABox existante."
    test: "Pytest / Benchmark"
  - id: EXG-MITM-02
    domaine: IN
    titre: "Réconciliation Seuil 0.85"
    description: "Toute entité ayant un score >= 0.85 doit être consolidée via skos:exactMatch au lieu d'être dupliquée."
    test: "Pytest (test_phase5_mitm)"
  - id: EXG-TB-01
    domaine: TB
    titre: "Alignement Taxonomique SKOS"
    description: "Les catégories de menaces et taxonomies d'actifs doivent intégrer skos:Concept et skos:ConceptScheme."
    test: "Validation SHACL"
  - id: EXG-SE-02
    domaine: SE
    titre: "Ségrégation TLP en Ingestion Interceptée"
    description: "L'Agent MITM ne doit jamais inscrire un triplet contenant des données TLP:RED dans la ABox CTI (TLP:CLEAR)."
    test: "Audit Graphe / Pytest"
  - id: EXG-HW-01
    domaine: HW
    titre: "Temps de Réponse Offline"
    description: "Le calcul de similitude pour une entité doit s'exécuter en ms en local (Air-Gapped)."
    test: "Benchmark / Pytest"
---

# 📜 Agent MITM, Consolidation SKOS & Réconciliation Sémantique

## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif
Cette spécification définit le cadre technique et l'implémentation de l'**Agent MITM (Man-In-The-Middle)** et du **Moteur de Consolidation SKOS** pour la Phase 5. L'Agent MITM intercepte, filtre et aligne les entités extraites des flux non structurés ou des sources CTI externes. Il utilise des modèles locaux légers (`all-MiniLM-L6-v2`) et applique une réconciliation sémantique déterministe enrichie par le vocabulaire **SKOS** (`skos:exactMatch`, `skos:broadMatch`, `skos:closeMatch`) afin d'éviter la duplication des entités dans le graphe.

### 1.2 Glossaire Métier & Technique
| Acronyme / Concept | Définition | Contexte DKG |
| :--- | :--- | :--- |
| **Agent MITM** | Agent d'Interception & Validation | Composant logiciel intermédiaire interceptant les entités candidates avant écriture. |
| **SKOS** | Simple Knowledge Organization System | Standard W3C pour la représentation de thésaurus et taxonomies réconciliées. |
| **Similarity Threshold** | Seuil de Similitude Cosinus | Valeur minimale (`0.85` selon `config.py`) requise pour déclencher un alignement `skos:exactMatch`. |
| **Air-Gapped IA** | Modèles IA hors-ligne | Utilisation stricte de modèles légers hébergés en local sans appel API externe. |

## 🏗️ 2. Périmètre & Architecture Technique

- **Positionnement dans l'Architecture** : Document de niveau **Niveau 3 — Cas d'Usage Technique**.
- **Gouvernance & Validation** : Validé par le Lead Architecte Sémantique et le Lead DevSecOps.

```
        [ Flux CTI Bruts / NER ] (TLP:CLEAR)
                 │
                 ▼
 ┌─────────────────────────────────────────┐
 │           AGENT MITM (P05)              │
 │  - Filtrage TLP & Validation SHACL      │
 │  - Vectorisation Embeddings (MiniLM)    │  <--- config.py (MITM_SIMILARITY_THRESHOLD = 0.85)
 │  - Calcul Similitude Cosinus            │
 └────────────────────┬────────────────────┘
                      │
              [ Alignement SKOS ]
                      │
        ┌────────────┴────────────┐
        ▼                         ▼
[ Match >= 0.85 ]         [ Match < 0.85 ]
skos:exactMatch           Création Nouvelle Entité
(Consolidation TBox)      + Alignement Contextuel
          │                         │
          └────────────┬────────────┘
                       ▼
      [ ABox Interne / Infered ] (TLP:RED / AMBER)
```


## 📐 3. Spécifications Formelles & Schémas Turtle

### 3.1 Extension TBox pour SKOS & Mapping Sémantique

```turtle
@prefix dkg: [http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#) .
@prefix dkg-data: [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#) .
@prefix dkg-cti: [http://dkg.cybersec.org/cti#](http://dkg.cybersec.org/cti#) .
@prefix skos: [http://www.w3.org/2004/02/skos/core#](http://www.w3.org/2004/02/skos/core#) .
@prefix owl: [http://www.w3.org/2002/07/owl#](http://www.w3.org/2002/07/owl#) .
@prefix rdfs: [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#) .
@prefix xsd: [http://www.w3.org/2001/XMLSchema#](http://www.w3.org/2001/XMLSchema#) .

# Concept Scheme pour la Taxonomie CyberSec DKG
dkg:CyberSecurityConceptScheme a skos:ConceptScheme ;
    rdfs:label "Taxonomie & Thesaurus DKG CyberSec"@fr ,
               "DKG CyberSec Taxonomy & Thesaurus"@en .

# Concept ThreatActor aligné SKOS
dkg:ThreatActorConcept a rdfs:Class , owl:Class ;
    rdfs:subClassOf skos:Concept .

# Propriété de score d'alignement gérée par le MITM
dkg:alignmentScore a owl:DatatypeProperty ;
    rdfs:domain skos:Concept ;
    rdfs:range xsd:float ;
    rdfs:label "score de similitude calculé par l'Agent MITM"@fr .
````

### 3.2 Règle d'Inférence SKOS pour la Consolidation (`SPARQL CONSTRUCT`)

#### Règle R-MITM-01 : Propagation des Identifiants Réconciliés (`skos:exactMatch`) [`EXG-MITM-02`]

Extrait de code

```sparql
PREFIX dkg: [http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)
PREFIX skos: [http://www.w3.org/2004/02/skos/core#](http://www.w3.org/2004/02/skos/core#)
PREFIX owl: [http://www.w3.org/2002/07/owl#](http://www.w3.org/2002/07/owl#)

CONSTRUCT {
    ?entityA owl:sameAs ?entityB .
    ?entityA skos:exactMatch ?entityB .
}
WHERE {
    ?entityA dkg:alignmentScore ?score .
    ?entityA dkg:candidateMatch ?entityB .
    FILTER(?score >= 0.85)
}
```

## 📊 4. Matrice d'Exigences & Critères d'Acceptation (EXG-)

|**Identifiant**|**Domaine**|**Intitulé de l'Exigence**|**Description & Critères d'Acceptation**|**Mode de Test / Asset**|
|---|---|---|---|---|
|**EXG-MITM-01**|`IA`|Interception & Calcul Similitude|L'Agent MITM doit vectoriser les entités via `all-MiniLM-L6-v2` et calculer la similarité cosinus.|Pytest / Benchmark|
|**EXG-MITM-02**|`IN`|Réconciliation Seuil 0.85|Toute entité ayant un score $\ge 0.85$ doit être consolidée via `skos:exactMatch` au lieu d'être dupliquée.|Pytest (`test_phase5_mitm`)|
|**EXG-TB-01**|`TB`|Alignement Taxonomique SKOS|Les catégories de menaces et taxonomies d'actifs doivent intégrer `skos:Concept` et `skos:ConceptScheme`.|Validation SHACL|
|**EXG-SE-02**|`SE`|Ségrégation TLP en Ingestion Interceptée|L'Agent MITM ne doit jamais inscrire un triplet contenant des données TLP:RED dans la ABox CTI (`TLP:CLEAR`).|Audit Graphe / Pytest|
|**EXG-HW-01**|`HW`|Temps de Réponse Offline|Le calcul de similitude pour une entité doit s'exécuter en $< 100$ ms en local (Air-Gapped).|Benchmark / Pytest|

## 🛡️ 5. Outillage, CI/CD & Traçabilité Pytest

- **Scripts de Génération / Exécution** :
    
    - `03-Application/Phase5/mitm_agent.py` (Agent d'interception et de scoring)
        
    - `03-Application/Phase5/skos_consolidator.py` (Moteur de consolidation TBox/SKOS)
        
- **Modèles Locaux Utilisés** : `sentence-transformers/all-MiniLM-L6-v2` (`DIR_EMBEDDING_MODEL`)
    
- **Suites de Tests Associées** : `03-Application/Tests/test_phase5_mitm.py`
    
- **Artefacts Produits** : `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_SKOS_Master.ttl`
    

## 📚 6. Documents Liés & Références

- **[SPC-FWK-P1-GOUVERNANCE_01]** : Gouvernance du Cadre Spécifications & Exigences DKG.
    
- **[SPC-FWK-P5-RULES_01]** : Reasoning Rules & RBox Inference.
    
- **[config.py]** : Single Source of Truth (`MITM_SIMILARITY_THRESHOLD = 0.85`).
