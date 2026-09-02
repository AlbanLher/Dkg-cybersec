
> **Classification** : `TLP:CLEAR`> 
> **Statut** : 🟢 Approuvé
> **Domaine** : Framework CTI / NLP & Named Entity Recognition (Vague 2 — Phase 4)
> **Matrice de Rattachabilité** : `EXG-NER-01`, `EXG-NER-02`, `EXG-SEC-01`, `EXG-QUAL-01`

## 📖 1. Glossaire des Acronymes

- **NER** : Named Entity Recognition (Reconnaissance d'entités nommées).
- **Unstructured CTI** : Bulletins de sécurité textuels bruts, avis de sécurité PDF, articles de blogs de menaces.
- **Confidence Score** : Indice de confiance (0.0 à 1.0) attribué par le modèle NLP aux entités et relations extraites.
    
## 🎯 2. Objet & Portée

La présente spécification (**SPEC-04**) encadre le traitement des sources CTI non structurées pour la **Phase 4**. Elle définit :
1. Le pipeline d'extraction NER pour la reconnaissance d'entités cyber (`ThreatActor`, `Vulnerability`, `SoftwareComponent`, `ThreatPattern`).
2. Les règles de conversion déterministe des prédictions NLP en triplets RDF valides.
3. Les critères de qualité, le seuil de confiance minimal et l'injection dans la ABox CTI (`TLP:CLEAR`).

## 📐 3. Spécifications Formelles & Règles Métier

### 3.1 Extraction NER Cyber & Alignement Ontologique
- **Identification des Entités & Relations** `[EXG-NER-01]` : Le modèle NER DOIT extraire et classifier les mentions textuelles en se référant aux classes de la TBox Master (`dkg:Vulnerability`, `dkg:ThreatPattern`, etc.) et identifier leurs relations (`dkg:exploitsWeakness`, `dkg:hasThreatPattern`).
### 3.2 Seuil de Confiance & Mapping RDF
- **Mapping Déterministe & Filtrage** `[EXG-NER-02]` : Tout triplet généré par le pipeline NER ne peut être injecté dans le DKG que si son score de confiance est supérieur ou égal à **0.85**. Chaque entité extraite reçoit la métadonnée `dkg:nerConfidenceScore`.

```turtle
# Example de triplets RDF issus de l'extraction NER (TLP:CLEAR)
@prefix dkg: <http://dkg.cybersec.org/schema#> .
@prefix dkg-cti: <http://dkg.cybersec.org/cti#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

dkg-cti:ThreatActor-APT29 a dkg:ThreatActor ;
    rdfs:label "APT29 (Cozy Bear)" ;
    dkg:nerConfidenceScore "0.94"^^xsd:float ;
    dkg:hasThreatPattern dkg-cti:Pattern-Spearphishing .

dkg-cti:Pattern-Spearphishing a dkg:ThreatPattern ;
    rdfs:label "Spearphishing Link" ;
    dkg:nerConfidenceScore "0.89"^^xsd:float .
```

### 3.3 Sanity Check & Isolation TLP

- **Validation SHACL & Ségrégation** `[EXG-QUAL-01]` / `[EXG-SEC-01]` : Les entités extraites du texte brut doivent satisfaire aux contraintes SHACL applicables (`dkg:VulnerabilityShape`) et être stockées exclusivement dans `ABOX_CTI_PATH` sous le marquage **TLP:CLEAR**.
    

## 📊 4. Matrice Synthétique des Exigences (Index de Traçabilité)

|**Identifiant**|**Intitulé de l'Exigence**|**Description & Critères d'Acceptation**|**Section Parent**|
|---|---|---|---|
|**EXG-NER-01**|**Extraction NER Cyber**|Extraction conforme aux concepts de la TBox Master depuis un texte brut.|Section 3.1|
|**EXG-NER-02**|**Validation Seuil & Mapping**|Score de confiance $\ge 0.85$ et enregistrement de `dkg:nerConfidenceScore`.|Section 3.2|
|**EXG-QUAL-01**|**Conformité SHACL NER**|Zéro violation SHACL lors de l'injection des entités NER dans ABox CTI.|Section 3.3|
|**EXG-SEC-01**|**Confidentialité TLP:CLEAR**|Données CTI textuelles publiques strictement isolées dans le graphe TLP:CLEAR.|Section 3.3|

## 🛡️ 5. Gouvernance, Outillage & Validation

- **Validation Automatisée** : Script `03-Application/tests/test_phase4_ner_validation.py`.
    
- **Artefacts Produits** : `01-Principes_Spécifications/Specifications_Framework/SPEC-04_Unstructured_CTI_NER.md`, module `03-Application/ner_cti_extractor.py`, mise à jour de `DKG_ABox_CTI_External.ttl`.