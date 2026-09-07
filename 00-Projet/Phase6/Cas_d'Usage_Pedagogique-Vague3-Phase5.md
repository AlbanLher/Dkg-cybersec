

## Contextualisation Metier
L'organisation fait face a une menace croissante d'attaques ciblees sur son infrastructure critique. Les bulletins CTI publics (TLP:CLEAR) signalent regulierement de nouvelles vulnerabilites (CVE) activement exploitees dans la nature par des groupes de menace (APT). 

L'objectif du SOC et de l'equipe de Cyber Threat Intelligence est d'automatiser l'analyse de pertinence : **comment savoir instantanement si une menace externe impacte un actif critique interne (TLP:RED) sans violer le cloisonnement des donnees et sans intervention humaine lourde ?**

---

## Deroulement du Scenario (Etape par Etape)

### 1. Interception & Alignment par l'Agent MITM (Air-Gapped)
* **Entree :** Un bulletin CTI est traite localement par les modeles NER/NLP offline (`03-Application/models/cache/`).
* **Traitement MITM :** L'Agent MITM (`mitm_agent.py`) valide la coherence des concepts extraits contre la TBox Master (`TLP_AMBER_Socle_TBox`).
* **Decision :** 
  * Si la similarite cosinus est $\ge 0.85$, le concept est directement aligne (`dkg:Vulnerability`, `dkg:Asset`).
  * Si le score est sous le seuil, l'agent isole l'entite et soumet une proposition d'extension de schema sous controle humain (Human-in-the-Loop).

### 2. Execution du Moteur d'Inference Semantique (`generate_phase5_inference.py`)
Le moteur d'inference agrege la TBox Master, l'ABox interne et l'ABox CTI externe pour executer les regles SPARQL CONSTRUCT (`DKG_Rules_Master.ttl`) :

* **Regle R-01 (Detection Asset a Haut Risque) :**
  $$\text{Asset} \xrightarrow{\text{hostsComponent}} \text{Component} \xrightarrow{\text{hasVulnerability}} \text{CVE (CISA KEV)} \implies \text{Asset a dkg:HighRiskAsset}$$
* **Regle R-02 (Propagation de Menace) :**
  $$\text{ThreatCampaign} \xrightarrow{\text{targetsComponent}} \text{Component} \xleftarrow{\text{hostsComponent}} \text{Asset} \implies \text{Campaign } \text{dkg:targetsAsset } \text{Asset}$$

### 3. Validation SHACL & Marquage TLP
* Le graphe deduit est controle par le validateur SHACL pour garantir l'absence de violences de typage.
* Le graphe enrichi est exporte dans `02-Donnees/Master_Transversal/TLP_RED_Infered_Graph/DKG_ABox_Infered.ttl` sous le marquage strict **TLP:RED**.

---

## Resultat pour l'Analyste SOC / CTI

| Indicateur            | Avant Inference Semantique     | Apres Inference (Phase 5)                                              |
| :-------------------- | :----------------------------- | :--------------------------------------------------------------------- |
| **Visibilite Menace** | Bulletin CTI isole (TLP:CLEAR) | Corrélation directe entre APT, CVE KEV et Actif Interne                |
| **Classif. Risque**   | Evaluation manuelle requise    | Actif reclassé automatiquement en `HighRiskAsset` (Score: 9.5)         |
| **Conformite**        | Risque de fuite TLP            | Cloisonnement TLP respecté (Inférences restreintes au domaine TLP:RED) |