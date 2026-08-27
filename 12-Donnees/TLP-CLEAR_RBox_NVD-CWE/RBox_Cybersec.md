# Restitution Visuelle RBox - Référentiel Externe (Open Data)

**Classification :** `TLP:CLEAR`  
**Source :** `12-Donnees/TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.ttl`  
**Nombre de Triplets RDF :** 12

---

## 1. Graphe d'Enrichissement RBox (Mermaid.js)

```mermaid
graph TD
    classDef cveStyle fill:#d62728,color:#fff,stroke:#333,stroke-width:2px;
    classDef cweStyle fill:#ff7f0e,color:#fff,stroke:#333,stroke-width:2px;
    subgraph Vulnerabilities ["Vulnerabilities - NVD (TLP:CLEAR)"]
        CVE-2021-23017["⚠️ <b>CVE-2021-23017</b><br/><i>1-byte memory overwrite in NGINX resolver</i><br/>Score CVSS: 7.5"]
    end
    subgraph Weaknesses ["Weaknesses - MITRE CWE (TLP:CLEAR)"]
        CWE-193["🛡️ <b>CWE-193</b><br/><i>Off-by-one Error</i>"]
    end
    class CVE-2021-23017 cveStyle;
    class CWE-193 cweStyle;
    CVE-2021-23017 -->|classifiedUnder| CWE-193
```

---

## 2. Dictionnaire des Vulnérabilités & Faiblesses

| Type DKG | Identifiant | Libellé / Score |
|---|---|---|
| `Ontology` | `rbox:` | RBox Public Reference Graph - DKG Cybersec |
| `Vulnerability` | `rbox:CVE-2021-23017` | 1-byte memory overwrite in NGINX resolver |
| `Weakness` | `rbox:CWE-193` | Off-by-one Error |
