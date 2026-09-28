# 🎯 Use Case Phase 2 - Analyse d'Impact et Traçabilité Cyber (TLP:RED)


## 📌 Objectif Métier
Le but de ce use case est de valider la capacité du graphe **DKG-CyberSec** à lier dynamiquement une ressource informatique physique du SI (**Asset**) jusqu'aux schémas d'attaques théoriques (**CAPEC**) à travers son exposition logicielle.

---

## 🏗️ Alignement TBox & Rôles des Concepts

Chaque instance générée dans l'ABox dérive strictement d'une classe formelle du socle `DKG_TBox_Master.ttl` :

| Concept TBox (`dkg:`) | Instance ABox (`dkg-data:`) | Rôle Métier / Gouvernance |
| :--- | :--- | :--- |
| `dkg:Asset` | `dkg-data:Asset-Srv-Prod-01` | Équipement cible hébergeant des données sensibles (Classé `TLP:AMBER`). |
| `dkg:SoftwareComponent` | `dkg-data:Comp-Apache-2-4` | Brique applicative déployée sur l'actif. |
| `dkg:Vulnerability` | `dkg-data:CVE-2021-41773` | Faille de sécurité publique associée à la version du composant. |
| `dkg:Weakness` | `dkg-data:CWE-22` | Catégorie de défaut logiciel (*Path Traversal*). |
| `dkg:ThreatPattern` | `dkg-data:CAPEC-126` | Vecteur d'attaque utilisable par un attaquant pour exploiter la faiblesse. |

---

## 🔍 Scénario de Validation SPARQL (Traçabilité Bout-en-Bout)

```sparql
PREFIX dkg:      [http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)
PREFIX dkg-data: [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#)
PREFIX rdfs:     [http://www.w3.org/2000/01/rdf-schema#](http://www.w3.org/2000/01/rdf-schema#)

SELECT ?assetLabel ?compLabel ?cveUri ?cweLabel ?capecLabel WHERE {
    ?asset a dkg:Asset ;
           rdfs:label ?assetLabel ;
           dkg:hasInstalledComponent ?comp .
    
    ?comp a dkg:SoftwareComponent ;
          rdfs:label ?compLabel ;
          dkg:hasVulnerability ?cve .
          
    ?cve a dkg:Vulnerability ;
         dkg:exploitsWeakness ?cwe .
         
    ?cwe a dkg:Weakness ;
         rdfs:label ?cweLabel ;
         dkg:hasThreatPattern ?capec .
         
    ?capec a dkg:ThreatPattern ;
           rdfs:label ?capecLabel .
}