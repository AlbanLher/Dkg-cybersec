* **TBox (Terminological Box)** : Schéma formel du domaine définissant le vocabulaire, les concepts (Classes), leurs hiérarchies (Sous-classes) et les règles d'association (Propriétés/Relations). C'est le contrat de structure immuable du graphe.
* **ABox (Assertional Box)** : Données réelles et instances concrètes (équipements, adresses IP, identifiants CVE, règles de sécurité) constituant la mémoire opérationnelle.

# 📖 Lexique Global d'Exposition (Phase 0)

> *Document généré automatiquement à partir du Vault consolidé (Lexiques, Ontologies, CVE, Inventory).*

---

## # Lexique Technique — Domain Knowledge Graph (DKG)

**Définition :** Aucune définition renseignée.

---

## # 🌐 Lexique Public : Standards Cyber & Architecture SI

**Définition :** Aucune définition renseignée.

---

## # 🔒 Lexique Privé : Jargon Métier, Code Names & Topologie Interne

**Définition :** Aucune définition renseignée.

---

## 1. Concepts de Modélisation de Graphes & Standards W3C

**Définition :** Aucune définition renseignée.

---

## 1. Concepts de Modélisation de Graphes & Standards W3C

**Définition :** Aucune définition renseignée.

---

## 2. Architecture Agentique, GraphRAG & Gouvernance

**Définition :** Aucune définition renseignée.

---

## 2. Architecture Agentique, GraphRAG & Gouvernance

**Définition :** Aucune définition renseignée.

---

## 3. Ingestion Cybersécurité & Référentiels Externes

**Définition :** Aucune définition renseignée.

---

## 3. Ingestion Cybersécurité & Référentiels Externes

**Définition :** Aucune définition renseignée.

---

## [AssetConcept] Équipement Système & Hôte

**Définition :** **Identifiant URI :** `cyber:Device` **Domaine :** Architecture & Infra **Terme Officiel (prefLabel) :** Équipement Système **Erreurs Fréquentes (hiddenLabel) :** Srvur, Servuer **Définition Métier :** Ressource physique ou virtuelle dotée d'une adresse IP et hébergeant des composants logiciels ou des services. **Exemple d'Usage :** *"L'instance SRV-WEB-01 est déployée sur l'hôte physique HYP-01."*

**Synonymes :** **Jargon & Acronymes (altLabel) :** Serveur, Machine, Host, SRV, Bécane, Instance, Bare-Metal

---

## [AssetConcept] Équipement Système Générique

**Définition :** **URI Ontologie :** `cyber:Device` **Terme Officiel (prefLabel) :** Équipement Système **Erreurs Fréquentes (hiddenLabel) :** Srvur, Servuer **Définition Métier :** Ressource matérielle ou virtuelle dotée d'une adresse IP et hébergeant des composants logiciels. **Exemple d'Usage :** *"L'hôte physique exécute deux machines virtuelles."*

**Synonymes :** **Jargon & Acronymes (altLabel) :** Serveur, Machine, Host, Node, Bare-Metal, Compute Instance

---

## [AssetConcept] Équipement Système Générique

**Définition :** Aucune définition renseignée.

---

## [BusinessUnitConcept] Entité & Propriétaire Applicatif

**Définition :** **URI Ontologie :** `entreprise:BusinessUnit` **Terme Officiel (prefLabel) :** Unité d'Organisation Métier **Définition Métier :** Entité interne ou direction opérationnelle responsable du budget et de la conformité d'un actif.

**Synonymes :** **Jargon & Acronymes (altLabel) :** BU, Branch, Propriétaire, Responsible Party, AppOwner

---

## [BusinessUnitConcept] Entité & Propriétaire Applicatif

**Définition :** Aucune définition renseignée.

---

## [ComponentConcept] Composant Applicatif & Service

**Définition :** **Identifiant URI :** `cyber:Software` **Domaine :** Architecture **Terme Officiel (prefLabel) :** Composant Logiciel **Définition Métier :** Programme ou ensemble d'exécutables exécutés sur un équipement pour fournir une fonction applicative. **Exemple d'Usage :** *"Le middleware Tomcat est le composant applicatif impacté."*

