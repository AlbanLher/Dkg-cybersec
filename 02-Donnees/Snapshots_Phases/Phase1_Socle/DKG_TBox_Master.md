# Extrait Sémantique : DKG_TBox_Master.ttl
**Source** : `02-Donnees/Snapshots_Phases/Phase1_Socle/DKG_TBox_Master.ttl`  
**Nombre total de triplets** : `106`  

---
## 1. Classes déclarées
* **`Asset`** (`Asset`): Ressource informatique du SI (serveur, poste, équipement réseau).
* **`SoftwareComponent`** (`SoftwareComponent`): Composant logiciel, bibliothèque ou dépendance système.
* **`TLPMarking`** (`TLPMarking`): Niveau de classification et de partage de l'information.
* **`ThreatPattern`** (`ThreatPattern`): Motif ou schéma d'attaque documenté (CAPEC).
* **`Vulnerability`** (`Vulnerability`): Faiblesse logicielle exploitable répertoriée (CVE).
* **`Weakness`** (`Weakness`): Famille d'erreur logicielle sous-jacente (CWE).

## 2. Propriétés
* **`assetId`** [DatatypeProperty]: asset identifier
* **`componentId`** [DatatypeProperty]: component identifier
* **`cveId`** [DatatypeProperty]: CVE identifier
* **`cvssScore`** [DatatypeProperty]: CVSS score
* **`cweId`** [DatatypeProperty]: CWE identifier
* **`hasInstalledComponent`** [ObjectProperty]: has installed component
* **`hasTLPMarking`** [ObjectProperty]: has TLP marking
* **`hasVulnerability`** [ObjectProperty]: has vulnerability
* **`hasWeakness`** [ObjectProperty]: has weakness
* **`hostname`** [DatatypeProperty]: hostname
* **`isComponentOf`** [ObjectProperty]: is component of
* **`isVulnerabilityOf`** [ObjectProperty]: is vulnerability of

## 3. Échantillon de Triplets (Top 20)
| Sujet | Prédicat | Objet |
| :--- | :--- | :--- |
| `isComponentOf` | `inverseOf` | `hasInstalledComponent` |
| `TLPMarking` | `definition` | `Niveau de classification et de partage de l'information.` |
| `hasVulnerability` | `prefLabel` | `has vulnerability` |
| `Vulnerability` | `definition` | `Faiblesse logicielle exploitable répertoriée (CVE).` |
| `ThreatPattern` | `definition` | `Motif ou schéma d'attaque documenté (CAPEC).` |
| `hasWeakness` | `prefLabel` | `has weakness` |
| `hasTLPMarking` | `comment` | `Applique une classification TLP sur l'entité` |
| `Asset` | `label` | `Asset` |
| `TLPMarking` | `altLabel` | `Niveau de confidentialité` |
| `assetId` | `domain` | `Asset` |
| `isVulnerabilityOf` | `type` | `ObjectProperty` |
| `Vulnerability` | `prefLabel` | `Vulnerability` |
| `hasWeakness` | `prefLabel` | `est de type faiblesse` |
| `isVulnerabilityOf` | `prefLabel` | `is vulnerability of` |
| `hasVulnerability` | `comment` | `Lie un composant à une vulnérabilité connue` |
| `ThreatPattern` | `altLabel` | `Mode opératoire d'attaque` |
| `cveId` | `range` | `string` |
| `cveId` | `prefLabel` | `identifiant CVE` |
| `cvssScore` | `prefLabel` | `CVSS score` |
| `ThreatPattern` | `label` | `ThreatPattern` |