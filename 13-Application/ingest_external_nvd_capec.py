#!/usr/bin/env python3
"""
Ingesteur de Référentiels Externes (Phase 3).
S'appuie sur l'ABox initiale (12-Donnees/ABox_init/) et prépare l'enrichissement
NVD, CAPEC et le marquage TLP.
"""

import json
from pathlib import Path
from rdflib import Graph, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent
ABOX_INIT_FILE = BASE_DIR / "12-Donnees" / "ABox_init" / "ABox_Cybersec.ttl"
CACHE_DIR = BASE_DIR / "12-Donnees" / "External_Cache"
CACHE_FILE = CACHE_DIR / "nvd_capec_mock_cache.json"

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_INST = Namespace("http://dkg.cybersec.org/abox#")

MOCK_EXTERNAL_DATA = {
    "CVE-2021-44228": {
        "description": "Apache Log4j2 JNDI features do not protect against attacker controlled LDAP endpoints.",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "severity": "CRITICAL"
    },
    "CVE-2021-23017": {
        "description": "1-byte memory write overflow in Nginx resolver allows denial of service or code execution.",
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
        "severity": "HIGH"
    },
    "CWE-502": {
        "capec_id": "CAPEC-112",
        "capec_title": "Command Injection",
        "capec_description": "Deserialization of Untrusted Data leading to arbitrary command execution."
    },
    "CWE-193": {
        "capec_id": "CAPEC-14",
        "capec_title": "Far Side Off-by-One Buffer Overflow",
        "capec_description": "Off-by-one calculation error leading to memory corruption."
    }
}


def ensure_cache():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if not CACHE_FILE.exists():
        CACHE_FILE.write_text(json.dumps(MOCK_EXTERNAL_DATA, indent=4), encoding="utf-8")


def fetch_enrichment_data() -> dict:
    ensure_cache()
    return json.loads(CACHE_FILE.read_text(encoding="utf-8"))


def ingest_external_data() -> Graph:
    assert ABOX_INIT_FILE.exists(), f"❌ ABox initiale introuvable dans {ABOX_INIT_FILE}."
    g = Graph()
    g.parse(ABOX_INIT_FILE, format="turtle")
    g.bind("dkg", DKG)
    g.bind("dkg-inst", DKG_INST)
    return g


if __name__ == "__main__":
    graph = ingest_external_data()
    cache = fetch_enrichment_data()
    print(f"✅ Ingestion Phase 3 initialisée ({len(graph)} triplets issus de ABox_init).")
