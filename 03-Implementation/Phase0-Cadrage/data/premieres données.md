---
jupyter:
  jupytext:
    cell_metadata_filter: -all
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.5
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

### Charger les dernières CVE

```python
(mlops_314_claude) lhermine@a515-f:/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase0-Cadrage$ 
python scripts/load_cve_feed.py > data/cve_data.ttl
```


### Générer un inventaire fictif
```python
(mlops_314_claude) lhermine@a515-f:/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase0-Cadrage$ python scripts/generate_inventory.py  > data/inventory.json
```




### Valider l’ontologie

`# Avec RDFLib (à installer : pip install rdflib) 

```python
from rdflib import Graph
from rdflib.namespace import RDF, OWL
g = Graph() 
g.parse('/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase0-Cadrage/data/cve_data.ttl', format='turtle') 
print('Ontologie valide ! Classes :', [str(s) for s in g.subjects(RDF.type, OWL.Class)])
```


## Chargement de CVE dans Neo4j
### Approche manuelle
```cypher
CALL apoc.load.json("file:///import/inventory.json") YIELD value
CREATE (v:Vulnerability {id: value.id, cvss: value.cvss})
```

```
Created 1 node, added 1 label
```



### Methode 1. Generation de requete Cypher par scrip python a partir du ttl
```bash
(mlops_314_claude) lhermine@a515-f:/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase0-Cadrage$ scripts/ttl_to_cypher.py data/cve_data.ttl > cve_import.cypher
```

### Methode 2 : utilisation deneurosemantic n10s
#### 2.1 - Lancement de Podman avec n10s
```bash
podman run -d \
  --name neo4j \
  --userns=keep-id \
  -p 7474:7474 -p 7687:7687 \
  -v /data/neo4j/data:/data:Z \
  -v /data/neo4j/import:/var/lib/neo4j/import:Z \
  -v /data/neo4j/conf:/var/lib/neo4j/conf:Z \
  -e NEO4J_PLUGINS='["apoc", "n10s"]' \
  -e NEO4J_AUTH=neo4j/Acad26DKG! \
  neo4j:2026.7.1
  
```

**`neo4j.conf`**
```
dbms.security.procedures.unrestricted=apoc.*,n10s.*
```

#### 2.2 -  Initialisation du Graph Configuration (Obligatoire)
Avant le tout premier import RDF, vous devez définir la contrainte d'unicité sur les URI et initialiser la configuration graph de `n10s`.

Exécutez ces requêtes Cypher dans **Neo4j Browser** ou votre driver :

```cypher
// 1. Créer la contrainte requise par n10s sur le nœud Resource
CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS
FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

// 2. Initialiser la configuration n10s par défaut
CALL n10s.graphconfig.init();
```

> **Options d'initialisation courantes :** Si vous souhaitez conserver les préfixes d'origine ou la gestion des types : `CALL n10s.graphconfig.init({ handleVocabUris: "IGNORE" });` (ignore les préfixes d'URI longs pour garder des labels simples comme `:Vulnerability`).


#### 2.3. Importer le fichier Turtle (`.ttl`)

Placez votre fichier `cve_data.ttl` dans le dossier monté `/data/neo4j/import/`.

##### Import depuis un fichier local (`file:///`)

```cypher
CALL n10s.rdf.import.fetch(
  "file:///import/cve_data.ttl",
  "Turtle"
);
```

##### Prévisualisation avant import (sans écrire en base)

```cypher
CALL n10s.rdf.preview.fetch(
  "file:///import/cve_data.ttl",
  "Turtle"
);
```
#### 2.4. Mapper les préfixes RDF vers des Labels Cypher personnalisés

Si vous souhaitez associer une classe RDF spécifique (ex: `[http://example.org/cyber-ontology#Vulnerability](http://example.org/cyber-ontology#Vulnerability)`) à un label Cypher court (ex: `Vulnerability`), configurez un mapping :

```cypher
// Ajouter un mapping de namespace
CALL n10s.nsprefixes.add("cyber", "http://example.org/cyber-ontology#");

// Mapper la classe RDF vers un label Cypher
CALL n10s.mapping.addSchema("http://example.org/cyber-ontology#Vulnerability", "Vulnerability");
```