**Synonymes :** **Jargon & Acronymes (altLabel) :** Application, App, Service, Brique, Micro-service, Package, Middleware

---

## [CriticalAssetConcept] Actif Critique Métier

**Définition :** **URI Ontologie :** `entreprise:CriticalAsset` **Terme Officiel (prefLabel) :** Actif Critique Métier **Définition Métier :** Équipement hébergeant des données de santé ou financières soumises à une indisponibilité maximale de 15 minutes. **Exemple d'Usage :** *"La Bécane Compta SRV-FIN-01 est classée Actif Critique."*

**Synonymes :** **Jargon & Acronymes (altLabel) :** SRV-CRIT, Bécane Compta, Machine Cœur de Réseau, Node-Core

---

## [CriticalAssetConcept] Actif Critique Métier

**Définition :** Aucune définition renseignée.

---

## [InternalZoneConcept] Zone Enclave Interne & Salles Blanches

**Définition :** **URI Ontologie :** `entreprise:InternalZone` **Terme Officiel (prefLabel) :** Enclave Sécurisée Interne **Définition Métier :** Zone isolée du SI soumise aux contrôles renforcés d'accès et au chiffrement de bout en bout. **Exemple d'Usage :** *"Seuls les flux authentifiés peuvent pénétrer la Bulle Sanctuarisée Z-PROD-01."*

**Synonymes :** **Jargon & Acronymes (altLabel) :** Landing Zone Prod, Zone PCI-DSS, Bulle Sanctuarisée, Z-PROD-01

---

## [InternalZoneConcept] Zone Enclave Interne & Salles Blanches

**Définition :** Aucune définition renseignée.

---

## [PublicZoneConcept] Zone Réseau Générique

**Définition :** **URI Ontologie :** `cyber:Environment` **Terme Officiel (prefLabel) :** Zone Réseau Standard **Définition Métier :** Périmètre réseau abstrait défini par un niveau d'exposition et des politiques de filtrage standardisées.

**Synonymes :** **Jargon & Acronymes (altLabel) :** DMZ, LAN, Subnet, Segment, Perimeter

---

## [PublicZoneConcept] Zone Réseau Générique

**Définition :** Aucune définition renseignée.

---

## [RequirementConcept] Exigence & Règle de Conformité

**Définition :** **Identifiant URI :** `cyber:Requirement` **Domaine :** Cyber & Compliance **Terme Officiel (prefLabel) :** Exigence de Sécurité **Définition Métier :** Obligation technique ou organisationnelle issue d'un référentiel (NIS2, ISO 27001) imposée à un composant ou une zone. **Exemple d'Usage :** *"L'exigence de chiffrement s'applique à la zone DMZ."*

**Synonymes :** **Jargon & Acronymes (altLabel) :** Mesure, Control, Règle NIS2, Directive, Standard, Safeguard

---

## [VulnerabilityConcept] Vulnérabilité & Faille

**Définition :** **Identifiant URI :** `cyber:Vulnerability` **Domaine :** Cyber **Terme Officiel (prefLabel) :** Vulnérabilité Sécurité **Erreurs Fréquentes (hiddenLabel) :** Vulnerabilite, Vullnerabilite **Définition Métier :** Faiblesse dans un composant ou une configuration pouvant être exploitée pour porter atteinte au système. **Exemple d'Usage :** *"La CVE-2026-1234 représente une brèche critique."*

**Synonymes :** **Jargon & Acronymes (altLabel) :** CVE, Faille, Flaw, Trou de sécurité, Brèche, Defaut

---

## [VulnerabilityConcept] Vulnérabilité & Faille Publique

**Définition :** **URI Ontologie :** `cyber:Vulnerability` **Terme Officiel (prefLabel) :** Vulnérabilité Sécurité **Erreurs Fréquentes (hiddenLabel) :** Vulnerabilite, Vullnerabilite **Définition Métier :** Faiblesse identifiée dans un composant logiciel (référencée ou non dans la base NVD/CVE) pouvant être exploitée. **Exemple d'Usage :** *"La vulnérabilité CVE-2026-1042 possède un score CVSS v3 de 9.8."*

