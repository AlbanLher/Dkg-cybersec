```
"""
03-Application/config.py
Single Source of Truth (SSOT) - Configuration centralisée du projet DKG-CyberSec.

Répertoires                :    Préfixés par DIR_ (ex: DIR_TBOX_AMBER, DIR_ABOX_RED)
Fichiers RDF / Artefacts   :    Terminés par _PATH (ex: TBOX_MASTER_PATH, ABOX_RED_PATH)
Namespaces RDF             :    En MAJUSCULES (ex: DKG, DKG_DATA, SH)

"""

from pathlib import Path
from rdflib import Namespace


# ==========================================
# 1. CHEMINS DE REPERTOIRES (DIR)
# ==========================================

# Ancrage dynamique depuis 03-Application/config.py
DIR_APP = Path(__file__).resolve().parent
DIR_ROOT = DIR_APP.parent  # Pointe directement vers Workspace/
DIR_DATA = DIR_ROOT / "02-Donnees"

# (Phase1) Socle
DIR_SNAPSHOT_P1 = DIR_DATA / "Snapshots_Phases" / "Phase1_Socle"
DIR_MASTER_TBOX = DIR_DATA / "Master_Transversal" / "TLP_AMBER_Socle_TBox"

# (Phase2) ABoc
DIR_INPUT_P2 = DIR_DATA / "Input_Phases" / "Phase2_ABox"
DIR_SNAPSHOT_P2 = DIR_DATA / "Snapshots_Phases" / "Phase2_ABox"
DIR_MASTER_ABOX = DIR_DATA / "Master_Transversal" / "TLP_RED_Instances_ABox"


# (Phase3) Enrichissement Externe et non structuré + TLP
DIR_SNAPSHOT_P3 = DIR_DATA / "Snapshots_Phases" / "Phase3_Socle"

##  Découpage TLP Strict (Seiton 5S)
DIR_TBOX_AMBER = DIR_MASTER_TBOX
DIR_ABOX_RED = DIR_DATA / "Master_Transversal" / "TLP_RED_Instances_ABox"
DIR_CTI_CLEAR = DIR_DATA / "Master_Transversal" / "TLP_CLEAR_CTI_External"  # Wave 2 / Phase 3 & 4
DIR_INFERED_RED = DIR_DATA / "Master_Transversal" / "TLP_RED_Infered_Graph"  # Wave 3 / Phase 5

# (Phase4) Source des bulletins bruts pour le NER
DIR_SNAPSHOT_P4 = DIR_DATA / "Snapshots_Phases" / "Phase4_Socle"
DIR_UNSTRUCTURED_CTI = DIR_CTI_CLEAR / "Raw_Sources"

# (Phase5) A Locale
DIR_SNAPSHOT_P5 = DIR_DATA / "Snapshots_Phases" / "Phase5_Socle"
DIR_MODELS = DIR_APP / "models" / "cache"
DIR_NER_MODEL = DIR_MODELS / "ner"
DIR_EMBEDDING_MODEL = DIR_MODELS / "embeddings"

# Alias de répertoires pour la Phase 5 & Socle IA
# BASE_DIR = DIR_ROOT
# DATA_DIR = DIR_DATA
# APP_DIR = DIR_APP
# ONTOLOGY_DIR = DIR_ONTOLOGY





# ==========================================
# 2. ARTEFACTS ET FICHIERS RDF
# ==========================================

# TBox & SHACL (TLP:AMBER)
TBOX_MASTER_PATH  = DIR_MASTER_TBOX / "DKG_TBox_Master.ttl"
SHACL_MASTER_PATH = DIR_MASTER_TBOX / "DKG_SHACL_Master.ttl"

# ABox Interne (TLP:RED)
ABOX_MASTER_PATH = DIR_MASTER_ABOX / "DKG_ABox_Master.ttl"

# ABox CTI Externe (TLP:CLEAR) - Wave 2 / Phase 3 & 4
ABOX_CTI_PATH = DIR_CTI_CLEAR / "DKG_ABox_CTI_External.ttl"
DOC_CTI_MD_PATH = DIR_CTI_CLEAR / "DOC_SYNTHESE_ABOX_CTI.md"

# ABox & Règles d'Inférence (TLP:RED / TLP:AMBER) - Wave 3 / Phase 5
RULES_MASTER_PATH = DIR_TBOX_AMBER / "DKG_Rules_Master.ttl"
ABOX_INFERED_PATH = DIR_INFERED_RED / "DKG_ABox_Infered.ttl"
DOC_INFERED_MD_PATH = DIR_INFERED_RED / "DOC_SYNTHESE_ABOX_INFERED.md"


# ==========================================
# 3. SOCLE IA LOCAL (AIR-GAPPED / OFFLINE)
# ==========================================

# Identifiants HF pour le bootstrap (fetch_models.py)
NER_MODEL_NAME = "urchade/gliner_large-v2.1"
NER_FALLBACK_MODEL_NAME = "dslim/bert-base-NER"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Seuils de décision Agent MITM
MITM_SIMILARITY_THRESHOLD = 0.85



# ==========================================
# 4. NAMESPACES RDF CENTRALISÉS
# ==========================================
DKG_TBOX = Namespace("http://dkg.cybersec.org/tbox#")
DKG_DATA = Namespace("http://dkg.cybersec.org/data#")
DKG_CTI = Namespace("http://dkg.cybersec.org/cti#")  # Namespace CTI Externe

# Standard W3C Namespaces
SH = Namespace("http://www.w3.org/ns/shacl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")





```
