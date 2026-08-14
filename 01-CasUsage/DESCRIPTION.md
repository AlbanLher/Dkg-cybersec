
📖 Histoire du Use Case : Alban et la Gestion des Vulnérabilités
"Comment une simple règle de sécurité peut devenir un casse-tête... et comment une ontologie bien conçue permet de le résoudre."

🎭 Personnages et Contexte
Personnage/Élément	Rôle	Description
Alban	Administrateur système	Gère un petit réseau personnel (1 PC, 1 routeur).
PC-Alban	Device	PC personnel avec OpenSSL 1.0.2 et Apache 2.4.57.
Router-Office	Device	Routeur du réseau local.
OpenSSL 1.0.2	Logiciel	Version vulnérable (CVE-2023-1234, CVSS 9.8).
Client-External-001	Device externe	PC d’un client qui se connecte au réseau d’Alban.
Server-Prod	Serveur interne	Ajouté en Phase 1, avec PostgreSQL 15.3.
Règle RGPD-32	Règle de conformité	"Tous les serveurs internes doivent avoir un score CVSS ≤ 5."
Contexte "Production"	Contexte	Environnement critique (règles strictes).
Contexte "Client Externe"	Contexte	Environnement moins contrôlé (tolérance plus élevée).
🌱 Phase 0 : Le POC Basique – "Un PC, Une Règle Simple"
Contexte :
Alban vient de découvrir qu’OpenSSL 1.0.2 (installé sur son PC) a une vulnérabilité critique (CVE-2023-1234, CVSS 9.8).
Il décide de modéliser son environnement pour mieux comprendre les risques.

Ce qu’il fait :

Il crée un graphe simple avec :

1 PC (PC-Alban) et 1 routeur (Router-Office).
2 logiciels : OpenSSL 1.0.2 et Apache 2.4.57.
1 vulnérabilité : CVE-2023-1234 (CVSS 9.8) liée à OpenSSL 1.0.2.
1 règle : "Mettre à jour OpenSSL vers 3.0.8".
Il visualise les liens :

PC-Alban a pour logiciel OpenSSL 1.0.2.
OpenSSL 1.0.2 est affecté par CVE-2023-1234.
CVE-2023-1234 nécessite l’action "Mettre à jour OpenSSL".
Résultat :
✅ Alban comprend immédiatement que son PC est vulnérable.
✅ Il sait quelle action prendre (mettre à jour OpenSSL).

Limites :
❌ Pas de différenciation entre les devices (tout est traité de la même façon).
❌ Pas de règles complexes (seulement des actions correctives basiques).

🏢 Phase 1 : La Micro-Entreprise – "Des Règles et des Serveurs"
Contexte :
Alban agrandit son réseau :

Il ajoute 2 employés (PC-Employee1, PC-Employee2) et 1 serveur (Server-Prod).
Il installe PostgreSQL 15.3 sur Server-Prod.
Il découvre que PostgreSQL 15.3 a aussi une vulnérabilité (CVE-2026-5678, CVSS 9.5).
Nouveau défi :
Alban veut appliquer des règles de conformité pour sa micro-entreprise.
Il décide :

"Tous les serveurs internes doivent avoir un score CVSS maximal de 5 pour être conformes au RGPD."

Problème :

Server-Prod a OpenSSL 1.0.2 (CVE-2023-1234, CVSS 9.8) ET PostgreSQL 15.3 (CVE-2026-5678, CVSS 9.5).
La règle est violée : Server-Prod a un CVSS > 5.
Ce qu’il fait :

Il enrichit son ontologie pour :

Différencier InternalDevice (PC des employés, serveur) et ExternalDevice (futurs clients).
Ajouter un statut de conformité (Conforme / Non conforme).
Ajouter des règles de conformité (ex: Compliance-CVSS-Low).
Il met à jour son graphe :

Server-Prod est marqué comme Non conforme (CVSS 9.8 > 5).
Les PC des employés sont Conformes (OpenSSL 3.0.8, CVSS bas).
Résultat :
✅ Alban peut identifier les devices non conformes.
✅ Il sait quelles vulnérabilités corriger en priorité.

Nouvelle limite :
❌ La règle "CVSS ≤ 5 pour les serveurs" est trop stricte :