**Synonymes :** **Jargon & Acronymes (altLabel) :** CVE, Faille, Flaw, Trou de sécurité, Bug, Weakness

---

## [VulnerabilityConcept] Vulnérabilité & Faille Publique

**Définition :** Aucune définition renseignée.

---

## [ZoneConcept] Zone Réseau & Partitionment

**Définition :** **Identifiant URI :** `cyber:Environment` **Domaine :** Architecture & Cyber **Terme Officiel (prefLabel) :** Zone Réseau **Définition Métier :** Périmètre réseau isolé soumis à une politique de filtrage et à un niveau de confiance homogène. **Exemple d'Usage :** *"Les API publiques doivent résider dans la Landing Zone DMZ."*

**Synonymes :** **Jargon & Acronymes (altLabel) :** DMZ, LAN, Segment, Zone Externe, Enclave, Landing Zone, Subnet

---

## Agent GraphRAG (Retrieval-Augmented Generation)

**Définition :** **Définition :** Architecture d'IA générative hybride combinant recherche vectorielle et traversée déterministe de graphes via requêtes Cypher multi-sauts pour alimenter un LLM avec un contexte métier certifié et traçable. **Domaine :** IA / Investigation **Mapping SKOS :** `skos:prefLabel "GraphRAG"@en`

**Synonymes :** **Synonymes / Acronymes :** GraphRAG, RAG Orienté Graphe

---

## Agent GraphRAG (Retrieval-Augmented Generation)

**Définition :** Aucune définition renseignée.

**Synonymes :** * **Synonymes / Acronymes :** GraphRAG, RAG Orienté Graphe

---

## Contraintes d'Unicité Cypher

**Définition :** **Définition :** Règles DDL Neo4j (`CREATE CONSTRAINT`) garantissant la déduplication, l'idempotence des requêtes `MERGE` et la performance de traversée sur l'ensemble des entités du graphe (Device, CVE, Host, Service, etc.). **Domaine :** Base de Données / Cypher **Mapping SKOS :** `skos:prefLabel "Cypher Constraint"@en` **GraphRAG / LLM :** _Vector Store, Embeddings, Cypher Injection, Grounding, Chunking, Prompt Template._ **Ontologies & Graphe :** _n10s (Neosemantics), OWL Class, SKOS Concept, Property Inherence, Triple Store, RDF/Turtle._ **Ingénierie & Ops :** _Drift Guard, Schema Enforcement, Graph Mutation, Deduplication._

**Synonymes :** **Synonymes / Acronymes :** Uniqueness Constraints, Indexation

---

## Contraintes d'Unicité Cypher

**Définition :** Aucune définition renseignée.

**Synonymes :** * **Synonymes / Acronymes :** Uniqueness Constraints, Indexation

---

## Dynamic Knowledge Graph (DKG)

**Définition :** **Définition :** Graphe de connaissances dynamique et évolutif capable d'absorber des flux d'informations temps réel (scans réseau, nouvelles CVE, feeds Threat Intel) tout en adaptant son schéma et son ontologie de manière semi-autonome grâce aux agents d'IA (Agent Guard / HITL). **Domaine :** Architecture / Sémantique Temps Réel

**Synonymes :** **Synonymes / Acronymes :** DKG, Graphe de Connaissances Dynamique, **Mapping SKOS :** `skos:prefLabel "Dynamic Knowledge Graph"@en` ; `skos:altLabel "DKG"@en`

---

## Dynamic Knowledge Graph (DKG)

**Définition :** Aucune définition renseignée.

**Synonymes :** * **Synonymes / Acronymes :** DKG, Graphe de Connaissances Dynamique

---

## Human-in-the-Loop (HITL)

**Définition :** **Définition :** Pattern d'architecture où les propositions d'agents autonomes (dérive ontologique, conflits, nouvelles entités) nécessitent une validation explicite d'un expert métier avant déploiement. **Domaine :** Gouvernance IA

**Synonymes :** **Synonymes / Acronymes :** HITL, Validation Humaine, **Mapping SKOS :** `skos:prefLabel "Human-in-the-Loop"@en` ; `skos:altLabel "HITL"@en`

