```
├── 00-Projet/                                        # Documents de la gestion de projet
│   ├── AssistanceLLM/
│   │   ├── Kits_Amorçage/                    # context bundle  (.md) permet aux nouvelles discussions LLM de collecter l'avancement
│   │   ├── Prompts/                               #  Prompts d'initialisation d'une discussion et ceux cadran chaque étapes
│   ├── PhaseX/                                      #  décomposées par phases
│   ├── REX/
│   └── Templates/                                  # utilisés par Obsidian/templeter pour générer des vues 
├── 01-Principes_Spécifications/          #  Documents sur les Princes technique et les SPEC avec 
│   ├── TRANSVERSAL/                          #  SPEC transverses applicable à d'autre cas d'usages
│   ├── USECASE_METIER/                    #  SPEC Métier Cyber 
│   └── USECASE_TECHNIQUE/             #  SPEC technique pour le dev
├── 02-Donnees/
│   ├── Input_Phases/                             # Données d'entrée générées pour le cas d'usage
│   │   └── PhaseX/                                     décomposées par phases
│   ├── Master_Transversal/                   #  Données capitalisées au travers des phases
│   └── Snapshots_Phases/                    #  Données générées dans chaque phases (snapshot)
│       └── PhaseX/                                        décomposées par phases
	└── 03-Application/                        #  Section des codes python
    ├── config.py                                      #  fichier utilisé contenant les variables utilisées par les script
    ├── conftest.py
    ├── models/                                         #  models chargés localement avec leur paramètres
    ├── PhaseX/                                         #  Script des fonctionnalités
    └── Test/                                               #  Script de test vérifiant un ensemble d'exigences

```
ci-dessous vue sur les princpaux fichiers avec lien d'accés directe  (utilise plugins Obsidian )

## Version dynamique avec Obsidan - plugins - javascript enables
###  1 - Index des répertoires `/01-Principes_Specification/[TRANSVERAL,USECASE_METIER,USECASE_TECHNIQUE]`

```dataviewjs
// ==============================================================================
// 6. Génération du Tableau 2 : Registre des Spécifications (Dossiers Cibles Strict)
// ==============================================================================

const specsFolderPath = "01-Principes_Spécifications";

// Liste stricte des 3 répertoires autorisés
const targetFolders = ["TRANSVERSAL", "USECASE_METIER", "USECASE_TECHNIQUE"];

const specFiles = app.vault.getFiles().filter(f => {
    if (f.extension !== "md") return false;
    
    // Vérifier si le fichier est strictement dans l'un des 3 sous-dossiers
    const relPath = f.path.substring(specsFolderPath.length + 1);
    const subFolder = relPath.split("/")[0];
    
    return targetFolders.includes(subFolder);
});

const tableRowsSpecs = [];

for (let file of specFiles) {
    const relPath = file.path.substring(specsFolderPath.length + 1);
    const subFolder = relPath.split("/")[0]; // TRANSVERSAL, USECASE_METIER ou USECASE_TECHNIQUE
    
    // Formatage propre du nom de la catégorie
    let catDisplay = subFolder.replace("_", " ");

    // 1. Lecture directe des métadonnées Dataview
    const page = dv.page(file.path);
    let statut = "⚪ Planifié";
    let phaseAssociee = "";

    if (page) {
        if (page.statut) statut = page.statut;
        
        // Recherche prioritaire dans le YAML
        if (page.phase_code) phaseAssociee = page.phase_code;
        else if (page.phase_num) phaseAssociee = `P${String(page.phase_num).padStart(2, '0')}`;
        else if (page.phase) phaseAssociee = page.phase;
    }

    // 2. Fallback dynamique par Regex sur le nom du fichier si absent du YAML
    if (!phaseAssociee || phaseAssociee === "Transversal") {
        const fileName = file.name;
        
        // Détecte -P05-, -P06-, -UC01-, -SOCLE-01-, etc.
        const matchP = fileName.match(/(?:-P|-SOCLE-|-UC)(\d+)/i);
        if (matchP) {
            phaseAssociee = `P${matchP[1].padStart(2, '0')}`;
        } else {
            phaseAssociee = "Transversal";
        }
    }

    tableRowsSpecs.push([
        `**${catDisplay}**`,
        `**${phaseAssociee}**`,
        `[[${file.path}|${file.name}]]`,
        statut
    ]);
}

// Tri : Catégorie -> Phase -> Nom de fichier
tableRowsSpecs.sort((a, b) => 
    a[0].localeCompare(b[0]) || 
    a[1].localeCompare(b[1]) || 
    a[2].localeCompare(b[2])
);

dv.header(2, "Index des répertoires `/01-Principes_Specification/[TRANSVERAL,USECASE_METIER,USECASE_TECHNIQUE]`");
dv.table(
    ["Portée", "Phase", "Document Spécification", "Statut SPEC"],
    tableRowsSpecs
);
```

