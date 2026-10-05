<%*
// 1. Lecture du contenu du fichier actuel
const currentContent = await app.vault.read(tp.config.target_file);
const currentLines = currentContent.split("\n");
let extractedExigences = [];

// 2. Parsing du tableau Markdown des exigences dans le corps de la note
for (let line of currentLines) {
    // Ignorer les lignes d'en-tête ou de séparation du tableau
    if (line.includes("---") || line.toLowerCase().includes("identifiant") || line.toLowerCase().includes("uid")) continue;
    
    if (line.trim().startsWith("|") && line.includes("EXG-")) {
        let cleanLine = line.replace(/<br\s*\/?>/gi, " ").replace(/<[^>]*>/g, "").replace(/\*\*/g, "");
        let cols = cleanLine.split("|").map(c => c.trim()).filter(Boolean);
        
        if (cols.length >= 5) {
            let exgList = cols.filter(c => c.startsWith("EXG-"));
            let finalId = cols[0].startsWith("EXG-") ? cols[0] : (exgList[0] || "EXG-OR-01");
            let finalUid = cols[1] && cols[1].startsWith("EXG-") ? cols[1] : (exgList[1] || finalId);

            extractedExigences.push({
                id: finalId,
                uid: finalUid,
                domaine: cols[2] || "OR",
                titre: cols[3] || "Titre de l'exigence",
                description: cols[4] || "Description formelle.",
                test: cols[5] || "PyTest / SHACL"
            });
        }
    }
}

// 3. Mise à jour exclusive de la clé "exigences" dans le Frontmatter YAML
app.fileManager.processFrontMatter(tp.config.target_file, (fm) => {
    if (extractedExigences.length > 0) {
        fm["exigences"] = extractedExigences;
    }
});
-%>