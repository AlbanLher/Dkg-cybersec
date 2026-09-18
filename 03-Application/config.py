"""
03-Application/config.py
Single Source of Truth (SSOT) - Configuration centralisée du projet DKG-CyberSec.
Sécurisé et validé par Pydantic V2 (EXG-OR-05, EXG-OR-07).
Phase 6 Active : Support API Gateway, Security Engine & Isolation TLP.
"""

from pathlib import Path
from typing import Annotated, List
from rdflib import Namespace
from pydantic import Field, AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DKGConfig(BaseSettings):
    """
    Modèle Pydantic V2 centralisant et validant l'intégralité des paramètres applicatifs.
    """
    model_config = SettingsConfigDict(
        env_prefix="DKG_",
        env_file=".env",
        extra="ignore"
    )

    # --------------------------------------------------------------------------
    # 1. SOCLE REPERTOIRES
    # --------------------------------------------------------------------------
    dir_app: Path = Field(default_factory=lambda: Path(__file__).resolve().parent)
    
    @property
    def dir_root(self) -> Path:
        return self.dir_app.parent

    @property
    def dir_data(self) -> Path:
        return self.dir_root / "02-Donnees"

    # Répertoires Snapshots & Masters (Phases 1 à 4)
    @property
    def dir_snapshot_p1(self) -> Path:
        return self.dir_data / "Snapshots_Phases" / "Phase1_Socle"

    @property
    def dir_master_tbox(self) -> Path:
        return self.dir_data / "Master_Transversal" / "TLP_AMBER_Socle_TBox"

    @property
    def dir_input_p2(self) -> Path:
        return self.dir_data / "Input_Phases" / "Phase2_ABox"

    @property
    def dir_snapshot_p2(self) -> Path:
        return self.dir_data / "Snapshots_Phases" / "Phase2_ABox"

    @property
    def dir_master_abox(self) -> Path:
        return self.dir_data / "Master_Transversal" / "TLP_RED_Instances_ABox"

    @property
    def dir_inputs_p3(self) -> Path:
        return self.dir_data / "Input_Phases" / "Phase3_CTI"

    @property
    def dir_snapshot_p3(self) -> Path:
        return self.dir_data / "Snapshots_Phases" / "Phase3_CTI"

    @property
    def dir_cti_abox(self) -> Path:
        return self.dir_data / "Master_Transversal" / "TLP_CLEAR_CTI_External"

    # Découpage TLP
    @property
    def dir_tbox_amber(self) -> Path:
        return self.dir_master_tbox

    @property
    def dir_abox_red(self) -> Path:
        return self.dir_master_abox

    @property
    def dir_cti_clear(self) -> Path:
        return self.dir_cti_abox

    @property
    def dir_infered_red(self) -> Path:
        return self.dir_data / "Master_Transversal" / "TLP_RED_Infered_Graph"

    @property
    def dir_inputs_p4(self) -> Path:
        return self.dir_data / "Input_Phases" / "Phase4_CTI"

    @property
    def dir_snapshot_p4(self) -> Path:
        return self.dir_data / "Snapshots_Phases" / "Phase4_CTI"

    @property
    def dir_unstructured_cti(self) -> Path:
        return self.dir_cti_clear / "Raw_Sources"

    # Répertoires Phase 5 (Reasoning & MITM)
    @property
    def dir_snapshot_p5(self) -> Path:
        return self.dir_data / "Snapshots_Phases" / "Phase5_Reasoning_MITM"

    @property
    def dir_models(self) -> Path:
        return self.dir_app / "models" / "cache"

    @property
    def dir_embedding_model(self) -> Path:
        return self.dir_models / "embeddings"

    @property
    def dir_ner_model(self) -> Path:
        return self.dir_models / "ner"

    # Répertoires Phase 6 (API Gateway & Security)
    @property
    def dir_snapshot_p6(self) -> Path:
        return self.dir_data / "Snapshots_Phases" / "Phase6_API_Gateway"

    @property
    def dir_inputs_p6(self) -> Path:
        return self.dir_data / "Input_Phases" / "Phase6_API_Gateway"

    @property
    def dir_projet_p6(self) -> Path:
        return self.dir_root / "00-Projet" / "Phase6"

    # Phase 7 Foyer 
    @property
    def dir_snapshot_p7(self) -> Path:
        return self.dir_data / "Snapshots_Phases" / "Phase7_Residential_Box"

    @property
    def dir_inputs_p7(self) -> Path:
        return self.dir_data / "Input_Phases" / "Phase7_Residential_Box"

    @property
    def dir_projet_p7(self) -> Path:
        return self.dir_root / "00-Projet" / "Phase7"

    @property
    def dir_private_red(self) -> Path:
        return self.dir_root / ".private"

    # --------------------------------------------------------------------------
    # 2. SEUILS & PARAMETRES IA
    # --------------------------------------------------------------------------
    embedding_model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    mitm_similarity_threshold: float = Field(default=0.85, ge=0.0, le=1.0)
    
    ner_model_name: str = Field(default="urchade/gliner_large-v2.1")
    ner_fallback_model_name: str = Field(default="dslim/bert-base-NER")

    # --------------------------------------------------------------------------
    # 3. NAMESPACES RDF (Validation d'URL)
    # --------------------------------------------------------------------------
    dkg_tbox_uri: str = "http://dkg.cybersec.org/tbox#"
    dkg_data_uri: str = "http://dkg.cybersec.org/data#"
    dkg_cti_uri: str = "http://dkg.cybersec.org/cti#"

    @field_validator("dkg_tbox_uri", "dkg_data_uri", "dkg_cti_uri")
    @classmethod
    def validate_rdf_uri(cls, v: str) -> str:
        if not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError(f"L'URI RDF doit débuter par http:// ou https:// : {v}")
        if not (v.endswith("#") or v.endswith("/")):
            raise ValueError(f"L'URI de namespace RDF doit se terminer par '#' ou '/' : {v}")
        return v

    def ensure_directories_exist(self) -> None:
        """Garantit l'existence de tous les dossiers critiques au lancement."""
        target_dirs = [
            self.dir_master_tbox, self.dir_master_abox, self.dir_cti_abox,
            self.dir_inputs_p3,  self.dir_snapshot_p3,
            self.dir_inputs_p4,  self.dir_snapshot_p4,
            self.dir_infered_red, self.dir_models, self.dir_embedding_model,
            self.dir_ner_model, self.dir_snapshot_p5,
            self.dir_inputs_p6,  self.dir_snapshot_p6, self.dir_projet_p6,
            self.dir_inputs_p7,  self.dir_snapshot_p7, self.dir_projet_p7,
            self.dir_private_red
        ]
        for d in target_dirs:
            d.mkdir(parents=True, exist_ok=True)


