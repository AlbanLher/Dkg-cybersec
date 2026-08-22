# 📖 Lexique Métier : Architecture SI & Cybersécurité

Ce document est le référentiel contrôlé du vocabulaire. Il est synchronisé automatiquement avec le graphe de connaissances (DKG) et les modèles de langue.

---

### [AssetConcept] Équipement Système & Hôte
* **Identifiant URI :** `cyber:Device`
* **Domaine :** Architecture & Infra
* **Terme Officiel (prefLabel) :** Équipement Système
* **Jargon & Acronymes (altLabel) :** Serveur, Machine, Host, SRV, Bécane, Instance, Bare-Metal
* **Erreurs Fréquentes (hiddenLabel) :** Srvur, Servuer
* **Définition Métier :** Ressource physique ou virtuelle dotée d'une adresse IP et hébergeant des composants logiciels ou des services.
* **Exemple d'Usage :** *"L'instance SRV-WEB-01 est déployée sur l'hôte physique HYP-01."*

---

### [ComponentConcept] Composant Applicatif & Service
* **Identifiant URI :** `cyber:Software`
* **Domaine :** Architecture
* **Terme Officiel (prefLabel) :** Composant Logiciel
* **Jargon & Acronymes (altLabel) :** Application, App, Service, Brique, Micro-service, Package, Middleware
* **Définition Métier :** Programme ou ensemble d'exécutables exécutés sur un équipement pour fournir une fonction applicative.
* **Exemple d'Usage :** *"Le middleware Tomcat est le composant applicatif impacté."*

---

### [ZoneConcept] Zone Réseau & Partitionment
* **Identifiant URI :** `cyber:Environment`
* **Domaine :** Architecture & Cyber
* **Terme Officiel (prefLabel) :** Zone Réseau
* **Jargon & Acronymes (altLabel) :** DMZ, LAN, Segment, Zone Externe, Enclave, Landing Zone, Subnet
* **Définition Métier :** Périmètre réseau isolé soumis à une politique de filtrage et à un niveau de confiance homogène.
* **Exemple d'Usage :** *"Les API publiques doivent résider dans la Landing Zone DMZ."*

---

### [VulnerabilityConcept] Vulnérabilité & Faille
* **Identifiant URI :** `cyber:Vulnerability`
* **Domaine :** Cyber
* **Terme Officiel (prefLabel) :** Vulnérabilité Sécurité
* **Jargon & Acronymes (altLabel) :** CVE, Faille, Flaw, Trou de sécurité, Brèche, Defaut
* **Erreurs Fréquentes (hiddenLabel) :** Vulnerabilite, Vullnerabilite
* **Définition Métier :** Faiblesse dans un composant ou une configuration pouvant être exploitée pour porter atteinte au système.
* **Exemple d'Usage :** *"La CVE-2026-1234 représente une brèche critique."*

---

### [RequirementConcept] Exigence & Règle de Conformité
* **Identifiant URI :** `cyber:Requirement`
* **Domaine :** Cyber & Compliance
* **Terme Officiel (prefLabel) :** Exigence de Sécurité
* **Jargon & Acronymes (altLabel) :** Mesure, Control, Règle NIS2, Directive, Standard, Safeguard
* **Définition Métier :** Obligation technique ou organisationnelle issue d'un référentiel (NIS2, ISO 27001) imposée à un composant ou une zone.
* **Exemple d'Usage :** *"L'exigence de chiffrement s'applique à la zone DMZ."*
