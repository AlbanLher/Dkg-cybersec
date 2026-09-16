# 🗺️ Master Index des Spécifications & Matrice d'Exigences

## 1. Cartographie des Spécifications
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

## 1.bis
```dataviewjs
let pages = dv.pages('"01-Principes_Spécifications"').where(p => p.type === "spec");
let rows = ["Fichier_Source\tDomaine\tID_Exigence\tTitre_Court"];

for (let page of pages) {
    let file = page.file.name;
    
    let processEx = (dom, ex) => {
        let id = ex.id || "SANS_ID";
        let titre = ex.titre || ex.intitule || "Sans titre";
        rows.push(`${file}\t${dom}\t${id}\t${titre}`);
    };

    if (page.exigences_par_domaine) {
        for (let dom in page.exigences_par_domaine) {
            let list = page.exigences_par_domaine[dom];
            if (Array.isArray(list)) {
                list.forEach(ex => processEx(dom, ex));
            }
        }
    } else if (Array.isArray(page.exigences)) {
        page.exigences.forEach(ex => processEx(page.domaine || "General", ex));
    }
}

dv.header(4, "🗺️ Cartographie des Spécifications (Format TSV)");
dv.paragraph("```tsv\n" + rows.join("\n") + "\n```");
```




## 2. Matrice Consolidée Traçabilité Exigences (`EXG-`)
```dataview
TABLE WITHOUT ID
    ex.id AS "Réf. Exigence",
    phase_code AS "Phase",
    ex.domaine AS "Domaine",
    ex.titre AS "Intitulé Exigence",
    ex.description AS "Critère d'Acceptation",
    ex.test AS "Mode de Test",
    statut AS "Statut Phase"
FROM "01-Principes_Spécifications"
WHERE type = "spec" AND exigences
FLATTEN exigences AS ex
SORT ex.id ASC
```

## 3. 
```dataview
TABLE WITHOUT ID
    ex.id AS "Réf. Exigence",
    domaine AS "Domaine",
    ex.titre AS "Intitulé Exigence",
    ex.desc AS "Critère d'Acceptation",
    ex.val AS "Mode de Test"
FROM "01-Principes_Spécifications"
WHERE type = "spec" AND exigences_par_domaine
FLATTEN objectPairs(exigences_par_domaine) AS p
FLATTEN p.key AS domaine
FLATTEN p.value AS ex
SORT ex.id ASC
```


## 4. 

```dataviewjs
let pages = dv.pages('"01-Principes_Spécifications"').where(p => p.type === "spec");
let rows = [];

for (let page of pages) {
    // Cas 1 : Structure sous 'exigences_par_domaine'
    if (page.exigences_par_domaine) {
        let dict = page.exigences_par_domaine;
        for (let key of Object.keys(dict)) {
            let list = dict[key];
            if (Array.isArray(list)) {
                for (let ex of list) {
                    rows.push([
                        ex.id || "-",
                        ex.domaine || key,
                        ex.titre || ex.intitule || "-",
                        ex.desc || ex.description || "-",
                        ex.val || ex.test || "-"
                    ]);
                }
            }
        }
    }
    // Cas 2 : Structure sous 'exigences' (liste à plat)
    else if (page.exigences && Array.isArray(page.exigences)) {
        for (let ex of page.exigences) {
            rows.push([
                ex.id || "-",
                ex.domaine || "-",
                ex.titre || ex.intitule || "-",
                ex.desc || ex.description || "-",
                ex.val || ex.test || "-"
            ]);
        }
    }
}

if (rows.length === 0) {
    dv.paragraph("⚠️ **Aucune exigence trouvée.** Vérifiez que vos fichiers dans `01-Principes_Spécifications` possèdent bien `type: spec` dans leur frontmatter.");
} else {
    rows.sort((a, b) => (a[0] || "").localeCompare(b[0] || ""));
    dv.table(
        ["Réf. Exigence", "Domaine", "Intitulé Exigence", "Critère d'Acceptation", "Mode de Test"],
        rows
    );
}
```


```dataviewjs
let pages = dv.pages('"01-Principes_Spécifications"').where(p => p.type === "spec");
let lines = ["ID\tDomaine\tTitre\tCritère\tTest"];

for (let page of pages) {
    // Cas 1 : Dictionnaire par domaine
    if (page.exigences_par_domaine) {
        let dict = page.exigences_par_domaine;
        for (let dom of Object.keys(dict)) {
            let list = dict[dom];
            if (Array.isArray(list)) {
                for (let ex of list) {
                    let id = ex.id || "-";
                    let titre = ex.titre || ex.intitule || "-";
                    let desc = ex.desc || ex.description || "-";
                    let val = ex.val || ex.test || "-";
                    lines.push(`${id}\t${dom}\t${titre}\t${desc}\t${val}`);
                }
            }
        }
    } 
    // Cas 2 : Liste simple d'exigences
    else if (page.exigences && Array.isArray(page.exigences)) {
        for (let ex of page.exigences) {
            let id = ex.id || "-";
            let dom = ex.domaine || "-";
            let titre = ex.titre || ex.intitule || "-";
            let desc = ex.desc || ex.description || "-";
            let val = ex.val || ex.test || "-";
            lines.push(`${id}\t${dom}\t${titre}\t${desc}\t${val}`);
        }
    }
}

// Rendu en bloc de code texte brut facilement copiable
dv.header(4, "📋 Master Index Compact (Format TSV pour LLM)");
dv.paragraph("```tsv\n" + lines.join("\n") + "\n```");
```