###  2 - Index des répertoires `/02-Donnes/Snaphots_Phases/PhaseX/`
```dataviewjs
// 1. Configuration des chemins sources
const snapshotsPath = "02-Donnees/Snapshots_Phases";
const configFilePath = "03-Application/config.py";
const roadmapFilePath = "00-Projet/Roadmap_Suivi-Avancement.md";
const specsFolderPath = "01-Principes_Spécification";

// 2. Lecture du fichier config.py
let configFileText = "";
const configFile = app.vault.getAbstractFileByPath(configFilePath);
if (configFile) {
    configFileText = await app.vault.read(configFile);
}

// 3. Parsing de la Roadmap pour mapper Phase -> Intitulé
const roadmapMap = new Map();
const roadmapFile = app.vault.getAbstractFileByPath(roadmapFilePath);

if (roadmapFile) {
    const roadmapContent = await app.vault.read(roadmapFile);
    const lines = roadmapContent.split("\n");
    let inSection2 = false;

    for (let line of lines) {
        if (line.includes("## 2")) { inSection2 = true; continue; }
        if (inSection2 && line.includes("## 3")) { break; }

        if (inSection2 && line.startsWith("|")) {
            const cleanLine = line.replace(/<br\s*\/?>/gi, " ").replace(/<[^>]*>/g, "").replace(/\*\*/g, "");
            const cols = cleanLine.split("|").map(c => c.trim());

            if (cols.length >= 5 && cols[2] && /^P\d+$/i.test(cols[2])) {
                const pCode = cols[2];
                const pNum = parseInt(pCode.replace(/[^0-9]/g, ""), 10);
                roadmapMap.set(pNum, {
                    code: pCode,
                    nom: cols[3] || ""
                });
            }
        }
    }
}

// 4. Scan des répertoires physiques Snapshots_Phases
const allSnapshotFiles = app.vault.getFiles().filter(f => f.path.startsWith(snapshotsPath));
const phaseFolders = new Map();

allSnapshotFiles.forEach(file => {
    const relativePath = file.path.substring(snapshotsPath.length + 1);
    const pathParts = relativePath.split("/");

    if (pathParts.length > 1) {
        const folderName = pathParts[0];
        const match = folderName.match(/^Phase(\d+)_/i);

        if (match) {
            const pNum = parseInt(match[1], 10);
            if (!phaseFolders.has(pNum)) {
                phaseFolders.set(pNum, { folderName: folderName, files: [] });
            }
            phaseFolders.get(pNum).files.push(file);
        }
    }
});

// 5. Génération du Tableau 1 : Snapshots & Phase_Content
const sortedPhaseNums = Array.from(phaseFolders.keys()).sort((a, b) => a - b);
const tableRowsSnapshots = [];

sortedPhaseNums.forEach(pNum => {
    const pData = phaseFolders.get(pNum);
    const rData = roadmapMap.get(pNum) || { 
        code: `P${pNum}`, 
        nom: pData.folderName.split("_").slice(1).join(" ") || "Inconnu"
    };

    // Détection du document Cadrage Phase (00-Projet/PhaseX/Phase_Content.md)
    const phaseContentPath = `00-Projet/Phase${pNum}/Phase_Content.md`;
    const phaseContentFile = app.vault.getAbstractFileByPath(phaseContentPath);
    const phaseContentLink = phaseContentFile 
        ? `[[${phaseContentFile.path}|📋 Phase_Content.md]]` 
        : `—`;

    let ttlFiles = [];
    let mdFiles = [];
    let otherFiles = [];

    pData.files.forEach(file => {
        const isConfigured = configFileText.includes(file.name);
        const displayLink = isConfigured 
            ? `[[${file.path}|${file.name}]] ⚙️` 
            : `[[${file.path}|${file.name}]]`;

        if (file.extension === "ttl") {
            ttlFiles.push(displayLink);
        } else if (file.extension === "md") {
            mdFiles.push(displayLink);
        } else {
            otherFiles.push(displayLink);
        }
    });

    tableRowsSnapshots.push([
        `**${rData.code}** : ${rData.nom}`,
        phaseContentLink,
        ttlFiles.length > 0 ? ttlFiles.join("<br>") : "—",
        mdFiles.length > 0 ? mdFiles.join("<br>") : "—",
        otherFiles.length > 0 ? otherFiles.join("<br>") : "—"
    ]);
});

dv.header(2, "Index des répertoires `/02-Donnes/Snaphots_Phases/PhaseX`");
dv.table(
    ["Phase & Intitulé", "Cadrage Phase (00-Projet)", "Artefacts RDF (.ttl)", "Doc Miroir (.md)", "Autres Fichiers"],
    tableRowsSnapshots
);


```

