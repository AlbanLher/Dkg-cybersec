### 2. Cadrage de la Phase 3 : Enrichissement Externe (RBox / Linking NVD & CWE)

Après avoir défini le schéma (**TBox - Phase 1**) et instancié les équipements privés (**ABox - Phase 2**), 
Les objectifs de la **Phase 3** sont 

1. **Enrichissement Externe (RBox)** : Lier automatiquement les vulnérabilités de l'ABox aux référentiels publics de failles (NVD / CVE) et faiblesses logicielles (MITRE CWE) avec leurs métadonnées universelles (scores CVSS, descriptions).
    
2. **Gouvernance de Confidentialité (TLP)** : Structurer l'arborescence de données `12-Donnees/` par **niveaux de sensibilité TLP (Traffic Light Protocol)** afin de protéger le jargon métier, la topologie privée et les données d'inventaire, sans impacter les artefacts gelés des Phases 1 & 2 (`TBox_init`, `ABox_init`).



## 2. Périmètre Opérationnel (IN / OUT)

|**Domaine**|**IN (Inclus dans la Phase 3)**|**OUT (Exclu / Phasing Utérieur)**|
|---|---|---|
|**Sources Externes**|Feed mock local au format JSON (`nvd_cwe_mock.json`) simulant les données NVD et MITRE CWE.|Requêtes temps réel/en direct vers les API distantes NVD/MITRE (évite verrous API et dépendance réseau).|
|**Confidentialité & Sécurité**|Application de la convention de nommage `[TLP-CODE]_[Type_Graph]_[Domaine]` pour les nouveaux dossiers sous `12-Donnees/`.|Gestion d'habilitation dynamique / ACL dans un moteur SPARQL distant (GraphDB/Fuseki).|
|**Liaisons Ontologiques**|Création des relations `dkg:Vulnerability` $\rightarrow$ `dkg:classifiedUnder` $\rightarrow$ `dkg:Weakness`.|Alignement d'ontologies complexes (`owl:sameAs` dynamique).|
|**Documentation & Rendu**|Génération du graphe RDF Turtle et de la vue Markdown / Mermaid montrant la chaîne complète d'enrichissement.|Calculs complexes de score de risque global du SI (reportés en Phase 4).|

## 3. Règle de Nommage et Séparation de Confidentialité

### Convention de Nommage des Répertoires

$$\text{[TLP-CODE]}\text{\_}\text{[Type\_Graph]}\text{\_}\text{[Domaine]}$$

### Matrice de Protection

```
12-Donnees/
├── TBox_init/                          [ ❄️ GÉLÉ - Phase 1 ]
├── ABox_init/                          [ ❄️ GÉLÉ - Phase 2 ]
│
├── TLP-AMBER_TBox_Cybersec/            [ 🟡 CONFIDENTIEL INTERNE ]
│   └── TBox_Cybersec.ttl               - Lexique métier, classes custom, règles SI
│
├── TLP-RED_ABox_Cybersec/              [ 🔴 STRICTEMENT RESTREINT ]
│   ├── inventory.json                  - Adresses IP, hôtes, comptes, inventaire brut
│   └── ABox_Cybersec.ttl               - Graphe d'instances réelles du SI
│
└── TLP-CLEAR_RBox_NVD-CWE/             [ 🟢 OPEN DATA / PUBLIC ]
    ├── nvd_cwe_mock.json               - Mock d'enrichissement CVE / CWE
    ├── RBox_Cybersec.ttl               - Graphe RDF d'enrichissement externe
    └── RBox_Cybersec.md                - Topologie visuelle Mermaid de la RBox
```

## 4. Matrice des Exigences et Règles Normatives (Phase 3)

### Règles de Confidentialité et Sécurité (SEC)

- **RULE-SEC-01 (Isolation par dossier TLP)** : Toute nouvelle donnée générée ou consommée doit impérativement résider dans un dossier préfixé par son niveau TLP (`TLP-AMBER`, `TLP-RED`, `TLP-CLEAR`).
    
