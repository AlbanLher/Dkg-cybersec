context_bundle_state_vector:
  project: "DKG-CyberSec"
  current_phase: "Phase X"
  status_summary: "P01-P0X PASSED"
  active_tsv_reference: "01-Principes_Spécifications/USECASE_TECHNIQUE/Specs_PhaseX.tsv"
  ssot_anchor: "03-Application/config.py"
  master_artifacts_registry:
    - "02-Donnees/Master_Transversal/TBOX_Master.ttl"
    - "02-Donnees/Master_Transversal/ABox_Master_RED.ttl"
  constraints_active:
    - "Pydantic V2 frozen=True"
    - "SHACL Closed World Assumption"
    - "Zero TLP Leakage"