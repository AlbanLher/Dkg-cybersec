document.addEventListener("DOMContentLoaded", () => {
    // Éléments Onglets
    const tabAudit = document.getElementById("tab-btn-audit");
    const tabStress = document.getElementById("tab-btn-stress");
    const viewAudit = document.getElementById("view-audit");
    const viewStress = document.getElementById("view-stress");

    // Éléments Interactifs Audit
    const btnRun = document.getElementById("btn-run-audit");
    const btnApprove = document.getElementById("btn-hitm-approve");
    const btnReject = document.getElementById("btn-hitm-reject");
    const toggleHost = document.getElementById("toggle-host-mode");

    // Gestion de la Navigation par Onglets
    tabAudit.addEventListener("click", () => {
        viewAudit.classList.remove("hidden");
        viewStress.classList.add("hidden");
        tabAudit.className = "px-4 py-2 text-xs font-bold rounded-lg bg-amber-600 text-white shadow";
        tabStress.className = "px-4 py-2 text-xs font-bold rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition";
    });

    tabStress.addEventListener("click", () => {
        viewStress.classList.remove("hidden");
        viewAudit.classList.add("hidden");
        tabStress.className = "px-4 py-2 text-xs font-bold rounded-lg bg-indigo-600 text-white shadow";
        tabAudit.className = "px-4 py-2 text-xs font-bold rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition";
    });

    // 1. REINITIALISATION IMMEDIATE AU BASCULEMENT DU TOGGLE
    toggleHost.addEventListener("change", (e) => {
        const isHost = e.target.checked;
        document.getElementById("label-mode-family").className = isHost ? "text-slate-500" : "font-bold text-amber-400";
        document.getElementById("label-mode-host").className = isHost ? "font-bold text-indigo-400" : "text-slate-500";
        document.getElementById("abox-source-label").innerText = isHost ? "PC Hôte Local" : "Foyer Familial";

        // EFFACEMENT DU BANDEAU ET DE LA SYNTHÈSE ASSESS
        resetAuditView();
    });

    if (btnRun) btnRun.addEventListener("click", runPhase8Audit);
    if (btnApprove) btnApprove.addEventListener("click", approveAndMerge);
    if (btnReject) btnReject.addEventListener("click", () => {
        document.getElementById("tbox-proposal-card").classList.add("hidden");
    });

    // Configuration des boutons de presets Stress-Test PME
    document.querySelectorAll(".stress-preset-btn").forEach(btn => {
        btn.addEventListener("click", (e) => {
            const scale = e.currentTarget.getAttribute("data-scale");
            const label = e.currentTarget.getAttribute("data-label");
            runStressTestSimulation(scale, label);
        });
    });
});

let currentDeltaTurtle = "";

// Efface le bandeau de frugalité du bas et la synthèse d'assessment CESU
function resetAuditView() {
    document.getElementById("frugality-footer").classList.add("hidden");
    document.getElementById("fusion-zone").classList.add("hidden");
    document.getElementById("tbox-proposal-card").classList.add("hidden");
    document.getElementById("abox-main-display").textContent = 'Cliquez sur "Lancer l\'Analyse"...';
    document.getElementById("cti-items-container").innerHTML = '<p class="text-slate-500 italic">En attente de lancement...</p>';
}

