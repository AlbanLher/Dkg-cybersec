# 🔴 DKG Master ABox Consolidée - Graphe d'Attaque (TLP:RED)

> **Classification Globale** : `TLP:RED` (Strictement confidentiel - Usage interne restreint)  
> **Répertoire** : `12-Donnees/TLP_RED_Consolidation_ABox/`

## 📊 Synthèse des Instances Consolidées

| Entité / Concept | Nb Instances | Niveau TLP |
| :--- | :--- | :--- |
| **Équipements (Assets)** | 2 | `TLP:RED` |
| **Composants Logiques** | 3 | `TLP:RED` |
| **Vulnérabilités (CVE)** | 2 | `TLP:CLEAR` |
| **Faiblesses (CWE)** | 2 | `TLP:CLEAR` |
| **Patterns d'Attaque (CAPEC)** | 2 | `TLP:CLEAR` |

## 🌐 Visualisation du Graphe d'Attaque Consolidé

```mermaid
graph TD
    srv-db-01[srv-db-01 - TLP:RED] -->|hasInstalledComponent| postgresql-13.2
    srv-web-01[srv-web-01 - TLP:RED] -->|hasInstalledComponent| log4j-core-2.14.1
    srv-web-01[srv-web-01 - TLP:RED] -->|hasInstalledComponent| nginx-1.18.0
    log4j-core-2.14.1 -->|hasVulnerability| CVE-2021-44228[CVE-2021-44228 - TLP:CLEAR]
    nginx-1.18.0 -->|hasVulnerability| CVE-2021-23017[CVE-2021-23017 - TLP:CLEAR]
    CVE-2021-23017 -->|hasWeakness| CWE-193
    CVE-2021-44228 -->|hasWeakness| CWE-502
    CWE-193 -->|hasThreatPattern| CAPEC-14
    CWE-502 -->|hasThreatPattern| CAPEC-112
```
