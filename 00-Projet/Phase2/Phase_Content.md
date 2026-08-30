_Initialisation & Peuplement de l'ABox (Graphe d'Instances)_


### 🔷 Phase 2 — Instanciation Interne du SI (ABox Intérieure)

- **Objectif** : Modéliser le système d'information réel de l'entreprise sous forme de graphe d'instances brutes (`TLP:RED`).
    
- **Périmètre** :
    
    - Instanciation des équipements (`Asset`), des adresses IP, des serveurs et des briques logicielles installées (`SoftwareComponent`).
        
    - Déclaration des vulnérabilités locales détectées (ex: scanner de vulnérabilités interne).
        
    - Validation stricte à l'entrée via les contraintes SHACL définies en Phase 1.
        
- **Répertoire Snapshot** : `12-Donnees/Snapshots_Phases/Phase_2_ABox_init/`







initialiser le projet en construisant une première instance A_Box sur le socle précédent,  multiformat correspondant aux cas d'usage 
Le livrable générique correspond aux spécifications : [SPEC-02](../../11-Principes_Architecture/Specifications/SPEC-02_Norme_Ingestion_ABox.md)
Une bonne partie des données sont en dur dans le premier script.
Les phase suivantes viseront a mettre en place les outils d'évolution

Ce premier socle est disponible en " format dont 1 en markdown (.md) pour que les parties prenantes en garde le controle [ABox_Human](../../12-Donnees/ABox_init/ABox_Cybersec.md)

Cette phase a été reprise suite au [REX-01](REX-01_rigueur_attendue_RDF-OWL.md)   




les données sont étendue "hard_coded"
- Des hôtes web et BDD (`srv-web-01`, `srv-db-01`).
    
- Des composants logiciels connus (`log4j-core-2.14.1`, `nginx-1.18.0`, `postgresql-13.2`).
    
- Des vulnérabilités majeures (`CVE-2021-44228` / Log4Shell, `CVE-2021-23017`).
    
- Des faiblesses CWE associées (`CWE-502`, `CWE-193`).
- 

## 📌 Traçabilité & Provenance des Données ABox

### 1. Jeu de Données de Référence (Gold Dataset)
Afin d'assurer des tests de non-régression reproductibles (idempotence) entre la Phase 1 et la Phase 2, les instances initiales générées dans `12-Donnees/ABox_init/` sont déterministes.

* **Mode de Génération** : Statique et Déterministe (sans aléatoire).
* **Source de Référence** : `generate_ABox_initiale.py` (Modèle d'infrastructure canonique multi-tiers : Serveur Web + BDD).
* **Ingestion Dynamique** : `ingest_inventory_abox.py` (Projection d'inventaires au format JSON/CMDB vers le graphe ABox).

### 2. Composition du Jeu d'Instances Initial
* **Infrastructure** : `srv-web-01` (Front-end Web), `srv-db-01` (Base de données BDD).
* **Composants applicatifs** : `log4j-core-2.14.1`, `nginx-1.18.0`, `postgresql-13.2`.
* **Vecteurs de vulnérabilités** : `CVE-2021-44228` (Log4Shell / `CWE-502`), `CVE-2021-23017` (Nginx / `CWE-193`).

### 3. Garanties d'Idempotence
Toute ré-exécution du pipeline (`ingest#` ➔ `generate#` ➔ `test#`) régénère de manière strictement identique les fichiers Turtle, JSON-LD et Markdown dans `12-Donnees/ABox_init/`, garantissant la stabilité de la suite d'intégration `test_phase2_abox_spec.py`.


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

| Action                                       | livrable                               | Localisation   | Commentaire       |                       |
| -------------------------------------------- | -------------------------------------- | -------------- | ----------------- | --------------------- |
| Mise en place de la specification de la ABox | SPEC-02_Norme_Ingestion_ABox.md        | 10-/2-/        | Fait a consolider | 🟢 Terminée / Validée |
| Génération d'un fichier syntetique           | `ìnventory.json`                       | 12-/ABox_init/ | fait              | 🟢 Terminée / Validée |
| test les exigences                           | `test_phase3_referentiel_nvd_spec.py ` | 13-/           | fait              | 🟢 Terminée / Validée |
|                                              | `ingest_inventory_abox.py`             | 13-/           | fait              | 🟢 Terminée / Validée |
|                                              | `generate_ABox_initiale.py`            | 13-/           | fait              | 🟢 Terminée / Validée |
|                                              |                                        |                |                   |                       |
|                                              |                                        |                |                   |                       |
|                                              |                                        |                |                   |                       |

- 