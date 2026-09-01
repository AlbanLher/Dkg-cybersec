

## ⚙️ Le Rôle Pivot de `03-Application/config.py`

Le fichier `config.py` est l'incarnation technique du **Seiton (Ranger)** et du **Seiketsu (Standardiser)** :

1. **Garant du Single Source of Truth (SSOT) :** Il empêche la "fricassée de chemins" entre les sous-dossiers `Phase1`, `Phase2`, `Phase2.5`, etc.
    
2. **Pivot des Inter-Vagues :** À chaque nouvelle vague (ex: passage de la Wave 1 à la Wave 2), c'est dans `config.py` que l'on déclare les nouveaux répertoires de données externes (`TLP_CLEAR_CTI_External/`) avant même d'écrire la moindre ligne de code de génération.
    
3. **Passeport CI/CD :** Les scripts de test, de génération et d'exportation consomment exactement les mêmes constantes, garantissant que l'environnement local et le runner GitHub Actions fonctionnent à l'identique.



### 1. Centraliser les Constantes dans un Module Unique
le fichier **`03-Application/config.py`** a été mis en place pour centraliser les Constantes dans un Module Unique, au lieu de redéfinir les chemins (`Path`), les URIs, et les espaces de noms (`Namespace`) dans chaque script de génération et de test (REX pb d'attention)

**Bénéfice :** Si la structure des dossiers évolue plus tard, un seul fichier est à modifier. Tous vos scripts de génération et vos suites `pytest` importeront directement `TBOX_MASTER_PATH` et `ABOX_MASTER_PATH`.

### 2. Fournir un "Filtre d'Attention" (Context Prompting / Anchoring)

À chaque nouvelle phase ou demande de dev, donnez-moi en amorce le **"Contrat d'Interface"** ou un mini-résumé technique des artefacts réels générés (par exemple, un extrait de l'arborescence réelle exécutée et le `config.py`).

Par exemple, au lieu de faire référence à un document général :

> _"Voici `config.py` et les classes/propriétés instanciées en Phase 1. Génère l'ABox Phase 2 sur cette base."_

Cela force l'attention de l'IA à se focaliser à 100% sur le code exécuté réel plutôt que sur une spécification théorique.

### 3. Automatiser les Pipeline & Tests d'Intégration Continue (CI)

Pour s'assurer que les phases s'enchaînent sans rupture de bout en bout, nous pouvons créer un script maître de pipeline global `03-Application/run_pipeline.py` :

```python
#!/usr/bin/env python3
"""
run_pipeline.py - Orchestrateur d'exécution et de validation CI.
"""
import subprocess
import sys

def run_step(title, command):
    print(f"\n[PIPELINE] === {title} ===")
    res = subprocess.run(command, shell=True)
    if res.returncode != 0:
        print(f"❌ Échec lors de l'étape : {title}")
        sys.exit(res.returncode)

if __name__ == "__main__":
    run_step("Phase 1 - Génération Socle TBox & SHACL", "python3 03-Application/Phase1/generate_phase1_socle.py")
    run_step("Phase 1 - Test Recette Quality TBox", "pytest -v 03-Application/Phase1/test_phase1_quality.py")
    run_step("Phase 2 - Génération ABox Master", "python3 03-Application/Phase2/generate_phase2_abox.py")
    run_step("Phase 2 - Test Recette Quality ABox", "pytest -v 03-Application/Phase2/test_phase2_abox.py")
    print("\n✅ Pipeline exécuté avec succès de bout en bout !")
```