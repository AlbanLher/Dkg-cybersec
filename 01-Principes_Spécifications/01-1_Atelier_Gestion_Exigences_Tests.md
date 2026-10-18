
## Tableau Humain

## Dashboard

```dataviewjs
(async () => {
    // 1. Collecte des exigences
    let specPages = dv.pages().where(p => p.type === "spec" && p.exigences && Array.isArray(p.exigences));
    let totalExgs = 0;
    let validExgs = new Set();
    
    for (let page of specPages) {
        for (let ex of page.exigences) {
            let id = (ex.uid || ex.id || "").trim();
            if (id) {
                validExgs.add(id);
                totalExgs++;
            }
        }
    }

    // 2. Collecte des tests et des liaisons
    let pyFiles = app.vault.getFiles().filter(f => f.path.includes("03-Application/Test/") && f.path.endsWith(".py"));
    let coveredExgs = new Set();
    let orphanFunctionsCount = 0;

    for (let file of pyFiles) {
        let content = await app.vault.read(file);
        let matches = content.match(/EXG-[\w-]+/gi) || [];
        matches.forEach(id => {
            let cleanId = id.trim();
            if (validExgs.has(cleanId)) coveredExgs.add(cleanId);
        });

        // Analyse fonction par fonction pour les orphelins
        let functions = content.split(/(?=def test_)/);
        for (let funcBlock of functions) {
            if (!funcBlock.trim().startsWith("def test_")) continue;
            let funcMatches = funcBlock.match(/EXG-[\w-]+/gi) || [];
            let validFuncMatches = funcMatches.map(id => id.trim()).filter(id => validExgs.has(id));
            if (validFuncMatches.length === 0) {
                orphanFunctionsCount++;
            }
        }
    }

    let coverageRate = totalExgs > 0 ? ((coveredExgs.size / totalExgs) * 100).toFixed(1) : 0;

    // Affichage sous forme de Callout / KPIs
    dv.paragraph(`
> [!info] **Tableau de Bord Exigences & Traçabilité V-Cycle**
> - 📋 **Total Exigences Actives :** \`${totalExgs}\`
> - 🎯 **Exigences Couvertes par un Test :** \`${coveredExgs.size} (${coverageRate}%)\`
> - ⚠️ **Exigences Non Couvertes :** \`${totalExgs - coveredExgs.size}\`
> - 🧩 **Fonctions de test sans lien explicite :** \`${orphanFunctionsCount}\`
    `);
})();
```


### 0. Definition des Domaines

| **Code Domaine** | **Nom Complet**             | **Description & Périmètre**                                                      | **Exemples de Périmètre**                                        |
| ---------------- | --------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| **`CT`**         | Cyber Threat Intelligence   | Modélisation des données CTI externes, vulnérabilités et menaces.                | CVE, CWE, CAPEC, CISA KEV, scores CVSS.                          |
| **`HW`**         | Hardware & Infrastructures  | Contraintes matérielles, d'exécution locale et de performance système.           | Limites RAM 16 Go, absence de GPU, mode Air-Gapped.              |
| **`IN`**         | Inférence & Graph Analytics | Règles de raisonnement sémantique, déduction de liens et calculs de propagation. | Détection de cascade de risque, classe `HighRiskAsset`.          |
| **`OR`**         | Organisation & Processus    | Gouvernance du projet, méthodologie Spec-Driven et standards de livraison.       | Traçabilité des phases, conventions Git, parité Master/Snapshot. |
| **`QU`**         | Qualité & Conformité        | Règles de validation de la qualité des données et métriques d'intégrité.         | Contrôles pySHACL, fermetures CWA, 0 violation SHACL.            |
| **`SE`**         | Sécurité & Isolation        | Étanchéité, marquage TLP et politiques de contrôle d'accès aux graphes.          | Ségrégation TLP:CLEAR vs TLP:RED, isolation des snapshots.       |
| **`SH`**         | SHACL Shapes                | Modélisation abstraite et concrète des formes de validation de structures.       | `sh:NodeShape`, `sh:PropertyShape`, méta-shapes.                 |
| **`TB`**         | TBox & Ontologies Master    | Définition formelle des classes, propriétés, relations inverses et SKOS.         | Classes OWL, `rdfs:domain`/`range`, `owl:inverseOf`, SKOS.       |
| **`TEC`**        | Technique & Core Framework  | Socle applicatif, gestion des types de données, immutabilité et bas niveau.      | Schemas Pydantic V2, horodatage UTC, immutabilité payloads.      |


### 1. Cartographie des Spécifications
```dataview
TABLE WITHOUT ID
    reference AS "Référence",
    phase_code AS "Phase",
    titre AS "Titre Spécification",
    description AS "Description / Objet",
    statut AS "Statut"
