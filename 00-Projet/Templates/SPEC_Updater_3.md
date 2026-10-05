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
    if (line.includes("---") || line.toLowerCase().includes("identifiant") || line.toLowerCase().includes("intitulé")) continue;
    
    if (line.trim().startsWith("|") && line.includes("EXG-")) {
        let cleanLine = line.replace(/<br\s*\/?>/gi, " ").replace(/<[^>]*>/g, "").replace(/\*\*/g, "").replace(/`/g, "");
        let cols = cleanLine.split("|").map(c => c.trim()).filter(Boolean);
        
        // Adaptation selon le nombre de colonnes (avec ou sans colonne UID séparée)
        if (cols.length >= 4) {
            let idVal = cols.find(c => c.startsWith("EXG-")) || cols[0];
            let rawDomaine = cols.find(c => domainMapping[c]) || "MET";
            let rawPhase = "P7"; // Forcé ou extrait de l'ID
            if (idVal.match(/-P(\d+)-/)) {
                rawPhase = "P" + idVal.match(/-P(\d+)-/)[1];
            }
            
            // Récupération intelligente du titre et du critère selon la position
            let titreVal = cols.length >= 5 ? cols[4] : "Titre de l'exigence";
            let critereVal = cols.length >= 6 ? cols[5] : "Critère formel vérifiable.";
            let testVal = cols.length >= 7 ? cols[6] : "PyTest";

            extractedExigences.push({
                id: idVal,
                domaine: rawDomaine,
                core: true,
                phase: rawPhase,
                spec_source: "SPC-MET-P07-assistant_soc_foyer_01",
                titre: titreVal,
                critere: critereVal,
                test: testVal
            });
        }
    }
}

app.fileManager.processFrontMatter(tp.config.target_file, (fm) => {
    if (extractedExigences.length > 0) {
        fm["exigences"] = extractedExigences;
    }
});
-%>