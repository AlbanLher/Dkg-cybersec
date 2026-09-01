#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération de l'ABox CTI Externe (TLP:CLEAR).
Projet : DKG-CyberSec - Phase 2.5 (Wave 2)
Conforme aux spécifications : SPEC-03 & SPEC-UC-02
"""

from rdflib import Graph, Literal, RDF, RDFS, XSD
from config import ABOX_CTI_PATH, DOC_CTI_MD_PATH, DKG, DKG_DATA, DKG_CTI

def generate_cti_abox():
    print("🚀 [Phase 2.5] Initialisation du graphe ABox CTI Externe (TLP:CLEAR)...")
    
    g = Graph()
    
    # Binding des prefixes pour une sérialisation Turtle propre
    g.bind("dkg", DKG)
    g.bind("dkg-data", DKG_DATA)
    g.bind("dkg-cti", DKG_CTI)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # -------------------------------------------------------------------------
    # 1. Instanciation CVE-2021-41773 (NVD / CISA KEV)
    # -------------------------------------------------------------------------
    cve_uri = DKG_CTI["CVE-2021-41773"]
    g.add((cve_uri, RDF.type, DKG.Vulnerability))
    g.add((cve_uri, RDFS.label, Literal("CVE-2021-41773 - Apache Path Traversal", lang="fr")))
    g.add((cve_uri, DKG.cvssScore, Literal(7.5, datatype=XSD.float)))
    g.add((cve_uri, DKG.isCisaKev, Literal(True, datatype=XSD.boolean)))
    
    # -------------------------------------------------------------------------
    # 2. Instanciation CWE-22 (MITRE Weakness)
    # -------------------------------------------------------------------------
    cwe_uri = DKG_CTI["CWE-22"]
    g.add((cwe_uri, RDF.type, DKG.Weakness))
    g.add((cwe_uri, RDFS.label, Literal("CWE-22: Path Traversal", lang="en")))
    
    # Liaison CVE -> CWE
    g.add((cve_uri, DKG.exploitsWeakness, cwe_uri))

    # -------------------------------------------------------------------------
    # 3. Instanciation CAPEC-126 (MITRE Threat Pattern)
    # -------------------------------------------------------------------------
    capec_uri = DKG_CTI["CAPEC-126"]
    g.add((capec_uri, RDF.type, DKG.ThreatPattern))
    g.add((capec_uri, RDFS.label, Literal("CAPEC-126: Directory Traversal", lang="en")))
    
    # Liaison CWE -> CAPEC
    g.add((cwe_uri, DKG.hasThreatPattern, capec_uri))

    # -------------------------------------------------------------------------
    # 4. Ancrage Cross-TLP (TLP:RED -> TLP:CLEAR)
    # Lien entre le composant local et l'instance CTI externe
    # -------------------------------------------------------------------------
    apache_uri = DKG_DATA["Apache-2.4.49"]
    g.add((apache_uri, DKG.hasVulnerability, cve_uri))

    # -------------------------------------------------------------------------
    # 5. Sérialisation Turtle
    # -------------------------------------------------------------------------
    ABOX_CTI_PATH.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(ABOX_CTI_PATH), format="turtle")
    print(f"✅ Graphe ABox CTI généré avec succès : {ABOX_CTI_PATH}")

    # -------------------------------------------------------------------------
    # 6. Génération automatisée de la documentation de synthèse (02_SYNTHESE_ABOX_CTI.md)
    # -------------------------------------------------------------------------
    generate_markdown_summary(g)

def generate_markdown_summary(graph: Graph):
    """Génère la documentation Markdown de synthèse pour l'ABox CTI Externe."""
    md_content = f"""# 📊 Synthèse ABox CTI Externe (`TLP:CLEAR`)

> **Généré automatiquement par :** `generate_phase3_cti_abox.py`  
> **Classification :** `TLP:CLEAR`  
> **Nombre total de triples :** `{len(graph)}`  

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
* **Relation :** `dkg:hasVulnerability` $\rightarrow$ `dkg-cti:CVE-2021-41773`
"""
    with open(DOC_CTI_MD_PATH, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"📝 Synthèse Markdown générée avec succès : {DOC_CTI_MD_PATH}")

if __name__ == "__main__":
    generate_cti_abox()
