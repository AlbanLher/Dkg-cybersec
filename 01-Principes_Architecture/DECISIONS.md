# 1 - Décisions Architecturales
## 1.1 -  Gestion des Données Sensibles
### 1.1 .1- Choix Actuel : `.gitignore` + `.private/`

| Critère           | Pourquoi ce choix ?                          | Avantages                               | Limites                                                |
| ----------------- | -------------------------------------------- | --------------------------------------- | ------------------------------------------------------ |
| **Simplicité**    | Pas besoin de gérer des clés de chiffrement. | ✅ Facile à mettre en œuvre.             | ❌ Données non versionnées (pas d’historique).          |
| **Compatibilité** | Fonctionne avec tous les outils Git.         | ✅ Intégration native avec Obsidian/Git. | ❌ Risque d’oubli (fichier non ignoré par erreur).      |
| **Performance**   | Pas de surcoût CPU/mémoire.                  | ✅ Rapide.                               | ❌ Pas de protection si `.gitignore` est mal configuré. |
| **Collaboration** | Chaque utilisateur gère ses données locales. | ✅ Pas de conflit de merge.              | ❌ Pas de partage sécurisé des données privées.         |

### 1.1.2 -  Alternative : Chiffrement (GPG/7-Zip)**

|Critère|Quand l’utiliser ?|Avantages|Limites|
|---|---|---|---|
|**Sécurité maximale**|Données **ultra-sensibles** (ex: logs, clés API).|✅ Protection même si GitHub est compromis.|❌ Gestion des clés complexe.|
|**Versionnage**|Historique des données sensibles.|✅ Historique chiffré possible.|❌ Requiert un outil externe (ex: `git-crypt`).|
|**Partage sécurisé**|Collaboration sur données sensibles.|✅ Contrôle d’accès fin (qui a la clé ?).|❌ Complexité pour les non-techniciens.|

### 1.1.3 - Choix Actuel : `.gitignore` + `.private/`
- **Décision** : Exclure `.private/` via `.gitignore` pour les données locales (inventaire réel, configs).
- **Justification** :
  - Simplicité pour un POC.
  - Compatible avec Obsidian/Git.
  - Pas de besoin de versionnage pour les données sensibles dans cette phase.
- **Fichiers concernés** :
  - `.private/inventory-reel.json`
  - `.private/config/neo4j.conf`
  - `.private/data/logs/`

