
> **Classification** : `TLP:RED` > **Statut** : 🟢 Approuvé 
> **Domaine** : UseCase Cyber / Validation d'Inférence 
> **Matrice de Rattachabilité** : `EXG-INF-01`, `EXG-INF-02`, `EXG-SEC-01`
---
## 📖 1. Glossaire des Acronymes 
* **Silent Cascade** : Scénario d'attaque par rebond où un attaquant exploite une vulnérabilité externe pour cibler une base de données critique non exposée. 
* **Pivot Asset** : Hôte intermédiaire compromis servant de passerelle. 
* --- 
## 🎯 2. Objet & Portée 

Cette spécification définit l'instanciation de validation pour le moteur d'inférence (Phase 4) sur le cas d'usage **Silent Cascade** (SPEC-UC-02). Elle décrit comment la superposition des graphes `ABOX_RED_PATH` et `ABOX_CTI_PATH` permet d'inférer dynamiquement des chemins d'attaque invisibles à l'état brut. --- 
## 📐 3. Spécifications Formelles & Règles Métier 
### 3.1 Chaîne d'Inférence Métier (Scénario UC-03) 
* **Faits Initiaux (Non-déduits)** :
* `dkg-data:Host-Proxy-DMZ` est un `dkg:Host`, `dkg:isExposedToInternet true`, et est lié à `dkg-cti:CVE-2024-SILENT`. 
* `dkg-cti:CVE-2024-SILENT` a la propriété `dkg:isCisaKev true`. 
* `dkg-data:Host-Proxy-DMZ` a la relation `dkg:connectsTo dkg-data:Host-DB-Internal`. 
* `dkg-data:Host-DB-Internal` a la propriété `dkg:criticalityLevel "CRITICAL"`. 
* **Faits Déduits Attendus (Post-Raisonnement Phase 4)** `[EXG-INF-01]`, `[EXG-INF-02]` : 

```turtle 
@prefix dkg: [http://dkg.cybersec.org/schema#](http://dkg.cybersec.org/schema#) . 
@prefix dkg-data: [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#) . 
@prefix dkg-cti: [http://dkg.cybersec.org/cti#](http://dkg.cybersec.org/cti#) . 

# Triplet déduit 1 : Qualification de l'hôte pivot 
dkg-data:Host-Proxy-DMZ a dkg:HighRiskAsset . 

# Triplet déduit 2 : Matérialisation de la cascade vers l'actif critique 
dkg-data:Host-Proxy-DMZ dkg:exposesToCascade dkg-data:Host-DB-Internal .
```
## 📊 4. Matrice Synthétique des Exigences (Index de Traçabilité)

|**Identifiant**|**Intitulé de l'Exigence**|**Description & Critères d'Acceptation**|**Section Parent**|
|---|---|---|---|
|**EXG-INF-01**|**Validation Hôte Pivot**|Inférence vérifiée sous Pytest : `dkg-data:Host-Proxy-DMZ` doit posséder le type `dkg:HighRiskAsset`.|Section 3.1|
|**EXG-INF-02**|**Validation Lien Cascade**|Inférence vérifiée sous Pytest : Existence du triple `dkg-data:Host-Proxy-DMZ dkg:exposesToCascade dkg-data:Host-DB-Internal`.|Section 3.1|

## 🛡️ 5. Gouvernance, Outillage & Validation

- **Validation Automatisée** : Intégrée dans `test_phase4_inference.py`.
    
- **Artefacts Produits** : Fichier `DKG_ABox_Infered.ttl` contenant l'instanciation des faits dérivés.
    

## 📚 6. Pour aller plus loin (Ressources Pédagogiques)

- **[SPEC-UC-02]** : _Scénario d'Attaque Silent Cascade (Description fonctionnelle)._