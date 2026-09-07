# Extrait Sémantique : DKG_ABox_CTI_External.ttl
**Source** : `02-Donnees/Snapshots_Phases/Phase3_CTI/DKG_ABox_CTI_External.ttl`  
**Nombre total de triplets** : `20`  

---
## 1. Classes déclarées
_Aucune classe explicitement déclarée._

## 2. Propriétés
_Aucune propriété explicitement déclarée._

## 3. Échantillon de Triplets (Top 20)
| Sujet | Prédicat | Objet |
| :--- | :--- | :--- |
| `ABox_CTI_External` | `type` | `Ontology` |
| `CAPEC-100` | `type` | `ThreatPattern` |
| `CAPEC-586` | `label` | `Object Injection` |
| `CVE-2023-4863` | `hasWeakness` | `CWE-119` |
| `CAPEC-100` | `label` | `Overflow Buffers` |
| `CWE-119` | `type` | `Weakness` |
| `CVE-2021-44228` | `hasWeakness` | `CWE-502` |
| `CWE-119` | `hasThreatPattern` | `CAPEC-100` |
| `CVE-2023-4863` | `comment` | `Heap buffer overflow in WebP in Google Chrome prior to 116.0.5845.187.` |
| `CVE-2021-44228` | `comment` | `Apache Log4j2 JNDI features do not protect against attacker controlled LDAP endpoints.` |
| `CAPEC-586` | `type` | `ThreatPattern` |
| `CAPEC-100` | `comment` | `Attacker targets a buffer overflow vulnerability to execute shellcode or cause DoS.` |
| `CWE-502` | `type` | `Weakness` |
| `CAPEC-586` | `comment` | `An attacker injects malicious objects into an application to execute arbitrary code.` |
| `CWE-502` | `hasThreatPattern` | `CAPEC-586` |
| `CVE-2021-44228` | `type` | `Vulnerability` |
| `ABox_CTI_External` | `label` | `DKG External CTI Feed - TLP:CLEAR` |
| `CVE-2021-44228` | `cvssScore` | `10.0` |
| `CVE-2023-4863` | `cvssScore` | `8.8` |
| `CVE-2023-4863` | `type` | `Vulnerability` |