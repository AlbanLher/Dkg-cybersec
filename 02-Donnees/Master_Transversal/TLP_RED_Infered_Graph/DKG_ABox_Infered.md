# 📑 Livrable Phase 5 - Raisonnement Sémantique & Inférences

**Classification :** `TLP:RED`  
**Nombre de faits déduits :** `0`

---

## 📖 Glossaire & Table des Acronymes Métier

| Acronyme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **CISA** | Cybersecurity and Infrastructure Security Agency | Agence fournissant le catalogue KEV. |
| **KEV** | Known Exploited Vulnerabilities | Base des vulnérabilités activement exploitées. |
| **SKOS** | Simple Knowledge Organization System | Normalisation du thésaurus de concepts intégré dans TBox. |
| **TLP** | Traffic Light Protocol | Protocole de ségrégation des données. |

---

## 🔄 Cascade d'Inférence Sémantique (R-01 & R-02)

```mermaid
flowchart TD
    CVE[dkg:Vulnerability] -->|isCisaKev true| R1[Règle R-01 CISA KEV]
    R1 --> ASSET[dkg:HighRiskAsset]
    ASSET -->|connectsTo+| R2[Règle R-02 Silent Cascade]
    R2 --> TARGET[dkg:exposesToCascade Target]
```

*Document généré automatiquement post-inférence.*
