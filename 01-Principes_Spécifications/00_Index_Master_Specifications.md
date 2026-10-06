# 🗺️ Master Index des Spécifications & Matrice d'Exigences

## Tableau Humain
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


### 3. Matrice Consolidée par Couche Applicative (V-Model / App_Layer)

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



```dataviewjs
(async () => {
    // 1. Récupération des fichiers de test Python dans le coffre (si présents)
    let pyFiles = app.vault.getFiles().filter(f => f.path.endsWith(".py"));
    let testMapping = {};

    for (let file of pyFiles) {
        let content = await app.vault.read(file);
        // Regex élargie pour capturer tous les formats d'ID d'exigences (ex: EXG-FWK-P1-T-R_1, EXG-TB-01, etc.)
        let matches = content.match(/EXG-[A-Z0-9\-_]+/g);
        if (matches) {
            let uniqueExgs = [...new Set(matches)];
            for (let exId of uniqueExgs) {
                if (!testMapping[exId]) testMapping[exId] = [];
                if (!testMapping[exId].includes(file.name)) {
                    testMapping[exId].push(file.name);
                }
            }
        }
    }

    // 2. Lecture des spécifications
    let pages = dv.pages('"01-Principes_Spécifications"').where(p => p.type === "spec");
    let rows = [];

    for (let page of pages) {
        let specRef = page.reference || page.file.name;
        // Création d'un lien Obsidian propre vers la spec source
        let specLink = `[[${page.file.path}|${specRef}]]`;

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

                // Recherche de la correspondance dans les tests
                let testedBy = testMapping[id] ? testMapping[id].join(", ") : "⚠️ Non couvert";

                rows.push([
                    specLink,
                    id,
                    domaine,
                    coreStatus,
                    titre,
                    testedBy
                ]);
            }
        }
    }

    if (rows.length === 0) {
        dv.paragraph("⚠️ **Aucune exigence trouvée.**");
    } else {
        rows.sort((a, b) => (a[0] + a[1]).localeCompare(b[0] + b[1]));
        
        dv.table(
            ["Spécification", "ID Exigence", "Domaine", "Core/Non-Core", "Intitulé", "Fichier(s) de Test Associé(s)"],
            rows
        );
    }
})();
```

