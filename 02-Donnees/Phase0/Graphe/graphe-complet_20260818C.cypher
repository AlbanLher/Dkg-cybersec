// === 1. Contraintes (optionnel, pour éviter les doublons)
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Device) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Software) REQUIRE (n.name, n.version) IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Vulnerability) REQUIRE n.id IS UNIQUE;

// === 2. Classes (Ontologie)
CREATE (Device:Class {uri: "http://example.org/cyber-ontology#Device", label: "Appareil", comment: "Un device physique ou virtuel (PC, routeur, serveur)."})
CREATE (Software:Class {uri: "http://example.org/cyber-ontology#Software", label: "Logiciel"})
CREATE (Vulnerability:Class {uri: "http://example.org/cyber-ontology#Vulnerability", label: "Vulnérabilité"})
CREATE (Action:Class {uri: "http://example.org/cyber-ontology#Action", label: "Action corrective"})
CREATE (Rule:Class {uri: "http://example.org/cyber-ontology#Rule", label: "Règle de sécurité"})
CREATE (Threat:Class {uri: "http://example.org/cyber-ontology#Threat", label: "Menace"})

// Hiérarchie
CREATE (Vulnerability)-[:SUB_CLASS_OF]->(Threat)

// === 3. Propriétés
CREATE (hasSoftware:Property {uri: "http://example.org/cyber-ontology#hasSoftware", label: "a pour logiciel", domain: "Device", range: "Software"})
CREATE (hasVulnerability:Property {uri: "http://example.org/cyber-ontology#hasVulnerability", label: "a pour vulnérabilité", domain: "Device", range: "Vulnerability"})
CREATE (requiresAction:Property {uri: "http://example.org/cyber-ontology#requiresAction", label: "nécessite l'action", domain: "Vulnerability", range: "Action"})
CREATE (cvssScore:Property {uri: "http://example.org/cyber-ontology#cvssScore", label: "score CVSS", domain: "Vulnerability", range: "float"})

// === 4. Données (Instances)
// Devices
CREATE (PC_Alban_POC:Device {id: "PC-Alban-POC", type: "PC", ip: "192.168.1.100"})
CREATE (Router_POC:Device {id: "Router-POC", type: "Router", ip: "192.168.1.1"})

// Software
CREATE (OpenSSL_1_0_2:Software {name: "OpenSSL", version: "1.0.2"})
CREATE (Apache_2_4_57:Software {name: "Apache", version: "2.4.57"})

// Vulnerabilities
CREATE (CVE_2023_1234:Vulnerability {id: "CVE-2023-1234", cvssScore: 9.8, description: "Vulnérabilité critique dans OpenSSL 1.0.2 permettant une exécution de code à distance."})

// Actions
CREATE (UpdateOpenSSL:Action {name: "Mettre à jour OpenSSL", description: "Mettre à jour OpenSSL vers la version 3.0.8 pour corriger CVE-2023-1234."})

// Rules
CREATE (Rule_001:Rule {name: "Règle de mise à jour OpenSSL", description: "Tous les devices avec OpenSSL < 3.0 doivent être mis à jour.", requiresAction: UpdateOpenSSL})

// === 5. Relations
// Devices → Software
CREATE (PC_Alban_POC)-[:HAS_SOFTWARE]->(OpenSSL_1_0_2)
CREATE (PC_Alban_POC)-[:HAS_SOFTWARE]->(Apache_2_4_57)
CREATE (Router_POC)-[:HAS_SOFTWARE]->(Apache_2_4_57)

// Software → Vulnerability
CREATE (OpenSSL_1_0_2)-[:AFFECTED_BY]->(CVE_2023_1234)

// Vulnerability → Action
CREATE (CVE_2023_1234)-[:REQUIRES_ACTION]->(UpdateOpenSSL)

// Rule → Action
CREATE (Rule_001)-[:REQUIRES_ACTION]->(UpdateOpenSSL)
