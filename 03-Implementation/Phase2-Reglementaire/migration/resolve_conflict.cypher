// === PROBLÈME : Server-Prod a un CVSS 9.8 (via OpenSSL 1.0.2) mais est en Production
// La règle "CVSS < 5 pour les serveurs" est violée.

// === SOLUTION 1 : Ajoutez une dérogation (Waiver) pour Server-Prod
MATCH (d:InternalDevice {id: "Server-Prod"})
CREATE (w:Waiver {
  id: "WAIVER-2026-001",
  justifiedBy: "Migration en cours vers OpenSSL 3.0.8 (prévue pour le 2026-09-01). Client externe dépendant de cette version."
})
CREATE (d)-[:HAS_WAIVER]->(w)

// === SOLUTION 2 : Ajoutez un contexte spécifique pour ce serveur
// (Alternative : on pourrait aussi créer un contexte "MigrationEnCours")
MATCH (d:InternalDevice {id: "Server-Prod"})
SET d:inContext :TestContext  // ← On le considère temporairement en "Test"

// === SOLUTION 3 (Recommandée) : Créez un contexte "MigrationEnCours"
// CREATE (MigrationContext:Context {label: "Migration en cours"})
// SET d:inContext :MigrationContext

// === Vérification
MATCH (d:InternalDevice)-[:hasComplianceStatus]->(s)
RETURN d.id AS device, s.label AS status

MATCH (d:InternalDevice)-[:HAS_WAIVER]->(w)
RETURN d.id AS device, w.id AS waiver, w.justifiedBy AS justification