En réalité, certains serveurs (ex: en test) peuvent avoir des CVSS plus élevés temporairement.
Mais Alban ne l’a pas encore réalisé...
💥 Phase 2 : Le Client Externe – "La Contradiction Apparente"
📌 Le Problème : Une Règle en Conflit avec la Réalité
Contexte :
Alban signe un contrat avec un client externe (Client-External-001).

Le client se connecte à Server-Prod pour accéder à une application.
Le client utilise OpenSSL 1.0.2 (même version vulnérable que Server-Prod).
Problème : Server-Prod et Client-External-001 partagent la même vulnérabilité (CVE-2023-1234, CVSS 9.8).
La contradiction :

Règle	Réalité	Conflit
"Tous les InternalDevice doivent avoir un CVSS ≤ 5."	Server-Prod (InternalDevice) a un CVSS 9.8.	❌ Violation de la règle
-	Client-External-001 (ExternalDevice) a aussi un CVSS 9.8.	❌ Mais ce n’est pas un InternalDevice !
Réaction initiale d’Alban :

"C’est une contradiction ! Ma règle est impossible à respecter si un client externe se connecte avec un logiciel vulnérable !"

Erreur d’Alban :
Il confond :

L’application stricte de la règle (sans nuance).
La réalité complexe (clients externes ≠ serveurs internes).
🔍 L’Analyse : Pourquoi Ce N’est PAS une Vraie Contradiction
Découverte :
En développant le contexte, Alban réalise que :

Server-Prod est un InternalDevice → Doit respecter CVSS ≤ 5.
Client-External-001 est un ExternalDevice → Ne doit pas respecter la même règle (car hors de son contrôle).
Solution :

Différencier les contextes :

Contexte "Production" : Règles strictes (CVSS ≤ 5 pour les InternalDevice).
Contexte "Client Externe" : Règles plus tolérantes (CVSS ≤ 7 pour les ExternalDevice).
Ajouter des exceptions :

Si un InternalDevice a un CVSS > 5 temporairement (ex: migration en cours), on peut ajouter une dérogation (Waiver) avec justification.
Exemple concret :

Server-Prod (InternalDevice) :

CVSS : 9.8 (via OpenSSL 1.0.2).
Contexte : Production.
Statut : Non conforme MAIS avec une dérogation (justifiée par : "Migration vers OpenSSL 3.0.8 prévue pour le 2026-09-01. Client-External-001 dépend de cette version pendant la transition.").
Client-External-001 (ExternalDevice) :

CVSS : 9.8 (via OpenSSL 1.0.2).
Contexte : Client Externe.
Statut : Conforme (car la règle pour les ExternalDevice tolère un CVSS ≤ 7).
✅ La Résolution : Enrichir l’Ontologie avec des Nuances
Ce qu’Alban fait :

Ajoute des classes :

:Context (Production, Client Externe, Test).
:Waiver (Dérogation temporaire).
Ajoute des propriétés :

:inContext (lie une règle ou un device à un contexte).
:hasWaiver (lie un device à une dérogation).
Met à jour les règles :

Règle 1 : "CVSS ≤ 5 pour les InternalDevice en contexte Production."
Règle 2 : "CVSS ≤ 7 pour les ExternalDevice en contexte Client Externe."
Applique les dérogations :

Server-Prod a une dérogation pour OpenSSL 1.0.2 (justifiée par la migration).
Résultat final :
✅ Plus de contradiction : Chaque device est évalué dans son contexte.
✅ Explicabilité : Alban (et son équipe) comprennent pourquoi Server-Prod est une exception.
✅ Évolutivité : Si un nouveau contexte apparaît (ex: "Test"), il peut l’ajouter sans casser l’existant.

🧩 Morale de l’Histoire : Pourquoi l’Ontologie est Cruciale
🔴 Sans Ontologie (Approche "En Vrac")
a

affecté par

CVSS 9.8

doit respecter

Server-Prod

OpenSSL 1.0.2

CVE-2023-1234

❌ PROBLÈME : Règle violée !

Règle CVSS ≤ 5

→ Résultat :

