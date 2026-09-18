# 🔧 Prompt 2/3 — Code, Data Pipeline & Tests PyTest (Axé TSV & SSOT)

## 📌 Fichiers à joindre obligatoirement dans votre message :
1. `03-Application/config.py`
2. Le fichier **TSV de Spécifications/Exigences** de la Phase active (ex: `01-Principes_Spécifications/.../Specs_PhaseX.tsv`)
3. `00-Projet/PhaseX/Phase_Content.md`

## Périmètre d'Action & Décomposition Systémique
- Traiter le problème par **modules sous-systèmes** indépendants définis dans le TSV.
- Pour chaque module, implémenter le triptyque : `Schéma Pydantic/Config` ➔ `Logique Métier / RDF` ➔ `Test PyTest associé`.

## 📋 Directives & Check-list Qualité Code
- [ ] **Traçabilité TSV :** Chaque fonction ou test unitaire doit inclure en docstring l'ID exact de l'exigence du TSV (ex: `# [EXG-INF-01]`).
- [ ] **SSOT Strict :** 100% des chemins et namespaces proviennent de `config.py`.
- [ ] **Conformité Pydantic V2 :** Utilisation de `ConfigDict(frozen=True)`.
- [ ] **Validation SHACL CWA & PyTest :** Couverture totale des critères d'acceptation du TSV.