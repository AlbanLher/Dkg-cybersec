# Phase 6 — API Gateway Cross-TLP & Security Engine

# Phase 6 — API Gateway Cross-TLP & Security Engine

## 1. Objectifs de la Phase
- Exposer une interface d'interrogation dynamique (SPARQL & abstractions GraphQL/JSON) sur le graphe unifié DKG.
- Implémenter un moteur d'isolation dynamique et strict des accès en fonction du niveau d'habilitation TLP de l'appelant (TLP:CLEAR, TLP:AMBER, TLP:RED).
- Garantir le principe de non-fuite d'information (Information Leakage Prevention) : un jeton TLP:CLEAR ne doit jamais percevoir l'existence ou les relations vers des entités TLP:AMBER ou TLP:RED.
- Assurer la traçabilité complète des requêtes via un journal d'audit en Snapshot et Master (`api_gateway_audit.log`).

## 2. Étapes de Réalisation
1. **Étape 1 (Cadrage & Contrats) :** Formalisation des spécifications (FWK et TEC), schémas Pydantic V2 d'habilitation et contrats de requêtes.
2. **Étape 2 (Sous-graphes TLP) :** Construction dynamique des sous-graphes d'union selon le contexte d'habilitation TLP (CLEAR / AMBER / RED).
3. **Étape 3 (Moteur de Filtrage SPARQL) :** Validation et exécution des requêtes SPARQL sur le graphe filtré.
4. **Étape 4 (Validation SHACL & Non-Régression) :** Contrôle de conformité SHACL sous Closed World Assumption (CWA) et exécution de la suite PyTest.
5. **Étape 5 (Auto-Documentation & Replay) :** Génération des bilans `.md` et synchronisation Snapshots / Masters.

## 3. Livrables Attendus
- `00-Projet/Phase6/Phase_Content.md`
- `00-Projet/Phase6/Memo_UseCase_Phase6.md`
- `01-Principes_Spécifications/TRANSVERSAL/SPEC-FWK-P6_Matrice_Habilitations_TLP.md`
- `01-Principes_Spécifications/USECASE_TECHNIQUE/SPEC-TEC-P06_API_Gateway_TLP.md`
- `02-Donnees/Input_Phases/Phase6_API_Gateway/sample_query_payloads.json`