# Restitution Visuelle ABox - Cartographie des Instances SI

**Source :** `12-Donnees/ABox_init/ABox_Cybersec.ttl`  
**Nombre de Triplets RDF :** 15

---

## 1. Topologie du SI Privé (Diagramme Mermaid.js)

```mermaid
graph TD
    classDef assetStyle fill:#1f77b4,color:#fff,stroke:#333,stroke-width:2px;
    classDef softStyle fill:#2ca02c,color:#fff,stroke:#333,stroke-width:1px;
    classDef vulnStyle fill:#d62728,color:#fff,stroke:#333,stroke-width:2px;
    srv-web-01["🖥️ Serveur Web Production"]:::assetStyle
    sw-nginx-1201["📦 NGINX Web Server"]:::softStyle
    srv-web-01 -->|hasInstalledComponent| sw-nginx-1201
    CVE-2021-23017["⚠️ CVE-2021-23017"]:::vulnStyle
    sw-nginx-1201 -->|hasVulnerability| CVE-2021-23017
```

---

## 2. Inventaire Synthétique des Instances

| Type DKG | Identifiant Instance (URI) | Libellé / Label |
|---|---|---|
| `Ontology` | `abox:` | ABox Instance Graph - DKG Cybersec |
| `Asset` | `abox:srv-web-01` | Serveur Web Production |
| `Vulnerability` | `abox:CVE-2021-23017` | Vulnérabilité CVE-2021-23017 |
| `SoftwareComponent` | `abox:sw-nginx-1201` | NGINX Web Server |
