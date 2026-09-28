## 1. Contexte & Problématique

Dans le cadre du projet **DKG-CyberSec**, nous concevons un système SOC souverain, _Air-Gapped_ et orienté graphe de connaissances, piloté par des agents LLM.

Jusqu'à présent, l'exposition des services reposait sur des architectures API-first traditionnelles (FastAPI). Bien que robustes pour des intégrations web classiques, ces architectures présentent des limites structurelles lorsqu'il s'agit d'être pilotées par des agents autonomes :

- **Surcharge contextuelle ("Context Stuffing") :** Nécessité de fournir de lourdes documentations (OpenAPI/Swagger) aux LLMs pour leur expliquer comment appeler les routes.
    
- **Complexité d'intégration :** Écriture de code de "glue" ad-hoc pour chaque nouvel outil mis à disposition de l'intelligence artificielle.
    
- **Gaspillage énergétique :** Multiplication des couches de transport HTTP et maintien de serveurs web permanents, en contradiction avec notre exigence de **Green Dev**.
    

## 2. Décision : Adoption du Model Context Protocol (MCP)

Il a été décidé d'adopter le **Model Context Protocol (MCP)**, initié par Anthropic, comme standard d'interopérabilité entre les agents LLM et le socle technique du graphe de connaissances.

Cette adoption s'articule autour de deux axes :

1. **Préparation immédiate (Phase 8) :** Structuration des scripts et modules (dossier `core/` et dossiers de phases `phases/`) selon des contrats d'interface stricts et typés, prêts à être wrappés en tant qu'outils (`Tools`) et ressources (`Resources`) MCP.
    
2. **Déploiement natif (Vague 5) :** Intégration complète du SDK MCP pour permettre une navigation agentique dynamique dans le graphe RDF.
    

## 3. Justifications & Valeur Ajoutée

### A. Sobriété Numérique & Green Dev

- **Découverte dynamique :** L'agent n'ingère pas de documentation monolithique en permanence ; il interroge à la demande les schémas stricts des outils mis à disposition, réduisant drastiquement la consommation de tokens et de calculs LLM.
    
- **Transport local `stdio` :** Capacité à exécuter les outils sous forme de processus locaux isolés via les flux d'entrées/sorties standard, **sans ouvrir le moindre port réseau**. Cela renforce la posture _Air-Gapped_ tout en supprimant l'overhead énergétique des serveurs permanents.
    

### B. Synergie avec le Filtrage Frugal (Phase 8)

Le couplage entre le protocole MCP et notre approche de filtrage frugal (`frugal_filter.py`) garantit que seuls des deltas de données extrêmement légers (ex: 42 Ko, 84 triplets) transitent et sont analysés en mémoire, respectant strictement le plafond `MAX_TRIPLES_IN_MEMORY`.

## 4. Conséquences et Consignes d'Implémentation

- **Standardisation du code :** Tout nouveau module développé dans le cadre des phases (à partir de la Phase 8) doit respecter un typage rigoureux (Pydantic / Type Hints) et être pensé pour une exposition future via MCP.
    
- **Dualité FastAPI / MCP :**
    
    - **FastAPI** conserve son rôle de passerelle API externe et d'interface web/REST globale.
        
    - **MCP** devient la couche d'abstraction souveraine dédiée aux interactions agentiques et à la manipulation fine du graphe de connaissances.