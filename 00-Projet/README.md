# Démonstrateur : Dynamique Knowledge Graph  Cybersécurité 

**Objectif** : Créer un Dynamic Knowledge Graph pour la gestion des vulnérabilités et règles de sécurité.
l'aspect dynamique , évoluant d'un usage individuel/familiale qui évolue  puis passe à une micro-entreprise.
L'aspect données publique et privé est un enjeux, mais dans le cadre de ce POC un status "pseudo-privé" sera utilisé pour pouvoir partager l'ensemble ( detail ci dessous)
**Les fonctionnalités  principales :**
- **Détecter** les vulnérabilités (CVE) sur des devices/logiciels.
- **Appliquer** des règles de sécurité adaptées (ex: RGPD, NIS2).
- **Évoluer** dynamiquement avec l’ajout de nouveaux devices ou menaces.

Le Graph de connaissance se base sur une ontologie. Cette Ontologie est au coeur de la structure de connaissance, fera l'objet d'une attention particulière. 

Il est **Important** prendre en compte le lexique comme référence sémantique pour s'assurer d'un compréhension commune ![LEXIQUE]. Il peut évoluer lui aussi.

# Cas d'Usage
Détection et correction de vulnérabilités (CVE, MITRE ATT&CK).
## 📖 Histoire du Use Case
Pour comprendre **pourquoi et comment** ce projet a évolué, lisez :
→ [Histoire d'Alban et la Gestion des Vulnérabilités](01-CasUsage/DESCRIPTION.md)

# Données :
  - Publiques : CVE, MITRE, OWASP.
  - Privées : Inventaire des devices/logiciels (générés).

| Source       | Type     | Format    | Fréquence   | Script Associé          | Exemple                                  |
| ------------ | -------- | --------- | ----------- | ----------------------- | ---------------------------------------- |
| CVE (CIRCL)  | Publique | JSON/RDF  | Quotidienne | `load_cve_feed.py`      | `cve:CVE-2023-1234`                      |
| MITRE ATT&CK | Publique | STIX/JSON | Mensuelle   | À développer            | `mitre:TA0001`                           |
| Inventaire   | Privé    | JSON/RDF  | Ponctuelle  | `generate_inventory.py` | `inventory-reel.json` (dans `.private/`) |

# Outils :

| Outil                     | Usage                          | Lien                                                      | commentaire          |
| ------------------------- | ------------------------------ | --------------------------------------------------------- | -------------------- |
| **Neo4j**                 | Base de données de graphe      | [neo4j.com](https://neo4j.com/)                           | en local pour le POC |
| **RDFLib**                | Manipulation RDF en Python     | [rdflib.readthedocs.io](https://rdflib.readthedocs.io/)   |                      |
| **Sentence Transformers** | Vectorisation                  | [sbert.net](https://www.sbert.net/) ,  `all-MiniLM-L6-v2` |                      |
| **spaCy**                 | NER (Reconnaissance d’entités) | [spacy.io](https://spacy.io/)                             |                      |
| **Faker**                 | Génération de données fictives | [faker.readthedocs.io](https://faker.readthedocs.io/)     |                      |
| Ontologie                 | OWL/TTL + Protégé              |                                                           |                      |
| NER                       | SpaCy (modèle personalisé)     |                                                           |                      |


---
##  Architecture des Ontologies : Publique vs Pseudo-Privée vs Privée

Ce projet utilise **trois niveaux d'ontologies** pour équilibrer **transparence** (POC public) et **confidentialité** (production).
Voici comment les distinguer et les utiliser :
###  1. Ontologie Publique 🌍 (`ontologie-publique.ttl`)

| **Caractéristique** | **Détail**                                                                 |
| ------------------- | -------------------------------------------------------------------------- |
| **Contenu**         | Classes/propriétés **génériques** applicables à tout projet cybersécurité. |
| **Exemples**        | `:Device`, `:Software`, `:Vulnerability`, `:hasSoftware`, `:cvssScore`.    |
| **Accès**           | ✅ **Public** (dans le dépôt GitHub).                                       |
| **Utilisation**     | Base commune pour tous les contributeurs.                                  |
| **Fichier**         | `02-Architecture/ONTOLOGIE/ontologie-publique.ttl`                         |

**→ Pour qui ?** Tous les utilisateurs du dépôt public.

---

###  2. Ontologie Pseudo-Privée  🟡 (`ontologie-pseudo-privee.ttl`)

| **Caractéristique** | **Détail**                                                                                          |
| ------------------- | --------------------------------------------------------------------------------------------------- |
| **Contenu**         | Extensions **spécifiques au POC** (ex: classes/propriétés pour les tests).                          |
| **Exemples**        | `:TestDevice`, `:MockVulnerability`, `:hasMockRule`.                                                |
| **Accès**           | 🔶 **"Pseudo-private"** : Public dans le POC, mais **marqué comme privé** dans la doc.              |
| **Utilisation**     | Permet à **tous les contributeurs** (y compris les agents comme moi) de voir la structure complète. |
| **Fichier**         | `02-Architecture/ONTOLOGIE/ontologie-pseudo-privee.ttl`                                             |
| **Avertissement**   | ⚠️ **Dans un vrai projet, ce fichier serait dans `.private/` et non public.**                       |

**→ Pourquoi cette approche ?**
- **POC** : Tout est public pour faciliter la collaboration.
- **Production** : Ce fichier serait **déplacé dans `.private/`** et **exclu de Git**.
- **Documentation** : On **documente clairement** cette différence pour éviter les malentendus.

**→ Pour qui ?** Contributeurs du POC (y compris les outils d’IA comme moi).

---

###  3. Ontologie Privée 🔒 (`.private/ontologie-privee.ttl`)

| **Caractéristique** | **Détail**                                                                          |
| ------------------- | ----------------------------------------------------------------------------------- |
| **Contenu**         | Extensions **spécifiques à votre entreprise** (ex: règles internes, devices réels). |
| **Exemples**        | `:InternalServer`, `:ComplianceRule`, `:hasEmployee`.                               |
| **Accès**           | ❌ **Privé** (exclu de Git via `.gitignore`).                                        |
| **Utilisation**     | Données **confidentielles** (ex: topologie réseau réelle, règles RGPD/NIS2).        |
| **Fichier**         | `.private/ontologie-privee.ttl` (non versionné dans Git).                           |

**→ Pour qui ?** Uniquement vous et votre équipe interne.

---

### 4. Comment Passer du POC à la Production ?
#### 1 -Déplacez `ontologie-pseudo-privee.ttl` :
```bash
   mv 02-Architecture/ONTOLOGIE/ontologie-pseudo-privee.ttl .private/ontologie-privee.ttl
```
#### 2 - Mettez à jour `.gitignore` : 
**gitignore**
        ```
    .private/
    *.secret
    ```
#### 3 -  Ajoutez l’ontologie privée à `.gitignore` :
```bash
    echo ".private/" >> .gitignore
    git add .gitignore
    git commit -m "chore: Exclure ontologie-privee de Git"
```
    
#### 4 - Documenter le changement
dans `CHANGELOG.md`     
    
```
    ## [v1.0.0] - 2026-08-12
    ### Changed
    - `ontologie-pseudo-privee.ttl` → `.private/ontologie-privee.ttl` (passage en production).
```

---

### 5.   ⚠️   Avertissement pour les Contributeurs

> **⚠️ ATTENTION : L’ontologie "pseudo-privée" (`ontologie-pseudo-privee.ttl`) est publique dans ce POC pour faciliter la collaboration.** **Dans un environnement de production, ce fichier doit être déplacé dans `.private/` et exclu de Git.** **Ne pas utiliser les classes/propriétés de ce fichier pour des données réelles sans les adapter à votre contexte.**



## 🔗 Liens Utiles
- [Dépôt GitHub](https://github.com/alban-lhermine/dkg-cybersec)
- [Neo4j Docs](https://neo4j.com/docs/)
- [MITRE ATT&CK](https://attack.mitre.org/)

