### 📋 Intégration dans le Bilan de Phase (Checklist de Clôture)

Pour chaque bilan de fin de phase, le protocole inclura désormais les actions suivantes :

1. **Audit des Artefacts Produits** : Identifier les fichiers `.ttl` générés, leurs sous-dossiers exacts et leurs rôles (TBox, SHACL, ABox, Rules).
    
2. **Mise à Jour Synchronisée de `config.py`** : Inscrire en dur ou mettre à jour les chemins (`Path`), les `Namespace` RDF et les préfixes d'instances.
    
3. **Mise à Jour du Fichier d'Ancrage Contextuel (`Phase_Content.md`)** : Consigner la configuration exacte de `config.py` dans la documentation de cadrage pour réinjecter ce contexte propre aux sessions suivantes.





### Automatiser ces vérifications directement sur votre dépôt GitHub

Pour automatiser ces vérifications directement sur votre dépôt GitHub à chaque `push` ou `pull request`, la meilleure solution est d'utiliser **GitHub Actions**. Cela crée un pipeline d'Intégration Continue (CI) qui exécutera automatiquement vos tests `pytest` sur les vrais fichiers du dépôt.

#### 🛠️ Étape 1 : Créer le Workflow GitHub Actions

Créez un fichier `.github/workflows/ci.yml` à la racine de votre projet local :

YAML

```
name: DKG CyberSec CI Pipeline

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: 1. Récupération du code (Checkout)
      uses: actions/checkout@v4

    - name: 2. Configuration de Python 3.12
      uses: actions/setup-python@v5
      with:
        python-version: "3.12"

    - name: 3. Installation des dépendances
      run: |
        python -m pip install --upgrade pip
        pip install rdflib pyshacl pytest faker anyio langsmith

    - name: 4. Exécution Génération Phase 1
      run: |
        python3 03-Application/Phase1/generate_phase1_socle.py

    - name: 5. Tests Recette Phase 1
      run: |
        pytest -v 03-Application/Phase1/test_phase1_quality.py

    - name: 6. Exécution Génération Phase 2
      run: |
        python3 03-Application/Phase2/generate_phase2_abox.py

    - name: 7. Tests Recette Phase 2
      run: |
        pytest -v 03-Application/Phase2/test_phase2_abox.py
```

#### 🚀 Étape 2 : Activer la vérification sur GitHub

Une fois le fichier créé localement, il vous suffit de le pousser sur GitHub :

Bash

```
git add .github/workflows/ci.yml
git commit -m "ci: ajout de l'intégration continue GitHub Actions"
git push origin main
```

#### 🔍 Étape 3 : Comment nous allons l'utiliser ensemble

Une fois en place, à chaque fois que vous ferez un `git push` :

- **Badge de statut & Logs** : L'onglet **Actions** de votre dépôt GitHub affichera un statut vert `PASSED` ou rouge `FAILED`.
    
- **Diagnostic IA direct** : Si une étape échoue sur GitHub, il vous suffira de me copier-coller le log d'erreur de GitHub Actions ou d'utiliser l'**API GitHub / GitHub CLI (`gh`)** si vous l'avez configurée dans votre terminal :
    

Bash

```
# Vérifier le statut du dernier push directement en CLI
gh run list
gh run view --log-failed
```