> **Légende :** Les artefacts accompagnés de l'icône **`⚙️`** sont ceux configurés et référencés dans `03-Application/config.py`.


###  3 - Index des répertoires `/02-Donnes/Master_Transversal/`

```dataviewjs
// ==============================================================================
// Vue : Master Transversal (Colonnes natives Obsidian + Word Wrap)
// ==============================================================================

const masterFolderPath = "02-Donnees/Master_Transversal";

// 1. Récupération des fichiers sous Master_Transversal
const masterFiles = app.vault.getFiles().filter(f => 
    f.path.startsWith(masterFolderPath + "/")
);

// 2. Regroupement par sous-dossier
const groupedByDir = {};

masterFiles.forEach(file => {
    const relPath = file.path.substring(masterFolderPath.length + 1);
    const pathSegments = relPath.split("/");
    
    // Nom du sous-dossier (ou "Racine" si le fichier est directement dans Master_Transversal)
    const dirName = pathSegments.length > 1 ? pathSegments[0] : "Racine";

    if (!groupedByDir[dirName]) {
        groupedByDir[dirName] = [];
    }
    groupedByDir[dirName].push(file);
});

// 3. Affichage regroupé en colonnes natives
dv.header(2, "📂 Données Master Transversal");

const sortedDirs = Object.keys(groupedByDir).sort();

if (sortedDirs.length === 0) {
    dv.paragraph("*Aucun fichier trouvé dans /02-Donnees/Master_Transversal/*");
} else {
    let html = '<div style="column-count: 2; column-gap: 2rem;">';
    
    for (const dir of sortedDirs) {
        html += '<div style="break-inside: avoid; margin-bottom: 1.5rem; word-break: break-word;">';
        html += '<h4 style="margin-top: 0; margin-bottom: 0.5rem; border-bottom: 1px solid var(--background-modifier-border); padding-bottom: 0.3rem;">📁 Subdir: ' + dir + '</h4>';
        html += '<ul style="margin: 0; padding-left: 1.2rem;">';
        
        const sortedFiles = groupedByDir[dir].sort((a, b) => a.name.localeCompare(b.name));
        for (const file of sortedFiles) {
            html += '<li style="margin-bottom: 0.3rem;"><a class="internal-link" href="' + file.path + '">' + file.name + '</a></li>';
        }
        
        html += '</ul></div>';
    }
    
    html += '</div>';
    dv.paragraph(html);
}
```
###  4 - Index des répertoires `/02-Donnes/Input_Phases/`

