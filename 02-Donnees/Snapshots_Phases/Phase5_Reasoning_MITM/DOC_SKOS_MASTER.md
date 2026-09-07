# 📑 Livrable Phase 5 - Thésaurus & Consolidation SKOS

**Classification :** `TLP:AMBER`  
**Nombre de triplets consolidés :** `120`

---

## 📖 Glossaire & Table des Acronymes Métier

| Acronyme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **OWL** | Web Ontology Language | Langage d'équivalence sémantique (`owl:sameAs`). |
| **SKOS** | Simple Knowledge Organization System | Normalisation du thésaurus de concepts. |
| **SSOT** | Single Source of Truth | Source unique de vérité (`config.py`). |
| **TBox** | Terminology Box | Définition du schéma sémantique et des concepts. |

---

## 🔄 Flux de Consolidation SKOS / TBox

```mermaid
flowchart TD
    ALIGN[Alignement Agent MITM] --> CONSOL[Règle R-MITM-01]
    TBOX[DKG_TBox_Master.ttl] --> CONSOL
    CONSOL -->|skos:exactMatch / owl:sameAs| SKOS_M[DKG_SKOS_Master.ttl]
```

*Document généré automatiquement post-consolidation SKOS.*
