exemple d'utilisation des prompt 
#### Cas 1 : Tu veux qu'on développe du code (Python / Pytest / Turtle)

Tu tapotes simplement ceci dans ton message :

> **[CONTEXT: DEV]**
> 
> Peux-tu me proposer le script `03-Application/queries_sparql.py` pour exécuter nos premières requêtes CTI ?

_(Dès que je vois `[CONTEXT: DEV]`, je sais que je dois respecter strictement `config.py`, la syntaxe `rdflib` et ajouter les `@prefix` Turtle)._

#### Cas 2 : On termine une phase et on veut faire le ménage

Tu m'envoies :

> **[CONTEXT: RETRO]**
> 
> Les tests Pytest passent tous. Faisons le bilan 5S de la Phase 2.5 et mettons à jour la Roadmap.

_(Dès que je vois `[CONTEXT: RETRO]`, j'adopte la posture d'audit : contrôle du code mort, vérification des fiches de synthèse Markdown et mise à jour du backlog)._

#### Cas 3 : On rédige des spécifications ou du cadrage

Tu m'envoies :

> **[CONTEXT: SPEC]**
> 
> On démarre la Phase 3. Rédigeons la fiche `SPEC-04_Moteur_Inference.md`.

_(Dès que je vois `[CONTEXT: SPEC]`, je me concentre uniquement sur la modélisation fonctionnelle, les cas d'usage et les diagrammes, sans produire de code d'application)._



### 🚀 Procédure idéale pour ouvrir la nouvelle session

Dans votre nouveau chat, il vous suffira de suivre ces 3 étapes simples :

#### Étape 1 : Injection du Master Prompt (Premier message)

Collez le contenu de `00-Projet/Prompts/SYSTEM_MASTER_PROMPT.md` pour fixer les règles immuables (`config.py`, `@prefix`, SSOT).

#### Étape 2 : Re-synchro rapide de l'état actif

Ajoutez un court résumé de 3 lignes sur le point de départ :

> _"Phase 2.5 validée par Pytest. Le fichier `config.py` est la SSOT officielle. Nous démarrons la Phase 3 (SPARQL & Moteur d'inférence)."_

#### Étape 3 : Activation du module voulu via l'Alias

Formulez votre premier besoin avec le tag approprié :

> **`[CONTEXT: SPEC]`** _(si vous souhaitez rédiger les cadrages/spécifications de la Phase 3)_
> 
> **ou**
> 
> **`[CONTEXT: DEV]`** _(si vous souhaitez directement coder les scripts Python/SPARQL de la Phase 3)_

Cette transition nette permettra de démarrer la Phase 3 sur des bases optimales et parfaitement réactives.