---
type: spec
reference: SPC-FWK-P9-Briques_Coeur_01
revision: 3
titre: Briques Cœur SOC_1 (hitm_gateway, EOL, llm_bridge)
titre_court: briques_coeur
description: Cadrage P9 rév. 3 — étape 0 de réalignement, périmètre des briques C1-C3, exigences tracées, recettes curl + résultat attendu, ordonnancement rebaseliné.
phase_code: P9
phase_nom: SOC_1 — Briques Cœur (vague V4)
statut: 🟡 ACTIVE
portee: TRANSVERSAL
public_vise: Développeur du projet DKG-CyberSec — didactique, poste unique, air-gapped, sans GPU dédié
fichier_source: 01.2 - Architecture.md (§ 1.bis.1, 1.bis.2, 1.quater) ; 01.3 - Scenario_Fil_Directeur.md (§ 1, 3, 6, 7) ; Cadrage_P9_Backlog.md (rébaseliné 23/11)
mise_a_niveau:
  - "2026-11-23 — rév. 3 : cadrage complet. Étape 0 exécutée (purge S5, questions ouvertes closes). 10 EXG-P9 nouvelles tracées, budget GOU_4 respecté, aucune intégration applicative (loi de séparation brique/application, Roadmap § 4.bis)."
exigences:
  - id: EXG-FWK-P9-GTW_1
    code_exigence: EXG-P9-01
    domaine: SE
    domaine_nom: Sécurité & Isolation
    core: true
    phase: P9
    titre: Passerelle HITL Unifiée (option A2)
    critere: Le contrôle HITL des routes migré dans le module core/hitm_gateway.py, exposé à la fois en API REST et en outils MCP ; le Golden Path P8 rejoué à l'identique (NonReg 61).
    test: "Rejeu du Golden Path P8 via exposition API puis MCP (curl documenté)"
    recette: auto
  
  - id: EXG-FWK-P9-GTW_2
    code_exigence: EXG-P9-02
    domaine: SE
    domaine_nom: Sécurité & Isolation
    core: true
    phase: P9
    titre: Régimes d'Écriture par la Passerelle
    critere: "Toute écriture passe par la passerelle avec son régime explicite — M1 écriture directe opérateur validée SHACL (déclarations parc : règles de filtrage, postures), M2 sources externes, HITL boucle pour liens implicites ; aucune autre voie d'écriture."
    test: "Recette des 3 régimes via curl + contrôle d'erreur sur écriture hors régime"
    recette: auto

  - id: EXG-FWK-P9-EOL_1
    code_exigence: EXG-P9-03
    domaine: CT
    domaine_nom: Cyber Threat Intelligence
    core: true
    phase: P9
    titre: Intégration EOL (moteur)
    critere: "Un moteur core (suffixe _engine) ingère la source EOL selon la mécanique des sources CTI : templates de stand-by réactivés, ingestion par delta, tests NonReg dédiés, source tracée."
    test: "Ingestion d'un delta EOL de recette + NonReg EOL"
    recette: auto


  - id: EXG-FWK-P9-EOL_2
    code_exigence: EXG-P9-04
    domaine: CT
    domaine_nom: Cyber Threat Intelligence
    core: true
    phase: P9
    titre: Namespace Dédié dkg-eol
    critere: "Les instances issues de la source EOL vivent dans un namespace dédié dkg-eol (arbitrage 23/11), marquage TLP:CLEAR, hébergées dans l'ABox Externe — séparation des sources par origine."
    test: "Sélection SPARQL du namespace dkg-eol (jamais regex .ttl)"
    recette: auto
  - id: EXG-FWK-P9-EOL_3
    code_exigence: EXG-P9-05
    domaine: CT
    domaine_nom: Cyber Threat Intelligence
    core: true
    phase: P9
    titre: Date EOL Sourcée Propagée
    critere: "La date d'obsolescence porte sa source et son commentaire (convention dkg:sourceNote) ; la vulnérabilité d'un finding s'étoffe CVE + KEV + EOL dès ingestion."
    test: "Requête SPARQL : composant EOL → finding enrichi, triple source présent"
    recette: auto
  - id: EXG-FWK-P9-LLM_1
    code_exigence: EXG-P9-06
    domaine: SE
    domaine_nom: Sécurité & Isolation
    core: true
    phase: P9
    titre: Propositionneur Moulé Lecture Seule
    critere: "llm_bridge est un propositionneur moulé sur l'ontologie (candidats TTL/SPARQL pré-contraints) ; il ne produit jamais une écriture directe — toute proposition transite par la passerelle et son régime."
    test: "Recette : toute sortie LLM est une proposition, aucune route d'écriture directe n'existe dans llm_bridge (grep d'imports = preuve de vie)"
    recette: auto
  - id: EXG-FWK-P9-LLM_2
    code_exigence: EXG-P9-07
    domaine: HW
    domaine_nom: Hardware & Infrastructures
    core: true
    phase: P9
    titre: Autodétection Runtime Local
    critere: "Détection automatique d'un runtime local (ollama / llama.cpp) au démarrage ; sans runtime, bascule silencieuse en mode dégradé — jamais d'appel API externe (air-gapped strict)."
    test: "Sans runtime : démarrage en mode dégradé sans erreur ; test SIDEBAR présence runtime simulé"
    recette: auto
  - id: EXG-FWK-P9-LLM_3
    code_exigence: EXG-P9-08
    domaine: SE
    domaine_nom: Sécurité & Isolation
    core: true
    phase: P9
    titre: Mode Dégradé Templates Figés
    critere: "Le mode dégradé produit des recommandations determinedistes depuis des templates figés (resserrer le filtrage / durcir l'OS) — reproductible, zéro coût d'inférence."
    test: "Recommandation identique bit-à-bit sur deux exécutions en mode dégradé"
    recette: auto
  - id: EXG-FWK-P9-FRG_1
    code_exigence: EXG-P9-09
    domaine: IN
    domaine_nom: Inférence & Graph Analytics
    core: true
    phase: P9
    titre: Pipeline Frugal (non fonctionnelle transversale)
    critere: "L'ingestion et les traitements s'exécutent en tâches séquentielles bornées : RAM bornée par tâche, taille de lot fixée, reprise sur checkpoint — capture sélective, jamais de requête ciblée source (01.2 § 1.bis.2)."
    test: "Recette : ingestion d'un delta avec checkpoint interrompu puis repris (aucune perte, mémoire mesurée sous seuil)"
    recette: auto
  - id: EXG-FWK-P9-RAP_1
    code_exigence: EXG-P9-10
    domaine: MET
    domaine_nom: Métier (usage SOC)
    core: true
    phase: P9
    titre: Rapport Évolutionné Vulnérabilité × Exploitabilité
    critere: "Le rapport affiche deux colonnes par finding (vulnérabilité, exploitabilité par contexte) avec hiérarchisation différenciée C1 > C2 > C3 — exigence déclarée ici (canonique, candidat acté 18/11), réalisée en P11 avec la métrique P10 ; P11 y renvoie."
    test: "Rappel : la recette complète (table C1/C2/C3, priorités P1-P4) se recette en P11 avec le fil directeur 01.3 § 7"
    recette: inspection
