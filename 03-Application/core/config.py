"""
03-Application/config.py
Single Source of Truth (SSOT) - Configuration centralisée du projet DKG-CyberSec.
Sécurisé et validé par Pydantic V2 (EXG-FWK-P1-GOU_5, GOU_7).
Phase 8 Active : Démonstrateur Seed/Reset, HITL, Simulateur (résolution canonique).
"""

from pathlib import Path
from rdflib import Namespace
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DKGConfig(BaseSettings):
    """Modèle Pydantic V2 centralisant et validant l'intégralité des paramètres.
    Sections : socle P1-P7, démonstrateur P8 (seed TLP-segmenté + workset),
    seuils IA, namespaces RDF."""

    model_config = SettingsConfigDict(
        env_prefix="DKG_",
        env_file=".env",
        extra="ignore"
    )

    # ==========================================================================
    # 1. SOCLE REPERTOIRES (P1 -> P7)
    # ==========================================================================
    dir_app: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent)

    @property
    def dir_root(self) -> Path:
        return self.dir_app.parent

    @property
    def dir_data(self) -> Path:
        return self.dir_root / "02-Donnees"

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
        return self.dir_cti_abox / "Raw_Sources"

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

    @property
    def dir_snapshot_p6(self) -> Path:
        return self.dir_data / "Snapshots_Phases" / "Phase6_API_Gateway"

    @property
    def dir_inputs_p6(self) -> Path:
        return self.dir_data / "Input_Phases" / "Phase6_API_Gateway"

    @property
    def dir_projet_p6(self) -> Path:
        return self.dir_root / "00-Projet" / "Phase6"

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

    @property
    def dir_snapshot_p8(self) -> Path:
        return self.dir_data / "Snapshots_Phases" / "Phase8_Compliance"

    @property
    def dir_inputs_p8(self) -> Path:
        return self.dir_data / "Input_Phases" / "Phase8_Compliance"

    @property
    def dir_projet_p8(self) -> Path:
        return self.dir_root / "00-Projet" / "Phase8"

    # ==========================================================================
    # 1.bis DÉMONSTRATEUR P8 — SEED (TLP-segmenté, EXG-MET-P8-RES_1, §31)
    # ==========================================================================
    @property
    def dir_seed_p8(self) -> Path:
        return self.dir_inputs_p8 / "seed"

    @property
    def dir_seed_tbox_amber(self) -> Path:
        return self.dir_seed_p8 / "TLP_AMBER_Socle_TBox"

    @property
    def dir_seed_abox_red(self) -> Path:
        return self.dir_seed_p8 / "TLP_RED_Instances_ABox"

    @property
    def dir_seed_cti_clear(self) -> Path:
        return self.dir_seed_p8 / "TLP_CLEAR_CTI_External"

    @property
    def seed_tbox_demo_path(self) -> Path:
        return self.dir_seed_tbox_amber / "DKG_TBox_DemoRef.ttl"

    @property
    def seed_shacl_demo_path(self) -> Path:
        return self.dir_seed_tbox_amber / "DKG_SHACL_DemoRef.ttl"

    @property
    def seed_rules_demo_path(self) -> Path:
        return self.dir_seed_tbox_amber / "DKG_Rules_DemoRef.ttl"

    @property
    def seed_abox_foyer_path(self) -> Path:
        return self.dir_seed_abox_red / "DKG_ABox_Residential.ttl"

    @property
    def seed_abox_hote_path(self) -> Path:
        return self.dir_seed_abox_red / "DKG_ABox_Master.ttl"

    @property
    def seed_cti_clear_path(self) -> Path:
        return self.dir_seed_cti_clear / "DKG_ABox_CTI_External.ttl"

    # ==========================================================================
    # 1.ter DÉMONSTRATEUR P8 — WORKING SET (seul espace écrit par la démo)
    # ==========================================================================
    @property
    def dir_workset_p8(self) -> Path:
        return self.dir_snapshot_p8 / "workset"

    @property
    def dir_workset_tbox_amber(self) -> Path:
        return self.dir_workset_p8 / "TLP_AMBER_Socle_TBox"

    @property
    def dir_workset_abox_red(self) -> Path:
        return self.dir_workset_p8 / "TLP_RED_Instances_ABox"

    @property
    def dir_workset_cti_clear(self) -> Path:
        return self.dir_workset_p8 / "TLP_CLEAR_CTI_External"

    # ==========================================================================
    # 2. SEUILS & PARAMETRES IA
    # ==========================================================================
    embedding_model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    mitm_similarity_threshold: float = Field(default=0.85, ge=0.0, le=1.0)

    ner_model_name: str = Field(default="urchade/gliner_large-v2.1")
    ner_fallback_model_name: str = Field(default="dslim/bert-base-NER")

    # ==========================================================================
    # 3. NAMESPACES RDF (Validation d'URL)
    # ==========================================================================
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

    # ==========================================================================
    # 4. PASSERELLE API (env-driven, GOU_5)
    # ==========================================================================
    api_gateway_host: str = Field(default="127.0.0.1")
    api_gateway_port: int = Field(default=8000, ge=1, le=65535)

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
            self.dir_private_red,
            self.dir_inputs_p8,  self.dir_snapshot_p8, self.dir_projet_p8,
            # Démonstrateur : seed (lecture seule) + workset (écriture démo)
            self.dir_seed_tbox_amber, self.dir_seed_abox_red,
            self.dir_seed_cti_clear,
            self.dir_workset_tbox_amber, self.dir_workset_abox_red,
            self.dir_workset_cti_clear,
        ]
        for d in target_dirs:
            d.mkdir(parents=True, exist_ok=True)


