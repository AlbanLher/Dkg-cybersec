#!/usr/bin/env python3
"""
generate_phase2_abox.py
Génération automatisée de l'ABox Master (DKG Phase 2 - UseCase Cyber).
Satisfait aux exigences EXG-UC-ABOX-01, EXG-UC-ABOX-02, EXG-UC-ABOX-03, EXG-FWK-02-* et EXG-QUAL-*.
"""
import sys
from  pathlib import Path
# Ajout du dossier parent (03-Application/) au PATH Python
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
import os
from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, Literal, URIRef
from config import DKG, DKG_DATA, ABOX_MASTER_PATH, DIR_INSTANCES_ABOX



# Paths
TBOX_PATH = "02-Donnees/Master_Transversal/DKG_TBox_Master.ttl"
SHACL_PATH = "02-Donnees/Master_Transversal/DKG_SHACL_Master.ttl"
OUTPUT_ABOX_PATH = "02-Donnees/Master_Transversal/DKG_ABox_Master.ttl"

# Namespaces
DKG = Namespace("http://dkg.cybersec.org/schema#")
DKG_DATA = Namespace("http://dkg.cybersec.org/data/")

def generate_abox():
    # 1. Assurer la présence du répertoire TLP_RED
    DIR_INSTANCES_ABOX.mkdir(parents=True, exist_ok=True)


    g = Graph()
    g.bind("dkg", DKG)
    g.bind("dkg-data", DKG_DATA)
    g.bind("owl", OWL)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    # =========================================================================
    # 🔒 EN-TÊTE DE GOUVERNANCE & MARQUAGE TLP:RED (À INSERER ICI)
    # =========================================================================
    abox_ont = DKG_DATA["ABox_Master"]
    g.add((abox_ont, RDF.type, OWL.Ontology))
    g.add((abox_ont, RDFS.label, Literal("DKG ABox Master - Operational Cyber Security Graph", lang="fr")))
    g.add((abox_ont, DKG.tlpMarking, Literal("TLP:RED")))
    # =========================================================================


    # ---------------------------------------------------------
    # 1. TLP Markings (Referentiel de securite)
    # ---------------------------------------------------------
    tlp_clear = DKG_DATA["TLP-CLEAR"]
    tlp_green = DKG_DATA["TLP-GREEN"]
    tlp_amber = DKG_DATA["TLP-AMBER"]
    tlp_red = DKG_DATA["TLP-RED"]

    for tlp in [tlp_clear, tlp_green, tlp_amber, tlp_red]:
        g.add((tlp, RDF.type, DKG.TLPMarking))

    g.add((tlp_clear, RDFS.label, Literal("TLP:CLEAR", lang="en")))
    g.add((tlp_green, RDFS.label, Literal("TLP:GREEN", lang="en")))
    g.add((tlp_amber, RDFS.label, Literal("TLP:AMBER", lang="en")))
    g.add((tlp_red, RDFS.label, Literal("TLP:RED", lang="en")))

    # ---------------------------------------------------------
    # 2. Modes Operatoires / Threats (CAPEC)
    # ---------------------------------------------------------
    capec_126 = DKG_DATA["CAPEC-126"]
    capec_63 = DKG_DATA["CAPEC-63"]

    g.add((capec_126, RDF.type, DKG.ThreatPattern))
    g.add((capec_126, RDFS.label, Literal("Path Traversal", lang="en")))
    g.add((capec_126, DKG.description, Literal("An attacker manipulates path references to access files outside the intended folder.", lang="en")))

    g.add((capec_63, RDF.type, DKG.ThreatPattern))
    g.add((capec_63, RDFS.label, Literal("Simple Pass-Through", lang="en")))
    g.add((capec_63, DKG.description, Literal("Attacker executes arbitrary code by passing commands through input fields.", lang="en")))

    # ---------------------------------------------------------
    # 3. Faiblesses Logiciel (CWE)
    # ---------------------------------------------------------
    cwe_22 = DKG_DATA["CWE-22"]
    cwe_78 = DKG_DATA["CWE-78"]

    g.add((cwe_22, RDF.type, DKG.Weakness))
    g.add((cwe_22, RDFS.label, Literal("Improper Limitation of a Pathname to a Restricted Directory", lang="en")))
    g.add((cwe_22, DKG.hasThreatPattern, capec_126))
    g.add((capec_126, DKG.isThreatPatternOf, cwe_22)) # Materialisation inverse EXG-FWK-02-03

    g.add((cwe_78, RDF.type, DKG.Weakness))
    g.add((cwe_78, RDFS.label, Literal("Improper Neutralization of Special Elements used in an OS Command", lang="en")))
    g.add((cwe_78, DKG.hasThreatPattern, capec_63))
    g.add((capec_63, DKG.isThreatPatternOf, cwe_78))

    # ---------------------------------------------------------
    # 4. Vulnerabilites NIST (CVE)
    # ---------------------------------------------------------
    cve_2021_41773 = DKG_DATA["CVE-2021-41773"]
    cve_2021_44228 = DKG_DATA["CVE-2021-44228"]

    g.add((cve_2021_41773, RDF.type, DKG.Vulnerability))
    g.add((cve_2021_41773, RDFS.label, Literal("Apache HTTP Server Path Traversal Vulnerability", lang="en")))
    g.add((cve_2021_41773, DKG.cvssScore, Literal(7.5, datatype=XSD.decimal)))
    g.add((cve_2021_41773, DKG.exploitsWeakness, cwe_22))
    g.add((cwe_22, DKG.isWeaknessExploitedBy, cve_2021_41773))

    g.add((cve_2021_44228, RDF.type, DKG.Vulnerability))
    g.add((cve_2021_44228, RDFS.label, Literal("Log4Shell Remote Code Execution", lang="en")))
    g.add((cve_2021_44228, DKG.cvssScore, Literal(10.0, datatype=XSD.decimal)))
    g.add((cve_2021_44228, DKG.exploitsWeakness, cwe_78))
    g.add((cwe_78, DKG.isWeaknessExploitedBy, cve_2021_44228))

    # ---------------------------------------------------------
    # 5. Composants Logiques (SoftwareComponent)
    # ---------------------------------------------------------
    comp_apache = DKG_DATA["Comp-Apache-2-4-49"]
    comp_log4j = DKG_DATA["Comp-Log4j-2-14"]

    g.add((comp_apache, RDF.type, DKG.SoftwareComponent))
    g.add((comp_apache, RDFS.label, Literal("Apache HTTP Server v2.4.49", lang="fr")))
    g.add((comp_apache, DKG.hasVulnerability, cve_2021_41773))
    g.add((cve_2021_41773, DKG.isVulnerabilityOf, comp_apache))

    g.add((comp_log4j, RDF.type, DKG.SoftwareComponent))
    g.add((comp_log4j, RDFS.label, Literal("Apache Log4j Core v2.14.1", lang="fr")))
    g.add((comp_log4j, DKG.hasVulnerability, cve_2021_44228))
    g.add((cve_2021_44228, DKG.isVulnerabilityOf, comp_log4j))

    # ---------------------------------------------------------
    # 6. Actifs du SI (Asset)
    # ---------------------------------------------------------
    srv_web_prod = DKG_DATA["Asset-Srv-Prod-01"]
    srv_auth_prod = DKG_DATA["Asset-Srv-Auth-02"]

    g.add((srv_web_prod, RDF.type, DKG.Asset))
    g.add((srv_web_prod, RDFS.label, Literal("Serveur Web Frontend Production", lang="fr")))
    g.add((srv_web_prod, DKG.hasTLPMarking, tlp_amber))
    g.add((srv_web_prod, DKG.hasInstalledComponent, comp_apache))
    g.add((comp_apache, DKG.isInstalledComponentOf, srv_web_prod))

    g.add((srv_auth_prod, RDF.type, DKG.Asset))
    g.add((srv_auth_prod, RDFS.label, Literal("Serveur Authentification Central", lang="fr")))
    g.add((srv_auth_prod, DKG.hasTLPMarking, tlp_red))
    g.add((srv_auth_prod, DKG.hasInstalledComponent, comp_log4j))
    g.add((comp_log4j, DKG.isInstalledComponentOf, srv_auth_prod))

    # Serialisation ABox Master
    g.serialize(destination=str(ABOX_MASTER_PATH), format="turtle")
    print(f"✅ ABox Master générée sous : {ABOX_MASTER_PATH} ({len(g)} triplets  ")


    # os.makedirs(os.path.dirname(OUTPUT_ABOX_PATH), exist_ok=True)
    # g.serialize(destination=OUTPUT_ABOX_PATH, format="turtle")
    # print(f"✅ ABox Master générée avec succès : {OUTPUT_ABOX_PATH} ({len(g)} triplets)")

if __name__ == "__main__":
    generate_abox()
