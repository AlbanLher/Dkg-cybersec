# Phase 6 : API Gateway SPARQL/GraphQL & Ségrégation TLP

## 1. Objectifs Fonctionnels & Techniques
- **Passerelle de Requêtage Sécurisée** : Exposer une API unifiée (endpoints SPARQL/GraphQL) permettant d'interroger le DKG-CyberSec.
- **Filtrage Dynamique par Marquage TLP** : Garantir l'isolation des données selon les habilitations du client (CLEAR, AMBER, RED) sans fuite de contexte inter-calques.
- **Moteur Graphique Multi-Niveaux** : Permettre des requêtes ciblant les sous-graphes (TBox, ABox Interne, CTI Externe, Graphe Inféré).

## 2. Étapes de Déploiement
1. **Cadrage & Spécifications (Étape 1)** : Validation du schéma Pydantic V2 de sécurité et de la matrice de contrôle d'accès TLP dans `01-Principes_Spécifications/USECASE_TECHNIQUE/`.
2. **Implémentation API (Étape 2)** : Développement de `api_gateway.py` avec FastAPI/GraphQL et filtrage dynamique SPARQL (Graph Union filtré).
3. **Tests & Recette (Étape 3)** : Exécution de `test_phase6_api.py` (PyTest) pour valider l'étanchéité des rôles CLEAR/AMBER/RED et la conformité des réponses[cite: 1].

## 3. Livrables Attendus
- `00-Projet/Phase6/Phase_Content.md`
- `00-Projet/Phase6/Memo_UseCase_Phase6.md`
- `01-Principes_Spécifications/USECASE_TECHNIQUE/SPEC-TECH-UC06_API_Gateway_CrossTLP.md`
- `03-Application/Phase6/schemas.py`
- `03-Application/Phase6/api_gateway.py`
- `03-Application/Test/test_phase6_api.py`