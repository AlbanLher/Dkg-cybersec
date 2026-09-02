# 🔧 Module Développement & Data Pipeline (`[CONTEXT: DEV]`)

## Périmètre d'Action
- Répertoire : `03-Application/`, `tests/`, fichiers `.ttl`
- Objectif : Scripting Python (rdflib, pyshacl), requêtes SPARQL, règles d'inférence, tests Pytest.

## 📋 Check-list Qualité Code & Data (À valider obligatoirement)
- [ ] **SSOT Imports :** 100% des constantes de chemins/namespaces proviennent de `config.py` (aucune variable en dur).
- [ ] **Turtle Valid :** Tous les fichiers Turtle générés contiennent l'en-tête `@prefix sh:` et les namespaces du projet.
- [ ] **Pytest Parity :** Les fixtures Pytest chargent l'union des graphes (`TBOX_MASTER_PATH`, `ABOX_RED_PATH`, `ABOX_CTI_PATH`).
- [ ] **CI Ready :** Les scripts et tests exécutables sont compatibles avec le pipeline GitHub Actions (`.github/workflows/ci.yml`).