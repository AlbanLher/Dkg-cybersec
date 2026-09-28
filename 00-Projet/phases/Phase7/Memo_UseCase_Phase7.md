# Memo_UseCase_Phase7.md — Scénario Métier : L'Assistant SOC du Foyer

# Memo_UseCase_Phase7.md — Scénario Métier : L'Assistant SOC du Foyer

## 1. Le Scénario de Vie Courante & Les Actifs Cibles
- **PC Windows 10 / Linux Fedora / Caméra IP / Tablette / Thermostat** (5 actifs hétérogènes du foyer).
- **Connexion Live CTI :** Récupération dynamique des flux structurés (CISA KEV) et non structurés (bulletins) basée sur le catalogue `02-Donnees/Input_Phases/external_sources_config.json`.
- **Mode Agent Conseil :** Évaluation en amont de l'installation de tout nouveau logiciel (vérification de la réputation du dépôt, des failles associées et proposition d'alternatives sécurisées).


## 2. Architecture des Micro-Agents & Flux de Données

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
        C1[(NVD / CAPEC / CERT-FR)] -->|Requête CVE/CWE| D[External_CTI_Agent]
    end

    B -->|ABox Locale Validée| E[Home_SOC_Orchestrator]
    D -->|Menaces & Failles| E

    E -->|Corrélation des Risques| F[Correlation_Agent]
    F -->|Graphe de Compromission| G[Advisor_Agent / UI Dashboard]
    
    G -->|Rapport Markdown & Remédiations| H[Utilisateur du Foyer]
```

## 3. Matrice de Ségrégation TLP

- **TLP:RED** : Données de télémétrie du réseau local, adresses IP privées, états des actifs du foyer (Strictement cloisonné).
    
- **TLP:CLEAR** : Flux CTI publics, descriptions de vulnérabilités NVD, CWE/CAPEC (Partageable).
    
- **Passerelle de Sécurité** : L'orchestrateur garantit qu'aucune donnée TLP:RED brute ne fuit vers les flux CTI externes, seule la corrélation sémantique locale est opérée.




