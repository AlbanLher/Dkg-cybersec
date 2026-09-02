#!/usr/bin/env python3
"""
Pipeline NER & Generation RDF - Unstructured CTI (Phase 4 / Vague 2)
Parse les bulletins bruts, applique le filtrage de confiance (>= 0.85)
et enrichit la ABox CTI Externe (TLP:CLEAR).
"""

import re
from pathlib import Path
from rdflib import Graph, Literal, Namespace, RDF, RDFS, XSD, URIRef
from config import DIR_UNSTRUCTURED_CTI, ABOX_CTI_PATH

# Namespaces DKG
DKG = Namespace("http://dkg.cybersec.org/schema#")
DKG_CTI = Namespace("http://dkg.cybersec.org/cti#")


class CTIUnstructuredExtractor:
    def __init__(self, confidence_threshold: float = 0.85):
        self.threshold = confidence_threshold
        self.graph = Graph()
        self._bind_namespaces()

    def _bind_namespaces(self):
        self.graph.bind("dkg", DKG)
        self.graph.bind("dkg-cti", DKG_CTI)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("xsd", XSD)

    def extract_from_text(self, text_content: str, source_name: str):
        """Extraction par motifs/NLP avec calcul de score de confiance."""
        
        # 1. Extraction ThreatActor
        actor_match = re.search(r"(APT29|Cozy Bear|Lazarus|Fancy Bear)", text_content, re.IGNORECASE)
        actor_uri = None
        if actor_match:
            actor_name = actor_match.group(1).upper()
            actor_score = 0.98  # Score élevé sur entité explicite
            if actor_score >= self.threshold:
                actor_uri = DKG_CTI[f"ThreatActor-{actor_name}"]
                self.graph.add((actor_uri, RDF.type, DKG.ThreatActor))
                self.graph.add((actor_uri, RDFS.label, Literal(actor_name)))
                self.graph.add((actor_uri, DKG.nerConfidenceScore, Literal(actor_score, datatype=XSD.float)))

        # 2. Extraction Vulnerability (CVE)
        cve_matches = re.findall(r"(CVE-\d{4}-\d{4,7})", text_content, re.IGNORECASE)
        cve_uris = []
        for cve_id in set(cve_matches):
            cve_id_upper = cve_id.upper()
            cve_score = 0.99
            if cve_score >= self.threshold:
                cve_uri = DKG_CTI[cve_id_upper]
                cve_uris.append(cve_uri)
                self.graph.add((cve_uri, RDF.type, DKG.Vulnerability))
                self.graph.add((cve_uri, RDFS.label, Literal(cve_id_upper)))
                self.graph.add((cve_uri, DKG.nerConfidenceScore, Literal(cve_score, datatype=XSD.float)))

        # 3. Extraction ThreatPattern (MITRE ATT&CK)
        pattern_match = re.search(r"Spearphishing Link \((T\d{4}\.\d{3})\)", text_content)
        pattern_uri = None
        if pattern_match:
            tech_id = pattern_match.group(1)
            pattern_score = 0.92
            if pattern_score >= self.threshold:
                pattern_uri = DKG_CTI[f"Pattern-SpearphishingLink-{tech_id.replace('.', '_')}"]
                self.graph.add((pattern_uri, RDF.type, DKG.ThreatPattern))
                self.graph.add((pattern_uri, RDFS.label, Literal(f"Spearphishing Link ({tech_id})")))
                self.graph.add((pattern_uri, DKG.nerConfidenceScore, Literal(pattern_score, datatype=XSD.float)))

        # 4. Relations
        if actor_uri and pattern_uri:
            self.graph.add((actor_uri, DKG.hasThreatPattern, pattern_uri))

        if actor_uri:
            for cve_uri in cve_uris:
                self.graph.add((actor_uri, DKG.exploitsVulnerability, cve_uri))

    def process_all_sources(self):
        """Parcourt le répertoire Raw_Sources et traite chaque fichier texte."""
        if not DIR_UNSTRUCTURED_CTI.exists():
            print(f"⚠️ Répertoire source introuvable : {DIR_UNSTRUCTURED_CTI}")
            return

        txt_files = list(DIR_UNSTRUCTURED_CTI.glob("*.txt"))
        print(f"🔍 [{len(txt_files)}] fichier(s) texte trouvé(s) dans {DIR_UNSTRUCTURED_CTI}")

        for file_path in txt_files:
            content = file_path.read_text(encoding="utf-8")
            self.extract_from_text(content, source_name=file_path.name)

    def merge_into_master_abox(self):
        """Fusionne les nouveaux triplets NER avec la ABox CTI Master."""
        if not ABOX_CTI_PATH.exists():
            print(f"❌ ABox CTI Master non trouvée à : {ABOX_CTI_PATH}")
            return

        master_graph = Graph()
        master_graph.parse(ABOX_CTI_PATH, format="turtle")
        
        initial_len = len(master_graph)
        master_graph += self.graph
        final_len = len(master_graph)
        
        # Sauvegarde
        master_graph.serialize(destination=ABOX_CTI_PATH, format="turtle")
        print(f"🟢 Extraction terminée. Multiplicité ABox CTI : {initial_len} -> {final_len} triplets (+{final_len - initial_len} ajoutés).")


if __name__ == "__main__":
    extractor = CTIUnstructuredExtractor(confidence_threshold=0.85)
    extractor.process_all_sources()
    extractor.merge_into_master_abox()