```dataviewjs
// ==============================================================================
// Vue : Données d'Entrée par Phase (/02-Donnees/Input_Phases/)
// ==============================================================================

const inputFolderPath = "02-Donnees/Input_Phases";

// 1. Récupération des fichiers sous Input_Phases
const inputFiles = app.vault.getFiles().filter(f => 
    f.path.startsWith(inputFolderPath + "/")
);

// 2. Regroupement par Phase
const groupedByPhaseInput = {};

inputFiles.forEach(file => {
    const relPath = file.path.substring(inputFolderPath.length + 1);
    const pathSegments = relPath.split("/");
    const subFolder = pathSegments.length > 1 ? pathSegments[0] : "Transversal";
    
    let phaseCode = "Transversal";
    const matchP = subFolder.match(/(?:Phase|P)[_-]?(\d+)/i);
    if (matchP) {
        phaseCode = `P${matchP[1].padStart(2, '0')}`;
    }

    if (!groupedByPhaseInput[phaseCode]) {
        groupedByPhaseInput[phaseCode] = [];
    }
    groupedByPhaseInput[phaseCode].push(file);
});

// 3. Affichage regroupé
dv.header(2, "📥 Données d'Entrée (Input Phases)");

const sortedInputPhases = Object.keys(groupedByPhaseInput).sort();

if (sortedInputPhases.length === 0) {
    dv.paragraph("*Aucun fichier trouvé dans /02-Donnees/Input_Phases/*");
} else {
    for (const phase of sortedInputPhases) {
        const headerTitle = phase.startsWith("P") ? `Phase ${phase}` : phase;
        dv.header(3, `📌 ${headerTitle}`);
        
        const filesList = groupedByPhaseInput[phase]
            .sort((a, b) => a.name.localeCompare(b.name))
            .map(f => `[[${f.path}|${f.name}]] (${f.extension.toUpperCase()})`);
        
        dv.list(filesList);
    }
}
```



###  5 - Index des répertoires `/03-Applications/PhaseX/`


```dataviewjs
const appFolderPath = "03-Application";

const appPyFiles = app.vault.getFiles().filter(f => {
    if (f.extension.toLowerCase() !== "py") return false;
    if (!f.path.startsWith(appFolderPath + "/")) return false;
    const relPath = f.path.substring(appFolderPath.length + 1);
    const pathSegments = relPath.split("/");
    return pathSegments.length >= 2 && /^Phase/i.test(pathSegments[0]);
});

const grouped = {};
appPyFiles.forEach(file => {
    const subFolder = file.path.substring(appFolderPath.length + 1).split("/")[0];
    const matchP = subFolder.match(/^Phase[_-]?(\d+)/i);
    const phaseCode = matchP ? `P${matchP[1].padStart(2, '0')}` : "P00";
    (grouped[phaseCode] = grouped[phaseCode] || []).push(file);
});

dv.header(2, "💻 Code d'Application Python (.py) par Phase");

const sortedPhases = Object.keys(grouped).sort();
if (sortedPhases.length === 0) {
    dv.paragraph("*Aucun fichier Python trouvé.*");
} else {
    let html = `<div style="column-count: 2; column-gap: 2rem;">`;
    for (const phase of sortedPhases) {
        html += `<div style="break-inside: avoid; margin-bottom: 1.5rem;">`;
        html += `<h4 style="margin-top:0;">📌 Phase ${phase}</h4><ul>`;
        grouped[phase].sort((a, b) => a.name.localeCompare(b.name)).forEach(f => {
            html += `<li><a class="internal-link" href="${f.path}">${f.name}</a></li>`;
        });
        html += `</ul></div>`;
    }
    html += `</div>`;
    dv.paragraph(html);
}
```






### 6 - Index du répertoire `/03-Applications/Test/` 

