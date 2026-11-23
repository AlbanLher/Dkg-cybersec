# Backlog Consolidé — Cadrage P9 (spec rév. 3)

> Document de travail pour la session de cadrage P9 « Briques Cœur ».
> Consolidé le 19/11/2026 à partir du journal de reprise (17-19/11), des 5S
> (spécifications + core post-MCP), de l'audit de couverture EXG, du scénario
> fil directeur (01.3) et des arbitrages ABox Interne/Externe.
> Rappel protocole : une session = une étape bornée ; budgétisation GOU_4
> (~10 EXG nouvelles / 3 sessions, sinon split au cadrage) ; toute
> suppression/renommage passe en non-régression des 61 tests (jamais à chaud).

## 0. Rappel du périmètre et du fil

La vague V4 = P9 (briques cœur) → P10 (modélisation exposition &
exploitabilité) → P11 (mise en œuvre + arbitrage GO/NO-GO Neo4j).
La session de cadrage P9 produit la **spec rév. 3** (SPC-P9-*), trace ses EXG,
et fixe l'ordre des étapes bornées. Le fil directeur 01.3 guide l'ordonnancement :
chaque brique doit faire avancer le scénario pilote d'une étape.

## 1. Lot A — Nettoyage 5S (approuvé 19/11, exécution P9)

