### 2. Cadrage de la Phase 3 : Enrichissement Externe (RBox / Linking NVD & CWE)

Après avoir défini le schéma (**TBox - Phase 1**) et instancié les équipements privés (**ABox - Phase 2**), l'objectif de la **Phase 3** est d'**enrichir automatiquement le graphe par liaison externe** (Linked Open Data / Knowledge Graph public).

#### Périmètre : Ce que l'on FAIT vs Ce que l'on NE FAIT PAS

|**Domaine**|**IN (Inclus dans la Phase 3)**|**OUT (Repoussé à une étape ultérieure)**|
|---|---|---|
|**Sources Externes**|**Mock local de référentiel CVE / CWE / NVD** : Simulation d'une API ou fichier pivot JSON/RDF représentant les failles (NVD) et faiblesses (Mitre CWE).|**Requêtes temps réel volumineuses vers les API NVD/MITRE** : Évite les verrous d'API (rate limiting), les clés API nécessaires et la dépendance réseau lors des builds/tests.|
|**Liaisons Ontologiques (RBox/Properties)**|**Instanciation des relations inter-domaines** : Liaison `dkg:Vulnerability` $\rightarrow$ `dkg:classifiedUnder` $\rightarrow$ `dkg:Weakness` (CWE).|**Alignement d'ontologies complexes (OWL SameAs / Alignment)** : Pas de mapping dynamique d'ontologies tierces complexes.|
|**Modèle de Données**|Enrichissement des nœuds `dkg:Vulnerability` avec leurs scores de sévérité (CVSS) et catégories CWE rattachées.|**Calculs dynamiques de score de risque global du SI** : Le moteur de calcul de risque reste du ressort des requêtes de Phase 4.|
|**Livrables & Visualisation**|Génération de `12-Donnees/RBox_Enrichment/Vulnerability_Knowledge.ttl` et mise à jour de la documentation visuelle Markdown avec le graphe enrichi.|**Base SPARQL Triple Store distante (GraphDB / Fuseki)** : Restera sur sérialisation locale Turtle.|

### 3. Matrice de Mapping d'Enrichissement Cible

```
[ Asset Privé ] ──(hasInstalledComponent)──> [ SoftwareComponent ]
                                                    │
                                          (hasVulnerability)
                                                    ▼
                                          [ Vulnerability (CVE) ] ◄── (Phase 3: Enrichissement NVD)
                                                    │               - Score CVSS
                                            (classifiedUnder)       - Description publique
                                                    ▼
                                          [ Weakness (CWE) ]     ◄── (Phase 3: Taxonomie Mitre)
                                                                    - Categorie CWE (ex: CWE-79)
```

### 4. Spécifications & Outillage à Venir (Phase 3)

1. **Spécification :** `11-Principes_Architecture/Specifications/SpecificationNormativeEnrichissementRBox.md`
    
2. **Fichier Source Mock Externe :** `12-Donnees/RBox_Enrichment/nvd_cwe_mock.json`
    
3. **Scripts `13-Application/` :**
    
    - `enrich_vulnerabilities_rbox.py` : Script d'alignement et d'enrichissement RDF.
        
    - `generate_RBox_initiale.py` : Génération de la vue visualisable complète (Asset $\rightarrow$ CVE $\rightarrow$ CWE).
        
    - `test_RBox_spec.py` : Suite de tests `pytest` vérifiant les liaisons inter-ontologies.


### 5.  Bilan des Actions et Livrables

| Action                                       | livrable                            | Localisation   | Commentaire       |                       |
| -------------------------------------------- | ----------------------------------- | -------------- | ----------------- | --------------------- |
| Mise en place de la specification de la ABox | SpecificationNormativeIngestionABox | 10-/2-/        | Fait a consolider | 🟢 Terminée / Validée |
| Génération d'un fichier syntetique           | `ìnventory.json`                    | 12-/ABox_init/ | fait              | 🟢 Terminée / Validée |
| test les exigences                           | `test_ABox_spec.py`                 | 13-/           | fait              | 🟢 Terminée / Validée |
|                                              | `ingest_inventory_abox.py`          | 13-/           | fait              | 🟢 Terminée / Validée |
|                                              | `generate_ABox_initiale.py`         | 13-/           | fait              | 🟢 Terminée / Validée |
|                                              |                                     |                |                   |                       |
|                                              |                                     |                |                   |                       |
|                                              |                                     |                |                   |                       |