# ==============================================================================
# INSTANCIATION & EXPORT COMPATIBLE (SSOT)
# ==============================================================================
_settings = DKGConfig()
_settings.ensure_directories_exist()

# 1. CHEMINS DE REPERTOIRES (DIR_)
DIR_APP = _settings.dir_app
DIR_ROOT = _settings.dir_root
DIR_DATA = _settings.dir_data

DIR_SNAPSHOT_P1 = _settings.dir_snapshot_p1
DIR_MASTER_TBOX = _settings.dir_master_tbox

DIR_INPUT_P2 = _settings.dir_input_p2
DIR_SNAPSHOT_P2 = _settings.dir_snapshot_p2
DIR_MASTER_ABOX = _settings.dir_master_abox

DIR_INPUTS_P3 = _settings.dir_inputs_p3
DIR_SNAPSHOT_P3 = _settings.dir_snapshot_p3
DIR_CTI_ABOX = _settings.dir_cti_abox

DIR_TBOX_AMBER = _settings.dir_tbox_amber
DIR_ABOX_RED = _settings.dir_abox_red
DIR_CTI_CLEAR = _settings.dir_cti_clear
DIR_INFERED_RED = _settings.dir_infered_red

DIR_INPUTS_P4 = _settings.dir_inputs_p4
DIR_SNAPSHOT_P4 = _settings.dir_snapshot_p4
DIR_UNSTRUCTURED_CTI = _settings.dir_unstructured_cti

DIR_SNAPSHOT_P5 = _settings.dir_snapshot_p5
DIR_MODELS = _settings.dir_models
DIR_EMBEDDING_MODEL = _settings.dir_embedding_model
DIR_NER_MODEL = _settings.dir_ner_model

DIR_SNAPSHOT_P6 = _settings.dir_snapshot_p6
DIR_INPUTS_P6 = _settings.dir_inputs_p6
DIR_PROJET_P6 = _settings.dir_projet_p6

DIR_SNAPSHOT_P7 = _settings.dir_snapshot_p7
DIR_INPUTS_P7 = _settings.dir_inputs_p7
DIR_PROJET_P7 = _settings.dir_projet_p7

