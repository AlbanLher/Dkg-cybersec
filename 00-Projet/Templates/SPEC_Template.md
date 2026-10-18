<%*
// 1. Parsing de la Roadmap (inchangé)
let roadmapFile = app.vault.getAbstractFileByPath("00-Projet/Roadmap_Suivi-Avancement.md");
if (!roadmapFile) roadmapFile = tp.file.find_tfile("Roadmap_Suivi-Avancement.md");
let phasesList = [];
if (roadmapFile) {
    const content = await app.vault.read(roadmapFile);
    const lines = content.split("\n");
    let inSection2 = false;
    for (let line of lines) {
        if (line.includes("## 2")) { inSection2 = true; continue; }
        if (inSection2 && line.includes("## 3")) break;
        if (inSection2 && line.startsWith(" ")) {
            let cols = line.replace(/<br\s*\/?>/gi, " ").replace(/<[^>]*>/g, "").replace(/\*\*/g, "").split("|").map(c => c.trim());
            if (cols.length >= 6 && cols[2] && /^P\d+$/i.test(cols[2]))
                phasesList.push({ code: cols[2].toUpperCase(), nom: cols[3] || "Sans nom", statut: cols[5] || "⚪ Planifié" });
        }
    }
}
if (phasesList.length === 0) phasesList.push({ code: "P1", nom: "Socle TBox & SHACL CWA", statut: "🟢 PASSED" });

// 2. Phase / Portée (inchangé)
const phaseDisplayList = phasesList.map(p => `${p.code} — ${p.nom} (${p.statut})`);
const selectedPhaseObj = await tp.system.suggester(phaseDisplayList, phasesList) || phasesList[0];
const targetPCode = selectedPhaseObj.code;
const pNom = selectedPhaseObj.nom;
const pStatut = selectedPhaseObj.statut;
const selectedType = await tp.system.suggester(["TRANSVERSAL", "USECASE_METIER", "USECASE_TECHNIQUE"], ["TRANSVERSAL", "USECASE_METIER", "USECASE_TECHNIQUE"]) || "TRANSVERSAL";
let porteeCode = "FWK";
if (selectedType === "USECASE_METIER") porteeCode = "MET";
if (selectedType === "USECASE_TECHNIQUE") porteeCode = "TEC";

// 3. Titres (inchangé)
let rawTitle = tp.file.title;
let defaultCleanTitle = rawTitle.replace(/^SPC[-_]+/, "").replace(/_/g, " ");
const specTitre = await tp.system.prompt("Titre complet de la spécification :", defaultCleanTitle);
let defaultSnake = specTitre.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9]/g, "_").replace(/_+/g, "_").replace(/^_+|_+$/g, "");
const titreSnake = await tp.system.prompt("Titre court (snake_case) :", defaultSnake);
const specDescription = await tp.system.prompt("Résumé / Description courte (1 phrase) :", "");

// 4. Domaine (NOUVEAU — suggère la vraie table 0, pas la portée)
const domainCodes = ["CT","HW","IN","OR","QU","SE","SH","TB","TEC","MET"];
const domaineDefaut = await tp.system.suggester(domainCodes, domainCodes) || "OR";

// 5. UID mnémonique (CORRIGÉ — prompt au lieu du substring bugué)
const uidMnemonic = await tp.system.prompt("Mnémonique de la 1re exigence (3-4 MAJUSCULES, ex: DEM, AGE, GOU) :",
    titreSnake.substring(0, 3).toUpperCase());
const defaultExUid = `EXG-${porteeCode}-${targetPCode}-${uidMnemonic.toUpperCase()}_1`;

// 6. Publics visés (inchangé)
const publicPresets = ["Architectes Ontologues", "Développeurs DevSecOps", "Analystes CTI / SOC, Lead Tech", "Architectes Ontologues, Analystes CTI / SOC", "✏️ Autre combinaison..."];
let chosenPublic = await tp.system.suggester(publicPresets, publicPresets) || publicPresets[0];
if (chosenPublic.startsWith("✏️")) chosenPublic = await tp.system.prompt("Saisir le(s) public(s) visé(s) :", "Architectes Ontologues");
const publicList = chosenPublic.split(",").map(p => p.trim()).filter(p => p.length > 0);

