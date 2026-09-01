#!/usr/bin/env python3
"""
config.py - Source unique de vérité du pipeline DKG-CyberSec.
Mis à jour automatiquement / manuellement à chaque Bilan de Phase.
"""
from pathlib import Path
from rdflib import Namespace

# --- 1. ARBORESCENCE ET RACINE ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 2. CHEMINS DES ARTEFACTS (Mis à jour au Bilan Phase 1 & 2) ---
DIR_DONNEES = BASE_DIR / "02-Donnees"
DIR_MASTER = DIR_DONNEES / "Master_Transversal"
DIR_SOCLE_TBOX = DIR_MASTER / "TLP_AMBER_Socle_TBox"
DIR_INSTANCES_ABOX = DIR_MASTER / "TLP_RED_Instances_ABox"

# Phase 1: TBox & SHACL
TBOX_MASTER_PATH = DIR_SOCLE_TBOX / "DKG_TBox_Master.ttl"
SHACL_MASTER_PATH = TBOX_MASTER_PATH  # Modèles & formes SHACL combinés dans la TBox

# Phase 2: ABox
ABOX_MASTER_PATH = DIR_INSTANCES_ABOX / "DKG_ABox_Master.ttl"

# --- 3. NAMESPACES CANONIQUES ---
DKG_PREFIX = "http://dkg.cybersec.org/schema#"
DKG_DATA_PREFIX = "http://dkg.cybersec.org/data/"

DKG = Namespace(DKG_PREFIX)
DKG_DATA = Namespace(DKG_DATA_PREFIX)
