# 🧹 Module Rétrospective & Clôture 5S (`[CONTEXT: RETRO]`)

## Périmètre d'Action
- Répertoire : `00-Projet/`, synthèses `02-Donnees/`, `Roadmap_Backlog_SOC.md`
- Objectif : Bilan de phase, audit d'artefacts, documentation, nettoyage et consolidation.

## 📋 Check-list de Clôture & Bilan 5S (À valider obligatoirement)
- [ ] **Audit des Artefacts :** Recensement exact des fichiers `.ttl` générés (TBox, SHACL, ABox, Rules) et vérification de leur rôle.
- [ ] **Synchro config.py :** Tous les nouveaux répertoires/fichiers sont-ils déclarés dans `config.py` ?
- [ ] **Synthèse Markdown :** La fiche `02_SYNTHESE_*.md` du sous-dossier de données est-elle générée et synchronisée ?
- [ ] **Bilan 5S :**
  - *Seiri (Tri) :* Suppression/archivage du code mort et des fichiers temporaires.
  - *Seiton (Rangement) :* Validation de l'emplacement SSOT des livrables.
  - *Seiso (Nettoyage) :* Exécution et succès de la suite `pytest` (local + GitHub Actions).
  - *Seiketsu (Standardisation) :* Mise à jour de `Roadmap_Backlog_SOC.md` (tâches cochées, REX).