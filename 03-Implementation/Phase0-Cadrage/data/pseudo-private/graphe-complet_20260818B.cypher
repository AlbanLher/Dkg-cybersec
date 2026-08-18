:begin
CREATE CONSTRAINT n10s_unique_uri FOR (node:Resource) REQUIRE (node.uri) IS UNIQUE;
CREATE CONSTRAINT UNIQUE_IMPORT_NAME FOR (node:`UNIQUE IMPORT LABEL`) REQUIRE (node.`UNIQUE IMPORT ID`) IS UNIQUE;
:commit
CALL db.awaitIndexes(300);
:begin
UNWIND [{uri:"http://example.org/cyber-ontology#Software", properties:{rdfs__label:"Logiciel"}}, {uri:"http://example.org/cyber-ontology#Action", properties:{rdfs__label:"Action corrective"}}, {uri:"http://example.org/cyber-ontology#Device", properties:{rdfs__comment:"Un device physique ou virtuel (PC, routeur, serveur).", rdfs__label:"Appareil"}}, {uri:"http://example.org/cyber-ontology#Threat", properties:{rdfs__label:"Menace"}}, {uri:"http://example.org/cyber-ontology#Vulnerability", properties:{rdfs__label:"Vulnérabilité"}}, {uri:"http://example.org/cyber-ontology#Rule", properties:{rdfs__label:"Règle de sécurité"}}] AS row
CREATE (n:Resource{uri: row.uri}) SET n += row.properties SET n:owl__Class;
UNWIND [{uri:"http://www.w3.org/2001/XMLSchema#float", properties:{}}] AS row
CREATE (n:Resource{uri: row.uri}) SET n += row.properties;
UNWIND [{_id:14, properties:{ip:"192.168.1.100", id:"PC-Alban-POC", type:"PC"}}, {_id:17, properties:{ip:"192.168.1.1", id:"Router-POC", type:"Router"}}, {_id:18, properties:{ip:"192.168.1.100", id:"PC-Alban-POC", type:"PC"}}, {_id:19, properties:{ip:"192.168.1.1", id:"Router-POC", type:"Router"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:Device;
UNWIND [{_id:0, properties:{owl:"http://www.w3.org/2002/07/owl#", rdfs:"http://www.w3.org/2000/01/rdf-schema#", ns0:"http://example.org/cyber-ontology#", ns1:"http://xmlns.com/foaf/0.1/"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:_NsPrefDef;
UNWIND [{uri:"http://example.org/cyber-ontology#requiresAction", properties:{rdfs__label:"nécessite l'action"}}, {uri:"http://example.org/cyber-ontology#hasVulnerability", properties:{rdfs__label:"a pour vulnérabilité"}}, {uri:"http://example.org/cyber-ontology#hasSoftware", properties:{rdfs__label:"a pour logiciel"}}] AS row
CREATE (n:Resource{uri: row.uri}) SET n += row.properties SET n:owl__ObjectProperty;
UNWIND [{_id:15, properties:{name:"OpenSSL", version:"1.0.2"}}, {_id:16, properties:{name:"Apache", version:"2.4.57"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:Software;
UNWIND [{uri:"https://cve.mitre.org/CVE-2023-1234", properties:{ns0__description:"Vulnérabilité critique dans OpenSSL 1.0.2 permettant une exécution de code à distance.", ns0__cvssScore:9.8, ns1__name:"CVE-2023-1234"}}] AS row
CREATE (n:Resource{uri: row.uri}) SET n += row.properties SET n:ns0__Vulnerability;
UNWIND [{uri:"http://example.org/cyber-ontology#cvssScore", properties:{rdfs__label:"score CVSS"}}] AS row
CREATE (n:Resource{uri: row.uri}) SET n += row.properties SET n:owl__DatatypeProperty;
UNWIND [{_id:12, properties:{_classLabel:"Class", _handleRDFTypes:0, _subClassOfRel:"SCO", _handleMultival:0, _objectPropertyLabel:"Relationship", _rangeRel:"RANGE", _domainRel:"DOMAIN", _keepLangTag:false, _keepCustomDataTypes:false, _classNamePropName:"name", _handleVocabUris:0, _applyNeo4jNaming:false, _relNamePropName:"name", _dataTypePropertyLabel:"Property", _subPropertyOfRel:"SPO"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:_GraphConfig;
:commit
:begin
UNWIND [{start: {uri:"http://example.org/cyber-ontology#cvssScore"}, end: {uri:"http://example.org/cyber-ontology#Vulnerability"}, properties:{}}] AS row
MATCH (start:Resource{uri: row.start.uri})
MATCH (end:Resource{uri: row.end.uri})
CREATE (start)-[r:rdfs__domain]->(end) SET r += row.properties;
UNWIND [{start: {_id:14}, end: {_id:15}, properties:{}}, {start: {_id:14}, end: {_id:16}, properties:{}}, {start: {_id:17}, end: {_id:16}, properties:{}}, {start: {_id:18}, end: {_id:15}, properties:{}}, {start: {_id:18}, end: {_id:16}, properties:{}}, {start: {_id:19}, end: {_id:16}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:HAS_SOFTWARE]->(end) SET r += row.properties;
UNWIND [{start: {uri:"http://example.org/cyber-ontology#Vulnerability"}, end: {uri:"http://example.org/cyber-ontology#Threat"}, properties:{}}] AS row
MATCH (start:Resource{uri: row.start.uri})
MATCH (end:Resource{uri: row.end.uri})
CREATE (start)-[r:rdfs__subClassOf]->(end) SET r += row.properties;
UNWIND [{start: {uri:"http://example.org/cyber-ontology#hasSoftware"}, end: {uri:"http://example.org/cyber-ontology#Software"}, properties:{}}, {start: {uri:"http://example.org/cyber-ontology#hasVulnerability"}, end: {uri:"http://example.org/cyber-ontology#Vulnerability"}, properties:{}}, {start: {uri:"http://example.org/cyber-ontology#requiresAction"}, end: {uri:"http://example.org/cyber-ontology#Action"}, properties:{}}] AS row
MATCH (start:Resource{uri: row.start.uri})
MATCH (end:Resource{uri: row.end.uri})
CREATE (start)-[r:rdfs__range]->(end) SET r += row.properties;
UNWIND [{start: {uri:"http://example.org/cyber-ontology#cvssScore"}, end: {uri:"http://www.w3.org/2001/XMLSchema#float"}, properties:{}}] AS row
MATCH (start:Resource{uri: row.start.uri})
MATCH (end:Resource{uri: row.end.uri})
CREATE (start)-[r:rdfs__range]->(end) SET r += row.properties;
UNWIND [{start: {uri:"http://example.org/cyber-ontology#requiresAction"}, end: {uri:"http://example.org/cyber-ontology#Vulnerability"}, properties:{}}, {start: {uri:"http://example.org/cyber-ontology#hasVulnerability"}, end: {uri:"http://example.org/cyber-ontology#Device"}, properties:{}}, {start: {uri:"http://example.org/cyber-ontology#hasSoftware"}, end: {uri:"http://example.org/cyber-ontology#Device"}, properties:{}}] AS row
MATCH (start:Resource{uri: row.start.uri})
MATCH (end:Resource{uri: row.end.uri})
CREATE (start)-[r:rdfs__domain]->(end) SET r += row.properties;
:commit
:begin
MATCH (n:`UNIQUE IMPORT LABEL`)  WITH n LIMIT 20000 REMOVE n:`UNIQUE IMPORT LABEL` REMOVE n.`UNIQUE IMPORT ID`;
:commit
:begin
DROP CONSTRAINT UNIQUE_IMPORT_NAME;
:commit
