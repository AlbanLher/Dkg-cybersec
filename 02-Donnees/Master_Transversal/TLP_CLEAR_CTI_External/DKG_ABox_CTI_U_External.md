# 📑 Livrable Phase 4 - Ingestion CTI Non Structurée (ABox-U)

**Classification :** `TLP:CLEAR` (Public / Partageable)  
**Source Turtle :** `DKG_ABox_CTI_U_External.ttl`  
**Nombre total de triples RDF :** 12  

---

## 📖 Glossaire & Acronymes

| Acronyme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **APT** | Advanced Persistent Threat | Groupe d'attaquants qualifiés menant des opérations ciblées. |
| **CTI** | Cyber Threat Intelligence | Renseignements structurés sur les menaces informatiques. |
| **CVE** | Common Vulnerabilities and Exposures | Référentiel des vulnérabilités publiques connues. |
| **TLP** | Traffic Light Protocol | Norme de restriction du partage de l'information. |
| **RDF** | Resource Description Framework | Modèle de représentation sous forme de graphes de triplets. |

---

## 🔄 Flux d'Ingestion & Validation Qualité

```mermaid
flowchart LR
    A[Avis Textuel Brut] -->|Parsing / Regex| B(Extractor CTI)
    B -->|Calcul Score| C{Confidence >= 0.85?}
    C -->|Non| D[Rejet / Journal d'Audit]
    C -->|Oui| E[Instanciation Triplets RDF]
    E --> F[Snapshot Phase 4]
    F -->|Synchro SSOT| G[Master CTI TLP:CLEAR]
```

---

## 📊 Entités Extraites & Niveaux de Confiance

| URI Entité (`cti:`) | Classe (`dkg:`) | Libellé / Concept | Score Confiance |
| :--- | :--- | :--- | :--- |
| `CVE-2024-21887` | `dkg:Vulnerability` | CVE-2024-21887 | **0.99** |
| `ThreatActor-APT29` | `dkg:ThreatActor` | APT29 (`APT`) | **0.98** |
| `Pattern-SpearphishingLink-T1566_002` | `dkg:ThreatPattern` | Spearphishing Link (T1566.002) | **0.92** |

---

## 🔗 Topology Network Graph (Extraite)

```mermaid
graph TD
    subgraph TLP:CLEAR [Périmètre CTI External Unstructured]
        TA[cti:ThreatActor-APT29] -->|dkg:exploitsVulnerability| VULN[cti:CVE-2024-21887]
        TA -->|dkg:hasThreatPattern| PAT[cti:Pattern-SpearphishingLink-T1566_002]
    end
```

---

## 🔗 Détail des Relations Extraites

| Menace (Threat Actor) | Vulnérabilité (CVE) | Pattern (ATT&CK) |
| :--- | :--- | :--- |
| `ThreatActor-APT29` | `CVE-2024-21887` | `Pattern-SpearphishingLink-T1566_002` |

---
*Document miroir généré automatiquement.*