# DESIGN — Brique C2 : Intégration EOL (moteur source)

**Projet** : DKG-CyberSec — Phase P9 « Briques Cœur » · **Étape bornée 4** (C2 + Lot D)
**Date** : 2026-11-24 · **Statut** : DESIGN — à valider avant impl
**Exigences portées** : EXG-FWK-P9-EOL_1, EOL_2, EOL_3 (+ FRG_1, GB GTW_2)
**NonReg plancher** : 119 passed (toute étape C2 ne peut descendre sous ce plancher)

---

## 1. Relevé de l'existant (vérifié au grep, session 5)

| Point de contact | État | Manque au regard de la spec |
|---|---|---|
| `audit_engine.py:201` | détection **mot-clé** (`end-of-life`, `smbv1`) dans le texte CTI → finding SMBv1 générique | pas une ingestion de source ; rien de structuré, rien de sourcé |
| `local_host_scanner.py:56` | `support_status` **statique** (`supported` par défaut, `unknown` en repli) | jamais confronté à une base de support réelle |
| `agent_local_host_abox.py` | véhicule `dkg:supportStatus` dans l'ABox du scan | plumbing sans source de vérité |
| ABox Externe (config `DIR_CTI_*`) | catalogues CTI TLP:CLEAR existants | `DIR_CTI_ABOX`/`DIR_CTI_CLEAR` = alias du même chemin (dette renommage Lot D) |
| TBox Master | aucun préfixe `dkg-eol` | spec l.192 : ajout du namespace à la déclaration des préfixes |
| Sources CTI (`cti_intake.py`) | mécanique complète déjà recettée (sources distances, per-cve/monolithic/head-only, cumul idempotent, marqueur `# SOURCES:`, offline-fallback, `record_write` M2) | **c'est le modèle à répliquer** — EOL_1 : « selon la mécanique des sources CTI » |
| « templates de stand-by » | à vérifier à l'impl (entrée EOL pré-déclarée dans le registre des sources ?) | geste V0 du plan |

**Conclusion relevé** : aucun moteur EOL n'existe ; la brique est neuve, mais elle
clône une mécanique déjà éprouvée — le risque d'impl est faible, le risque est
dans le **couplage** (Lot D, TBox Master, greffon audit).

---

## 2. Décisions d'architecture (bornées, en attente de ton OK)

