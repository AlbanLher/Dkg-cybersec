# 📜 [PREFIXE]-[CODE] — [Titre de la Spécification]

> **Classification** : `TLP:CLEAR` | `TLP:AMBER` | `TLP:RED`
> **Statut** : 🟡 En Révision | 🟢 Approuvé | 🔴 Obsolète
> **Niveau d'Abstraction** : 🟢 SOCLE_TRANSVERSAL | 🔵 USECASE_METIER | 🟡 USECASE_TECHNIQUE
> **Public Cible** : [ex: SOC / Analystes CTI / Architectes Ontologues / Développeurs DevSecOps]
> **Domaine Principal** : `TB` | `QU` | `SH` | `CT` | `IN` | `SE`
> **Matrice de Rattachabilité** : `EXG-[DOM]-[NUM]`, `EXG-[DOM]-[NUM]`

---

## 📖 1. Résumé Executif & Glossaire

### 1.1 Objectif
[Décrire en 2-3 phrases le but de cette spécification et sa valeur pour le projet]

### 1.2 Glossaire Métier & Technique
| Acronyme / Concept | Définition | Contexte DKG |
| :--- | :--- | :--- |
| **Exemple** | Définition courte | Application dans le graphe |

---

## 🎯 2. Périmètre & Rôle de la Spécification

* **Positionnement dans l'Architecture** : [Expliquer à quelle couche du projet s'adresse ce document]
* **Gouvernance & Validation** : [Préciser qui doit valider ce document (ex: Validation Métier SOC ou Validation Dev)]

---

## 📐 3. Spécifications Formelles

<!-- SECTION A ADAPTER SELON LE NIVEAU DE SPECIFICATION -->

### Option A : Si Niveau METIER (SOC / Fonctionnel)
#### 3.1 Scenario Métier & Kill Chain
[Diagramme Mermaid / Schéma ASCII de l'attaque ou du cas d'usage]

#### 3.2 Modélisation Conceptuelle & Traçabilité TLP
[Description des entités métier et requêtes SPARQL d'analyse]

---

### Option B : Si Niveau TECHNIQUE ou SOCLE (Dev / Ontologie)
#### 3.1 Axiomes, Structures RDF & Inférences
[Snippets Turtle, règles SWRL/SHACL, schémas TBox/RBox]

#### 3.2 Directives d'Implémentation Code & Scripts
[Modules Python associés, fonctions de génération]

---

## 📊 4. Matrice d'Exigences & Critères d'Acceptation (`EXG-`)

| Identifiant | Domaine | Intitulé de l'Exigence | Description & Critères d'Acceptation | Mode de Test / Asset |
| :--- | :---: | :--- | :--- | :--- |
| **EXG-XX-01** | `XX` | Nom de l'exigence | Critère formel vérifiable. | Pytest / SPARQL / SHACL |

---

## 🛡️ 5. Outillage, CI/CD & Traçabilité Pytest

* **Scripts de Génération / Exécution** : `03-Application/[script].py`
* **Suite de Test Associée** : `tests/test_[exigence].py`
* **Artefacts Produits** : `[Fichier_Maître.ttl]`

---

## 📚 6. Documents Liés & Références

* **[SPEC-PARENTE]** : [Lien vers la spec de niveau supérieur ou dépendante]