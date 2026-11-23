# 📐 Prompt 1/3 — Cadrage & Spécifications Phase X (`[CONTEXT: CADRAGE-SPEC]`) — rév. 2026-11-23

> Rév. 2026-11-23 : intègre l'étape 0 de réalignement backlog, le fil directeur
> 01.3, le budget GOU_4 et la sobriété documentaire §7 du 01.1. Le Context
> Bundle (archivé par 5S) est remplacé par la mémoire projet + le backlog
> consolidé.

## 📌 Fichiers à joindre obligatoirement dans votre message (demander si absents) :
- [ ] **`config.py`** — état de fin de phase précédente ou intermédiaire courant
- [ ] **`Roadmap.md`** — vagues V1-V8, phases P1-P17, statuts (vue YAML de la § 5)
- [ ] **`01.3 - Scenario_Fil_Directeur.md`** — le scénario pilote qui guide
      l'ordonnancement des briques de la vague (étape d'avancement à jour)
- [ ] **`Cadrage_P9_Backlog.md`** (ou backlog consolidé de la phase active) —
      les lots (nettoyage, dette, briques, renommages, EXG candidates)
- [ ] **Journal de reprise** (mémoire projet, ex. `reprise-2026-11-17.md`) —
      décisions actées non encore reflétées dans les specs

## Périmètre d'action
- Répertoires : `00-Projet/phases/PhaseX/`, `01-Principes_Spécifications/`,
  `03-Application/config.py`
- Objectif : réaligner le terrain, valider les pré-requis, définir le périmètre
  fonctionnel, formaliser les SPEC (TRANSVERSAL, USECASE_METIER,
  USECASE_TECHNIQUE) et le schéma des données d'entrée.

## 📋 Directives & Check-list Cadrage

### Étape 0 — Réalignement (AVANT toute spécification du neuf)
- [ ] **Gatekeeper Phase N-1 :** clôture 100% PASSED de la phase précédente ;
      si la clôture de scope impose un arbitrage, vérifier qu'il est **documenté**.
- [ ] **Purge du registre :** vérifier qu'aucun doublon d'EXG n'est apparu
      depuis (une exigence = une déclaration canonique) ; tracer les
      corrections/dette comme EXG, pas comme travaux fantômes.
- [ ] **Clore les questions ouvertes** du backlog (chacune reçoit sa décision
      écrite ; une question non tranchée devient un arbitrage traçable).
- [ ] **Vérification GOU_4 :** inventorier les EXG candidates du backlog vs le
      budget (~10 EXG nouvelles / 3 sessions) ; **split au cadrage si dépassement**.

### Étape 1 — Fonctionnel → Design
- [ ] **Inventaire SSOT :** constantes existantes à réutiliser dans `config.py`
      et nouvelles à déclarer (chemins, namespaces, seuils). Jamais de duplicata.
- [ ] **Scénario métier & données d'entrée :** histoire métier consistante et
      schémas d'entrée figés (JSON/Pydantic V2 ou fichiers bruts CTI/logs),
      données synthétiques si nécessaire.
- [ ] **Modélisation sémantique :** structure TBox/ABox cible (domaines, ranges,
      cardinalités, marquage TLP). Vocabulaire canonique obligatoire : **ABox
      Interne (TLP:RED)** / **ABox Externe (TLP:CLEAR)**.
- [ ] **Design données de sortie :** mise à jour proposée de `config.py`.
- [ ] **Alignement fil directeur :** chaque brique cadrée doit faire avancer
      le scénario pilote (01.3) d'une étape identificable.

### Étape 2 — Artefacts de cadrage obligatoires
- [ ] `00-Projet/phases/PhaseX/Phase_Content.md` (objectifs, étapes, livrables)
- [ ] `00-Projet/phases/PhaseX/Memo_UseCase_PhaseX.md` (scénario métier + flux
      Mermaid — vérifier l'équilibre `subgraph`/`end` après édition)
- [ ] Spécifications formelles dans `01-Principes_Spécifications/` (taxonomie
      TRANSVERSAL / USECASE_METIER / USECASE_TECHNIQUE), chaque EXG avec son
      champ `recette: auto | visuelle | inspection`
- [ ] **Backlog rebaseliné** : chaque item reçoit son EXG, son lot, son étape
      bornée — le backlog devient le carnet de session.

*(Interdiction de produire du code applicatif Python dans ce step — une brique
se spécifie avant de s'écrire, et l'intégration applicative n'a pas sa place
dans une phase brique ; loi de séparation, Roadmap § 4.bis.)*
