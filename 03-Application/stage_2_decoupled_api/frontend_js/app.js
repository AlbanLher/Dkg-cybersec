const API_BASE_URL = "http://127.0.0.1:8000";
let currentSourceMode = "local"; // "local" ou "family"

function toggleDataSource() {
    const btn = document.getElementById("toggle-source-btn");
    if (currentSourceMode === "local") {
        currentSourceMode = "family";
        btn.innerText = "🔄 Mode Actuel : Cas d'École (Famille)";
        btn.className = "bg-yellow-600 hover:bg-yellow-500 text-white font-bold py-2 px-4 rounded shadow transition";
    } else {
        currentSourceMode = "local";
        btn.innerText = "🔄 Mode Actuel : Poste Local (TLP:RED)";
        btn.className = "bg-purple-600 hover:bg-purple-500 text-white font-bold py-2 px-4 rounded shadow transition";
    }
    // Recharge automatiquement l'inventaire avec la nouvelle source
    loadInventory();
}

async function loadInventory() {
    const container = document.getElementById("inventory-container");
    const title = document.getElementById("inventory-title");
    
    if (title) title.innerText = `📂 Inventaire (${currentSourceMode === 'local' ? 'Poste Local TLP:RED' : 'Cas d\'École Famille'})`;
    if (container) container.innerHTML = "<p class='text-yellow-400'>Chargement de l'inventaire depuis l'API...</p>";

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/inventory?source=${currentSourceMode}`);
        if (!response.ok) throw new Error("Erreur réseau lors de la récupération de l'inventaire.");
        
        const data = await response.json();
        let html = `<p class="text-sm text-gray-400 mb-2">Source : <span class="text-green-400 font-mono">${data.source_mode}</span> | Total actifs : ${data.household_assets.length}</p>`;
        
        data.household_assets.forEach(asset => {
            html += `
                <div class="bg-gray-700 p-3 rounded mb-2 border-l-4 ${currentSourceMode === 'local' ? 'border-purple-500' : 'border-yellow-500'}">
                    <strong>${asset.name}</strong> (${asset.ip_address})<br>
                    <span class="text-xs text-gray-300">OS: ${asset.os} | Zone: ${asset.zone}</span><br>
                    <span class="text-xs text-blue-300">Services: ${asset.exposed_services.join(', ')}</span>
                </div>
            `;
        });
        if (container) container.innerHTML = html;
    } catch (error) {
        if (container) container.innerHTML = `<p class="text-red-400">Erreur : ${error.message}.</p>`;
    }
}


async function loadAudit() {
    const container = document.getElementById("audit-container");
    const title = document.getElementById("audit-title");
    title.innerText = `🛡️ Audit SOC en cours (${currentSourceMode.toUpperCase()})...`;
    container.innerHTML = "<p class='text-yellow-400'>Exécution de l'analyse sémantique et corrélation CTI...</p>";

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/audit?source=${currentSourceMode}`);
        if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);
        
        const data = await response.json();
        title.innerText = `🛡️ Résultats de l'Audit (${data.source_mode.toUpperCase()})`;
        
        let html = `<div class="space-y-4">`;
        
        // Encart de traçabilité sémantique
        html += `
            <div class="bg-gray-900 p-3 rounded border border-blue-500 text-xs text-gray-300">
                <strong class="text-blue-400">🧠 Traçabilité du Rapprochement Sémantique :</strong><br>
                - Source active : <span class="text-green-400 font-mono">${data.source_mode}</span><br>
                - Moteur : Corrélation entre les services exposés (JSON) et les CVE de la base CTI.
            </div>
        `;

        const reports = data.audit_data || [];
        
        if (reports.length === 0) {
            html += `<p class="text-green-400">Aucun rapport d'actif généré pour cette source.</p>`;
        } else {
            reports.forEach(rep => {
                let borderColor = "border-green-500";
                if (rep.risk_level && rep.risk_level.includes("CRITIQUE")) borderColor = "border-red-500";
                else if (rep.risk_level && rep.risk_level.includes("MOYEN")) borderColor = "border-yellow-500";

                html += `
                    <div class="bg-gray-700 p-4 rounded border-l-4 ${borderColor}">
                        <div class="flex justify-between items-center mb-1">
                            <strong>🖥️ ${rep.asset_name || 'Actif Inconnu'}</strong>
                            <span class="text-xs px-2 py-0.5 rounded bg-gray-800 text-gray-200">${rep.risk_level || 'FAIBLE'}</span>
                        </div>
                        <p class="text-xs text-gray-300 mb-2">IP : ${rep.ip || 'N/A'} | Zone : ${rep.zone || 'N/A'}</p>
                `;

                // Gestion robuste des menaces (qu'elles soient sous forme de texte ou d'objet)
                if (rep.matched_threats && rep.matched_threats.length > 0) {
                    html += `<div class="bg-gray-800 p-2 rounded mb-2 text-xs">
                                <strong class="text-red-400">⚠️ Menaces & Applicatifs mis en cause :</strong>
                                <ul class="list-disc list-inside mt-1 space-y-1">`;
                    
                    rep.matched_threats.forEach(t => {
                        if (typeof t === 'string') {
                            html += `<li><span class="text-yellow-300 font-mono">${t}</span></li>`;
                        } else {
                            html += `<li><span class="text-yellow-300 font-mono">${t.cve || 'CVE'}</span> (Composant : <span class="text-white">${t.component || 'N/A'}</span> ➔ Service : <span class="text-blue-300">${t.service_matched || 'N/A'}</span>)</li>`;
                        }
                    });
                    html += `</ul></div>`;
                } else {
                    html += `<p class="text-xs text-green-400 mb-2">✔️ Aucune menace sémantique corrélée.</p>`;
                }

                html += `
                        <div class="text-xs text-blue-300">
                            <strong>Recommandations :</strong>
                            <ul class="list-disc list-inside mt-1">
                                ${(rep.recommendations || ['Aucune recommandation']).map(rec => `<li>${rec}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                `;
            });
        }
        html += `</div>`;
        container.innerHTML = html;

    } catch (error) {
        console.error("Erreur Audit:", error);
        container.innerHTML = `<p class="text-red-400 font-bold">Erreur lors du chargement de l'audit :<br><span class="text-xs font-normal">${error.message}</span></p>`;
    }
}

// Fonction pour récupérer et afficher le rapport de conformité de la Phase 8
async function loadComplianceReport() {
    const container = document.getElementById('compliance-status-container');
    if (!container) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/compliance/report`);
        if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);
        
        const data = await response.json();
        const metrics = data.resource_profiling;

        let html = `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-gray-700 p-4 rounded border-l-4 border-purple-500">
                    <p class="text-sm text-gray-200"><strong>Portée :</strong> ${data.compliance_scope}</p>
                    <p class="text-sm text-gray-200 mt-1"><strong>Cadre :</strong> ${data.framework}</p>
                    <p class="text-sm text-gray-200 mt-1"><strong>Triplets normatifs :</strong> <span class="text-blue-300 font-mono">${data.standards_triplets_count}</span></p>
                </div>
                <div class="bg-gray-700 p-4 rounded border-l-4 border-green-500">
                    <h4 class="font-bold text-green-400 mb-1">🌱 Profiling Green-by-Design</h4>
                    <p class="text-xs text-gray-300">Statut : <span class="text-green-300 font-mono">${metrics.status}</span></p>
                    <p class="text-xs text-gray-300">Temps d'exécution : <span class="text-white font-mono">${metrics.execution_time_ms} ms</span></p>
                    <p class="text-xs text-gray-300">Pic mémoire : <span class="text-white font-mono">${metrics.memory_peak_mb} Mo</span></p>
                </div>
            </div>
            <div class="mt-4 bg-gray-900 p-3 rounded border border-gray-700 text-xs">
                <details class="cursor-pointer">
                    <summary class="font-bold text-purple-300">Afficher l'échantillon des règles normatives (TLP:CLEAR)</summary>
                    <ul class="list-disc list-inside mt-2 space-y-1 text-gray-300">
                        ${data.standards_sample.map(item => `<li><span class="text-blue-300 font-mono">${item.predicate.split('#').pop()}</span> : ${item.object}</li>`).join('')}
                    </ul>
                </details>
            </div>
        `;
        container.innerHTML = html;
    } catch (error) {
        console.error("Erreur chargement conformité:", error);
        container.innerHTML = `<p class="text-red-400 text-sm">❌ Impossible de charger le rapport de conformité depuis l'API.</p>`;
    }
}

