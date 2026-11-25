# 🧹 Prompt 3/3 — Rétrospective 5S, Rejeu & Clôture (`[CONTEXT: RETRO-5S]`) — rév. 2026-11-25

> Rév. 2026-11-25 : la doctrine Replay change radicalement (étape 3) :
> `Snapshots_Phases/` est ABROGÉ physiquement (a015a37 →
> 06-Archives/Snapshots_Phases_Historique) ; la capitalisation se fait en
> **delta Master direct** depuis le rejeu `phases/PhaseX/`. Plancher NonReg
> 61 → **130 passed**. Ajoute le rejeu témoin, le grep de sûreté (bruit BNodes
> vs rajeunissement générationnel) et la règle « un Master jamais rejouable =
> suspect de pollution manuelle ».

## 📌 Fichiers à joindre obligatoirement dans votre message :
1. Résultat complet de l'exécution `pytest` (NonReg **130 passed** inclus)
2. `03-Application/config.py`
3. `Roadmap.md` (vagues statuts) + `README.md` (tableau macro)
4. Les diffs générés par le rejeu des zones Master concernées
5. Le backlog de la phase (carnet de session) — items traités et restants

## Périmètre d'action
- Répertoires : `02-Donnees/Master_Transversal/`, `00-Projet/`,
  `01-Principes_Spécifications/`, `03-Application/`
- Objectif : procéder au **rejeu témoin** sur les zones Master, appliquer les
  deltas, procéder au nettoyage 5S, mettre à jour l'avancement et clôturer
  l'étape/la phase par arbitrage documenté.

## 📋 Directives & Check-list 5S
- [ ] **Rejeu témoin (AVANT tout commit de zone Master) :** régénérer les
      artefacts `.ttl` depuis `03-Application/phases/PhaseX/`, comparer au
      Master courant, n'accepter que le delta attendu. `Snapshots_Phases/`
      n'existe plus — aucun copy/capitalisation depuis des snapshots.
- [ ] **Grep de sûreté sur le diff :** distinguer le bruit attendu (re-ID de
      BNodes déterministes, score MiniLM flottant) d'un vrai rajeunissement
      générationnel. Un Master jamais rejouable à l'identique = suspect de
      pollution manuelle (fossiles, greffes) — à auditer, pas à commiter.
- [ ] **Delta Master :** fusion ABROGÉE ; un delta = un delta (0 fait = vrai ;
      égalité = pas d'arc). Les Masters : TBox AMBER, ABox Interne RED
      (Instances_ABox), ABox Externe CLEAR (CTI_External), Infered RED,
      GREEN (API_Gateway).
- [ ] **Vue générée à la demande :** si une vue graphique est utile, elle est
      produite par `core/mermaid_views.py` (marquée « générée, ne pas éditer »)
      — jamais manuscrite ; miroirs `.md`/`.json` interdits. Vérifier
      l'équilibre `subgraph`/`end` de tout Mermaid édité.
- [ ] **Nettoyage 5S (règles consolidées — 01.1 §7) :**
  - *Seiton :* synchronisation de `config.py` ; un fichier = un seul groupe
    cohérent ; nommage canonique et docstring d'en-tête conformes.
  - *Seiso :* purge des `__pycache__` et fichiers errants selon backlog ;
    un engagement : le journal HAB_3 `api_gateway_audit.log` est VERSIONNÉ
    (exception .gitignore ligne 84) — ne jamais le purger.
  - *Seiketsu :* section « Synthèse de Clôture » de `Phase_Content.md` ;
    registre purgé et versionné (une exigence = une déclaration ; champ
    `recette` renseigné ; les EXG `prevue` passent PASSED avec preuve de
    commits) ; dashboard de couverture relu sur le critère « recetté ».
  - *Sustain :* le **grep d'imports réel** confirme qu'aucun module mort ne
    survit au tree (`core` n'importe jamais `phases`) ; les items de backlog
    ne quittent le carnet qu'à leur NonReg vert (**130 passed**).
- [ ] **Fichiers vitrines :** (1) statut de la phase dans `Roadmap.md`
  (🟢 PASSED — et si clôture de scope, l'**arbitrage documenté** joint) ;
  (2) mise à jour synchrone de la vue détaillée et du tableau macro du
  `README.md` ; (3) vue LLM (Roadmap § 5) actualisée pour le contexte de la
  session suivante.
- [ ] **Passe specs :** vérifier que les specs citant des chemins abrogés
  (ex. specs P5 → `Snapshots_Phases/`, abrogés en étape 3) sont alignées ou
  tracées au backlog.
- [ ] **Mémoire projet :** consigner au journal (mémoire Vibe) les décisions
  de la phase, arbitrages, questions restées ouvertes et la prochaine étape
  du fil directeur (01.3) — c'est l'amorce de la phase suivante.

## 📤 Livrables attendus
1. Zones Master consolidées en delta (rejeu témoin + grep de sûreté joints)
2. Mises à jour de `Roadmap.md`, `README.md`, `config.py` synchronisées
3. Registre d'exigences purgé/versionné + `Phase_Content.md` clôturé
4. Backlog de phase soldé (items fermés à NonReg vert, reste re-porté)
5. Journal mémoire projet mis à jour (amorce de la phase suivante)
