# 🧹 Prompt 3/3 — Rétrospective 5S, Replay & Clôture (`[CONTEXT: RETRO-5S]`) — rév. 2026-11-23

> Rév. 2026-11-23 : le miroir TTL→MD (abrogé par 5S du 19/11, règle §7 du
> 01.1) est remplacé par la vue générée à la demande ; le 5S gagne ses
> critères consolidés (grep d'imports = preuve de vie, NonReg avant tout) ;
> les fichiers vitrines sont actualisés ; le Context Bundle archivé est
> remplacé par la mémoire projet.

## 📌 Fichiers à joindre obligatoirement dans votre message :
1. Résultat complet de l'exécution `pytest` (logs de recette, NonReg 61 inclus)
2. `03-Application/config.py`
3. `Roadmap.md` (vagues statuts) + `README.md` (tableau macro)
4. Liste des artefacts générés dans `02-Donnees/Snapshots_Phases/PhaseX…/`
5. Le backlog de la phase (carnet de session) — items traités et restants

## Périmètre d'action
- Répertoires : `02-Donnees/Master_Transversal/`, `00-Projet/`, `01-Principes_Spécifications/`, `03-Application/`
- Objectif : appliquer le principe de Replay, générer les vues à la demande,
  procéder au nettoyage 5S, mettre à jour l'avancement et clôturer
  l'étape/la phase par arbitrage documenté.

## 📋 Directives & Check-list 5S
- [ ] **Principe de Replay :** copier/capitaliser les `.ttl` de
      `Snapshots_Phases/` vers `Master_Transversal/` (TBox AMBER, ABox
      Interne RED, ABox Externe CLEAR). **Les `.ttl` seulement** — aucun
      miroir `.md`/`.json` (abrogés) ; les chemins miroirs du SSOT sont
      supprimés au Lot A/D.
- [ ] **Vue générée à la demande (remplace l'auto-documentation) :** si une
      vue graphique est jugée utile, elle est produite par
      `core/mermaid_views.py` (moteur de vue) et marquée « générée, ne pas
      éditer » — jamais manuscrite. Vérifier l'équilibre `subgraph`/`end`
      de tout Mermaid édité.
- [ ] **Nettoyage 5S (règles consolidées — 01.1 §7) :**
  - *Seiton (Rangement) :* synchronisation de `config.py` ; un fichier = un
    seul groupe cohérent ; nommage canonique et docstring d'en-tête
    conformes (01.2 § 1.quater).
  - *Seiso (Nettoyage) :* parité stricte Snapshots vs Masters ; purge des
    `__pycache__` et fichiers errants prévus au backlog.
  - *Seiketsu (Standardisation) :* remplissage de la section « Synthèse de
    Clôture » dans `Phase_Content.md` ; registre d'exigences purgé (une
    exigence = une déclaration ; champ `recette` renseigné) ; dashboard de
    couverture relu sur le critère « recetté ».
  - *Sustain :* le **grep d'imports réel** confirme qu'aucun module mort ne
    survit au tree (`core` n'importe jamais `phases`) ; les items de backlog
    ne quittent le carnet qu'à leur NonReg vert.
- [ ] **Couverture & dette :** exiger que les EXG nouvelles de la phase
      aient leur test (ou leur étiquette `visuelle`/`inspection`) ; les tests
      de dette planifiés au cadrage sont écrits ou re-reportés avec motif.
- [ ] **Fichiers vitrines :** (1) statut de la phase dans `Roadmap.md`
      (🟢 PASSED — et si clôture de scope, l'**arbitrage documenté** joint) ;
      (2) mise à jour synchrone de la vue détaillée et du tableau macro du
      `README.md` ; (3) vue LLM (Roadmap § 5) actualisée pour le contexte
      de la session suivante.
- [ ] **Mémoire projet :** consigner au journal (mémoire Vibe) les décisions
      de la phase, arbitrages, questions restées ouvertes et la prochaine
      étape du fil directeur (01.3) — c'est l'amorce de la phase suivante
      (remplace le Context Bundle, archivé).

## 📤 Livrables attendus
1. Fichiers `.ttl` capitalisés dans `Master_Transversal/` (replay)
2. Mises à jour de `Roadmap.md`, `README.md`, `config.py` synchronisées
3. Registre d'exigences purgé + `Phase_Content.md` clôturé (synthèse)
4. Backlog de phase soldé (items fermés à NonReg vert, reste re-porté)
5. Journal mémoire projet mis à jour (amorce de la phase suivante)
