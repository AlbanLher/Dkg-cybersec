// === 1. Ajoutez les nouvelles classes de Phase1
CREATE (InternalDevice:Class {
  uri: "http://example.org/cyber-ontology#InternalDevice",
  label: "Device interne",
  comment: "Device appartenant à l'entreprise."
})

CREATE (ExternalDevice:Class {
  uri: "http://example.org/cyber-ontology#ExternalDevice",
  label: "Device externe",
  comment: "Device hors du réseau de l'entreprise."
})

CREATE (ComplianceRule:Class {
  uri: "http://example.org/cyber-ontology#ComplianceRule",
  label: "Règle de conformité",
  comment: "Règle liée à une exigence réglementaire."
})

CREATE (ComplianceStatus:Class {
  uri: "http://example.org/cyber-ontology#ComplianceStatus",
  label: "Statut de conformité"
})

CREATE (Compliant:ComplianceStatus {
  uri: "http://example.org/cyber-ontology#Compliant",
  label: "Conforme"
})

CREATE (NonCompliant:ComplianceStatus {
  uri: "http://example.org/cyber-ontology#NonCompliant",
  label: "Non conforme"
})

// === 2. Ajoutez les nouvelles propriétés
CREATE (hasComplianceStatus:Property {
  uri: "http://example.org/cyber-ontology#hasComplianceStatus",
  label: "a pour statut de conformité",
  domain: "http://example.org/cyber-ontology#InternalDevice",
  range: "http://example.org/cyber-ontology#ComplianceStatus"
})

CREATE (appliesTo:Property {
  uri: "http://example.org/cyber-ontology#appliesTo",
  label: "s'applique à",
  domain: "http://example.org/cyber-ontology#ComplianceRule",
  range: "http://example.org/cyber-ontology#InternalDevice"
})

// === 3. Migrez les devices existants vers InternalDevice
MATCH (d:Device)
WHERE d.id IN ["PC-Alban-POC", "Router-POC"]
SET d:InternalDevice

// === 4. Chargez les nouvelles données de Phase1
CALL apoc.load.json('file:///public/inventory-v2.json') YIELD value
UNWIND value.devices AS device
MERGE (d:Device {id: device.id})
ON CREATE SET d.type = device.type, d.internal = device.internal, d.ip = device.ip
ON MATCH SET d.internal = device.internal, d.ip = device.ip
WITH device, d
UNWIND device.software AS sw
MERGE (s:Software {name: sw.name, version: sw.version})
CREATE (d)-[:HAS_SOFTWARE]->(s)

// === 5. Chargez les nouvelles CVE
CALL n10s.rdf.import.file('file:///public/cve_data-v2.ttl', 'Turtle')

// === 6. Chargez les nouvelles règles
CALL n10s.rdf.import.file('file:///pseudo-private/rules-v2.ttl', 'Turtle')

// === 7. Appliquez la règle de conformité CVSS < 5
MATCH (d:InternalDevice)-[:HAS_SOFTWARE]->(s:Software)<-[:AFFECTED_BY]-(v:Vulnerability)
WITH d, MAX(v.cvssScore) AS maxCVSS
SET d:hasComplianceStatus ->
  CASE WHEN maxCVSS <= 5.0 THEN :Compliant
       ELSE :NonCompliant
  END
