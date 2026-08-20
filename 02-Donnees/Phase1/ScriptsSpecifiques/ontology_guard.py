import os
import json
from rdflib import Graph, Namespace, RDF, RDFS, OWL

# Definitions des Namespaces
CYBER = Namespace("http://example.org/cyber-ontology#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class OntologyGuard:
    def __init__(self, ontology_path: str):
        self.ontology_path = ontology_path
        self.onto_graph = Graph()
        self.onto_graph.parse(ontology_path, format="ttl")
        
        # Extraction du schéma actuel
        self.existing_classes = self._get_classes(self.onto_graph)
        self.existing_properties = self._get_properties(self.onto_graph)

    def _get_classes(self, g: Graph) -> set:
        classes = set()
        for s in g.subjects(RDF.type, OWL.Class):
            classes.add(self._short_name(s))
        for s in g.subjects(RDF.type, RDFS.Class):
            classes.add(self._short_name(s))
        return classes

    def _get_properties(self, g: Graph) -> set:
        props = set()
        for p_type in [OWL.DatatypeProperty, OWL.ObjectProperty, RDF.Property]:
            for s in g.subjects(RDF.type, p_type):
                props.add(self._short_name(s))
        return props

    def _short_name(self, uri) -> str:
        uri_str = str(uri)
        if "#" in uri_str:
            return uri_str.split("#")[-1]
        elif "/" in uri_str:
            return uri_str.split("/")[-1]
        return uri_str

    def analyze_rdf(self, rdf_path: str):
        data_graph = Graph()
        data_graph.parse(rdf_path, format="ttl")
        
        new_classes = set()
        new_props = set()

        # Inspection des types d'instances dans les données
        for s, p, o in data_graph.triples((None, RDF.type, None)):
            c_name = self._short_name(o)
            if c_name not in ["Resource", "NamedIndividual"]:
                if c_name not in self.existing_classes:
                    new_classes.add(c_name)

        # Inspection des prédicats utilisés
        for s, p, o in data_graph:
            p_name = self._short_name(p)
            if p_name not in ["type"] and p_name not in self.existing_properties:
                new_props.add(p_name)

        return new_classes, new_props

    def analyze_json_inventory(self, json_path: str):
        new_classes = set()
        new_props = set()

        # Dictionnaire des propriétés connues par classe en V0
        known_class_props = {
            "Device": {"id", "ip", "type", "importedAt"},
            "Software": {"key", "name", "version"}
        }

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        devices = data.get("devices", [])
        for dev in devices:
            for key in dev.keys():
                if key != "software" and key not in known_class_props["Device"]:
                    new_props.add(f"Device.{key}")
            
            for soft in dev.get("software", []):
                for key in soft.keys():
                    if key not in known_class_props["Software"]:
                        new_props.add(f"Software.{key}")

        return new_classes, new_props


    def generate_report(self, new_classes: set, new_props: set, output_report_path: str):
        has_changes = bool(new_classes or new_props)
        status = "Cas 2 / Cas 3 : Écart d'ontologie détecté" if has_changes else "Cas 1 : Aucune modification requise (RAS)"

        # 1. Extraction et isolation des propriétés par classe
        dev_props = [p.split(".")[-1] for p in new_props if "Device" in p or p == "internal"]
        vuln_props = [p.split(".")[-1] for p in new_props if "Vulnerability" in p or p in ["description", "name"]]

        # Construction dynamique des lignes Mermaid pour Device
        dev_mermaid_lines = [
            "        +String id",
            "        +String ip",
            "        +String type"
        ]
        for p in dev_props:
            dev_mermaid_lines.append(f"        +String {p} :: NOUVEAU ::")

        # Construction dynamique des lignes Mermaid pour Vulnerability
        vuln_mermaid_lines = [
            "        +String name",
            "        +Float cvssScore"
        ]
        for p in vuln_props:
            if p != "name": # 'name' existe déjà en V0
                vuln_mermaid_lines.append(f"        +String {p} :: NOUVEAU ::")

        # 2. Construction dynamique du bloc Requirement
        req_diagram_block = ""
        if "Requirement" in new_classes:
            req_diagram_block = (
                "    class Requirement {\n"
                "        +String reqId\n"
                "        +String description\n"
                "    }\n"
                "    Vulnerability \"*\" --> \"*\" Requirement : requiresCompliance :: NOUVELLE REL ::\n"
            )

        # 3. Assemblage des lignes du rapport
        lines = []
        lines.append("# 🛡️ Rapport d'Analyse d'Ingestion & Validation d'Ontologie\n")
        lines.append(f"**Statut d'Ingestion :** `{status}`\n")
        lines.append("---\n")
        lines.append("## 1. Bilan des Écarts Détectés\n")
        lines.append(f"* **Nouvelles Classes Identifiées :** `{list(new_classes) if new_classes else 'Aucune'}`")
        lines.append(f"* **Nouvelles Propriétés / Attributs :** `{list(new_props) if new_props else 'Aucune'}`\n")
        lines.append("---\n")
        lines.append("## 2. Comparaison Visuelle (Diff Mermaid)\n")
        lines.append("### Structure Actuelle (Avant / V0)")
        lines.append("```mermaid")
        lines.append("classDiagram")
        lines.append("    direction LR")
        lines.append("    class Device {")
        lines.append("        +String id")
        lines.append("        +String ip")
        lines.append("        +String type")
        lines.append("    }")
        lines.append("    class Software {")
        lines.append("        +String key")
        lines.append("        +String name")
        lines.append("        +String version")
        lines.append("    }")
        lines.append("    class Vulnerability {")
        lines.append("        +String name")
        lines.append("        +Float cvssScore")
        lines.append("    }")
        lines.append("    Device \"1\" --> \"*\" Software : HAS_SOFTWARE")
        lines.append("    Software \"1\" --> \"*\" Vulnerability : HAS_VULNERABILITY")
        lines.append("```\n")
        lines.append("### Structure Proposée (Après / V1)")
        lines.append("```mermaid")
        lines.append("classDiagram")
        lines.append("    direction LR")
        lines.append("    class Device {")
        lines.extend(dev_mermaid_lines)
        lines.append("    }")
        lines.append("    class Software {")
        lines.append("        +String key")
        lines.append("        +String name")
        lines.append("        +String version")
        lines.append("    }")
        lines.append("    class Vulnerability {")
        lines.extend(vuln_mermaid_lines)
        lines.append("    }")
        lines.append("    Device \"1\" --> \"*\" Software : HAS_SOFTWARE")
        lines.append("    Software \"1\" --> \"*\" Vulnerability : HAS_VULNERABILITY")
        if req_diagram_block:
            lines.append(req_diagram_block)
        lines.append("```\n")
        lines.append("---\n")
        lines.append("## 3. Snippet Turtle (`.ttl`) à intégrer dans `ontologie.ttl` \n")
        lines.append("```turtle")
        lines.append("# ==========================================")
        lines.append("# EXTENSION PROPOSÉE PHASE 1")
        lines.append("# ==========================================")
        for p in new_props:
            prop_name = p.split(".")[-1]
            lines.append(f"\ncyber:{prop_name} a owl:DatatypeProperty ;")
            lines.append(f'    rdfs:label "{prop_name}" ;')
            lines.append('    rdfs:range xsd:string .')
        lines.append("```\n")

        with open(output_report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"✅ Rapport régénéré avec succès dans : {output_report_path}")

if __name__ == "__main__":
    # Chemins relatifs par rapport à la racine du projet
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    ONTO_PATH = os.path.join(BASE_DIR, "/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase0-Cadrage/ONTOLOGIE/ontologie.ttl")
    JSON_PATH = os.path.join(BASE_DIR, "/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase1-Infrastructure/data/public/inventory-v2.json")
    RDF_PATH = os.path.join(BASE_DIR, "/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase1-Infrastructure/data/public/cve_data-v2.ttl")
    REPORT_PATH = os.path.join(BASE_DIR, "/data/SyncData/Projets/T2C_1/Workspace/03-Implementation/Phase1-Infrastructure/ONTOLOGIE/Rapport_Ecart_Ontologie.md")

    if os.path.exists(ONTO_PATH):
        guard = OntologyGuard(ONTO_PATH)
        
        classes_rdf, props_rdf = guard.analyze_rdf(RDF_PATH) if os.path.exists(RDF_PATH) else (set(), set())
        classes_json, props_json = guard.analyze_json_inventory(JSON_PATH) if os.path.exists(JSON_PATH) else (set(), set())

        all_new_classes = classes_rdf.union(classes_json)
        all_new_props = props_rdf.union(props_json)

        guard.generate_report(all_new_classes, all_new_props, REPORT_PATH)
    else:
        print(f"⚠️ Fichier ontologie de référence introuvable : {ONTO_PATH}")
