---
jupyter:
  jupytext:
    cell_metadata_filter: -all
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.5
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Neo4j & apoc & n10s
## Installation Neo4j avec Podman (Fedora 44)

### Prérequis
- Podman installé :                                                      **`sudo dnf install podman`**
- SELinux activé (par défaut sur Fedora)


### Commande de Lancement

```bash
podman run -d
   --name neo4j   
   --userns=keep-id   
   -p 7474:7474 
   -p 7687:7687   
   -v /data/neo4j/data:/data:Z   
   -v /data/neo4j/logs:/logs:Z   
   -v /data/neo4j/conf:/var/lib/neo4j/conf:Z   
   -v /data/neo4j/plugins:/var/lib/neo4j/plugins:Z 
   -v /data/SyncData/Projets/T2C_1/Workspace/ImportNeo4J:/var/lib/neo4j/import:z 
   -e NEO4J_PLUGINS='["apoc"]' 
   -e NEO4J_AUTH=neo4j/Acad26DKG!   
   neo4j:latest
```
REX
- ne pas renseigner dans `NEO4J_PLUGINS='["apoc","n10s"]'`  la mise en place du jar n10s dans le repertoire /plugins/ suffit
- pour charger les fichiers dans neo4j ils doisent être placé dans le volume local `/var/lib/neo4j/import'
  et la commande `CALL n10s.rdf.import.fetch("file:///var/lib/neo4j/import/cve_data.ttl", "Turtle");`
- rappel podman :
	- pour naviguer dans le repertoire interne au docker : `podman exec -it neo4j ls -la /var/lib/neo4j/import`
	- copies directes `podman cp /chemin/vers/cve_data.ttl neo4j:/var/lib/neo4j/import/cve_data.ttl`


### Explications

- `--userns=keep-id`                             : Évite les erreurs de permissions (utilise votre UID).
- `:Z`                                                       : Autorise SELinux à accéder aux volumes montés.
- `/data/neo4j/...`                               : Données stockées dans `/data/` (et non `/var/lib/`).
- -e NEO4J_PLUGINS : (
	- apoc:chargement de données  
	- n10s: Le plugin **neosemantics (n10s)** permet d'importer, exporter et manipuler des données RDF (Turtle, JSON-LD, RDF/XML) directement dans Neo4j via Cypher sans passer par un script de conversion intermédiaire.     /!\ ne pas utiliser

### Accès

- **URL** : [http://localhost:7474](http://localhost:7474)
- **Identifiants** : `neo4j` / `motdepasse!`
- **Dossier des données** : `/data/neo4j/`

## Test
APOC : CALL apoc.help("version")
RETURN apoc.version() AS version;

### Dépannage

- **Permissions** : `sudo chcon -Rt container_file_t /data/neo4j`
- **SELinux** : `sudo setenforce 0` (temporaire pour tester)
- **Logs** : `podman logs neo4j`
- **Redémarrage** : `podman restart neo4j`

---
## 🎯 **Pourquoi Cette Solution est Optimale pour Vous**
1. **Données dans `/data/`** : Comme demandé, pas dans `/var/lib/`.
2. **Compatibilité SELinux** : Le `:Z` résout les problèmes de contexte.
3. **Permissions automatiques** : `--userns=keep-id` évite les erreurs `chown`.
4. **Portabilité** : Facile à sauvegarder ou déplacer (`/data/neo4j/` est auto-contenu).






## conf neo4j {APOC, }
Configuration d’APOC pour Neo4j 5.x+
⚠️ Important Depuis **Neo4j 5.x**, les paramètres APOC **doivent** être dans un fichier **`apoc.conf` séparé**. Ne les placez **plus** dans `neo4j.conf` !``

**neo4j.conf**
```
# Paramètres de base
server.memory.pagecache.size=512M
server.default_listen_address=0.0.0.0

# Désactive les restrictions de sécurité pour APOC
dbms.security.procedures.unrestricted=apoc.*,apoc.meta.*

# Autorise le chargement des procédures au démarrage
dbms.security.procedures.allowlist=apoc.*
server.directories.logs=/logs
```



```
# Configuration réseau & mémoire
server.memory.pagecache.size=512M
server.default_listen_address=0.0.0.0

# Autorisations pour APOC et n10s (sans restriction)
dbms.security.procedures.unrestricted=apoc.*,n10s.*

# Liste autorisée (inclut APOC et n10s)
dbms.security.procedures.allowlist=apoc.*,n10s.*
server.directories.logs=/logs
```





**`apoc.conf`**
```
vi /data/neo4j/conf/apoc.conf
```

```
# Configuration APOC pour Neo4j 5.x+
# Autorise les procédures APOC non restreintes
# dbms.security.procedures.unrestricted=apoc.*

# Active l'import de fichiers
apoc.import.file.enabled=true
apoc.import.file.allow_read_from_filesystem=true

