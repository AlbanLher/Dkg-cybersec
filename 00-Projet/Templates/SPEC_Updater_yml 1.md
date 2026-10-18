<%*
const domainMapping = {
    "CT": "Cyber Threat Intelligence",
    "HW": "Hardware & Infrastructures",
    "IN": "Inférence & Graph Analytics",
    "OR": "Organisation & Processus",
    "QU": "Qualité & Conformité",
    "SE": "Sécurité & Isolation",
    "SH": "SHACL Shapes",
    "TB": "TBox & Ontologies Master",
    "TEC": "Technique & Core Framework",
    "MET": "Méthodologie & Agents"
};

const currentContent = await app.vault.read(tp.config.target_file);
const currentLines = currentContent.split("\n");

let extractedExigences = [];

for (let line of currentLines) {
    // Ignore les en-têtes de tableaux et les séparateurs Markdown
    if (line.includes("---") || line.toLowerCase().includes("identifiant") || line.toLowerCase().includes("intitulé") || line.includes("---")) continue;
    
    // Vérifie si la ligne est une ligne de tableau contenant un ID d'exigence
    if (line.trim().startsWith("|") && line.includes("EXG-")) {
        let cleanLine = line.replace(/<br\s*\/?>/gi, " ").replace(/<[^>]*>/g, "").replace(/\*\*/g, "").replace(/`/g, "");
        let cols = cleanLine.split("|").map(c => c.trim()).filter(Boolean);
        
        if (cols.length >= 4) {
            // 1. Extraction de l'UID (id)
            let idVal = cols.find(c => c.startsWith("EXG-")) || cols[0];
            
            // 2. Extraction du domaine
            let rawDomaine = cols.find(c => domainMapping[c]) || "MET";
            
            // 3. Détermination du statut Core/Non-Core (true/false)
            let coreCol = cols.find(c => c.toLowerCase().includes("core") || c.toLowerCase().includes("non-core"));
            let isCore = coreCol ? !coreCol.toLowerCase().includes("non-core") : true;

            // 4. Extraction dynamique des textes restants (Intitulé, Description, Mode de validation)
            let textCols = cols.filter(c => !c.startsWith("EXG-") && !domainMapping[c] && c.toLowerCase() !== "core" && c.toLowerCase() !== "non-core" && c.toLowerCase() !== "true" && c.toLowerCase() !== "false");
            
            let titreVal = textCols.length > 0 ? textCols[0] : "Intitulé de l'exigence";
            let critereVal = textCols.length > 1 ? textCols[1] : "Description de l'exigence.";
            let testVal = textCols.length > 2 ? textCols[2] : "PyTest";

            // Construction de l'objet exigence avec les clés strictes requises
            extractedExigences.push({
                id: idVal,
                domaine: rawDomaine,
                core: isCore,
                titre: titreVal,
                critere: critereVal,
                test: testVal
            });
        }
    }
}

// Mise à jour ciblée du frontmatter YAML du document
app.fileManager.processFrontMatter(tp.config.target_file, (fm) => {
    if (extractedExigences.length > 0) {
        fm["exigences"] = extractedExigences;
    }
});
-%>