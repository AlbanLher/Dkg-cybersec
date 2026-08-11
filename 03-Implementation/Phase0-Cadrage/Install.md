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

# Installation Neo4j avec Podman (Fedora 44)

### Prérequis
- Podman installé : `sudo dnf install podman`
- SELinux activé (par défaut sur Fedora)


### Commande de Lancement
```bash
mkdir -p /data/neo4j/{data,logs,conf}
podman run -d \
  --name neo4j \
  --userns=keep-id \
  -p 7474:7474 -p 7687:7687 \
  -v /data/neo4j/data:/data\:Z \
  -v /data/neo4j/logs:/logs\:Z \
  -v /data/neo4j/conf:/var/lib/neo4j/conf\:Z \
  -e NEO4J_AUTH=neo4j/Acad26DKG! \
  neo4j\:latest
```

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
   -e NEO4J_PLUGINS='["apoc","n10s"]]' 
   -e NEO4J_AUTH=neo4j/Acad26DKG!   
   neo4j:latest
```

f02fcd2414af958313eda1e618f471ce499ba574f5f27b9c87ee9ca42cb82fe8

### Explications

- `--userns=keep-id` : Évite les erreurs de permissions (utilise votre UID).
- `:Z` : Autorise SELinux à accéder aux volumes montés.
- `/data/neo4j/...` : Données stockées dans `/data/` (et non `/var/lib/`).
- -e NEO4J_PLUGINS : (
	- apoc:chargement de données  
	- n10s: Le plugin **neosemantics (n10s)** permet d'importer, exporter et manipuler des données RDF (Turtle, JSON-LD, RDF/XML) directement dans Neo4j via Cypher sans passer par un script de conversion intermédiaire.

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






# conf neo4j {APOC, }
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










# Connexion neo4j  depuis Python
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