FROM "01-Principes_Spécifications"
WHERE type = "spec"
SORT phase_code ASC, reference ASC
```


### 2. Table Spec_Exigence  

```dataviewjs
let pages = dv.pages('"01-Principes_Spécifications"').where(p => p.type === "spec");
let rows = [];

for (let page of pages) {
    let specRef = page.reference || page.file.name;

    if (page.exigences && Array.isArray(page.exigences)) {
        for (let ex of page.exigences) {
            // Conversion propre du booléen core en texte
            let coreStatus = "-";
            if (ex.core !== undefined) {
                coreStatus = ex.core ? "Core" : "Non-Core";
            }

            rows.push([
                specRef,
                ex.uid || ex.id || "-",
                ex.domaine || "-",
                coreStatus,
                ex.titre || ex.intitule || "-"
            ]);
        }
    }
}

if (rows.length === 0) {
    dv.paragraph("⚠️ **Aucune exigence trouvée.** Vérifiez que vos fichiers dans `01-Principes_Spécifications` possèdent bien `type: spec` dans leur frontmatter.");
} else {
    // Tri par spécification puis par ID
    rows.sort((a, b) => (a[0] + a[1]).localeCompare(b[0] + b[1]));
    
    dv.table(
        ["Spécification", "ID Exigence", "Domaine", "Core / Non-Core", "Intitulé"],
        rows
    );
}

```


### 3. Table Spec_Exigence_TSV 

```dataviewjs
let pages = dv.pages('"01-Principes_Spécifications"').where(p => p.type === "spec");

let header = "Spécification\tID Exigence\tDomaine\tCore / Non-Core\tIntitulé";
let rows = [];

for (let page of pages) {
    let specRef = page.reference || page.file.name;

    if (page.exigences && Array.isArray(page.exigences)) {
        for (let ex of page.exigences) {
            let id = ex.uid || ex.id || "-";
            let domaine = ex.domaine || "-";
            
            let coreStatus = "-";
            if (ex.core !== undefined) {
                coreStatus = ex.core ? "Core" : "Non-Core";
            }
            
            let titre = ex.titre || ex.intitule || "-";
            titre = String(titre).replace(/(\r\n|\n|\r)/gm, " ");

            rows.push(`${specRef}\t${id}\t${domaine}\t${coreStatus}\t${titre}`);
        }
    }
}

