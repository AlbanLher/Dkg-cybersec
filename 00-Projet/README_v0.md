# Démonstrateur : Dynamique Knowledge Graph  Cybersécurité 

**Objectif** : Créer un Assistant IA utilisant un "Dynamic Knowledge Graph" dans le domaine de la cybersécurité avec en particulier la gestion des vulnérabilités et les règles de sécurité.
l'aspect dynamique , évoluant d'un usage individuel/familiale qui évolue  puis passe à une micro-entreprise.
L'aspect données publique et privé est un enjeux, mais dans le cadre de ce POC un status "pseudo-privé" sera utilisé pour pouvoir partager l'ensemble ( detail ci dessous)
**Les fonctionnalités  principales :**
- **Détecter** les vulnérabilités (CVE) sur des devices/logiciels.
- **Appliquer** des règles de sécurité adaptées (ex: RGPD, NIS2).
- **Évoluer** dynamiquement avec l’ajout de nouveaux devices ou menaces.

Le Graph de connaissance se base sur une ontologie. Cette Ontologie est au cœur de la structure de connaissance, fera l'objet d'une attention particulière. 

Il est **Important** prendre en compte le lexique comme référence sémantique pour s'assurer d'une compréhension commune [Lexique](00-Projet/LEXIQUE.md) .

Il peut évoluer lui aussi.

# Le Cas d'Usage est avant tout une histoire 

Il s'agit d'un assistant IA dans une entreprise qui capitalise le savoir faire de l'entreprise et assiste les employés a bien comprendre et appliquer les processus internes et externe et a vérifier l'état de conformité aux régles qui définissent ce savoir faire.
.
Le domaine d'application sera pour ce POC la cyber-sécurité.

L'ensemble de ces connaissances évolue en permanence , on découvre des vulnérabilités tous les jours, par ailleurs dans les entreprises l'innovation, la prise en compte des retour d'expérience et enfin les réorganisation, conduisent a adapter et faire évoluer le savoir faire et soin contexte.

La notion de Knowledge Graph nous conduit a développer la notion d'ontologie qui sera développée dans le paragraphe 02-Architecture ainsi que l'outil de Graph selectionné ici neo4j pour sa flexibilité (mais les principes peuvent être transposé aux autres outils)

Pour illustrer l'aspect dynamique on commence par un cas d'usage en 3 phases.
L'enjeu étant de montrer qu'entre ces phases, des migrations permette de faire évoluer le Graph { ontologie + data}

nota : l'enrichissement de connaissance, se fait souvent en ajoutant de nouvelles règles qui parfois contredisent des règles existantes mais sont cloisonnées à un nouveau contexte particulier, qui lui est décrit dans une version évoluée de l'ontologie.

L'enjeux est de discerner ce contexte ( NLP, classification, NER, vectorisation ) Différentes 

**Phase 0 :**  "Un PC, Une Règle Simple"
**Phase 1 :**  "La Micro-Entreprise – "Des Règles et des Serveurs"
**Phase 2 :**  "Le Client Externe – "La Contradiction Apparente"


ce cas d'usage sert à définir une architecture développé dans le chapitre 02 et sa mise en place dans le chapitre 03
Les cas d'usages peuvent être tres nombreux et les choix d'architecture pourront varier en fonction. L'objectif de ce POC est de développer des principe qui puissent être appliqué à d'autres cas d'usage, qui peuvent ou conserver l'architecture proposée ( qui se veut assez évolutive) ou se baser sur des choix différent pour s'adapter à des environnement existants

Pour approfondir la compréhension du cas d'usage, lisez → [Histoire d'Alban et la Gestion des Vulnérabilités](01-CasUsage/DESCRIPTION.md)

### 📊 Évolution du Graphe (A confirmer)

| Phase  | Nœuds | Relations | Nouvelles Classes                | Nouvelles Propriétés             |
| ------ | ----- | --------- | -------------------------------- | -------------------------------- |
| Phase0 | 10    | 15        | Device, Software, Vulnerability  | hasSoftware, hasVulnerability    |
| Phase1 | 25    | 40        | +InternalServer, +ComplianceRule | +hasComplianceStatus, +appliesTo |
| Phase2 | ?     | ?         | +NetworkZone, +ThreatActor       | +inZone, +targets                |