// Ajout des fonctions de pilotage didactique dans app.js

async function resetABoxToFamily() {
    updateActiveAgent("ABoxManager (Reset)");
    const container = document.getElementById("inventory-container");
    container.innerHTML = "<p class='text-yellow-400'>Réinitialisation de l'ABox vers la situation 'Family'...</p>";

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/abox/reset`, { method: "POST" });
        if (!response.ok) throw new Error("Erreur lors du reset de l'ABox.");
        
        const data = await response.json();
        alert("✅ " + data.message);
        currentSourceMode = "family";
        loadInventory();
    } catch (error) {
        alert("❌ Erreur : " + error.message);
    }
}

function updateActiveAgent(agentName) {
    const badge = document.getElementById("current-agent");
    if (badge) badge.innerText = agentName;
}

async function triggerTBoxGuardian() {
    updateActiveAgent("TBoxGuardianAgent");
    const hitmContainer = document.getElementById("hitm-container");
    hitmContainer.innerHTML = "<p class='text-yellow-400'>Analyse des sources externes et détection de concepts T-Box en cours...</p>";

    setTimeout(() => {
        hitmContainer.innerHTML = `
            <div class="bg-gray-900 p-4 rounded border border-yellow-500">
                <p class="text-sm text-yellow-300 font-bold">⚠️ Proposition d'enrichissement sémantique détectée par le Gardien T-Box</p>
                <p class="text-xs text-gray-300 mt-1">Concepts identifiés dans les flux externes nécessitant une intégration dans la T-Box maître.</p>
                <div class="mt-3 flex gap-2">
                    <button onclick="resolveHitM(true)" class="bg-green-600 hover:bg-green-500 text-white text-xs font-bold py-1 px-3 rounded">✅ Valider (HitM)</button>
                    <button onclick="resolveHitM(false)" class="bg-red-600 hover:bg-red-500 text-white text-xs font-bold py-1 px-3 rounded">❌ Rejeter</button>
                </div>
            </div>
        `;
        updateActiveAgent("HitM Gateway (En attente opérateur)");
    }, 1000);
}

async function resolveHitM(approved) {
    if (approved) {
        updateActiveAgent("TBoxGuardianAgent (Fusion validée)");
        document.getElementById("hitm-container").innerHTML = `
            <p class="text-green-400 text-sm">✔️ Enrichissement validé par l'opérateur. La T-Box maître a été enrichie avec succès.</p>
        `;
    } else {
        updateActiveAgent("Idle");
        document.getElementById("hitm-container").innerHTML = `
            <p class="text-red-400 text-sm">❌ Proposition rejetée. Aucun changement appliqué à la T-Box.</p>
        `;
    }
}

// Surcharge de loadAudit pour indiquer l'agent en cours
const originalLoadAudit = loadAudit;
loadAudit = async function() {
    updateActiveAgent("SOCEngine & MITMEngine");
    await originalLoadAudit();
    updateActiveAgent("Idle");
};












// Chargement automatique au démarrage de la page
document.addEventListener('DOMContentLoaded', () => {
    loadComplianceReport();
});


