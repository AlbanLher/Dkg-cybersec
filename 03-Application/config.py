"""
03-Application/config.py
Single Source of Truth (SSOT) - Configuration centralisée du projet DKG-CyberSec.
"""
from pathlib import Path
from rdflib import Namespace

# ==========================================
# 1. CHEMINS DE REPERTOIRES (DIR)
# ==========================================
DIR_ROOT = Path(__file__).resolve().parent.parent
DIR_DATA = DIR_ROOT / "02-Donnees"
DIR_MASTER = DIR_DATA / "Master_Transversal"

# Découpage TLP Strict (Seiton 5S)
DIR_TBOX_AMBER = DIR_MASTER / "TLP_AMBER_Socle_TBox"
DIR_ABOX_RED = DIR_MASTER / "TLP_RED_Instances_ABox"
DIR_CTI_CLEAR = DIR_MASTER / "TLP_CLEAR_CTI_External"  # Wave 2 / Phase 3 & 4
DIR_INFERED_RED = DIR_MASTER / "TLP_RED_Infered_Graph"  # Wave 3 / Phase 5

# Source des bulletins bruts pour le NER (Phase 4)
DIR_UNSTRUCTURED_CTI = DIR_CTI_CLEAR / "Raw_Sources"

# ==========================================
# 2. ARTEFACTS ET FICHIERS RDF
# ==========================================
# TBox & SHACL combinés (TLP:AMBER)
TBOX_MASTER_PATH = DIR_TBOX_AMBER / "DKG_TBox_Master.ttl"
SHACL_MASTER_PATH = TBOX_MASTER_PATH  # Modèles & formes SHACL combinés dans la TBox

# ABox Interne (TLP:RED)
ABOX_RED_PATH = DIR_ABOX_RED / "DKG_ABox_Master.ttl"

# ABox CTI Externe (TLP:CLEAR) - Wave 2 / Phase 3 & 4
ABOX_CTI_PATH = DIR_CTI_CLEAR / "DKG_ABox_CTI_External.ttl"
DOC_CTI_MD_PATH = DIR_CTI_CLEAR / "02_SYNTHESE_ABOX_CTI.md"

# ABox & Règles d'Inférence (TLP:RED / TLP:AMBER) - Wave 3 / Phase 5
RULES_MASTER_PATH = DIR_TBOX_AMBER / "DKG_Rules_Master.ttl"
ABOX_INFERED_PATH = DIR_INFERED_RED / "DKG_ABox_Infered.ttl"
DOC_INFERED_MD_PATH = DIR_INFERED_RED / "02_SYNTHESE_ABOX_INFERED.md"

# ==========================================
# 3. NAMESPACES RDF CENTRALISÉS
# ==========================================
DKG = Namespace("http://dkg.cybersec.org/schema#")
DKG_DATA = Namespace("http://dkg.cybersec.org/data#")
DKG_CTI = Namespace("http://dkg.cybersec.org/cti#")  # Namespace CTI Externe
