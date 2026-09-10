<%*
// 1. Parsing de la Roadmap pour extraire les phases
let roadmapFile = app.vault.getAbstractFileByPath("00-Projet/Roadmap_Suivi-Avancement.md");
if (!roadmapFile) {
    roadmapFile = tp.file.find_tfile("Roadmap_Suivi-Avancement.md");
}

let phasesList = [];
if (roadmapFile) {
    const content = await app.vault.read(roadmapFile);
    const lines = content.split("\n");
    let inSection2 = false;

    for (let line of lines) {
        if (line.includes("## 2")) { inSection2 = true; continue; }
        if (inSection2 && line.includes("## 3")) { break; }

        if (inSection2 && line.startsWith("|")) {
            let cleanLine = line.replace(/<br\s*\/?>/gi, " ").replace(/<[^>]*>/g, "").replace(/\*\*/g, "");
            let cols = cleanLine.split("|").map(c => c.trim());

            if (cols.length >= 6 && cols[2] && /^P\d+$/i.test(cols[2])) {
                phasesList.push({
                    code: cols[2].toUpperCase(),
                    nom: cols[3] || "Sans nom",
                    statut: cols[5] || "⚪ Planifié"
                });
            }
        }
    }
}

if (phasesList.length === 0) {
    phasesList.push({ code: "P01", nom: "Phase Initiale", statut: "⚪ Planifié" });
}

// 2. Sélection de la Phase
const phaseDisplayList = phasesList.map(p => `${p.code} — ${p.nom} (${p.statut})`);
const selectedPhaseObj = await tp.system.suggester(phaseDisplayList, phasesList) || phasesList[0];

const targetPCode = selectedPhaseObj.code;
const pNom = selectedPhaseObj.nom;
const pStatut = selectedPhaseObj.statut;

// 3. Sélection de la Portée
const typeOptions = ["TRANSVERSAL", "USECASE_METIER", "USECASE_TECHNIQUE"];
const selectedType = await tp.system.suggester(typeOptions, typeOptions) || "TRANSVERSAL";

let porteeCode = "FWK";
if (selectedType === "USECASE_METIER") porteeCode = "MET";
if (selectedType === "USECASE_TECHNIQUE") porteeCode = "TEC";

// 4. Titre complet et Titre court Snake_Case
let rawTitle = tp.file.title;
let defaultCleanTitle = rawTitle.replace(/^SPEC-[^-]+-/, "").replace(/_/g, " ");
const specTitre = await tp.system.prompt("Titre complet de la spécification :", defaultCleanTitle);

let defaultSnake = specTitre.toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9]/g, "_")
    .replace(/_+/g, "_")
    .replace(/^_|_$/g, "");

const titreSnake = await tp.system.prompt("Titre court (snake_case) :", defaultSnake);

// Numéro de révision par défaut (numérique)
const revisionNum = 1;
const revisionSuffix = String(revisionNum).padStart(2, "0");

// Génération de la Référence Unique (ex: SPC-TECH-P06-api_gateway_01)
const specReference = `SPC-${porteeCode}-${targetPCode}-${titreSnake}_${revisionSuffix}`;

// 5. Publics visés
const publicPresets = [
    "Architectes Ontologues, Développeurs DevSecOps",
    "Analystes CTI / SOC, Lead Tech",
    "Architectes Ontologues, Analystes CTI / SOC",
    "✏️ Autre combinaison..."
];

let chosenPublic = await tp.system.suggester(publicPresets, publicPresets) || publicPresets[0];
if (chosenPublic.startsWith("✏️")) {
    chosenPublic = await tp.system.prompt("Saisir le(s) public(s) visé(s) (séparés par des virgules) :", "Architectes Ontologues");
}

const publicList = chosenPublic
    ? chosenPublic.split(",").map(p => p.trim()).filter(p => p.length > 0)
    : ["Architectes Ontologues"];

// 6. Injection dans les propriétés YAML (Frontmatter)
app.fileManager.processFrontMatter(tp.config.target_file, (fm) => {
    fm["type"] = "spec";
    fm["reference"] = specReference;
    fm["revision"] = revisionNum;
    fm["titre"] = specTitre;
    fm["titre_court"] = titreSnake;
    fm["phase_code"] = targetPCode;
    fm["phase_nom"] = pNom;
    fm["statut"] = pStatut;
    fm["portee"] = selectedType;
    fm["public_vise"] = publicList;
});
-%>
---
type: spec
reference: <% specReference %>
revision: <% revisionNum %>
titre: "<% specTitre %>"
titre_court: <% titreSnake %>
phase_code: <% targetPCode %>
phase_nom: "<% pNom %>"
statut: "<% pStatut %>"
portee: <% selectedType %>
public_vise:
<% publicList.map(p => `  - "${p}"`).join("\n") %>
---
# 📜 <% specTitre %>



## 📖 1. Résumé Executif & Glossaire

### 1.1 Objectif
[Décrire en 2-3 phrases le but de cette spécification et sa valeur pour le projet]

### 1.2 Glossaire Métier & Technique
| Acronyme / Concept | Définition | Contexte DKG |
| :--- | :--- | :--- |
| **Exemple** | Définition courte | Application dans le graphe |

## 🏗️ 2. Spécification & Modélisation
```mermaid
graph TD
    A[Composant A] --> B[Composant B]
```

## 📐 3. Spécifications Formelles

<!-- SECTION A ADAPTER SELON LE NIVEAU DE SPECIFICATION -->

### Option A : Si Niveau METIER (SOC / Fonctionnel)
#### 3.1 Scenario Métier & Kill Chain
[Diagramme Mermaid / Schéma ASCII de l'attaque ou du cas d'usage]

#### 3.2 Modélisation Conceptuelle & Traçabilité TLP
[Description des entités métier et requêtes SPARQL d'analyse]

---

### Option B : Si Niveau TECHNIQUE ou SOCLE (Dev / Ontologie)
#### 3.1 Axiomes, Structures RDF & Inférences
[Snippets Turtle, règles SWRL/SHACL, schémas TBox/RBox]

#### 3.2 Directives d'Implémentation Code & Scripts
[Modules Python associés, fonctions de génération]

---

## 📊 4. Matrice d'Exigences & Critères d'Acceptation (`EXG-`)

| Identifiant | Domaine | Intitulé de l'Exigence | Description & Critères d'Acceptation | Mode de Test / Asset |
| :--- | :---: | :--- | :--- | :--- |
| **EXG-XX-01** | `XX` | Nom de l'exigence | Critère formel vérifiable. | Pytest / SPARQL / SHACL |

---

## 🛡️ 5. Outillage, CI/CD & Traçabilité Pytest

* **Scripts de Génération / Exécution** : `03-Application/[script].py`
* **Suite de Test Associée** : `tests/test_[exigence].py`
* **Artefacts Produits** : `[Fichier_Maître.ttl]`

---

## 📚 6. Documents Liés & Références

* **[SPEC-PARENTE]** : [Lien vers la spec de niveau supérieur ou dépendante]