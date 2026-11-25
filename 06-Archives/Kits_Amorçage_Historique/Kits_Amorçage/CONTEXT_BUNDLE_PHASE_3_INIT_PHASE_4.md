📦 CONTEXT BUNDLE - DKG-CyberSec & Agent IA SOC

Phase Active : Phase 3 - Ingestion CTI Externe & Superposition Cross-TLP (TLP:CLEAR)

Jalon / Vague : Clôture Phase 3 ➔ Clôture Vague 2 (Prêt pour Phase 4 / Ingestion NER Non-Structurée)

Statut Global : 🟢 ALL TESTS PASSED (PyTest 100% - Conformité SHACL & Recette Cross-TLP)

Horodatage : Septembre 2026

  

📌 1. Bilan & Mémoire d'Avancement Complexe (State Vector Master)

🟢 Acquis Totaux Valides (Phases 1, 2 & 3)

Phase 1 - Socle TBox & SHACL (TLP:AMBER) : Ontologie OWL2/RDFS stabilisée sous [http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#). Profils SHACL configurés pour valider sous Closed World Assumption (CWA).

Phase 2 - Cartographie Interne (TLP:RED) : Représentation des actifs métiers, composants logiciels et vulnérabilités internes sous [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#). Export miroir automatisé et parité Markdown/Turtle validée.

Phase 3 - Référentiel CTI Externe (TLP:CLEAR) : Ingestion et normalisation réussies des flux publics (NVD, MITRE ATT&CK, CISA KEV) sous [http://dkg.cybersec.org/cti#](http://dkg.cybersec.org/cti#) dans 02-Donnees/Master_Transversal/TLP_CLEAR_CTI_External/.

Superposition & Alignement Cross-TLP : Connexion étanche et unidirectionnelle entre l'infrastructure interne (TLP:RED), le socle ontologique (TLP:AMBER), et les référentiels publics (TLP:CLEAR).

Validation SHACL sous CWA : Validation à 100% du graphe d'union (TBox + ABox RED + ABox CTI) sans aucune violation. Datatypes des scores CVSS ancrés en xsd:float et drapeau CISA KEV typé en xsd:boolean.

Standardisation RBox Canonique : Adoption stricte du prédicats RBox dkg:exploitsWeakness pour la liaison Vulnerability ➔ Weakness.

Règles d'Architecture & Qualité Inviolables :SSOT Stricte (EXG-OR-05) : Centralisation absolue dans 03-Application/config.py avec validation Pydantic V2 et création dynamique garantie des dossiers.

Double Export & Parité (EXG-OR-06) : Synchronisation automatique et vérifiée sans conflit de chemins (snapshot.resolve() != master.resolve()) entre les snapshots de phase et les dossiers masters.

🎯 Objectifs Entrants (Phase 4 / Vague 2)

Epic 2.2 (Ingestion CTI Non-Structurée & NER) : Extraction d'entités menaces à partir de rapports textuels bruts PDF/Markdown via modèles NER (gliner_large-v2.1 / bert-base-NER).

Extension Ontologique Dynamique (Agent MITM / SKOS) : Réconciliation des entités extraites par NLP avec les taxonomies existantes du Knowledge Graph.

⚙️ 2. Fichier SSOT config.py Intégral (Active Runtime Only)

Règle SSOT (EXG-OR-05) : Aucune valeur en dur (nom de fichier, chemin, URI) hors de ce bloc.

Python

  

import os

from pathlib import Path

from rdflib import Namespace

  

# --- REPERTOIRES SYSTEME ---

BASE_DIR = Path(__file__).resolve().parent.parent

DIR_DATA = BASE_DIR / "02-Donnees"

DIR_MASTER_TRANSVERSAL = DIR_DATA / "Master_Transversal"

  

# Phase Masters & Snapshots

DIR_MASTER_TBOX = DIR_MASTER_TRANSVERSAL / "TLP_AMBER_Socle_TBox"

DIR_MASTER_ABOX = DIR_MASTER_TRANSVERSAL / "TLP_RED_Instances_ABox"

DIR_CTI_CLEAR = DIR_MASTER_TRANSVERSAL / "TLP_CLEAR_CTI_External"

  

DIR_INPUTS_P3 = DIR_DATA / "Input_Phases" / "Phase3_CTI"

DIR_SNAPSHOT_P3 = DIR_DATA / "Snapshots_Phases" / "Phase3_CTI"

  

# --- FICHIERS MASTERS & DOCS ---

TBOX_MASTER_PATH = DIR_MASTER_TBOX / "DKG_TBox_Master.ttl"

SHACL_MASTER_PATH = DIR_MASTER_TBOX / "DKG_SHACL_Master.ttl"

  

ABOX_RED_PATH = DIR_MASTER_ABOX / "DKG_ABox_Master.ttl"

ABOX_RED_MD_PATH = DIR_MASTER_ABOX / "DKG_ABox_Master.md"

  

INPUT_CTI_JSON_PATH = DIR_INPUTS_P3 / "external_nvd_capec_feed.json"

ABOX_CTI_PATH = DIR_CTI_CLEAR / "DKG_ABox_CTI_External.ttl"

ABOX_CTI_MD_PATH = DIR_CTI_CLEAR / "DKG_ABox_CTI_External.md"

  

# --- NAMESPACES RDF VALIDÉS ---

DKG_TBOX = Namespace("http://dkg.cybersec.org/tbox#")

DKG_DATA = Namespace("http://dkg.cybersec.org/data#")

DKG_CTI = Namespace("http://dkg.cybersec.org/cti#")

📐 3. Contrats d'Interface & Schémas Canoniques Intégraux

Datatypes & Normalisation Stricte

cvssScore : xsd:float (stricte conformité SHACL)

isCisaKev : xsd:boolean

Identifiants CTI : Normalisation Regex (CVE-\d{4}-\d+, CWE-\d+, CAPEC-\d+).

Isolation des Namespaces :Concept ontologique / schéma : dkg: ([http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#))

Données d'infrastructure internes : dkg-data: ([http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#))

Données CTI publiques : dkg-cti: ([http://dkg.cybersec.org/cti#](http://dkg.cybersec.org/cti#))

Graphe Cross-TLP Canonique Complet

Plaintext

  

[dkg-data:Asset] (TLP:RED)

│

└──(dkg:hasInstalledComponent)──> [dkg-data:SoftwareComponent] (TLP:RED)

│

└──(dkg:hasVulnerability)──> [dkg-cti:Vulnerability] (TLP:CLEAR)

│

├──(dkg:cvssScore)──> xsd:float

├──(dkg:isCisaKev)──> xsd:boolean

│

└──(dkg:exploitsWeakness)──> [dkg-cti:Weakness] (TLP:CLEAR)

│

└──(dkg:hasThreatPattern)──> [dkg-cti:ThreatPattern] (TLP:CLEAR)

📂 4. État des Artefacts & Code de la Phase 3

📄 Documentation & Spécifications

Phase_Content.md : Fiche d'étape révisée et alignée SSOT.

Memo_UseCase_Phase3.md : Cas d'usage multi-TLP avec requêtes SPARQL Cross-TLP validées.

🐍 Scripts Applicatifs (03-Application/Phase3/)

generate_phase3_cti_abox.py : Module d'ingestion du flux JSON external_nvd_capec_feed.json et génération de DKG_ABox_CTI_External.ttl.

export_phase3_cti_md.py : Générateur de documentation miroir Markdown DKG_ABox_CTI_External.md avec schémas Mermaid et tables multi-hop.

schemas.py : Modèles Pydantic V2 (CtiFeedEntry, CisaKevEntry) pour la validation préalable des entrées.

test_phase3_cti_validation.py : Suite de recette PyTest automatisée (vérification du raccordement RBox, typage xsd:float/xsd:boolean et validation SHACL PySHACL).

📋 Checklist de Clôture Totale (Autosuffisance Garantie)

SSOT Intégré : config.py embarque toutes les constantes nécessaires aux Phase 1, 2 et 3 sans dépendance externe.

Schéma Complet : La chaîne RBox et le graphe Cross-TLP couvrent l'intégralité du parcours Asset ➔ ThreatPattern.

Validations Passées : PyTest à 100% (recette RDF + SHACL PySHACL sur l'union des graphes).

Passeport Phase 4 : Prêt à servir de kit d'entrée unique et autonome pour l'amorce de la Phase 4.