
## 1. Objet et Portée

Ce document définit les exigences formelles et les critères de conformité applicables à la **TBox (Terminological Box)** du Knowledge Graph Cyberdéfense (DKG).

Toute modification, mise à jour ou outil de génération automatique (script, pipeline CI/CD, Agent IA) **doit obligatoirement se conformer aux règles de cette spécification**.


## 2. Exigences d'Entrée et de Source de Vérité

- **EXG-SRC-01 (Source Unique)** : Le fichier Turtle `12-Donnees/TBox_init/TBox_Cybersec.ttl` constitue la **seule et unique source de vérité (SSOT)** du modèle ontologique.
    
- **EXG-SRC-02 (Grammaire)** : La TBox maître doit être rédigée selon la syntaxe W3C Turtle (`.ttl`) et exploiter les vocabulaires standard `owl`, `rdfs`, et `skos`.

- **P1-1 (Normalisation URI/Namespaces)** : Spécifier la convention stricte des séparateurs (`#` vs `/`) pour éviter la dérive des préfixes entre TBox, ABox et RBox.
    
- **P1-2 (Intégrité des Object Properties)** : Rendre obligatoire la présence des clauses `rdfs:domain` et `rdfs:range` sur chaque relation (`hasInstalledComponent`, `hasVulnerability`, etc.).
    
- **P1-3 (Co-évolution TBox $\rightarrow$ SHACL)** : Documenter la responsabilité de la TBox dans la définition ou l'export des règles de validation SHACL métiers.



## 3. Exigences sur les Sorties Dérivées (Multi-Formats)

Toute compilation ou extraction de la TBox maître doit produire automatiquement **deux artefacts dérivés dérivés** dans le répertoire `12-Donnees/TBox_init/` :
```
12-Donnees/TBox_init/
├── TBox_Cybersec.ttl        ◄── [Source de Vérité]
├── TBox_Cybersec.json       ◄── [Format Machine / API]
└── TBox_Cybersec.md         ◄── [Format Humain / Documentation & Lexique]
```

### 3.1. Spécification du Format Machine (`TBox_Cybersec.json`)

- **EXG-JSON-01 (Interface)** : Destiné à la consommation par des API, des validateurs de schémas et des modules d'ingestion automatisés.
    
- **EXG-JSON-02 (Contenu)** : Doit sérialiser l'intégralité des classes, propriétés d'objets, propriétés de données, synonymes (`skos:altLabel`) et descriptions (`rdfs:comment`).
    

### 3.2. Spécification du Format Humain & Lexique (`TBox_Cybersec.md`)

La version Markdown doit obligatoirement intégrer la dimension **Lexicalisation et Lisibilité Humaine** à travers 4 sections normatives :

1. **Section Acronymes & Vocabulaire Sémantique/Cyber** :
    
    - Liste explicite et structurée des acronymes W3C/OWL (`RDF`, `RDFS`, `OWL`, `SKOS`, `TTL`, `SPARQL`, `TBox`, `ABox`) et Cyber (`CPE`, `CVE`, `CWE`).
        
2. **Section Représentations Graphiques Multi-Niveaux** :
    
    - **Vue Synthétique Globale (Niveau 0)** : Diagramme de classe Mermaid (`classDiagram`) de haut niveau montrant les macro-domaines.
        
    - **Vues Métier Segmentées (Niveau 1 - Zooms)** : Diagrammes Mermaid ciblant un domaine précis (ex: _Actifs SI_, _Threat Intelligence / CVE_).
        
3. **Dictionnaire des Classes & Lexique Métier** :
    
    - Tableau comprenant : `Concept`, `Libellé FR`, `Synonymes / Acronymes (skos:altLabel)`, `Description (rdfs:comment)`.
        
4. **Dictionnaire des Relations et Attributs** :
    
    - Tableau comprenant : `Propriété`, `Domaine (Origine)`, `Range (Cible)`, `Libellé FR`.


## 4. Matrice de Validation et Critères d'Acceptabilité (Testabilité)

Un outil de test automatisé (ex: `pytest` ou validateur CI/CD) vérifiera la conformité de la TBox selon la grille de contrôle suivante :

|**Code Test**|**Exigence**|**Condition de Réussite (Pass Criterion)**|
|---|---|---|
|`TEST-TBOX-01`|**EXG-SRC-01**|Le fichier `TBox_Cybersec.ttl` existe et est un graphe RDF/OWL valide (`g.parse()` sans erreur).|
|`TEST-TBOX-02`|**EXG-JSON-01**|Le fichier `TBox_Cybersec.json` est un JSON valide et contient la clé root `"classes"`.|
|`TEST-TBOX-03`|**EXG-MD-ACRO**|Le fichier `TBox_Cybersec.md` contient un tableau référençant explicitement les acronymes W3C (RDF, OWL, SKOS, TTL).|
|`TEST-TBOX-04`|**EXG-MD-DIAG**|Le fichier `TBox_Cybersec.md` contient au moins **deux blocs de code diagramme `mermaid`** (Niveau 0 et Niveau 1).|
|`TEST-TBOX-05`|**EXG-MD-SKOS**|Les annotations `skos:altLabel` présentes dans le `.ttl` sont correctement reportées dans la colonne "Synonymes / Acronymes" du `.md`.|



 