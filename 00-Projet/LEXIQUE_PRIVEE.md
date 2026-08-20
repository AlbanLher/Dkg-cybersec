# 🔒 Lexique Privé : Jargon Métier, Code Names & Topologie Interne

Ce référentiel confidentiel rassemble la nomenclature interne, les acronymes de projets et le jargon d'entreprise.

---

### [CriticalAssetConcept] Actif Critique Métier
* **URI Ontologie :** `entreprise:CriticalAsset`
* **Terme Officiel (prefLabel) :** Actif Critique Métier
* **Jargon & Acronymes (altLabel) :** SRV-CRIT, Bécane Compta, Machine Cœur de Réseau, Node-Core
* **Définition Métier :** Équipement hébergeant des données de santé ou financières soumises à une indisponibilité maximale de 15 minutes.
* **Exemple d'Usage :** *"La Bécane Compta SRV-FIN-01 est classée Actif Critique."*

---

### [InternalZoneConcept] Zone Enclave Interne & Salles Blanches
* **URI Ontologie :** `entreprise:InternalZone`
* **Terme Officiel (prefLabel) :** Enclave Sécurisée Interne
* **Jargon & Acronymes (altLabel) :** Landing Zone Prod, Zone PCI-DSS, Bulle Sanctuarisée, Z-PROD-01
* **Définition Métier :** Zone isolée du SI soumise aux contrôles renforcés d'accès et au chiffrement de bout en bout.
* **Exemple d'Usage :** *"Seuls les flux authentifiés peuvent pénétrer la Bulle Sanctuarisée Z-PROD-01."*

---

### [BusinessUnitConcept] Entité & Propriétaire Applicatif
* **URI Ontologie :** `entreprise:BusinessUnit`
* **Terme Officiel (prefLabel) :** Unité d'Organisation Métier
* **Jargon & Acronymes (altLabel) :** BU, Branch, Propriétaire, Responsible Party, AppOwner
* **Définition Métier :** Entité interne ou direction opérationnelle responsable du budget et de la conformité d'un actif.