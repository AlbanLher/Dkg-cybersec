// LOGIQUE PHASE 8 v3 (Étape B) — EXG-MET-P8-DEM_1 (Tri-Boîtes), DEM_2
// (Air-Gapped), DEM_3 (HITL), DEM_4 (didactique/Mermaid/frugalité),
// DEM_5 (audit trail), RES_1 (Seed/Reset), EXG-FWK-P8-AGE_1 (Local-First).
// tracabilité : EXG-MET-P8-DEM_1, EXG-MET-P8-DEM_4a, EXG-MET-P8-DEM_4d, EXG-MET-P8-DEM_4e, EXG-MET-P8-RES_1 (bouton reset), EXG-FWK-P8-AGE_2
// ==============================================================================

let currentProposedDelta = null;
let lastBilanItems = [];   // EXG-MET-P8-DEM_4b : findings courants pour la vue superposition
let currentDidacticDefault = null;

// --- EXG-MET-P8-DEM_4a : message didactique (mise à jour à chaque étape) ------
function setDidactic(message) {
    const el = document.getElementById("p8-didactic-text");
    if (el) el.textContent = message;
}

document.addEventListener("DOMContentLoaded", () => {
    loadPhase8TBox();               // Exécute EXG-MET-P8-DEM_1 : TBox dès l'ouverture
    loadPhase8SourcesCatalog();
    refreshPhase8Frugality();        // EXG-FWK-P8-AGE_2 : abaque Green-Dev à l'ouverture
    const modeSelect = document.getElementById("p8-mode-select");
    if (modeSelect) modeSelect.addEventListener("change", onModeChanged);
});

// --- Étape 1 : TBox au chargement (EXG-MET-P8-DEM_1) ---------------------------
async function loadPhase8TBox() {
    const pane = document.getElementById("p8-ttl-tbox");
    try {
        const res = await fetch("/api/phase8/tbox");
        const data = await res.json();
        pane.textContent = data.tbox_ttl || "# TBox vide";
        updateFrugalFooter(data.tbox_ttl ? data.tbox_ttl.length : 0, "TBox");
    } catch (err) {
        pane.textContent = `# Erreur chargement TBox : ${err.message}`;
    }
    setDidactic("La TBox (volet AMBER) est l'ossature historique du socle : vocabulaire et règles, affichés dès votre arrivée. Cliquez sur [Vue graphique] si le Turtle vous rebute. Prochaine étape : choisissez votre terrain avec le Toggle.");
}

// --- Étape 2 : Terrain ABox (EXG-MET-P8-DEM_4c : .private/ hors Git) -----------
async function onModeChanged() {
    const mode = document.getElementById("p8-mode-select").value;
    // Préchargement ABox côté UI : l'ABox est servie par l'audit ; ici on annonce.
    if (mode === "scan") {
        setDidactic("Terrain « Poste réel » sélectionné : l'ABox sera celle de VOTRE machine (scan non intrusif, TLP:RED, .private/). Si aucun scan n'a encore été fait, cliquez sur [🖥️ Scanner mon poste] — c'est un acte HITL, jamais automatique. La confrontation CTI s'appliquera ensuite à l'identique des terrains simulés.");
    } else if (mode === "hote") {
        setDidactic("Terrain « SI Hôte » (simulé) sélectionné : l'inventaire serveur du seed (Log4j 2.14.1, Apache 2.4.49) sera projeté en TLP:RED. Cochez maintenant des sources CTI si besoin, puis lancez l'analyse.");
    } else {
        setDidactic("Terrain « Foyer » (simulé) sélectionné : l'inventaire résidentiel du seed (box, PC, caméra FreeRTOS…) sera projeté en TLP:RED (bordure rouge). Rien n'est parti sur le réseau. Cochez maintenant des sources CTI si besoin, puis lancez l'analyse.");
    }
    await onTriggerSelected();     // RBox + CTI rafraîchis à chaque trigger
}