### 1.1.4 - Alternative Future : Chiffrement
- **Cas d’usage** : Si le projet passe en production avec des données critiques (ex: logs clients).
- **Outils** :
  - **GPG** : `gpg --symmetric --cipher-algo AES256 fichier.txt`
  - **git-crypt** : [https://github.com/AGWA/git-crypt](https://github.com/AGWA/git-crypt) (intégration Git).
  - **7-Zip** : `7z a -p -mhe=on archive.7z dossier/`
- **Migration** :
  - Déplacer les fichiers de `.private/` vers `.private/encrypted/`.
  - Documenter la procédure de chiffrement/déchiffrement.


### 1.1.5 -  Données Publiques vs Privées

| Type          | Stockage                             | Raison                      | Exemples                          |
| ------------- | ------------------------------------ | --------------------------- | --------------------------------- |
| **Publiques** | Dépôt GitHub (public)                | Partage et collaboration    | Ontologie, scripts, documentation |
| **Privées**   | `.private/` (exclu par `.gitignore`) | Sécurité et confidentialité | Inventaire réel, configs, logs    |
### 1.1.6 - Alternatives pour les Données Sensibles
- **Chiffrement** :
  - **Outils** : GPG, 7-Zip (AES-256), git-crypt.
  - **Cas d’usage** : Données critiques (ex: logs clients, clés API).
  - **Migration** :
    ```bash
    # Exemple avec git-crypt
    git-crypt init
    echo "*.secret filter=git-crypt diff=git-crypt" >> .gitattributes
    git add .gitattributes
    git commit -m "Ajout git-crypt pour les fichiers sensibles"
    ```
- **Sous-modules Git** :
  - **Avantage** : Versionnage des données privées dans un dépôt séparé.
  - **Exemple** :
    ```bash
    git submodule add git@github.com\:AlbanLher/dkg-private-data.git .private
    ```

---


## 1.2. Choix du Graphe : Neo4j vs NetworkX

### 1.2.1 - Comparatif Neo4j vs NetworkX

| Critère           | Neo4j (Docker Community)               | NetworkX                   | Recommandation                   |
| ----------------- | -------------------------------------- | -------------------------- | -------------------------------- |
| **Type**          | Base de données graphique              | Bibliothèque Python        | Neo4j pour la production         |
| **Performance**   | ⚡ **Très élevée** (indexée, optimisée) | ⏳ Moyenne (en mémoire)     | Neo4j pour >10k nœuds            |
| **Requêtes**      | Cypher (langage dédié)                 | Python (code personnalisé) | Cypher plus lisible              |
| **Persistance**   | ✅ Oui (fichiers sur disque)            | ❌ Non (en mémoire)         | Neo4j pour la durabilité         |
| **Scalabilité**   | ✅ Horizontale (cluster)                | ❌ Limitée par la RAM       | Neo4j pour l’évolutivité         |
| **Intégration**   | API REST/Bolt                          | Python natif               | NetworkX pour les prototypes     |
| **Docker**        | ✅ Image officielle (`neo4j:community`) | ❌ Non applicable           | Neo4j Docker = simple à déployer |
| **Licence**       | GPL (Community)                        | BSD                        | Les deux open-source             |
| **Visualisation** | ✅ Neo4j Browser/Bloom                  | ❌ Matplotlib (basique)     | Neo4j pour l’UI                  |
| **Apprentissage** | Courbe moyenne (Cypher)                | Courbe faible (Python)     | NetworkX pour les débutants      |

#### 2.1.1 - Choix : Neo4j (Docker Community)
| Critère         | Valeur                     | Justification              |
| --------------- | -------------------------- | -------------------------- |
| **Type**        | Base de données graphique  | Persistance et performance |
| **Déploiement** | Docker (`neo4j:community`) | Simplicité et portabilité  |
| **Langage**     | Cypher                     | Standard pour les graphes  |
| **Licence**     | GPL                        | Open-source et gratuit     |
| **Évolutivité** | Cluster possible           | Adapté à la croissance     |

#### 2.1.2 - Alternative : NetworkX
| Critère         | Valeur                    | Cas d’Usage                         |
| --------------- | ------------------------- | ----------------------------------- |
| **Type**        | Bibliothèque Python       | Prototypage rapide                  |
| **Déploiement** | `pip install networkx`    | Pas besoin de Docker                |
| **Langage**     | Python                    | Intégration facile avec vos scripts |
| **Licence**     | BSD                       | Open-source                         |
| **Limites**     | Pas de persistance native | Données en mémoire seulement        |

#### 2.1.3 - Migration Neo4j → NetworkX (ou inversement)
- **Neo4j → NetworkX** :
```python
  from neo4j import GraphDatabase
  import networkx as nx

  # Exporter depuis Neo4j
  driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
  with driver.session() as session:
      results = session.run("MATCH (n) RETURN n")
      # Convertir en NetworkX...

  # Importer dans NetworkX
  G = nx.Graph()
  for node in results:
      G.add_node(node["n"]["id"], **node["n"].properties)



```





### 1.2.2 - Analyse des Enjeux pour Votre Cas d’Usage

Avantage Neo4j Docker Community pour le projet

1. **POC/Rapide à déployer** :
    
```bash
docker run -p 7474:7474 -p 7687:7687 -v neo4j_data:/data neo4j:community
```
    
    → **1 commande** pour avoir un graphe opérationnel.
    
2. **Intégration avec votre ontologie** :
    
    - Neo4j **comprend nativement RDF/OWL** (via plugins comme [Neo4j RDF](https://github.com/neo4j-labs/neordf)).
    - Exemple de requête Cypher pour charger votre ontologie :
     
```cypher
// Créer les nœuds depuis votre TTL
CREATE (d:Device {name: "PC Alban"})
CREATE (s:Software {name: "OpenSSL", version: "1.0.2"})
CREATE (v:Vulnerability {id: "CVE-2023-1234", cvss: 9.8})
CREATE (d)-[:HAS_SOFTWARE]->(s)
CREATE (d)-[:HAS_VULNERABILITY]->(v)
```
        
3. **Évolutivité** :
    
    - **Phase 1 (Individu)** : Neo4j local en Docker = suffisant.
    - **Phase 2 (Micro-entreprise)** : Passer à Neo4j **Enterprise** (si besoin de haute disponibilité).
    - **Phase 3 (Production)** : Cluster Neo4j ou **AuraDB** (cloud managé).
4. **Outils complémentaires** :
    
    - **APOC** (librairie Neo4j) : Pour importer des JSON/CSV directement.
    - **Neo4j Bloom** : Visualisation interactive des graphes.
    - **Python Driver** : `pip install neo4j` pour interagir depuis vos scripts.

---

#  2 - Roadmap DB Graph  
### 2.1 - Court Terme  - (POC) 
1. **Conserver Neo4j Docker Community** :
- Simple, suffisant pour un POC. 
- **Action** : Documenter la commande de déploiement dans `02-Architecture/SCHEMA.md`. 
2. **Conserver `.gitignore` + `.private/`** : - Suffisant pour les données locales du POC. - **Action** : Ajouter une section "Sécurité" dans `README.md`. 
3. **Ajouter un script de chargement dans Neo4j** : - Exemple : `load_into_neo4j.py` pour importer `inventory.json` + `cve_data.ttl`. 
### 2.2 - Moyen Terme  - (Micro-Entreprise)** 
1. **Passer à Neo4j AuraDB** (si besoin de cloud) : 
- **Avantage** : Pas de gestion d’infrastructure. 
- **Coût** : Gratuit pour les petits projets. 
2. **Ajouter git-crypt** : 
- **Cas d’usage** : Si vous devez versionner des données sensibles (ex: règles internes). 
- **Action** : Documenter la clé de chiffrement dans un canal sécurisé (ex: Signal). 
2. **Intégrer MITRE ATT&CK** : 
- **Script** : `load_mitre_attack.py` pour charger les tactiques/techniques. 
### 2.3 - Long Terme  - (Production) 
1. **Neo4j Enterprise** : 
- **Avantage** : Haute disponibilité, backup automatique. 
- **Coût** : Payant (mais abordable pour une micro-entreprise). 
2. **Chiffrement des logs** : 
- **Outils** : GPG + stockage dans un bucket S3 chiffré. 
2. **Audit de sécurité** : 
- **Outils** : Neo4j APOC pour des requêtes de sécurité (ex: "Trouver tous les devices vulnérables à une CVE critique"). --- --- 




