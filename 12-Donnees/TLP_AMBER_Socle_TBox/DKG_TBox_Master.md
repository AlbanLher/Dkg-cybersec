# 📖 DKG TBox Master - Ontologie Canonique

> **Classification** : `TLP:AMBER`  
> **Répertoire** : `12-Donnees/TLP_AMBER_Socle_TBox/`

## 📌 Classes

| Classe | URI | Description |
| :--- | :--- | :--- |
| **`dkg:Asset`** | `http://dkg.cybersec.org/tbox#Asset` | Concept du modèle DKG |
| **`dkg:SoftwareComponent`** | `http://dkg.cybersec.org/tbox#SoftwareComponent` | Concept du modèle DKG |
| **`dkg:TLPMarking`** | `http://dkg.cybersec.org/tbox#TLPMarking` | Concept du modèle DKG |
| **`dkg:ThreatPattern`** | `http://dkg.cybersec.org/tbox#ThreatPattern` | Concept du modèle DKG |
| **`dkg:Vulnerability`** | `http://dkg.cybersec.org/tbox#Vulnerability` | Concept du modèle DKG |
| **`dkg:Weakness`** | `http://dkg.cybersec.org/tbox#Weakness` | Concept du modèle DKG |

## 🔗 Propriétés d'Objets

| Propriété | Domaine | Range |
| :--- | :--- | :--- |
| **`dkg:hasInstalledComponent`** | `dkg:Asset` | `dkg:SoftwareComponent` |
| **`dkg:hasTLPMarking`** | `dkg:Thing` | `dkg:TLPMarking` |
| **`dkg:hasThreatPattern`** | `dkg:Weakness` | `dkg:ThreatPattern` |
| **`dkg:hasVulnerability`** | `dkg:SoftwareComponent` | `dkg:Vulnerability` |
| **`dkg:hasWeakness`** | `dkg:Vulnerability` | `dkg:Weakness` |
| **`dkg:isComponentOf`** | `dkg:SoftwareComponent` | `dkg:Asset` |

## 🏷️ Propriétés de Données (Attributs)

| Attribut | Domaine | Datatype |
| :--- | :--- | :--- |
| **`dkg:componentName`** | `dkg:SoftwareComponent` | `xsd:string` |
| **`dkg:cveDescription`** | `dkg:Vulnerability` | `xsd:string` |
| **`dkg:cveId`** | `dkg:Vulnerability` | `xsd:string` |
| **`dkg:cvssScore`** | `dkg:Vulnerability` | `xsd:float` |
| **`dkg:cvssV3Vector`** | `dkg:Vulnerability` | `xsd:string` |
| **`dkg:hostname`** | `dkg:Asset` | `xsd:string` |
| **`dkg:ipAddress`** | `dkg:Asset` | `xsd:string` |
| **`dkg:lastEnrichedAt`** | `dkg:Thing` | `xsd:dateTime` |
| **`dkg:patternDescription`** | `dkg:ThreatPattern` | `xsd:string` |
| **`dkg:severityLabel`** | `dkg:Vulnerability` | `xsd:string` |
| **`dkg:tlpColor`** | `dkg:TLPMarking` | `xsd:string` |
| **`dkg:version`** | `dkg:SoftwareComponent` | `xsd:string` |