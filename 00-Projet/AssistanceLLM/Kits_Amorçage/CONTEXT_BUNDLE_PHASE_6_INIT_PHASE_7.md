context_bundle_cumulative:
  project_info:
    name: "DKG-CyberSec"
    version: "1.0.0-P06"
    status: "🟢 ALL_PHASES_PASSED"
    current_milestone: "Phase 6 Finalized"
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

  validated_codebase:
    config_ssot: "03-Application/config.py"
    core_modules:
      p5_inference: "03-Application/Phase5/generate_phase5_inference.py"
      p5_mitm_agent: "03-Application/Phase5/mitm_agent.py"
      p6_schemas: "03-Application/Phase6/p6_schemas.py"
      p6_gateway: "03-Application/Phase6/api_gateway.py"
      p6_orchestrator: "03-Application/Phase6/generate_phase6_gateway.py"
    test_suites:
      p5_tests: "03-Application/Test/test_phase5_inference.py"
      p6_tests: "03-Application/Test/test_phase6_gateway.py"

  master_transversal_assets:
    directory: "02-Donnees/Master_Transversal/"
    graphs:
      - "TBOX_Master.ttl"
      - "ABox_Master_RED.ttl"
      - "CTI_CLEAR.ttl"
      - "ABox_Inferred_RED.ttl"
    documentation_mirrors:
      - "DOC_Phase5_Inference_Master.md"
      - "DOC_Phase6_Gateway_Master.md"

  specifications_registry:
    framework_specs:
      - "01-Principes_Spécifications/TRANSVERSAL/SPEC-FWK-P6_Matrice_Habilitations_TLP.md"
    technical_specs:
      - "01-Principes_Spécifications/USECASE_TECHNIQUE/SPEC-TEC-P06_API_Gateway_TLP.md"

  security_and_compliance:
    pydantic_mode: "ConfigDict(frozen=True)"
    time_standard: "datetime.now(timezone.utc)"
    shacl_validation: "Closed World Assumption (CWA)"
    isolation_guarantee: "0 leakage of TLP:RED/AMBER triples to TLP:CLEAR tokens"

  next_phase_bootstrap:
    target_phase: "Phase 7 - Orchestration Globale & Déploiement CI/CD"
    inputs_required: "Full Cumulative Context Bundle"