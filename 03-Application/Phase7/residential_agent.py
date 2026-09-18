import sys
from pathlib import Path
import shutil

# Injection dynamique du répertoire parent (03-Application) dans le sys.path (SSOT)
CURRENT_DIR = Path(__file__).resolve().parent
APPLICATION_DIR = CURRENT_DIR if CURRENT_DIR.name == "03-Application" else CURRENT_DIR.parent
if str(APPLICATION_DIR) not in sys.path:
    sys.path.insert(0, str(APPLICATION_DIR))

import json
from rdflib import Graph, Literal, RDF, BNode, URIRef

from config import (
    INPUT_RESIDENTIAL_JSON_PATH, 
    ABOX_RESIDENTIAL_PATH, 
    ABOX_MASTER_PATH, 
    DIR_SNAPSHOT_P7,
    DKG_DATA
)
from Phase7.residential_models import ResidentialFamilyEnvironment
from Phase7.external_cti_agent import ExternalCTIAgent
from Phase7.correlation_agent import CorrelationAgent, RiskPath


def generate_markdown_report(env_data: ResidentialFamilyEnvironment, risks: list[RiskPath], md_output_path: Path) -> None:
    """Génère le rapport humain complet au format .md incluant les risques corrélés et le diagramme Mermaid."""
    md_content = f"""# 📄 Rapport d'Audit & SOC Résidentiel (`TLP:RED`)

## 1. Vue d'ensemble de la Passerelle
- **Box FAI :** `{env_data.network_environment.gateway_name}`
- **Risque d'Exposition WAN :** `{env_data.network_environment.wan_exposure_risk}`
- **Service Exposé :** `{env_data.network_environment.exposed_service}`
- **Accès Wi-Fi Partagé/Invité :** `{env_data.network_environment.wifi_shared_access}`

## 2. Inventaire des Actifs Foyer ({len(env_data.assets)} équipements)
"""
    for asset in env_data.assets:
        md_content += f"""### - `{asset.host_id}` ({asset.name or 'Équipement'})
- **OS / Firmware :** `{asset.os}`
- **Adresse IP :** `{asset.ip_address}`
- **Services Locaux :**\n"""
        for srv in asset.local_services:
            md_content += f"  - `{srv.name}` (Port: `{srv.port}`, Statut: `{srv.status}`, CVE: `{srv.associated_cve}`)\n"

    md_content += f"""
## 3. Analyse des Risques & Chemins de Compromission ({len(risks)} alertes détectées)
| Niveau | Actif | Description du Risque | Action Recommandée |
| :--- | :--- | :--- | :--- |
"""
    for r in risks:
        md_content += f"| **{r.risk_level}** | `{r.asset_id}` | {r.description} | {r.recommended_action} |\n"

    md_content += """
## 4. Topologie & Vecteurs de Risque (Diagramme Mermaid)
```mermaid
graph TD
    subgraph Box_FAI ["Passerelle Domestique"]
        WAN[Exposition WAN: Plex]
        LAN[Réseau Local LAN]
    end
"""
    for asset in env_data.assets:
        clean_id = asset.host_id.replace("-", "_")
        md_content += f"    LAN --- {clean_id}\n"

    for r in risks:
        if r.risk_level == "CRITICAL":
            clean_id = r.asset_id.replace("-", "_")
            md_content += f"    style {clean_id} fill:#ff9999,stroke:#ff0000,stroke-width:2px;\n"

    md_content += """```
"""
    md_output_path.parent.mkdir(parents=True, exist_ok=True)
    md_output_path.write_text(md_content, encoding="utf-8")

