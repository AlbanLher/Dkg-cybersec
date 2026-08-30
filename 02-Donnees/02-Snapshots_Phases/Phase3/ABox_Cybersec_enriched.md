# 🚀 Rapport d'Enrichissement de l'ABox (NVD & MITRE CAPEC)

> **Statut** : ABox Enrichie (Phase 3)
> **Répertoire** : `12-Donnees/ABox_enriched/`

## 📊 Métriques d'Enrichissement Externe

| Indicateur | Valeur | Description |
| :--- | :--- | :--- |
| **Vulnérabilités Totales** | 2 | Total CVEs présentes dans l'ABox |
| **CVEs Enrichies NVD** | 2 | Vulnérabilités avec CVSS v3.1 & Sévérité |
| **Faiblesses CWE** | 2 | Classification des erreurs sous-jacentes |
| **Patterns d'Attaque (CAPEC)** | 2 | Total ThreatPatterns raccordés |
| **Taux de Couverture CAPEC** | 100% | Pourcentage de CWEs associées à au moins un CAPEC |

## 🌐 Chaine d'Enrichissement Complète (Asset ➔ CAPEC)

```mermaid
graph TD
    srv-db-01 -->|hasInstalledComponent| postgresql-13.2
    srv-web-01 -->|hasInstalledComponent| log4j-core-2.14.1
    srv-web-01 -->|hasInstalledComponent| nginx-1.18.0
    log4j-core-2.14.1 -->|hasVulnerability| CVE-2021-44228
    nginx-1.18.0 -->|hasVulnerability| CVE-2021-23017
    CVE-2021-23017 -->|hasWeakness| CWE-193
    CVE-2021-44228 -->|hasWeakness| CWE-502
    CWE-193 -->|hasThreatPattern| CAPEC-14
    CWE-502 -->|hasThreatPattern| CAPEC-112
```
