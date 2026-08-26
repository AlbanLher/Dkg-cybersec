# Lexique du Projet : Dynamic Knowledge Graph (DKG) Cybersécurité

## 1. Concepts du Web Sémantique & Knowledge Graphs
* **TBox (Terminological Box)** : Le schéma / modèle de données abstrait. Il définit les classes (ex. `Asset`, `Vulnerability`), leurs propriétés et leurs relations. C'est l'équivalent du schéma de base de données.
* **ABox (Assertional Box)** : Les données d'instances réelles enregistrées selon le modèle de la TBox (ex. *"Le serveur SRV-WEB-01 instancie la classe Asset"*).
* **Ontologie** : Structuration formelle d'un domaine de connaissances au moyen d'un vocabulaire partagé (RDFS/OWL).
* **Named Graph** : Partitionnement logique du graphe global permettant d'isoler des ensembles de triplets (ex. `graph:public` pour les données CVE publiques vs `graph:private` pour l'inventaire confidentiel).
* **URI / IRI** : Identifiant unique mondial d'un nœud ou d'une relation (ex. `http://dkg.cybersec.org/tbox#Asset`).

## 2. Concepts Métier Cybersecurity
* **Asset (Actif)** : Équipement physique, serveur, machine virtuelle ou service critique appartenant au SI privé.
* **SoftwareComponent (Composant Logiciel)** : Application, librairie, OS ou package installé sur un actif (identifié souvent par un CPE).
* **Vulnerability / CVE (Common Vulnerabilities and Exposures)** : Faille de sécurité publique identifiée sur un composant logiciel spécifique.
* **Weakness / CWE (Common Weakness Enumeration)** : Catégorie d'erreur d'architecture ou de code sous-jacente à une ou plusieurs CVE.
* **Exposure (Exposition)** : Relation mesurée entre un actif privé et une vulnérabilité publique en fonction de son niveau de criticité (CVSS).