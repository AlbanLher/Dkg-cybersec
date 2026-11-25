# 📖 README — Utilisation des prompts DKG-CyberSec — rév. 2026-11-25

## Rôle des fichiers
- `SYSTEM_MASTER_PROMPT.md` — socle immuable : règles Spec-Driven, SSOT, TLP,
  vocabulaire canonique, doctrine delta Master, plancher NonReg 130. À coller
  en premier message de toute nouvelle session.
- `PROMPT_CADRAGE-SPEC.md` — step 1 : cadrage, réalignement backlog, specs,
  mise à jour du registre d'exigences versionné.
- `PROMPT_STEP_DEV_DATA.md` — step 2 : code, data pipeline, tests, recettes.
- `PROMPT_STEP_RETRO_5S.md` — step 3 : rejeu témoin, delta Master, 5S,
  fichiers vitrines, clôture par arbitrage documenté.
- `../Kits_Amorçage/` — **HISTORIQUE** : les Context Bundles P2→P8 sont
  remplacés depuis la reprise du 17/11 par la **mémoire projet** (journal de
  reprise Vibe). Ne plus les utiliser comme amorce de session.

## Procédure d'ouverture d'une nouvelle session
1. **Injection du Master Prompt** : coller `SYSTEM_MASTER_PROMPT.md` dans le
   premier message (règles immuables : config.py, @prefix, SSOT, 130).
2. **Re-synchro rapide** : coller l'état en 3 lignes
   (ex. « Étape 3 close (CI vert, 130 passed). P10 vague EOL ouverte : spec
   SPC-FWK-P10-EOL_01 posée, registre v2.5. Prochain geste : record SMBv1
   dans le fonds. »).
3. **Joindre la mémoire projet** : le journal de reprise
   (`reprise-2026-11-17.md`) remplace le Context Bundle ; joindre aussi le
   backlog consolidé de la phase active et `config.py` selon le step.

## Exemples d'activation par alias
- **Cadrage/spécifications de la phase :**
  > **[CONTEXT: SPEC]**
  > On ouvre la vague suivante de P10. Réalignons le backlog et posons la spec.
- **Développement :**
  > **[CONTEXT: DEV]**
  > Implémente le record SMBv1 dans le fonds EOL selon EXG-FWK-P10-FOND_1.
  _(Dès que je vois `[CONTEXT: DEV]` : respect strict de `config.py`, syntaxe
  rdflib, `@prefix` Turtle, NonReg 130 avant commit, un geste = un commit.)_
- **Rétrospective/clôture :**
  > **[CONTEXT: RETRO]**
  > Les 130 tests passent. Faisons le 5S de l'étape et mettons à jour Roadmap/README.
  _(Dès que je vois `[CONTEXT: RETRO]` : posture d'audit — rejeu témoin,
  grep d'imports, arbitrage documenté, mémoire projet mise à jour.)_

## Rappel des invariants de travail (vagues ≥ V4)
- Une session = une étape bornée ; gestes ≤ 5s ; un commit par geste, par
  chemin explicite (jamais `git add -A`).
- Plancher NonReg inviolable : **130 passed**, rejoué AVANT commit.
- Une seule version finale par livrable ; échec sonore, jamais silencieux ;
  SPARQL pour le graphe, jamais de regex sur `.ttl`.
