# 📜 SPEC-METIER-UC03 — Ingestion & Traitement de l'Intelligence sur les Menaces (CTI)

> **Classification** : `TLP:CLEAR`
> **Statut** : 🟢 Approuvé
> **Niveau d'Abstraction** : 🔵 USECASE_METIER
> **Public Cible** : Analystes CTI, Opérateurs SOC, Responsables Threat Intelligence
> **Domaine Principal** : `CT` | `QU` | `SE`
> **Matrice de Rattachabilité** : `EXG-CT-01`, `EXG-NER-01`, `EXG-NER-02`, `EXG-SE-03`

---

## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif
Cette spécification définit le cadre fonctionnel pour l'ingestion, la qualification et la normalisation des flux de renseignement sur les menaces (CTI) ouverts (NVD, CISA KEV, bulletins d'alerte)[cite: 10, 11]. Elle permet au SOC de transformer des données non structurées (rapports textuels, blogs CTI) en faits RDF structurés directement exploitables par le DKG[cite: 11].

### 1.2 Glossaire Métier & Technique
| Acronyme / Concept | Définition | Contexte DKG |
| :--- | :--- | :--- |
| **CTI** | Cyber Threat Intelligence | Renseignement sur les menaces, vulnérabilités et acteurs d'attaque[cite: 10]. |
| **Bulletin CTI Non-Structuré** | Rapport textuel d'analyse | Texte brut décrivant une campagne d'attaque sans formatage RDF initial[cite: 11]. |
| **Normalisation SKOS** | Alignement terminologique | Résolution d'acronymes ou alias (*"Cozy Bear"*, *"APT29"*) vers une URI canonique[cite: 10, 11]. |

---

## 🎯 2. Périmètre & Rôle de la Spécification

* **Positionnement dans l'Architecture** : Niveau 2 (Cas d'Usage Métier). Spécifie les besoins fonctionnels des équipes CTI/SOC pour l'ingestion externe[cite: 10, 14].
* **Gouvernance & Validation** : Validé par le Responsable CTI et le Lead Architecte Sémantique[cite: 10, 14].

---

## 📐 3. Spécifications Formelles

### 3.1 Scenario Métier & Workflow Ingestion CTI