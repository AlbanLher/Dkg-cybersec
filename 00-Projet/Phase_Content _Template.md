# 📋 Phase [X] : [Nom de la Phase]

> **Statut** : [En cours / 🟢 Validée & Close]  
> **Date de début** : [JJ/MM/AAAA]  
> **Date de clôture** : [JJ/MM/AAAA]  

---

## 🎯 1. Objectifs & Périmètre
* **But principal** : [Description synthétique des ambitions de la phase]
* **Livrables attendus** : [Liste des composants logiciels, schémas ou documents produits]

---

## 🛠️ 2. Traçabilité des Livrables par Brique

### A. Spécification & Gouvernance (SPEC Framework)
* **Spécification associée** : [`SPEC-XX-Titre.md`](../../01-Exigences/SPEC-XX.md)
* **Exigences couvertes** : Explicitation des règles Métier/Framework adressées dans cette phase.

### B. Instanciation & Use Case Pédagogique (Lisible Humain)
* **Document d'illustration** : [`Human_UseCase.md`](./Human_UseCase.md)
* **Description** : Scénario concrétisé démontrant la valeur métier sans jargon brut.

### C. Données & Ontologies (Data / Graph RDF)
* **Artefacts Master** : [`Donnees_Master.ttl`](../../02-Donnees/Master_Transversal/...)
* **Artefacts Snapshot** : [`Snapshot_Phase_X/`](../../02-Donnees/Snapshots_Phases/...)

### D. Scripts & Outillage (Automation & CI/CD)
* **Générateur** : [`generate_phaseX.py`](./generate_phaseX.py)
* **Tests Qualité** : [`test_phaseX_quality.py`](./test_phaseX_quality.py)

---

## 🏁 3. Synthèse de Clôture & Ressources

### Résumé Exécutif
[Synthèse globale de l'atterrissage de la phase, des acquis et de l'état du code/graphe]

### Matrice Récapitulative des Livrables
| Brique | Composant / Fichier | Description |
| :--- | :--- | :--- |
| **Framework** | [`SPEC-XX.md`](../../01-Exigences/...) | Spécification des contraintes & règles |
| **Instanciation** | [`Human_UseCase.md`](./...) | Cas d'usage métier expliqué |
| **Data** | [`Graphe_Master.ttl`](../../02-Donnees/...) | Fichiers RDF / Turtle générés |
| **Script** | [`generate_phaseX.py`](./...) | Script de génération et synchronisation |

---

## 📚 4. Pour aller plus loin (Ressources Pédagogiques)
*(Liens documentaires et tutoriels pour approfondir les concepts de la phase)*
* **[Concept 1]** : [Lien / Référence] — *Brève description du concept.*
* **[Concept 2]** : [Lien / Référence] — *Brève description du concept.*