# DKG Cybersécurité - Démonstrateur

**Objectif** : Créer un Dynamic Knowledge Graph pour la gestion des vulnérabilités et règles de sécurité, évoluant d'un individu à une micro-entreprise.

## 🎯 Périmètre
- **Cas d'usage** : Détection et correction de vulnérabilités (CVE, MITRE ATT&CK).
- **Données** :
  - Publiques : CVE, MITRE, OWASP.
  - Privées : Inventaire des devices/logiciels (générés).
- **Outils** :
  - Graphe : Neo4j (local).
  - Ontologie : OWL/TTL + Protégé.
  - Vectorisation : Sentence Transformers (`all-MiniLM-L6-v2`).
  - NER : spaCy (modèle personnalisé).

## 🔗 Liens Utiles
- [Dépôt GitHub](https://github.com/alban-lhermine/dkg-cybersec)
- [Neo4j Docs](https://neo4j.com/docs/)
- [MITRE ATT&CK](https://attack.mitre.org/)
