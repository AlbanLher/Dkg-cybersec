
# Généralités
## Netoyage du graph : effacer les artefact n10s  aprés import

### 1-  Supprimez les nœuds internes de n10s
```cypher
MATCH (n:`UNIQUE IMPORT LABEL`)
DETACH DELETE n;

MATCH (n:Resource)
WHERE n.uri STARTS WITH "http://www.w3.org/" OR
      n.uri STARTS WITH "http://xmlns.com/" OR
      n.uri STARTS WITH "_"
DETACH DELETE n;
```
### 1.2 - Supprimez les propriétés internes (préfixées par `_`)
```cypher
MATCH (n)
WHERE ANY(prop IN keys(n) WHERE prop STARTS WITH "_")
SET n = {uri: n.uri, label: n.rdfs__label, comment: n.rdfs__comment}
```
### 1.3 - Supprimez les doublons (ex: PC-Alban-POC)
```cypher
MATCH (n:Device)
WITH n.id AS deviceId, collect(n) AS nodes
WHERE size(nodes) > 1
CALL apoc.refactor.mergeNodes(nodes)
YIELD node
RETURN node;
```

## Nettoyage v2


### 2.1 - Supprimez TOUTES les contraintes n10s

```cypher
CALL apoc.schema.assert(
 {Device: ['id']}, // Contraintes  UNIQUE
 {}, // Pas d'index supplémentaire 
 true // ⭐ true = Ignore les conflits
);`
```
REX conflit avec contraine n10s
```
CALL apoc.schema.assert(
  {Device: ['id']},
  {Device: ['id']},
  false
);
```

### 2.2 - Supprimez les nœuds Resource inutiles (URIs standard)
```cypher
MATCH (n:Resource)
WHERE n.uri STARTS WITH "http://www.w3.org/" OR
      n.uri STARTS WITH "http://xmlns.com/" OR
      n.uri CONTAINS "_NsPrefDef" OR
      n.uri CONTAINS "_GraphConfig"
DETACH DELETE n;
```
### 2.3 - Nettoyez les propriétés préfixées (rdfs__, ns0__, ns1__)


```cypher
MATCH (n)

WHERE ANY(prop IN keys(n) WHERE prop STARTS WITH "rdfs__" OR prop STARTS WITH "ns0__" OR prop STARTS WITH "ns1__")

WITH n, [p IN keys(n) WHERE p STARTS WITH "rdfs__" OR p STARTS WITH "ns0__" OR p STARTS WITH "ns1__"] AS propsToRemove

FOREACH (prop IN propsToRemove |

REMOVE n[prop]

)

RETURN count(n) AS properties_removed;
```
REX KO
```
MATCH (n)
WHERE ANY(prop IN keys(n) WHERE prop STARTS WITH "rdfs__" OR prop STARTS WITH "ns0__" OR prop STARTS WITH "ns1__")
SET n += {
  label: n.rdfs__label,
  description: COALESCE(n.ns0__description, n.rdfs__comment),
  name: n.ns1__name
}
WITH n
CALL apoc.any.property.remove(n, [p IN keys(n) WHERE p STARTS WITH "rdfs__" OR p STARTS WITH "ns0__" OR p STARTS WITH "ns1__"])
YIELD n
RETURN count(n) AS properties_removed;
```



### 2.4 - Supprimez les labels inutiles (owl__Class, owl__ObjectProperty)
```cypher
MATCH (n)
WHERE ANY(label IN labels(n) WHERE label STARTS WITH "owl__" OR label = "Resource")
SET n :Class
REMOVE n:`owl__Class`:Resource;
```
### 2.5 - Renommez les relations préfixées (rdfs__domain, rdfs__range)
```cypher
// 1. Collectez tous les types de relations à renommer
MATCH ()-[r]->()
WHERE type(r) STARTS WITH "rdfs__" OR type(r) STARTS WITH "ns0__" OR type(r) STARTS WITH "ns1__"
WITH collect(DISTINCT type(r)) AS typesToRename

// 2. Renommez chaque type un par un
UNWIND typesToRename AS oldType
CALL apoc.refactor.rename.type(
  oldType,
  CASE
    WHEN oldType STARTS WITH 'rdfs__' THEN replace(oldType, 'rdfs__', '')
    WHEN oldType STARTS WITH 'ns0__' THEN replace(oldType, 'ns0__', '')
    WHEN oldType STARTS WITH 'ns1__' THEN replace(oldType, 'ns1__', '')
  END
)
YIELD batch, operations
RETURN oldType AS old_type, batch, operations;

```
REX
```
MATCH ()-[r]->()
WHERE type(r) STARTS WITH "rdfs__" OR type(r) STARTS WITH "ns0__"
CALL apoc.refactor.rename.type(type(r), apoc.text.regexReplace(type(r), 'rdfs__|ns0__|ns1__', ''))
YIELD oldType, newType
RETURN oldType, newType;
```
### 2. 6 - Supprimez les nœuds isolés (optionnel)
```cypher
MATCH (n)
WHERE NOT (n)-[]-()
DETACH DELETE n;
```