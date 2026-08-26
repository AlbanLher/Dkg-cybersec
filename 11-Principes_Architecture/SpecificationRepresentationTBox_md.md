### 1. Spécification du Besoin : Lexique & Acronymes (Volet Sémantique)

- La version Markdown (`TBox_Cybersec.md`) pour être explicative pour les développeurs comme pour les décideurs, doit embarquer du **SKOS** (`skos:altLabel`, `skos:definition`, `skos:notation`). Le scrip qui l agenère doit extraire ces annotations.

- Chaque classe/propriété doit posséder `rdfs:comment` (description métier) ET `skos:altLabel` (acronymes/synonymes).  ( **Niveau OWL/RDFS** : )

- La documentation générée doit inclure un tableau exhaustif des standards W3C (`RDF`, `RDFS`, `OWL`, `SKOS`, `SPARQL`, `TTL`, `IRI`, `TBox`, `ABox`) -> Section Dédiée aux Acronymes W3C/Sémantiques :

### 2. Spécification du Besoin : Représentation Graphique Multi-Niveaux (Vue Globale & Zooms Métier)

Pour éviter "l'effet sac de nœuds", la représentation visuelle pour les humains doit suivre le principe de **Navigabilité par Cartes/Domaines** (Pattern "Overview First, Zoom and Filter") :

- Vue Globale de Synthèse (Niveau 0) : Schéma d'architecture de haut niveau ne montrant que les 4-5 Macro-domaines (`Actifs`, `Logiciels`, `Vulnérabilités`, `Menaces`).
    
- Vues Métier Segmentées (Niveau 1 - Zooms) :  
    - **Domaine Inventaire SI** : Nœuds `Asset`, `NetworkInterface`, `SoftwareComponent` + leurs propriétés.
    - **Domaine Threat Intelligence / CVE** : Nœuds `SoftwareComponent`, `Vulnerability` (CVE), `Weakness` (CWE).
    - **Domaine Résolution / Remediation** : Nœuds `Vulnerability`, `Patch`, `ActionPlan`.
        
3. **Format Standardisé de Rendu** : Intégration directe de diagrammes **Mermaid.js** dans `TBox_Cybersec.md` (rendu natif dans GitHub et VS Code sans passer par des images lourdes).

