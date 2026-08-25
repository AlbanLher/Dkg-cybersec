
| **Concepts/Fonctions**                   | **Phase** | **Data**                                  | **Scripts**                         | **Tests**            | **Commentaire**       | Livrable |
| ---------------------------------------- | --------- | ----------------------------------------- | ----------------------------------- | -------------------- | --------------------- | -------- |
| **Lexique, Sémantique, Ontologie, TBox** | 1         | inventory.json, CVE_data.ttl, FIRST, MISP | `build_tbox.py`, `validate_tbox.py` | `test_tbox.py`       | Base du DKG           |          |
| **3 versions TBox** (.ttl, .md, .json)   | 1         | '-                                        | `generate_versions.py`              | `test_versions.py`   | Pour machines/humains |          |
| **Données instanciées (ABox)**           | 2         | inventory.json étendu, CVE feed           | `orchestrator_phase1.py`            | `test_abox.py`       | Instances concrètes   |          |
| **NER Hybride** (Regex + LLM)            | 3         | Rapports PDF/MD, Logs                     | `ner_pipeline.py`                   | `test_ner.py`        | Extraction d'entités  |          |
| **Vectorisation**                        | 4         | Embeddings locaux                         | `vectorizer.py`                     | `test_vectorizer.py` | Indexation Neo4j      |          |
| **Analyse critique + HITL**              | 5         | Nouvelles données                         | `agent_guard.py`                    | `test_agent.py`      | Validation humaine    |          |
| **Ré-ingestion si TBox évolue**          | 5         | Toutes données                            | `reingest_pipeline.py`              | `test_reingest.py`   | Cohérence ABox/TBox   |          |
| **Fine-tuning modèles**                  | 6         | Données labellisées                       | `fine_tune.py`                      | `test_fine_tune.py`  | Cloud si nécessaire   |          |
