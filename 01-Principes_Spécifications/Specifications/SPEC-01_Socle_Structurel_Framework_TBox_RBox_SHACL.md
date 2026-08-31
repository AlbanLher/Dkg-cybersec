_(Phase 1 : Socle Structurel Sémantique)_


> **Fichier** : `01-Principes_Spécifications/Specifications/SPEC-01_Norme_TBox_RBox.md`  
> **Statut** : Approuvé (Phase 1)  
> **Classification TLP** : `TLP:AMBER`  
> **Portée** : Méta-Modèle & Framework Agnostique (Réutilisable tout domaine)

---

## 🛠️ 1. Exigences Normatives de Développement TBox & RBox

Toute ontologie générée par le framework doit satisfaire aux exigences suivantes :

### 1.1 Normalisation des Namespaces et URIs
* **`EXG-TBOX-01` (Délimiteur d'URI)** : Tous les concepts sémantiques de la TBox doivent obligatoirement utiliser le séparateur `#` et le préfixe unique `http://dkg.cybersec.org/tbox#`. L'usage des délimiteurs mixtes (`/` vs `#`) est strictement interdit.
* **`EXG-TBOX-02` (Typage OWL/RDFS)** : Chaque concept doit être formellement instancié sous un type OWL 2 explicite (`owl:Class`, `owl:ObjectProperty`, ou `owl:DatatypeProperty`).

### 1.2 Intégrité des Relations d'Objets (RBox)
* **`EXG-TBOX-03` (Domaine et Portée strictes)** : Toute `owl:ObjectProperty` doit explicitement déclarer au moins un `rdfs:domain` et un `rdfs:range`.
* **`EXG-TBOX-04` (Axiomes de RBox)** : Les caractéristiques algébriques des propriétés (transitivité, inversibilité, symétrie) doivent être déclarées au niveau du schéma (ex: declaration formelle des `owl:inverseOf`).

---

## 🛡️ 2. Exigences du Moteur de Intégrité SHACL (CWA)

* **`EXG-QUAL-01` (Couplage TBox ↔ SHACL)** : Toute classe définie dans la TBox doit obligatoirement posséder une forme SHACL (`sh:NodeShape`) correspondante.
* **`EXG-QUAL-04` (Validation sous CWA)** : Le moteur de validation SHACL applique l'Hypothèse du Monde Fermé (Closed World Assumption) : toute instance ne respectant pas les cardinalités ou les types stricts est rejetée.

* **`EXG-QUAL-05` (Couche Lexicale SKOS Obligatoire)** : Toute entité TBox (`owl:Class`, `owl:ObjectProperty`, `owl:DatatypeProperty`) **doit** comporter au moins :
	  1. Un libellé préférentiel FR/EN (`skos:prefLabel`)
	  2. Une définition explicite (`skos:definition`)
	  3. Des alias ou synonymes métier (`skos:altLabel`) si applicables.


---

## ⚙️ 3. Contrat de Restitution Triple-Format (`EXG-PROJ-02`)

Le framework impose une génération synchronisée dans 3 formats :
1. **RDF Turtle (`.ttl`)** : Format canonique OWL 2.
2. **JSON-LD (`.json`)** : Format d'échange et d'API.
3. **Markdown (`.md`)** : Documentation lisible par l'humain, intégrant obligatoirement le **Glossaire des Acronymes** et la représentation graphique **Mermaid.js** du schéma.