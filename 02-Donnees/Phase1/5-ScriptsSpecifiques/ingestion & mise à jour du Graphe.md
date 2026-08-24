```cypher
// ====================================================================
// 1. DÉCLARATION DES NAMESPACES & CHARGEMENT DE L'ONTOLOGIE V1
// ====================================================================
CALL n10s.nsprefixes.add("cyber", "http://example.org/cyber-ontology#");
CALL n10s.nsprefixes.add("foaf", "http://xmlns.com/foaf/0.1/");

// Chargement de l'ontologie V1 modifiée dans le moteur n10s
CALL n10s.onto.import.fetch("file:///var/lib/neo4j/import/pseudo-private/ontologie_v1.ttl", "Turtle");

// ====================================================================
// 2. INGESTION DU RÉFÉRENTIEL DE VULNÉRABILITÉS (cve_data-v2.ttl)
// ====================================================================
CALL n10s.rdf.import.fetch("file:///var/lib/neo4j/import/public/cve_data-v2.ttl", "Turtle");

// Post-traitement : Alignement des propriétés 'foaf__name' et 'description'
MATCH (v:cyber__Vulnerability)
WHERE v.foaf__name IS NOT NULL AND v.name IS NULL
SET v.name = v.foaf__name;

MATCH (v:cyber__Vulnerability)
WHERE v.cyber__description IS NOT NULL AND v.description IS NULL
SET v.description = v.cyber__description;

// ====================================================================
// 3. INGESTION DE L'INVENTAIRE ÉTENDU (inventory-v2.json)
// ====================================================================
CALL apoc.load.json("file:///var/lib/neo4j/import/public/inventory-v2.json") YIELD value
UNWIND value.devices AS devData
WITH devData WHERE devData.id IS NOT NULL

// Création / Mise à jour des Devices (avec gestion de la nouvelle propriété 'internal')
MERGE (d:Device {id: devData.id})
ON CREATE SET 
    d.ip = devData.ip,
    d.type = devData.type,
    d.internal = coalesce(devData.internal, true),
    d.importedAt = datetime()
ON MATCH SET
    d.ip = devData.ip,
    d.internal = coalesce(devData.internal, d.internal),
    d.updatedAt = datetime()

// Gestion des composants Software
WITH d, coalesce(devData.software, []) AS softwares
UNWIND (CASE WHEN size(softwares) = 0 THEN [null] ELSE softwares END) AS soft

WITH d, soft, (soft.name + "@" + soft.version) AS softKey
WHERE soft IS NOT NULL

MERGE (s:Software {key: softKey})
ON CREATE SET 
    s.name = soft.name,
    s.version = soft.version

MERGE (d)-[:HAS_SOFTWARE]->(s);

// ====================================================================
// 4. RAPPROCHEMENT INTELLIGENT (Software <-> Vulnerability)
// ====================================================================
MATCH (s:Software)
MATCH (v:cyber__Vulnerability)
WHERE (v.name IS NOT NULL AND v.name CONTAINS s.name)
   OR (v.foaf__name IS NOT NULL AND v.foaf__name CONTAINS s.name)
   OR (v.uri IS NOT NULL AND v.uri CONTAINS s.name)
   OR (v.description IS NOT NULL AND toLower(v.description) CONTAINS toLower(s.name))
MERGE (s)-[r:HAS_VULNERABILITY]->(v)
ON CREATE SET r.linkedAt = datetime();

// ====================================================================
// 5. RAPPORT D'EXÉCUTION
// ====================================================================
RETURN 
    count(DISTINCT d) AS TotalDevices,
    count(DISTINCT s) AS TotalSoftwares,
    count(DISTINCT v) AS TotalVulnerabilities;
```
