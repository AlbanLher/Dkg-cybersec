# Extrait Sémantique : DKG_ABox_Master.ttl
**Source** : `02-Donnees/Master_Transversal/DKG_ABox_Master.ttl`  
**Nombre total de triplets** : `57`  

---
## 1. Classes déclarées
_Aucune classe explicitement déclarée._

## 2. Propriétés
* **`hasThreatPattern`** [ObjectProperty]: has threat pattern

## 3. Échantillon de Triplets (Top 20)
| Sujet | Prédicat | Objet |
| :--- | :--- | :--- |
| `CWE-22` | `label` | `Improper Limitation of a Pathname to a Restricted Directory` |
| `CWE-22` | `type` | `Weakness` |
| `CAPEC-63` | `label` | `Simple Pass-Through` |
| `CWE-22` | `isWeaknessExploitedBy` | `CVE-2021-41773` |
| `CAPEC-126` | `label` | `Path Traversal` |
| `CWE-22` | `hasThreatPattern` | `CAPEC-126` |
| `CAPEC-63` | `description` | `Attacker executes arbitrary code by passing commands through input fields.` |
| `Comp-Apache-2-4-49` | `isInstalledComponentOf` | `Asset-Srv-Prod-01` |
| `Asset-Srv-Auth-02` | `type` | `Asset` |
| `Asset-Srv-Prod-01` | `hasTLPMarking` | `TLP-AMBER` |
| `TLP-CLEAR` | `type` | `TLPMarking` |
| `Asset-Srv-Auth-02` | `hasTLPMarking` | `TLP-RED` |
| `CVE-2021-41773` | `exploitsWeakness` | `CWE-22` |
| `CVE-2021-44228` | `cvssScore` | `10.0` |
| `CWE-78` | `label` | `Improper Neutralization of Special Elements used in an OS Command` |
| `hasThreatPattern` | `range` | `ThreatPattern` |
| `CAPEC-63` | `isThreatPatternOf` | `CWE-78` |
| `ABox_Master` | `tlpMarking` | `TLP:RED` |
| `CVE-2021-41773` | `cvssScore` | `7.5` |
| `hasThreatPattern` | `type` | `ObjectProperty` |