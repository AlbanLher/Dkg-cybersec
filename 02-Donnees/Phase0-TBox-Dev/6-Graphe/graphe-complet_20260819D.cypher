:begin
CREATE CONSTRAINT n10s_unique_uri FOR (node:Resource) REQUIRE (node.uri) IS UNIQUE;
CREATE CONSTRAINT unique_device_id FOR (node:Device) REQUIRE (node.id) IS UNIQUE;
CREATE CONSTRAINT unique_software_key FOR (node:Software) REQUIRE (node.key) IS UNIQUE;
CREATE CONSTRAINT UNIQUE_IMPORT_NAME FOR (node:`UNIQUE IMPORT LABEL`) REQUIRE (node.`UNIQUE IMPORT ID`) IS UNIQUE;
:commit
CALL db.awaitIndexes(300);
:begin
UNWIND [{key:"OpenSSL@1.0.2", properties:{name:"OpenSSL", version:"1.0.2"}}, {key:"Apache@2.4.57", properties:{name:"Apache", version:"2.4.57"}}] AS row
CREATE (n:Software{key: row.key}) SET n += row.properties;
UNWIND [{_id:19, properties:{cyber:"http://example.org/cyber-ontology#", foaf:"http://xmlns.com/foaf/0.1/"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:_NsPrefDef;
UNWIND [{uri:"https://cve.mitre.org/CVE-2023-1234", properties:{cyber__description:"Vulnérabilité critique dans OpenSSL 1.0.2 permettant une exécution de code à distance.", cyber__cvssScore:9.8, foaf__name:"CVE-2023-1234"}}] AS row
CREATE (n:Resource{uri: row.uri}) SET n += row.properties SET n:cyber__Vulnerability;
UNWIND [{id:"PC-Alban-POC", properties:{importedAt:datetime('2026-08-19T13:07:13.411Z'), ip:"192.168.1.100", type:"PC"}}, {id:"Router-POC", properties:{importedAt:datetime('2026-08-19T13:07:13.411Z'), ip:"192.168.1.1", type:"Router"}}] AS row
CREATE (n:Device{id: row.id}) SET n += row.properties;
UNWIND [{_id:18, properties:{_classLabel:"Class", _handleRDFTypes:0, _subClassOfRel:"SCO", _objectPropertyLabel:"Relationship", _handleMultival:0, _rangeRel:"RANGE", _domainRel:"DOMAIN", _keepLangTag:false, _keepCustomDataTypes:false, _classNamePropName:"name", _handleVocabUris:0, _applyNeo4jNaming:false, _relNamePropName:"name", _dataTypePropertyLabel:"Property", _subPropertyOfRel:"SPO"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:_GraphConfig;
:commit
:begin
UNWIND [{start: {id:"PC-Alban-POC"}, end: {key:"OpenSSL@1.0.2"}, properties:{}}, {start: {id:"PC-Alban-POC"}, end: {key:"Apache@2.4.57"}, properties:{}}, {start: {id:"Router-POC"}, end: {key:"Apache@2.4.57"}, properties:{}}] AS row
MATCH (start:Device{id: row.start.id})
MATCH (end:Software{key: row.end.key})
CREATE (start)-[r:HAS_SOFTWARE]->(end) SET r += row.properties;
UNWIND [{start: {key:"OpenSSL@1.0.2"}, end: {uri:"https://cve.mitre.org/CVE-2023-1234"}, properties:{linkedAt:datetime('2026-08-19T13:17:17.464Z')}}] AS row
MATCH (start:Software{key: row.start.key})
MATCH (end:Resource{uri: row.end.uri})
CREATE (start)-[r:HAS_VULNERABILITY]->(end) SET r += row.properties;
:commit
:begin
MATCH (n:`UNIQUE IMPORT LABEL`)  WITH n LIMIT 20000 REMOVE n:`UNIQUE IMPORT LABEL` REMOVE n.`UNIQUE IMPORT ID`;
:commit
:begin
DROP CONSTRAINT UNIQUE_IMPORT_NAME;
:commit
