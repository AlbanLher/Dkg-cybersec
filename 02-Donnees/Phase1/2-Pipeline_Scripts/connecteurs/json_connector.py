import json
import re
from pathlib import Path
from rdflib import Graph, Literal, RDF, RDFS, XSD, URIRef
from connectors.base_connector import BaseConnector, EX, INST

class JSONInventoryConnector(BaseConnector):
    SOFTWARE_KEYS = {"software", "softwares", "applications", "apps", "installed_software", "os"}

    def extract_to_abox(self, graph: Graph) -> Graph:
        if not self.file_path.exists():
            print(f"⚠️ Fichier introuvable : {self.file_path}")
            return graph

        data = json.loads(self.file_path.read_text(encoding="utf-8"))
        self._process_node(data, graph)
        return graph

    def _process_node(self, obj, graph: Graph):
        if isinstance(obj, dict):
            # Détection d'un équipement (presence de clés caractéristiques)
            if any(k in obj for k in ["hostname", "ip", "ip_address", "mac", "device_type"]) or "name" in obj:
                self._extract_equipment(obj, graph)
            else:
                for v in obj.values():
                    self._process_node(v, graph)
        elif isinstance(obj, list):
            for item in obj:
                self._process_node(item, graph)

    def _extract_equipment(self, item: dict, graph: Graph):
        asset_id = item.get("hostname") or item.get("name") or item.get("id") or "unknown_asset"
        clean_asset_id = re.sub(r'[^a-zA-Z0-9_]', '_', str(asset_id))
        equipment_uri = INST[f"Equipment_{clean_asset_id}"]

        # Typage et Label de l'équipement
        graph.add((equipment_uri, RDF.type, EX.Equipment))
        graph.add((equipment_uri, RDFS.label, Literal(str(asset_id))))

        for key, val in item.items():
            clean_key = re.sub(r'[^a-zA-Z0-9_]', '_', key)

            # Extraction des logiciels associés (ex:hasSoftware)
            if key.lower() in self.SOFTWARE_KEYS:
                soft_list = val if isinstance(val, list) else [val]
                for idx, soft in enumerate(soft_list):
                    self._extract_software(soft, equipment_uri, clean_asset_id, idx, graph)

            # Attributs scalaires de l'équipement (IP, MAC, OS, etc.)
            elif isinstance(val, (str, int, float, bool)):
                prop_uri = EX[clean_key]
                graph.add((equipment_uri, prop_uri, Literal(val)))

    def _extract_software(self, soft, equipment_uri: URIRef, eq_id: str, idx: int, graph: Graph):
        if isinstance(soft, dict):
            soft_name = soft.get("name") or soft.get("id") or f"{eq_id}_soft_{idx}"
            clean_soft_id = re.sub(r'[^a-zA-Z0-9_]', '_', str(soft_name))
            software_uri = INST[f"Software_{clean_soft_id}"]

            graph.add((software_uri, RDF.type, EX.Software))
            graph.add((software_uri, RDFS.label, Literal(str(soft_name))))
            graph.add((equipment_uri, EX.hasSoftware, software_uri))

            for s_key, s_val in soft.items():
                if isinstance(s_val, (str, int, float, bool)):
                    graph.add((software_uri, EX[re.sub(r'[^a-zA-Z0-9_]', '_', s_key)], Literal(s_val)))

        elif isinstance(soft, str):
            clean_soft_id = re.sub(r'[^a-zA-Z0-9_]', '_', soft)
            software_uri = INST[f"Software_{clean_soft_id}"]

            graph.add((software_uri, RDF.type, EX.Software))
            graph.add((software_uri, RDFS.label, Literal(soft)))
            graph.add((equipment_uri, EX.hasSoftware, software_uri))