// 7. Référence
const revisionNum = 1;
const revisionSuffix = String(revisionNum).padStart(2, "0");
const specReference = `SPC-${porteeCode}-${targetPCode}-${titreSnake}_${revisionSuffix}`;

// 8. MÉTADONNÉES SEULEMENT — pas d'exigences ici (SSOT : le corps fait foi,
//    le YAML des exigences est régénéré par SPEC_Update_yml depuis la table §4)
app.fileManager.processFrontMatter(tp.config.target_file, (fm) => {
    fm["type"] = "spec";
    fm["reference"] = specReference;
    fm["revision"] = revisionNum;
    fm["titre"] = specTitre;
    fm["titre_court"] = titreSnake;
    fm["description"] = specDescription;
    fm["phase_code"] = targetPCode;
    fm["phase_nom"] = pNom;
    fm["statut"] = pStatut;
    fm["portee"] = selectedType;
    fm["public_vise"] = publicList;
});
-%>
# 📜 <% specTitre %>

## 📖 1. Résumé Exécutif & Glossaire

### 1.1 Objectif
Décrire en 2-3 phrases le but de cette spécification, son rôle dans l'architecture DKG-CyberSec et sa valeur métier/technique.

### 1.2 Glossaire Métier & Technique
 | Acronyme / Concept | Définition              | Contexte DKG                                 |
 | :----------------- | :---------------------- | :------------------------------------------- |
 | **DKG**            | Dynamic Knowledge Graph | Graphe de connaissances dynamique du projet. |

## 🏗️ 2. Périmètre & Rôle de la Spécification
- **Positionnement dans l'Architecture** : Préciser s'il s'agit d'un socle transversal, d'un cas d'usage métier ou d'une implémentation technique.
- **Gouvernance & Validation** : Validé par l'Architecte Sémantique et IA SOC.

```mermaid
graph TD
    A[Composant A] --> B[Composant B]
```

## 📐 3. Spécifications Formelles & Règles

### 3.1 Axiomes, Structures RDF ou Scénario Métier

[Description détaillée, règles formelles, schémas de données ou flux d'agents]

### 3.2 Directives d'Implémentation Code & Scripts

[Règles d'utilisation des objets de `config.py`, contraintes d'immutabilité Pydantic V2, séparation TLP. Chaque point d'application porte l'UID complet en commentaire.]

## 📊 4. Matrice des Exigences & Critères d'Acceptation (EXG-)

> **SSOT** : cette table est la source des exigences. Après édition, exécuter le script **SPEC_Update_yml** sur ce fichier pour régénérer le frontmatter. Ne jamais éditer `exigences:` dans le YAML à la main.  
> **Convention (GOU_24)** : UID complets, MAJUSCULES, uniques (ex. `EXG-MET-P8-DEM_1`).

|Identifiant|UID|Domaine|Core/Non-Core|Intitulé de l'Exigence|Description & Critères d'Acceptation|Mode de Test / Asset|
|---|---|---|---|---|---|---|
|<% defaultExUid %>|`<% defaultExUid %>`|`<% domaineDefaut %>`|Core|Exigence Initiale|Description formelle et critères d'acceptation.|Pytest / SPARQL / SHACL|

## 🛡️ 5. Outillage, CI/CD & Traçabilité Pytest

- **Scripts de Génération / Exécution** : `03-Application/[script].py`
- **Suites de Tests Associées** : `03-Application/Test/test_[module].py`
- **Critères d'Acceptation** : [Validation syntaxique, tests unitaires]
- **Artefacts Produits** : [Fichier_Maître.ttl]

## 📚 6. Documents Liés & Références

- **[SPEC-PARENTE]** : [Lien vers la spécification de niveau supérieure ou dépendante]