**A1 — Moteur : `core/eol_engine.py` (EOL_1).**
Nature MOTEUR (vocabulaire 01.2 §1.quater : suffixe `_engine`, jamais « agent
EOL »). Rôle unique : **source EOL → delta TTL `dkg-eol` → ABox Externe**.
Aucune route d'écriture directe ; l'unique écriture est l'ajout au volume EOL
de l'ABox Externe, journalisée au sas en **régime M2** (source externe — même
règle que l'ingestion CTI, aucune boucle HITL pour une source publique
TLP:CLEAR). Docstring d'en-tête A4 : `"""MOTEUR — intégration EOL (source)
— recette/EXG : EOL_1, EOL_2, EOL_3, FRG_1"""`.

**A2 — Namespace & hébergement (EOL_2).**
- URI : `http://dkg.cybersec.org/eol#` (préfixe `dkg-eol`), **séparation par
  origine** : jamais dans `dkg-data`, jamais mélangé aux catalogues CTI.
- Hébergement : **ABox Externe (TLP:CLEAR)**, fichier dédié
  `DKG_EOL_Source.ttl` dans le répertoire ABox Externe renommé (Lot D).
- Chaque instance porte : `dkg:hasTLPMarking` TLP:CLEAR, `dkg:providedBy`
  `<source EOL>`, `dkg:supportStatus`, et (EOL_3) `dkg:eolDate xsd:date` +
  `dkg:sourceNote` (la date porte sa source et son commentaire).
- TBox Master : **une ligne** — ajout du préfixe `dkg-eol` à la déclaration
  (spec l.192). Acte M1 opérateur via le sas (comme toute écriture TBox),
  puis figé. Aucune évolution structurelle TBox en P9.

**A3 — Mécanique d'ingestion (EOL_1 + FRG_1) : clone de la mécanique CTI.**
- La source EOL est déclarée dans le **registre des sources** (stand-by
  réactivé — geste V0 vérifie l'entrée existante ou la crée : `id`,
  `label`, `mode` de sonde, `url` publique).
- Ingestion **par delta, cumul idempotent** (RDF set, jamais de doublon),
  marqueur `# SOURCES:` équivalent, **offline-fallback** (hors-ligne →
  volume simulé depuis le fonds local de recette, jamais de crash).
- Frugalité FRG_1 : sous-ensemble minimal, un seul volume local,
  jamais le flux complet si la source est volumineuse.
- Journal unique : `record_write("M2", "EOL_INGEST", detail=..., target=...)`.

**A4 — Enrichissement des findings (EOL_3, greffon audit_engine).**
Dans `_generate_risk_analysis` : requête SPARQL qui **relie** (jamais regex
sur `.ttl`) les composants de l'ABox audité aux instances `dkg-eol` quand la
correspondance composant↔EOL existe — alors :
- `status` du finding enrichi : statut support + date EOL sourcée ;
- la vulnérabilité du finding s'étoffe **CVE + KEV + EOL** dès ingestion ;
- le triplet source (`dkg:sourceNote`) est présent dans le finding enrichi.
Les findings sans correspondance EOL restent strictement inchangés
(non-régression garantie par les tests existants + nouveau).

**A5 — Couplage Lot D (ordre d'impl, pas d'entrelacement).**
Les renommages ABox Externe et la suppression `DELTA_BUFFER_PATH` **précèdent**
la brique : C2 écrit dans l'arborescence finale, pas dans celle qu'on va renommer.
Tout l'ancien nom (`DIR_CTI_ABOX`/`DIR_CTI_CLEAR` alias) est abrogé dans le
même geste — renommage physique des répertoires + config.py SSOT + replay
NonReg immédiat, avant toute ligne du moteur EOL.

---

## 3. Contrats

**config.py (SSOT, après Lot D)** — ajouts :
- `DIR_ABOX_EXTERNE` (nom canonique, remplace les alias `DIR_CTI_*`)
- `ABOX_EXTERNE_EOL_PATH = DIR_ABOX_EXTERNE / "DKG_EOL_Source.ttl"`
- `EOL_SOURCE_ID = "eol_source"` (registre des sources)

**`core/eol_engine.py`** — surface publique minimale :
- `ingest_eol_source() -> dict` : sonde la source (mode selon registre),
  construit le delta TTL `dkg-eol`, fusionne en cumul idempotent dans
  `ABOX_EXTERNE_EOL_PATH`, journalise M2, retourne les ratios de frugalité
  (distant sondé / téléchargé / local / RAM — mêmes champs que CTI).
- Interdits (loi de séparation inc_1, déjà testée) : aucun import `fastapi`,
  `api`, `phases` ; aucune écriture hors ABox Externe ; jamais les seeds
  ni le scan réel.

**Route (exposition, adaptateur fin)** — `POST /api/phase8/eol/ingest` dans
`routes_phase8.py`, pur délégué au moteur, réponse = dict du moteur.
Non ajoutée au registre MCP cette étape (P11 arbitrera l'exposition MCP des
moteurs ; C2 reste serveable en API REST, contrat minimal).

---

## 4. Recettes & NonReg (cibles)

Nouveaux tests `test_eol_engine.py` (estimation : ~10) :
1. ingestion offline du stand-by de recette → 200/SUCCESS, volume écrit ;
2. namespace SPARQL : 100% des instances en `dkg-eol` **(sélection SPARQL,
   jamais regex .ttl — EOL_2)** ;
3. marquage TLP:CLEAR sur chaque instance ;
4. `eolDate xsd:date` + `sourceNote` présents (EOL_3) ;
5. cumul idempotent (double ingestion → 0 doublon) ;
6. trace journal `EOL_INGEST regime='M2'` ;
7. isolation : seeds + scan réel + TBox intacts (sha) après ingestion ;
8. greffon audit : composant EOL → finding enrichi, **triple source présent** ;
9. findings non-EOL inchangés (non-régression) ;
10. réponse aux intrants absents/corrompus : marqueur visible, pas de crash.

Recettes curl (GTW_2, préfigurées) : `POST /eol/ingest` → SUCCESS ;
`tail` du journal → `EOL_INGEST regime='M2'` ; `POST /audit` sur un équipement
→ finding EOL enrichi.

**Cible full** : 119 + ~10 = ~129 passed (le chiffre exact tombera à l'écriture
des tests ; toute chute sous 119 = régression bloquante).

---

## 5. Plan d'impl borné (gestes 5S, un commit par geste)

| # | Geste | Preuve de sortie |
|---|---|---|
| V0 | Vérification stand-by : le registre des sources contient-il une entrée EOL ? Sinon la créer (recette : source publique de recette sandbox, jamais réseau en test) | grep + extrait |
| V1 | **Lot D** : renommages ABox Externe + abrogation alias `DIR_CTI_*` + suppression `DELTA_BUFFER_PATH` (arbitrage : suppression) | NonReg 119 passed |
| V2 | Préfixe `dkg-eol` dans TBox Master (acte M1 via sas, une ligne) + `config.py` (chemins C2) | parse OK + NonReg 119 |
| V3 | `core/eol_engine.py` complet (livrable remplaçable, comme toujours) | py_compile + NonReg 119 |
| V4 | Greffon `audit_engine` EOL_3 (enrichissement SPARQL, aucun regex .ttl) | NonReg 119 (findings non-EOL inchangés) |
| V5 | Route `POST /eol/ingest` (adaptateur fin) + Live UI check | curl + 200 |
| V6 | `test_eol_engine.py` (~10 tests) + recettes + update conftest mapping | full ~129 passed |
| V7 | Commit de clôture C2+D, statut release α au dashboard | git log |

---

## 6. Risques & arbitres ouverts (à lever avant/pendant V1)

1. **Source EOL réelle** : la spec parle de réactiver un stand-by — je n'ai
   pas l'entrée sous les yeux (V0 le confirme ou la crée). Forme attendue :
   source publique (ex. catalogue de fin de support d'un éditeur) **ou** fonds
   local de recette si la source réelle attend P10+. Sandbox obligatoire :
   le moteur doit fonctionner offline pour la recette (FRG_1).
2. **Le texte exact de FRG_1** n'a pas été re-collé dans les extraits — je le
   traite comme « ingestion frugale par delta, sous-ensemble minimal »
   (cohérent avec la mécanique CTI). Contre-ordre bienvenu si le texte dit autre chose.
3. **`DELTA_BUFFER_PATH`** : la suppression suppose qu'aucun code vivant ne
   l'utilise (grep V1 avant suppression — le test d'architecture inc_1 ne couvre
   pas config.py, un grep manuel le fera).
4. **Multi-instances** : le défaut d'imbrication composants/actifs dans
   `agent_local_host_abox.py` (tracé session 4) devient **matériel** dès que
   l'audit EOL confronte plusieurs actifs — à corriger en V4 si V0 le confirme déclenchant.

---

*Design borné — aucune impl avant validation. Conformité vocabulaire 01.2
§1.quater vérifiée (MOTEUR `_engine`, ABox Interne/Externe, « intégration EOL,
jamais agent EOL », docstring A4).*
