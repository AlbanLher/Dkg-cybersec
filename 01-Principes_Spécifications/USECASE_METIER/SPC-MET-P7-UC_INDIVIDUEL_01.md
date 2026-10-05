---
type: spec
reference: SPC-MET-P07-assistant_soc_foyer_01
revision: 2
titre: Assistant SOC du Foyer et Analyse de Risque Résidentiel
titre_court: assistant_soc_foyer
description: Cadrage métier, modélisation comportementale et règles décisionnelles (Agent Conseil) pour la sécurité d'un réseau domestique.
phase_code: P7
phase_nom: P7 (Micro-Agents Télémétrie PME)
statut: 🟢 ACTIVE
portee: USECASE_METIER
public_vise:
  - Analystes CTI / SOC, Lead Tech
  - Utilisateurs / Propriétaires de l'infrastructure
exigences:
  - id: EXG-MET-P7-01
    domaine: MET
    core: true
    phase: P7
    spec_source: SPC-MET-P07-assistant_soc_foyer_01
    titre: Cartographie Résidentielle
    critere: Ingestion et validation des 5 actifs du foyer.
    test: PyTest / Schéma Pydantic V2
  - id: EXG-MET-P7-02
    domaine: MET
    core: true
    phase: P7
    spec_source: SPC-MET-P07-assistant_soc_foyer_01
    titre: Analyse d'Exposition WAN
    critere: Détection des services exposés couplée aux flux TLP:CLEAR.
    test: PyTest / Validation SPARQL
  - id: EXG-MET-P7-03
    domaine: MET
    core: true
    phase: P7
    spec_source: SPC-MET-P07-assistant_soc_foyer_01
    titre: Restitution & Agent Conseil
    critere: Génération du rapport de risque et arbitrage de pré-installation.
    test: Validation Markdown / Test API
---


# 📜 Assistant SOC du Foyer et Analyse de Risque Résidentiel

## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif
Cette spécification définit le cadre métier permettant à un particulier d'auditer et de sécuriser son réseau domestique hétérogène (5 actifs)[cite: 5] à l'aide d'un assistant agentique, tout en bénéficiant d'un **Agent Conseil proactif** capable de statuer sur l'installation de nouveaux logiciels en amont.

### 1.2 Glossaire Métier & Technique
| Acronyme / Concept | Définition | Contexte DKG |
| :--- | :--- | :--- |
| **Actif Résidentiel** | Équipement connecté au réseau local (PC, IoT, tablette, thermostat)[cite: 5]. | Entité ABox de niveau TLP:RED. |
| **Agent Conseil** | Module décisionnel d'aide à l'installation logicielle. | Évalue le dépôt, la CTI et propose des alternatives. |
| **Chemin de Compromission** | Séquence logique reliant une vulnérabilité externe à un point d'entrée faible[cite: 5]. | Corrélation multi-agents (Local + CTI). |

## 🏗️ 2. Spécification & Modélisation
```mermaid
graph TD
    subgraph Foyer_TLP_RED [Environnement Domestique - TLP:RED]
        A1[PC Windows 10 - SMB] -->|Télémétrie| B[Local_Inventory_Agent]
        A2[PC Fedora 44 - Plex WAN] -->|Télémétrie| B
        A3[Caméra IP - Telnet] -->|Télémétrie| B
        A4[Tablette Android] -->|Télémétrie| B
        A5[Thermostat API] -->|Télémétrie| B
    end

    subgraph CTI_TLP_CLEAR [Catalogues Externe - TLP:CLEAR]
        C1[(NVD / CISA KEV / CERT-FR)] -->|Requête CVE/CWE| D[External_CTI_Agent]
    end

    B -->|ABox Locale Validée| E[Home_SOC_Orchestrator]
    D -->|Menaces & Failles| E

    E -->|Corrélation & Risques| F[Correlation_Agent]
    F -->|Évaluation Pré-installation| G[Advisor_Agent / API Agnostique]
    
    G -->|Verdict & Recommandation| H[Utilisateur du Foyer]
```
## 📐 3. Spécifications Formelles & Règles Métier

### 3.1 Scénario de Vie & Règle de l'Agent Conseil

Avant toute installation de logiciel sur un actif du foyer, l'Agent Conseil exécute la séquence métier suivante :

1. **Consultation de l'Actif Cible :** Vérification du niveau de patch et du rôle de la machine (LAN vs WAN).
    
2. **Vérification du Dépôt source :** Analyse de la réputation de l'URL ou du miroir de téléchargement.
    
3. **Croisement CTI Live :** Interrogation des bases structurées et non structurées (chargées via le fichier de configuration externe).
    
4. **Verdict Métier :**
    
    - _BLOQUER_ si une faille critique (ex: CISA KEV) est liée au logiciel ou si le dépôt n'est pas sûr.
        
    - _AUTORISER_ si le risque est maîtrisé.
        
    - _SUGGÉRER_ un équivalent logiciel plus sécurisé si une alternative existe.
        

## 📊 4. Matrice d'Exigences & Critères d'Acceptation (EXG-)

| Identifiant | UID | Domaine | Core/Non-Core | Intitulé de l'Exigence | Description & Critères d'Acceptation | Mode de Test / Asset |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **EXG-MET-P7-01** | EXG-MET-P7-01 | MET | Core | Cartographie Résidentielle | Ingestion et validation des 5 actifs du foyer. | PyTest / Schéma Pydantic V2 |
| **EXG-MET-P7-02** | EXG-MET-P7-02 | MET | Core | Analyse d'Exposition WAN | Détection des services exposés couplée aux flux TLP:CLEAR. | PyTest / Validation SPARQL |
| **EXG-MET-P7-03** | EXG-MET-P7-03 | MET | Core | Restitution & Agent Conseil | Génération du rapport de risque et arbitrage de pré-installation. | Validation Markdown / Test API |

## 🛡️ 5. Outillage & Traçabilité

- **Scripts d'Orchestration :** `03-Application/home_soc_orchestrator.py`
    
- **Artefacts :** `DKG_ABox_Residential.ttl`