<%*
// 1. Récupération sécurisée de la Roadmap
let roadmapFile = app.vault.getAbstractFileByPath("00-Projet/Roadmap_Suivi-Avancement.md");
if (!roadmapFile) {
    roadmapFile = tp.file.find_tfile("Roadmap_Suivi-Avancement.md");
}

let selected = null;

if (!roadmapFile) {
    new Notice("❌ Erreur : Fichier Roadmap_Suivi-Avancement.md introuvable !");
} else {
    const content = await app.vault.read(roadmapFile);
    const lines = content.split("\n");
    
    let currentVague = "V1";
    let phaseOptions = [];
    let inSection2 = false;

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];
        
        if (line.includes("## 2")) {
            inSection2 = true;
            continue;
        }
        if (inSection2 && line.includes("## 3")) {
            break;
        }

        if (inSection2 && line.startsWith("|")) {
            let cleanLine = line.replace(/<br\s*\/?>/gi, " ")
                                  .replace(/<[^>]*>/g, "")
                                  .replace(/\*\*/g, "");
            
            let cols = cleanLine.split("|").map(c => c.trim());

            if (cols.length >= 5 && cols[2] && cols[2].match(/^P\d+$/i)) {
                if (cols[1] && cols[1].match(/^V\d+$/i)) {
                    currentVague = cols[1];
                }

                let phaseCode = cols[2];
                let phaseNom = cols[3];
                let phaseStatut = cols[5] || "⚪ Planifié"; 
                let phaseNum = phaseCode.replace(/[^0-9]/g, "").padStart(2, "0");

                phaseOptions.push({
                    display: phaseCode + " | " + phaseNom + " (" + currentVague + " - " + phaseStatut + ")",
                    pCode: phaseCode,
                    pNum: phaseNum,
                    pNom: phaseNom,
                    pVague: currentVague,
                    pStatut: phaseStatut
                });
            }
        }
    }

    if (phaseOptions.length === 0) {
        new Notice("⚠️ Aucune phase trouvée dans le chapitre 2 de la Roadmap !");
    } else {
        selected = await tp.system.suggester(
            phaseOptions.map(o => o.display),
            phaseOptions
        );
    }
}

let pNum = selected ? selected.pNum : "00";
let pCode = selected ? selected.pCode : "P0";
let pNom = selected ? selected.pNom : "Nom de la Phase";
let pVague = selected ? selected.pVague : "V1";
let pStatut = selected ? selected.pStatut : "⚪ Planifié";
-%>
---
type: phase
phase_num: "<% pNum %>"
phase_code: "<% pCode %>"
phase_nom: "<% pNom %>"
vague: "<% pVague %>"
statut: "<% pStatut %>"
date_debut: <% tp.file.creation_date("YYYY-MM-DD") %>
date_cloture: 
---
# 📋 <% pCode %> : <% pNom %>

> **Rattachement** : <% pVague %>  
> **Statut Initial** : <% pStatut %>  
> **Date de création** : <% tp.file.creation_date("DD/MM/YYYY") %>  
> **Source de Vérité** : [[Roadmap_Suivi-Avancement]]

---

## 🎯 1. Objectifs & Périmètre
* **But principal** : [Description synthétique]
* **Livrables attendus** : [Composants logiciels, schémas ou documents]

---

## 🛠️ 2. Traçabilité des Livrables par Brique

### A. Spécification & Gouvernance (SPEC Framework)
* **Spécification associée** : `SPEC-<% pNum %>.md`

### B. Données & Ontologies (Data / Graph RDF)
* **Artefacts Master** : `Master_Transversal/`
* **Artefacts Snapshot** : `Snapshot_Phase_<% pNum %>/`

### C. Scripts & Outillage (Automation & CI/CD)
* **Générateur** : `generate_phase<% pNum %>.py`
* **Tests Qualité** : `test_phase<% pNum %>_quality.py`