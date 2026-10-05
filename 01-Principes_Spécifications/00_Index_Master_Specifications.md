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


### 2. Matrice Consolidée Traçabilité Exigences (`EXG-`)
```dataviewjs
let pages = dv.pages('"01-Principes_Spécifications"').where(p => p.type === "spec");
let rows = [];

for (let page of pages) {
    // Récupération de la référence de la spec (depuis le frontmatter 'reference' ou à défaut le nom du fichier)
    let specRef = page.reference || page.file.name;

    // Cas 1 : Structure sous 'exigences_par_domaine'
    if (page.exigences_par_domaine) {
        let dict = page.exigences_par_domaine;
        for (let key of Object.keys(dict)) {
            let list = dict[key];
            if (Array.isArray(list)) {
                for (let ex of list) {
                    rows.push([
                        specRef,
                        ex.uid || ex.id || "-",
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
                specRef,
                ex.uid || ex.id || "-",
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
    // Tri par référence de spec puis par ID/UID d'exigence
    rows.sort((a, b) => (a[0] + a[1]).localeCompare(b[0] + b[1]));
    
    dv.table(
        ["Spécification Source", "ID / UID Exigence", "Domaine", "Intitulé Exigence", "Critère d'Acceptation", "Mode de Test"],
        rows
    );
}
```



```dataviewjs
let pages = dv.pages('"01-Principes_Spécifications"').where(p => p.type === "spec");
let rows = [];

for (let page of pages) {
    // Cas 1 : Structure sous 'exigences_par_domaine' (dictionnaire)
    if (page.exigences_par_domaine) {
        let dict = page.exigences_par_domaine;
        for (let key of Object.keys(dict)) {
            let list = dict[key];
            if (Array.isArray(list)) {
                for (let ex of list) {
                    rows.push([
                        ex.uid || ex.id || "-",
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
    // Cas 2 : Structure sous 'exigences' (liste à plat présente dans votre YAML)
    else if (page.exigences && Array.isArray(page.exigences)) {
        for (let ex of page.exigences) {
            rows.push([
                ex.uid || ex.id || "-",   // Si 'uid' n'est pas dans le YAML, utilise 'id'
                ex.id || "-",
                ex.domaine || "-",
                ex.titre || ex.intitule || "-",
                ex.description || ex.desc || "-",
                ex.test || ex.val || "-"
            ]);
        }
    }
}

if (rows.length === 0) {
    dv.paragraph("⚠️ **Aucune exigence trouvée.** Vérifiez que vos fichiers dans `01-Principes_Spécifications` possèdent bien `type: spec` dans leur frontmatter.");
} else {
    // Tri principal par l'identifiant de la première colonne
    rows.sort((a, b) => (a[0] || "").localeCompare(b[0] || ""));
    
    dv.table(
        ["UID", "ID", "Domaine", "Intitulé Exigence", "Critère d'Acceptation", "Mode de Test"],
        rows
    );
}
```
### 5. - Matrice Consolidée Traçabilité Exigences décomposées par App_Layer
```dataviewjs
let pages = dv.pages('"01-Principes_Spécifications"').where(p => p.type === "spec");

// En-têtes complets correspondant à votre structure d'exigence souhaitée
let header = "ID\tDomaine\tTitre\tCritère\tTest";
let layers = {
    "Core": [header],
    "Agent": [header],
    "Interface": [header]
};

function getAppLayer(domaine) {
    if (!domaine) return "Interface";
    let d = String(domaine).trim().toUpperCase();
    
    // Core : Modèle sémantique, Ontologie, Schémas, Formes
    if (["TB", "SH", "ONT"].includes(d)) return "Core";
    
    // Agent : Inférence, Analyse, CTI, Traitement de texte, Intelligence/MITM
    if (["IN", "CT", "IA"].includes(d)) return "Agent";
    
    // Interface : Organisation, Sécurité, Qualité, Technique, Hardware, etc.
    return "Interface";
}

for (let page of pages) {
    let pageDomaine = page.domaine || page.domain || "General";
    
    let processEx = (dom, ex) => {
        let id = ex.uid || "-";
        let titre = ex.titre || ex.intitule || "-";
        let desc = ex.desc || ex.description || "-";
        let val = ex.val || ex.test || "-";
        
        // Nettoyage des retours à la ligne potentiels dans les descriptions pour ne pas casser le format TSV
        desc = String(desc).replace(/(\r\n|\n|\r)/gm, " ");
        val = String(val).replace(/(\r\n|\n|\r)/gm, " ");

        // Détermination du domaine effectif et de la couche
        let effectiveDom = dom || pageDomaine;
        if (ex.id) {
            let match = ex.id.match(/^EXG-([A-Z]+)-/);
            if (match) effectiveDom = match[1];
        }
        
        let targetLayer = getAppLayer(effectiveDom);
        layers[targetLayer].push(`${id}\t${effectiveDom}\t${titre}\t${desc}\t${val}`);
    };

    if (page.exigences_par_domaine) {
        for (let dom in page.exigences_par_domaine) {
            let list = page.exigences_par_domaine[dom];
            if (Array.isArray(list)) {
                list.forEach(ex => processEx(dom, ex));
            }
        }
    } else if (Array.isArray(page.exigences)) {
        page.exigences.forEach(ex => processEx(pageDomaine, ex));
    }
}

// Génération dynamique des 3 blocs TSV d'exigences complètes
for (let layerName of ["Core", "Agent", "Interface"]) {
    dv.header(4, `📋 Matrice des Exigences — Couche : ${layerName} (Format TSV complet)`);
    if (layers[layerName].length > 1) {
        dv.paragraph("```tsv\n" + layers[layerName].join("\n") + "\n```");
    } else {
        dv.paragraph("_Aucune exigence pour cette couche._");
    }
}
```