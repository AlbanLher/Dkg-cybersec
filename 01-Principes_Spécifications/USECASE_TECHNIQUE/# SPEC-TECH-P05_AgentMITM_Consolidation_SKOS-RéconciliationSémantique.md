Voici la spécification technique **SPEC-TECH-P05** conçue sur mesure pour encadrer le développement de l'**Agent MITM** et le mécanisme de **Consolidation Sémantique via SKOS**, en respectant scrupuleusement la gouvernance DKG, le Master Context et la SSOT `config.py`.

# SPEC-TECH-P05 — Agent MITM, Consolidation SKOS & Réconciliation Sémantique

> **Classification** : `TLP:AMBER`
> 
> **Statut** : 🟢 Approuvé
> 
> **Niveau d'Abstraction** : 🛠️ IMPLEMENTATION_DEVSECOPS (Niveau 3)
> 
> **Public Cible** : Architectes Ontologues, Développeurs DevSecOps, Analystes SOC
> 
> **Domaine Principal** : `IN` | `TB` | `QU` | `SE` | `IA`
> 
> **Matrice de Rattachabilité** : `EXG-MITM-01` à `03`, `EXG-SKOS-01` à `02`, `EXG-SE-01`, `EXG-HW-01`

## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif

Cette spécification définit le cadre technique et l'implémentation de l'**Agent MITM (Man-In-The-Middle)** et du **Moteur de Consolidation SKOS** pour la Phase 5 (Vague 2 / Consolidation). L'Agent MITM intercepte, filtre et aligne les entités extraites des flux non structurés (Phase 4) ou des sources CTI externes (Phase 3). Il utilise des modèles locaux légers (GLiNER & MiniLM) et applique une réconciliation sémantique déterministe enrichie par le vocabulaire **SKOS** (`skos:exactMatch`, `skos:broadMatch`, `skos:closeMatch`) afin de résoudre les ambiguïtés et éviter la duplication des entités dans le graphe DKG.

### 1.2 Glossaire Métier & Technique

|**Acronyme / Concept**|**Définition**|**Contexte DKG**|
|---|---|---|
|**Agent MITM**|Agent d'Interception & Validation|Composant logiciel intermédiaire interceptant les triplets/entités candidates avant écriture dans le graphe master.|
|**SKOS**|Simple Knowledge Organization System|Standard W3C pour la représentation de thesaurus, taxonomies et concepts réconciliés.|
|**Similarity Threshold**|Seuil de Similitude Cosinus|Valeur minimale (`0.85` selon `config.py`) requise pour déclencher un alignement automatique `skos:exactMatch`.|
|**Air-Gapped IA**|Modèles IA hors-ligne|Utilisation stricte de modèles légers hébergés en local (`models/cache`) sans appel API externe.|

## 🎯 2. Périmètre & Architecture Technique

### 2.1 Positionnement dans la Chaîne de Traitement

```
  [ Flux CTI Bruts / NER ] (TLP:CLEAR)
             │
             ▼
┌─────────────────────────────────────────┐
│           AGENT MITM (P05)              │
│  - Filtrage TLP & Validation SHACL     │
│  - Vectorisation Embeddings (MiniLM)   │  <--- config.py (MITM_SIMILARITY_THRESHOLD = 0.85)
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
@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix dkg-data: <http://dkg.cybersec.org/data#> .
@prefix dkg-cti: <http://dkg.cybersec.org/cti#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Concept Scheme pour la Taxonomie CyberSec DKG
dkg:CyberSecurityConceptScheme a skos:ConceptScheme ;
    rdfs:label "Taxonomie & Thesaurus DKG CyberSec"@fr ,
               "DKG CyberSec Taxonomy & Thesaurus"@en .

# Exemple de Mapping Sémantique SKOS d'un Synonyme ou Vulnérabilité
dkg:ThreatActorConcept a rdfs:Class , owl:Class ;
    rdfs:subClassOf skos:Concept .

# Propriété de score d'alignement gérée par le MITM
dkg:alignmentScore a owl:DatatypeProperty ;
    rdfs:domain skos:Concept ;
    rdfs:range xsd:float ;
    rdfs:label "score de similitude calculé par l'Agent MITM"@fr .
```

### 3.2 Règle d'Inférence SKOS pour la Consolidation (`SPARQL CONSTRUCT`)

#### Règle R-MITM-01 : Propagation des Identifiants Réconciliés (`skos:exactMatch`)

```sparql
PREFIX dkg: <http://dkg.cybersec.org/tbox#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

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

## 📊 4. Matrice d'Exigences & Critères d'Acceptation (`EXG-`)

|**Identifiant**|**Domaine**|**Intitulé de l'Exigence**|**Description & Critères d'Acceptation**|**Mode de Test / Asset**|
|---|---|---|---|---|
|**EXG-MITM-01**|`IA` / `IN`|Interception & Calcul Similitude|L'Agent MITM doit vectoriser les entités via `all-MiniLM-L6-v2` et calculer la similarité cosinus avec la TBox/ABox existante.|Pytest / Benchmark|
|**EXG-MITM-02**|`IN`|Réconciliation Seuil `0.85`|Toute entité ayant un score $\ge 0.85$ doit être consolidée via `skos:exactMatch` au lieu d'être dupliquée.|Pytest (`test_phase5_mitm`)|
|**EXG-SKOS-01**|`TB`|Alignement Taxonomique SKOS|Les catégories de menaces et taxonomies d'actifs doivent intégrer `skos:Concept` et `skos:ConceptScheme`.|Validation SHACL|
|**EXG-SKOS-02**|`SE`|Ségrégation TLP en Ingestion Interceptée|L'Agent MITM ne doit jamais inscrire un triplet contenant des données TLP:RED dans la ABox CTI (`TLP:CLEAR`).|Audit Graphe / Pytest|
|**EXG-HW-01**|`HW`|Temps de Réponse Offline|Le calcul de similitude pour une entité doit s'exécuter en $< 100$ ms en local (Air-Gapped).|Benchmark / Pytest|

## 🛡️ 5. Outillage, CI/CD & Traçabilité Pytest

- **Scripts de Génération / Exécution** :
    
    - `03-Application/Phase5/mitm_agent.py` (Agent d'interception et de scoring)
        
    - `03-Application/Phase5/skos_consolidator.py` (Moteur de consolidation TBox/SKOS)
        
- **Modèles Locaux Utilisés** :
    
    - Embedding : `DIR_EMBEDDING_MODEL` (`sentence-transformers/all-MiniLM-L6-v2`)
        
- **Suite de Test Associée** : `03-Application/Tests/test_phase5_mitm.py`
    
- **Artefacts Produits** : `02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/DKG_SKOS_Master.ttl`
    
    [cite: 2]
    

## 📚 6. Documents Liés & Références

- **[SPEC-SOCLE-00]** : Gouvernance du Cadre Spécifications & Exigences DKG.
    
- **[SPEC-SOCLE-04]** : Rules, RBox & Engine Inférence.
    
- **[config.py]** : Single Source of Truth (`MITM_SIMILARITY_THRESHOLD = 0.85`)[cite: 2].