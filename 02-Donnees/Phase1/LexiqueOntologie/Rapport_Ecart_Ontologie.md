# 🛡️ Rapport d'Analyse d'Ingestion & Validation d'Ontologie

**Statut d'Ingestion :** `Cas 2 / Cas 3 : Écart d'ontologie détecté`

---

## 1. Bilan des Écarts Détectés

* **Nouvelles Classes Identifiées :** `Aucune`
* **Nouvelles Propriétés / Attributs :** `['description', 'name', 'Device.internal']`

---

## 2. Comparaison Visuelle (Diff Mermaid)

### Structure Actuelle (Avant / V0)
```mermaid
classDiagram
    direction LR
    class Device {
        +String id
        +String ip
        +String type
    }
    class Software {
        +String key
        +String name
        +String version
    }
    class Vulnerability {
        +String name
        +Float cvssScore
    }
    Device "1" --> "*" Software : HAS_SOFTWARE
    Software "1" --> "*" Vulnerability : HAS_VULNERABILITY
```

### Structure Proposée (Après / V1)
```mermaid
classDiagram
    direction LR
    class Device {
        +String id
        +String ip
        +String type
        +String internal :: NOUVEAU ::
    }
    class Software {
        +String key
        +String name
        +String version
    }
    class Vulnerability {
        +String name
        +Float cvssScore
        +String description :: NOUVEAU ::
    }
    Device "1" --> "*" Software : HAS_SOFTWARE
    Software "1" --> "*" Vulnerability : HAS_VULNERABILITY
```

---

## 3. Snippet Turtle (`.ttl`) à intégrer dans `ontologie.ttl` 

```turtle
# ==========================================
# EXTENSION PROPOSÉE PHASE 1
# ==========================================

cyber:description a owl:DatatypeProperty ;
    rdfs:label "description" ;
    rdfs:range xsd:string .

cyber:name a owl:DatatypeProperty ;
    rdfs:label "name" ;
    rdfs:range xsd:string .

cyber:internal a owl:DatatypeProperty ;
    rdfs:label "internal" ;
    rdfs:range xsd:string .
```
