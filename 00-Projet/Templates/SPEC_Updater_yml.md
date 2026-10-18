<%*
// ── SPEC_Update_yml (v2) : régénère le frontmatter `exigences` depuis la
// table §4 du corps. SSOT : le corps fait foi. Convention GOU_24 : UID
// complets, MAJUSCULES. Ne jamais éditer le YAML à la main.

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
let warnings = [];
let seenUids = new Set();

for (let line of currentLines) {
    // Ignore séparateurs de tableaux et en-têtes
    if (/^\s*\|[\s:-]+\|\s*$/.test(line)) continue;
    if (line.toLowerCase().includes("identifiant") || line.toLowerCase().includes("intitulé")) continue;

    if (!line.trim().startsWith("|") || !line.includes("EXG-")) continue;

    // Nettoyage APRÈS split : chaque cellule est nettoyée individuellement
    let cols = line.split("|")
        .map(c => c.replace(/<br\s*\/?>/gi, " ")
                    .replace(/<[^>]*>/g, "")
                    .replace(/\*\*/g, "")
                    .replace(/`/g, "")
                    .trim())
        .filter(Boolean);

    if (cols.length < 4) continue;

    // 1. UID : première cellule commençant par EXG-, NORMALISÉE en MAJUSCULES
    let idVal = (cols.find(c => /^EXG-/i.test(c)) || "").toUpperCase().trim();
    if (!idVal) continue;

    // Unicité : doublon dans la table = alerte, on garde la 1re occurrence
    if (seenUids.has(idVal)) {
        warnings.push(`UID dupliqué dans la table : ${idVal}`);
        continue;
    }
    seenUids.add(idVal);

    // 2. Domaine : par position (3e cellule), fallback mapping, défaut OR visible
    let domCand = (cols[2] || "").toUpperCase().trim();
    let rawDomaine = domainMapping[domCand] ? domCand : null;
    if (!rawDomaine) {
        rawDomaine = cols.find(c => domainMapping[c.toUpperCase()])?.toUpperCase() || null;
    }
    if (!rawDomaine) {
        rawDomaine = "OR";
        warnings.push(`${idVal} : domaine non reconnu → OR par défaut (à corriger dans la table)`);
    }

    // 3. Core : colonne explicite sinon true par défaut
    let coreCol = cols.find(c => /^(non[-\s]?core|core)$/i.test(c));
    let isCore = coreCol ? !/non/i.test(coreCol) : true;

    // 4. Textes : cellules restantes dans l'ordre (intitulé, critère, test)
    let textCols = cols.filter(c =>
        !/^EXG-/i.test(c) &&
        !domainMapping[c.toUpperCase()] &&
        !/^(non[-\s]?core|core)$/i.test(c));

    let titreVal  = textCols.length > 0 ? textCols[0] : "Intitulé à compléter";
    let critereVal = textCols.length > 1 ? textCols[1] : "Critère à compléter.";
    let testVal   = textCols.length > 2 ? textCols[2] : "PyTest";

    extractedExigences.push({
        id: idVal,
        domaine: rawDomaine,
        core: isCore,
        titre: titreVal,
        critere: critereVal,
        test: testVal
    });
}

// Garde-fou : n'écrase JAMAIS un YAML existant par un résultat tronqué
const fmNow = app.metadataCache.getFileCache(tp.config.target_file)?.frontmatter;
const existingCount = Array.isArray(fmNow?.exigences) ? fmNow.exigences.length : 0;

if (extractedExigences.length === 0) {
    const msg = `⚠️ AUCUNE exigence détectée dans la table §4 — YAML INTACT (${existingCount} exigences conservées). Vérifier le format des lignes (| … EXG-… | …).`;
    new Notice(msg);
    tR += `\n> [!warning] ${msg}\n`;
} else {
    app.fileManager.processFrontMatter(tp.config.target_file, (fm) => {
        fm["exigences"] = extractedExigences;
    });
    let msg = `✅ YAML régénéré : ${extractedExigences.length} exigences (avant : ${existingCount}).`;
    if (warnings.length) msg += `\n⚠️ ${warnings.length} alerte(s) :\n- ${warnings.join("\n- ")}`;
    if (extractedExigences.length < existingCount)
        msg += `\n⚠️ ATTENTION : le nouveau YAML contient MOINS d'exigences que l'ancien (${extractedExigences.length} < ${existingCount}) — vérifier que toutes les lignes de la table sont bien parsées.`;
    new Notice(msg);
    tR += `\n> [!info] ${msg}\n`;
}
-%>