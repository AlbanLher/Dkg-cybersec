#!/usr/bin/env python3
"""
Script d'ingestion et de mise en cache des données externes (NVD/CAPEC).
Classification : TLP:CLEAR
Emplacement Cache : 12-Donnees/Caches_Externes/TLP_CLEAR_NVD_CAPEC/
"""

import json
from pathlib import Path
from rdflib import Graph, Namespace

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CACHE_DIR = BASE_DIR / "12-Donnees" / "3-Caches_Externes" / "TLP_CLEAR_NVD_CAPEC"
CACHE_FILE = CACHE_DIR / "nvd_capec_mock_cache.json"
ABOX_INIT_FILE = BASE_DIR / "12-Donnees" / "2-Snapshots_Phases" / "Phase_2_ABox_init" / "ABox_Cybersec_init.ttl"

DKG = Namespace("http://dkg.cybersec.org/tbox#")
DKG_INST = Namespace("http://dkg.cybersec.org/abox#")

MOCK_NVD_CAPEC_DATA = {
    "CVE-2021-44228": {
        "description": "Apache Log4j2 JNDI features do not protect against attacker controlled LDAP and other JNDI related endpoints.",
        "cvss_score": 10.0,
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
        "severity": "CRITICAL",
        "cwe_id": "CWE-502",
        "capec_id": "CAPEC-586",
        "capec_title": "Object Injection",
        "capec_description": "An attacker injects malicious objects into an application to execute arbitrary code."
    },
    "CVE-2023-4863": {
        "description": "Heap buffer overflow in WebP in Google Chrome prior to 116.0.5845.187 allowed a remote attacker to perform an arbitrary code execution.",
        "cvss_score": 8.8,
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H",
        "severity": "HIGH",
        "cwe_id": "CWE-119",
        "capec_id": "CAPEC-100",
        "capec_title": "Overflow Buffers",
        "capec_description": "Attacker targets a buffer overflow vulnerability to execute shellcode or cause Denial of Service."
    }
}


def ensure_cache_exists() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    if not CACHE_FILE.exists():
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(MOCK_NVD_CAPEC_DATA, f, indent=4, ensure_ascii=False)
    return CACHE_FILE


def fetch_enrichment_data() -> dict:
    cache_path = ensure_cache_exists()
    with open(cache_path, "r", encoding="utf-8") as f:
        return json.load(f)


def ingest_external_data() -> Graph:
    g = Graph()
    if ABOX_INIT_FILE.exists():
        g.parse(str(ABOX_INIT_FILE), format="turtle")
    return g
