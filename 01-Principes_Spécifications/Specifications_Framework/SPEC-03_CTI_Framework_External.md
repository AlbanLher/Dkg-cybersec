_(Phase 2/3 : Instances Vulnérabilités & Mappings)_
# 📐 SPEC-03 : Framework CTI Externe & Superposition Cross-TLP (`TLP:CLEAR`)

> **Projet :** DKG-CyberSec  
> **Classification :** `TLP:AMBER` (Modèle) / Ingestion : `TLP:CLEAR`  
> **Évolution :** Absorbe le périmètre RBox/Propriétés de relations externes  
> **Statut :** Formalisé (Wave 2 / Phase 2.5)  

---

## 🎯 1. Objet
Définir le cadre d'ingestion des référentiels CTI ouverts (NVD, MITRE, CISA KEV) et leur raccordement avec le socle TBox/ABox existant.

---

## 🧬 2. Modèle de Rôles & Relations (RBox / Object Properties)

| Propriété (Role) | Domain (Source) | Range (Cible) | Nature OWL / TLP |
| :--- | :--- | :--- | :--- |
| `dkg:hasVulnerability` | `dkg:SoftwareComponent` (`TLP:RED`) | `dkg:Vulnerability` (`TLP:CLEAR`) | `owl:ObjectProperty` (Lien Cross-TLP) |
| `dkg:exploitsWeakness` | `dkg:Vulnerability` (`TLP:CLEAR`) | `dkg:Weakness` (`TLP:CLEAR`) | `owl:ObjectProperty` |
| `dkg:hasThreatPattern` | `dkg:Weakness` (`TLP:CLEAR`) | `dkg:ThreatPattern` (`TLP:CLEAR`) | `owl:ObjectProperty` |

---

## 📊 3. Dictionnaire de Données CTI (`Datatype Properties`)

| Propriété       | Domaine             | Type XSD      | Description                                  |
| :-------------- | :------------------ | :------------ | :------------------------------------------- |
| `dkg:cvssScore` | `dkg:Vulnerability` | `xsd:float`   | Score de sévérité CVSS.                      |
| `dkg:isCisaKev` | `dkg:Vulnerability` | `xsd:boolean` | Indicateur d'exploitation active (CISA KEV). |