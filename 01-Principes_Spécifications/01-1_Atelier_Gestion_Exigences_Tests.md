
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
