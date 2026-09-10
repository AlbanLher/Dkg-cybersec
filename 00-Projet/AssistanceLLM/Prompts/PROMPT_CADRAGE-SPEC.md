# 📐 Prompt 1/3 — Cadrage & Spécifications Phase X (`[CONTEXT: CADRAGE-SPEC]`)

## 📌 Fichiers à joindre obligatoirement dans votre message :
1. `03-Application/config.py` (SSOT Actuel)
2. `Roadmap_Suivi-Avancement.md` (Vision Roadmap globale)
3. Fichier de synthèse de la Phase N-1 (ex: `Phase_Content.md, DOC_DKG_...md` ou Bilan PyTest)

## Périmètre d'Action
- Répertoires : `00-Projet/PhaseX/`, `01-Principes_Spécification/`
- Objectif : Valider les pré-requis, définir le périmètre fonctionnel, formaliser les SPEC (Transversal, UC, Tech) et définir le schéma des données d'entrée.

## 📋 Directives & Check-list Cadrage
- [ ] **Gatekeeper Phase N-1 :** Confirmer la clôture 100% PASSED de la phase précédente.
- [ ] **Inventaire SSOT :** Identifier dans `config.py` les constantes existantes à réutiliser et déclarer les nouvelles (Chemins, Namespaces, Thresholds).
- [ ] **Modélisation Sémantique :** Définir la structure TBox/ABox cible (Domaine, Range, Cardinalités, marquage TLP : CLEAR/AMBER/RED).
- [ ] **Design Données d'Entrée :** Définir les schémas JSON/Pydantic V2 ou fichiers source bruts (CTI/Logs) nécessaires pour les tests.

## 📤 Livrables Attendus
1. `00-Projet/PhaseX/Phase_Content.md` (Objectifs, étapes, livrables)
2. `00-Projet/PhaseX/Memo_UseCase_PhaseX.md` (Explication métier + Diagramme Mermaid)
3. `01-Principes_Spécification/SPEC-0X_....md` (Spécification technique détaillée)
*(Interdiction de produire du code applicatif Python dans ce step)*