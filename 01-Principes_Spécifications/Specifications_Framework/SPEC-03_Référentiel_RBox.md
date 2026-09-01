_(Phase 2/3 : Instances Vulnérabilités & Mappings)_


**Périmètre :** Phase 2 Bis / Phase 3 — Ingestion et alignement du dictionnaire public de vulnérabilités (TLP:CLEAR).

### Système de Numérotation des Exigences : `EXG-REF-*`

#### 1. Alignement des URIs de Vulnérabilités

- **`EXG-REF-01` (Format des Clés de Correspondance - Match Key)** : L'identifiant de vulnérabilité produit par l'ABox infrastructure doit utiliser un format canonique standardisé (`[http://dkg.cybersec.org/rbox#CVE-YYYY-NNNN](http://dkg.cybersec.org/rbox#CVE-YYYY-NNNN)`) correspondant exactement aux URIs du dictionnaire NVD/CWE.
    
- **`EXG-REF-02` (Typage des Métadonnées Externe)** : Les propriétés associées aux failles externes doivent respecter les datatypes de la TBox (`dkg:cvssScore` en `xsd:float`, `dkg:cweId` en `xsd:string`).
    

#### 2. Résilience des Traversées SPARQL

- **`EXG-REF-03` (Isolation des données optionnelles)** : Les enrichissements externes (CVSS, CWE, recommandations) doivent être requêtés via des clauses SPARQL `OPTIONAL` pour éviter l'exclusion d'un équipement de l'ABox en cas d'absence de fiche NVD complète.