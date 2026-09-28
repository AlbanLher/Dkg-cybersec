# Phase_Content.md — Phase 7 : L’Assistant SOC du Foyer (Micro-Agents & Télémétrie)


# Phase_Content.md — Phase 7 : L’Assistant SOC du Foyer & Agents Autonomes

## 1. Objectifs de la Phase
Mettre en œuvre une application SOC agentique capable de :
- Auditer un réseau domestique hétérogène (5 actifs).
- Charger dynamiquement les sources de menaces externes via un registre de configuration (`external_sources_config.json` dans `02-Donnees/Input_Phases/`).
- Interroger en live les flux CTI (structurés et non structurés).
- Exécuter le raisonnement sémantique (Phase 5) pour corréler les expositions locales (`TLP:RED`) et les menaces externes (`TLP:CLEAR`).
- Proposer un **Agent Conseil proactif** (pré-installation de logiciels, évaluation des dépôts et alternatives).

## 2. Étapes de Réalisation
1. **Cadrage & Spécifications :** Rédaction des SPEC-MET (UC07) et SPEC-TEC (Micro-agents et API agnostique).
2. **Configuration Externe :** Alimentation du registre de sources dans `02-Donnees/Input_Phases/external_sources_config.json`.
3. **Orchestration Live & Agents :** Exécution de l'agent CTI connecté au réseau, du scanner d'actifs locaux et du `ReasoningEngine`.
4. **Validation & Traçabilité :** Génération des snapshots RDF et des rapports d'auto-documentation.

## 1. Objectifs de la Phase
Mettre en œuvre une application agentique locale s'exécutant sur le PC personnel, capable de :
- Auditer un réseau domestique hétérogène (5 actifs aux profils variés).
- Structurer et valider la télémétrie locale sous un format rigoureux et immuable (Pydantic V2 / ABox TLP:RED).
- Corréler les faiblesses locales avec les flux CTI externes structurés (NVD/CAPEC - TLP:CLEAR).
- Orchestrer des micro-agents spécialisés pour produire un diagnostic de risque unifié et des recommandations actionnables pour le particulier.

## 2. Étapes de Réalisation
1. **Étape 1 - Cadrage & Spécifications :** Formalisation des spécifications (Transversal, Métier, Technique) dans `01-Principes_Spécifications/`.
2. **Étape 2 - Modélisation des Données d'Entrée :** Implémentation du fichier JSON d'entrée (`input_residential_family_env.json`) décrivant le parc d'actifs hétérogène.
3. **Emitter & Orchestration Agentique :** Développement des micro-agents (Local Inventory, External CTI, Correlation, Advisor/UI) pilotés par `Home_SOC_Orchestrator`.
4. **Étape 4 - Validation SHACL & Génération Turtle :** Export de l'ABox résidentielle (`DKG_ABox_Residential.ttl`) et génération du rapport d'auto-documentation associé (`.md`).

## 3. Livrables Attendus
Récapitulatif des Livrables Validés (Phase 7)
Les livrables de la Phase 7 sont désormais alignés sur une architecture découplée (Backend Python / API REST / IHM agnostique) et intègrent les exigences de robustesse (parsers défensifs et Pydantic V2 frozen=True) :
- Spécifications Métier (SPC-MET-P7-UC_INDIVIDUEL_01.md) :
	- Cadrage du réseau domestique (5 actifs hétérogènes).  MD
	- Formalisation du parcours de l'Agent Conseil (analyse d'exposition WAN, vérification des dépôts et arbitrage de pré-installation).  MD

- Spécifications Techniques (SPC-TEC-P7_TELEMETRIE_PME_01.md) :
	- Contrats d'API REST agnostiques pour séparer la logique d'analyse de l'interface utilisateur.
	- Règles de robustesse sur la lecture des propriétés (gestion des clés optionnelles et des dictionnaires tiers).

- Fichiers de Données et Configuration (02-Donnees/Input_Phases/Phase7_Residential_Box/) :
	- input_residential_family_env.json (Inventaire initial des actifs).
	- external_sources_config.json (Registre dynamique des flux CTI TLP:CLEAR).
	- 
- Scripts d'Orchestration et Snapshots :
	- home_soc_orchestrator.py / micro_agents_runner.py.  MD+ 1
	- Génération de l'ABox résidentielle validée sous DKG_ABox_Residential.ttl.   PY