// --- v-real : scan du poste (ACTE HITL — POST /api/phase8/scan) ----------------
async function scanLocalHost() {
    const btn = document.getElementById("p8-btn-scan");
    if (!btn) return;
    // Consentement explicite : la demande elle-même est le geste HITL.
    if (!confirm("Scanner CE poste ?\n\nCollecte non intrusive : hostname, IP locale, OS, ports en écoute sur 127.0.0.1, composants logiciels détectés.\n\nDonnées classées TLP:RED, écrites dans .private/ (hors Git), ne quittent jamais votre poste.\nLe consentement est journalisé dans l'audit trail.")) {
        setDidactic("Scan annulé — aucune donnée collectée. Le démonstrateur ne scanne JAMAIS sans votre geste explicite (HITL).");
        return;
    }
    btn.disabled = true;
    btn.textContent = "Scan en cours...";
    setDidactic("Scan non intrusif en cours : lecture locale uniquement (aucun paquet vers l'extérieur). Le JSON TLP:RED part dans .private/, puis l'agent d'inventaire le matérialise en ABox conforme à la TBox.");
    try {
        const res = await fetch("/api/phase8/scan", { method: "POST" });
        const result = await res.json();
        if (!res.ok) throw new Error(result.detail || `HTTP ${res.status}`);
        setDidactic(`Scan TLP:RED enregistré (HITL journalisé) : ${result.assets || 1} actif(s), ${result.components || 0} composant(s) détecté(s) — ABox dans .private/, jamais purgée par le reset. Basculez le terrain sur « Poste réel » puis lancez l'analyse : la confrontation CTI s'appliquera à VOS vraies versions.`);
        // Sélection du terrain scan pour fluidifier la démo
        const modeSelect = document.getElementById("p8-mode-select");
        if (modeSelect) { modeSelect.value = "scan"; await onModeChanged(); }
        refreshPhase8Frugality();
    } catch (err) {
        setDidactic(`Échec du scan : ${err.message} — vérifiez que core/local_host_scanner.py et core/local_host_abox_agent.py sont déposés (cf. PATCH_scan_reel.md).`);
    } finally {
        btn.disabled = false;
        btn.textContent = "🖥️ Scanner mon poste (TLP:RED)";
    }
}

// --- Étape 3 : catalogue + checkbox (EXG-MET-P8-DEM_2) -------------------------
async function loadPhase8SourcesCatalog() {
    const container = document.getElementById("p8-sources-container");
    if (!container) return;
    try {
        const res = await fetch("/api/phase8/sources");
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const sources = await res.json();
        container.innerHTML = "";
        if (!Array.isArray(sources) || sources.length === 0) {
            container.innerHTML = '<span class="text-slate-500 italic">Aucune source CTI disponible.</span>';
            return;
        }
        sources.forEach(src => {
            const div = document.createElement("div");
            div.className = "flex items-center space-x-2";
            const srcId = src.id || "src_unknown";
            const acronym = src.acronym || "CTI";
            const label = src.label || src.name || "Source CTI";
            div.innerHTML = `
                <input type="checkbox" id="src-${srcId}" value="${srcId}"
                       onchange="onTriggerSelected(); updatePhase8NetworkBadge()"
                       class="rounded">
                <label for="src-${srcId}" class="text-xs text-slate-300 cursor-pointer select-none">
                    <strong class="text-amber-400">[${acronym}]</strong> ${label}
                </label>`;
            container.appendChild(div);
        });
    } catch (err) {
        container.innerHTML = `<span class="text-rose-400 text-xs">Erreur catalogue : ${err.message}</span>`;
    }
}

function updatePhase8NetworkBadge() {
    const checked = document.querySelectorAll("#p8-sources-container input[type='checkbox']:checked");
    const badge = document.getElementById("p8-network-badge");
    if (!badge) return;
    if (checked.length === 0) {
        badge.className = "text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 font-mono";
        badge.textContent = "0 requête (Air-Gapped)";
        setDidactic("Aucune source cochée : le démonstrateur reste Air-Gapped — 0 requête réseau. L'analyse raisonnerea uniquement sur les fichiers .ttl locaux (frugalité Green IT).");
    } else {
        badge.className = "text-xs px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-mono";
        badge.textContent = `${checked.length} requête(s) réseau`;
        setDidactic(`${checked.length} source(s) CTI cochée(s) : l'Agent Gardien interrogera uniquement ces sources pour enrichir le fonds local TLP:CLEAR (volet VERT). Décochez tout pour revenir en Air-Gapped.`);
    }
}