---



# SPC-FWK-P9 — Briques Cœur SOC_1 — spécification rév. 3

> Phase P9 (vague V4/SOC_1). Statut : 🟡 ACTIVE.
> Dépend des specs rév. 2+ corrigées (chirurgie du 23/11, dossier `specs/`, 77 exigences
> canoniques + renvois). Interdiction de produire du code applicatif dans ce cadrage :
> une brique se spécifie avant de s'écrire (loi de séparation, Roadmap § 4.bis).

## 0. Étape 0 — Réalignement (exécuté avant spécification du neuf)

### 0.1 État du terrain documentaire (au 23/11/2026)

- **Chirurgie S1-S4 exécutée** : 25 SPC corrigés dans `specs/`. 93 → 82 EXG
  (S1 : 6 re-déclarations malformées du P8-démonstrateur ; S2 : GOU_14-17 & GOU_23
  en renvois vers T-R_*). Champ `recette: auto|visuelle|inspection` sur chaque bloc
  (69/11/2). RGPD renuméroté SPC-MET-P12 (vague V5/SOC_2).
- **Purge S5 exécutée (cadrage)** : règle arbitrée = *la spec la plus spécifique du
  domaine garde la déclaration, les autres deviennent des renvois* :
  GOU_10 → renvoi vers **RUL_4** (EXG-HW-01, raisonnement local économe) ;
  GOU_19 → renvoi vers **T-R_6** (EXG-QU-01, couplage SHACL) ;
  GOU_21 → renvoi vers **ABO_2** (EXG-QU-03, sanity check zéro violation) ;
  RUL_2 → renvoi vers **DAT_2** (EXG-IN-02, inférence cascade, recette pytest prouvée) ;
  TEC-P8-soc_2 → renvoi vers **NER_4** (SE-03, NLP air-gapped).
  **Faux positifs maintenus** : SIL_1 (EXG-IN-01 — corrélation < 1s, distincte de la
  matérialisation), FWK-P8-soc_2 (étanchéité TLP), NER_2 (seuil de confiance 0.85).
  Total registre : **77 EXG canoniques**.
