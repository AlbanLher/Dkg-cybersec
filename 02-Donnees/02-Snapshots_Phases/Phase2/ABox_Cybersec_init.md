# 📙 Rapport de l'ABox DKG Initialisée (TLP:AMBER)

> **Statut** : Instances de Référence Générées Automatiquement
> **Namespace Instances** : `http://dkg.cybersec.org/abox#`

## 📊 Métriques du Jeu d'Instances

| Type d'Entité | Nombre d'Instances | Classe TBox Associée |
| :--- | :--- | :--- |
| **Assets** | 2 | `dkg:Asset` |
| **Composants Logiciels** | 3 | `dkg:SoftwareComponent` |
| **Vulnérabilités** | 2 | `dkg:Vulnerability` |

## 🌐 Graphe d'Instances (Vue Synthétique)

```mermaid
graph TD
    srv-web-01 -->|hasInstalledComponent| log4j-core-2.14.1
    srv-web-01 -->|hasInstalledComponent| nginx-1.18.0
    srv-db-01 -->|hasInstalledComponent| postgresql-13.2
    log4j-core-2.14.1 -->|hasVulnerability| CVE-2021-44228
    nginx-1.18.0 -->|hasVulnerability| CVE-2021-23017
    CVE-2021-44228 -->|hasWeakness| CWE-502
    CVE-2021-23017 -->|hasWeakness| CWE-193
```