// --- RBox + CTI : rafraîchis à chaque trigger (coche ou mode) -----------------
async function onTriggerSelected() {
    await Promise.all([refreshPhase8RBox(), refreshPhase8CtiSelection()]);
}

async function refreshPhase8RBox() {
    // RBox non affichée en v2 (intégrée à la TBox) : conservée pour l'API
    try { await fetch("/api/phase8/rbox"); } catch (e) { /* silencieux */ }
}

async function refreshPhase8CtiSelection() {
    const pane = document.getElementById("p8-ttl-cti");
    if (!pane) return;
    const selected = Array.from(
        document.querySelectorAll("#p8-sources-container input[type='checkbox']:checked")
    ).map(cb => cb.value);
    if (selected.length === 0) {
        pane.textContent = "# TLP:CLEAR non chargé — cochez des sources CTI.";
        updateFrugalFooter(0, "CTI");
        return;
    }
    try {
        const res = await fetch("/api/phase8/cti/select", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ source_ids: selected })
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        pane.textContent = data.cti_clear_ttl || "# CTI vide";
        updateFrugalFooter((data.cti_clear_ttl || "").length, "CTI", {
            remote: data.remote_volume_bytes,
            downloaded: data.downloaded_volume_bytes,
            local: data.local_volume_bytes,
            ram: data.ram_volume_bytes
        });
        showBulletin(data.cti_clear_ttl);
    } catch (err) {
        pane.textContent = `# Erreur CTI : ${err.message}`;
    }
}

// --- EXG-MET-P8-DEM_4d : bulletin brut replié ----------------------------------
function showBulletin(raw) {
    const card = document.getElementById("p8-bulletin-card");
    const pre = document.getElementById("p8-bulletin-raw");
    if (card && pre && raw) {
        pre.textContent = raw;
        card.classList.remove("hidden");
    }
}

// --- Footer frugalité (EXG-FWK-P8-AGE_2 + ratios v-live distant/local/RAM) -----
function updateFrugalFooter(bytes, zone, ratios) {
    const el = document.getElementById("p8-frugal-footer");
    const checked = document.querySelectorAll("#p8-sources-container input[type='checkbox']:checked").length;
    if (!el) return;
    const ko = b => (b / 1024).toFixed(1);
    if (ratios && ratios.remote > 0) {
        // v-live : ratios réels issus de la sonde distante (POST /cti/select)
        const pctLocal = ratios.remote ? (100 * ratios.local / ratios.remote).toFixed(2) : "0";
        el.textContent = `Frugalité v-live : distant sondé ${ko(ratios.remote)} Ko → téléchargé ${ko(ratios.downloaded)} Ko → local ${ko(ratios.local)} Ko (${pctLocal}% du distant) → RAM ${ko(ratios.ram)} Ko — ${checked} source(s) consultée(s).`;
    } else {
        el.textContent = `Frugalité : ${(bytes / 1024).toFixed(1)} Ko chargés (${zone}) — ${checked} requête(s) réseau.`;
    }
}