class DemoConfig(BaseSettings):
    """Profil de démo + paramètres Simulateur (EXG-FWK-P8-SIM_1..4).
    Classe SÉPARÉE du SSOT principal (GOU_5 : un seul config.py, deux modèles)."""

    model_config = SettingsConfigDict(
        env_prefix="DKG_DEMO_",
        env_file=".env",
        extra="ignore"
    )

    # Profil d'ABox au lancement : foyer | hote (EXG-MET-P8-DEM_1, toggle IHM)
    profile: str = Field(default="foyer", pattern="^(foyer|hote)$")

    # Personas du Simulateur (EXG-FWK-P8-SIM_1) — défaut rév.2 (~3 actifs/pers, ×4 composants)
    persona_foyer_actifs: int = Field(default=5, ge=1)
    persona_startup_actifs: int = Field(default=60, ge=1)
    persona_pme_actifs: int = Field(default=250, ge=1)
    persona_eti_actifs: int = Field(default=800, ge=1)
    composants_par_actif: int = Field(default=4, ge=1, le=20)
    cve_par_composant: float = Field(default=0.5, ge=0.0, le=1.0)

    # Seuil de recette Green (EXG-FWK-P8-AGE_2)
    bilan_max_seconds: float = Field(default=1.0, gt=0.0)


# ==============================================================================
# INSTANCIATION & EXPORTS (SSOT)
# ==============================================================================
_settings = DKGConfig()
_settings.ensure_directories_exist()
_demo = DemoConfig()

# --- 1. CHEMINS DE REPERTOIRES ---
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
DIR_TBOX_AMBER = _settings.dir_master_tbox
DIR_ABOX_RED = _settings.dir_master_abox
DIR_CTI_CLEAR = _settings.dir_cti_abox
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
DIR_PRIVATE_RED = _settings.dir_private_red
DIR_INPUTS_P8 = _settings.dir_inputs_p8
DIR_SNAPSHOT_P8 = _settings.dir_snapshot_p8
DIR_PROJET_P8 = _settings.dir_projet_p8          # (coquille dir_projet_p8i corrigée)

# Démonstrateur : SEED (lecture seule) + WORKSET (seul espace écrit, TLP-segmenté)
DIR_SEED_P8 = _settings.dir_seed_p8
DIR_WORKSET_P8 = _settings.dir_workset_p8
DIR_WORKSET_TBOX_AMBER = _settings.dir_workset_tbox_amber
DIR_WORKSET_ABOX_RED = _settings.dir_workset_abox_red
DIR_WORKSET_CTI_CLEAR = _settings.dir_workset_cti_clear

