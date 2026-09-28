Le paramétrage du filtrage et de la haute densité sémantique repose directement sur les variables centralisées dans le fichier de configuration unique (**SSOT**), situé dans `03-Application/core/config.py`.

Voici comment ce filtrage est finement configuré pour concilier sobriété (_Green-by-Design_) et précision :

### 1. Les Seuils et Modèles Clés dans `config.py`

Le comportement du filtrage et du rapprochement repose sur plusieurs paramètres configurables :

- **Le Seuil de Similarité Sémantique (`mitm_similarity_threshold`) :**
    
    - **Valeur par défaut :** `0.85` (sur une échelle de `0.0` à `1.0`).
        
    - **Rôle :** C'est le filtre de densité absolue. Seuls les éléments externes dont la proximité vectorielle avec le socle interne dépasse 85 % de similarité sont retenus pour les propositions d'enrichissement. Cela évite d'ingérer du bruit inutile.
        
- **Le Moteur d'Embeddings Local (`embedding_model_name`) :**
    
    - **Modèle par défaut :** `sentence-transformers/all-MiniLM-L6-v2` (stocké localement dans `models/cache/embeddings/`).
        
    - **Rôle :** Il transforme les descriptions textuelles et les concepts CTI en vecteurs numériques denses, permettant le calcul de distance cosinus sans aucune connexion externe (_Air-Gapped_).
        
- **Les Modèles de Reconnaissance d'Entités (`ner_model_name`) :**
    
    - **Modèles par défaut :** `urchade/gliner_large-v2.1` (et son modèle de repli `dslim/bert-base-NER` stocké dans `models/cache/ner/`).
        
    - **Rôle :** Ils structurent les flux bruts non structurés (bulletins, rapports) en extrayant les entités clés (menaces, vulnérabilités, actifs) avant le passage dans le filtre frugal.
        

### 2. Comment s'articule ce filtrage au niveau des moteurs (`core/`) ?

1. **La Frugalité en amont (`frugal_engine.py`) :** Le moteur applique un premier écrémage syntaxique et structurel sur les gros flux publics (MITRE/CVE) pour ne conserver que les paquets de données touchant directement le périmètre de l'organisation.
    
2. **La Densité Sémantique (`mitm_engine.py`) :** Les paquets retenus sont vectorisés grâce au modèle d'embedding local. L'agent applique le seuil `mitm_similarity_threshold = 0.85` : si un concept externe correspond à un concept existant de la TBox à plus de 85 %, il génère un alignement de type `skos:exactMatch`.
    
3. **Le Tampon de Delta :** Le résultat de ce filtrage haute densité est consigné dans un fichier tampon léger (`frugal_delta_buffer.ttl`), prêt à être audité par l'**Agent Gardien TBox** et soumis à la validation de l'analyste via la passerelle **HitM**.