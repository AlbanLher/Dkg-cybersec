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

  global_roadmap_matrix:
    P01: { name: "Socle TBox & SKOS", status: "🟢 PASSED", scope: "TLP:AMBER", asset: "TBox Master & Rules" }
    P02: { name: "ABox & Instances Internal", status: "🟢 PASSED", scope: "TLP:RED", asset: "ABox Master Red" }
    P03: { name: "Ingestion CTI Externe", status: "🟢 PASSED", scope: "TLP:CLEAR", asset: "ABox CTI Feeds" }
    P04: { name: "CTI Textuelle & NLP", status: "🟢 PASSED", scope: "TLP:CLEAR", asset: "GLiNER NLP Annotations" }
    P05: { name: "Inférence & Agent MITM", status: "🟢 PASSED", scope: "TLP:RED", asset: "Agent MITM & Inferred Graph" }
    P06: { name: "API Gateway & Security Engine", status: "🟢 PASSED", scope: "CROSS-TLP", asset: "Gateway SPARQL & Audit Engine" }
    P07: { name: "SOC Résidentiel & Local", status: "🟢 PASSED", scope: "CROSS-TLP", asset: "Home SOC Orchestrator & UI" }

  validated_codebase:
    config_ssot: "03-Application/config.py"
    core_modules:
      p7_orchestrator: "03-Application/Phase7/home_soc_orchestrator.py"
      p7_local_agent: "03-Application/Phase7/local_inventory_agent.py"
      p7_cti_agent: "03-Application/Phase7/external_cti_agent.py"
      p7_api_backend: "03-Application/stage_2_decoupled_api/api_backend.py"
      p7_frontend: "03-Application/stage_2_decoupled_api/frontend_js/app.js"
    test_suites:
      p5_tests: "03-Application/Test/test_phase5_inference.py"
      p6_tests: "03-Application/Test/test_phase6_gateway.py"
      p7_tests: "03-Application/Test/test_phase7_residential.py"

  master_transversal_assets:
    directory: "02-Donnees/Master_Transversal/"
    graphs:
      - "TBOX_Master.ttl"
      - "ABox_Master_RED.ttl"
      - "CTI_CLEAR.ttl"
      - "ABox_Inferred_RED.ttl"
      - "abox_residential_family.ttl"
      - "abox_local_tlp_red.ttl"
    documentation_mirrors:
      - "DOC_Phase5_Inference_Master.md"
      - "DOC_Phase6_Gateway_Master.md"
      - "DOC_abox_residential_family.md"
      - "DOC_abox_local_tlp_red.md"

  specifications_registry:
    framework_specs:
      - "01-Principes_Spécifications/TRANSVERSAL/SPEC-FWK-P6_Matrice_Habilitations_TLP.md"
    technical_specs:
      - "01-Principes_Spécifications/USECASE_TECHNIQUE/SPEC-TEC-P06_API_Gateway_TLP.md"
      - "01-Principes_Spécifications/USECASE_TECHNIQUE/SPEC-TEC-P07_SOC_Residentiel.md"

  security_and_compliance:
    pydantic_mode: "ConfigDict(frozen=True)"
    time_standard: "datetime.now(timezone.utc)"
    shacl_validation: "Closed World Assumption (CWA)"
    isolation_guarantee: "0 leakage of TLP:RED/AMBER triples to TLP:CLEAR tokens"

  next_phase_bootstrap:
    target_phase: "Clôture du Projet / Déploiement Final et Archivage"
    inputs_required: "Full Cumulative Context Bundle P07"