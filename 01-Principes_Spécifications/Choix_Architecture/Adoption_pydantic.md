### **1. Mémo d'Architecture : Adoption de Pydantic V2**

**Fichier à inclure :** `01-Principes_Specification/00_Architecture_Principles.md`

#### **Vision Architecturale : Clean Architecture & Validated Boundaries**

RDFLib gère la persistance, l'inférence et le requêtage SPARQL. Cependant, en tant que moteur de graphe, il ne valide pas strictement la forme des données métiers lors de l'ingestion ou de l'exposition. **Pydantic V2** intervient comme **garde-fou aux frontières de l'application** (_Fail-Fast Principle_).

```
[ Flux Externe / CTI / LLM / API ]
               │
               ▼
   ┌──────────────────────┐
   │   Pydantic Models    │  <-- Validation des types, contraintes & contrats
   └───────────┬──────────┘
               │ (Données validées)
               ▼
   ┌──────────────────────┐
   │    RDFLib Graph      │  <-- Conversion en URIRef, Literal, SPARQL
   └──────────────────────┘
```

#### **Périmètres d'Application**

- **Gestion Globale des Configurations (`pydantic-settings`) :** Remplacement de `config.py` statique par un modèle typé validant les variables d'environnement, la validité des dossiers (`Path`) et les seuils numériques au démarrage.
    
- **Ingestion Zero-Trust :** Validation systématique des données avant leur conversion en triplets RDF.
    
- **Frontières API / LLM :** Garantie de structures JSON valides pour l'intégration avec FastAPI, Instructor ou LangChain.
    

### **2. Analyse de l'Impact de Pydantic sur l'Ensemble du Pipeline (Phases 1 à 5)**

| **Phase / Composant**             | **Rôle de Pydantic**                                                                | **Apport / Bénéfice Métier**                                                                                                                   |
| --------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| **Phase 0 (Config & Socle)**      | Subclassing de `BaseSettings` dans `config.py`.                                     | Validation au boot de l'existence des chemins (`Path`), validation des URIs de base, typage strict des seuils (ex: `0.0 <= THRESHOLD <= 1.0`). |
| **Phase 1 (Data Ingestion)**      | Validation des JSON/CSV/Logs bruts entrants avant parsing RDFLib.                   | Rejet immédiat des lignes corrompues ou des IPs/CVEs malformées avant pollution du graphe master.                                              |
| **Phase 2 (SHACL & Validations)** | Modélisation des rapports de violation SHACL sous forme de schémas Pydantic.        | Formatage propre des rapports de non-conformité TBox/ABox pour enregistrement et alertes CI/CD.                                                |
| **Phase 3 (Enrichissement CTI)**  | Typage des réponses d'APIs externes (CISA KEV, NVD, MITRE ATT&CK).                  | Robustesse face aux breaking changes des schemas JSON des APIs CTI tierces.                                                                    |
| **Phase 4 (Storage & Querying)**  | Mapping d'objets Pydantic vers/depuis des requêtes `SPARQL SELECT`.                 | ORM-like léger permettant de manipuler des objets Python typés au lieu de dictionnaires RDFLib bruts.                                          |
| **Phase 5 (MITM & Inférence)**    | Structuration des entités candidates à la vectorisation et des scores d'alignement. | Contrôle strict du type des `prefLabel`, du format des vecteurs ($384\text{d}$) et du seuil de réconciliation SKOS.                            |