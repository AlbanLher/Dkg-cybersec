Les 3 premiers documents décrivent **ce que les formats doivent contenir** (le _quoi_ par phase). Ce 4ᵉ document décrit **comment vérifier automatiquement la chaîne globale** (le _comment_ transverse) :

- **Matrice de Traçabilité** : Table croisée associant une règle TBox à sa Shape SHACL et son test SPARQL ASK.
    
- **Stratégie de Test & CI/CD** : Définition des scripts de vérification locaux (`verify_abox.py`, `pyshacl`, `pytest`).
    
- **Assertions de pré-requis (Pre-flight checks)** : Règles d'interruption du pipeline si un graphe orphelin est détecté.