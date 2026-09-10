# 🧹 Prompt 3/3 — Rétrospective 5S, Replay & Clôture (`[CONTEXT: RETRO-5S]`)

## 📌 Fichiers à joindre obligatoirement dans votre message :
1. Résultat complet de l'exécution `pytest` (Logs de recette)
2. `03-Application/config.py`
3. `Roadmap_Suivi-Avancement.md`
4. Liste des artefacts générés dans `02-Donnees/Snapshots_Phases/PhaseX.../`

## Périmètre d'Action
- Répertoires : `02-Donnees/Master_Transversal/`, `00-Projet/`, `Roadmap_Suivi-Avancement.md`
- Objectif : Appliquer le principe de Replay, générer la documentation miroir Markdown, procéder au nettoyage 5S et mettre à jour le State Vector Master.

## 📋 Directives & Check-list 5S
- [ ] **Principe de Replay :** Copier/Capitaliser les fichiers `.ttl` de `Snapshots_Phases/` vers `Master_Transversal/` (TBox AMBER, ABox RED, CTI CLEAR).
- [ ] **Auto-Documentation (TTL ➔ MD) :** Générer pour chaque fichier `.ttl` son miroir `.md` contenant :
  - Un tableau des acronymes utilisés (Glossaire).
  - Un diagramme Mermaid synthétique des entités et relations.
- [ ] **Nettoyage 5S :**
  - *Seiri (Tri) :* Suppression des fichiers temporaires ou scripts de debug.
  - *Seiton (Rangement) :* Synchronisation intégrale de `config.py`.
  - *Seiso (Nettoyage) :* Vérification de la parité stricte Snapshots vs Masters.
  - *Seiketsu (Standardisation) :* Remplissage de la section "Synthèse de Clôture" dans `Phase_Content.md`.
- [ ] **Mise à Jour Roadmap :** Passage du statut de la phase à 🟢 **PASSED** dans `Roadmap_Suivi-Avancement.md`.
- [ ] **Mise à Jour Systématique des 2 Fichiers Vitrines :** S'assurer que le Prompt 3 exige  : (1) Passage du statut de la phase à 🟢 **PASSED** dans `Roadmap_Suivi-Avancement.md`, (2) la mise à jour synchrone de `Roadmap_Suivi-Avancement.md` (vue détaillée des phases) et (3) du tableau macro dans `README.md`.

## 📤 Livrables Attendus
1. Fichiers Markdown miroirs (`DOC_*.md`) dans `Master_Transversal/`
2. Mises à jour de `Roadmap_Suivi-Avancement.md` et `config.py`
3. Nouveau **Context Bundle** mis à jour pour amorcer la phase suivante.