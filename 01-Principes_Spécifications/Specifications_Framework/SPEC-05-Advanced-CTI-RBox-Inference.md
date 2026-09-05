
## 1. Contexte & Alignement Exigences
Ce document définit les exigences fonctionnelles et techniques de la Phase 5 (Vague 3). Il régit l'embarquement offline des modèles IA, l'ingestion CTI advanced, le composant de gouvernance (Agent MITM), et le moteur de raisonnement sur le Knowledge Graph DKG.

Rattachement direct :
- `SPEC-00_ExigencesProjet.md` : EXG-SEC-01 (Isolation TLP), EXG-AI-01 (Exécution 100% Locale / Air-gapped), EXG-SEM-02 (Validation SHACL sous CWA).

---

## 2. Socle IA Local & Exécution Air-Gapped

### 2.1 Contraintes d'Architecture
- Aucun appel à des API externes (ex: OpenAI, Anthropic) n'est autorisé.
- Tous les modèles doivent être téléchargés une seule fois au déploiement via `03-Application/models/fetch_models.py` et mis en cache dans le volume local `03-Application/models/cache/`.
- Dépendances logicielles : `transformers`, `gliner`, `sentence-transformers`, `torch` (exécuté sur CPU/CUDA local).

### 2.2 Modèles Sélectionnés
1. **Extraction NER Cyber :** `gliner-community/gliner_large-v2.1` (Zero-shot NER local).
2. **Alignement Sémantique Embeddings :** `sentence-transformers/all-MiniLM-L6-v2` (Vecteurs 384d).

---

## 3. Spécifications du Pipeline Agent MITM (Gouvernance Sémantique)


```
L'Agent MITM intercepte toute entité issue du traitement NLP/NER avant écriture dans la ABox CTI.

[Texte CTI Brut] --> [NER Local] --> [Entités Extraites] 
               |
               v 
                 +-------------------------+
                 |       Agent MITM        | 
                 | (Alignement Embeddings) |
                 +-------------------------+ 
                            /      \
                           /         \
  	Score Cosinus >= 0.85 /           \ Score Cosinus < 0.85 
	          v                                 v 
	[Mapping TBox Existante]           [Proposition Extension] 
	          |                                 | 
	          v                                 v 
	  [Injection ABox]                 [Validation Humaine]

```


## 4. Modélisation Sémantique (Entités & Relations Phase 5) 
### 4.1 Modélisation des Entités (TBox Extension) 

| Entité               | Parent Class    | Domain / Range      | Niveau TLP  | Description                                                          |     |
| :------------------- | :-------------- | :------------------ | :---------- | :------------------------------------------------------------------- | --- |
| `dkg:HighRiskAsset`  | `dkg:Asset`     | Domain: `dkg:Asset` | `TLP:RED`   | Classe dérivée désignant un actif à haut risque suite à l'inférence. |     |
| `dkg:ThreatCampaign` | `rdfs:Resource` | Domain: N/A         | `TLP:CLEAR` | Campagne d'attaque identifiée par la CTI.                            |     |
| `dkg:AttackPattern`  | `rdfs:Resource` | Domain: N/A         | `TLP:CLEAR` | TTPs associés aux référentiels (ex: MITRE ATT&CK).                   |     |

### 4.2 Modélisation des Relations (Properties)

| Propriété | Type OWL | Domain | Range | TLP | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `dkg:targetsAsset` | `owl:ObjectProperty` | `dkg:ThreatCampaign` | `dkg:Asset` | `TLP:RED` | Lien déduit entre une campagne active et un actif vulnérable interne. |
| `dkg:hasAssociatedCVE`| `owl:ObjectProperty` | `dkg:AttackPattern` | `dkg:Vulnerability`| `TLP:CLEAR` | Relation entre motif d'attaque et failles CVE associées. |
| `dkg:isExploitedBy` | `owl:ObjectProperty` | `dkg:SoftwareComponent`| `dkg:ThreatCampaign`| `TLP:RED` | Relation issue du croisement CISA KEV / ABox RED. | 

--- 

## 5. Règles d'Inférence Sémantique (SWRL / SPARQL CONSTRUCT)

### Règle R-01 : Déduction d'un HighRiskAsset (Calcul de Surface d'Attaque) 

* Logique : Si un composant logiciel interne (`dkg:SoftwareComponent`) possède une vulnérabilité (`dkg:Vulnerability`) enregistrée comme activement exploitée dans CISA KEV, et que ce composant est hébergé sur un actif (`dkg:Asset`), alors cet actif est instancié comme `dkg:HighRiskAsset`. 
* **Formalisation SPARQL CONSTRUCT :** 

```sparql
 PREFIX dkg: [http://dkg.cybersec.org/schema#](http://dkg.cybersec.org/schema#) 
 PREFIX dkg-data: [http://dkg.cybersec.org/data#](http://dkg.cybersec.org/data#) 
 PREFIX dkg-cti: [http://dkg.cybersec.org/cti#](http://dkg.cybersec.org/cti#) 
 PREFIX rdf: [http://www.w3.org/1999/02/22-rdf-syntax-ns#](http://www.w3.org/1999/02/22-rdf-syntax-ns#) 
 CONSTRUCT { 
     ?asset a dkg:HighRiskAsset ; 
         dkg:hasRiskReason "Exposed vulnerability listed in CISA KEV" . 
 } 
 WHERE { 
     ?asset dkg:hostsComponent ?component . 
     ?component dkg:hasVulnerability ?cve . 
     ?cve dkg-cti:isCisaKevListed true . 
 }
```

### Règle R-02 : Règle de Ségrégation & Projections TLP

- Logique : Tout triple dérivé impliquant à la fois une entité `TLP:CLEAR` (CTI) et une entité `TLP:RED` (Actif Interne) hérite strictement du niveau de classification `TLP:RED` et est consigné exclusivement dans `ABOX_RED_PATH`.
    

## 6. Critères de Recette & Validation CI/CD

1. **Execution Offline :** Validation que `fetch_models.py` charge les modèles et qu'aucune requête HTTP hors-réseau n'est exécutée pendant le NER ou l'alignement vectoriel.
    
2. **Intégrité SHACL :** Pass de validation SHACL sous Closed World Assumption sur le graphe enrichi post-inférence.
    
3. **Zéro Fuite TLP :** Aucune entité interne (`dkg-data:`) ne doit apparaître dans `ABOX_CTI_PATH` (`TLP:CLEAR`).


