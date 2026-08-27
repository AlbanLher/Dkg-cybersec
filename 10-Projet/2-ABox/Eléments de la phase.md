### 1. Périmètre de la Phase 2 : Ce que l'on FAIT vs Ce que l'on NE FAIT PAS

| **Domaine**                        | **IN (Inclus dans la Phase 2)**                                                                                      | **OUT (Repoussé à une étape ultérieure)**                                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Périmètre Données (ABox)**       | **Instanciation locale uniquement** : Conversion de `inventory.json` en triplets RDF (`ABox_Cybersec.ttl`).          | **Ingestion de flux externes (NVD/CVE, CWE, CISA KEV)** : Pas de requêtes réseau vers la NVD ou Mitre (Phase 3).               |
| **Alignement TBox/ABox**           | Rattachement direct des instances de `inventory.json` aux classes de la TBox (`dkg:Asset`, `dkg:SoftwareComponent`). | **Raisonnement OWL / Inférence complexe** : Pas d'exécution de raisonneur (Pellet/HermiT) pour déduire de nouvelles relations. |
| **Adaptation de `inventory.json`** | Simplification de la structure du fichier JSON pour garantir la lisibilité et l'aspect pédagogique.                  | **Structures JSON complexes ou imbriquées indéfiniment** : Pas de parsing de formats hétérogènes multi-sources.                |
| **Livrables Formats**              | Génération du fichier ABox maître en Turtle (`ABox_Cybersec.ttl`) + export JSON/Markdown simple.                     | **Base de données Graph (GraphDB, Neo4j, Stardog)** : L'alimentation d'un SPARQL Endpoint physique est repoussée.              |
| **Validation**                     | Tests `pytest` de conformité RDF (existence des URIs, types RDF, liaisons à la TBox).                                | **Validation de règles Métier/SHACL complexes** : Validation de contraintes de formes avancées (Phase 4).                      |


### 2. Adaptation Didactique du Cas d'Usage & de `inventory.json`

Pour maximiser l'efficacité pédagogique, nous adaptons le fichier `inventory.json` d'entrée afin qu'il illustre **3 motifs d'instanciation clés** :

1. **Un Asset (Serveur)** $\rightarrow$ représenté par un nom, une IP et un rôle.
    
2. **Un Composant Logiciel (SoftwareComponent)** $\rightarrow$ identifié par sa version et un identifiant CPE (Common Platform Enumeration).
    
3. **Une Vulnérabilité / Faiblesse "Fantôme" (Mocked)** $\rightarrow$ une déclinaison illustrative locale (ex: une CVE fictive ou locale attachée au composant pour montrer la structure de liaison).


Données synthetisées ->     **`./12-Donnees/ABox_init/inventory.json`**
```json
{
  "assets": [
    {
      "id": "srv-web-01",
      "label": "Serveur Web Production",
      "ip": "192.168.1.10",
      "installed_software": [
        {
          "id": "sw-nginx-1201",
          "label": "NGINX Web Server",
          "cpe": "cpe:2.3:a:f5:nginx:1.20.1:*:*:*:*:*:*:*",
          "version": "1.20.1",
          "known_vulnerabilities": ["CVE-2021-23017"]
        }
      ]
    }
  ]
}
```




### 3. Chaîne d'Outillage à Construire (3 Scripts)

Comme en Phase 1, nous conserverons une architecture explicite et modulaire dans `13-Application/` :

1. `build_initial_inventory_json.py` : Script de génération/mise à jour du fichier d'entrée `inventory.json` modèle.
    
2. `ingest_inventory_abox.py` : Script de transformation (Mappeur JSON $\rightarrow$ RDF Turtle `ABox_Cybersec.ttl`).
    
3. `test_ABox_spec.py` : Suite de tests `pytest` vérifiant la conformité ABox (URIs, types, relations).



### 3.  Bilan des Actions et Livrables

| Action                                       | livrable                            | Localisation   | Commentaire       |
| -------------------------------------------- | ----------------------------------- | -------------- | ----------------- |
| Mise en place de la specification de la ABox | SpecificationNormativeIngestionABox | 10-/2-/        | Fait a consolider |
| Génération d'un fichier syntetique           | `ìnventory.json`                    | 12-/ABox_init/ | fait              |
| test les exigences                           | `test_ABox_spec.py`                 | 13-/           | fait              |
|                                              | `ingest_inventory_abox.py`          | 13-/           | fait              |
|                                              | `generate_ABox_initiale.py`         | 13-/           | fait              |
|                                              |                                     |                |                   |
|                                              |                                     |                |                   |
|                                              |                                     |                |                   |

- 