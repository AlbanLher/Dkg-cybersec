# 📦 CONTEXT BUNDLE - DKG-CyberSec & Agent IA SOC
**Phase Active :** Phase 3 - Ingestion CTI Externe, NER & Superposition (Vague 2)  
**Jalon / Vague :** Passage Vague 1 ➔ Vague 2  
**Statut Global :** 🟢 ALL TESTS PASSED (PyTest 100% - 6/6 tests)  
**Horodatage :** Septembre 2026  

---

## 📌 1. Bilan & Mémoire d'Avancement (State Vector)

### 🟢 Acquis Valides (Fin Phase 2 / Vague 1)
* **TBox & RBox Master (`TLP:AMBER`) :** Schéma OWL2/RDFS stabilisé sous `http://dkg.cybersec.org/tbox#`.
* **ABox Master (`TLP:RED`) :** Représentation des actifs, composants, vulnérabilités et règles de marquage sous `http://dkg.cybersec.org/data#`[cite: 14].
* **Validation SHACL sous CWA (`EXG-QUAL-02/03`) :** Zéro violation tolérée. Datatypes des scores CVSS ajustés en `xsd:float` pour respecter strictes formes SHACL.
* **Chaîne CTI Traversante (`SPEC-TECH-UC01`) :** Prédicats normés et validés :
  `Asset -> dkg:hasInstalledComponent -> SoftwareComponent -> dkg:hasVulnerability -> Vulnerability -> dkg:exploitsWeakness -> Weakness -> dkg:hasThreatPattern -> ThreatPattern`.
* **Règles d'Architecture & Qualité :**
  * **SSOT Stricte (`EXG-OR-05`) :** Emploi de `config.py` avec validation dynamique des constantes (`getattr()`).
  * **Double Export & Parité (`EXG-OR-06`) :** Synchronisation contrôlée entre `DIR_SNAPSHOT_P2` et `DIR_MASTER_ABOX` avec vérification `snapshot.resolve() != master.resolve()`.
  * **Qualité de Test :** PyTest 100% fonctionnel sous Python 3.14.

### 🎯 Objectifs Entrants (Phase 3 / Vague 2)
* **Epic 2.1 (Ingestion CTI Structurée - `TLP:CLEAR`) :** Importer et mapper les flux publics NVD, MITRE ATT&CK et CISA KEV sous `02-Donnees/Master_Transversal/TLP_CLEAR_CTI_External/`[cite: 14].
* **Superposition Cross-TLP :** Lier les instances internes `TLP:RED` aux nœuds CTI `TLP:CLEAR` via la TBox commune `TLP:AMBER` sans fuite de confidentialité[cite: 14].
* **Alignement Sémantique (Agent MITM / SKOS) :** Consolidation des taxonomies et schémas[cite: 14].

---

## ⚙️ 2. Extrait SSOT `config.py` (Active Runtime Only)

> **Règle SSOT (`EXG-OR-05`) :** Aucune valeur en dur (nom de fichier, chemin, URI) hors de ce bloc.

```python
from pathlib import Path
from rdflib import Namespace

# --- REPERTOIRES SYSTEME ---
BASE_DIR = Path(__file__).resolve().parent.parent
DIR_DATA = BASE_DIR / "02-Donnees"
DIR_MASTER_TRANSVERSAL = DIR_DATA / "Master_Transversal"

# Phase 1 & 2 Masters
DIR_MASTER_TBOX = DIR_MASTER_TRANSVERSAL / "TLP_AMBER_Schema_TBox"
DIR_MASTER_ABOX = DIR_MASTER_TRANSVERSAL / "TLP_RED_Instances_ABox"
DIR_SNAPSHOT_P2 = DIR_DATA / "Snapshots_Phases" / "Phase_2_ABox"

# Phase 3 Directories (Vague 2)
DIR_CTI_EXTERNAL = DIR_MASTER_TRANSVERSAL / "TLP_CLEAR_CTI_External"
DIR_SNAPSHOT_P3 = DIR_DATA / "Snapshots_Phases" / "Phase_3_CTI"

# --- FICHIERS MASTERS & DOCS ---
TBOX_MASTER_PATH = DIR_MASTER_TBOX / "DKG_TBox_Master.ttl"
SHACL_MASTER_PATH = DIR_MASTER_TBOX / "DKG_SHACL_Master.ttl"
ABOX_MASTER_PATH = DIR_MASTER_ABOX / "DKG_ABox_Master.ttl"
ABOX_MASTER_MD_PATH = DIR_MASTER_ABOX / "DKG_ABox_Master.md"

# --- NAMESPACES RDF VALIDÉS ---
DKG_TBOX = Namespace("[http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)")
DKG_DATA = Namespace("[http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#)")

```


## 📐 3. Contrats d'Interface & Schémas Actifs

- **Datatypes & Normalisation Stricte :**
    
    - `dkg:cvssScore` : `xsd:float` (stricte conformité avec `dkg:CvssScorePropertyShape`).
        
    - Identifiants : Normalisation Regex (`CVE-\d{4}-\d+`, `CWE-\d+`, `CAPEC-\d+`).
        
- **Graphe CTI Canonique Validé :**
    
    ```
    [dkg:Asset] ──(dkg:hasInstalledComponent)──> [dkg:SoftwareComponent]
                                                       │
                                                       └──(dkg:hasVulnerability)──> [dkg:Vulnerability]
                                                                                         │
                                                                                         └──(dkg:exploitsWeakness)──> [dkg:Weakness]
                                                                                                                         │
                                                                                                                         └──(dkg:hasThreatPattern)──> [dkg:ThreatPattern]
    ```
    
- **Isolation du Namespace Data :** Toutes les instances métiers résident exclusivement sous `http://dkg.cybersec.org/data#`.
    

## 📂 4. Code & Modules d'Entrée à Traiter (Phase 3 - Vague 2)

> Fichiers cibles pour la Vague 2 à charger au démarrage du refactoring :

1. `03-Application/Phase3/ingest_phase3_cti.py` (Module d'ingestion CTI Externe `TLP:CLEAR`)[cite: 14]
    
2. `03-Application/Phase3/test_phase3_quality.py` (Suite de recettes PyTest pour la superposition Phase 3)
    

```

---

### 📋 Checklist de Validation Avant Ouverture de Session Phase 3

* [x] **Mémoire de Phase N-1 :** Tests Phase 2 à 100% PASSED enregistrés.
* [x] **Extrait `config.py` :** Inscription uniquement des chemins et constantes runtime utiles à la Phase 3.
* [x] **Contrats de données :** Typage `xsd:float` et prédicat `dkg:exploitsWeakness` ancrés.
* [x] **Trame du Kit :** Format normalisé prêt à être réinjecté en premier message de la nouvelle session.
```