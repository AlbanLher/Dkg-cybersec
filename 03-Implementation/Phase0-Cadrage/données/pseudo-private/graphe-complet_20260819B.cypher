:begin
CREATE RANGE INDEX FOR (n:Device) ON (n.id);
CREATE CONSTRAINT UNIQUE_IMPORT_NAME FOR (node:`UNIQUE IMPORT LABEL`) REQUIRE (node.`UNIQUE IMPORT ID`) IS UNIQUE;
:commit
CALL db.awaitIndexes(300);
:begin
UNWIND [{_id:4, properties:{uri:"http://example.org/cyber-ontology#cvssScore"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:Class:owl__DatatypeProperty;
UNWIND [{_id:14, properties:{ip:"192.168.1.100", id:"PC-Alban-POC", type:"PC"}}, {_id:17, properties:{ip:"192.168.1.1", id:"Router-POC", type:"Router"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:Device;
UNWIND [{_id:2, properties:{uri:"http://example.org/cyber-ontology#Software"}}, {_id:5, properties:{uri:"http://example.org/cyber-ontology#Action"}}, {_id:7, properties:{uri:"http://example.org/cyber-ontology#Device"}}, {_id:8, properties:{uri:"http://example.org/cyber-ontology#Threat"}}, {_id:10, properties:{uri:"http://example.org/cyber-ontology#Vulnerability"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:Class;
UNWIND [{_id:15, properties:{name:"OpenSSL", version:"1.0.2"}}, {_id:16, properties:{name:"Apache", version:"2.4.57"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:Software;
UNWIND [{_id:3, properties:{uri:"http://example.org/cyber-ontology#requiresAction"}}, {_id:6, properties:{uri:"http://example.org/cyber-ontology#hasVulnerability"}}, {_id:9, properties:{uri:"http://example.org/cyber-ontology#hasSoftware"}}] AS row
CREATE (n:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row._id}) SET n += row.properties SET n:owl__ObjectProperty:Class;
:commit
:begin
UNWIND [{start: {_id:14}, end: {_id:15}, properties:{}}, {start: {_id:14}, end: {_id:16}, properties:{}}, {start: {_id:17}, end: {_id:16}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:HAS_SOFTWARE]->(end) SET r += row.properties;
UNWIND [{start: {_id:9}, end: {_id:7}, properties:{}}, {start: {_id:3}, end: {_id:10}, properties:{}}, {start: {_id:6}, end: {_id:7}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:domain]->(end) SET r += row.properties;
UNWIND [{start: {_id:4}, end: {_id:10}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:domain]->(end) SET r += row.properties;
UNWIND [{start: {_id:3}, end: {_id:5}, properties:{}}, {start: {_id:6}, end: {_id:10}, properties:{}}, {start: {_id:9}, end: {_id:2}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:range]->(end) SET r += row.properties;
UNWIND [{start: {_id:10}, end: {_id:8}, properties:{}}] AS row
MATCH (start:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.start._id})
MATCH (end:`UNIQUE IMPORT LABEL`{`UNIQUE IMPORT ID`: row.end._id})
CREATE (start)-[r:subClassOf]->(end) SET r += row.properties;
:commit
:begin
MATCH (n:`UNIQUE IMPORT LABEL`)  WITH n LIMIT 20000 REMOVE n:`UNIQUE IMPORT LABEL` REMOVE n.`UNIQUE IMPORT ID`;
:commit
:begin
DROP CONSTRAINT UNIQUE_IMPORT_NAME;
:commit