SEED_TBOX_DEMO_PATH = _settings.seed_tbox_demo_path
SEED_SHACL_DEMO_PATH = _settings.seed_shacl_demo_path
SEED_RULES_DEMO_PATH = _settings.seed_rules_demo_path
SEED_ABOX_FOYER_PATH = _settings.seed_abox_foyer_path
SEED_ABOX_HOTE_PATH = _settings.seed_abox_hote_path
SEED_CTI_CLEAR_PATH = _settings.seed_cti_clear_path

WORKSET_TBOX_PATH = DIR_WORKSET_TBOX_AMBER / "DKG_TBox_Working.ttl"
WORKSET_RULES_PATH = DIR_WORKSET_TBOX_AMBER / "DKG_Rules_Working.ttl"
WORKSET_CTI_BUFFER_PATH = DIR_WORKSET_CTI_CLEAR / "selected_cti_clear_buffer.ttl"
WORKSET_HITL_AUDIT_LOG_PATH = DIR_WORKSET_TBOX_AMBER / "hitl_validation_audit.log"
WORKSET_SIM_ABAQUE_PATH = DIR_WORKSET_TBOX_AMBER / "abaques"
WORKSET_RESOURCE_REPORT_PATH = DIR_WORKSET_TBOX_AMBER / "resource_profile_report.json"

# --- 2. ARTEFACTS ET FICHIERS RDF (_PATH) ---
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

DELTA_BUFFER_PATH = DIR_SNAPSHOT_P8 / "frugal_delta_buffer.ttl"     # legacy (frugal_engine)
SOC_AUDIT_REPORT_PATH = DIR_SNAPSHOT_P8 / "soc_audit_compliance_report.json"

# TLP:RED sécurisés et non versionnés
SECURE_INPUT_RESIDENTIAL_PATH = DIR_PRIVATE_RED / "input_residential_family_env.json"
SECURE_ABOX_RESIDENTIAL_PATH = DIR_PRIVATE_RED / "DKG_ABox_Residential.ttl"

# Registres Phase 8
INPUT_P8_REGULATION_PATH = DIR_INPUTS_P8 / "external_sources_compliance_registry.json"
EXTERNAL_SOURCES_COMPLIANCE_REGISTRY_PATH = INPUT_P8_REGULATION_PATH
ABOX_COMPLIANCE_STANDARDS_CLEAR_PATH = DIR_CTI_CLEAR / "abox_compliance_standards_clear.ttl"

# --- 3. PARAMÈTRES DÉMO & SIMULATEUR ---
DEMO_PROFILE = _demo.profile
SIM_PERSONAS = {
    "foyer": _demo.persona_foyer_actifs,
    "startup": _demo.persona_startup_actifs,
    "pme": _demo.persona_pme_actifs,
    "eti": _demo.persona_eti_actifs,
}
SIM_COMPOSANTS_PAR_ACTIF = _demo.composants_par_actif
SIM_CVE_PAR_COMPOSANT = _demo.cve_par_composant
BILAN_MAX_SECONDS = _demo.bilan_max_seconds

# --- 4. PASSERELLE API (env-driven) ---
API_GATEWAY_HOST = _settings.api_gateway_host
API_GATEWAY_PORT = _settings.api_gateway_port

# --- 5. GRAPHS DE LECTURE TLP (empilement par niveau d'accès) ---
TLP_CLEAR_READ_GRAPH = [ABOX_CTI_PATH, ABOX_CTI_U_PATH]
TLP_AMBER_READ_GRAPH = TLP_CLEAR_READ_GRAPH + [TBOX_MASTER_PATH]
TLP_RED_READ_GRAPH = TLP_AMBER_READ_GRAPH + [ABOX_MASTER_PATH, ABOX_INFERED_PATH]

# --- 6. SOCLE IA LOCAL ---
EMBEDDING_MODEL_NAME = _settings.embedding_model_name
MITM_SIMILARITY_THRESHOLD = _settings.mitm_similarity_threshold
NER_MODEL_NAME = _settings.ner_model_name
NER_FALLBACK_MODEL_NAME = _settings.ner_fallback_model_name

# --- 7. NAMESPACES RDF CENTRALISÉS ---
DKG_TBOX = Namespace(_settings.dkg_tbox_uri)
DKG_DATA = Namespace(_settings.dkg_data_uri)
DKG_CTI = Namespace(_settings.dkg_cti_uri)

SH = Namespace("http://www.w3.org/ns/shacl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
