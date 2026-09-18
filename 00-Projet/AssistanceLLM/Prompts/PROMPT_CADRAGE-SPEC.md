# 📐 Prompt 1/3 — Cadrage & Spécifications Phase X (`[CONTEXT: CADRAGE-SPEC]`)

## 📌 Fichiers à joindre obligatoirement dans votre message :
Vérifier que tu as bien reçu et demande si tu ne les as pas ! :
- [ ] **`config.py`** dans l'état ou de la fin de phase précédente ou de l'état intermédiaire de la phase en cours
- [ ] **La roadmap** présenté en YAML (Vision Roadmap globale)
- [ ] **Context_bundle.md** Fichier de synthèse de la Phase N-1. Complete la Roadmap et le config.py pour collecter du contexte

## Périmètre d'Action
- Répertoires : `00-Projet/PhaseX/`, `01-Principes_Spécification/`, `03-Application/config.py`
- Objectif : Valider les pré-requis, définir le périmètre fonctionnel, formaliser les SPEC (TRANSVERSAL, USECASE_METIER, USECASE_TECHNIQUE) et définir le schéma des données d'entrée.

## 📋 Directives & Check-list Cadrage
- [ ] **Gatekeeper Phase N-1 :** Confirmer la clôture 100% PASSED de la phase précédente.
- [ ] **Inventaire SSOT :** Identifier dans `config.py` les constantes existantes à réutiliser et déclarer les nouvelles (Chemins, Namespaces, Thresholds).
- [ ] - **Formalisation du Scénario Métier & Fichier d'Entrée** : Définir l'histoire métier consistante (ex: le foyer connecté et ses 5 actifs) et figer le schéma des données d'entrée (`input_residential_family_env.json`)..
- [ ] **Modélisation Sémantique :** Définir la structure TBox/ABox cible (Domaine, Range, Cardinalités, marquage TLP : CLEAR/AMBER/RED).
- [ ] **Design Données d'Entrée :** Souvent données synthetique permettant d'illustre le cas d'usage, ou un catalogue de données externe. Définir les schémas JSON/Pydantic V2 ou fichiers source bruts (CTI/Logs) nécessaires pour les tests.
- [ ] **Design Données de sortie :** Et avec les données d'entrée proposer la mise a jour du confug.py.
- [ ] **Génération des Artefacts de Cadrage Obligatoires** :    
    - Le fichier `00-Projet/Phase7/Phase_Content.md` (Objectifs, étapes, livrables).
    - Le fichier `00-Projet/Phase7/Memo_UseCase_Phase7.md` (Scénario métier détaillé et diagramme Mermaid de flux).
    - Les spécifications formelles associées dans `01-Principes_Spécifications/` (en respectant la taxonomie `TRANSVERSAL`, `USECASE_METIER`, `USECASE_TECHNIQUE`).


*(Interdiction de produire du code applicatif Python dans ce step)*