```dataviewjs
const testFolderPath = "03-Application/Test";

const testPyFiles = app.vault.getFiles().filter(f => 
    f.extension.toLowerCase() === "py" && f.path.startsWith(testFolderPath)
);

const grouped = {};
testPyFiles.forEach(file => {
    const matchTest = file.name.match(/test[_-](?:phase|p)[_-]?(\d+)/i) || file.name.match(/(?:Phase|P)[_-]?(\d+)/i);
    const phaseCode = matchTest ? `P${matchTest[1].padStart(2, '0')}` : "P00";
    (grouped[phaseCode] = grouped[phaseCode] || []).push(file);
});

dv.header(2, "🧪 Fichiers de Test Python (.py) par Phase");

const sortedPhases = Object.keys(grouped).sort();
if (sortedPhases.length === 0) {
    dv.paragraph("*Aucun fichier de test Python trouvé.*");
} else {
    let html = `<div style="column-count: 2; column-gap: 2rem;">`;
    for (const phase of sortedPhases) {
        html += `<div style="break-inside: avoid; margin-bottom: 1.5rem;">`;
        html += `<h4 style="margin-top:0;">🧪 Phase ${phase}</h4><ul>`;
        grouped[phase].sort((a, b) => a.name.localeCompare(b.name)).forEach(f => {
            html += `<li><a class="internal-link" href="${f.path}">${f.name}</a></li>`;
        });
        html += `</ul></div>`;
    }
    html += `</div>`;
    dv.paragraph(html);
}
```



## Version Statique

###  1 - Index des répertoires `/01-Principes_Specification/[TRANSVERAL,USECASE_METIER,USECASE_TECHNIQUE]`

