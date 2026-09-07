# Extrait Sémantique : DKG_ABox_Infered.ttl
**Source** : `02-Donnees/Snapshots_Phases/Phase6_NER_Local/DKG_ABox_Infered.ttl`  
**Nombre total de triplets** : `213`  

---
## 1. Classes déclarées
* **`Asset`** (`Asset`): Ressource informatique du SI (serveur, poste, équipement réseau).
* **`SoftwareComponent`** (`SoftwareComponent`): Composant logiciel, bibliothèque ou dépendance système.
* **`TLPMarking`** (`TLPMarking`): Niveau de classification et de partage de l'information.
* **`ThreatActor`** (`Threat Actor`): Groupe ou entité menant des attaques ciblées (ex: APT).
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
* **`hasThreatPattern`** [ObjectProperty]: has threat pattern
* **`hasVulnerability`** [ObjectProperty]: has vulnerability
* **`hasWeakness`** [ObjectProperty]: has weakness
* **`hostname`** [DatatypeProperty]: hostname
* **`isComponentOf`** [ObjectProperty]: is component of
* **`isVulnerabilityOf`** [ObjectProperty]: is vulnerability of
* **`nerConfidenceScore`** [DatatypeProperty]: NER Confidence Score

## 3. Échantillon de Triplets (Top 20)
| Sujet | Prédicat | Objet |
| :--- | :--- | :--- |
| `isComponentOf` | `inverseOf` | `hasInstalledComponent` |
| `TLPMarking` | `definition` | `Niveau de classification et de partage de l'information.` |
| `hasWeakness` | `prefLabel` | `has weakness` |
| `RuleThreatCampaignPropagation` | `comment` | `Lie une campagne CTI externe à un actif interne hébergeant le composant visé.` |
| `RuleThreatCampaignPropagation` | `rule` | `n5f4cbfb918604a5baa164d51ca15ab48b2` |
| `hasTLPMarking` | `comment` | `Applique une classification TLP sur l'entité` |
| `TLPMarking` | `altLabel` | `Niveau de confidentialité` |
| `Asset` | `label` | `Asset` |
| `CAPEC-586` | `type` | `ThreatPattern` |
| `isVulnerabilityOf` | `type` | `ObjectProperty` |
| `ThreatActor` | `prefLabel` | `Threat Actor` |
| `hasVulnerability` | `comment` | `Lie un composant à une vulnérabilité connue` |
| `CWE-502` | `type` | `Weakness` |
| `hasThreatPattern` | `domain` | `Weakness` |
| `ThreatPattern` | `altLabel` | `Mode opératoire d'attaque` |
| `cveId` | `prefLabel` | `identifiant CVE` |
| `cvssScore` | `prefLabel` | `CVSS score` |
| `CAPEC-63` | `label` | `Simple Pass-Through` |
| `SoftwareComponent` | `prefLabel` | `Composant Logiciel` |
| `RuleThreatCampaignPropagation` | `label` | `Règle R-02 : Propagation Cible de Campagne de Menace` |