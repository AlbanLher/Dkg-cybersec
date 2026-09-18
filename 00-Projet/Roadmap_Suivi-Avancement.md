***Roadmap Produit & Backlog Évolutif : DKG-CyberSec & Agent IA SOC***

La roadmap est contruite en 3 niveaux
- ***Vague :*** Regroupement de principes pedagogique intégrés dans le dévelopement
- ***Phase :*** Décomposition de la vague autour de sous ensemble ou fonctionnel ou architecturaux
- ***Etape :*** Application strique commune a toutes les phase de dévelopement "Spec-Driven"

---

## 1  -  Roadmap  vision des principe pédagogiques par vagues

| **Vague** | **Titre**                                                     | **Sens & Principes Pédagogiques (P#)**                                                                                                                                                                                                                                                      | **Status**     |
| --------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| **V1**    | **Socle Structurel & <br>Cartographie Interne**               | **Principes :** (P1) Usage des standards (OWL2, SKOS, SHACL), <br>(P2) Confidentialité native (TLP:AMBER / TLP:RED).<br><br>**Cas d'usage minimal :** PC individuel.                                                                                                                        | 🟢 **PASSED**  |
| **V2**    | **Ingestion CTI, NER & <br>Alignement Primitif**              | **Principes :** (P3) Superposition de graphes, <br>(P4) Rapprochement sémantique (NER).<br><br>**Cas d'usage :** Superposer la CTI externe (NVD, CISA KEV) et le texte brut.                                                                                                                | 🟢 **PASSED**  |
| **V3**    | **Industrialisation, <br>Micro-Agents & Multi-Contextes PME** | **Principe :** (P5) Structure IA Agentique.<br><br>**Cas d'usage :** Passer au niveau Micro-Entreprise (API Gateway, Agents de logs & Veille CTI).                                                                                                                                          | 🟡 **ACTIVE**  |
| **V4**    | **Désambiguïsation Sémantique, <br>SKOS & Human-in-the-Loop** | **Principe :** (P6) Maintien de la cohérence du graphe face à la croissance des données.<br><br>**Cas d'usage :** Finesse taxonomique SKOS & Arbitrage Humain (MITM).                                                                                                                       | ⚪ **Planifié** |
| **V5**    | **Agent Copilot SOC, <br>GraphRAG & Fine-Tuning Continu**     | **Principe :** (P7) Agents locaux qui s'améliorent grâce aux données du DKG.<br><br>**Cas d'usage :** Entraînement/LoRA continu du SLM sur le DKG pour un Copilot explicable.                                                                                                               | ⚪ **Planifié** |
| **V6**    | **Streaming Temps Réel & <br>SOAR Adaptatif (POC Ciblé)**     | **Principe :** (P8) Démonstration de valeur sur boucle de réaction courte.<br><br>**Cas d'usage ciblé :** Reactivité SIEM/EDR temps réel sur le cas PC **OU**<br>Analyse d'impact statique sur PME (éviter la sur-simulation d'infrastructures). <br>Déclenchement de playbooks YARA/Sigma. | ⚪ **Planifié** |



## 2 - Tableau Détaillé des Vagues & Phases (Niveau Micro)
### 2.1 - Vue Tableau

| **Vague** | **Phase** | **Intitulé Fonctionnel**           | **Objectif Technique / Livrable**                                                              |  **Statut**   |
| :-------: | :-------: | ---------------------------------- | ---------------------------------------------------------------------------------------------- | :-----------: |
|  **V1**   |  **P1**   | Socle TBox & SHACL CWA             | Ontologie Master OWL2 (`TLP:AMBER`) et formes SHACL.                                           | 🟢 **PASSED** |
|           |  **P2**   | Cartographie ABox Interne          | Actifs, logiciels et failles d'un PC individuel (`TLP:RED`).                                   | 🟢 **PASSED** |
|  **V2**   |  **P3**   | Ingestion CTI Structurée           | Flux NVD, CAPEC, CISA KEV (`TLP:CLEAR`).                                                       | 🟢 **PASSED** |
|           |  **P4**   | Ingestion CTI Textuelle (NER)      | Extraction d'entités CTI avec score de confiance `dkg:nerConfidenceScore`.                     | 🟢 **PASSED** |
|           |  **P5**   | Agent MITM & Reasoning Base        | Moteur d'inférence R-01/R-02 et alignement vectoriel Cosinus MiniLM.                           | 🟢 **PASSED** |
|  **V3**   |  **P6**   | API Gateway & Ségrégation TLP      | Endpoint SPARQL/GraphQL sécurisé avec filtrage dynamique par niveau d'habilitation.            | 🟢 **PASSED** |
|           |  **P7**   | Micro-Agents Télémétrie            | Agent Veille CTI Externe. Extension topologie family.                                          | 🟢 **PASSED** |
|           |  **P8**   | SOC Dashboard & Replay Ops         | Agent surveillance Logs, Dynamic Overlay du graphe, vue multi-calques et automatisation CI/CD. | 🟡 **ACTIVE** |
|  **V4**   |  **P9**   | Taxonomies SKOS & Poly-hiérarchies | Structuration fine des domaines produits/familles et gestion des périmètres étanches.          |  ⚪ Planifié   |
|           |  **P10**  | Agent MITM Human-in-the-Loop       | Interface d'arbitrage actif quand $0.65 \le \text{Score} < 0.85$. Enrichissement guidé.        |  ⚪ Planifié   |
|  **V5**   |  **P11**  | GraphRAG & NL-to-SPARQL            | Indexation hybride du DKG, explicabilité par sous-graphes RDF de preuves.                      |  ⚪ Planifié   |
|           |  **P12**  | Fine-Tuning Continu SLM            | Dataset d'entraînement automatique DKG ➔ SPARQL et ré-entraînement LoRA/QLoRA.                 |  ⚪ Planifié   |
|  **V6**   |  **P13**  | Streaming SIEM & SOAR              | Ingestion en continu d'événements et génération de playbooks YARA/Sigma.                       |  ⚪ Planifié   |
### 2.2 - Vue Graph

```mermaid
graph TB
    %% Styles de statut
    classDef passed fill:#d4edda,stroke:#28a745,stroke-width:2px,color:#155724;
    classDef active fill:#fff3cd,stroke:#ffc107,stroke-width:2px,color:#856404;
    classDef planned fill:#f8f9fa,stroke:#6c757d,stroke-width:1px,stroke-dasharray: 5 5,color:#383d41;

    subgraph V1 ["🌊 Vague 1 : Socle Structurel & Cartographie Interne (🟢 PASSED)"]
        direction LR
        P1["Phase 1: TBox & SHACL CWA<br/>(TLP:AMBER)"] --> P2["Phase 2: ABox Interne<br/>(TLP:RED)"]
    end

    subgraph V2 ["🌊 Vague 2 : Ingestion CTI, NER & Alignement MITM (🟢 PASSED)"]
        direction LR
        P3["Phase 3: Flux CTI Structurés<br/>(TLP:CLEAR)"] --> P4["Phase 4: CTI Non-Structurée<br/>& NER"] --> P5["Phase 5: Agent MITM,<br/>SKOS & Reasoning Base"]
    end

    subgraph V3 ["🌊 Vague 3 : Industrialisation API & Multi-Contextes PME (🟡 ACTIVE)"]
        direction LR
        P6["Phase 6: API Gateway Cross-TLP<br/>& Security Engine"] --> P7["Phase 7: Micro-Agents<br/>Logs EDR & Veille CTI"] --> P8["Phase 8: SOC Dashboard<br/>Dynamic Overlay & Replay"]
    end

    subgraph V4 ["🌊 Vague 4 : Désambiguïsation Sémantique & HITL (⚪ Planifié)"]
        direction LR
        P9["Phase 9: Taxonomies SKOS<br/>& Poly-hiérarchies"] --> P10["Phase 10: Agent MITM<br/>Human-in-the-Loop"]
    end

    subgraph V5 ["🌊 Vague 5 : Copilot SOC & Fine-Tuning Continu (⚪ Planifié)"]
        direction LR
        P11["Phase 11: GraphRAG<br/>& NL-to-SPARQL"] --> P12["Phase 12: Fine-Tuning SLM<br/>Dataset DKG -> SPARQL"]
    end

    subgraph V6 ["🌊 Vague 6 : Streaming Temps Réel & SOAR Adaptatif (⚪ Planifié)"]
        direction LR
        P13["Phase 13: Streaming SIEM/EDR<br/>& Playbooks YARA/Sigma"]
    end

    %% Chaînage des Vagues
    V1 ==> V2
    V2 ==> V3
    V3 ==> V4
    V4 ==> V5
    V5 ==> V6

    %% Application des classes
    class P1,P2,P3,P4,P5,P6,P7 passed;
    class P8 active;
    class P9,P10,P11,P12,P13 planned;
```

## 3  -  Backlog Non Intégré

Idées non encore intégrées à la Roadmap Vague/Phase


