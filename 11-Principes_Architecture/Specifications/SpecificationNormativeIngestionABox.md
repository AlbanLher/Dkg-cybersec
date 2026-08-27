**Référence Documentaire :** `SPEC-ABOX-001`
**Statut :** Normatif
**Portée :** Phase 2 - Ancrage des Instances de SI Privé sur la TBox Maître
**Dépendance Cible :** `12-Donnees/TBox_init/TBox_Cybersec.ttl` (`[http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)`)

## 1. Objet & Principes Directeurs

La présente spécification définit les règles d'ingestion des données brutes d'inventaire (`inventory.json`) et leur transformation en triplets RDF/Turtle ABox (`ABox_Cybersec.ttl`).

L'objectif principal est de créer les **Named Individuals** (instances) représentants les actifs et briques physiques/logiques du SI, en assurant un **alignement strict et exhaustif** avec les concepts déclarés dans le Référentiel TBox de Phase 1.

```
       [ Source Brute SI ]                    [ Référentiel Phase 1 ]
   12-Donnees/ABox_init/inventory.json    12-Donnees/TBox_init/TBox_Cybersec.ttl
               │                                      │
               │ (Parsing & Mapping RDF)              │ (Imports / Alignement)
               └───► [ 12-Donnees/ABox_init/ABox_Cybersec.ttl ] ◄───┘
```

## 2. Déclaration des Namespaces & Ontologie ABox

- **EXG-ABOX-NS-01 (Espaces de Noms)** :
    
    L'ABox privée doit utiliser le namespace de base dédié `[http://dkg.cybersec.org/abox#](http://dkg.cybersec.org/abox#)` (préfixe `abox:`), et importer explicitement le namespace TBox `[http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)` (préfixe `dkg:`).
    
- **EXG-ABOX-NS-02 (Liaison à la TBox)** :
    
    L'ontologie ABox doit contenir une directive d'import OWL vers la TBox maître :
    
    Extrait de code
    
    ```
    <http://dkg.cybersec.org/abox#> a owl:Ontology ;
        owl:imports <http://dkg.cybersec.org/tbox#> .
    ```
    

## 3. Matrice de Mapping JSON $\rightarrow$ Ontologie TBox

Toute entité extraite du fichier d'inventaire source doit impérativement respecter la grille de correspondance suivante :

| **Champ JSON (inventory.json)**              | **Type / Propriété RDF cible (TBox)**            | **Plage / Structure Cible**                                                  | **Exemple de Génération RDF**                                    |
| -------------------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `assets[].id`                                | `rdf:type` $\rightarrow$ `dkg:Asset`             | Named Individual                                                             | `abox:srv-web-01 a dkg:Asset .`                                  |
| `assets[].label`                             | `rdfs:label`                                     | Literal (`xsd:string` @fr)                                                   | `rdfs:label "Serveur Web Production"@fr`                         |
| `assets[].ip`                                | Propriété DataType de TBox (ex: `dkg:ipAddress`) | Literal (`xsd:string`)                                                       | `dkg:ipAddress "192.168.1.10"`                                   |
| `installed_software[]`                       | `rdf:type` $\rightarrow$ `dkg:SoftwareComponent` | Named Individual                                                             | `abox:sw-nginx-1201 a dkg:SoftwareComponent .`                   |
| `assets[].installed_software`                | Propriété Objet : `dkg:hasInstalledComponent`    | Domaine: `dkg:Asset`<br><br>  <br><br>Range: `dkg:SoftwareComponent`         | `abox:srv-web-01 dkg:hasInstalledComponent abox:sw-nginx-1201 .` |
| `installed_software[].known_vulnerabilities` | Propriété Objet : `dkg:hasVulnerability`         | Domaine: `dkg:SoftwareComponent`<br><br>  <br><br>Range: `dkg:Vulnerability` | `abox:sw-nginx-1201 dkg:hasVulnerability abox:CVE-2021-23017 .`  |

## 4. Exigences Normatives d'Ingestion & Validation (EXG-ABOX)

### 4.1 Identifiants & URIs

- **EXG-ABOX-URI-01 (Normalisation)** : Tout identifiant local (ex: `srv-web-01`) doit être assaini pour former une URI RFC-3986 valide sous l'espace `[http://dkg.cybersec.org/abox#](http://dkg.cybersec.org/abox#)`.
    
- **EXG-ABOX-URI-02 (Unicité des Instances)** : Deux composants possédant le même CPE ou la même identification réseau doivent réutiliser la même URI d'instance au sein de l'ABox.
    

### 4.2 Typage & Conformité TBox

- **EXG-ABOX-TYP-01 (Typage Référentiel)** : Aucune instance ne peut exister sans au moins une déclaration `rdf:type` désignant une classe OWL valide du référentiel TBox (`dkg:Asset`, `dkg:SoftwareComponent`, `dkg:Vulnerability`, `dkg:Weakness`).
    
- **EXG-ABOX-TYP-02 (Respect des Domaines & Ranges)** : Tout triplet d'instance $(S, P, O)$ reliant deux individus ABox doit respecter les contraintes `rdfs:domain` et `rdfs:range` stipulées dans `TBox_Cybersec.ttl`.
    

### 4.3 Traçabilité & Provenance

- **EXG-ABOX-PROV-01 (Métadonnées de Phase)** : Le fichier généré `ABox_Cybersec.ttl` doit contenir les annotations `rdfs:comment` et `dcterms:created` spécifiant le script d'ingestion source et l'horodatage d'exécution.



---- Intégration a vérifier !!

- **EXG-ABOX-01 (Nommage des URIs / Named Individuals)** : Toutes les instances ABox doivent utiliser le namespace `[http://dkg.cybersec.org/abox#](http://dkg.cybersec.org/abox#)` (ex: `abox:srv-web-01`).
    
- **EXG-ABOX-02 (Typage TBox)** : Chaque instance créée doit comporter une déclaration de type RDF (`rdf:type`) pointant vers une classe valide de la TBox (`dkg:Asset`, `dkg:SoftwareComponent`, `dkg:Vulnerability`).
    
- **EXG-ABOX-03 (Relations d'Inventaire)** :
    
    - Les liens entre Asset et Logiciel doivent utiliser la propriété `dkg:hasInstalledComponent`.
        
    - Les liens entre Logiciel et Vulnérabilité doivent utiliser la propriété `dkg:hasVulnerability`.
        
- **EXG-ABOX-04 (Traceabilité de la Source)** : Les métadonnées d'instanciation (date d'ingestion, fichier source) doivent être attachées à l'ontologie ABox via `rdfs:comment` ou `dcterms:source`.