// --- Abaque Green-Dev (EXG-FWK-P8-AGE_2) : volumes + TOP entités --------------
async function refreshPhase8Frugality() {
    const pane = document.getElementById("p8-frugal-detail");
    if (!pane) return;
    try {
        const mode = document.getElementById("p8-mode-select").value;
        const res = await fetch("/api/phase8/frugality?mode=" + mode);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const f = await res.json();
        const ko = b => (b / 1024).toFixed(1);
        pane.innerHTML = `
            <p class="text-slate-400"><strong>Volume chargé (session) :</strong>
               TBox workset ${ko(f.loaded.tbox_workset_bytes)} Ko · ABox ${ko(f.loaded.abox_bytes)} Ko ·
               CTI ${ko(f.loaded.cti_bytes)} Ko · Règles ${ko(f.loaded.rules_workset_bytes)} Ko
               — soit <strong class="text-amber-300">${ko(f.loaded_total_bytes)} Ko</strong></p>
            <p class="text-slate-400"><strong>Volume disponible (magasin seeds + workset) :</strong>
               ${ko(f.available_total_bytes)} Ko —
               <strong class="${f.loaded_vs_available_pct < 50 ? "text-emerald-400" : "text-amber-300"}">la session n'en charge que ${f.loaded_vs_available_pct} %</strong></p>
            <p class="text-slate-400 mt-1"><strong>Entités les plus conséquentes du graphe actif :</strong></p>
            <ul class="list-disc ml-5 text-slate-300 text-xs">
                ${f.top_entities.map(e => `<li>${e.entity} — ${e.triplets} triplet(s)</li>`).join("")}
            </ul>`;
    } catch (err) {
        pane.innerHTML = `<span class="text-rose-400 text-xs">Erreur abaque : ${err.message}</span>`;
    }
}

// --- Étape 4 : Audit (EXG-MET-P8-DEM_1 & DEM_2) ---------------------------------
async function runPhase8Audit() {
    const btn = document.getElementById("p8-btn-audit");
    const modeSelect = document.getElementById("p8-mode-select");
    if (!btn || !modeSelect) return;
    const mode = modeSelect.value;
    const selectedSources = Array.from(
        document.querySelectorAll("#p8-sources-container input[type='checkbox']:checked")
    ).map(cb => cb.value);

    btn.disabled = true;
    btn.textContent = "Analyse en cours...";
    setDidactic("Analyse en cours : le moteur superpose les graphes — votre exposition (ABox) croisée avec les menaces connues (CTI locale). Le raisonnement est 100 % local : aucune requête réseau à ce stade.");
    try {
        const response = await fetch("/api/phase8/audit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mode, enabled_network_sources: selectedSources })
        });
        if (!response.ok) throw new Error(`Erreur serveur (${response.status})`);
        const data = await response.json();

        renderPhase8Bilan(data.nl_bilan);
        refreshPhase8Frugality();      // AGE_2 : abaque rafraîchi après audit
        document.getElementById("p8-ttl-tbox").textContent = data.tbox_ttl || "# TBox vide";
        document.getElementById("p8-ttl-abox").textContent = data.abox_ttl || "# ABox vide";
        document.getElementById("p8-ttl-cti").textContent = data.cti_clear_ttl || "# CTI vide";

        const hitlBox = document.getElementById("p8-hitl-box");
        if (data.delta_tbox_proposed && data.delta_tbox_proposed.trim().length > 0) {
            currentProposedDelta = data.delta_tbox_proposed;
            document.getElementById("p8-delta-tbox").textContent = data.delta_tbox_proposed;
            hitlBox.classList.remove("hidden");
            setDidactic("L'analyse révèle un écart : le fonds CTI coché utilise un vocabulaire que la TBox de référence ne connaît pas encore. La carte de l'Agent Gardien (au-dessus de la TBox) attend VOTRE décision : rien ne sera fusionné sans votre approbation — vous êtes le Gatekeeper.");
        } else {
            hitlBox.classList.add("hidden");
            currentProposedDelta = null;
            setDidactic("Analyse terminée : graphe conforme, aucune extension d'ontologie requise. Le bilan ci-dessus synthétise les expositions détectées et les actions conseillées.");
        }
    } catch (err) {
        alert(`Échec de l'analyse : ${err.message}`);
    } finally {
        btn.disabled = false;
        btn.textContent = "Lancer l'Analyse";
    }
}