- **Gatekeeper P8** : clôture PASSED de la phase P8 acquise ( démonstrateur &
  NonReg 61) ; les travaux correctifs P9 (PATCH mcp_server, lot rouge B2) sont tracés
  § 6, pas en travaux fantômes.

### 0.2 Questions ouvertes du backlog — clôtures actées (23/11)

| # | Question | Décision |
|---|---|---|
| 1 | Namespace instances EOL | **Namespace dédié `dkg-eol`** (arbitrage 23/11), marquage TLP:CLEAR, dans l'ABox Externe — séparation des sources par origine |
| 2 | `scan_terrain.py` : que charge l'importlib ? | **Différé à la session terrain propre** (étape 2), lecture préalable obligatoire avant toute suppression A1 |
| 3 | `DELTA_BUFFER_PATH` | **Maintien documenté à P9** (legacy vivant, consommé par soc_engine) ; suppression au Lot D en une seule fenêtre de maintenance `config.py` (replay + NonReg 61) |
| 4 | Budget GOU_4 | **10 EXG nouvelles / ordonnancement en 5 sessions bornées** (§ 7) — dans le budget, pas de split |
| 5 | Vue traçabilité P8 (`CANVAS_SECTIONS` §34.x/§36.x) | Recalage **rév. 3 concédé comme travaux d'atelier** tracé § 6 (inspection) — DEM_11/12/13 |
| 6 | SSOT `pytest.ini` / `05-Bin/config.py` | **`pytest.ini` à la racine fait foi** ; `05-Bin/config.py` et `pytest.ini` de `03-Application` direction `06-Archives` à la session terrain propre (étape 2) |
| 7 | Stand-by technique EOL | **Confirmé inchangé** : templates en stand-by, tests NonReg EOL, nettoyage `03-Application`, voix-off |

### 0.3 Vocabulaire canonique (01.2 § 1.quater) — rappels opposables

Source / Moteur (`_engine`) / Agent (`agent_*`) / Orchestrateur ; **ABox Interne
(TLP:RED)** / **ABox Externe (TLP:CLEAR)** ; « intégration EOL » (jamais « agent EOL ») ;
docstring d'en-tête obligatoire `"""MOTEUR|AGENT|VUE|GATEWAY — rôle — recette/EXG"""`.

## 1. Périmètre P9 — les briques C1-C3

