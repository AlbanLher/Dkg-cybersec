# 🔧 Prompt 2/3 — Code, Data Pipeline & Tests PyTest (Axé Contrat & SSOT) — rév. 2026-11-25

> Rév. 2026-11-25 : NonReg 61 → **130** (plancher inviolable, rejoué AVANT
> commit) ; la source des exigences est le `registry_exigences.json` vivant
> (v2.5) ; ajoute les leçons étape 3 (échec sonore, engagement « import »
> prohibited in core docstrings, une seule version finale par livrable).

## 📌 Fichiers à joindre obligatoirement dans votre message :
1. `03-Application/config.py`
2. Le **registre des exigences** vivant :
   `01-Principes_Spécifications/registry_exigences.json` (TSV de la phase si
   encore utilisé)
3. `00-Projet/phases/PhaseX/Phase_Content.md`
4. L'étape bornée du backlog correspondante (le carnet de session du cadrage)

## Périmètre d'action & décomposition systémique
- Traiter le problème par **modules sous-systèmes** indépendants définis dans
  le registre — **une étape bornée = une session, pas deux** ; en phase brique,
  AUCUNE intégration applicative (pas de route, pas d'IHM) : on écrit la
  bibliothèque, ses tests et sa recette.
- Pour chaque module, implémenter le triptyque :
  `Schéma Pydantic/Config` ➔ `Logique Métier / RDF` ➔ `Test PyTest associé`.

## 📋 Directives & Check-list Qualité Code
- [ ] **Traçabilité registre :** chaque fonction ou test inclut en docstring
      l'ID exact de l'exigence (ex. `# [EXG-FWK-P9-EOL_1]`) — et pour les tests,
      le **nom de la fonction** porte l'UID qu'elle recette (citation ≠
      recette, convention du 01.1 §4).
- [ ] **SSOT strict :** 100% des chemins et namespaces proviennent de
      `config.py` ; ancrage file-relatif
      `Path(__file__).resolve().parent.parent` (…selon profondeur), jamais
      CWD-relatif ; vérifier par simulation avant publication.
- [ ] **Nommage canonique (01.2 § 1.quater) :** `_engine` moteur, `agent_`
      agent, `_views`/`_gateway`/`_intake`/`_volumes`/`_simulator` selon la
      nature ; **docstring d'en-tête obligatoire** :
      `"""MOTEUR|AGENT|VUE|GATEWAY — rôle — recette/EXG tracés"""`
      (jamais d'énoncé d'`import` en toutes lettres dans les docstrings de
      core/ — grep CI en dépend).
- [ ] **Loi des répertoires :** un script de rejeu vit dans `phases/PhaseX/`,
      un moteur partagé dans `core/` — **jamais de copie entre les deux**
      (l'import fait le pont, `phases` est l'AMONT du rejeu, `core` l'AVAL
      capitalisé) ; aucun module de `core` n'importe `phases` (le test
      anti-monolithe le vérifie).
- [ ] **Conformité Pydantic V2 :** `ConfigDict(frozen=True)`.
- [ ] **Validation SHACL CWA & PyTest :** couverture totale des critères
      d'acceptation ; toute écriture graphe est validée SHACL.
- [ ] **Recette par livrable :** chaque livrable s'accompagne de sa recette
      (commande + résultat attendu) ; toute analyse du graphe passe par
      SPARQL, jamais par regex sur `.ttl` ; **échec SONORE obligatoire**, pas
      de tolérance silencieuse ni de valeur par défaut masquante.
- [ ] **Non-régression :** le plancher **130 passed** doit rester vert —
      rejoué AVANT chaque commit, jamais après ; tout renommage/suppression
      passe par le rejeu des données et le NonReg avant consolidation.
      Un NonReg cassé par une réorientation n'est PAS commitable.
- [ ] **Livraison en une version finale :** un livrable = UN fichier complet
      prêt à remplacer, jamais de fragments ni de versions intermédiaires.
- [ ] **Frugalité (Green Dev, 01.2 § 1.bis.2) :** traitement par lots bornés
      en RAM, tampon disque, reprise sur point de contrôle — jamais le volume
      total en mémoire vive.
- [ ] **Gestes bornés :** un geste ≤ 5s, un commit par geste, chemins
      explicites (`git add <chemin>`, jamais `git add -A`) ; jamais
      d'apostrophes dans les commandes sed/heredoc livrées.
