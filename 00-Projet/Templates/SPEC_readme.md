
## Ce que ça change, en résumé 

| Défaut                                       | Correction                                                                                                             |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Deux blocs YAML concurrents                  | Un seul (via `processFrontMatter`), le corps commence à `# 📜`                                                         |
| UID `…_%_1` bugué                            | Prompt du mnémonique → `EXG-MET-P8-DEM_1` propre                                                                       |
| `domaine: FWK` (portée ≠ domaine)            | Suggesteur sur la table 0 (CT…MET)                                                                                     |
| `id`/`uid` dupliqués, `intitule`/`mode_test` | Plus écrits par le template du tout — c'est `SPEC_Update_yml` qui les pose, dans **sa** convention, depuis la table §4 |
| YAML écrit en dur à la création              | Workflow SSOT : corps §4 = source → script → YAML                                                                      |

Deux conséquences à noter : 
- (1) au moment de la création, le frontmatter **n'a pas encore de clé `exigences`** — le dashboard l'ignorera jusqu'au premier passage de `SPEC_Update_yml` (à lancer juste après création, seed déjà conforme) ; 
- (2) j'ai volontairement **omis la clé `design`/section canvas** — décision actée : les SSOT sont les specs et les scripts, pas de 4e ancrage.[[SPEC_readme]]


Trois points d'attention :

1. **Le script t'envoie aussi les avertissements dans le corps du fichier** (`tR += "> [!info] …"`) — si tu préfères une notice éphémère uniquement, supprime les deux lignes `tR +=` ;
2. **La détection d'en-tête** saute toute ligne contenant « identifiant » ou « intitulé » — tes tables §4 utilisent ces mots en en-tête ✅, mais si une exigence a « identifiant » dans son intitulé, la ligne serait sautée (cas improbable, à savoir) ;
3. **Convention d'écriture** : la v2 écrit `id`, `domaine`, `core`, `titre`, `critere`, `test` — identique à tes specs existantes, et le template corrigé ne les écrit plus du tout, donc plus de conflit.

Avec ces deux scripts (template + update) harmonisés, la chaîne création → édition → consolidation est cohérente de bout en bout : **création par template (métadonnées) → exigences rédigées dans la table §4 → `SPEC_Update_yml` régénère le YAML → ateliers Dataview consolident** — et chaque étape a une convention unique. Il reste à faire la passe de recalage sur les specs existantes (les blocs §1/§2 DEM_4a-4e/RES_1/DEM_5/6/7 dans le corps de la spec demonstrateur + relance du script) — veux-tu qu'on la déroule maintenant, fichier par fichier ?