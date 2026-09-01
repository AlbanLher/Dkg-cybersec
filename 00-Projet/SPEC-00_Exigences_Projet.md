# 📜 SPEC-00 — Cadre Global de Gouvernance & Matrice des Exigences Projet

> **Classification** : `TLP:AMBER`  
> **Statut** : 🟢 Approuvé  
> **Domaine** : Meta-Framework & Gouvernance DKG  
> **Matrice de Rattachabilité** : `EXG-TBOX-*`, `EXG-QUAL-*`, `EXG-SEC-*`, `EXG-ORG-*`, `EXG-SHACL-*`

---

## 📖 1. Glossaire des Acronymes

* **DKG** : Dynamic Knowledge Graph (Graphe de connaissances dynamique)
* **SDD** : Spec-Driven Development (Développement piloté par les spécifications formelles)
* **CI/CD** : Continuous Integration / Continuous Deployment (Intégration et déploiement continus)
* **TLP** : Traffic Light Protocol (Standard de classification de la sensibilité des données)
* **CWA** : Closed World Assumption (Hypothèse du monde fermé pour la validation SHACL)

---

## 🎯 2. Objet & Portée

La présente spécification constitue le **document cadre (spécification mère)** du projet DKG-CyberSec. Elle fixe :
1. Les exigences fondamentales de gouvernance, de qualité et de sécurité applicables à l'ensemble du dépôt.
2. Les critères d'acceptabilité pour la validation automatisée (Pytest, SHACL, parité Master/Snapshot).
3. Le sas de qualification (**Gatekeeper**) régissant la transition entre les différentes phases du projet.

---

## 📐 3. Spécifications Formelles & Règles Métier

### 3.1 Principes Directeurs
* **Spec-Driven First** `[EXG-ORG-01]` : Aucun code, script ou fichier ontologique ne peut être produit ou modifié sans une spécification formelle préalable (`SPEC-XX` ou `SPEC-UC-XX`).
* **Traçabilité par Phase** `[EXG-ORG-03]` : Chaque phase dispose de son dossier dédié dans `00-Projet/` avec traçabilité complète à travers 4 briques (Framework, Instanciation, Data, Scripts).
* **Parité Binaire Master/Snapshot** `[EXG-ORG-02]` : Les données maîtres dans `02-Donnees/Master_Transversal/` doivent posséder une empreinte binaire identique aux snapshots figés dans `02-Donnees/Snapshots_Phases/`.
* **Gatekeeper & Checklist** `[EXG-ORG-04]` : L'ouverture d'une Phase $N$ est conditionnée par la validation de `00-Projet/Cadrage_Checklist.md` et le contrôle de clôture de la Phase $N-1$.

### 3.2 Normes Métriques & Qualité
* **Namespace & Séparateur** `[EXG-TBOX-01]` : Espace de noms racine unique avec séparateur `#` pour la TBox.
* **Typage OWL Strict** `[EXG-TBOX-02]` : Typage formel `owl:Class`, `owl:ObjectProperty`, `owl:DatatypeProperty`.
* **Domaine & Portée Explicites** `[EXG-TBOX-03]` : Interdiction de déclarer une propriété sans `rdfs:domain` ni `rdfs:range`.
* **Inverses RBox** `[EXG-TBOX-04]` : Déclaration obligatoire de la propriété inverse via `owl:inverseOf`.
* **Couche Lexicale SKOS** `[EXG-TBOX-05]` : Présence de `skos:prefLabel` (FR/EN) et `skos:definition`.
* **Couverture SHACL** `[EXG-QUAL-01]` / `[EXG-SHACL-01]` : Contraintes SHACL (`NodeShape`, `PropertyShape`) obligatoires.
* **Conformité des Données** `[EXG-QUAL-02]` : Validation des datatypes, longueurs et plages de valeurs sous CWA.
* **Sanity Check Automatisé** `[EXG-QUAL-03]` : Absence totale de violation de sévérité `sh:Violation`.
* **Marquage TLP** `[EXG-SEC-01]` : Marquage TLP explicite sur tout artefact.
* **Isolation Snapshots** `[EXG-SEC-02]` : Snapshots figés en lecture seule.

---

## 📊 4. Matrice Synthétique des Exigences (Index de Traçabilité)

| Identifiant | Intitulé de l'Exigence | Description & Critères d'Acceptation | Section Parent |
| :--- | :--- | :--- | :--- |
| **EXG-TBOX-01** | **Espace de Noms & Séparateur URI** | Namespace TBox unique avec séparateur `#`. | Section 3.2 |
| **EXG-TBOX-02** | **Typage OWL Strict** | Typage formel obligatoire (`owl:Class`, `owl:ObjectProperty`, etc.). | Section 3.2 |
| **EXG-TBOX-03** | **Déclaration Domaine & Portée** | `rdfs:domain` et `rdfs:range` obligatoires sur toute propriété. | Section 3.2 |
| **EXG-TBOX-04** | **Sémantique RBox & Inverses** | Rôles inverses obligatoires via `owl:inverseOf`. | Section 3.2 |
| **EXG-TBOX-05** | **Couche Lexicale SKOS Obligatoire** | Labels multilingues (FR/EN) et définitions SKOS. | Section 3.2 |
| **EXG-QUAL-01** | **Couverture SHACL** | Validation SHACL couvrante sur l'ensemble du schéma. | Section 3.2 |
| **EXG-QUAL-02** | **Contrôle de Conformité Données** | Datatypes, plages et formats validés sous CWA. | Section 3.2 |
| **EXG-QUAL-03** | **Sanity Check Automatisé** | $0$ violation `sh:Violation` au contrôle pySHACL. | Section 3.2 |
| **EXG-SHACL-01** | **Shapes Structurales Abstraites** | Méta-shapes de validation intégrées au schéma. | Section 3.2 |
| **EXG-SEC-01** | **Marquage TLP Obligatoire** | Tag TLP présent sur tout document/graphe. | Section 3.2 |
| **EXG-SEC-02** | **Isolation des Snapshots** | Immuabilité des snapshots de jalons. | Section 3.2 |
| **EXG-ORG-01** | **Spec-Driven Development** | Mise à jour SPEC obligatoire avant toute modification de code. | Section 3.1 |
| **EXG-ORG-02** | **Parité Master / Snapshot** | Empreinte binaire identical entre Master et Snapshot. | Section 3.1 |
| **EXG-ORG-03** | **Standard Traçabilité Phase_Content** | Découpage strict des livrables selon les 4 briques. | Section 3.1 |
| **EXG-ORG-04** | **Gatekeeper & Checklist Cadrage** | Validation préalable du formulaire de cadrage inter-phase. | Section 3.1 |

---

## 🛡️ 5. Gouvernance, Outillage & Validation

* **Validation Automatisée** : Suite Pytest (`pytest 03-Application/test_phase1_quality.py`).
* **Seuil de Tolérance CI/CD** : $0$ erreur de parité binaire, $0$ violation SHACL.
* **Artefacts Produits** : `PhasesProjet.md`, `Cadrage_Checklist.md`, `Cartographie_SPEC_Framework.md`.

---

## 📚 6. Pour aller plus loin (Ressources Pédagogiques)

* **[FIRST] Traffic Light Protocol (TLP) Standard** : [FIRST TLP v2.0](https://www.first.org/tlp/)
* **[W3C] SHACL Recommendation** : [W3C SHACL](https://www.w3.org/TR/shacl/)