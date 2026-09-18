import sys
from pathlib import Path
import json
import streamlit as st

# Injection SSOT (Single Source of Truth)
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from config import INPUT_RESIDENTIAL_JSON_PATH
from Phase7.residential_models import ResidentialFamilyEnvironment
from Phase7.external_cti_agent import ExternalCTIAgent
from Phase7.correlation_agent import CorrelationAgent

# Intégration du module technologique Phase 5
try:
    from Phase5.reasoning_engine import ReasoningEngine
    PHASE5_AVAILABLE = True
except ImportError:
    PHASE5_AVAILABLE = False
    ReasoningEngine = None

from modules.source_catalog import SOURCES_CATALOG
from modules.system_scanner import scan_local_machine

st.set_page_config(
    page_title="DKG-CyberSec | SOC Agentique & CTI",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ DKG-CyberSec — Centre d'Opérations de Sécurité (SOC) Agentique")
st.markdown("*Pipeline Global : ABox Phase 7 ➔ Moteur de Raisonnement Sémantique Phase 5 ➔ CTI TLP:CLEAR.*")

# --- CHARGEMENT STRICT DE L'ABOX PHASE 7 ---
if not INPUT_RESIDENTIAL_JSON_PATH.exists():
    st.error(f"❌ Erreur critique : L'artéfact ABox de la Phase 7 est introuvable à l'emplacement : `{INPUT_RESIDENTIAL_JSON_PATH}`.")
    st.info("Veuillez exécuter le pipeline de la Phase 7 pour générer l'environnement initial avant d'ouvrir l'interface.")
    st.stop()

try:
    with open(INPUT_RESIDENTIAL_JSON_PATH, "r", encoding="utf-8") as f:
        env_data = json.load(f)
    env_model = ResidentialFamilyEnvironment(**env_data)
except Exception as e:
    st.error(f"Erreur de chargement du modèle de données Phase 7 : {e}")
    st.stop()

if "cti_loaded" not in st.session_state:
    st.session_state.cti_loaded = False

if "phase5_executed" not in st.session_state:
    st.session_state.phase5_executed = False

# --- SIDEBAR : ORCHESTRATEUR CTI & MOTEUR PHASE 5 ---
st.sidebar.header("📡 Catalogue des Sources CTI")
for src in SOURCES_CATALOG:
    badge = "📊 Structurée" if src["type"] == "Structured" else "📝 Non Structurée"
    st.sidebar.markdown(f"- **{src['name']}** (`{badge}`)")

st.sidebar.markdown("---")
st.sidebar.header("🤖 Agents & Moteur Sémantique")

# Chargement CTI et calcul des compteurs structurés / non structurés
cti_entries = []
structured_count = 0
unstructured_count = 0

if st.session_state.cti_loaded:
    try:
        cti_agent = ExternalCTIAgent()
        cti_entries = cti_agent.load_cti_database()
        # Distinction selon la source ou le type de données
        structured_count = sum(1 for e in cti_entries if getattr(e, 'source_type', 'Structured') == 'Structured' or hasattr(e, 'cvss_score'))
        unstructured_count = len(cti_entries) - structured_count
        if unstructured_count < 0:
            unstructured_count = 0
    except Exception as e:
        cti_entries = []

if not st.session_state.cti_loaded:
    st.sidebar.warning("⚠️ CTI externe non chargée.")
    if st.sidebar.button("🚀 Lancer l'Agent Récupérateur TLP:CLEAR"):
        with st.spinner("Synchronisation des sources CTI..."):
            st.session_state.cti_loaded = True
            st.rerun()
else:
    st.sidebar.success("✅ Flux CTI TLP:CLEAR actif.")
    st.sidebar.markdown(f"""
    - **Éléments structurés récupérés :** `{structured_count}`
    - **Éléments non structurés récupérés :** `{unstructured_count}`
    - **Total flux CTI :** `{len(cti_entries)}`
    """)
    if st.sidebar.button("🔄 Réinitialiser l'État CTI"):
        st.session_state.cti_loaded = False
        st.session_state.phase5_executed = False
        st.rerun()

# Bouton d'activation du Moteur de Raisonnement Phase 5
if PHASE5_AVAILABLE and st.session_state.cti_loaded:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 Raisonnement Sémantique (Phase 5)")
    if st.sidebar.button("⚙️ Exécuter le ReasoningEngine"):
        with st.spinner("Exécution des règles d'inférence R-01 & R-02..."):
            try:
                engine = ReasoningEngine()
                exec_time = engine.run_inference()
                engine.save_and_document()
                st.session_state.phase5_executed = True
                st.sidebar.success(f"Inférence réussie en {exec_time:.3f}s !")
            except Exception as ex:
                st.sidebar.error(f"Erreur Phase 5 : {ex}")

# Corrélation Phase 7
try:
    correlation_agent = CorrelationAgent()
    risks = correlation_agent.analyze_risks(env_model, cti_entries) if st.session_state.cti_loaded else []
except Exception as e:
    risks = []

# --- ONGLETS PRINCIPAUX ---
tab1, tab2, tab3 = st.tabs([
    "🚨 Triage & Investigation des Menaces", 
    "💻 Scan Local & Enrichissement", 
    "🧪 Simulation de Remédiation"
])

with tab1:
    if not st.session_state.cti_loaded:
        st.info("ℹ️ **Mode Inactif :** Veuillez lancer l'Agent Récupérateur CTI dans la barre latérale pour initier le pipeline.")
        
        st.markdown("### 📋 Inventaire ABox (Phase 7)")
        for asset in env_model.assets:
            st.markdown(f"- **🖥️ {asset.host_id}** ({asset.name} - OS: `{asset.os}`)")
            for srv in asset.local_services:
                st.markdown(f"  - 📦 Logiciel : `{srv.name}` (v{srv.version})")
    
    elif not st.session_state.phase5_executed:
        st.warning("⚠️ **Raisonnement non exécuté :** Le catalogue CTI est chargé, mais le moteur sémantique de la Phase 5 doit être lancé.")
        st.info("👈 Cliquez sur le bouton **'⚙️ Exécuter le ReasoningEngine'** dans la barre latérale pour effectuer le rapprochement sémantique.")
        
        st.markdown(f"### 📊 État Actuel de la Récupération CTI")
        col_c1, col_c2 = st.columns(2)
        col_c1.metric("Éléments Structurés (API / NVD)", structured_count)
        col_c2.metric("Éléments Non Structurés (Bulletins / RSS)", unstructured_count)

    else:
        # Phase 5 exécutée : Affichage détaillé des rapprochements et des actifs à haut risque
        high_risk_assets = [r for r in risks if r.risk_level in ["CRITICAL", "HIGH"]]
        matched_elements_count = len(risks)

        st.markdown("### 🔍 Résultats du Rapprochement Sémantique (Phase 5 & 7)")
        st.success(f"✅ Rapprochement effectué avec succès : **{matched_elements_count}** éléments corrélés au total, dont **{len(high_risk_assets)}** actifs qualifiés à haut risque.")

        # Affichage métriques
        m1, m2, m3 = st.columns(3)
        m1.metric("Éléments Rapprochés", matched_elements_count)
        m2.metric("Actifs à Haut Risque", len(high_risk_assets))
        m3.metric("Règles Appliquées", "R-01 (KEV) & R-02 (Cascade)")

        st.markdown("---")
        st.markdown("### 🚨 Liste des Actifs à Haut Risque Identifiés")

        if not high_risk_assets:
            st.info("Aucun actif critique ou hautement risqué répertorié après inférence.")
        else:
            # Sélection interactive de l'actif / alerte
            risk_options = {f"Actif : {r.asset_id} | Risque : {r.risk_level} — {r.description[:60]}...": r for r in high_risk_assets}
            selected_label = st.selectbox("Sélectionner un actif à haut risque pour inspection approfondie :", list(risk_options.keys()))
            selected_risk = risk_options[selected_label]

            st.markdown("---")
            st.markdown("#### 🔬 Inspecteur d'Investigation Détaillé")

            col_inv_left, col_inv_right = st.columns(2)

            target_asset = next((a for a in env_model.assets if a.host_id == selected_risk.asset_id), None)

            with col_inv_left:
                st.markdown("##### 🖥️ Actif & Logiciel Impacté (ABox Phase 7)")
                if target_asset:
                    st.markdown(f"- **Nom de l'Actif :** `{target_asset.name}` (`{target_asset.host_id}`)")
                    st.markdown(f"- **Adresse IP / Zone :** `{target_asset.ip_address}` ({target_asset.zone})")
                    st.markdown(f"- **Système d'Exploitation :** `{target_asset.os}`")
                    st.markdown("##### 📦 Logiciels audités sur cet actif :")
                    for srv in target_asset.local_services:
                        cve_val = getattr(srv, 'associated_cve', 'N/A')
                        st.markdown(f"  - **Logiciel :** `{srv.name}` (v{srv.version})")
                        st.markdown(f"  - **CVE Associée :** `{cve_val}`")
                else:
                    st.warning("Détails de l'actif introuvables dans l'ABox.")

            with col_inv_right:
                st.markdown("##### 📡 Détails de la Donnée Externe CTI (Structurée & Non Structurée)")
                
                # Recherche de la CVE correspondante dans le catalogue CTI chargé
                target_cve = None
                if target_asset:
                    for srv in target_asset.local_services:
                        if hasattr(srv, 'associated_cve') and srv.associated_cve:
                            target_cve = srv.associated_cve
                            break
                
                matched_entry = next((e for e in cti_entries if target_cve and e.cve_id == target_cve), cti_entries[0] if cti_entries else None)

                if matched_entry:
                    st.info(f"**CVE Cible :** `{matched_entry.cve_id}` (Score CVSS : `{matched_entry.cvss_score}`)")
                    
                    with st.expander("📊 Donnée Structurée (API / KEV / NVD)", expanded=True):
                        st.json({
                            "cve_id": matched_entry.cve_id,
                            "severity": matched_entry.severity,
                            "cvss_score": matched_entry.cvss_score,
                            "affected_product": matched_entry.affected_product,
                            "is_cisa_kev": getattr(matched_entry, 'is_cisa_kev', True)
                        })

                    with st.expander("📝 Donnée Non Structurée (Bulletin Éditeur / Advisory)", expanded=True):
                        st.markdown(f"> *Extrait brut du flux textuel CTI :*\n>\n> `{matched_entry.description}`")
                else:
                    st.warning("Aucun détail de source externe trouvé pour cette alerte.")

with tab2:
    st.markdown("### 💻 Analyse du Poste Local & Enrichissement de l'ABox")
    if st.button("🔍 Extraire les logiciels de la machine hôte"):
        local_sw = scan_local_machine()
        st.success(f"Extraction réussie ! {len(local_sw)} composants détectés.")
        
        selected_to_add = st.selectbox("Composant à injecter dans l'ABox :", [s["name"] for s in local_sw])
        if st.button("Ajouter à l'ABox (Phase 7)"):
            target_sw = next((s for s in local_sw if s["name"] == selected_to_add), None)
            if target_sw:
                new_asset = {
                    "host_id": f"machine_locale_{target_sw['name']}",
                    "name": f"Poste Hôte ({target_sw['name']})",
                    "ip_address": "127.0.0.1",
                    "os": "Dynamic Host OS",
                    "zone": "LAN",
                    "local_services": [target_sw]
                }
                env_data["assets"].append(new_asset)
                with open(INPUT_RESIDENTIAL_JSON_PATH, "w", encoding="utf-8") as f:
                    json.dump(env_data, f, indent=4)
                st.success(f"Logiciel `{target_sw['name']}` injecté dans l'ABox !")
                st.session_state.phase5_executed = False  # Réinitialise le moteur suite au changement d'inventaire
                st.rerun()

with tab3:
    st.markdown("### 🧪 Simulation de Remédiation")
    current_assets = env_data.get("assets", [])
    if current_assets:
        asset_to_remove = st.selectbox("Actif à retirer de l'ABox :", [a["host_id"] for a in current_assets])
        if st.button("🛡️ Appliquer la Remédiation"):
            env_data["assets"] = [a for a in current_assets if a["host_id"] != asset_to_remove]
            with open(INPUT_RESIDENTIAL_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(env_data, f, indent=4)
            st.success(f"Actif `{asset_to_remove}` retiré de l'ABox !")
            st.session_state.phase5_executed = False
            st.rerun()
    else:
        st.info("Aucun actif présent.")
