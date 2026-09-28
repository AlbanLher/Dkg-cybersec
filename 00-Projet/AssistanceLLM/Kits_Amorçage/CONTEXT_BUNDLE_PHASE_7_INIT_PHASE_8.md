context_bundle_cumulative:
  project_info:
    name: "DKG-CyberSec"
    vague: 3
    phase :P7"
    status: "🟢 PASSED"
    current_milestone: "Phase 7 Finalized - SOC Résidentiel & Local"
    environment:
      python_version: "3.14+"
      pytest_version: "9.1+"
      ssot_config: "03-Application/config.py"

context_bundle_cumulative:
  project_info:
    name: "DKG-CyberSec"
    version: "1.0.0-P07"
    status: "🟢 ALL_PHASES_PASSED"
    current_milestone: "Phase 7 Finalized - SOC Résidentiel & Local"
    environment:
      python_version: "3.14+"
      pytest_version: "9.1+"
      ssot_config: "03-Application/config.py"

  master_roadmap_reference: "Intégration de la Vue des Vagues (V1 à V6) & Vue des Spécifications (P1 à P8)"

  
  mandatory_context_checklist:
    - document: "Roadmap Vagues & Phases"
      purpose: "Cadrage macro, sens pédagogique et statut d'avancement global."
    - document: "Tableau des Spécifications (Spec Registry)"
      purpose: "Référentiel des spécifications par phase (Framework, Technique, Métier)."
    - document: "Tableau des Exigences (EXG-)"
      purpose: "Cahier des charges contractuel, unitaire et testable."
    - document: "Fichier de configuration unique (config.py)"
      purpose: "Source Unique de Vérité (SSOT) des chemins et paramètres techniques."

  architecture_topology:
    description: "Cartographie des flux, isolation des niveaux de classification et frontières d'exécution."
    layers:
      - layer_name: "Couche IHM / Client"
        components: ["Dashboard Streamlit / JS App", "API Gateway (FastAPI)"]
      - layer_name: "Couche Agents & Orchestration"
        components: ["Home SOC Orchestrator", "Agent MITM", "Agent Orchestrateur SOC (HitM)"]
      - layer_name: "Couche Sémantique & Moteur de Règles"
        components: ["TBox Master (OWL/SKOS/SHACL)", "Moteur d'Inférence SPARQL / pySHACL"]
      - layer_name: "Couche Données & Ségrégation TLP"
        components: 
          - "TLP:CLEAR (CTI Externe, Standards publics)"
          - "TLP:AMBER (Règles de gouvernance, TBox)"
          - "TLP:RED (Actifs du foyer, Vulnérabilités internes - Air-Gapped)"

  security_and_compliance:
    pydantic_mode: "ConfigDict(frozen=True)"
    time_standard: "datetime.now(timezone.utc)"
    shacl_validation: "Closed World Assumption (CWA)"
    tlp_matrix_rules:
      tlp_clear: "Données publiques et flux CTI externes partagés sans restriction."
      tlp_amber: "Données sensibles limitées au cercle interne de confiance et de gouvernance TBox."
      tlp_red: "Données hautement confidentielles du foyer, des actifs et des vulnérabilités (étanchéité absolue requise)."
    isolation_guarantee: "0 leakage of TLP:RED/AMBER triples to TLP:CLEAR tokens under any circumstances."