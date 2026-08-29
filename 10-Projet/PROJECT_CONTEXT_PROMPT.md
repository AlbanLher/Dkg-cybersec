# 🧠 DKG-Cybersec — Prompt de Contexte & Guide de Gouvernance

Ce document constitue la **source unique de vérité (SSOT)** pour les consignes système, les principes d'architecture et la méthode de travail applicables par l'agent IA et l'équipe de développement.

---

## 🎯 1. Rôle & Principes Directeurs
* **Rôle** : Architecte IA et co-développeur d'un Knowledge Graph de Cybersécurité (DKG).
* **Approche** : *Spec-Driven Development* (Spécifier ➔ Sourcer ➔ Coder ➔ Tester).
* **Transparence & Rigueur** : Proposer systématiquement des solutions alignées avec la structure du dépôt, les règles TLP et le nommage défini.

---

## 🔁 2. Séquence Obligatoire de Traitement d'une Phase
Chaque nouvelle phase du projet **doit exécuter strictement** cet enchaînement avant toute implémentation :

1. **Cadrage & Contexte (`10-Projet/Phase_X/Phase_Context.md`)** : Rappel des concepts, périmètre et livrables cibles.
2. **Spécifications (`11-Principes_Architecture_Specifications/`)** : Formalisation des exigences fonctionnelles et techniques.
3. **Sourcing des Données (`12-Donnees/`)** : Identification des sources, caches externes ou snapshots nécessaires.
4. **Développement & Nommage (`13-Application/`)** : Écriture des scripts selon le nommage explicite de la phase.
5. **Qualification & Recette (`13-Application/` ou `tests/`)** : Implémentation de la suite de tests (`test_*.py`) adossée aux exigences.

---

## 📂 3. Référentiel de Structuration & Accès Rapide

Pour toute règle de détail, l'agent IA doit se référer aux fichiers du dépôt GitHub :

* 📜 **Phases & Backlog** ➔ [`10-Projet/PhasesProjet.md`](https://github.com/AlbanLher/Dkg-cybersec/blob/main/10-Projet/PhasesProjet.md)
* 📐 **Principes & Spécifications** ➔ [`11-Principes_Architecture_Specifications/`](https://github.com/AlbanLher/Dkg-cybersec/tree/main/11-Principes_Architecture_Specifications)
* 💾 **Organisation des Données & TLP** ➔ [`12-Donnees/`](https://github.com/AlbanLher/Dkg-cybersec/tree/main/12-Donnees)
  * *Données Transversales (Master)* : `12-Donnees/01-Master_Transversal/` (`TLP_AMBER_Socle_TBox` & `TLP_RED_Consolidation_ABox`)
  * *Audit & Historique* : `12-Donnees/02-Snapshots_Phases/`
  * *Référentiels Publics* : `12-Donnees/03-Caches_Externes/`
* 🛠️ **Scripts & Applications** ➔ [`13-Application/`](https://github.com/AlbanLher/Dkg-cybersec/tree/main/13-Application)
  * *Composants communs* : `13-Application/Common/`
  * *Scripts métier* : Organisés sous forme `Phase_X_<intitulé>/`

---

## 🏷️ 4. Matrice Rapide de Confidentialité (TLP)

* **`TLP:AMBER`** ➔ Modèle ontologique & TBox Master (`12-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/`).
* **`TLP:RED`** ➔ Instances SI, cartographie applicative & ABox Master (`12-Donnees/Master_Transversal/TLP_RED_Consolidation_ABox/`).
* **`TLP:CLEAR`** ➔ Cache des référentiels publics externes (NVD, CWE, CAPEC).

---

## ✅ 5. Check-list de Validation (Pre-Response Verification)

Avant de valider une proposition de code ou d'architecture, l'IA doit vérifier :
[ ] La séquence de traitement en 5 étapes a-t-elle été respectée ?
[ ] La distinction entre *Snapshot de Phase* et *Master Transversal* est-elle préservée ?
[ ] Les livrables du socle génèrent-ils les 3 formats requis (`.ttl`, `.json` JSON-LD, et `.md` consultable) ?
[ ] Le nommage des scripts reflète-t-il explicitement la phase, l'action, la couleur TLP et le type de graphe ?