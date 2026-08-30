

## Fichiers
### `TBox_init.ttl`
```ttl
@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

dkg: a owl:Ontology ;
    rdfs:label "Ontologie DKG Cybersec"@fr ;
    rdfs:comment "TBox minimale pour le DKG Cybersec - Phase 1 Initialisation"@fr .

dkg:classifiedUnder a owl:ObjectProperty ;
    rdfs:label "classé sous faiblesse"@fr ;
    rdfs:domain dkg:Vulnerability ;
    rdfs:range dkg:Weakness .

dkg:hasInstalledComponent a owl:ObjectProperty ;
    rdfs:label "a composant installé"@fr ;
    rdfs:domain dkg:Asset ;
    rdfs:range dkg:SoftwareComponent .

dkg:hasVulnerability a owl:ObjectProperty ;
    rdfs:label "présente vulnérabilité"@fr ;
    rdfs:domain dkg:SoftwareComponent ;
    rdfs:range dkg:Vulnerability .

dkg:Asset a owl:Class ;
    rdfs:label "Actif Privé"@fr ;
    rdfs:comment "Équipement informatique physique ou virtuel du SI."@fr ;
    skos:altLabel "Host"@fr,
        "Machine"@fr,
        "Serveur"@fr,
        "Équipement"@fr .

dkg:Weakness a owl:Class ;
    rdfs:label "Faiblesse Logicielle"@fr ;
    rdfs:comment "Catégorisation des erreurs de conception/code."@fr ;
    skos:altLabel "CWE"@fr,
        "Faiblesse"@fr .

dkg:SoftwareComponent a owl:Class ;
    rdfs:label "Composant Logiciel"@fr ;
    rdfs:comment "Brique logicielle ou système d'exploitation installé."@fr ;
    skos:altLabel "Application"@fr,
        "CPE"@fr,
        "OS"@fr,
        "Package"@fr .

dkg:Vulnerability a owl:Class ;
    rdfs:label "Vulnérabilité"@fr ;
    rdfs:comment "Faille de sécurité répertoriée publiquement."@fr ;
    skos:altLabel "Breche"@fr,
        "CVE"@fr,
        "Faille"@fr .
```


### `ABox_init.ttl`

@prefix abox: <http://dkg.cybersec.org/abox#> .
@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

abox: a owl:Ontology ;
    rdfs:label "ABox Instance Graph - DKG Cybersec"@fr ;
    rdfs:comment "Généré automatiquement par ingest_inventory.py le Thu Aug 27 13:12:55 2026"@fr ;
    owl:imports dkg: .

abox:srv-web-01 a dkg:Asset ;
    rdfs:label "Serveur Web Production"@fr ;
    dkg:hasInstalledComponent abox:sw-nginx-1201 ;
    dkg:ipAddress "192.168.1.10"^^xsd:string .

abox:CVE-2021-23017 a dkg:Vulnerability ;
    rdfs:label "Vulnérabilité CVE-2021-23017"@fr .

abox:sw-nginx-1201 a dkg:SoftwareComponent ;
    rdfs:label "NGINX Web Server"@fr ;
    dkg:cpeIdentifier "cpe:2.3:a:f5:nginx:1.20.1:*:*:*:*:*:*:*"^^xsd:string ;
    dkg:hasVulnerability abox:CVE-2021-23017 ;
    dkg:version "1.20.1"^^xsd:string .






### `TLP-AMBER_TBox_Cybersec.ttl`

@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

dkg: a owl:Ontology ;
    rdfs:label "DKG Cybersecurity Master TBox (TLP:AMBER)"@en ;
    rdfs:comment "Ontologie maître et dictionnaire sémantique du DKG."@fr .

dkg:classifiedUnder a owl:ObjectProperty ;
    rdfs:label "est classé sous la faiblesse"@fr ;
    rdfs:domain dkg:Vulnerability ;
    rdfs:range dkg:Weakness .

dkg:cvssScore a owl:DatatypeProperty ;
    rdfs:label "Score CVSS (0.0 - 10.0)"@fr ;
    rdfs:domain dkg:Vulnerability ;
    rdfs:range xsd:float .

dkg:cvssVector a owl:DatatypeProperty ;
    rdfs:label "Vecteur CVSS v3.1"@fr ;
    rdfs:domain dkg:Vulnerability ;
    rdfs:range xsd:string .

dkg:hasInstalledComponent a owl:ObjectProperty ;
    rdfs:label "a installé le composant"@fr ;
    rdfs:domain dkg:Asset ;
    rdfs:range dkg:SoftwareComponent .

