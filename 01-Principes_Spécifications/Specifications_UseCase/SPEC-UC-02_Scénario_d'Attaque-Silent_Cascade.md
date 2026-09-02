
- **Référence** : SPEC-UC-02   
- **Statut** : Approuvé
- **Classification TLP** : TLP:AMBER (Cas d'usage interne SOC)
- **Auteur** : Architecte Sémantique DKG-CyberSec
- **Dépendances** : SPEC-03 (Framework CTI Externe), `DKG_TBox_Master.ttl`
## 1. Contexte & Objectif
Le scénario **Silent Cascade** simule une attaque sophistiquée à faible bruit (Low & Slow). L'attaquant exploite une vulnérabilité CTI connue (TLP:CLEAR) présente sur un composant d'infrastructure exposé, puis s'en sert comme pivot pour compromettre silencieusement des actifs critiques internes (TLP:RED).

L'objectif de ce cas d'usage est de valider la capacité du Dynamic Knowledge Graph (DKG) à **corréler les données CTI externes avec la topologie réseau interne** pour détecter des chemins d'attaque invisibles aux SIEM traditionnels.

## 2. Description de la Chaîne d'Attaque (Kill Chain)
```
[Attaquant Externe]
       │
       ▼ (1. Exploitation CVE / KEV)
[Serveur DMZ : Proxy Web] ── (TLP:CLEAR + TLP:RED)
       │
       ▼ (2. Mouvement Latéral Silent)
[Base de Données Interne] ── (TLP:RED)
       │
       ▼ (3. Exfiltration / Compromission)
[Données Sensibles / Core Business]
```

1. **Initial Access** : Exploitation d'une vulnérabilité référencée CISA-KEV (ex: RCE sur service Web/Proxy).
2. **Pivot & Propagation** : Déplacement latéral via des identifiants compromis ou des flux autorisés en DMZ.
3. **Impact** : Atteinte d'un actif critique non exposé directement à Internet mais dépendant du composant vulnérable.

## 3. Modélisation Sémantique DKG (Ontologie & Multi-Graphes)

### 3.1 Entités & Alignement des Graphes

- **Graphe CTI Externe (`dkg-cti:`, TLP:CLEAR)** :
    - Instance `dkg:Vulnerability` (ex: `CVE-2024-XXXX`).
    - Attributs : `dkg:cvssScore`, `dkg:isCisaKev "true"^^xsd:boolean`, `dkg:hasThreatPattern`.
- **Graphe Interne SOC (`dkg-data:`, TLP:RED)** :
    - Assets : `dkg:Host` (Proxy DMZ, Serveur BDD).
    - Relations : `dkg:hasVulnerability`, `dkg:connectsTo`, `dkg:dependsOn`.
### 3.2 Modèle Turtle d'Exemple (Extrait de Validation)

```
@prefix dkg: <http://dkg.cybersec.org/schema#> .
@prefix dkg-data: <http://dkg.cybersec.org/data#> .
@prefix dkg-cti: <http://dkg.cybersec.org/cti#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Asset exposé (TLP:RED)
dkg-data:Host-Proxy-DMZ a dkg:Host ;
    rdfs:label "Proxy DMZ Principal" ;
    dkg:isExposedToInternet "true"^^xsd:boolean ;
    dkg:hasVulnerability dkg-cti:CVE-2024-SILENT ;
    dkg:connectsTo dkg-data:Host-DB-Internal .

# Vulnerabilité CTI (TLP:CLEAR)
dkg-cti:CVE-2024-SILENT a dkg:Vulnerability ;
    dkg:cvssScore "9.8"^^xsd:float ;
    dkg:isCisaKev "true"^^xsd:boolean .

# Asset Critique Interne (TLP:RED)
dkg-data:Host-DB-Internal a dkg:Host ;
    rdfs:label "Base de Donnees RH Core" ;
    dkg:criticalityLevel "CRITICAL" .
```

## 4. Règle de Détection & Inférence (Recherche de Chemin d'Attaque)

L'intérêt du DKG dans ce cas d'usage est d'exécuter une requête SPARQL (ou règle de raisonnement) pour identifier les chemins de vulnérabilité en cascade :
```
PREFIX dkg: <http://dkg.cybersec.org/schema#>

SELECT ?exposedHost ?vulnerability ?criticalTarget WHERE {
  # 1. Hôte exposé à Internet
  ?exposedHost dkg:isExposedToInternet true ;
               dkg:hasVulnerability ?vulnerability ;
               dkg:connectsTo+ ?criticalTarget .
  
  # 2. Vulnérabilité critique exploitée dans le sauvage (KEV)
  ?vulnerability dkg:isCisaKev true .
  
  # 3. Cible finale critique
  ?criticalTarget dkg:criticalityLevel "CRITICAL" .
}
```

## 5. Critères d'Acceptation pour le SOC

- [x] La vulnérabilité impliquée dans _Silent Cascade_ doit obligatoirement respecter la forme SHACL `dkg:VulnerabilityShape`.
    
- [x] La séparation TLP est strictement conservée : les CVE sont dans `ABOX_CTI_PATH`, l'infrastructure dans `ABOX_RED_PATH`.
    
- [x] Le pipeline Pytest valide l'existence du chemin d'attaque sans altérer la cohérence globale du graphe.