_(Phase 1 : Socle Structurel Sémantique)_


**Périmètre :** Phase 1 — Définition immuable des classes, propriétés et relations logiques (DL).

### Système de Numérotation des Exigences : `EXG-TBOX-*`

#### 1. Normalisation des Namespaces et URIs

- **`EXG-TBOX-01` (Délimiteur d'URI)** : Tous les concepts sémantiques de la TBox doivent obligatoirement utiliser le séparateur `#` et le préfixe unique `[http://dkg.cybersec.org/tbox#](http://dkg.cybersec.org/tbox#)`. L'usage des délimiteurs mixtes (`/` vs `#`) est strictement interdit.
    
- **`EXG-TBOX-02` (Typage OWL/RDFS)** : Chaque concept doit être formellement instancié comme un `owl:Class`, `owl:ObjectProperty`, ou `owl:DatatypeProperty`.
    

#### 2. Intégrité des Relations d'Objets (Object Properties)

- **`EXG-TBOX-03` (Domaine et Portée strictes)** : Toute `owl:ObjectProperty` doit explicitement déclarer au moins un `rdfs:domain` et un `rdfs:range`.
    
    - _Exemple :_ `dkg:hasInstalledComponent` $\rightarrow$ `rdfs:domain dkg:Asset`, `rdfs:range dkg:SoftwareComponent`.
        
- **`EXG-TBOX-04` (Axiomes de RBox)** : Les caractéristiques algébriques des propriétés (transitivité, inversibilité, symétrie) doivent être déclarées au niveau du schéma (RBox stricte).
    
    - _Exemple :_ `dkg:isComponentOf owl:inverseOf dkg:hasInstalledComponent`.