def run_residential_pipeline() -> tuple[Path, Path]:
    """
    1. Valide les données JSON du foyer (Pydantic V2).
    2. Charge la CTI externe (ExternalCTIAgent).
    3. Exécute l'analyse de corrélation (CorrelationAgent).
    4. Génère le RDF snapshot TLP:RED incluant les risques.
    5. Promeut vers le Master Transversal (ABOX_MASTER_PATH).
    6. Génère le rapport Markdown complet avec Mermaid.
    """
    input_path = INPUT_RESIDENTIAL_JSON_PATH
    output_turtle = ABOX_RESIDENTIAL_PATH
    output_master = ABOX_MASTER_PATH
    output_md = DIR_SNAPSHOT_P7 / "DKG_ABox_Residential.md"
    
    if not input_path.exists():
        raise FileNotFoundError(f"Fichier d'entrée introuvable : {input_path}")
        
    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    # 1. Validation Pydantic V2
    env_data = ResidentialFamilyEnvironment(**raw_data)
    
    # 2. Chargement CTI Externe
    cti_agent = ExternalCTIAgent()
    cti_entries = cti_agent.load_cti_database()
    
    # 3. Corrélation des Risques
    correlation_agent = CorrelationAgent()
    risks = correlation_agent.analyze_risks(env_data, cti_entries)
    
    # 4. Construction du Graphe RDF enrichi
    g = Graph()
    g.bind("dkg-data", DKG_DATA)
    
    snapshot_ref = URIRef(DKG_DATA.ResidentialSnapshot)
    g.add((snapshot_ref, RDF.type, URIRef(DKG_DATA.SecuritySnapshot)))
    g.add((snapshot_ref, URIRef(DKG_DATA.hasTLP), Literal("TLP:RED")))
    
    gw_ref = URIRef(DKG_DATA[env_data.network_environment.gateway_name])
    g.add((gw_ref, RDF.type, URIRef(DKG_DATA.Gateway)))
    g.add((gw_ref, URIRef(DKG_DATA.wanExposureRisk), Literal(env_data.network_environment.wan_exposure_risk)))
    
    for asset in env_data.assets:
        asset_ref = URIRef(DKG_DATA[asset.host_id])
        g.add((asset_ref, RDF.type, URIRef(DKG_DATA.HostAsset)))
        g.add((asset_ref, URIRef(DKG_DATA.operatingSystem), Literal(asset.os)))
        g.add((asset_ref, URIRef(DKG_DATA.ipAddress), Literal(asset.ip_address)))
        g.add((asset_ref, URIRef(DKG_DATA.connectedToGateway), gw_ref))
        
        for srv in asset.local_services:
            srv_node = BNode()
            g.add((asset_ref, URIRef(DKG_DATA.runsService), srv_node))
            g.add((srv_node, URIRef(DKG_DATA.serviceName), Literal(srv.name)))
            g.add((srv_node, URIRef(DKG_DATA.servicePort), Literal(srv.port)))
            g.add((srv_node, URIRef(DKG_DATA.serviceStatus), Literal(srv.status)))

    # Injection des risques corrélés dans le graphe RDF
    for r in risks:
        risk_node = BNode()
        g.add((snapshot_ref, URIRef(DKG_DATA.hasSecurityRisk), risk_node))
        g.add((risk_node, RDF.type, URIRef(DKG_DATA.SecurityRisk)))
        g.add((risk_node, URIRef(DKG_DATA.riskLevel), Literal(r.risk_level)))
        g.add((risk_node, URIRef(DKG_DATA.riskDescription), Literal(r.description)))
        g.add((risk_node, URIRef(DKG_DATA.recommendedAction), Literal(r.recommended_action)))

    # 5. Sérialisation Snapshot Turtle
    output_turtle.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(output_turtle), format="turtle")
    
    # 6. Promotion vers le Master Transversal
    output_master.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(output_turtle, output_master)
    
    # 7. Génération du rapport Markdown enrichi (Tableau de risques + Mermaid)
    generate_markdown_report(env_data, risks, output_md)
    
    return output_turtle, output_master

if __name__ == "__main__":
    t_snap, t_master = run_residential_pipeline()
    print(f"[SUCCESS] Pipeline complet exécuté !")
    print(f" -> Snapshot Turtle : {t_snap}")
    print(f" -> Master Transversal : {t_master}")