dkg:hasVulnerability a owl:ObjectProperty ;
    rdfs:label "présente la vulnérabilité"@fr ;
    rdfs:domain dkg:SoftwareComponent ;
    rdfs:range dkg:Vulnerability .

dkg:ipAddress a owl:DatatypeProperty ;
    rdfs:label "Adresse IP"@fr ;
    rdfs:domain dkg:Asset ;
    rdfs:range xsd:string .

dkg:Weakness a owl:Class ;
    rdfs:label "Faiblesse Logicielle / CWE"@fr ;
    rdfs:comment "Catégorie de défaut de conception ou d'implémentation (ex: CWE-193)."@fr .

dkg:Asset a owl:Class ;
    rdfs:label "Équipement informatique / Asset SI"@fr ;
    rdfs:comment "Toute ressource matérielle ou virtuelle du SI."@fr .

dkg:SoftwareComponent a owl:Class ;
    rdfs:label "Composant Logiciel"@fr ;
    rdfs:comment "Brique logicielle, service ou application installée."@fr .

dkg:Vulnerability a owl:Class ;
    rdfs:label "Vulnérabilité / Faille"@fr ;
    rdfs:comment "Faille de sécurité référencée (ex: CVE)."@fr .




### `TLP-RED_ABox_Cybersec.ttl`

@prefix abox: <http://dkg.cybersec.org/abox#> .
@prefix dkg: <http://dkg.cybersec.org/tbox#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rbox: <http://dkg.cybersec.org/rbox#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

abox: a owl:Ontology ;
    owl:imports dkg: .

abox:srv-web-01 a dkg:Asset ;
    rdfs:label "Serveur Web Production"@fr ;
    dkg:hasInstalledComponent abox:sw-nginx-1201 ;
    dkg:ipAddress "192.168.1.50"^^xsd:string .

abox:sw-nginx-1201 a dkg:SoftwareComponent ;
    rdfs:label "NGINX Web Server v1.20.1"@fr ;
    dkg:hasVulnerability rbox:CVE-2021-23017 .


## Analyse comparative

Des fichiers du dépôt Git (`12-Donnees/`) permettant d'identifier la conformité du modèle, les dérives constatées et le statut d'opérationnalité de chaque composant.

### Analyse Comparative des Fichiers DKG

| **Fichier / Composant**                                | **Rôle & Contenu**                                                                                                                   | **Statut**       | **Dérives & Incohérences Détectées**                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`TBox_Cybersec.ttl`**<br><br>  <br><br>_(TLP:AMBER)_ | Déclaration des classes (`Asset`, `SoftwareComponent`, `Vulnerability`) et propriétés (`hasInstalledComponent`, `hasVulnerability`). | **NON CONFORME** | **Namespace hybride et non unifié** : La TBox déclare des propriétés avec le préfixe `[http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)`, mais génère une instabilité dans l'ABox lorsque les URIs cibles (comme les CVE/CWE) sautent vers un namespace `rbox#` sans alignement strict. |
| **`ABox_Cybersec.ttl`**<br><br>  <br><br>_(TLP:RED)_   | Instances d'équipements (`srv-web-01`), logiciels et liens contextuels.                                                              | **NON CONFORME** | **Absence des Object Properties (Relations)** : Le fichier crée l'individu `srv-web-01` et l'individu `sw-nginx-1201`, mais n'écrit jamais le triplet `abox:srv-web-01 dkg:hasInstalledComponent abox:sw-nginx-1201`. Les nœuds restent totalement orphelins en mémoire.                             |
| **`RBox_Cybersec.ttl`**<br><br>  <br><br>_(TLP:CLEAR)_ | Enrichissement des failles (CVE-2021-23017 $\rightarrow$ CWE-193, score CVSS).                                                       | **PARTIEL**      | **Dépendance stricte sans fallback** : Les triplets CVE $\rightarrow$ CVSS et CVE $\rightarrow$ CWE existent, mais la RBox s'attend à ce que l'ABox pointe vers le même schéma exact de préfixe (`rbox#CVE-...`). En cas de divergence sur le hash/slash (`/` vs `#`), la correspondance échoue.     |
| **`TLP_ABox.md`**<br><br>  <br><br>_(Source Initiale)_ | Fichier Markdown d'inventaire source servant à la conversion.                                                                        | **NON CONFORME** | **Perte de structure au parsing** : Le parser qui lit ce fichier génère les métadonnées de surface (IP, Label) mais abandonne l'extraction de l'arborescence des sous-éléments (Composants), provoquant la génération d'une ABox incomplète.                                                         |

### Synthèse des Écarts Didactiques

