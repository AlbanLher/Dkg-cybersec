// === 1. Ajoutez les nouvelles classes de Phase2
CREATE (Context:Class {
  uri: "http://example.org/cyber-ontology#Context",
  label: "Contexte",
  comment: "Contexte dans lequel une règle s'applique."
})

CREATE (ProductionContext:Context {
  uri: "http://example.org/cyber-ontology#ProductionContext",
  label: "Contexte Production"
})

CREATE (TestContext:Context {
  uri: "http://example.org/cyber-ontology#TestContext",
  label: "Contexte Test"
})

CREATE (ExternalContext:Context {
  uri: "http://example.org/cyber-ontology#ExternalContext",
  label: "Contexte Externe"
})

CREATE (Waiver:Class {
  uri: "http://example.org/cyber-ontology#Waiver",
  label: "Dérogeance",
  comment: "Exception temporaire à une règle de conformité."
})

// === 2. Ajoutez les nouvelles propriétés
CREATE (inContext:Property {
  uri: "http://example.org/cyber-ontology#inContext",
  label: "s'applique dans le contexte",
  domain: "http://example.org/cyber-ontology#Rule",
  range: "http://example.org/cyber-ontology#Context"
})

CREATE (hasWaiver:Property {
  uri: "http://example.org/cyber-ontology#hasWaiver",
  label: "a une dérogation",
  domain: "http://example.org/cyber-ontology#Device",
  range: "http://example.org/cyber-ontology#Waiver"
})

CREATE (justifiedBy:Property {
  uri: "http://example.org/cyber-ontology#justifiedBy",
  label: "est justifiée par",
  domain: "http://example.org/cyber-ontology#Waiver",
  range: "http://www.w3.org/2001/XMLSchema#string"
})

// === 3. Migrez les règles existantes avec un contexte
MATCH (r:ComplianceRule {name: "CVSS < 5 pour les serveurs"})
SET r:inContext :ProductionContext

// === 4. Chargez les nouvelles données de Phase2
CALL apoc.load.json('file:///public/inventory-v3.json') YIELD value
UNWIND value.devices AS device
MERGE (d:Device {id: device.id})
ON CREATE SET d.type = device.type, d.internal = device.internal, d.ip = device.ip
ON MATCH SET d.internal = device.internal, d.ip = device.ip
WITH device, d
UNWIND device.software AS sw
MERGE (s:Software {name: sw.name, version: sw.version})
CREATE (d)-[:HAS_SOFTWARE]->(s)

// === 5. Chargez les nouvelles CVE
CALL n10s.rdf.import.file('file:///public/cve_data-v3.ttl', 'Turtle')

// === 6. Chargez les nouvelles règles
CALL n10s.rdf.import.file('file:///pseudo-private/rules-v3.ttl', 'Turtle')

// === 7. Appliquez les règles avec contexte
// Règle Production : CVSS < 5 pour les InternalDevice
MATCH (d:InternalDevice)-[:HAS_SOFTWARE]->(s:Software)<-[:AFFECTED_BY]-(v:Vulnerability)
WITH d, MAX(v.cvssScore) AS maxCVSS
SET d:hasComplianceStatus ->
  CASE WHEN maxCVSS <= 5.0 THEN :Compliant
       ELSE :NonCompliant
  END

// Règle Externe : CVSS < 7 pour les ExternalDevice
MATCH (d:ExternalDevice)-[:HAS_SOFTWARE]->(s:Software)<-[:AFFECTED_BY]-(v:Vulnerability)
WITH d, MAX(v.cvssScore) AS maxCVSS
SET d:hasComplianceStatus ->
  CASE WHEN maxCVSS <= 7.0 THEN :Compliant
       ELSE :NonCompliant
  END
