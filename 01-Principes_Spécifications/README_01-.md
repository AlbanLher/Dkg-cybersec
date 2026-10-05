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

Ce repertoire rassemble les Spécifications considérées utiles pour le Framework mais aussi celles complétée pour la mise en application sur le cas d'usage Cyber SOC, respectivement dans les sous-répertoires : 
- **`./Specification_Framework/`**  et
- **`./Specification_UseCase/`**

A noter que les spécifications UseCase ne font que compléter les spécification UseCase.

📐 RÈGLE STRICTE DE NOMMAGE ET NUMÉROTATION DES SPÉCIFICATIONS (01-Principes_Spécifications/) :

1. ARBORESCENCE OBLIGATOIRE :
   - 01-Principes_Spécifications/TRANSVERSAL/ (Socles, TBox, SHACL, Règlements)
   - 01-Principes_Spécifications/USECASE_METIER/ (Vision fonctionnelle SOC / Métier)
   - 01-Principes_Spécifications/USECASE_TECHNIQUE/ (Implémentations, APIs, Agents)

2. RÈGLES DE NUMÉROTATION & MAPPING PHASE/UC :
   - Fichiers Transversaux : SPEC-SOCLE-XX_<Libellé>.md
   - Fichiers Métiers : SPEC-METIER-UCXX_<Libellé>.md (UC = Use Case Métier)
   - Fichiers Techniques de Phase : SPEC-TECH-PXX_<Libellé>.md (PXX = Numéro de Phase active)
   - En cas d'écart entre le numéro du Cas d'Usage Métier (UC) et le numéro de Phase (P), le prefixe 'PXX' prévaut pour identifier la Phase de livraison dans USECASE_TECHNIQUE/.

1. INTERDICTION : Aucun fichier markdown de spécification ne doit être créé à la racine de 01-Principes_Spécifications/.




```python
import os
import json
import yaml

VAULT_PATH = "."  # Chemin vers votre vault Obsidian
OUTPUT_JSON = "registry_exigences.json"

registry = {
    "metadata": {
        "description": "Registre centralisé des exigences DKG-CyberSec",
        "spec_driven_version": "2.0"
    },
    "exigences": []
}

# Parcours de l'arborescence du vault
for root, dirs, files in os.walk(VAULT_PATH):
    # Ignorer les dossiers cachés comme .git ou .obsidian
    if ".obsidian" in root or ".git" in root:
        continue
        
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # Extraction du Frontmatter YAML
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        fm = yaml.safe_load(parts[1])
                        if isinstance(fm, dict) and fm.get("type") == "spec":
                            spec_ref = fm.get("reference", file)
                            spec_phase = fm.get("phase_code", "P1")
                            
                            for ex in fm.get("exigences", []):
                                registry["exigences"].append({
                                    "id": ex.get("id"),
                                    "domaine": ex.get("domaine"),
                                    "core": ex.get("core", True),
                                    "phase": spec_phase,
                                    "spec_source": spec_ref,
                                    "titre": ex.get("titre"),
                                    "critere": ex.get("critere"),
                                    "test": ex.get("test")
                                })
            except Exception as e:
                print(f"Erreur de lecture sur {file_path}: {e}")

# Sauvegarde du registre global
with open(OUTPUT_JSON, "w", encoding="utf-8") as out:
    json.dump(registry, out, indent=2, ensure_ascii=False)

print(f"Succès : {len(registry['exigences'])} exigences indexées dans {OUTPUT_JSON}")
```


