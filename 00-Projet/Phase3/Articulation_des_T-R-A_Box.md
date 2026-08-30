```
je comprends la generation de RBox#.ttl a partir de données json
Mais je voudrais meix comprendre comment on l'articule avec e TBox et ABox générées précédemment !
C'est une excellente question, car c'est **précisément là que réside toute la puissance des Knowledge Graphs (Web Sémantique / Linked Data)**.
```

L'articulation entre la **TBox** (Schéma), l'**ABox** (Instances Privées) et la **RBox** (Enrichissement Externe) ne se fait pas en fusionnant manuellement les fichiers, mais par **maillage d'URIs (Identifiants Sémantiques Uniques)** et par **import OWL (`owl:imports`)**.

Voici l'explication mécanique pas à pas.

### 1. La Clé de Voûte : Le Triple Triplet RDF (Sujet → Prédicat → Objet)

Chaque sous-graphe apporte sa part de la vérité au sein d'une **même architecture d'URIs** :

|Étape / Graphe|Fichier RDF Source|Triple RDF Généré|Explication Sémantique|
|---|---|---|---|
|**Phase 1 (TBox)**|`TLP-AMBER_TBox_Cybersec/TBox_Cybersec.ttl`|`dkg:Vulnerability a owl:Class .``dkg:classifiedUnder a owl:ObjectProperty .`|**Le Vocabulaire** : On définit ce qu'est une Vulnérabilité et ce que veut dire "classé sous".|
|**Phase 2 (ABox)**|`TLP-RED_ABox_Cybersec/ABox_Cybersec.ttl`|`abox:sw-nginx-1201 dkg:hasVulnerability rbox:CVE-2021-23017 .`|**L'Inventaire Privé** : Mon serveur web privé possède la vulnérabilité référencée sous la clé `rbox:CVE-2021-23017`.|
|**Phase 3 (RBox)**|`TLP-CLEAR_RBox_NVD-CWE/RBox_Cybersec.ttl`|`rbox:CVE-2021-23017 dkg:cvssScore 7.5 .``rbox:CVE-2021-23017 dkg:classifiedUnder rbox:CWE-193 .`|**L'Enrichissement Public** : La faille `CVE-2021-23017` a un score de 7.5 et correspond à l'erreur `CWE-193`.|

### 2. Le Mécanisme de Liaison Mémoire (Pointeur d'URI)

Remarquez la magie qui s'opère :

1. L'**ABox Privée (TLP-RED)** cite l'URI `[http://dkg.cybersec.org/rbox#CVE-2021-23017](http://dkg.cybersec.org/rbox#CVE-2021-23017)` **sans savoir ce qu'elle contient dans le détail**. Elle se contente de dire : _"Mon composant NGINX est affecté par cette CVE"_.
    
2. La **RBox Publique (TLP-CLEAR)** définit l'URI `[http://dkg.cybersec.org/rbox#CVE-2021-23017](http://dkg.cybersec.org/rbox#CVE-2021-23017)` **sans savoir sur quel serveur du SI elle est installée**. Elle se contente de donner la fiche technique publique de la CVE.
    
3. **Au moment de la requête SPARQL ou du chargement dans Python (`rdflib`)**, lorsqu'on charge la TBox + l'ABox + la RBox ensemble dans la mémoire du graphe :
    
    Les nœuds rbox:CVE-2021-23017 des deux fichiers se superposent exactement.
    

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