
# Lexique Technique — Domain Knowledge Graph (DKG)

> **Domaine :** Architecture de Connaissances, Graphes, IA Agentique & Cybersécurité  
> **Statut :** Référentiel Source pour `md_to_skos.py`  
> **Version :** 2.0 (Enrichi Post-Phase 0)

---

## 1. Concepts de Modélisation de Graphes & Standards W3C

### Dynamic Knowledge Graph (DKG)
* **Définition :** Graphe de connaissances dynamique et évolutif capable d'absorber des flux d'informations temps réel (scans réseau, nouvelles CVE, feeds Threat Intel) tout en adaptant son schéma et son ontologie de manière semi-autonome grâce aux agents d'IA (Agent Guard / HITL).
* **Synonymes / Acronymes :** DKG, Graphe de Connaissances Dynamique
* **Domaine :** Architecture / Sémantique Temps Réel
* **Mapping SKOS :** `skos:prefLabel "Dynamic Knowledge Graph"@en` ; `skos:altLabel "DKG"@en`

### Simple Knowledge Organization System (SKOS)
* **Définition :** Standard du W3C conçu pour la représentation de thesaurus, taxonomies, schémas de concepts et vocabulaires contrôlés au format RDF.
* **Synonymes / Acronymes :** SKOS
* **Domaine :** W3C Standard
* **Mapping SKOS :** `skos:prefLabel "SKOS"@en`

### Neosemantics (n10s)
* **Définition :** Plugin officiel pour Neo4j permettant l'importation, l'exportation et le traitement natif de données structurées RDF, OWL et SKOS directement dans un modèle LPG (Labeled Property Graph).
* **Synonymes / Acronymes :** n10s, Neo4j RDF Plugin
* **Domaine :** Base de Données / Graphe
* **Mapping SKOS :** `skos:prefLabel "Neosemantics"@en` ; `skos:altLabel "n10s"@en`

### SHACL (Shapes Constraint Language)
* **Définition :** Langage de validation W3C permettant de définir des contraintes de structure et de typage sur un graphe RDF (exécuté par l'Agent Guard avant chargement en base).
* **Synonymes / Acronymes :** SHACL, Validation de Forme RDF
* **Domaine :** Sémantique / Qualité
* **Mapping SKOS :** `skos:prefLabel "SHACL"@en`

---

## 2. Architecture Agentique, GraphRAG & Gouvernance

### Agent GraphRAG (Retrieval-Augmented Generation)
* **Définition :** Architecture d'IA générative hybride combinant recherche vectorielle et traversée déterministe de graphes via requêtes Cypher multi-sauts pour alimenter un LLM avec un contexte métier certifié et traçable.
* **Synonymes / Acronymes :** GraphRAG, RAG Orienté Graphe
* **Domaine :** IA / Investigation
* **Mapping SKOS :** `skos:prefLabel "GraphRAG"@en`

### Human-in-the-Loop (HITL)
* **Définition :** Pattern d'architecture où les propositions d'agents autonomes (dérive ontologique, conflits, nouvelles entités) nécessitent une validation explicite d'un expert métier avant déploiement.
* **Synonymes / Acronymes :** HITL, Validation Humaine
* **Domaine :** Gouvernance IA
* **Mapping SKOS :** `skos:prefLabel "Human-in-the-Loop"@en` ; `skos:altLabel "HITL"@en`

### Request for Comments (RFC) Ontologique
* **Définition :** Proposition automatique d'évolution du schéma ou du lexique générée par l'Agent Guard et soumise au RSSI via le dashboard Streamlit lors de la détection de dérives.
* **Synonymes / Acronymes :** RFC Ontologique, Proposition de Schéma
* **Domaine :** Gouvernance / DevOps
* **Mapping SKOS :** `skos:prefLabel "Ontology RFC"@en`

---

## 3. Ingestion Cybersécurité & Référentiels Externes

### Taxonomie MISP (Machine Tags)
* **Définition :** Système mondial de classification structuré au format JSON sous forme de triplets `namespace:predicate="value"` utilisé pour le marquage de Threat Intelligence (ingesté via `misp_to_skos.py`).
* **Synonymes / Acronymes :** MISP Taxonomy, Machine Tag
* **Domaine :** Threat Intelligence / SKOS Externe
* **Mapping SKOS :** `skos:exactMatch https://www.misp-project.org/taxonomies/`

### Contraintes d'Unicité Cypher
* **Définition :** Règles DDL Neo4j (`CREATE CONSTRAINT`) garantissant la déduplication, l'idempotence des requêtes `MERGE` et la performance de traversée sur l'ensemble des entités du graphe (Device, CVE, Host, Service, etc.).
* **Synonymes / Acronymes :** Uniqueness Constraints, Indexation
* **Domaine :** Base de Données / Cypher
* **Mapping SKOS :** `skos:prefLabel "Cypher Constraint"@en`

---
OLD VERSION ci dessous

- **GraphRAG / LLM :** _Vector Store, Embeddings, Cypher Injection, Grounding, Chunking, Prompt Template._
    
- **Ontologies & Graphe :** _n10s (Neosemantics), OWL Class, SKOS Concept, Property Inherence, Triple Store, RDF/Turtle._
    
- **Ingénierie & Ops :** _Drift Guard, Schema Enforcement, Graph Mutation, Deduplication._
    

> **Intérêt :** Ce lexique servira au _prompt engineering_ du système agentique (pour que l'agent de dev / de maintenance comprenne l'architecture du code) et facilitera l'onboarding de tout nouveau développeur sur le projet.