**1. La dérive du graphe orphelin (ABox)** Le problème majeur réside dans la dissociation entre la **déclaration d'existence** et la **relation de structure**. L'ABox d'origine déclare l'équipement et le logiciel dans le même fichier, mais omets d'écrire l'arc RDF (`dkg:hasInstalledComponent`). 
En Semantic Web, l'absence de triplet équivaut à une inexistence de lien, d'où le résultat vide lors de la traversée SPARQL.

**2. La dérive de rupture de schéma (TBox / ABox)** Les règles métiers définies dans la TBox (`dkg:hasInstalledComponent rdfs:domain dkg:Asset`) exigent une correspondance exacte d'URI. La dérive constatée montre un décalage entre le modèle théorique et la sérialisation Python qui utilisait des variables dynamiques instables lors de l'export en Turtle.






Excellente démarche didactique. Mettre en évidence les ruptures de chaîne dans la modélisation RDF/OWL (TBox vs ABox vs RBox) est le meilleur moyen de comprendre la rigueur qu'impose le Semantic Web.

Voici l'analyse des écarts et des données manquantes observés dans vos fichiers `.ttl`, exploitable pour vos supports de cours ou synthèses pédagogiques.


### Synthèse des Écarts Didactiques par Fichier TTL

- **1. L'ABox (`12-Donnees/TLP-RED_ABox_Cybersec/ABox_Cybersec.ttl`)**
    
    - **Symptôme** : L'ABox isolait les entités sans créer les arcs de liaison.
        
    - **Analyse de l'écart** : Les individus `abox:srv-web-01` (Asset) et `abox:sw-nginx-1201` (Software) étaient instanciés avec leur type (`a dkg:Asset`), mais le triplet explicite `abox:srv-web-01 dkg:hasInstalledComponent abox:sw-nginx-1201` manquait. De même, la relation `dkg:hasVulnerability` vers `rbox:CVE-2021-23017` était omise.
        
    - **Impact didactique** : En RDF, la simple déclaration de coexistence dans un même fichier ne crée pas de relation. Sans arc explicite (Objet Property), SPARQL traite les nœuds comme un graphe disjoint.
        
- **2. La TBox (`12-Donnees/TLP-AMBER_TBox_Cybersec/TBox_Cybersec.ttl`)**
    
    - **Symptôme** : Décalage potentiel de Namespaces entre la TBox et les instances.
        
    - **Analyse de l'écart** : Les propriétés `dkg:hasInstalledComponent` et `dkg:hasVulnerability` sont correctement définies avec leurs domaines (`rdfs:domain`) et portées (`rdfs:range`). Cependant, l'utilisation de préfixes hybrides (ex: appeler une CVE sous `rbox#` alors que la TBox définit les propriétés sous `tbox#`) force l'ABox à réimporter explicitement le bon Namespace.
        
    - **Impact didactique** : Montre l'importance du contrat d'interface (Ontologie/TBox). Si le parser d'ABox n'utilise pas rigoureusement le même URI exact pour le prédicat, la requête SPARQL échoue silencieusement.
        
- **3. La RBox (`12-Donnees/TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.ttl`)**
    
    - **Symptôme** : Données d'enrichissement NVD/CWE parfois partielles ou isolées.
        
    - **Analyse de l'écart** : Les métadonnées (`dkg:cvssScore`, `dkg:classifiedUnder`) existent pour `rbox:CVE-2021-23017`, mais si l'ABox pointe vers `rbox:CVE-2021-23017` sans que le parser de la RBox n'ait instancié la classe `dkg:Vulnerability`, la traversée SPARQL sans bloc `OPTIONAL` élimine le résultat.
        
    - **Impact didactique** : Illustre la dépendance aux vocabulaires externes. L'enrichissement (Phase 3) échoue si la clé d'alignement (l'URI de la CVE) présente la moindre variation de casse ou de format.
        

### Tableau Récapitulatif pour Support Didactique

| **Composant DKG**    | **Rôle théorique**                               | **Erreur courante observée**                                | **Conséquence SPARQL**                  |
| -------------------- | ------------------------------------------------ | ----------------------------------------------------------- | --------------------------------------- |
| **TBox** (TLP:AMBER) | Modèle sémantique & Règles (`Class`, `Property`) | Incohérence dans la déclaration des Namespaces (`/` vs `#`) | Échec de résolution des préfixes        |
| **ABox** (TLP:RED)   | Instances concrètes (`Asset`, `Software`)        | Omission des Object Properties (`hasInstalledComponent`)    | Nœuds isolés (0 résultat sur jointure)  |
| **RBox** (TLP:CLEAR) | Connaissances externes (`CVE`, `CWE`, `CVSS`)    | Mismatch d'URI entre ABox et RBox                           | Enrichissement impossible (valeurs N/A) |
