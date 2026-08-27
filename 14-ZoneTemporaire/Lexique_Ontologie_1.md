
```
[ Sources Humaines / Markdown ]
  - 1-Lexique/Inernal_Input/Prive/LEXIQUE_METIER.md
  - 2-Ontologie/Inernal_Input/Prive/demandeEvolutionOntologie/TEMPLATE...
          │
          ▼  (Exécution de 7-ScriptsSpecifiques/orchestrator_phase0.py)
[ Compilation & Standardisation TTL ]
  - 3-App_Referential_Vault/LEXIQUE_PRIVEE.ttl
  - 3-App_Referential_Vault/ontologie-privee-v0.ttl
          │
          ├─────────────────────────────────────────┐
          ▼                                         ▼
[ Ingestion Neo4j ]                     [ Génération Restitution ]
  - 6-Graphe/graphe-complet_...cypher     - 4-App_publication_md/Lexiques/
                                          - 4-App_publication_md/Ontologies/par_domaines/
                                            
```
```mermaid
flowchart TD
    subgraph SOURCES_INTERNES [1. Inputs Internes - Markdown]
        Lex_Int_Priv[1-Lexique/Inernal_Input/Prive/LEXIQUE_METIER.md]
        Lex_Int_Pub[1-Lexique/Inernal_Input/Public/LEXIQUE_PUBLIQUE.md]
        Ont_Evol[2-Ontologie/Inernal_Input/Prive/demandeEvolutionOntologie/*.md]
    end

    subgraph SOURCES_EXTERNES [2. Inputs Externes - TTL / Feeds]
        Lex_Ext_Pub[1-Lexique/External_Input/Public/misp-taxonomies.ttl]
        Lex_Ext_Priv[1-Lexique/External_Input/Prive/partner-taxonomies.ttl]
        Ont_Ext_Pub[2-Ontologie/External_Input/Public/cve_data.ttl]
        Ont_Ext_Priv[2-Ontologie/External_Input/Prive/partner_schema.ttl]
    end

    subgraph ENGINE [7-ScriptsSpecifiques]
        Orchestrator[orchestrator_phase0.py]
        LoaderNeo4j[load_into_neo4j.py / ttl_to_cypher.py]
    end

    subgraph VAULT [3-App_Referential_Vault - TTL Unifié]
        Vault_Lex_Pub[LEXIQUE_PUBLIQUE.ttl]
        Vault_Lex_Priv[LEXIQUE_PRIVEE.ttl]
        Vault_Ont_Pub[ontologie-publique-v0.ttl]
        Vault_Ont_Priv[ontologie-privee-v0.ttl]
    end

    subgraph PUBLICATION [4-App_publication_md]
        Pub_Lex[Lexiques/PUBLICATION_LEXIQUE_GLOBAL.md]
        Pub_Ont[Ontologies/par_domaines/DOMAINE_*.md]
    end

    subgraph GRAPH_DB [6-Graphe & Neo4j DB]
        Cypher[graphe-complet_2026.cypher]
        Neo4j[(Neo4j Instance / n10s)]
    end

    %% Connexions des flux
    SOURCES_INTERNES -->|Parsing MD -> SKOS/OWL| Orchestrator
    SOURCES_EXTERNES -->|Validation SHACL & Alignement| Orchestrator

    Orchestrator -->|Compilation & Consolidation| VAULT
    Orchestrator -->|Génération Doc & Diagrams Mermaid| PUBLICATION

    VAULT --> LoaderNeo4j
    LoaderNeo4j -->|Export Cypher| Cypher
    LoaderNeo4j -->|Injection directe| Neo4j
    
```