# Autorise l'accès au système de fichiers
apoc.export.file.enabled=true
apoc.load.json.enabled=true
apoc.load.csv.enabled=true      
```



## Connexion neo4j  depuis Python
```python
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "Acad26DKG!")

with GraphDatabase.driver(URI, auth=AUTH).session() as session:
    results = session.run("MATCH (n) RETURN n LIMIT 10")
    for record in results:
        print(record["n"])
```


`
```python
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Acad26DKG!"))
```


## Quelques exemple de commande CYPHER
`// Supprimez d'abord les données de test (si nécessaire)
```cypher
MATCH (n) DETACH DELETE n
```



// Chargez l'inventaire 
```cypher
CALL apoc.load.json("file:///import/inventory.json") 
YIELD value UNWIND value.devices AS device 
CREATE (d:Device { id: device.id, type: device.type, ip: device.ip })
FOREACH (sw IN device.software | MERGE (s:Software {name: sw.name, version: sw.version}) CREATE (d)-[:HAS_SOFTWARE]->(s) ) 
RETURN count(d) AS devices_created
```


## liens utiles

[cheatsheets_neo4j](https://github.com/cherkavi/cheat-sheet/blob/master/neo4j.md)
[GitHub_neosemantic(n10s)](https://github.com/neo4j-labs/neosemantics/releases)





# initdata_Gemini
### Script Cypher complet d'initialisation (Phase 0)

Exécutez ces blocs dans l'ordre dans votre **Neo4j Browser** ou via `cypher-shell`.

#### 1. Nettoyage initial et création des contraintes d'unicité
```Cypher
// A. Vider la base de données (si ré-exécution à zéro)
MATCH (n) DETACH DELETE n;

// B. Créer la contrainte d'unicité obligatoire pour n10s (URI RDF)
CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS
FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

// C. Créer les contraintes d'unicité pour les entités métier
CREATE CONSTRAINT unique_device_id IF NOT EXISTS
FOR (d:Device) REQUIRE d.id IS UNIQUE;

CREATE CONSTRAINT unique_software_key IF NOT EXISTS
FOR (s:Software) REQUIRE s.key IS UNIQUE;
```

#### 2. Initialisation n10s & Mappings des Namespaces

Configurons les alias pour que n10s applique directement vos noms de classes et propriétés Cypher (`Device`, `cvssScore`, etc.) sans générer de préfixes `ns0__`.
```cypher
// 1. Contrainte d'unicité (obligatoire)
CREATE CONSTRAINT n10s_unique_uri IF NOT EXISTS
FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

// 2. Initialisation du graphe n10s
CALL n10s.graphconfig.init({ handleVocabUris: "SHORTEN" });

// 3. Déclaration des préfixes personnalisés
CALL n10s.nsprefixes.add("cyber", "http://example.org/cyber-ontology#");
CALL n10s.nsprefixes.add("foaf", "http://xmlns.com/foaf/0.1/");
```

```Cypher
// Initialiser la configuration n10s
CALL n10s.graphconfig.init({ handleVocabUris: "SHORTEN" });

// Ajouter les mappings de namespace
CALL n10s.mapping.addSchema("http://example.org/cyber-ontology#");
CALL n10s.mapping.add("Device", "Device");
CALL n10s.mapping.add("Software", "Software");
CALL n10s.mapping.add("Vulnerability", "Vulnerability");

CALL n10s.mapping.addProperty("http://example.org/cyber-ontology#cvssScore", "cvssScore");
CALL n10s.mapping.addProperty("http://example.org/cyber-ontology#description", "description");
```

#### 3. Ingestion des données RDF (`cve_data.ttl`)

Import des instances de vulnérabilités à partir du fichier Turtle.

```Cypher
CALL n10s.rdf.import.fetch("file:///var/lib/neo4j/import/public/cve_data.ttl", "Turtle");
```

#### 4. Ingestion de l'inventaire JSON via APOC (`inventory.json`)

Import des équipements (`Device`) et composants logiciels (`Software`), puis création des relations `:HAS_SOFTWARE`.

```cypher
CALL apoc.load.json("file:///var/lib/neo4j/import/public/inventory.json") YIELD value
UNWIND value.devices AS devData
WITH devData 
WHERE devData.id IS NOT NULL

// 1. Création / Fusion du Device
MERGE (d:Device {id: devData.id})
ON CREATE SET 
    d.ip = devData.ip,
    d.type = devData.type,
    d.importedAt = datetime()

// 2. Traitement des logiciels
WITH d, coalesce(devData.software, []) AS softwares
UNWIND (CASE WHEN size(softwares) = 0 THEN [null] ELSE softwares END) AS soft

WITH d, soft, (soft.name + "@" + soft.version) AS softKey
WHERE soft IS NOT NULL

// 3. Création du Software et de la relation
MERGE (s:Software {key: softKey})
ON CREATE SET 
    s.name = soft.name,
    s.version = soft.version

