# 📝 Changelog — DKG-CyberSec

Toutes les modifications notables de ce projet sont documentées dans ce fichier.
Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/) et le projet adhère au versioning sémantique ([SemVer](https://semver.org/spec/v2.0.0.html)).


| Date       | Release | Comment                                                                                                                                               |
| ---------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 10/09/2026 | v1.0.0  | First release.  Scope : Roadmap Wave 1 & 2.<br>Purpose : Step in with  first principles :  Graph, RTF/OWL standards, TLP & confidentiality management |
| 22/09/2026 | v1.1.0  | Vague 3 : Industrialisation & Première Application :                                                                                                                                                    |




---

## [1.1.0] — (Clôture de la Vague 3)
### 🚀 Nouveautés (Vague 3 : Industrialisation & Première Application)
- **API Gateway (Phase 6) :** 
  - Implantation d'une passerelle API sécurisée et agnostique.
  - Mise en place d'un filtrage dynamique et étanche des flux selon les niveaux de classification TLP (`CLEAR`, `AMBER`, `RED`).
  - Journalisation des accès via un système d'audit traçable (`api_gateway_audit.log`).
- **Micro-Agents & Cas d'Usage Résidentiel (Phase 7) :**
  - Ingestion, modélisation et validation structurelle des 5 actifs du foyer connecté (`input_residential_family_env.json`).
  - Analyse formelle de l'exposition WAN couplée aux bases CTI TLP:CLEAR.
  - Découplage complet entre la logique backend Python et l'IHM / HMI (permettant un client Streamlit ou JavaScript).
- **Architecture & Robustesse :**
  - Généralisation de l'immutabilité des objets (`frozen=True`) sous Pydantic V2.
  - Intégration du socle de développement *Green-by-Design* (`EXG-GREEN-01`, `02`, `03`) garantissant une sobriété matérielle et un mode *Local-First* sur des postes standards (PC 16 Go RAM sans GPU, Air-Gapped).

---

## [1.0.0] — (Clôture de la Vague 2)
### 🎉 Version Initiale Stable
- **Socle Sémantique & TBox (Phase 1) :**
  - Ontologie Master OWL2 (`TLP:AMBER`) et validation formelle sous formes SHACL (CWA).
- **Cartographie ABox Interne (Phase 2) :**
  - Modélisation de la topologie d'un poste individuel (`TLP:RED`).
- **Ingestion CTI Structurée & Non-Structurée (Phases 3 & 4) :**
  - Intégration des flux NVD, CAPEC et CISA KEV (`TLP:CLEAR`).
  - Extracteur NER local Air-Gapped avec score de confiance.
- **Agent MITM & Inférence (Phase 5) :**
  - Moteur de réconciliation cosinus (`all-MiniLM-L6-v2`, seuil $\ge 0.85$) et matérialisation des cascades de risques.