// --- Bilan NL (EXG-MET-P8-DEM_1) ------------------------------------------------
function renderPhase8Bilan(bilanItems) {
    const container = document.getElementById("p8-bilan-list");
    if (!container) return;
    container.innerHTML = "";
    if (!bilanItems || bilanItems.length === 0) {
        container.innerHTML = '<p class="text-sm text-emerald-400">Aucune vulnérabilité ou menace détectée.</p>';
        return;
    }
    lastBilanItems = bilanItems || [];   // EXG-MET-P8-DEM_4b : pour la vue superposition
    bilanItems.forEach((item, idx) => {
        const sev = item.severity || "INFO";
        const color = sev === "RED" ? "rose" : (sev === "AMBER" ? "amber" : "emerald");
        const itemDiv = document.createElement("div");
        itemDiv.className = `p-3 bg-slate-900 border-l-4 border-${color}-500 rounded text-xs space-y-1`;
        itemDiv.innerHTML = `
            <div class="flex justify-between items-center">
                <span class="font-bold text-slate-200">${item.equipment || "Équipement"} — ${item.component || "Composant"}</span>
                <span class="flex items-center gap-1">
                    <button onclick="showSuperpositionGraph(${idx})" title="Superposition verticale TBox/ABox/CTI de cette alerte (rouge = interne TLP:RED, vert = CTI TLP:CLEAR)"
                            class="text-[10px] px-2 py-0.5 bg-slate-800 text-amber-300 rounded border border-slate-700 hover:bg-slate-700 transition">Vue superposition</button>
                    <span class="px-2 py-0.5 font-bold rounded-full ${item.linkage === "implicite" ? "bg-rose-500/20 text-rose-400" : "bg-emerald-500/20 text-emerald-400"}"
                          title="${item.linkage === "implicite" ? "Liaison détectée par mot-clé : le lien ABox↔CTI n'est pas formalisé dans le graphe (candidate Gardien ABox §37)" : "Liaison formelle : le raisonnement suit le graphe (SPARQL)"}">
                        ${item.linkage === "implicite" ? "⚠️ implicite" : "✓ formel"}</span>
                    <span class="px-2 py-0.5 bg-${color}-500/20 text-${color}-400 font-bold rounded-full">${sev}</span>
                </span>
            </div>
            <p class="text-slate-400"><strong>Statut :</strong> ${item.status || "N/A"}</p>
            <p class="text-amber-300"><strong>Action requise :</strong> ${item.action || "Aucune action"}</p>`;
        container.appendChild(itemDiv);
    });
}

// --- Étape 5 : HITL Approuver / Rejeter (EXG-MET-P8-DEM_3 + DEM_5) -------------
async function mergePhase8TBox() {
    if (!currentProposedDelta) {
        alert("Aucune proposition à fusionner.");
        return;
    }
    try {
        const res = await fetch("/api/phase8/tbox/merge", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ delta_ttl: currentProposedDelta })
        });
        const result = await res.json();
        if (!res.ok) throw new Error(result.detail || "Échec de la fusion");
        document.getElementById("p8-hitl-box").classList.add("hidden");
        currentProposedDelta = null;
        await loadPhase8TBox();      // TBox consolidée réaffichée
        setDidactic(`L'ontologie vient d'évoluer sous votre contrôle : le delta a été validé (rdflib), fusionné une seule fois (idempotence), dans le WORKING SET TLP:AMBER — jamais le Master ni les seeds. Décision journalisée dans l'audit trail (DEM_5). Relancez l'analyse : plus aucune proposition ne devrait apparaître — la boucle est bouclée.`);
    } catch (err) {
        alert(`Erreur HITL : ${err.message}`);
    }
}

