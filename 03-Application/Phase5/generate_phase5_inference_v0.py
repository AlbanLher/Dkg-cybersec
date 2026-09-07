#!/usr/bin/env python3
"""
generate_phase5_inference.py
Pipeline d'Inférence Sémantique (Wave 3) & Validation SHACL.
Conforme aux exigences d'exécution Air-Gapped / Offline.
"""

import sys
import shutil
from pathlib import Path
from rdflib import Graph
import pyshacl

# Ancrage dynamique du dossier 03-Application dans le PYTHONPATH
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from config import (
    TBOX_MASTER_PATH,
    ABOX_RED_PATH,
    ABOX_CTI_PATH,
    RULES_MASTER_PATH,
    ABOX_INFERED_PATH,
    DIR_SNAPSHOT_P5,
    DIR_INFERED_RED,
    DOC_INFERED_MD_PATH,
    DKG_TBOX,
    DKG_DATA,
    DKG_CTI
)

def run_pipeline():
    print("======================================================================")
    print("🛡️ DKG-CyberSec — Moteur d'Inférence Sémantique & SHACL (Phase 5)")
    print("======================================================================")

    # 1. Chargement des Graphes RDF (TBox, ABox Interne, ABox CTI, Règles)
    full_graph = Graph()
    
    paths_to_load = [
        ("TBox Master (TLP:AMBER)", TBOX_MASTER_PATH),
        ("ABox Interne (TLP:RED)", ABOX_RED_PATH),
        ("ABox CTI Externe (TLP:CLEAR)", ABOX_CTI_PATH),
        ("Règles Master (TLP:AMBER)", RULES_MASTER_PATH)
    ]

    for label, path in paths_to_load:
        p = Path(path)
        if p.exists():
            try:
                full_graph.parse(str(p), format="ttl")
                print(f"[✓] Chargé {label} : {len(full_graph)} triples")
            except Exception as e:
                print(f"[❌] ERREUR DE SYNTAXE RDF/Turtle dans {label} ({p}) : {e}")
                sys.exit(1)
        else:
            print(f"[!] Fichier manquant ({label}) : {p}")

    initial_triple_count = len(full_graph)
    print(f"[*] Total Triples Initiaux : {initial_triple_count}")

    # 2. Exécution des Règles d'Inférence (pySHACL Advanced / SPARQL CONSTRUCT)
    print("[+] Exécution du moteur d'inférence SHACL Advanced...")
    shapes_graph = Graph()
    if Path(RULES_MASTER_PATH).exists():
        shapes_graph.parse(str(RULES_MASTER_PATH), format="ttl")

    conforms, report_graph, report_text = pyshacl.validate(
        data_graph=full_graph,
        shacl_graph=shapes_graph,
        advanced=True,
        inplace=True
    )

    inferred_triple_count = len(full_graph) - initial_triple_count
    print(f"[✓] Inférences exécutées. Triples déduits : {inferred_triple_count}")

    # 3. Sauvegarde & Synchronisation du Graphe Enrichi (ABox Infered TLP:RED)
    DIR_SNAPSHOT_P5.mkdir(parents=True, exist_ok=True)
    snapshot_ttl_path = DIR_SNAPSHOT_P5 / ABOX_INFERED_PATH.name
    full_graph.serialize(destination=str(snapshot_ttl_path), format="ttl")
    print(f"[📦] Snapshot Turtle généré : {snapshot_ttl_path}")

    DIR_INFERED_RED.mkdir(parents=True, exist_ok=True)
    if snapshot_ttl_path.resolve() != ABOX_INFERED_PATH.resolve():
        shutil.copy(snapshot_ttl_path, ABOX_INFERED_PATH)
        print(f"[✅] Graphe Master synchronisé dans : {ABOX_INFERED_PATH}")

    # 4. Validation SHACL Finale de Conformité
    print("[+] Validation SHACL finale sur le graphe unifié...")
    shacl_shapes = Graph()
    if Path(TBOX_MASTER_PATH).exists():
        shacl_shapes.parse(str(TBOX_MASTER_PATH), format="ttl")

    final_conforms, _, final_report = pyshacl.validate(
        data_graph=full_graph,
        shacl_graph=shacl_shapes,
        advanced=False
    )

    print(f"[*] Conformité SHACL globale : {'CONFORME (PASS)' if final_conforms else 'NON CONFORME (FAIL)'}")

    # 5. Définition explicite des chemins Markdown & Génération du rapport
    snapshot_md_path = DIR_SNAPSHOT_P5 / DOC_INFERED_MD_PATH.name
    master_md_path = DOC_INFERED_MD_PATH

    md_content = f"""# 📑 Livrable Phase 5 - Inférence Sémantique & Unification du Graphe

**Classification :** `TLP:RED` (Confidentiel SI / Usage Interne)  
**Moteur d'Inférence :** pySHACL Advanced (Rules Engine)  
**Statut de Conformité SHACL :** {"✅ CONFORME (PASS)" if final_conforms else "❌ NON CONFORME (FAIL)"}

---

## 📖 Glossaire & Table des Acronymes Métier

| Acronyme | Définition Complète | Contextualisation DKG |
| :--- | :--- | :--- |
| **APT** | Advanced Persistent Threat | Groupe d'attaquants qualifiés (`dkg:ThreatActor`). |
| **RBox** | Relationship Box | Composante d'ontologie définissant les règles d'inférence et propriétés de relations. |
| **CTI** | Cyber Threat Intelligence | Renseignements structurés externes (`TLP:CLEAR`). |
| **SHACL** | Shapes Constraint Language | Langage W3C de validation de contraintes et de règles d'inférence. |
| **TLP** | Traffic Light Protocol | Protocole de partage (`TLP:CLEAR`, `TLP:AMBER`, `TLP:RED`). |

---

## 🔄 Flux d'Inférence Sémantique Cross-Domain

```mermaid
flowchart TD
    subgraph TLP_AMBER [Périmètre Socle - TLP:AMBER]
        TBOX[dkg_tbox.ttl]
        RULES[DKG_Rules_Master.ttl]
    end

    subgraph Inputs [Graphes Sources]
        ABOX_RED[ABox Interne SI - TLP:RED]
        ABOX_CTI[ABox CTI Externe - TLP:CLEAR]
    end

    subgraph Engine [Phase 5 - Moteur pySHACL Advanced]
        INF[Inference Engine]
    end

    subgraph Output [Master Inferred - TLP:RED]
        GRAPH_INF[DKG_ABox_Infered.ttl]
    end

    TBOX --> INF
    RULES --> INF
    ABOX_RED --> INF
    ABOX_CTI --> INF
    INF -->|SPARQL CONSTRUCT / Rules| GRAPH_INF
```

Métrique,Valeur
Triples Initiaux,{initial_triple_count}
Triples Déduits (Règles),+{inferred_triple_count}
Total Triples Enrichis,{len(full_graph)}

🔍 Rapport Détaillé SHACL
{final_report}


Document généré automatiquement post-pipeline Phase 5.
"""


    # Écriture dans le Snapshot Phase 5
    with open(snapshot_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[📦] Documentation Snapshot générée : {snapshot_md_path}")

    # Synchronisation vers Master TLP:RED
    master_md_path.parent.mkdir(parents=True, exist_ok=True)
    if snapshot_md_path.resolve() != master_md_path.resolve():
        shutil.copy(snapshot_md_path, master_md_path)
        print(f"[✅] Documentation Master synchronisée : {master_md_path}")

if __name__ == "__main__":
    run_pipeline()

