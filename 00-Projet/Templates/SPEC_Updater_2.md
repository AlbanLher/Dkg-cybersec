<%*
// 1. Table de correspondance officielle des Domaines
const domainMapping = {
    "CT": "Cyber Threat Intelligence",
    "HW": "Hardware & Infrastructures",
    "IN": "Inférence & Graph Analytics",
    "OR": "Organisation & Processus",
    "QU": "Qualité & Conformité",
    "SE": "Sécurité & Isolation",
    "SH": "SHACL Shapes",
    "TB": "TBox & Ontologies Master",
    "TEC": "Technique & Core Framework"
};

// 2. Lecture du contenu du fichier Markdown actuel
const currentContent = await app.vault.read(tp.config.target_file);
const currentLines = currentContent.split("\n");
let extractedExigences = [];

// 3. Parsing du tableau Markdown pour extraire les exigences, domaines et statuts
for (let line of currentLines) {
    if (line.includes("---") || line.toLowerCase().includes("id") || line.toLowerCase().includes("uid")) continue;
    
    if (line.trim().startsWith("|") && line.includes("EXG-")) {
        let cleanLine = line.replace(/<br\s*\/?>/gi, " ").replace(/<[^>]*>/g, "").replace(/\*\*/g, "");
        let cols = cleanLine.split("|").map(c => c.trim()).filter(Boolean);
        
        if (cols.length >= 6) {
            let idVal = cols[0].startsWith("EXG-") ? cols[0] : (cols[1] || "EXG-OR-01");
            
            // Extraction ou déduction du domaine
            let rawDomaine = cols.find(c => domainMapping[c]) || "OR";
            
            // Extraction ou déduction du statut Core / Non-Core
            let rawCoreCol = cols.find(c => c.toUpperCase().includes("CORE") || c.toUpperCase().includes("NON-CORE"));
            let isCore = true;
            if (rawCoreCol) {
                isCore = !rawCoreCol.toUpperCase().includes("NON");
            } else {
                isCore = idVal.includes("-P1-") || idVal.includes("GOU") || idVal.includes("ABO");
            }

            extractedExigences.push({
                id: idVal,
                domaine: rawDomaine,
                domaine_nom: domainMapping[rawDomaine] || "Organisation & Processus",
                titre: cols[4] || "Titre de l'exigence",
                critere: cols[5] || "Critère formel vérifiable.",
                test: cols[6] || "PyTest / SHACL",
                core: isCore
            });
        }
    }
}

// 4. Mise à jour exclusive du Frontmatter YAML
app.fileManager.processFrontMatter(tp.config.target_file, (fm) => {
    if (extractedExigences.length > 0) {
        fm["exigences"] = extractedExigences;
    }
});
-%>