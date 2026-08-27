
En Représentation des Connaissances (et dans l'écosystème du Web Sémantique / RDF / Web Ontology Language), la **TBox** et la **ABox** sont les deux composantes fondamentales d'une base de connaissances.

Pour le dire de manière très simple : la **TBox est le dictionnaire** (la structure), et la **ABox représente la réalité du terrain** (les données).

### 1. La TBox (Terminological Box) = Le Modèle / Le Dictionnaire

La **TBox** contient le vocabulaire, les règles, les catégories et la structure conceptuelle. Elle définit **ce qui a le droit d'exister** et **comment les choses s'organisent**, sans parler de données réelles.

- **Ce qu'on y trouve** : Des classes (concepts), des sous-classes, et des propriétés (relations).
    
- **Dans votre projet (Phase 0)** : C'est le fichier `ONTOLOGY_TBOX.ttl`.
    

**Exemples de déclarations TBox :**

- _Un `Serveur` est une catégorie d'équipement._
    
- _Un `ServeurLinux` est un sous-type de `Serveur`._
    
- _Un `Serveur` peut posséder une `AdresseIP` (relation : `hasIP`)._
    
- _Une `Vulnérabilité` affecte un `Logiciel` (relation : `affects`)._
    

### 2. La ABox (Assertional Box) = Les Données Réelles / Les Instances

La **ABox** contient les faits concrets, les individus et les données réelles du système d'information. Elle décrit **ce qui existe actuellement sur le terrain** en s'appuyant sur les règles de la TBox.

- **Ce qu'on y trouve** : Des instances (nœuds réels) et des liens précis entre ces instances.
    
- **Dans votre projet (Phase 1)** : C'est le fichier `INSTANCES_ABOX.ttl`.
    

**Exemples de déclarations ABox :**

- _`SRV-WEB-01` est un `ServeurLinux`._ (Ici `SRV-WEB-01` est une instance réelle).
    
- _`SRV-WEB-01` a pour adresse IP `192.168.1.50`._
    
- _`CVE-2023-4863` est une `Vulnérabilité`._
    
- _`CVE-2023-4863` affecte le logiciel `Nginx-1.18` installé sur `SRV-WEB-01`._
    

### 📊 Tableau Comparatif

|Critère|**TBox** (Phase 0)|**ABox** (Phase 1)|
|---|---|---|
|**Rôle**|Définit le schéma et les règles du domaine|Stocke la donnée réelle et les faits|
|**Analogie BDD**|Le schéma SQL (`CREATE TABLE`, clés étrangères)|Les lignes dans la table (`INSERT INTO`)|
|**Analogie POO**|La Définition des Classes (`class Server:`)|Les Objets instanciés (`s1 = Server()`)|
|**Stabilité**|Change très rarement (modèle métier)|Change constamment (nouveaux scans, logs)|
|**Fichier Projet**|`ONTOLOGY_TBOX.ttl`|`INSTANCES_ABOX.ttl`|

### 💡 Pourquoi cette séparation est importante dans votre GraphRAG ?

1. **Sans la TBox (Phase 0)** : Vos scripts d'extraction NER (Phase 1) extrairaient des mots au hasard sans structure (ex: créer un type `ServeurWeb`, un autre `Serveur_Linux`, un autre `Host`).
    
2. **Grâce à la TBox** : Votre LLM et vos scripts d'alignement (`entity_aligner.py`) savent exactement dans quelle "case" officielle ranger chaque équipement découvert sur votre réseau.


----
La distinction entre la **ABox** et le **Graphe Neo4j** repose sur la différence entre le **concept logique (la donnée)** et le **moteur de stockage (la base de données)**.

En clair : **la ABox est le contenu**, et **Neo4j est le conteneur/moteur d'exécution**.

### 1. La ABox : Le Fichier de Faits RDF (Niveau Sémantique & Standard)

La **ABox** (Assertional Box) est une représentation **formelle, portable et indépendante de tout logiciel**. Elle est exprimée sous forme de graphe RDF (fichiers `.ttl` / Turtle) et suit strictement les normes du W3C.

- **Format** : Fichier texte standard (`INSTANCES_ABOX.ttl`).
    
- **Représentation** : Triplets W3C de type `Sujet -> Prédicat -> Objet`.
    
- **Rôle** : Servir de **sauvegarde neutre et interopérable** de l'ensemble des données réelles du SI (équipements, logiciels, vulnérabilités).
    
- **Portabilité** : Ce fichier `.ttl` peut être chargé dans n'importe quelle base sémantique du marché (GraphDB, Stardog, Jena, Amazon Neptune) sans aucune modification.
    

**Exemple ABox (Turtle) :**

Extrait de code

```
inst:Equipment_SRV_WEB_01 a ex:Equipment ;
    rdfs:label "SRV-WEB-01" ;
    ex:hasSoftware inst:Software_Apache_2_4_49 .
```

### 2. Le Graphe Neo4j : L'Index de Calcul, de Traitement et de Recherche (Niveau Physique)

Le **Graphe Neo4j** est la **projection de la ABox dans une base de données Property Graph** hautement optimisée pour les requêtes à très haute performance, la recherche hybride (Vector Search + Fulltext) et le RAG.

- **Format** : Base de données orientée objets/propriétés (modèle Labeled Property Graph - LPG).
    
- **Représentation** : Nœuds, Étiquettes (_Labels_), Relations et Propriétés clé-valeur.
    
- **Rôle** : Servir de **moteur d'exécution opérationnel**. C'est lui qui exécute les traversées de liens rapides (Cypher), stocke les vecteurs d'embeddings (`bge-small-en-v1.5`) et répond aux requêtes du LLM en temps réel.
    

**Exemple Neo4j (Cypher) :**

Cypher

```
(:Equipment {id: "SRV-WEB-01", text: "..."})-[:HAS_SOFTWARE]->(:Software {name: "Apache_2_4_49"})
```

### ⚖️ Comparaison Synthétique

|Critère|**La ABox** (`INSTANCES_ABOX.ttl`)|**Le Graphe Neo4j** (Database)|
|---|---|---|
|**Nature**|Norme sémantique / Modèle de données|Logiciel / Moteur de base de données|
|**Stockage**|Fichier Turtle (`.ttl`) sur le disque|Base de données NoSQL / Index en mémoire|
|**Indexation**|Aucune (fichier brut)|**Vector Index** (Cosine) + **Fulltext Index** (Lucene)|
|**Langage**|SPARQL|Cypher|
|**Poids/Rôle**|**Source de vérité d'instances (ABox)**|**Moteur de calcul RAG & Traversée rapide**|

### 🔄 Le Flux dans Votre Architecture Phase 1

1. Vos scripts d'ingestion (JSON, NER) extraient les données et génèrent le fichier **`INSTANCES_ABOX.ttl`** (La ABox officielle).
    
2. Ce fichier ABox est ensuite **projeté/chargé dans Neo4j**.
    
3. Dans Neo4j, le module `embedder.py` enrichit ces nœuds avec leurs **embeddings vectoriels** pour permettre la recherche hybride (GraphRAG).