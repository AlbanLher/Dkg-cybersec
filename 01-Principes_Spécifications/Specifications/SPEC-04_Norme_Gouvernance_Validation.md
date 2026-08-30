_(Transverse : Pipeline CI/CD, PySHACL & Tests)_

**Périmètre :** Transverse — Contrôle automatisé de conformité par SHACL, PyTest et SPARQL ASK.

### Système de Numérotation des Exigences : `EXG-GOV-*`

#### 1. Validation SHACL Automatisée

- **`EXG-GOV-01` (Gatekeeper SHACL)** : Le pipeline d'ingestion (Phase 2) doit exécuter un contrôle **PySHACL** avec les formes définies dans `12-Donnees/SHACL_Shapes/shapes_abox.ttl`. Tout échec de validation doit immédiatement interrompre le processus et empêcher la sauvegarde sur disque.
    
- **`EXG-GOV-02` (Co-évolution TBox / SHACL Shapes)** : À chaque modification ou ajout de concept dans la TBox (`SPEC-01`), la Shape SHACL associée (`SPEC-04`) doit être mise à jour pour refléter les nouvelles règles d'obligation (`sh:minCount`, `sh:datatype`).
    

#### 2. Tests Unitaires de Structure (PyTest & SPARQL ASK)

- **`EXG-GOV-03` (Assertions de Schéma - Phase 1)** : Un test unitaire (`tests/test_phase1_tbox.py`) doit exécuter une requête SPARQL `ASK` pour valider la conformité des domaines/portées et l'existence des classes fondamentales avant le lancement de la Phase 2.
    
- **`EXG-GOV-04` (Diagnostic Pré-vol Applicatif - Phase 3)** : Avant d'exécuter la requête métier globale, l'application Phase 3 doit exécuter un contrôle `ASK` vérifiant la présence d'au moins une chaîne complète d'information (`Asset -> Component -> Vulnerability -> CVSS`). En cas de retour `False`, l'application produit un rapport d'erreur explicite au lieu de renvoyer un tableau vide.