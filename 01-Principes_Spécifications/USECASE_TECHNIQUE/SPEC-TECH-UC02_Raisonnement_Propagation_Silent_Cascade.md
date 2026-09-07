# 📜 SPEC-TECH-UC03 — Instanciation & Raisonnement (Propagation Silent Cascade) 
>**Classification** : `TLP:RED` 
>**Statut** : 🟢 Approuvé 
>**Niveau d'Abstraction** : 🟡 USECASE_TECHNIQUE 
>*Public Cible** : Développeurs DevSecOps, Ingénieurs Inférence & Graphe 
>***Domaine Principal** : `IN` | `QU` | `SH` 
>**Matrice de Rattachabilité** : `EXG-INF-01`, `EXG-INF-02`, `EXG-QU-03`, `EXG-OR-05` --- 
 
## 📖 1. Résumé Exécutif & Glossaire 
> 
### 1.1 Objectif 
Spécifier le jeu de données de validation ABox et le harnais d'exécution Pytest pour le moteur de raisonnement sur le cas d'usage *Silent Cascade* (SPEC-METIER-UC02). 
### 1.2 Glossaire Métier & Technique
| Acronyme / Concept | Définition | Contexte DKG | 
| :--- | :--- | :--- |
| **ABox Inferred** | Graphe de Faits Déduits | Stockage dédié (`DKG_ABox_Infered.ttl`) recevant les résultats d'inférence. | 
| **Pivot Asset** | Actif Intermédiaire | Serveur DMZ intermédiaire exposé servant de point de rebond. | 

--- 
## 🎯 2. Périmètre & Rôle de la Spécification 
* **Positionnement dans l'Architecture** : Niveau 3 (Cas d me Technique). Encadre l'exécution technique de la Vague 3. 
* **Gouvernance & Validation** : Validé par le Lead DevSecOps. 
 --- 

## 📐 3. Spécifications Formelles 
### 3.1 Graphe d'Entrée & Instanciation ABox Source (`TLP:RED` / `TLP:CLEAR`) 

```turtle 
@prefix dkg: [http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#) . 
@prefix dkg-data: [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#) . 
@prefix dkg-cti: [http://dkg.cybersec.org/cti#](http://dkg.cybersec.org/cti#) . 
@prefix xsd: [http://www.w3.org/2001/XMLSchema#](http://www.w3.org/2001/XMLSchema#) . 
# Données d'infrastructure (ABox Interne TLP:RED) 
dkg-data:Host-Proxy-DMZ a dkg:Host ; 
	rdfs:label "Proxy DMZ Principal" ; 
	dkg:isExposedToInternet "true"^^xsd:boolean ; 
	dkg:hasVulnerability dkg-cti:CVE-2024-SILENT ; 
	dkg:connectsTo dkg-data:Host-DB-Internal . 
	
dkg-data:Host-DB-Internal a dkg:Host ; 
	rdfs:label "Base de Données RH Core" ; 
	dkg:criticalityLevel "CRITICAL" . 
	
# Données CTI (ABox CTI TLP:CLEAR) 
dkg-cti:CVE-2024-SILENT a dkg:Vulnerability ; 
	dkg:cvssScore "9.8"^^xsd:float ; 
	dkg:isCisaKev "true"^^xsd:boolean .
```
### 3.2 Triplet Attendu en Sortie du Raisonneur (`DKG_ABox_Infered.ttl`)

Le moteur d'inférence doit générer de façon exacte et déterministe le bloc Turtle suivant :
```turtle
@prefix dkg: [http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#) .
@prefix dkg-data: [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#) .
```
# Inférence 1 : Qualification du risque hôte
dkg-data:Host-Proxy-DMZ a dkg:HighRiskAsset ;
    dkg:hasRiskReason "Exposed vulnerability listed in CISA KEV" .

# Inférence 2 : Matérialisation de la trajectoire d'attaque
dkg-data:Host-Proxy-DMZ dkg:exposesToCascade dkg-data:Host-DB-Internal .

📊 4. Matrice d'Exigences & Critères d'Acceptation (EXG-)
Identifiant	Domaine	Intitulé de l'Exigence	Description & Critères d'Acceptation	Mode de Test / Asset
EXG-INF-01	IN	Inférence Hôte Pivot	Assertion Pytest vérifiée : dkg-data:Host-Proxy-DMZ a dkg:HighRiskAsset.	test_phase3_inference.py
EXG-INF-02	IN	Inférence Cascade	Assertion Pytest vérifiée : présence du triplet dkg-data:Host-Proxy-DMZ dkg:exposesToCascade dkg-data:Host-DB-Internal.	test_phase3_inference.py
EXG-QU-03	QU	Validation SHACL Post-Inférence	Le graphe fusionné (Base + Inferred) doit produire zéro violation SHACL (sh:Violation).	pySHACL
🛡️ 5. Outillage, CI/CD & Traçabilité Pytest
Scripts de Génération / Exécution : 03-Application/reasoning_engine.py

Suite de Test Associée : tests/test_phase3_inference.py

Artefacts Produits : 02-Donnees/Master_Transversal/DKG_ABox_Infered.ttl

📚 6. Documents Liés & Références
[SPEC-SOCLE-00] : Gouvernance du Cadre Spécifications & Exigences DKG.  
MD

[SPEC-SOCLE-04] : Règles d'Inférence, RBox & Gouvernance du Moteur de Raisonnement.

[SPEC-METIER-UC02] : Scénario d'Attaque Silent Cascade.  
MD