MERGE (d)-[:HAS_SOFTWARE]->(s)
RETURN d.id AS DeviceId, count(s) AS SoftwareCount;
```

#### 5. Rapprochement et Création des liens `:HAS_VULNERABILITY`

Liaison déterministe entre les logiciels créés par le JSON et les CVE importées par le fichier Turtle RDF.

Cypher

```
MATCH (s:Software)
MATCH (v:Vulnerability)
// Jointure exacte sur le nom de la vulnérabilité/CVE associée au logiciel
WHERE v.name CONTAINS s.name OR v.uri CONTAINS s.name
MERGE (s)-[r:HAS_VULNERABILITY]->(v)
ON CREATE SET r.linkedAt = datetime();
```



#### 6 - Les 3 noeuds **méta-nœuds de structure et de configuration** 
 
 Ils sont créés automatiquement par l'extension **neosemantics (n10s)** lors de l'initialisation et de l'import de données RDF/Turtle. Ils ne représentent pas des objets de votre domaine métier (comme vos serveurs ou vulnérabilités), mais servent de système d'exploitation sémantique à Neo4j.

##### 1. Le nœud `_GraphConfig`

- **Rôle :** Il s'agit du **registre de configuration globale** du moteur sémantique n10s pour votre base de données.
    
- **Fonction :** Il conserve en mémoire (persistée dans le graphe) la manière dont n10s doit traiter les URIs, les littéraux et la structure lors des imports RDF.
    
- **Ce qu'il contient :** Des propriétés de paramétrage définies lors du `CALL n10s.graphconfig.init(...)`, telles que :
    
    - `handleVocabUris`: définit si les URIs doivent être raccourcies (`SHORTEN`), conservées en entier (`FULL`), ou ignorées (`IGNORE`).
        
    - `handleMultival`: indique comment traiter les propriétés RDF répétées (ex: sous forme de tableau Cypher).
        
    - `keepLangTag`: indique si les balises de langue RDF (ex: `@fr`, `@en`) doivent être conservées.
        

##### 2. Le nœud `_NsPrefDef`

- **Rôle :** Il sert de **table de correspondance (Dictionnaire) pour les préfixes de Namespaces RDF**.
    
- **Fonction :** Il stocke l'association entre une URI d'ontologie complète et le préfixe lisible que vous souhaitez utiliser dans vos labels et propriétés Cypher.
    
- **Ce qu'il contient :** Les paires préfixe/URI enregistrées via `n10s.nsprefixes.add(...)`, par exemple :
    
    - `cyber` $\rightarrow$ `[http://example.org/cyber-ontology#](http://example.org/cyber-ontology#)`
        
    - `foaf` $\rightarrow$ `[http://xmlns.com/foaf/0.1/](http://xmlns.com/foaf/0.1/)`
        
    - `owl` $\rightarrow$ `[http://www.w3.org/2002/07/owl#](http://www.w3.org/2002/07/owl#)`
        
    
    C'est grâce à ce nœud que n10s sait nommer un nœud `cyber__Vulnerability` au lieu d'utiliser un préfixe générique comme `ns0__Vulnerability`.
    

### 3. Le label `Resource`

- **Rôle :** C'est le **label générique racine** appliqué par n10s à **tous les nœuds créés à partir d'un fichier RDF/Turtle**.
    
- **Fonction :** En RDF, toute entité possédant une URI est une "ressource". Neo4j applique ce label pour garantir qu'il existe un identifiant unique universel (`uri`) sur lequel poser des contraintes d'unicité.
    
- **Son utilité en pratique :**
    
    - Il permet à n10s d'exécuter des opérations `MERGE` de manière sûre sur l'ensemble du graphe via la contrainte obligatoire :
        
        `CREATE CONSTRAINT FOR (r:Resource) REQUIRE r.uri IS UNIQUE;`
        
    - Il vous permet de requêter d'un coup l'intégralité des éléments importés depuis le Web Sémantique :
        
        `MATCH (r:Resource) RETURN r;`
        
    - Vos nœuds métiers importés via n10s possèdent donc toujours **au moins deux labels** : le label métier (ex: `cyber__Vulnerability`) et le label technique (`Resource`).
        

##### En résumé

| **Nœud / Label**   | **Type**         | **Utilité**                                          | **Doit-on y toucher ?**                              |
| ------------------ | ---------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| **`_GraphConfig`** | Méta-nœud unique | Stocke les règles d'import n10s.                     | Non (géré par `n10s.graphconfig.*`).                 |
| **`_NsPrefDef`**   | Méta-nœud unique | Dictionnaire des préfixes RDF (`cyber__`, `foaf__`). | Non (géré par `n10s.nsprefixes.*`).                  |
| **`Resource`**     | Label Cypher     | Identifie toute donnée issue d'un import RDF/Turtle. | Oui, sert d'ancrage aux contraintes d'unicité `uri`. |
