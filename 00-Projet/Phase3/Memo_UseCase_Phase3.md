Ce document formalise la valeur d'affaires du raccordement multi-TLP entre le SI interne (`TLP:RED`) et les flux de menaces externes (`TLP:CLEAR`).



# 🎯 Use Case Phase 3 - Réconciliation Multi-TLP et Enrichissement CTI

## 📌 Objectif Métier
Le but de ce use case est de valider le croisement de données hautement confidentielles du SI (**ABox TLP:RED**) avec des flux d'intelligence sur les menaces issus de sources ouvertes (**ABox CTI TLP:CLEAR**) sans compromettre la compartimentation des secrets.

---

## 🏛️ Modèle d'Isolation et de Raccordement Cross-TLP

L'architecture s'appuie sur une séparation stricte des graphes RDF par classification TLP :

```

┌────────────────────────────────────────┐ ┌────────────────────────────────────────┐

│ ABox Interne SI (TLP:RED) │ │ ABox CTI Externe (TLP:CLEAR) │

│ data:Asset-Srv-Auth-02 │ │ cti:CVE-2021-44228 │

│ └─ dkg:hasInstalledComponent │ │ ├─ dkg:cvssScore 10.0 │

│ └─ data:Comp-Log4j-2-14 │ │ └─ dkg:hasWeakness cti:CWE-502 │

└──────────────────┬─────────────────────┘ └──────────────────┬─────────────────────┘

│ │

└─────────── dkg:hasVulnerability ───────────────┘

(Lien Cross-TLP)

````

| Périmètre    | Classification | Contenu                                        | Répertoire Master SSOT                       |
| :----------- | :------------- | :--------------------------------------------- | :------------------------------------------- |
| **ABox SI**  | `TLP:RED`      | Infrastructure, serveurs, composants installés | `Master_Transversal/TLP_RED_Instances_ABox/` |
| **ABox CTI** | `TLP:CLEAR`    | Référentiels CVE, CWE, CAPEC et scores CVSS    | `Master_Transversal/TLP_CLEAR_CTI_External/` |

---

## 🔍 Requête SPARQL Cross-TLP (Détection d'Exposition Critique)

Cette requête fédère les deux graphes pour identifier les serveurs internes exposés à des vulnérabilités critiques (CVSS >= 9.0) issues des flux externes :

```sparql
PREFIX dkg:  [http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)
PREFIX data: [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#)
PREFIX cti:  [http://dkg.cybersec.org/cti#](http://dkg.cybersec.org/cti#)

SELECT ?asset ?component ?cve ?cvssScore ?capec WHERE {
    # 1. Périmètre Interne (TLP:RED)
    ?asset a dkg:Asset ;
           dkg:hasInstalledComponent ?component .
           
    # 2. Jointure Interne -> Externe
    ?component dkg:hasVulnerability ?cve .
    
    # 3. Périmètre Externe CTI (TLP:CLEAR)
    ?cve a dkg:Vulnerability ;
         dkg:cvssScore ?cvssScore .
         
    OPTIONAL {
        ?cve dkg:hasWeakness ?cwe .
        ?cwe dkg:hasThreatPattern ?capec .
    }
    
    # Filtre sur la sévérité
    FILTER(?cvssScore >= 9.0)
}
ORDER BY DESC(?cvssScore)
````

## 🛡️ Règles de Gouvernance

1. **Étancheité TLP :** Un export `TLP:CLEAR` ne doit sous aucun prétexte contenir de triplets décrivant un `dkg:Asset` du SI.
    
2. **Cycle de Vie :** La mise à jour des flux NVD/CAPEC en `TLP:CLEAR` s'effectue indépendamment du rythme de mise à jour des inventaires d'actifs en `TLP:RED`.
    


---

### Séquence d'Exécution Complète Phase 3

```bash
# 1. Génération du graphe CTI depuis les flux JSON d'entrée
python 03-Application/Phase3/generate_phase3_cti.py

# 2. Génération de la documentation de synthèse
python 03-Application/Phase3/export_phase3_cti_md.py

# 3. Exécution des tests de parité et de conformité
python -m pytest 03-Application/Test/ -v
````