---

## Human-in-the-Loop (HITL)

**Définition :** Aucune définition renseignée.

**Synonymes :** * **Synonymes / Acronymes :** HITL, Validation Humaine

---

## Lexique Technique — Domain Knowledge Graph (DKG)

**Définition :** Aucune définition renseignée.

---

## Neosemantics (n10s)

**Définition :** **Définition :** Plugin officiel pour Neo4j permettant l'importation, l'exportation et le traitement natif de données structurées RDF, OWL et SKOS directement dans un modèle LPG (Labeled Property Graph). **Domaine :** Base de Données / Graphe

**Synonymes :** **Synonymes / Acronymes :** n10s, Neo4j RDF Plugin, **Mapping SKOS :** `skos:prefLabel "Neosemantics"@en` ; `skos:altLabel "n10s"@en`

---

## Neosemantics (n10s)

**Définition :** Aucune définition renseignée.

**Synonymes :** * **Synonymes / Acronymes :** n10s, Neo4j RDF Plugin

---

## Request for Comments (RFC) Ontologique

**Définition :** **Définition :** Proposition automatique d'évolution du schéma ou du lexique générée par l'Agent Guard et soumise au RSSI via le dashboard Streamlit lors de la détection de dérives. **Domaine :** Gouvernance / DevOps **Mapping SKOS :** `skos:prefLabel "Ontology RFC"@en`

**Synonymes :** **Synonymes / Acronymes :** RFC Ontologique, Proposition de Schéma

---

## Request for Comments (RFC) Ontologique

**Définition :** Aucune définition renseignée.

**Synonymes :** * **Synonymes / Acronymes :** RFC Ontologique, Proposition de Schéma

---

## SHACL (Shapes Constraint Language)

**Définition :** **Définition :** Langage de validation W3C permettant de définir des contraintes de structure et de typage sur un graphe RDF (exécuté par l'Agent Guard avant chargement en base). **Domaine :** Sémantique / Qualité **Mapping SKOS :** `skos:prefLabel "SHACL"@en`

**Synonymes :** **Synonymes / Acronymes :** SHACL, Validation de Forme RDF

---

## SHACL (Shapes Constraint Language)

**Définition :** Aucune définition renseignée.

**Synonymes :** * **Synonymes / Acronymes :** SHACL, Validation de Forme RDF

---

## Simple Knowledge Organization System (SKOS)

**Définition :** **Définition :** Standard du W3C conçu pour la représentation de thesaurus, taxonomies, schémas de concepts et vocabulaires contrôlés au format RDF. **Domaine :** W3C Standard **Mapping SKOS :** `skos:prefLabel "SKOS"@en`

**Synonymes :** **Synonymes / Acronymes :** SKOS

---

## Simple Knowledge Organization System (SKOS)

**Définition :** Aucune définition renseignée.

**Synonymes :** * **Synonymes / Acronymes :** SKOS

---

## Taxonomie MISP (Machine Tags)

**Définition :** **Définition :** Système mondial de classification structuré au format JSON sous forme de triplets `namespace:predicate="value"` utilisé pour le marquage de Threat Intelligence (ingesté via `misp_to_skos.py`). **Domaine :** Threat Intelligence / SKOS Externe **Mapping SKOS :** `skos:exactMatch https://www.misp-project.org/taxonomies/`

**Synonymes :** **Synonymes / Acronymes :** MISP Taxonomy, Machine Tag

---

## Taxonomie MISP (Machine Tags)

**Définition :** Aucune définition renseignée.

**Synonymes :** * **Synonymes / Acronymes :** MISP Taxonomy, Machine Tag

---

## 🌐 Lexique Public : Standards Cyber & Architecture SI

**Définition :** Aucune définition renseignée.

---

## 🌐 Référentiels Publics Externe Intégrés au Lexique SKOS

**Définition :** Aucune définition renseignée.

---

## 📖 Lexique Métier : Architecture SI & Cybersécurité

**Définition :** Aucune définition renseignée.

---

## 🔒 Lexique Privé : Jargon Métier, Code Names & Topologie Interne

**Définition :** Aucune définition renseignée.

---
