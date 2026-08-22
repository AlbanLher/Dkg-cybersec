# 🌐 Lexique Public : Standards Cyber & Architecture SI

Ce référentiel contient le vocabulaire standardisé et le jargon sectoriel ouvert (CVE, MITRE ATT&CK, catégories d'équipements génériques).

---

### [AssetConcept] Équipement Système Générique
* **URI Ontologie :** `cyber:Device`
* **Terme Officiel (prefLabel) :** Équipement Système
* **Jargon & Acronymes (altLabel) :** Serveur, Machine, Host, Node, Bare-Metal, Compute Instance
* **Erreurs Fréquentes (hiddenLabel) :** Srvur, Servuer
* **Définition Métier :** Ressource matérielle ou virtuelle dotée d'une adresse IP et hébergeant des composants logiciels.
* **Exemple d'Usage :** *"L'hôte physique exécute deux machines virtuelles."*

---

### [VulnerabilityConcept] Vulnérabilité & Faille Publique
* **URI Ontologie :** `cyber:Vulnerability`
* **Terme Officiel (prefLabel) :** Vulnérabilité Sécurité
* **Jargon & Acronymes (altLabel) :** CVE, Faille, Flaw, Trou de sécurité, Bug, Weakness
* **Erreurs Fréquentes (hiddenLabel) :** Vulnerabilite, Vullnerabilite
* **Définition Métier :** Faiblesse identifiée dans un composant logiciel (référencée ou non dans la base NVD/CVE) pouvant être exploitée.
* **Exemple d'Usage :** *"La vulnérabilité CVE-2026-1042 possède un score CVSS v3 de 9.8."*

---

### [PublicZoneConcept] Zone Réseau Générique
* **URI Ontologie :** `cyber:Environment`
* **Terme Officiel (prefLabel) :** Zone Réseau Standard
* **Jargon & Acronymes (altLabel) :** DMZ, LAN, Subnet, Segment, Perimeter
* **Définition Métier :** Périmètre réseau abstrait défini par un niveau d'exposition et des politiques de filtrage standardisées.