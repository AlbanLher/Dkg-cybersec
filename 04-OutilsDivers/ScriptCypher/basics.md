
## Supprimez d'abord les données de test (si nécessaire)
```cypher
MATCH (n) DETACH DELETE n
```
## lister et retirer des contraintes ou index
```cypher
SHOW INDEXES;
SHOW CONSTRAINTS;
DROP INDEX index_name;
DROP CONSTRAINT constraint_name;
```



```cypher
CALL apoc.cypher.runMany(" 
	SHOW INDEXES YIELD name 
	WHERE name IS NOT NULL 
	CALL apoc.index.remove(name) YIELD value 
	RETURN count(*) AS indexesRemoved ");
```


## apoc
```cypher
CALL apoc.help("version") YIELD name, signature
RETURN apoc.version() AS version;
```


```cypher
CALL apoc.load.json("file:///import/data/public/inventory.json") YIELD value
CREATE (v:Vulnerability {id: value.id, cvss: value.cvss})
```

```cypher
// Chargez l'inventaire
CALL apoc.load.json("file:///var/lib/neo4j/import/public/inventory.json") YIELD value
UNWIND value.devices AS device
CREATE (d:Device {
id: device.id,
type: device.type,
ip: device.ip
})

FOREACH (sw IN device.software |
MERGE (s:Software {name: sw.name, version: sw.version})
CREATE (d)-[:HAS_SOFTWARE]->(s)
)
RETURN count(d) AS devices_created
```




## n10s

Initiaisation
```cypher
CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE

// 1. Créer la contrainte requise par n10s sur le nœud Resource
CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS
FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

// 2. Initialiser la configuration n10s par défaut
CALL n10s.graphconfig.init();
```


```cypher
`-- Chargez l'ontologie (depuis /var/lib/neo4j/ontologies/) 
CALL n10s.rdf.import.file('file:///ontologies/ontologie.ttl', 'Turtle') 
-- Chargez les CVE (depuis /var/lib/neo4j/import/public/) 
CALL n10s.rdf.import.file('file:///public/cve_data.ttl', 'Turtle')`
```



```cypher
CALL n10s.rdf.import.fetch(
"file:///var/lib/neo4j/import/public/cve_data.ttl",
"Turtle"
);
```


## Exportez le graphe en Cypher :
```cypher
# Dans Neo4j Browser, exécutez :
CALL apoc.export.cypher.all("graphe-complet.cypher", {format: 'cypher-shell'})
```
   
   _(Le fichier sera généré dans `/var/lib/neo4j/import/graphe-complet.cypher`.)_