async function runPhase8Audit() {
    const btnRun = document.getElementById("btn-run-audit");
    const isHostMode = document.getElementById("toggle-host-mode").checked;

    try {
        if (btnRun) btnRun.disabled = true;

        const modeQuery = isHostMode ? "host" : "family";
        const response = await fetch(`/api/phase8/audit?mode=${modeQuery}&load_factor=1`);
        if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);

        const data = await response.json();

        if (data.status === "success") {
            currentDeltaTurtle = data.delta_ttl || "";

            // ABox
            if (data.abox_ttl && data.abox_ttl.trim().length > 0) {
                document.getElementById("abox-main-display").textContent = data.abox_ttl;
            } else if (data.assets && data.assets.length > 0) {
                let aboxTtl = "@prefix data: <http://home.secure/data#> .\n@prefix soc1: <http://home.secure/ontology/soc1#> .\n\n";
                data.assets.forEach(asset => {
                    const services = asset.exposed_services.join(", ") || "Aucun";
                    aboxTtl += `data:${asset.asset_id} a soc1:ResidentialAsset ;\n`;
                    aboxTtl += `    rdfs:label "${asset.name}" ;\n`;
                    aboxTtl += `    soc1:ip "${asset.ip_address}" ;\n`;
                    aboxTtl += `    soc1:os "${asset.os}" ;\n`;
                    aboxTtl += `    soc1:service "${services}" .\n\n`;
                });
                document.getElementById("abox-main-display").textContent = aboxTtl.trim();
            }

            // Affichage du Bandeau de Frugalité du Bas
            const rawMb = (data.frugality.raw_bytes / 1000000).toFixed(2);
            document.getElementById("frugality-raw").innerText = `~${rawMb} Mo`;
            document.getElementById("frugality-filtered").innerText = `${data.frugality.filtered_bytes} octets`;
            document.getElementById("frugality-badge").innerText = `-${data.frugality.reduction_pct}% Gain`;
            document.getElementById("frugality-footer").classList.remove("hidden");

            // CTI items
            const ctiContainer = document.getElementById("cti-items-container");
            if (isHostMode) {
                ctiContainer.innerHTML = `
                    <div class="p-2 bg-emerald-950/40 rounded border border-emerald-800/60 text-[11px]">
                        <span class="font-bold text-emerald-300 block">FastAPI Local Binding</span>
                        <span class="text-slate-400">127.0.0.1:8000 (Sain)</span>
                    </div>`;
            } else {
                ctiContainer.innerHTML = `
                    <div class="p-2 bg-emerald-950/40 rounded border border-emerald-800/60 text-[11px] space-y-1">
                        <span class="font-bold text-emerald-300 block">CVE-2017-0144 (EternalBlue)</span>
                        <span class="text-red-400 font-semibold">Windows 10 (192.168.1.10)</span>
                    </div>`;
            }

            document.getElementById("tbox-delta-preview").textContent = currentDeltaTurtle;
            document.getElementById("tbox-proposal-card").classList.remove("hidden");
        }
    } catch (err) {
        console.error(err);
    } finally {
        if (btnRun) btnRun.disabled = false;
    }
}

async function approveAndMerge() {
    const isHostMode = document.getElementById("toggle-host-mode").checked;
    
    document.getElementById("tbox-proposal-card").classList.add("hidden");
    const tboxDisplay = document.getElementById("tbox-main-display");
    tboxDisplay.textContent += "\n\n# --- TRIPLETS MERGED ---\n" + currentDeltaTurtle;

    const naturalReport = document.getElementById("natural-language-report");
    naturalReport.innerHTML = isHostMode ? 
        `<p class="text-emerald-300 font-semibold">✔️ Diagnostic Système Hôte : Configuration réseau et composants Python conformes.</p>` :
        `<p class="text-red-300 font-semibold">🚨 Risque Foyer : La machine Windows 10 présente une vulnérabilité critique SMB (CVE-2017-0144).</p>`;

    const fusionZone = document.getElementById("fusion-zone");
    fusionZone.classList.remove("hidden");
    fusionZone.scrollIntoView({ behavior: "smooth" });
}

// SIMULATION DE STRESS TEST (VUE DEDIEE)
async function runStressTestSimulation(scaleFactor, profileLabel) {
    try {
        const response = await fetch(`/api/phase8/audit?mode=family&load_factor=${scaleFactor}`);
        const data = await response.json();

        if (data.status === "success") {
            const assetCount = scaleFactor * 4;
            const serviceCount = scaleFactor * 12;
            const rawMb = (data.frugality.raw_bytes / 1000000).toFixed(1);

            document.getElementById("stress-count-assets").innerText = assetCount;
            document.getElementById("stress-count-services").innerText = serviceCount;
            document.getElementById("stress-count-raw").innerText = `${rawMb} Mo`;
            document.getElementById("stress-count-frugal").innerText = `${data.frugality.filtered_bytes} octets`;

            let aboxSummary = `# PROFIL APPLICATIF : ${profileLabel.toUpperCase()}\n`;
            aboxSummary += `# Volume Télémétrie Traité : ${rawMb} Mo bruts\n`;
            aboxSummary += `# Métriques Sémantiques Agrégées :\n`;
            aboxSummary += `soc1:OrganizationPME a soc1:EnterpriseContext ;\n`;
            aboxSummary += `    soc1:totalAssetsCount ${assetCount} ;\n`;
            aboxSummary += `    soc1:activeServicesCount ${serviceCount} ;\n`;
            aboxSummary += `    soc1:frugalCompressionRatio "${data.frugality.reduction_pct}%" ;\n`;
            aboxSummary += `    soc1:masterTBoxTriplesInjected ${data.frugality.triple_count} .\n`;

            document.getElementById("stress-abox-summary").textContent = aboxSummary;
        }
    } catch (err) {
        console.error("Erreur lors du Stress-Test :", err);
    }
}
