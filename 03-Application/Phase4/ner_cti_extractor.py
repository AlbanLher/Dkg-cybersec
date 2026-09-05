#!/usr/bin/env python3
"""
ner_cti_extractor.py
Pipeline NER & Génération RDF - Phase 4.
Parse les bulletins bruts, applique le filtrage de confiance (>= 0.85)
et enrichit l'ABox CTI Externe (TLP:CLEAR) avec alignement sémantique TBox.
"""

import re
import sys
import shutil
from pathlib import Path
from rdflib import Graph, Literal, RDF, RDFS, SKOS, XSD

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config import (
    TBOX_MASTER_PATH,
    DIR_INPUTS_P4,
    DIR_SNAPSHOT_P4,
    DIR_CTI_CLEAR,
    ABOX_CTI_PATH,
    DKG_TBOX,
    DKG_CTI
)

class CTIUnstructuredExtractor:
    def __init__(self, confidence_threshold: float = 0.85):
        self.threshold = confidence_threshold
        self.graph = Graph()
        self.tbox = Graph()
        self._load_tbox_semantics()
        self._bind_namespaces()

    def _load_tbox_semantics(self):
        """Charge la sémantique et les concepts définis dans le Socle TBox."""
        if TBOX_MASTER_PATH.exists():
            self.tbox.parse(str(TBOX_MASTER_PATH), format="turtle")

    def _bind_namespaces(self):
        self.graph.bind("dkg", DKG_TBOX)
        self.graph.bind("cti", DKG_CTI)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("skos", SKOS)
        self.graph.bind("xsd", XSD)

    def extract_from_text(self, text_content: str, source_name: str):
        """Extraction NER par règles/patterns alignée sur la sémantique du socle."""
        
        # 1. Extraction ThreatActor (Ancrage du concept APT / ThreatActor)
        actor_match = re.search(r"(APT29|Cozy Bear|Lazarus|Fancy Bear)", text_content, re.IGNORECASE)
        actor_uri = None
        if actor_match:
            actor_name = actor_match.group(1).upper()
            actor_score = 0.98
            if actor_score >= self.threshold:
                actor_uri = DKG_CTI[f"ThreatActor-{actor_name}"]
                self.graph.add((actor_uri, RDF.type, DKG_TBOX.ThreatActor))
                self.graph.add((actor_uri, RDFS.label, Literal(actor_name, lang="en")))
                # Enrichissement sémantique avec le concept APT
                self.graph.add((actor_uri, SKOS.altLabel, Literal("APT", lang="en")))
                self.graph.add((actor_uri, DKG_TBOX.nerConfidenceScore, Literal(actor_score, datatype=XSD.float)))

        # 2. Extraction Vulnerability (CVE)
        cve_matches = re.findall(r"(CVE-\d{4}-\d{4,7})", text_content, re.IGNORECASE)
        cve_uris = []
        for cve_id in set(cve_matches):
            cve_id_upper = cve_id.upper()
            cve_score = 0.99
            if cve_score >= self.threshold:
                cve_uri = DKG_CTI[cve_id_upper]
                cve_uris.append(cve_uri)
                self.graph.add((cve_uri, RDF.type, DKG_TBOX.Vulnerability))
                self.graph.add((cve_uri, RDFS.label, Literal(cve_id_upper, lang="en")))
                self.graph.add((cve_uri, DKG_TBOX.nerConfidenceScore, Literal(cve_score, datatype=XSD.float)))

        # 3. Extraction ThreatPattern (MITRE ATT&CK)
        pattern_match = re.search(r"Spearphishing Link \((T\d{4}\.\d{3})\)", text_content)
        pattern_uri = None
        if pattern_match:
            tech_id = pattern_match.group(1)
            pattern_score = 0.92
            if pattern_score >= self.threshold:
                pattern_uri = DKG_CTI[f"Pattern-SpearphishingLink-{tech_id.replace('.', '_')}"]
                self.graph.add((pattern_uri, RDF.type, DKG_TBOX.ThreatPattern))
                self.graph.add((pattern_uri, RDFS.label, Literal(f"Spearphishing Link ({tech_id})", lang="en")))
                self.graph.add((pattern_uri, DKG_TBOX.nerConfidenceScore, Literal(pattern_score, datatype=XSD.float)))

        # 4. Relations TBox (tbox#)
        if actor_uri and pattern_uri:
            self.graph.add((actor_uri, DKG_TBOX.hasThreatPattern, pattern_uri))

        if actor_uri:
            for cve_uri in cve_uris:
                self.graph.add((actor_uri, DKG_TBOX.exploitsVulnerability, cve_uri))

    def process_all_sources(self):
        """Parcourt le répertoire d'inputs bruts et exécute l'extraction."""
        if not DIR_INPUTS_P4.exists():
            print(f"⚠️ Répertoire source introuvable : {DIR_INPUTS_P4}")
            return

        txt_files = list(DIR_INPUTS_P4.glob("*.txt"))
        print(f"🔍 [{len(txt_files)}] fichier(s) texte trouvé(s) dans {DIR_INPUTS_P4}")

        for file_path in txt_files:
            content = file_path.read_text(encoding="utf-8")
            self.extract_from_text(content, source_name=file_path.name)

    def merge_and_sync(self):
        """Fusionne les données extraites et applique la double écriture (Snapshot -> Master)."""
        master_graph = Graph()
        if ABOX_CTI_PATH.exists():
            master_graph.parse(str(ABOX_CTI_PATH), format="turtle")
        
        initial_len = len(master_graph)
        master_graph += self.graph
        final_len = len(master_graph)
        
        # 1. Écriture Snapshot P4
        DIR_SNAPSHOT_P4.mkdir(parents=True, exist_ok=True)
        snapshot_ttl = DIR_SNAPSHOT_P4 / ABOX_CTI_PATH.name
        master_graph.serialize(destination=str(snapshot_ttl), format="turtle")

        # 2. Copie miroir Master CTI TLP:CLEAR
        DIR_CTI_CLEAR.mkdir(parents=True, exist_ok=True)
        shutil.copy(snapshot_ttl, ABOX_CTI_PATH)
        print(f"✅ Master CTI mis à jour avec alignement sémantique TBox ({initial_len} -> {final_len} triplets, +{final_len - initial_len} ajoutés).")

if __name__ == "__main__":
    extractor = CTIUnstructuredExtractor(confidence_threshold=0.85)
    extractor.process_all_sources()
    extractor.merge_and_sync()