---
# Confidentialité - Données privées - POC versus PROD

Le principe de DKG qui rassemble des savoir faire et par nature confidentiel, quand bien même de nombreuse données sont communes et publiques.

Le POC est un démonstrateur voulu accessible (dépot publique)

Nous avons fait le choix d'utiliser l'étiquette "pseudo-privé"  pour présenter les données  de façon publique, qui seraient privées et donc cachées dans un cas de Production.
Une note sur l'adaptation POC -> PROD permet d'illustrer les adaptation qui seraient nécessaires)

# Hypothèses materiel

Les ressources disponibles pour ce projet sont : 
- PC ACER ASPIRE A515-40 16Go
- Des ressource cloud GPU  si besoin pour le fine tuning de modèle.

L'objectif de départ est de pouvoir faire les inférence sur ce PC local.

# Données :
  - Publiques : CVE, MITRE, OWASP.
  - Pseudo-Privées : Issue de la créativité se basant sur le cas d'usage (générées).

| Source       | Type     | Format    | Fréquence   | Script Associé          | Exemple                                  |
| ------------ | -------- | --------- | ----------- | ----------------------- | ---------------------------------------- |
| CVE (CIRCL)  | Publique | JSON/RDF  | Quotidienne | `load_cve_feed.py`      | `cve:CVE-2023-1234`                      |
| MITRE ATT&CK | Publique | STIX/JSON | Mensuelle   | À développer            | `mitre:TA0001`                           |
| Inventaire   | Privé    | JSON/RDF  | Ponctuelle  | `generate_inventory.py` | `inventory-reel.json` (dans `.private/`) |


# Structure documentaire  [accessible sous ce lien](00-Projet/STRUCTURE_DOCUMENTAIRE.md)

### Contrainte prise en compte pour établir la structure
- Logique projet
- Articulation des données avec Neo4j  et le volume import monté dans le docker

### Solution choisie : 
avoir un répertoire data dans l'arborescence qui correspondra au volume monté sur le docker Neo4j.
sur ce répertoire data viendront pointer par lien symbolique les docnnées des phase listée dans le chapitre 003 Implémentationb

```bash
# 1. Mettez à jour les liens
cd data/current
rm -rf public pseudo-private
ln -s ../Phase1-Infrastructure/public public
ln -s ../Phase1-Infrastructure/pseudo-private pseudo-private

# 2. Redémarrez Neo4j
podman restart neo4j

# 3. Exécutez la migration (via Neo4j Browser)
CALL apoc.cypher.runFile('file:///to_phase1.cypher')
```




###  **Automatisez avec un script** (`update_current_phase.sh`) :
```bash
#!/bin/bash
# Usage: ./update_current_phase.sh Phase1-Infrastructure
TARGET_PHASE=\$1
cd data/current
rm -rf public pseudo-private
ln -s ../\$TARGET_PHASE/public public
ln -s ../\$TARGET_PHASE/pseudo-private pseudo-private
echo "✅ data/current/ pointe maintenant vers \$TARGET_PHASE"
```

### 🔄 Changer de Phase
```bash
./update_current_phase.sh Phase1-Infrastructure
podman restart neo4j
```


###  Exécutez la migration (via Neo4j Browser)
```cypher
CALL apoc.cypher.runFile('file:///to_phase1.cypher')`
```


### 📌 **Avantages de Cette Structure**

|Bénéfice|Détail|
|---|---|
|**Évolution claire**|Chaque phase est **isolée** et **versionnable**.|
|**Migrations explicites**|Les changements du graphe sont **documentés** dans `migrations/`.|
|**Données centralisées**|`data/` contient **toutes les versions** des données.|
|**Flexibilité**|Passez d’une phase à l’autre en **modifiant un lien**.|
|**Cohérence Docker**|Un **seul volume** (`data/current/`) pour Neo4j.|
|**Nettoyage automatique**|Les anciens liens sont **supprimés** avant les nouveaux.|


# 🔗 Liens Utiles
- [Dépôt GitHub](https://github.com/alban-lhermine/dkg-cybersec)
- [Neo4j Docs](https://neo4j.com/docs/)
- [MITRE ATT&CK](https://attack.mitre.org/)

