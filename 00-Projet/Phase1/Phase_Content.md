
# Objectifs de la phase  : 


### 🔷 Phase 1 — Socle Modèle Canonique & Qualité (TBox / RBox / SHACL)

- **Objectif** : Définir la structure de connaissance, les règles d'inférence de relations et le contrat d'intégrité des données (`TLP:AMBER`).
    
- **Livrables constitutifs (Le Triptyque)** :
    
    1. **TBox (Classes & Attributs)** : Taxonomie des concepts (`Asset`, `Vulnerability`, `Weakness`, etc.).
        
    2. **RBox (Relations & Logique)** : Propriétés d'objets, hiérarchie de relations, propriétés inverses (`isComponentOf` ↔ `hasInstalledComponent`), transitivité ou symétrie.
        
    3. **SHACL (Shapes & Validation)** : Garde-fous impératifs (monde fermé / CWA), vérification des motifs (Regex IP/CVE), cardinalités (`minCount 1`) et bornes numériques (CVSS $0.0 \le x \le 10.0$).
        
- **Répertoire Master** : `12-Donnees/Master_Transversal/TLP_AMBER_Socle_TBox/`





initialiser le projet en construisant une première socle structurel TBox-RBox  multiformat minimale correspondant aux cas d'usage 
Le livrable générique correspond aux spécifications : [SPEC-01](../../11-Principes_Architecture/Specifications/SPEC-01_Norme_TBox_RBox.md)
Une bonne partie des données sont en dur dans le premier script.
Les phase suivantes viseront a mettre en place les outils d'évolution

Ce premier socle est disponible en " format dont 1 en markdown (.md) pour que les parties prenantes en garde le controle [TBox_Human](../../12-Donnees/TBox_init/TBox_Cybersec.md)

Cette phase a été reprise suite au [REX-01](REX-01_rigueur_attendue_RDF-OWL.md)   


# Bilan des Actions et Livrables

| Action                                    | livrable                                | Localisation       | Commentaire                   |                       |
| ----------------------------------------- | --------------------------------------- | ------------------ | ----------------------------- | --------------------- |
| Mise en place de la specification du TBox | SPEC-01_Norme_TBox_RBox                 | 11-/Specification/ | sert aux tests                | 🟢 Terminée / Validée |
| Mise a disposition de données sources     | cve_data.ttl                            | 12-/1-/2-          | une seule cve sur le use case | 🟢 Terminée / Validée |
| Script de génération d'un premier ttl     | build_inital_ttl_TBox.py                | 13-/               |                               | 🟢 Terminée / Validée |
| Premier ttl généré par cript précédent    | TBox_Cybersec.ttl                       | 12-/TBox_init      |                               | 🟢 Terminée / Validée |
| Scrip de génération md et json            | generate_TBox_initiale.py               | 13-/               |                               | 🟢 Terminée / Validée |
| generation TBox tout format               | `TBox_Cybersec.jon`, `TBox_Cybersec.md` | 12-/TBox_init      |                               | 🟢 Terminée / Validée |
| test des fichiers TBox % specifications   | `test_phase1_tbox_rbox_spec.py`         | 13-/               |                               | 🟢 Terminée / Validée |
|                                           |                                         |                    |                               |                       |

- 
# Memo didactique

### 5. Explicitation de la Génération de `TBox_Cybersec.ttl`

Pour clarifier le processus de création et de mise à jour de `TBox_Cybersec.ttl` auprès de tous les intervenants (humains et agents IA), le flux de génération s'établit comme suit :

1. **Origine Métier / Modélisation** : Édition des concepts formels dans `TBox_Cybersec.ttl` via des éditeurs d'ontologies (Protégé, TopBraid) ou écriture manuelle en syntaxe Turtle W3C.
    
2. **Enrichissement Lexical (SKOS)** : Ajout systématique des annotations `rdfs:label` (français/anglais) et `skos:altLabel` (synonymes métier et acronymes) directement sur chaque nœud du fichier Turtle.
    
3. **Pipeline de Compilation** : Exécution du script `13-Application/generate_TBox_initiale.py` qui lit la source Turtle et compile automatiquement les fichiers `TBox_Cybersec.json` et `TBox_Cybersec.md`.
    
4. **Contrôle Qualité Automatique** : Exécution de `pytest 13-Application/test_tbox_spec.py` pour valider qu'aucune modification de la TBox n'a enfreint le contrat de spécification.