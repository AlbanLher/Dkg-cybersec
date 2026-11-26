---

#### B. Extrait du Template Épuré à Transmettre au LLM (Message 1)

Transmettez ce bloc sous le nom `template_spec.md` lors de l'initialisation de la nouvelle discussion :


<!-- Règle 8 (01.1 §7) : reference = ID mécanique IMMABLE (slug = aide-mémoire non
     normatif, renommage interdit : abroger + reposer) ; titre = libellé fonctionnel
     officiel ≤ 60 caractères (le sens vit ICI, pas dans la référence) ; description =
     l'objet en 1-2 phrases (pourquoi, périmètre — jamais le comment).
     Le champ statut est un cache : l'affichage fait foi par lookup dans la Roadmap. -->
---
type: spec
reference: "SPC-[MET|TEC|FWK]-P[phase]-[slug-court]_01"
revision: 1
titre: "Libellé fonctionnel officiel (≤ 60 caractères)"
titre_court: slug_court
description: "L'objet en 1-2 phrases : pourquoi, périmètre"
phase_code: P1
phase_nom: "Nom de la Phase"
statut: "📝 DRAFT"
portee: TRANSVERSAL
public_vise:
  - "Architectes Ontologues"
  - "Développeurs DevSecOps"
exigences:
  - id: EXG-FWK-P1-MNEMO_1        # format : EXG-{MET|TEC|FWK}-P{phase}-{MNÉMO}_{n}
    domaine: SE
    core: true
    spec_source: "SPC-FWK-P1-…_01"  # jointure sur la référence (immuable)
    titre: "Titre de l'exigence"
    critere: "Critère formel vérifiable"
    test: "PyTest / SHACL"
    recette: auto                   # auto | visuelle | inspection | prevue
---


# 📜 [Titre Complet de la Spécification]

> **SSOT** : le frontmatter `exigences` est un cache de confort — l'index machine
> unique est `01-Principes_Spécifications/registry_exigences.json` ; en cas d'écart,
> le registre fait foi (toute EXG nouvelle y entre avec son `recette`).

## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif
[Décrire en 2-3 phrases le but de cette spécification et sa valeur pour le projet]

### 1.2 Glossaire Métier & Technique

| Acronyme / Concept | Définition | Contexte DKG |
| :--- | :--- | :--- |
| **Exemple** | Définition courte | Application dans le graphe |

## 🏗️ 2. Spécification & Modélisation
```mermaid
graph TD
    A[Composant A] --> B[Composant B]
```
## 📐 3. Spécifications Formelles
### 3.1 Axiomes, Structures RDF & Inférences (ou Scénario Métier)
[Description formelle, snippets Turtle, règles SWRL/SHACL ou diagramme d'attaque]

### 3.2 Directives d'Implémentation Code & Scripts
[Modules Python associés, fonctions de génération, contraintes bas niveau]

## 📊 4. Matrice d'Exigences & Critères d'Acceptation (EXG-)
Identifiant	Domaine	Intitulé de l'Exigence	Description & Critères d'Acceptation	Mode de Test / Asset
EXG-SE-01	SE	Nom de l'exigence	Critère formel vérifiable.	Pytest / SPARQL / SHACL

## 🛡️ 5. Outillage, CI/CD & Traçabilité Pytest
Scripts de Génération / Exécution : 03-Application/[script].py

Suite de Test Associée : tests/test_[exigence].py

Artefacts Produits : [Fichier_Maître.ttl]

## 📚 6. Documents Liés & Références
[SPEC-PARENTE] : [Lien vers la spec de niveau supérieur ou dépendante]