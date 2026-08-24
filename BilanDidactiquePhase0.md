# 🎓 Bilan Didactique et Manuel de Prise en Main - Phase 0

> **Objectif de la Phase 0 :** Établir le **Méta-modèle, la Gouvernance et le Référentiel Formel** (Lexiques SKOS, Ontologies OWL/TTL) sans s'encombrer de l'instanciation de données brutes.
## 1. Ce qui a été mis en œuvre (Architecture & Concept)

En Phase 0, nous avons posé les fondations du Graph de Connaissances Référentiel (_Data Knowledge Graph_) en séparant strictement le **Méta-modèle (TBox / Lexique)** des **Données Réelles (ABox / Instances)**.
```
[ Sources Brutes ]           [ Vault RDF ]              [ Projection Graph ]
  • 1-Lexique/*.md    ──┐                           ┌──> Neo4j Schema (.cypher)
  • 2-Ontologie/*.ttl ──┼─> [ VAULT_CONSOLIDE.ttl ] ┤
                        │                           └──> doc_ontologie_globale.md
                        └─ (Vérifications TBox)
```

### Acquis structuraux :

1. **Périmètre Lexical (`1-Lexique/`)** : Définition des concepts métiers en Markdown, convertis dynamiquement en vocabulaire normé **SKOS** (`skos:Concept`, `skos:prefLabel`, `skos:definition`).
    
2. **Périmètre Ontologique (`2-Ontologie/`)** : Structure formelle des classes et relations de domaine sous forme de fichiers Turtle/OWL (`.ttl`).
    
3. **Référentiel Central (`3-App_Referential_Vault/`)** : Unification des ontologies et du lexique au sein d'un graphe RDF unique : **`VAULT_CONSOLIDE.ttl`**.
    
4. **Validation par Contrôles de Couverture** :
    
    - **Vérification 1 (Input ➔ Vault)** : S'assurer que 100% des concepts déclarés dans les lexiques sont présents dans le Vault.
        
    - **Vérification 2 (Vault ➔ Neo4j)** : S'assurer que la structure de classes du Vault est fidèlement projetée dans le schéma Cypher.
        
5. **Architecture Modulaire Python (`7-ScriptsSpecifiques/`)** :
    
    - `parsers/` : Ingestion des lexiques MD et ontologies TTL.
        
    - `checkers/` : Contrôle de couverture et de conformité structurelle.
        
    - `exporters/` : Publication automatique des documentations Markdown et scripts Cypher.
        

## 2. Parcours Pas à Pas pour un Nouveau Arrivant

Si vous rejoignez le projet ou souhaitez rejouer la Phase 0 pas à pas :

### Étape 1 : Préparer l'environnement

Assurez-vous d'avoir Python installé avec la bibliothèque `rdflib` :

Bash

```
pip install rdflib
```

### Étape 2 : Inspecter les sources du Méta-modèle

1. Ouvrez un fichier dans `1-Lexique/` (ex: `lexique_global.md`) pour observer la structure des concepts métiers et leurs synonymes.
    
2. Ouvrez un fichier ontologique dans `2-Ontologie/` (ex: `ontologie_securite.ttl`) pour visualiser la hiérarchie des classes RDF (`owl:Class`).
    

### Étape 3 : Exécuter l'Orchestrateur de Structure

Lancez le script d'ordonnancement depuis la racine du workspace :

Bash

```
python 02-Donnees/Phase0/7-ScriptsSpecifiques/orchestrator_phase0.py
```

### Étape 4 : Analyser les livrables générés

- **Vault Consolidé** : Consultez `3-App_Referential_Vault/VAULT_CONSOLIDE.ttl`.
    
- **Documentation** : Parcourez `4-App_publication_md/Ontologies/doc_ontologie_globale.md`.
    
- **Rapport de Couverture** : Vérifiez le score dans `4-App_publication_md/REPORTING_VAULT.md`.
    
- **Schéma Neo4j** : Inspectez `6-Graphe/graphe-global_schema.cypher`.