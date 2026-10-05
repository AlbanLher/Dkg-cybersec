---
type: spec
reference: SPC-MET-P8-compliance_rgpd_01
revision: 1
titre: Conformité & Preuve Réglementaire RGPD (Art. 32)
titre_court: compliance_rgpd
description: Expression des règles métier de non-conformité réglementaire appliquées aux actifs du foyer.
phase_code: P9
phase_nom: Orchestration MCP & Moteurs d'Agents Souverains
statut: 🟡 ACTIVE
portee: USECASE_METIER
public_vise:
  - Analystes CTI / SOC
  - Architectes Ontologues
exigences:
  - id: EXG-MET-P8-com_1
    code_exigence: EXG-P8-02
    domaine: QU
    domaine_nom: Qualité & Conformité
    core: true
    phase: P8
    titre: Qualification Non-Conformité
    critere: Association actif -> standard RGPD
    test: Pytest / SPARQL
---

# 📜 Conformité & Preuve Réglementaire RGPD (Art. 32) 
## 1. Résumé Exécutif & Glossaire 
Formalisation des exigences fonctionnelles permettant d'associer un constat de vulnérabilité technique à un manquement réglementaire légal (RGPD Article 32 - Sécurité du traitement). 
## 2. Règles Métier 
- **Lien de Violation :** Établissement d'un triplet d'inférence sécurisé en `TLP:RED`. 
- **Zéro fuite normative :** Le référentiel public reste strictly étanche en `TLP:CLEAR`. 
## 3. Matrice des Exigences 
| Identifiant   | UID              | Domaine | Core/Non-Core | Intitulé                     | Description                        | Mode de Test    |
| :------------ | :--------------- | :------ | :------------ | :--------------------------- | :--------------------------------- | :-------------- |
| **EXG-P8-02** | EXG-MET-P8-com_1 | `QU`    | Core          | Qualification Non-Conformité | Association actif -> standard RGPD | Pytest / SPARQL |
# 📜 Conformité & Preuve Réglementaire RGPD (Art. 32)

## 1. Règles Métier de Qualification (OK / KO)
- **État Conforme (OK) :** Les actifs audités dans l'ABox (`TLP:RED`) respectent les exigences de sécurité formalisées dans la TBox validée (absence de CVE critique non traitée, services cloisonnés).
- **État Non Conforme (KO) :** Tout actif présentant un risque d'exposition critique ou une faille non corrigée viole l'exigence normative (ex: `dkg:violatesStandard` pointant vers l'Article 32 du RGPD).
- **Traçabilité des Remédiations :** Le statut KO s'accompagne obligatoirement d'une prescription sémantique d'action de mitigation issue de l'enrichissement validé.