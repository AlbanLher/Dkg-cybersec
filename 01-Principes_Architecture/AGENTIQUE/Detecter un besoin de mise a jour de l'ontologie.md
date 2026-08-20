
Quand l'assistant ingère un document, comment sait-il que l'information qu'il lit nécessite de **modifier la structure (l'ontologie)** et pas seulement d'**ajouter des données (les instances)** ?

Ce mécanisme repose sur une boucle de détection en 3 étapes :


```
[Document Source (ex: Bulletin Cyber / Rapport Audit)]
                             │
                             ▼ 
               [Agent d'Ingestion / NER]
                             │
        ┌────────────────────┴────────────────────┐
        ▼                                         ▼
[Entités/Relations Connues]              [Entités/Relations Inconnues]
(Conformes à l'Ontologie V0)             (Non mappables sur l'Ontologie V0) 
        │                                         │
        ▼                                         ▼ 
[Insertion Directe Neo4j]          [Leurres de Détection / Out-of-Vocabulary] 
                                                  │
                                                  ▼ 
                                     [Agent "Ontology Governor"] 
                                                  │ 
                                                  ▼ 
                                    [Proposition d'Évolution Ontologique (V1)]
```



#### Étape A : Le Test de Conformité au Schéma (Validation SHACL / Dynamic Schema Guard)

L'Agent d'Extraction tente de convertir un texte brut en triplets RDF en suivant la grammaire de l'ontologie actuelle.

- Si le document parle d'un nouveau routeur `Router-123` avec `OpenSSL 3.0.8`, l'Agent reconnaît `Device` et `Software` : **c'est une simple nouvelle instance**.
    
- Si le document mentionne : _"L'équipement est soumis à la norme NIS2 et nécessite le patch REQ-88"_, l'Agent constate qu'il n'existe aucun concept `Requirement` ou `Standard` dans son schéma d'entrée : **c'est une rupture de schéma (Out-of-Vocabulary)**.
    

#### Étape B : La Détection des "Symptômes" d'Évolution

L'Agent d'extraction génère un **Rapport d'Anomalie Sémantique** lorsqu'il rencontre :

1. **Des propriétés sans classe cible :** L'Agent trouve une information pertinente qu'il doit stocker dans un champ génerique `unmapped_properties: {"compliance": "NIS2"}`.
    
2. **Des relations orphelines :** L'Agent détecte un lien logique entre un `Device` et une entité inconnue qu'il ne sait pas typer.
    

#### Étape C : La Proposition d'Amendement (Le Rôle du "Ontology Governor")

L'Agent IA ne doit **jamais modifier l'ontologie de référence de manière autonome en production**. À la place, un Agent spécialisé (l'_Ontology Governor_) :

1. Regroupe les anomalies récurrentes d'ingestion.
    
2. Génère une **Proposition d'Extension Turtle (`ontologie_v1_draft.ttl`)**.
    
3. Reconstruit le **Mermaid mis à jour** et une note de synthèse.
    
4. **Soumet la demande de modification à l'humain (Human-in-the-loop / Le Garant Métier)**.
    

Une fois la modification validée par l'expert, l'ontologie passe en V1, et la procédure de ré-ingestion/migration est lancée.