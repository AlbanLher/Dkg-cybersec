#!/usr/bin/env python3
"""
run_pipeline.py
Script d'orchestration globale du pipeline DKG-CyberSec (Phases 1 à 6).
Exécute séquentiellement les générateurs de données et la suite Pytest exhaustive.
"""

import subprocess
import sys
from pathlib import Path

# Résolution de la racine du projet
ROOT_DIR = Path(__file__).resolve().parent.parent
APP_DIR = ROOT_DIR / "03-Application"

def run_step(name: str, command: list[str]):
    """Exécute une étape du pipeline avec gestion des erreurs."""
    print(f"\n==================================================")
    print(f"🚀 [PIPELINE] Étape en cours : {name}")
    print(f"==================================================\n")
    
    result = subprocess.run(command, cwd=str(ROOT_DIR))
    if result.returncode != 0:
        print(f"\n❌ [ERREUR] L'étape '{name}' a échoué (Code : {result.returncode}).")
        sys.exit(result.returncode)
    print(f"\n✅ [SUCCÈS] Étape '{name}' validée avec succès.\n")

def main():
    # 1. Création de l'arborescence cible
    dirs_to_create = [
        ROOT_DIR / "02-Donnees/Snapshots_Phases/Phase1_Socle",
        ROOT_DIR / "02-Donnees/Snapshots_Phases/Phase2_ABox",
        ROOT_DIR / "02-Donnees/Snapshots_Phases/Phase5_Inference",
        ROOT_DIR / "02-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox",
        ROOT_DIR / "02-Donnees/Master_Transversal/TLP_RED_Instances_ABox",
    ]
    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
    print("📁 Arborescence des dossiers de données vérifiée.")

    # 2. Génération Phase 1 (Socle TBox & SHACL)
    run_step(
        "Génération Phase 1 (Socle)",
        [sys.executable, "03-Application/Phase1/generate_phase1_socle.py"]
    )

    # 3. Génération Phase 2 (ABox Interne)
    run_step(
        "Génération Phase 2 (ABox Interne)",
        [sys.executable, "03-Application/Phase2/generate_phase2_abox.py"]
    )

    # 4. Exécution de la suite Pytest globale (Phases 1 à 6)
    run_step(
        "Exécution de la suite de tests Pytest (V1 à V6)",
        [
            sys.executable, "-m", "pytest", "-v",
            "03-Application/Test/",
         #   "03-Application/Tests/",
            "--junitxml=test-results.xml"
        ]
    )

    print("🎉 Pipeline DKG-CyberSec exécuté de bout en bout avec succès !")

if __name__ == "__main__":
    main()