| Brique | Nature | Contenu borné | EXG |
|---|---|---|---|
| **C1. hitm_gateway** | Gateway (option A2) | Refactor : la logique HITL des routes migre dans `core/hitm_gateway.py` ; exposition API+MCP ; régime d'écriture explicite par flux (M1/M2/HITL) ; Golden Path rejoué | GTW_1, GTW_2 |
| **C2. Intégration EOL** | Moteur (source) | Réactivation du stand-by : ingestion source EOL par delta, namespace `dkg-eol`, TLP:CLEAR, source tracée, NonReg EOL | EOL_1, EOL_2, EOL_3, FRG_1 |
| **C3. llm_bridge** | Propositionneur | Propositionneur moulé lecture seule ; autodétection runtime local ; mode dégradé templates figés | LLM_1, LLM_2, LLM_3 |

**Exclusions explicites** (hors P9, gel de périmètre) :
- TBox exposition (règles de filtrage, posture de durcissement) & métrique
  d'exploitabilité → **P10** ; l'opérateur réclamera ces données via la passerelle en M1
  mais la TBox qui les structure se modélise en P10.
- Rapport évolutionné, boucle de remédiation, what-if applicatif → **P11**
  (l'exigence RAP_1 est *déclarée* ici, *réalisée* là-bas).
- Arbitrage des deux apps FastAPI (`main.py` vs `mcp_server.py`), registre MCP maison
  vs `@mcp.tool()` → **P11**.
- Toute intégration applicative dans les routes de démo : interdite en phase brique.

## 2. Modélisation & inventaire SSOT (design données)

### 2.1 Répartition des données

| Zone | Contenu P9 | Marquage |
|---|---|---|
| **ABox Externe** | Instances EOL (namespace `dkg-eol`), catalogues CTI existants | TLP:CLEAR |
| **ABox Interne** | Déclarations opérateur attendues en P9 (règles/postures : structure figée en P10) — la passerelle les accepte en M1 SHACL-validé, la TBox dédiée arrive en P10 | TLP:RED |
| **TBox Master** | Aucune évolution structurelle en P9 ; ajout du namespace `dkg-eol` à la déclaration des préfixes | — |

### 2.2 Inventaire SSOT `config.py` (inventaire, pas d'écriture dans ce step)

À réutiliser sans duplicata : `DIR_*` existants, chemins TBox/ABox, seuils du
frugal_engine. À déclarer à l'étape design de chaque brique (une écriture SSOT) :

- `EOL_SOURCE_URI` / constante de source EOL (M2) ;
- préfixe `dkg-eol` dans la table des namespaces ;
- constantes du bornage frugal (RAM max/tâche, taille de lot, chemin checkpoint) si
  absentes de frugal_engine — sinon réutilisation pure.

**Trace DELTA_BUFFER_PATH** (décision 0.2 n°3) : reste en l'état, documenté
« legacy vivant — suppression Lot D avec replay + NonReg 61 ». Les miroirs `.md`/`.json`
tombent aussi au Lot D (joint A2).

## 3. Articulation avec le fil directeur (01.3)

P9 livre l'étape 1 du scénario « serveur domotique Foyer » : intégration EOL ingère la
date d'obsolescence ; hitm_gateway reçoit les déclarations opérateur M1 ; llm_bridge
produit la recommandation en mode dégradé (templates figés). Les étapes 2-4 (rapport,
what-if, régression) consomment P10/P11 — l'étape se joue en assistance v0 documentée
si une brique manque, jamais suspendue (règle de dépendance § 3.2.4).

## 4. Recettes (curl + résultat attendu) — préfiguration figée par brique

Chaque brique reçoit sa recette complète à son étape bornée ; forme canonique :

- **C1** :
  `curl -X POST .../gateway/propositions/<id>/decision -d '{"decision":"approve"}'`
  → `{"status":"written","regime":"M1","shacl":"valid"}` — Golden Path rejoué via
  exposition API **et** MCP, sortie identique.
- **C2** :
  `curl -X POST .../sources/eol/ingest -d '{"delta":"delta_eol_recette.json"}'`
  → `{"ingested":N,"namespace":"dkg-eol","tlp":"CLEAR"}` + sélection SPARQL
  `PREFIX dkg-eol: ...` qui liste les composants EOL avec leur date sourcée.
- **C3** :
  `curl .../recommend?finding=<id>` sans runtime local →
  `{"mode":"degrade","template":"tpl_durcissement","run":null}` ; deux exécutions
  identiques (déterminisme).

Le checkpoint (FRG_1) se recette en interrompant l'ingestion d'un delta volumineux
puis en reprenant : aucune perte, mémoire sous le seuil affiché par frugal_engine.

## 5. Dette tracée (corrections = EXG ou travaux tracés, pas de travaux fantômes)

| Travaux | Nature | Portée EXG | Recette |
|---|---|---|---|
| PATCH mcp_server (3 imports cassés : json, config, AuditRequest) | Correction, étape 2 | Ports les endpoints `source="scan"` existants | curl + NonReg 61 |
| Lot rouge B2 (8-9 tests : ABO_3, HAB_3, GAT_2, GOU_7, GOU_12, mi_1, GOU_9, inc_1, GOU_11) | Complétion de recette d'EXG existantes | Complètent les EXG concernées (recette de ABO_3, etc.) | auto |
| Mapping conftest `test_phase8_confrontation.py` | Correction atelier | — | auto |
| Vue traçabilité `CANVAS_SECTIONS` §34.x/§36.x | Travaux atelier (inspection) | — | inspection |
| Recalage registre 77 EXG + renvois (S1-S5) | Fait 23/11 | — | inspection |

## 6. S6 — Notes de migration vocabulaire (à propager au Lot D et aux P10+)

- « ABox Externe » reste absent des SPC-* publiés avant le 23/11 : propagation au Lot D
  (renommages physiques) et prioritairement dans les specs P10/P11 lors de leur rédaction.
- `AgentMITM` (TEC-P5-CONSO) : nom historique antérieur au vocabulaire canonique ; le
  rôle tenu est *moteur de confrontation/consolidation* — note de migration en tête de
  la spec à sa prochaine révision, renommage du concept seulement s'il remonte dans le
  code (sinon note morte).
- « intégration EOL » partout ; le préfixe `agent_` est réservé aux agents, un moteur
  ne s'appelle jamais agent.

## 7. Ordonnancement P9 (backlog rebaseliné — carnet de session)

| Étape bornée | Contenu | EXG mises en jeu |
|---|---|---|
| 1. Cadrage (cette session) | Spec rév. 3, questions closes, purge S5 faite | déclaration des 10 |
| 2. Terrain propre + recette | Lot A (morts, miroirs .md/.json, PATCH mcp_server, archives SSOT, importlib scan_terrain) + NonReg 61 | GTW_1 (préalable A2), corrections § 5 |
| 3. Brique C1 | hitm_gateway A2 + Golden Path | GTW_1, GTW_2 |
| 4. Brique C2 + D | Intégration EOL + renommages ABox Externe + replay + suppression DELTA_BUFFER_PATH | EOL_1, EOL_2, EOL_3, FRG_1 |
| 5. Brique C3 | llm_bridge + mode dégradé | LLM_1, LLM_2, LLM_3 |
| 6. Dette test B2 | Lot rouge 8-9 tests + étiquetage inspection/visuelle | complétions § 5 |

**Budget GOU_4** : 10 EXG nouvelles / 5 sessions bornées hors cadrage — conforme
(≤ ~10 EXG / 3 sessions au rythme de la vague). RAP_1 déclarée P9, réalisation P11,
renvoi depuis la spec P11 à sa rédaction.

## 8. Critères de sortie de phase P9

1. Les 10 EXG-P9 recettées (curl + résultat attendu, preuve archivée) ;
2. NonReg 61 vert au terme de chaque étape (jamais de suppression/renommage à chaud) ;
3. Golden Path P8 rejoué via hitm_gateway (API et MCP) ;
4. Fil directeur : étape 1 du scénario Foyer jouée de bout en bout en mode réel
   (EOL ingéré, déclaration M1 acceptée, recommandation dégradée produite) ;
5. Registre : 77 EXG canoniques + 10 nouvelles = **87**, zéro doublon (grep du
   registre = preuve).