- **RULE-SEC-02 (Politique d'Ignore Git)** : Les fichiers contenant des topologies ou identifiants réels sous `**/TLP-RED_*/*.json` doivent pouvoir être ignorés par le versionnage sans impacter le reste du dépôt.
    
- **RULE-SEC-03 (Protection de la TBox)** : Le dictionnaire sémantique et les descriptions métier de la TBox sont classés **TLP-AMBER** pour ne pas révéler la maturité ni les règles de sécurité internes du SI à des tiers.
    

### Règles d'Enrichissement RBox (RBOX)

- **RULE-RBOX-01 (Linking NVD/CWE)** : Chaque vulnérabilité issue du mock NVD doit être associée à un score CVSS (`dkg:cvssScore`) et rattachée à au moins une catégorie CWE (`dkg:classifiedUnder`).
    
- **RULE-RBOX-02 (Non-pollution de l'ABox)** : Les descriptions publiques des CVE et la taxonomie universelle des CWE doivent être écrites exclusivement dans l'espace `TLP-CLEAR_RBox_NVD-CWE/`.
    

## 5. Livrables à Produire en Phase 3

1. **Spécification :** `11-Principes_Architecture/Specifications/SpecificationNormativeEnrichissementRBox.md`
    
2. **Données Mock Externes :** `12-Donnees/TLP-CLEAR_RBox_NVD-CWE/nvd_cwe_mock.json`
    
3. **Scripts Python (`13-Application/`) :**
    
    - `enrich_vulnerabilities_rbox.py` (Transformation JSON Mock $\rightarrow$ RDF Turtle TLP-CLEAR)
        
    - `generate_RBox_initiale.py` (Génération de la vue Markdown / Mermaid)
        
    - `test_RBox_spec.py` (Suite de tests `pytest` sur la conformité RBox et TLP)


### 3. Matrice de Mapping d'Enrichissement Cible

```
[ Asset Privé ] ──(hasInstalledComponent)──> [ SoftwareComponent ]
                                                    │
                                          (hasVulnerability)
                                                    ▼
                                          [ Vulnerability (CVE) ] ◄── (Phase 3: Enrichissement NVD)
                                                    │               - Score CVSS
                                            (classifiedUnder)       - Description publique
                                                    ▼
                                          [ Weakness (CWE) ]     ◄── (Phase 3: Taxonomie Mitre)
                                                                    - Categorie CWE (ex: CWE-79)
```


### 5.  Bilan des Actions et Livrables

| Action                    | livrable | Localisation | Commentaire |                       |
| ------------------------- | -------- | ------------ | ----------- | --------------------- |
| Création arborescence TLP | /2-/TLP# | /2-          |             | 🟢 Terminée / Validée |
|                           |          |              |             | 🟢 Terminée / Validée |
|                           |          |              |             | 🟢 Terminée / Validée |
|                           |          |              |             | 🟢 Terminée / Validée |
|                           |          |              |             | 🟢 Terminée / Validée |


###  6.  Articulation TBox ABox RBox 


C'est **précisément dans cette articulation que réside toute la puissance des Knowledge Graphs (Web Sémantique / Linked Data)**.

L'articulation entre la **TBox** (Schéma), l'**ABox** (Instances Privées) et la **RBox** (Enrichissement Externe) ne se fait pas en fusionnant manuellement les fichiers, mais par **maillage d'URIs (Identifiants Sémantiques Uniques)** et par **import OWL (`owl:imports`)**.

Voici l'explication mécanique pas à pas.

### 1. La Clé de Voûte : Le Triple Triplet RDF (Sujet $\rightarrow$ Prédicat $\rightarrow$ Objet)

Chaque sous-graphe apporte sa part de la vérité au sein d'une **même architecture d'URIs** :

| **Étape / Graphe** | **Fichier RDF Source**                      | **Triple RDF Généré**                                                                             | **Explication Sémantique**                                                                                            |
| ------------------ | ------------------------------------------- | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Phase 1 (TBox)** | `TLP-AMBER_TBox_Cybersec/TBox_Cybersec.ttl` | `dkg:Vulnerability a owl:Class .``dkg:classifiedUnder a owl:ObjectProperty .`                     | **Le Vocabulaire** : On définit ce qu'est une Vulnérabilité et ce que veut dire "classé sous".                        |
| **Phase 2 (ABox)** | `TLP-RED_ABox_Cybersec/ABox_Cybersec.ttl`   | `abox:sw-nginx-1201 dkg:hasVulnerability rbox:CVE-2021-23017 .`                                   | **L'Inventaire Privé** : Mon serveur web privé possède la vulnérabilité référencée sous la clé `rbox:CVE-2021-23017`. |
| **Phase 3 (RBox)** | `TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.ttl`  | `rbox:CVE-2021-23017 dkg:cvssScore 7.5 .``rbox:CVE-2021-23017 dkg:classifiedUnder rbox:CWE-193 .` | **L'Enrichissement Public** : La faille `CVE-2021-23017` a un score de 7.5 et correspond à l'erreur `CWE-193`.        |

### 2. Le Mécanisme de Liaison Mémoire (Pointeur d'URI)

Remarquez la magie qui s'opère :

1. L'**ABox Privée (TLP-RED)** cite l'URI `[http://dkg.cybersec.org/rbox#CVE-2021-23017](http://dkg.cybersec.org/rbox#CVE-2021-23017)` **sans savoir ce qu'elle contient dans le détail**. Elle se contente de dire : _"Mon composant NGINX est affecté par cette CVE"_.
    
2. La **RBox Publique (TLP-CLEAR)** définit l'URI `[http://dkg.cybersec.org/rbox#CVE-2021-23017](http://dkg.cybersec.org/rbox#CVE-2021-23017)` **sans savoir sur quel serveur du SI elle est installée**. Elle se contente de donner la fiche technique publique de la CVE.
    
3. **Au moment de la requête SPARQL ou du chargement dans Python (`rdflib`)**, lorsqu'on charge la TBox + l'ABox + la RBox ensemble dans la mémoire du graphe :
    
    $$\text{Les nœuds } \texttt{rbox:CVE-2021-23017} \text{ des deux fichiers se superposent exactement.}$$
    

Extrait de code

```
graph LR
    subgraph ABox ["🔒 02_ABox (TLP-RED)"]
        ASSET["🖥️ abox:srv-web-01"] -->|hasInstalledComponent| SW["📦 abox:sw-nginx-1201"]
        SW -->|hasVulnerability| CVE["⚠️ rbox:CVE-2021-23017"]
    end

    subgraph RBox ["🌐 03_RBox (TLP-CLEAR)"]
        CVE -->|cvssScore| SCORE["7.5"]
        CVE -->|classifiedUnder| CWE["🛡️ rbox:CWE-193"]
        CWE -->|rdfs:label| LBL["Off-by-one Error"]
    end

    subgraph TBox ["🟡 01_TBox (TLP-AMBER)"]
        VOCAB["Modèle de données & Règles sémantiques"]
    end

    style ABox fill:#ffebe9,stroke:#d62728;
    style RBox fill:#e6f5d0,stroke:#2ca02c;
    style TBox fill:#fff3cd,stroke:#ffc107;
```

### 3. Comment les Scripts Python Rapprochent les Graphes (Exemple Concret)

Lorsque nous voulons poser une question globale (ex: _"Quels sont mes serveurs impactés par une faille de type Off-by-one de score > 7 ?"_), le script Python charge simplement les 3 fichiers TTL dans **un seul objet `Graph`** :

Python

```
from rdflib import Graph

# 1. On instancie un graphe global en mémoire
kg_global = Graph()

# 2. On importe les 3 piliers (TBox + ABox + RBox)
kg_global.parse("12-Donnees/TLP-AMBER_TBox_Cybersec/TBox_Cybersec.ttl", format="turtle")
kg_global.parse("12-Donnees/TLP-RED_ABox_Cybersec/ABox_Cybersec.ttl", format="turtle")
kg_global.parse("12-Donnees/TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.ttl", format="turtle")

# 3. La traversée de graphe franchit naturellement les frontières ABox <-> RBox !
query = """
SELECT ?assetLabel ?cveId ?cvss ?cweLabel WHERE {
    ?asset dkg:hasInstalledComponent ?sw .
    ?asset rdfs:label ?assetLabel .
    ?sw dkg:hasVulnerability ?cve .
    
    ?cve dkg:cvssScore ?cvss .
    ?cve dkg:classifiedUnder ?cwe .
    ?cwe rdfs:label ?cweLabel .
    
    FILTER(?cvss >= 7.0)
}
"""

for row in kg_global.query(query):
    print(f"ALERTE : {row.assetLabel} est vulnérable à {row.cve} (Score: {row.cvss}, Type: {row.cweLabel})")
```

### Pourquoi cette Architecture est Géniale pour la Cybersécurité ?

1. **Étanchéité des données** : Vous pouvez partager votre fichier `RBox_Cybersec.ttl` ou `TBox_Cybersec.ttl` à des partenaires externes ou à des chercheurs en sécurité sans **JAMAIS** exposer `ABox_Cybersec.ttl` (qui contient vos vrais serveurs et adresses IP).
    
2. **Mise à jour sans douleur** : Si la NVD met à jour le score CVSS d'une CVE, vous réexécutez seulement `enrich_vulnerabilities_rbox.py`. Votre ABox privée reste totalement intacte.