# 📝 Changelog — DKG-CyberSec

Toutes les modifications notables de ce projet sont documentées dans ce fichier.
Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/) et le projet adhère au versioning sémantique ([SemVer](https://semver.org/spec/v2.0.0.html)).


| Date       | Release | Comment                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ---------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 10/09/2026 | v1.0.0  | First release.  Scope : Roadmap Wave 1 & 2.<br>Purpose : Step in with  first principles :  Graph, RTF/OWL standards, TLP & confidentiality management                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| 22/09/2026 | v1.1.0  | Vague 3 : Industrialisation & Première Application :                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| 18/10/2026 | v1.2.0  | Vague 4 - Phase 8 : Structure Applicative MCP sur première partie du role SOC **SOC_1** (Actifs, Vulnérabilités, Menaces),<br>Objectif : <br>- Amélioration du démonstrateur permettant d'illustrer l'articulation données publique et privées autour des standars OWL..<br>- Illustration de connexion aux données externe (Bulletin ANSSI, Rapport CISA ...)<br>- Confrontation à la TBox, demande de validation de mise a jour et identification des vulnerabilité. <br>- Présentation de l'analyse resultant de la superposition des graphs avec pour chaque vulnérabilité un graphique.<br>       _( Deux cas prédéfinis plus le scan du PC hôte de l'installation.)_<br>- Traçabilité : extension à la traçabilité exigence  - <-> design <br> |
|            |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

---

## [1.2.0] — (Clôture de la Phase 8 de la Vague 4)
### 🚀 Nouveautés 
- **MCP** vient compléter l'API Gateway : 
- **Renforcement des illustration sur cas d'usage**
  - Priorité mise à l'illustration de l’intégration de données externes réelles non simulées. (Mais toujours compatible d'une gestion de sécurité complète TLP )
  - Illustration d'évolution de TBox suite à l'ingestion de données externe. 
  - 3 cas de détection de vulnérabilités: mot-clés , formelle complète, formelle partielle ( Modification TBox non acceptée par le SOC)
  - Le cas du PC local est désormais un scan du PC Hôte dont les données sont dans `.gitignore` non transmises.

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

