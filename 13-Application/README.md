# 📁 Structure des Scripts

## Phase 1 (TBox)
- `phase1/build_tbox.py` : Fusion lexique + ontologie
- `phase1/validate_tbox.py` : Vérification cohérence
- `phase1/generate_versions.py` : Génération .ttl/.md/.json

## Phase 2 (ABox)
- `phase2/orchestrator.py` : Pipeline d'ingestion
- `phase2/connectors/` : JSON/PDF/Logs
- `phase2/ner/` : Extraction d'entités