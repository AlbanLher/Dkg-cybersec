# 🔧 Prompt 2/3 — Code, Data Pipeline & Tests PyTest (Axé TSV & SSOT) — rév. 2026-11-23

> Rév. 2026-11-23 : ajoute la loi brique/application, le nommage canonique des
> scripts (01.2 § 1.quater), la docstring d'en-tête, le test anti-monolithe et
> l'exigence de recette par livrable.

## 📌 Fichiers à joindre obligatoirement dans votre message :
1. `03-Application/config.py`
2. Le fichier **TSV de Spécifications/Exigences** de la phase active
   (ex: `01-Principes_Spécifications/.../Specs_PhaseX.tsv`)
3. `00-Projet/phases/PhaseX/Phase_Content.md`
4. L'étape bornée du backlog correspondante (le carnet de session du cadrage)

## Périmètre d'action & décomposition systémique
- Traiter le problème par **modules sous-systèmes** indépendants définis dans
  le TSV — **une étape bornée = une session, pas deux** ; en phase brique,
  AUCUNE intégration applicative (pas de route, pas d'IHM) : on écrit la
  bibliothèque, ses tests et sa recette.
- Pour chaque module, implémenter le triptyque :
  `Schéma Pydantic/Config` ➔ `Logique Métier / RDF` ➔ `Test PyTest associé`.

## 📋 Directives & Check-list Qualité Code
- [ ] **Traçabilité TSV :** chaque fonction ou test inclut en docstring l'ID
      exact de l'exigence (ex: `# [EXG-FWK-P9-...]`) — et pour les tests, le
      **nom de la fonction** porte l'UID qu'elle recette (citation ≠ recette,
      convention du 01.1 §4).
- [ ] **SSOT strict :** 100% des chemins et namespaces proviennent de
      `config.py`.
- [ ] **Nommage canonique (01.2 § 1.quater) :** `_engine` moteur, `agent_`
      agent, `_views`/`_gateway`/`_intake`/`_volumes`/`_simulator` selon la
      nature ; **docstring d'en-tête obligatoire** :
      `"""MOTEUR|AGENT|VUE|GATEWAY — rôle — recette/EXG tracés"""`.
- [ ] **Loi des répertoires :** un script de rejeu vit dans
      `phases/PhaseX/`, un moteur partagé dans `core/` — **jamais de copie
      entre les deux** (l'import fait le pont) ; aucun module de `core`
      n'importe `phases` (le test anti-monolithe le vérifie).
- [ ] **Conformité Pydantic V2 :** `ConfigDict(frozen=True)`.
- [ ] **Validation SHACL CWA & PyTest :** couverture totale des critères
      d'acceptation du TSV ; toute écriture graphe est validée SHACL.
- [ ] **Recette par livrable :** chaque livrable s'accompagne de sa recette
      (commande curl + résultat attendu) ; toute analyse du graphe passe par
      SPARQL, jamais par regex sur `.ttl`.
- [ ] **Non-régression :** les 61 tests doivent rester verts ; tout renommage
      ou suppression prévu par le backlog passe par le replays des données
      et le NonReg avant consolidation.
- [ ] **Frugalité (Green Dev, 01.2 § 1.bis.2) :** traitement par lots bornés
      en RAM, tampon disque, reprise sur point de contrôle — jamais le volume
      total en mémoire vive.
