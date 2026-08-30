
## 🔄 Workflow


| Lot |                     Phase<br>Content                     | Titre                                                                                                                                                                  |      Status      | Ecemple<br>SPEC |                Exemple <br>d'instantiation                |                                          Commentaire                                           |
| :-: | :------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------: | :-------------: | :-------------------------------------------------------: | :--------------------------------------------------------------------------------------------: |
|  1  |  [**Phase1**](./1-TBox_Initialisation/Phase_Content.md)  | initialisation Socle Modèle Canonique & Qualité<br>- TBox (class Datatype) , <br>- RBox { relations, Inverse)<br>- SHACL (shapes & validation)}<br>dans un cas simple. | Reprise en cours |     SPEC-01     | [TBox_Human](../../12-Donnees/TBox_init/TBox_Cybersec.md) |                                 Comprendre les enjeux du socle                                 |
|  1  |          [**Phase2**](2-ABox/Phase_Content.md)           | initialisation de l'instanciation interne<br>- - ABox                                                                                                                  |   A reprendre.   |     SPEC-02     | [ABox_Human](../../12-Donnees/ABox_init/ABox_Cybersec.md) |                                                                                                |
|  1  | [**Phase3**](./3-EnrichissementExterne/Phase_Content.md) | Enrichissement avec des donnéesExterne<br>+ Gouvernance ( TLP )                                                                                                        |   A Reprendre    |                 |                                                           | Comprendre l'articulation de TBox, RBox, ABox ref [lien](Phase3/Articulation_des_T-R-A_Box.md) |
|     |                        **Phase4**                        |                                                                                                                                                                        |                  |                 |                                                           |                                                                                                |


## backlog taches  :
- query sur un graph , comprendre la superposition
- mise en place neo4j
- NER Hybride** (Regex + LLM),
- Vectorisation : Embeddings ,
- RAG : Requêtage hybride
- Analyse critique + HITL
- Ré-ingestion si TBox évolue
- Fine-tuning modèles