On ajoute une exception manuelle dans un fichier Excel.
Personne ne sait pourquoi Server-Prod est une exception.
Impossible de reproduire la logique pour un nouveau serveur.
🟢 Avec Ontologie (Votre Approche)
a

affecté par

CVSS 9.8

est dans le contexte

a une dérogation

justifiée par

applique la règle

viole

résout

Server-Prod

OpenSSL 1.0.2

CVE-2023-1234

Vulnérabilité

Production

WAIVER-001

Migration vers OpenSSL 3.0.8

CVSS ≤ 5

→ Résultat :

Tout est structuré : On sait pourquoi Server-Prod est une exception.
Reproductible : La même logique s’applique à un nouveau serveur.
Évolutif : On peut ajouter de nouveaux contextes (ex: "Test") sans tout recoder.
🎯 Leçons Apprises (À Retenir pour le POC)

ConceptSans OntologieAvec OntologieBénéfice
Contradiction On ignore ou On enrichit le Explicabilité
apparenteon ajoute une modèle pour
exception sans capturer la nuance.
explication.
Règles complexesLes règles sont Les règles sont Précision
isolées et difficiles liées à un contexte.
à appliquer.
Évolution du On ajoute des On met à jour Maintenabilité
systèmedonnées sans l’ontologie +
schéma → migrations →
désordre.cohérence.
Collaboration"Pourquoi ce "Pourquoi ce Transparence
serveur est-il une serveur est-il une
exception ?" → exception ?" →
Réponse : "Je ne Réponse : "Voir
sais pas."WAIVER-001, justifiée par [raison]."
Vectorisation/NERLes modèles Les modèles Qualité des
ignorent les apprennent les données
nuances (ex: nuances via
"contexte").l’ontologie.
📌 Résumé des 3 Phases en 1 Schéma
📖 Intégration dans Votre Projet
Phase 2 : Startup + RGPD

a

affecté par

CVSS 9.8

dans le contexte

a une dérogation

justifiée par

applique

viole

résout

Server-Prod

OpenSSL 1.0.2

CVE-2023-1234

Vulnérabilité

Production

WAIVER-001

Migration en cours

Règle: CVSS ≤ 5

Phase 1 : Micro-Entreprise

a

affecté par

CVSS 9.8

violation de

Server-Prod

OpenSSL 1.0.2

CVE-2023-1234

❌ Non conforme

Règle: CVSS ≤ 5

Phase 0 : POC Basique

a

affecté par

CVSS 9.8

PC-Alban

OpenSSL 1.0.2

CVE-2023-1234

⚠️ Vulnérable

Phase0 -->|Évolution| Phase1 -->|Contradiction apparente| Phase2 -->|Résolution| 

📖 Intégration dans Votre Projet
📌 Où Placer Cette Histoire ?
 1. Dans 01-CasUsage/DESCRIPTION.md :
- Remplacez le contenu existant par cette histoire.
- Ajoutez un lien vers les implémentations techniques (Phase 0/1/2) dans 03-Implementation/.
 2. Dans le README.md du dépôt :
- Ajoutez un résumé avec un lien vers 01-CasUsage/DESCRIPTION.md :
## 📖 Histoire du Use Case
Pour comprendre **pourquoi et comment** ce projet a évolué, lisez :
→ [Histoire d'Alban et la Gestion des Vulnérabilités](01-CasUsage/DESCRIPTION.md)


---
old
---


# Cas d'Usage : Cybersécurité (Individu → Micro-Entreprise)

## 🎯 Scénario
**Problématique** : Gérer les vulnérabilités logicielles et appliquer des règles de sécurité adaptées à son environnement.

**Exemple** :
- **Individu** : 1 PC + 1 routeur → Détecter les CVE critiques.
- **Micro-entreprise** : +2 employés + 1 serveur → Appliquer RGPD/NIS2.

## 📌 Données
### Publiques
- [CVE](https://cve.mitre.org/) : Vulnérabilités.
- [MITRE ATT&CK](https://attack.mitre.org/) : Tactiques/Techniques.
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) : Bonnes pratiques.

### Privées (à générer)
- Inventaire des devices (PC, routeur, serveur).
- Logiciels installés (OpenSSL, Apache, etc.).
- Règles internes (ex: "Bloquer le port 22").
