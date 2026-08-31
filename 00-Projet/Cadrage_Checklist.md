# 🚦 Checklist de Cadrage & Gatekeeper Inter-Phases

> **Objectif** : Valider formellement la clôture de la Phase N-1 avant d'autoriser le démarrage de la Phase N.

---

## 🔒 Étape Préliminaire : Audit de Clôture de la Phase Précédente
Avant de rédiger le plan de la nouvelle phase, le responsable de projet doit cocher les éléments suivants concernant la phase écoulée :

* [ ] **1. Synthèse de Clôture** : Le fichier `Phase_Content.md` de la phase N-1 contient bien sa section `## 🏁 Synthèse de Clôture` remplie.
* [ ] **2. Traçabilité des Liens (`PhasesProjet.md`)** : Le tableau de bord global pointe explicitement vers :
  * La spécification associée (`SPEC-XX`).
  * Le document human-readable / use-case d'illustration.
  * Le fichier de contenu de phase.
* [ ] **3. Intégrité des Artefacts & Tests** : Tous les scripts de génération et la suite Pytest associée renvoient un statut `PASSED` (parité Master/Snapshot OK).

---

## 🚀 Étape Active : Initialisation de la Phase N
* [ ] **4. Rédaction du Cadrage** : Création du dossier de la nouvelle phase et rédaction de son `Phase_Content.md` en mode "Objectifs & Périmètre".
* [ ] **5. Alignement Exigences** : Rattachement des nouveaux livrables aux exigences de `SPEC-00_ExigencesProjet.md`.