if (rows.length === 0) {
    dv.paragraph("⚠️ **Aucune exigence trouvée.** Vérifiez que vos fichiers dans `01-Principes_Spécifications` possèdent bien `type: spec` dans leur frontmatter.");
} else {
    // Tri alphabétique des lignes de données
    rows.sort((a, b) => a.localeCompare(b));
    
    // Insertion de l'en-tête en première position
    rows.unshift(header);

    dv.paragraph("```tsv\n" + rows.join("\n") + "\n```");
}
```

---
---
### 4. Couverture des exigences par des tests
```dataviewjs
(async () => {
    // 1. Récupération des fichiers de test Python dans le coffre avec la regex robuste aux underscores
    let pyFiles = app.vault.getFiles().filter(f => f.path.endsWith(".py"));
    let testMapping = {};
    let nonRegMapping = {}; 

    for (let file of pyFiles) {
        let content = await app.vault.read(file);
        let hasNonRegMark = /non_regression/i.test(content);

        let matches = content.match(/EXG-[\w-]+/gi);
        if (matches) {
            let uniqueExgs = [...new Set(matches.map(id => id.trim()))];
            for (let exId of uniqueExgs) {
                if (!testMapping[exId]) testMapping[exId] = [];
                if (!testMapping[exId].includes(file.name)) {
                    testMapping[exId].push(file.name);
                }
                if (hasNonRegMark) {
                    nonRegMapping[exId] = true;
                }
            }
        }
    }

    // 2. Lecture des spécifications (élargie à tout le coffre pour inclure les sous-dossiers)
    let pages = dv.pages().where(p => p.type === "spec" && p.exigences && Array.isArray(p.exigences));
    let rows = [];

    for (let page of pages) {
        let specRef = page.reference || page.file.name;
        let specLink = `[[${page.file.path}|${specRef}]]`;

        for (let ex of page.exigences) {
            let id = (ex.uid || ex.id || "-").trim();
            let domaine = ex.domaine || "-";
            
            let coreStatus = "-";
            if (ex.core !== undefined) {
                coreStatus = ex.core ? "Core" : "Non-Core";
            }
            
            let nonRegStatus = nonRegMapping[id] ? "✅" : "❌";
            
            let titre = ex.titre || ex.intitule || "-";
            titre = String(titre).replace(/(\r\n|\n|\r)/gm, " ");

            let testedBy = testMapping[id] ? testMapping[id].join(", ") : "⚠️ Non couvert";

            rows.push([
                specLink,
                id,
                domaine,
                coreStatus,
                nonRegStatus,
                titre,
                testedBy
            ]);
        }
    }

    if (rows.length === 0) {
        dv.paragraph("⚠️ **Aucune exigence trouvée.**");
    } else {
        rows.sort((a, b) => (a[0] + a[1]).localeCompare(b[0] + b[1]));
        
        dv.table(
            ["Spécification", "ID Exigence", "Domaine", "Core/Non-Core", "NonReg", "Intitulé", "Fichier(s) de Test Associé(s)"],
            rows
        );
    }
})();
```



---
---
### 5. Tests Orphelins

```dataviewjs
(async () => {
    let specPages = dv.pages().where(p => p.type === "spec" && p.exigences && Array.isArray(p.exigences));
    let validExgs = new Set();
    
    for (let page of specPages) {
        for (let ex of page.exigences) {
            let id = (ex.uid || ex.id || "").trim();
            if (id) validExgs.add(id);
        }
    }

    let pyFiles = app.vault.getFiles().filter(f => f.path.includes("03-Application/Test/") && f.path.endsWith(".py"));
    let rows = [];

    for (let file of pyFiles) {
        let content = await app.vault.read(file);
        
        // Vérification globale du fichier
        let fileMatches = content.match(/EXG-[\w-]+/gi) || [];
        let fileHasValidExg = fileMatches.some(id => validExgs.has(id.trim()));

        let functions = content.split(/(?=def test_)/);
        
        for (let funcBlock of functions) {
            if (!funcBlock.trim().startsWith("def test_")) continue;
            
            let funcNameMatch = funcBlock.match(/def\s+(test_[a-zA-Z0-9_]+)\s*\(/);
            let funcName = funcNameMatch ? funcNameMatch[1] : "test_inconnu";
            
            let matches = funcBlock.match(/EXG-[\w-]+/gi) || [];
            let uniqueExgs = [...new Set(matches.map(id => id.trim()))];
            let attachedExgs = uniqueExgs.filter(id => validExgs.has(id));
            
            if (attachedExgs.length === 0) {
                if (!fileHasValidExg) {
                    rows.push([
                        `[[${file.path}|${file.name}]]`,
                        funcName,
                        "❌ Aucun EXG valide dans le fichier (Orphelin Total)"
                    ]);
                } else {
                    // Présent dans le fichier globalement mais absent de la docstring de la fonction
                    rows.push([
                        `[[${file.path}|${file.name}]]`,
                        funcName,
                        "⚠️ Présent au niveau fichier mais manquant dans la docstring fonctionnelle"
                    ]);
                }
            }
        }
    }

    if (rows.length === 0) {
        dv.paragraph("🎉 **Parfait !** Tous les tests sont rattachés à une exigence valide.");
    } else {
        dv.paragraph(`⚠️ **${rows.length} alerte(s) de traçabilité détectée(s) :**`);
        dv.table(
            ["Fichier de Test", "Fonction de Test", "Statut de Traçabilité"],
            rows
        );
    }
})();

```




```dataviewjs
(async () => {
    // 1. Récupérer toutes les exigences valides depuis les specs (dans tout le coffre, y compris les sous-dossiers)
    let specPages = dv.pages().where(p => p.type === "spec" && p.exigences && Array.isArray(p.exigences));
    let validExgs = new Set();
    
    for (let page of specPages) {
        for (let ex of page.exigences) {
            let id = (ex.uid || ex.id || "").trim();
            if (id) validExgs.add(id);
        }
    }

    // 2. Récupérer tous les fichiers .py situés dans le dossier 03-Application/Test/
    let pyFiles = app.vault.getFiles().filter(f => f.path.includes("03-Application/Test/") && f.path.endsWith(".py"));
    let rows = [];

    for (let file of pyFiles) {
        let content = await app.vault.read(file);
        
        // Découpage du fichier par fonction de test (def test_...)
        let functions = content.split(/(?=def test_)/);
        
        for (let funcBlock of functions) {
            if (!funcBlock.trim().startsWith("def test_")) continue;
            
            // Extraire le nom de la fonction de test
            let funcNameMatch = funcBlock.match(/def\s+(test_[a-zA-Z0-9_]+)\s*\(/);
            let funcName = funcNameMatch ? funcNameMatch[1] : "test_inconnu";
            
            // Utilisation de \w pour capturer sans erreur les tirets et les underscores (ex: EXG-..._1)
            let matches = funcBlock.match(/EXG-[\w-]+/gi) || [];
            let uniqueExgs = [...new Set(matches.map(id => id.trim()))];
            
            // Filtrer pour voir s'il y a des EXG valides reconnus dans le coffre
            let attachedExgs = uniqueExgs.filter(id => validExgs.has(id));
            
            if (attachedExgs.length === 0) {
                // Vérifier si l'ID est au moins présent globalement dans le fichier
                let fileMatches = content.match(/EXG-[\w-]+/gi) || [];
                let fileHasExg = fileMatches.some(id => validExgs.has(id.trim()));
                
                if (!fileHasExg) {
                    rows.push([
                        `[[${file.path}|${file.name}]]`,
                        funcName,
                        "❌ Aucun EXG valide trouvé (Orphelin)"
                    ]);
                } else {
                    rows.push([
                        `[[${file.path}|${file.name}]]`,
                        funcName,
                        "⚠️ Présent dans le fichier mais absent de la fonction"
                    ]);
                }
            }
        }
    }

    // 3. Affichage du résultat sous forme de tableau
    if (rows.length === 0) {
        dv.paragraph("🎉 **Parfait !** Tous les tests sont correctement rattachés à une exigence valide.");
    } else {
        dv.paragraph(`⚠️ **${rows.length} test(s) détecté(s) sans rattachement fonctionnel explicite :**`);
        dv.table(
            ["Fichier de Test", "Fonction de Test", "Statut"],
            rows
        );
    }
})();

```



---
---
Objet : vue consolidée de traçabilité P8 — chaque exigence (EXG-*) tracée jusqu'à son implémentation (fichier · ligne), son test et sa section de conception. Convention : le code porte l'UID complet en commentaire au point d'application. **Généré dynamiquement** — toute dérive spec/code/test apparaît ici sans maintenance manuelle.

```dataviewjs
(async () => {
    // ── Table manuelle : sections de conception canvas (le seul ancrage non scannable)
    const CANVAS_SECTIONS = {
        "EXG-MET-P8-DEM_1":  "§34.2, §36.2",
        "EXG-MET-P8-DEM_2":  "§34.2, §36.1",
        "EXG-MET-P8-DEM_3":  "§34.1, §34.2",
        "EXG-MET-P8-DEM_4a": "§36.1, §36.2",
        "EXG-MET-P8-DEM_4b": "§34.2, §36.1, design §37.2",
        "EXG-MET-P8-DEM_4c": "§34.2",
        "EXG-MET-P8-DEM_4d": "§36.1, §36.2",
        "EXG-MET-P8-DEM_4e": "§36.2, §36.4",
        "EXG-MET-P8-DEM_5":  "§34.1",
        "EXG-MET-P8-DEM_6":  "§34.1",
        "EXG-MET-P8-DEM_7":  "§34.2 (découpage v2)",
        "EXG-MET-P8-RES_1":  "§34.2, §36.1",
        "EXG-FWK-P8-AGE_1":  "§34.2",
        "EXG-FWK-P8-AGE_2":  "§34.2, §36.1, §36.2",
        "EXG-FWK-P1-GOU_22":"§25 (seeds), §34.2",
        "EXG-FWK-P1-GOU_11":"§36.2, §36.4",
        "EXG-FWK-P1-GOU_13":"§36.2, §36.4"
    };

    // ── 1. Registre : exigences des specs P8 (+ P1 invoquées par P8)
    const specPages = dv.pages().where(p =>
        p.type === "spec" && p.exigences &&
        (String(p.phase_code).includes("P8")  | p.phase_code === undefined ||
         /P8|demonstrateur/i.test(p.reference || "")));
    const reg = {};  // uid -> {titre, spec, domaine}
    for (const page of specPages)
        for (const ex of page.exigences || []) {
            const id = (ex.uid || ex.id || "").trim();
            if (id && /-P8-|GOU_/.test(id))
                reg[id] = { titre: ex.titre || ex.intitule || "—",
                            spec: `[[${page.file.path}|${page.reference || page.file.name}]]`,
                            domaine: ex.domaine || "—" };
        }

    // ── 2. Scan CODE : chaque annotation EXG-* avec fichier + ligne + contexte
    const codeFiles = app.vault.getFiles().filter(f =>
        f.path.startsWith("03-Application/") &&
        /\.(py|js|html|css)$/.test(f.path) &&
        !f.path.includes("/Test/") && !f.path.includes("__pycache__"));
    const impl = {};   // uid -> [ "file\:Lxx (ctx)" ]
    for (const f of codeFiles) {
        const lines = (await app.vault.read(f)).split("\n");
        lines.forEach((line, i) => {
            for (const m of line.matchAll(/EXG-[\w]+(?:-[\w]+)*/g)) {
                const uid = m[0];
                (impl[uid] = impl[uid] || []).push(
                    `[[${f.path}|${f.name}]]:L${i + 1}`);
            }
        });
    }

    // ── 3. Scan TESTS : uid -> [ fichier(s) ]
    const testFiles = app.vault.getFiles().filter(f =>
        f.path.startsWith("03-Application/Test/") && f.path.endsWith(".py"));
    const tests = {};
    for (const f of testFiles) {
        const content = await app.vault.read(f);
        const blocks = content.split(/(?=def test_)/);
        for (const blk of blocks) {
            const fn = blk.match(/def\s+(test_[\w]+)/);
            if (!fn) continue;
            for (const m of blk.matchAll(/EXG-[\w]+(?:-[\w]+)*/g))
                (tests[m[0]] = tests[m[0]] || []).push(
                    `[[${f.path}|${fn[1]}]]`);
        }
    }
    for (const k in tests) tests[k] = [...new Set(tests[k])];

    // ── 4. Fusion : toutes les exigences P8, ancrage par ancrage
    const allUids = [...new Set([...Object.keys(reg),
        ...Object.keys(impl), ...Object.keys(tests)])]
        .filter(id => /-P8-|GOU_/.test(id)).sort();

    const rows = allUids.map(id => [
        reg[id] ? reg[id].spec : "⚠️ **ABSENT DE LA SPEC**",
        id,
        reg[id] ? reg[id].titre : "—",
        impl[id] ? impl[id].join("<br>") : "— (voir recette visuelle/inspection)",
        tests[id] ? tests[id].join("<br>") : "⚠️ non couvert",
        CANVAS_SECTIONS[id] || "—"
    ]);

    dv.table(["Spécification", "Exigence", "Intitulé",
              "Implémentation (fichier · ligne)", "Test pytest", "Section canvas"],
             rows);

    // ── 5. KPI de dérive
    const noSpec = allUids.filter(id => !reg[id]);
    const noCode = allUids.filter(id => reg[id] && !impl[id] && !tests[id]);
    const noTest = allUids.filter(id => reg[id] && !tests[id]);
    dv.paragraph(
        `> [!info] KPI traçabilité P8 — ${allUids.length} exigences<br>` +
        (noSpec.length  ? `⚠️ Sans spec : ${noSpec.join(", ")}<br>`  : "✅ Toutes déclarées en spec<br>") +
        (noTest.length  ? `⚠️ Sans test : ${noTest.join(", ")}<br>`  : "✅ Toutes testées (ou recette visuelle)<br>") +
        (noCode.length  ? `⚠️ Sans ancrage code : ${noCode.join(", ")}` : "✅ Toutes ancrées dans le code"));
})();
```

**Règle de maintenance (inchangée, pérennisée)** : cette vue est régénérée à l'ouverture — nulle copie manuelle à mettre à jour. Toute nouvelle exigence apparaît dès qu'elle est déclarée en spec **et** annotée `EXG-*` dans le code ; toute évolution de livrable canonique met seulement à jour la table `CANVAS_SECTIONS` en tête de script. Les exigences sans test automatisable portent la mention « recette visuelle » ou « inspection » dans la spec — elles restent traçables.




---
---

### 6. Cartographie des Canvas de Conception (lecture humaine)


```dataviewjs
(async () => {
    // ── 0. Configuration : dossiers des canvas de design (à ajuster)
    const CANVAS_FOLDERS = ["00-Projet/phases/", "00-Projet/canvases/"];

    // ── 1. Registre : uid -> {titre, spec, design, domaine}
    const specPages = dv.pages().where(p => p.type === "spec" && p.exigences);
    const reg = {};
    for (const page of specPages)
        for (const ex of page.exigences  | []) {
            const id = (ex.uid || ex.id || "").trim();
            if (id) reg[id] = {
                titre: ex.titre || ex.intitule || "—",
                spec: `[[${page.file.path}|${page.reference || page.file.name}]]`,
                design: (ex.design || "").trim(),
                domaine: ex.domaine || "—"
            };
        }

    // ── 2. Scan CODE et TESTS (pour la colonne couverture) — version corrigée
    const scan = async (pred) => {
        const map = {};  // uid -> Set(files)
        const files = app.vault.getFiles().filter(pred);
        for (const f of files) {
            const content = await app.vault.read(f);
            for (const m of content.matchAll(/EXG-[\w]+(?:-[\w]+)*/g)) {
                (map[m[0]] = map[m[0]] || new Set()).add(f.name);
            }
        }
        return map;
    };
    const impl = await scan(f => f.path.startsWith("03-Application/") &&
        /\.(py|js|html|css)$/.test(f.path) &&
        !f.path.includes("/Test/") && !f.path.includes("__pycache__"));
    const tests = await scan(f => f.path.startsWith("03-Application/Test/"));

    // ── 3. Index inverse : section (§xx) -> [uid]
    const sections = {};
    for (const [uid, info] of Object.entries(reg)) {
        if (!info.design) continue;
        for (const sec of info.design.match(/§[\d.]+/g) || []) {
            (sections[sec] = sections[sec] || []).push(uid);
        }
    }

    // ── 4. Lecture des canvas : titres de sections réels
    const canvasFiles = app.vault.getFiles().filter(f =>
        CANVAS_FOLDERS.some(d => f.path.startsWith(d)) && f.extension === "md");
    const sectionTitles = {};  // "§34.2" -> {titre, canvas}
    for (const f of canvasFiles) {
        const lines = (await app.vault.read(f)).split("\n");
        for (let i = 0; i < lines.length; i++) {
            const m = lines[i].match(/^#{1,4}\s*(?:§)?\s*(\d+(?:\.\d+)*)\s*[—–-]?\s*(.*)/);
            if (m) {
                const sec = `§${m[1]}`;
                if (!sectionTitles[sec])
                    sectionTitles[sec] = {
                        titre: m[2].trim() || "(sans titre)",
                        canvas: `[[${f.path}|${f.name}]]`
                    };
            }
        }
    }

    // ── 5. Rendu : un tableau par canvas
    const byCanvas = {};
    const allSecs = new Set([...Object.keys(sections), ...Object.keys(sectionTitles)]);
    for (const sec of allSecs) {
        const info = sectionTitles[sec] ||
            { titre: "⚠️ citée en spec mais introuvable dans les canvas", canvas: "—" };
        (byCanvas[info.canvas] = byCanvas[info.canvas] || []).push({ sec, info });
    }

    for (const [canvas, secs] of Object.entries(byCanvas)) {
        dv.header(3, canvas.replace(/\[\[|\]\]|.*\|/g, ""));
        const rows = secs
            .sort((a, b) => a.sec.localeCompare(b.sec, "fr", { numeric: true }))
            .map(({ sec, info }) => {
                const uids = sections[sec] || [];
                const exgCell = uids.length
                    ? uids.map(u => reg[u]
                        ? `${u} — ${reg[u].titre}`
                        : `${u} ⚠️ (hors registre)`).join("<br>")
                    : "—";
                const specCell = [...new Set(
                    uids.map(u => reg[u] && reg[u].spec).filter(Boolean))].join("<br>") || "—";
                const codeOk = uids.some(u => impl[u]);
                const testOk = uids.length > 0 && uids.every(u => tests[u]);
                return [sec, info.titre, exgCell, specCell,
                        codeOk ? "✅" : "—",
                        testOk ? "✅" : "❌"];
            });
        dv.table(["Section", "Titre", "Exigences ancrées", "Spec", "Code", "Test"], rows);
    }

    // ── 6. KPI d'alerte
    const ghostSecs = Object.keys(sections).filter(s => !sectionTitles[s]);
    if (ghostSecs.length)
        dv.paragraph(`⚠️ **Sections citées en spec mais introuvables :** ${ghostSecs.join(", ")} — à recalage (C6).`);
    const orphanSecs = Object.keys(sectionTitles).filter(s => !sections[s]);
    if (orphanSecs.length)
        dv.paragraph(`ℹ️ **Sections sans exigence ancrée :** ${orphanSecs.length} (design sans contrainte — normal pour les sections méthodo).`);
})();
```


```dataviewjs
(async () => {
    const f = app.vault.getAbstractFileByPath("00-Projet/phases/Phase8/Phase8_content.md");
    if (!f) { dv.paragraph("❌ fichier introuvable"); return; }
    const lines = (await app.vault.read(f)).split("\n");
    const hits = [];
    lines.forEach((line, i) => {
        if (/^#{1,4}\s/.test(line)) {           // tous les headings
            const m = line.match(/^#{1,4}\s*(?:§)?\s*(\d+(?:\.\d+)*)\s*[—–-]?\s*(.*)/);
            hits.push(`${m ? "✅" : "❌"} L${i+1} : ${line.slice(0, 80)}`);
        }
    });
    dv.paragraph(hits.length
        ? `<br>${hits.join("<br>")}`
        : "❌ Aucun heading trouvé dans ce fichier.");
})();
```