async function rejectPhase8TBox() {
    // EXG-MET-P8-DEM_3 : le rejet est une issue EXPLICITE passée par la passerelle
    // (POST /tbox/reject) => décision journalisée dans l'audit trail (DEM_5).
    // L'ancienne version masquait la carte localement sans tracer : corrigé.
    if (!currentProposedDelta) {
        alert("Aucune proposition à rejeter.");
        return;
    }
    try {
        const res = await fetch("/api/phase8/tbox/reject", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ delta_ttl: currentProposedDelta })
        });
        const result = await res.json();
        if (!res.ok) throw new Error(result.detail || "Échec du rejet");
        document.getElementById("p8-hitl-box").classList.add("hidden");
        currentProposedDelta = null;
        // EXG-MET-P8-DEM_4 : conséquences du rejet en langage clair SOC.
        setDidactic("Proposition REJETÉE et décision journalisée (audit trail DEM_5). Conséquence pour le raisonnement : les liens exploitWeakness / isCisaKev ne sont PAS déclarés dans la TBox de référence — le graphe reste INCOMPLET. Tant que l'écart persiste, le moteur ne peut pas raisonner sur ces relations (ex. relier une CVE à la faiblesse qu'elle exploite, ou signaler un critère CISA KEV) : chaque audit avec cette CTI cochée reproposera le même delta. Pour sortir de cette boucle : soit vous acceptez un jour le merge, soit la TBox de référence est enrichie par la voie de gouvernance (pipeline, HITL CLI) — jamais automatiquement.");
    } catch (err) {
        alert(`Erreur rejet : ${err.message}`);
    }
}

// --- EXG-MET-P8-RES_1 : Réinitialisation de la démo (Seed/Reset) --------------
async function resetPhase8Demo() {
    // RES_1 : retour garanti au point de départ — seeds JAMAIS modifiés,
    // workset restauré, buffer CTI purgé, audit trail réinitialisé.
    const btn = document.getElementById("p8-btn-reset");
    if (btn) { btn.disabled = true; btn.textContent = "Réinitialisation..."; }
    try {
        const res = await fetch("/api/phase8/reset", { method: "POST" });
        const result = await res.json();
        if (!res.ok) throw new Error(result.detail || "Échec du reset");

        // Restauration UI complète : carte Gardien, delta, bilan, CTI, badge.
        document.getElementById("p8-hitl-box").classList.add("hidden");
        currentProposedDelta = null;
        document.getElementById("p8-bilan-list").innerHTML =
            '<p class="text-sm text-slate-500 italic">Lancez l\'analyse pour afficher le bilan.</p>';
        document.getElementById("p8-ttl-abox").textContent =
            "# Basculez le Toggle pour charger l'ABox.";
        document.getElementById("p8-ttl-cti").textContent =
            "# TLP:CLEAR non chargé — cochez des sources CTI.";
        document.querySelectorAll("#p8-sources-container input[type='checkbox']")
            .forEach(cb => { cb.checked = false; });
        updatePhase8NetworkBadge();   // badge -> Air-Gapped
        await loadPhase8TBox();        // TBox workset restaurée réaffichée
        refreshPhase8Frugality();      // AGE_2 : abaque recalculé après reset
        setDidactic("Démonstrateur réinitialisé (RES_1) : le working set est restauré depuis les seeds, le buffer CTI est purgé et l'audit trail repart de zéro. Les seeds, eux, n'ont JAMAIS été modifiés — votre point de départ est garanti identique pour la prochaine session. Rejouez le scénario : Toggle, coche CTI, analyse, décision de Gatekeeper.");
    } catch (err) {
        alert(`Échec du reset : ${err.message}`);
    } finally {
        if (btn) { btn.disabled = false; btn.textContent = "Réinitialiser la démo"; }
    }
}

