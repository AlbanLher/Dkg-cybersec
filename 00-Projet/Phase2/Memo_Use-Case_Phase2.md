# 🎯 Use Case Phase 2 - Analyse d'Impact et Traçabilité Cyber (TLP:RED)

## 📌 Objectif Métier
Le but de ce use case est de valider la capacité du graphe **DKG-CyberSec** à lier dynamiquement une ressource informatique physique du SI (**Asset**) jusqu'aux schémas d'attaques théoriques (**CAPEC**) à travers son exposition logicielle.

---

## 🏗️ Alignement TBox & Rôles des Concept

Chaque instance générée dans l'ABox dérive strictement d'une classe formelle du socle `DKG_TBox_Master.ttl` :

| Concept TBox (`dkg:`) | Instance ABox (`data:`) | Rôle Métier / Gouvernance |
| :--- | :--- | :--- |
| `dkg:Asset` | `data:Asset-Srv-Prod-01` | Équipement cible hébergeant des données sensibles (Classé `TLP:AMBER`). |
| `dkg:SoftwareComponent` | `data:Comp-Apache-2-4-49` | Brique applicative déployée sur l'actif. |
| `dkg:Vulnerability` | `data:CVE-2021-41773` | Faille de sécurité publique associée à la version du composant. |
| `dkg:Weakness` | `data:CWE-22` | Catégorie de défaut logiciel (*Path Traversal*). |
| `dkg:ThreatPattern` | `data:CAPEC-126` | Vecteur d'attaque utilisable par un attaquant pour exploiter la faiblesse. |

---

## 🔍 Scénario de Validation SPARQL (Traçabilité Bout-en-Bout)

La requête de qualification métier ci-dessous permet aux équipes SOC/CTI d'identifier instantanément le mode opératoire d'attaque menaçant un serveur de production :

```sparql
PREFIX dkg:  [http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)
PREFIX data: [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#)

SELECT ?assetLabel ?compLabel ?cveId ?cweLabel ?capecLabel WHERE {
    ?asset a dkg:Asset ;
           rdfs:label ?assetLabel ;
           dkg:hasInstalledComponent ?comp .
    
    ?comp a dkg:SoftwareComponent ;
          rdfs:label ?compLabel ;
          dkg:hasVulnerability ?cve .
          
    ?cve a dkg:Vulnerability ;
         dkg:cveId ?cveId ;
         dkg:hasWeakness ?cwe .
         
    ?cwe a dkg:Weakness ;
         rdfs:label ?cweLabel ;
         dkg:hasThreatPattern ?capec .
         
    ?capec a dkg:ThreatPattern ;
           rdfs:label ?capecLabel .
}