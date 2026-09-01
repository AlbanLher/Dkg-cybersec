_Vue de l'avancement par phases_
Vision plus globale de la [roadmap Produit ici](./Roadmap_Produit.md)
## 1  -  Status de Developement

_des liens vous permettent d'accéder à :_
- Phase_content.md de chaque phase décrivant les étapes et livrables de cette phase
- Exemple de Specification resultant pour le Framework
- Exemple de livrable en version human .md de l'instanciation sur Use Case

| Avancement -> | Vague | Phase | étape |
| :-----------: | :---: | :---: | :---: |
|               |   1   |   2   |   2   |

## 2  -  Phases


| Vague |                     Phase<br>Content                     | Titre                                                                                                                                                                  |      Status      |                                                    Exemple<br>SPEC                                                    |                               Exemple <br>d'instantiation                                |                                          Commentaire                                           |
| :---: | :------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------: | :-------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------: |
|   1   |         [**Phase1**](./Phase1/Phase_Content.md)          | initialisation Socle Modèle Canonique & Qualité<br>- TBox (class Datatype) , <br>- RBox { relations, Inverse)<br>- SHACL (shapes & validation)}<br>dans un cas simple. | Reprise en cours | [SPEC-01](01-Principes_Spécifications/Specifications_Framework/SPEC-01_Socle_Structurel_Framework_TBox_RBox_SHACL.md) |     [TBox_Human](../../02-Donnees/Snapshots_Phases/Phase_1_Socle/DKG_TBox_Master.md)     |   Comprendre les enjeux du socle<br>Ajout manuel des Acronymes T-R-A Box dans lexique du .md   |
|   1   |          [**Phase2**](2-ABox/Phase_Content.md)           | initialisation de l'instanciation interne<br>- - ABox                                                                                                                  |   A reprendre.   |                                                        SPEC-02                                                        | [ABox_Human](../02-Donnees/Master_Transversal/TLP_RED_Instances_ABox/DKG_ABox_Master.md) |                                                                                                |
|   2   | [**Phase3**](./3-EnrichissementExterne/Phase_Content.md) | Enrichissement avec des donnéesExterne<br>+ Gouvernance ( TLP )                                                                                                        |   A Reprendre    |                                                                                                                       |                                                                                          | Comprendre l'articulation de TBox, RBox, ABox ref [lien](Phase3/Articulation_des_T-R-A_Box.md) |
|       |                        **Phase4**                        |                                                                                                                                                                        |                  |                                                                                                                       |                                                                                          |                                                                                                |


## 3  -  Backlog des principes et fonctions  :
- query sur un graph , comprendre la superposition
- mise en place neo4j
- NER Hybride** (Regex + LLM),
- Vectorisation : Embeddings ,
- RAG : Requêtage hybride
- Analyse critique + HITL
- Ré-ingestion si TBox évolue
- Fine-tuning modèles