// --- EXG-MET-P8-DEM_4b : Vue graphique Mermaid de la TBox ------------------------
// --- EXG-MET-P8-DEM_4b : rendu Mermaid générique (TBox et ABox) ----------------
async function renderMermaid(endpoint, title, errorMessage) {
    const section = document.getElementById("p8-graph-section");
    const target = document.getElementById("p8-graph-target");
    const heading = document.getElementById("p8-graph-title");
    section.classList.remove("hidden");
    heading.textContent = title;
    target.innerHTML = "<p class='text-slate-500 text-sm p-4'>Génération du graphe…</p>";
    let def = "";
    try {
        const res = await fetch(endpoint);
        if (!res.ok) throw new Error(`HTTP ${res.status} (endpoint absent ou erreur serveur ?)`);
        const data = await res.json();
        def = (data.mermaid || "").trim();
        if (!def) throw new Error("définition Mermaid vide renvoyée par le serveur");
        // Mermaid v10+ UMD : l'API vit sous window.mermaid.default (DEM_4b)
        const m = (window.mermaid && window.mermaid.default) || window.mermaid;
        if (!m || !m.render) throw new Error("mermaid.min.js non chargé ou version incompatible (vérifier /static/mermaid.min.js)");
        m.initialize({ startOnLoad: false, theme: "default" });
        // Conteneur ATTACHÉ et mesurable : hors écran mais PAS display:none —
        // un conteneur masqué produit un rendu VIDE (la « ligne blanche », DEM_4b).
        const tmpId = "p8-mermaid-tmp-svg";
        let tmp = document.getElementById(tmpId);
        if (!tmp) { tmp = document.createElement("div"); tmp.id = tmpId; document.body.appendChild(tmp); }
        tmp.style.cssText = "position:absolute;left:-99999px;top:0;width:800px;height:600px;visibility:hidden;";
        const { svg } = await m.render(tmpId + "-" + Date.now(), def, tmp);
        if (!svg || !svg.trim()) throw new Error("rendu Mermaid vide (définition invalide ?)");
        target.innerHTML = svg;
    } catch (err) {
        target.innerHTML = `<pre class="text-rose-500 text-xs p-4">${errorMessage} — ${err.message}</pre>`;
        if (def) target.innerHTML += `<pre class="text-slate-800 bg-slate-100 p-2 text-xs">${def}</pre>`;
    }
    section.scrollIntoView({ behavior: "smooth" });
}

function hideGraph() {
    document.getElementById("p8-graph-section").classList.add("hidden");
}

async function showTBoxGraph() {
    // Exécute EXG-MET-P8-DEM_4b : vue graphique de la TBox de référence (AMBER).
    await renderMermaid("/api/phase8/tbox/graph",
        "Vue graphique de la TBox de référence (TLP:AMBER)",
        "Erreur vue TBox");
    setDidactic("Vue graphique de la TBox : chaque boîte est une classe, chaque flèche une propriété d'objet. Comparez avec le Turtle du volet AMBER : même information, lecture différente.");
}

async function showABoxGraph() {
    // Exécute EXG-MET-P8-DEM_4b étendu : vue graphique de l'ABox active (RED).
    const mode = document.getElementById("p8-mode-select").value;
    const terrain = mode === "foyer" ? "Foyer (simulé)"
        : (mode === "scan" ? "Poste réel (scan)" : "SI Hôte (simulé)");
    await renderMermaid("/api/phase8/abox/graph?mode=" + mode,
        "Vue graphique de l'ABox " + terrain + " (TLP:RED)",
        "Erreur vue ABox");
    setDidactic(`Vue graphique de l'ABox (${terrain}) : chaque instance réelle de votre terrain apparaît sous sa classe (Asset, SoftwareComponent, Vulnerability…). C'est l'inventaire vivant qui vient d'être projeté — en TLP:RED.`);
}

// --- EXG-MET-P8-DEM_4b étendu : superposition TBox/ABox/CTI PAR ALERTE ------
async function showSuperpositionGraph(idx) {
    // Graphe VERTICAL de la chaîne de raisonnement de CETTE alerte :
    // interne en rouge (TLP:RED), fonds CTI externe en vert (TLP:CLEAR).
    const item = lastBilanItems[idx];
    if (!item) return;
    const mode = document.getElementById("p8-mode-select").value;
    await renderMermaid(
        `/api/phase8/superposition/graph?mode=${mode}&equipment=${encodeURIComponent(item.equipment || "")}`,
        `Superposition TBox/ABox/CTI — ${item.equipment || "alerte"}`,
        "Erreur vue superposition");
    setDidactic("Vue superposition de l'alerte : la chaîne verticale relie l'actif, ses composants et vulnérabilités (rouge, TLP:RED) jusqu'au fonds CTI externe (vert, TLP:CLEAR). Un lien pointillé ⚠️ signale un vocabulaire non déclaré en TBox — c'est la rupture de raisonnement qu'entretiendrait un rejet du Gardien.");
}
