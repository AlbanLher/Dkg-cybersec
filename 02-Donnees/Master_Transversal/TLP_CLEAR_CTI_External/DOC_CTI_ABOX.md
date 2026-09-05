# 📑 Livrable Phase 3 - ABox CTI Externe & Référentiels Menaces

**Classification :** `TLP:CLEAR` (Public / Partageable)  
**Source Turtle :** `DKG_ABox_CTI_External.ttl`  
**Nombre total de triples RDF :** 32  

---

## 📖 Glossaire & Acronymes

| Acronyme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **APT** | Advanced Persistent Threat | Groupe d'attaquants hautement qualifiés menant des attaques ciblées et prolongées. |
| **CTI** | Cyber Threat Intelligence | Renseignements structurés sur les menaces informatiques. |
| **CVE** | Common Vulnerabilities and Exposures | Dictionnaire public des vulnérabilités de sécurité connues. |
| **CWE** | Common Weakness Enumeration | Système de classification des faiblesses logicielles et matérielles. |
| **CAPEC** | Common Attack Pattern Enumeration and Classification | Référentiel des schémas et patterns d'attaque. |
| **CVSS** | Common Vulnerability Scoring System | Système standardisé d'évaluation de la sévérité des vulnérabilités. |
| **TLP** | Traffic Light Protocol | Norme de classification du niveau de partage de l'information. |
| **RDF** | Resource Description Framework | Modèle de données en graphe sous forme de triplets (Sujet-Prédicat-Objet). |

---

## 🔄 Flux d'Ingestion Structuré (Pipeline Phase 3)

```mermaid
flowchart LR
    A[Sources CTI Structurées: NVD / MITRE] -->|Parsing JSON / XML| B(Extracteur Phase 3)
    B -->|Mappage Ontologique| C[Génération Triplets RDF]
    C -->|Validation SHACL| D{Conforme?}
    D -->|Non| E[Rejet / Error Log]
    D -->|Oui| F[Snapshot Phase 3]
    F -->|Synchronisation| G[Master CTI TLP:CLEAR]
```

---

## 📊 Synthèse des Entités CTI Ingestées

| Classe Schéma (`dkg:`) | Nombre d'Instances |
| :--- | :--- |
| `dkg:Vulnerability` | **3** |
| `dkg:ThreatPattern` | **3** |
| `dkg:Weakness` | **2** |
| `dkg:ThreatActor` | **1** |

---

## 🔗 Cartographie du Référentiel CTI Externe

```mermaid
graph TD
    subgraph TLP:CLEAR [Chainage CTI Structuré]
        CVE[dkg:Vulnerability / CVE] -->|dkg:cvssScore| SCORE[Score CVSS]
        CVE -->|dkg:hasWeakness| CWE[dkg:Weakness / CWE]
        CWE -->|dkg:hasThreatPattern| CAPEC[dkg:ThreatPattern / CAPEC]
    end
```

---

## 🔗 Détail des Dépendances Multi-Hop (CVE -> CWE -> CAPEC)

| Vulnérabilité (CVE) | Score CVSS | Faiblesse (CWE) | Pattern d'Attaque (CAPEC) |
| :--- | :--- | :--- | :--- |
| `CVE-2021-44228` | `10.0` | `CWE-502` | `CAPEC-586` |
| `CVE-2023-4863` | `8.8` | `CWE-119` | `CAPEC-100` |
| `CVE-2024-21887` | `N/A` | `ThreatActor-APT29` | `Pattern-SpearphishingLink-T1566_002` |
| `CVE-2024-21887` | `N/A` | `CWE-119` | `CAPEC-100` |
| `CVE-2024-21887` | `N/A` | `CWE-502` | `CAPEC-586` |

---
*Document généré automatiquement conformément aux exigences de livrables TLP:CLEAR.*