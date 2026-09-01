# 📊 Synthèse ABox CTI Externe (`TLP:CLEAR`)

> **Généré automatiquement par :** `generate_phase3_cti_abox.py`  
> **Classification :** `TLP:CLEAR`  
> **Nombre total de triples :** `11`  

---

## 📑 Ingestion des Référentiels CTI (Scénario Silent Cascade)

### 1. Vulnérabilités (NVD / CISA KEV)
* **`dkg-cti:CVE-2021-41773`**
  * **Libellé :** Apache Path Traversal
  * **Score CVSS v3 :** `7.5`
  * **CISA KEV (Exploitation active) :** `True` 🔴
  * **Faiblesse associée :** `dkg-cti:CWE-22`

### 2. Faiblesses (MITRE CWE)
* **`dkg-cti:CWE-22`**
  * **Libellé :** Path Traversal
  * **Schéma d'attaque (CAPEC) :** `dkg-cti:CAPEC-126`

### 3. Motifs d'Attaque (MITRE CAPEC)
* **`dkg-cti:CAPEC-126`**
  * **Libellé :** Directory Traversal

---

## 🔗 Raccordement Cross-TLP
* **Composant source (`TLP:RED`) :** `dkg-data:Apache-2.4.49`
* **Relation :** `dkg:hasVulnerability` $
ightarrow$ `dkg-cti:CVE-2021-41773`