PROJECT_ROOT = _settings.dir_root
DIR_PRIVATE_RED = _settings.dir_private_red
DIR_PRIVATE_RED.mkdir(parents=True, exist_ok=True)

# 2. ARTEFACTS ET FICHIERS RDF (_PATH)
TBOX_MASTER_PATH = DIR_MASTER_TBOX / "DKG_TBox_Master.ttl"
TBOX_MASTER_MD_PATH = DIR_MASTER_TBOX / "DKG_TBox_Master.md"

SHACL_MASTER_PATH = DIR_MASTER_TBOX / "DKG_SHACL_Master.ttl"
SHACL_MASTER_MD_PATH = DIR_MASTER_TBOX / "DKG_SHACL_Master.md"

ABOX_MASTER_PATH = DIR_MASTER_ABOX / "DKG_ABox_Master.ttl"
ABOX_MASTER_MD_PATH = DIR_MASTER_ABOX / "DKG_ABox_Master.md"

ABOX_RED_PATH = ABOX_MASTER_PATH

INPUT_CTI_JSON_PATH = DIR_INPUTS_P3 / "external_nvd_capec_feed.json"
ABOX_CTI_PATH = DIR_CTI_CLEAR / "DKG_ABox_CTI_External.ttl"
ABOX_CTI_MD_PATH = DIR_CTI_CLEAR / "DKG_ABox_CTI_External.md"

INPUT_CTI_U_JSON_PATH = DIR_INPUTS_P4 / "bulletin_apt29.txt"
ABOX_CTI_U_PATH = DIR_CTI_CLEAR / "DKG_ABox_CTI_U_External.ttl"
ABOX_CTI_U_MD_PATH = DIR_CTI_CLEAR / "DKG_ABox_CTI_U_External.md"

RULES_MASTER_PATH = DIR_TBOX_AMBER / "DKG_Rules_Master.ttl"
RULES_MASTER_MD_PATH = DIR_TBOX_AMBER / "DKG_Rules_Master.md"

ABOX_INFERED_PATH = DIR_INFERED_RED / "DKG_ABox_Infered.ttl"
ABOX_INFERED_MD_PATH = DIR_INFERED_RED / "DKG_ABox_Infered.md"

INPUT_P6_QUERY_PAYLOAD = DIR_INPUTS_P6 / "sample_query_payloads.json"
PATH_P6_GATEWAY_LOG = DIR_SNAPSHOT_P6 / "api_gateway_audit.log"

INPUT_RESIDENTIAL_JSON_PATH = DIR_INPUTS_P7 / "input_residential_family_env.json"
ABOX_RESIDENTIAL_PATH = DIR_SNAPSHOT_P7 / "DKG_ABox_Residential.ttl"

EXTERNAL_SOURCES_CONFIG_PATH = DIR_INPUTS_P7 / "external_sources_config.json"
EXTERNAL_SOURCES_CATALOG_PATH = DIR_INPUTS_P7 / "external_sources_catalog.json"

# Chemins TLP:RED sécurisés et non versionnés
SECURE_INPUT_RESIDENTIAL_PATH = DIR_PRIVATE_RED / "input_residential_family_env.json"
SECURE_ABOX_RESIDENTIAL_PATH = DIR_PRIVATE_RED / "DKG_ABox_Residential.ttl"


# Paramètres de Sécurité & Filtrage TLP
API_GATEWAY_HOST = "127.0.0.1"
API_GATEWAY_PORT = 8000
TLP_CLEAR_READ_GRAPH = [ABOX_CTI_PATH, ABOX_CTI_U_PATH]
TLP_AMBER_READ_GRAPH = TLP_CLEAR_READ_GRAPH + [TBOX_MASTER_PATH]
TLP_RED_READ_GRAPH = TLP_AMBER_READ_GRAPH + [ABOX_MASTER_PATH, ABOX_INFERED_PATH]

# 3. SOCLE IA LOCAL
EMBEDDING_MODEL_NAME = _settings.embedding_model_name
MITM_SIMILARITY_THRESHOLD = _settings.mitm_similarity_threshold
NER_MODEL_NAME = _settings.ner_model_name
NER_FALLBACK_MODEL_NAME = _settings.ner_fallback_model_name

# 4. NAMESPACES RDF CENTRALISÉS
DKG_TBOX = Namespace(_settings.dkg_tbox_uri)
DKG_DATA = Namespace(_settings.dkg_data_uri)
DKG_CTI = Namespace(_settings.dkg_cti_uri)

SH = Namespace("http://www.w3.org/ns/shacl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