|Portée12|Phase|Document Spécification|Statut SPEC|
|---|---|---|---|
|**TRANSVERSAL**|**P1**|[SPC-FWK-P1-GOUVERNANCE_01.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/TRANSVERSAL/SPC-FWK-P1-GOUVERNANCE_01.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**TRANSVERSAL**|**P1**|[SPC-FWK-P1-T-RBOX_SHACL_01.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/TRANSVERSAL/SPC-FWK-P1-T-RBOX_SHACL_01.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**TRANSVERSAL**|**P2**|[SPC-FWK-P2-ABOX_01.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/TRANSVERSAL/SPC-FWK-P2-ABOX_01.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**TRANSVERSAL**|**P3**|[SPC-FWK-P3-CTI__Framework_External.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/TRANSVERSAL/SPC-FWK-P3-CTI__Framework_External.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**TRANSVERSAL**|**P5**|[SPC-FWK-P5-RULES_01__Reasoning_Rules_RBox_Inference.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/TRANSVERSAL/SPC-FWK-P5-RULES_01__Reasoning_Rules_RBox_Inference.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**USECASE METIER**|**P2**|[SPC-MET-P2-CARTO_01__Cartographie_Infrastructures.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/USECASE_METIER/SPC-MET-P2-CARTO_01__Cartographie_Infrastructures.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**USECASE METIER**|**P3**|[SPC-MET-P3-SILENT_01__Scenario_Silent_Cascade.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/USECASE_METIER/SPC-MET-P3-SILENT_01__Scenario_Silent_Cascade.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**USECASE METIER**|**P5**|[SPC-MET-P5-CTI_01__Ingestion_Traitement_Intelligence_sur_les_Menaces(CTI).md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/USECASE_METIER/SPC-MET-P5-CTI_01__Ingestion_Traitement_Intelligence_sur_les_Menaces\(CTI\).md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**USECASE TECHNIQUE**|**P2**|[SPC-TEC-P2-ABOX_01__Instanciation_ABox_Cyber.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/USECASE_TECHNIQUE/SPC-TEC-P2-ABOX_01__Instanciation_ABox_Cyber.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**USECASE TECHNIQUE**|**P5**|[SPC-TEC-P5-CONSO_01__AgentMITM_Consolidation_SKOS-RéconciliationSémantique.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/USECASE_TECHNIQUE/SPC-TEC-P5-CONSO_01__AgentMITM_Consolidation_SKOS-R%C3%A9conciliationS%C3%A9mantique.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**USECASE TECHNIQUE**|**P5**|[SPC-TEC-P5-DATA_01_Raisonnement_Propagation_Silent_Cascade.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/USECASE_TECHNIQUE/SPC-TEC-P5-DATA_01_Raisonnement_Propagation_Silent_Cascade.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|
|**USECASE TECHNIQUE**|**P5**|[SPC-TEC-P5-NER_01__Ingestion_CTI_NER_Normalisation.md](app://obsidian.md/01-Principes_Sp%C3%A9cifications/USECASE_TECHNIQUE/SPC-TEC-P5-NER_01__Ingestion_CTI_NER_Normalisation.md)|![🟢](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f7e2.png) PASSED|


###  2 - Index des répertoires `/02-Donnes/Snaphots_Phases/PhaseX/`


|Phase & Intitulé6|Cadrage Phase (00-Projet)|Artefacts RDF (.ttl)|Doc Miroir (.md)|Autres Fichiers|
|---|---|---|---|---|
|**P1** : Socle TBox & SHACL CWA|[![📋](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f4cb.png) Phase_Content.md](app://obsidian.md/00-Projet/Phase1/Phase_Content.md)|[DKG_TBox_Master.ttl](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase1_Socle/DKG_TBox_Master.ttl) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)  <br>[DKG_SHACL_Master.ttl](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase1_Socle/DKG_SHACL_Master.ttl) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|[DKG_TBox_Master.md](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase1_Socle/DKG_TBox_Master.md) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|[DKG_TBox_Master.json](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase1_Socle/DKG_TBox_Master.json)|
|**P2** : Cartographie ABox Interne|[![📋](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f4cb.png) Phase_Content.md](app://obsidian.md/00-Projet/Phase2/Phase_Content.md)|[DKG_ABox_Master.ttl](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase2_ABox/DKG_ABox_Master.ttl) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|[DKG_ABox_Master.md](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase2_ABox/DKG_ABox_Master.md) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|—|
|**P3** : Ingestion CTI Structurée|[![📋](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f4cb.png) Phase_Content.md](app://obsidian.md/00-Projet/Phase3/Phase_Content.md)|[DKG_ABox_CTI_External.ttl](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase3_CTI/DKG_ABox_CTI_External.ttl) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|[DKG_ABox_CTI_External.md](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase3_CTI/DKG_ABox_CTI_External.md) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|—|
|**P4** : Ingestion CTI Textuelle (NER)|[![📋](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f4cb.png) Phase_Content.md](app://obsidian.md/00-Projet/Phase4/Phase_Content.md)|[DKG_ABox_CTI_U_External.ttl](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase4_CTI/DKG_ABox_CTI_U_External.ttl) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|[DKG_ABox_CTI_U_External.md](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase4_CTI/DKG_ABox_CTI_U_External.md) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|—|
|**P5** : Agent MITM & Reasoning Base|[![📋](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f4cb.png) Phase_Content.md](app://obsidian.md/00-Projet/Phase5/Phase_Content.md)|[DKG_TBox_Master.ttl](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase5_Reasoning_MITM/DKG_TBox_Master.ttl) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)  <br>[DKG_MITM_Test_Alignment.ttl](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase5_Reasoning_MITM/DKG_MITM_Test_Alignment.ttl)  <br>[DKG_ABox_Infered.ttl](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase5_Reasoning_MITM/DKG_ABox_Infered.ttl) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|[DKG_MITM_Test_Alignment.md](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase5_Reasoning_MITM/DKG_MITM_Test_Alignment.md)  <br>[DKG_TBox_Master.md](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase5_Reasoning_MITM/DKG_TBox_Master.md) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)  <br>[DKG_ABox_Infered.md](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase5_Reasoning_MITM/DKG_ABox_Infered.md) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|—|
|**P6** : API Gateway & Ségrégation TLP|[![📋](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/1f4cb.png) Phase_Content.md](app://obsidian.md/00-Projet/Phase6/Phase_Content.md)|[DKG_ABox_Infered.ttl](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase6_NER_Local/DKG_ABox_Infered.ttl) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|[DKG_ABox_Infered.md](app://obsidian.md/02-Donnees/Snapshots_Phases/Phase6_NER_Local/DKG_ABox_Infered.md) ![⚙️](https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/2699.png)|—|
> **Légende :** Les artefacts accompagnés de l'icône **`⚙️`** sont ceux configurés et référencés dans `03-Application/config.py`.