**A1. Fichiers morts/hors-sol du code**
- `core/audit_engine_arch_261018A.py` → `06-Archives`
- `core/models/` (doublon du `models/cache` applicatif — SSOT vérifié)
- 8 `.html` de `core/` (dont typo `tbox_gardian.html`) → docs/corbeille
- `__pycache__` : purge + `.gitignore`
- Errants de racine : `Sans titre*.md`, `MEMEO CONTETE.md`, `config_bkup.py`,
  `residential_agent_mc1.py`, `index2.html`, `tree.txt`, `audit_tracabilite.py`,
  ``DOC_Phase6_Gateway.md`.md``
- Condamnés **sous condition** ( lecture préalable de `scan_terrain.py` :
  l'`importlib` charge-t-il dynamiquement les scanners ?) :
  `core/local_host_scanner.py`, `core/local_host_abox_agent.py`
- `pytest.ini` racine vs `03-Application/` : arbitrer lequel fait foi
- `05-Bin/config.py` : contradiction SSOT → arbitrer (archives probable)

**A4. Nomming des scripts (acté 23/11/2026, règle codifiée au 01.2 § 1.quater)**
- Préfixe `agent_` pour les agents : `tbox_guardian.py` → `agent_tbox_guardian.py`
- Fichiers au nom trompeur : `scan_terrain.py` → `scan_engine.py`
  (sous condition importlib) ; `local_host_abox_agent.py` (mort, cf. A1)
- Docstring d'en-tête obligatoire pour tout `core/*.py` :
  `"""MOTEUR|AGENT|VUE|GATEWAY — rôle — recette/EXG tracés"""`
- Tous renommages avec NonReg 61 (mêmes étapes que A1/A2)

**A2. Sobriété documentaire (règles codifiées au 01.1 §7)**
- Miroirs `.md` et `.json` des graphes (`Master_Transversal` +
  `Snapshots_Phases`) : suppression, y compris les chemins SSOT
  (`ABOX_CTI_MD_PATH`, `DKG_TBox_Master.json`, etc.) — à fusionner avec le
  renommage ABox Externe (lot D)
- Exportateurs `export_phase*_md.py` → `06-Archives`
- Génération `SPEC-*` de `05-Bin` → `06-Archives` (une génération canonique
  SPC-*, `registry_exigences.json` = index unique)
- Bundles `Kits_Amorçage/CONTEXT_BUNDLE_*` → `06-Archives`
- `Architecture v_post_phase8_12-10-2026.md` (01-Principes) → archives

**A3. PATCH mcp_server.py (3 bugs confirmés)**
- Ajouter `import json`, `import core.config as settings`
- Importer `AuditRequest` (défini dans `api/routes_phase8.py`) en local
- Corriger l'import fragile `from simulator import` → `from core.simulator import`
- Recette : les 3 endpoints `source="scan"` + NonReg 61
- Tracé pour la suite (P11, pas P9) : arbitrage des deux apps FastAPI
  (`main.py` vs `mcp_server.py`), registre MCP maison vs vraies primitives

## 2. Lot B — Dette de test (audit couverture EXG du 19/11)

**B1. Purge du registre (avant toute écriture de test)**
  *État 23/11 : partiellement exécuté par la chirurgie specs S1-S3
  (sources : `/home/user/artifacts/specs/`, 82 EXG, renvois en place,
  `recette` sur chaque bloc — 69 auto / 11 inspection / 2 visuelle).*
- ~~Doublons de déclaration frontmatter : GOU_14-17 ≡ T-R_1-4, GOU_23 ≡
  T-R_7~~ **fait (S2, renvois)** ; ~~re-déclarations du
  `SPC-MET-P8-demonstrateur_phase8_01` (6 intitulés cassés)~~ **fait (S1,
  renvois)** ; ~~champ `recette` par EXG~~ **fait (S3)**
- ~~Arbitrages S5~~ **FAIT 23/11** (règle : la spec la plus spécifique garde la
  déclaration) — détail en § 6
- Durcir le §4 du 01.1 (« recetté » compté sur les fonctions de test,
  citation ≠ recette)
- Grep de sûreté au dépôt : `SPC-MET-P9-Compliance` / références à
  l'ancienne numérotation RGPD (renumérotée SPC-MET-P12 le 23/11) —
  vérifier registres et commentaires de code
- S6 (à la rédaction de la spec rév. 3, propagation Lot D) : « ABox
  Externe » absent des SPC-* ; note de migration vocabulaire
  (`AgentMITM` → rôle agent, `agent EOL` → `intégration EOL`)

**B2. Lot rouge (8-9 tests à écrire, candidats EXG de test P9)**
1. ABO_3 — Matérialisation des inverses (TB)
2. HAB_3 — Audit de traçabilité gateway (le log existe, le test manque)
3. GAT_2 — Horodatage UTC (trivial)
4. GOU_7 — Validation aux frontières Pydantic
5. GOU_12 — Isolation des snapshots (SE)
6. mi_1 — Immuabilité & parsers défensifs (TEC)
7. GOU_9 — Formatage des IDs
8. inc_1 — Interdiction monolithique : **automatiser le grep d'imports 5S
   en test** (« aucun module de `core` n'importe `phases` »)
9. GOU_11 — Marquage TLP générique (instances couvertes ; arbitrer un test dédié)
- com_1 (qualification RGPD) : **renvoyé à la vague V5/SOC_2**, pas une dette
- Étiquetage inspection/visuelle : DEM_4d/4e, GOU_1/4/6 (GOU_8 déjà
  partiellement exécutée par conftest), gr_2/gr_3 (preuve par abaque P11),
  mi_3, GOU_4

**B3. Mapping conftest**
- `test_phase8_confrontation.py` absent de `FILE_DOMAIN_MAPPING` (warning
  actif) → à mapper

## 3. Lot C — Briques cœur P9 (le cœur de la phase)

Chaque brique : spec `SPC-P9-*` + recette (curl + résultat attendu) sous la
règle « 1 brique = 1 étape bornée, AUCUNE intégration applicative » :
- **C1. hitm_gateway (option A2)** : refactor du contrôle HITL en module
  `core/hitm_gateway.py` exposé API+MCP, re-validation du Golden Path
  (le module existe déjà et est vivant — le refactor le promeut, le logique
  HITL des routes migre dedans)
- **C2. Intégration EOL** : moteur d'ingestion de la source EOL
  (templates, tests NonReg, mécanique sources CTI)
- **C3. llm_bridge** : propositionneur moulé (TTL/SPARQL, jamais d'écriture),
  autodétection ollama/llama.cpp, mode dégradé templates figés

## 4. Lot D — Renommages physiques ABox Externe (acté 18/11)

À exécuter avec la brique EOL (mais après spec + purge registre) :
- Dossier `TLP_CLEAR_CTI_External` → ABox Externe
- Fichiers `DKG_ABox_CTI_External*.ttl`
- Namespace `dkg-cti`
- Variables `DIR_CTI_*` (dont les alias `DIR_CTI_ABOX`/`DIR_CTI_CLEAR`)
- Suppression des chemins miroirs `.md`/`.json` (joint avec A2)
- Replay des données + NonReg 61
- Path `DELTA_BUFFER_PATH` (legacy, vivant — consommé par `soc_engine`) :
  décision à la spec (suppression avec replay, ou maintien documenté)

## 5. Lot E — Candidats EXG fonctionnels (issus du 01.3 et des assistances)

À tracer en EXG-* à la spec rév. 3 (certains relèvent de P10) :
1. **Rapport évolutionné** : colonnes vulnérabilité × exploitabilité par
   contexte, hiérarchisation différenciée (candidat EXG P9, arbitré 18/11)
2. Modélisation des règles de filtrage dans l'ABox Interne — **brique P10**
3. Modélisation de la posture de durcissement OS — **brique P10**
4. Métrique d'exploitabilité (comparable, reproductible, sensible aux
   mitigations) — **brique P10**
5. What-if lecture seule avant écriture opérateur (requêtes d'atteignabilité
   P10, consommées P11)
6. Clôture vérifiée / régression / MTTR (assistance 2)
7. Pipeline frugal en exigence non fonctionnelle : RAM bornée par tâche,
   taille de lot, reprise sur checkpoint (01.2 § 1.bis.2)
8. Les 8 assistances SOC_1 du 01.2 § 1.bis.1 (quotidiennes/périodiques) :
   à figer comme exigences de contrat fonctionnel

## 6. Questions ouvertes — CLOSURES ACTÉES 23/11 (cadrage, étape 0)

Décisions écrites dans `specs/SPC-FWK-P9-Briques_Coeur_01.md` § 0.2. Résumé :
1. EOL → namespace dédié **dkg-eol** (TLP:CLEAR, ABox Externe) ;
2. `scan_terrain.py`/importlib → lecture à la session terrain propre (étape 2) ;
3. `DELTA_BUFFER_PATH` → maintien documenté P9, suppression au Lot D (replay + NonReg 61) ;
4. GOU_4 → 10 EXG nouvelles / 5 sessions bornées, pas de split ;
5. Vue traçabilité → travaux d'atelier tracés en spec P9 § 5 (inspection) ;
6. SSOT → **pytest.ini racine fait foi** ; `05-Bin/config.py` et doublon `03-Application` → 06-Archives (étape 2) ;
7. Stand-by technique EOL confirmé inchangé.

**S5 exécuté 23/11** : 5 doublons → renvois (GOU_10→RUL_4, GOU_19→T-R_6,
GOU_21→ABO_2, RUL_2→DAT_2, TEC-P8-soc_2→NER_4) ; faux positifs maintenus
(SIL_1 EXG-IN-01 distincte, FWK-P8-soc_2 étanchéité TLP, NER_2 seuil confiance).
Registre : **77 EXG canoniques**.

## 7. Proposition d'ordonnancement P9 (suggestion soumise au cadrage)

| Étape bornée | Contenu | Étape 01.3 correspondante |
|---|---|---|
| 1. Cadrage (cette session) | Spec rév. 3, EXG tracées, purge registre planifiée | — |
| 2. Nettoyage + recette | Lot A (fichiers, miroirs, PATCH mcp_server) + NonReg | terrain propre |
| 3. Brique C1 | hitm_gateway A2 + Golden Path | étape 1 |
| 4. Brique C2 + D | Intégration EOL + renommages ABox Externe + replay | étape 1 (EOL) |
| 5. Brique C3 | llm_bridge + mode dégradé | étape 1 (recommandation) |
| 6. Dette test B2 | lot rouge (8-9 tests, dont anti-monolithe) | sécurisation |

Chaque étape = 1 session au maximum ; la clôture de phase = arbitrage
documenté (DoD § 4.bis Roadmap).
