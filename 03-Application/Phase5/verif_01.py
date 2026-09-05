from rdflib import Graph
from pathlib import Path

import sys

# Ajoute le dossier parent '03-Application' au sys.path
APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

# Import propre depuis config.py
from config import (
    TBOX_MASTER_PATH,
    ABOX_RED_PATH,
    ABOX_CTI_PATH,
    RULES_MASTER_PATH,
    ABOX_INFERED_PATH,
    MODELS_DIR,
    EMBEDDING_MODEL_DIR,
    MITM_SIMILARITY_THRESHOLD,
    DKG,
    RDFS,
    DOC_INFERED_MD_PATH
)


g = Graph()
g.parse(str(ABOX_RED_PATH), format="ttl")
g.parse(str(ABOX_CTI_PATH), format="ttl")

# Vérification des liens entre composants et vulnérabilités KEV
query = """
PREFIX dkg: <http://dkg.cybersec.org/schema#>
PREFIX dkg-cti: <http://dkg.cybersec.org/cti#>

SELECT ?asset ?component ?cve ?isKev WHERE {
    OPTIONAL { ?asset dkg:hostsComponent ?component . }
    OPTIONAL { ?component dkg:hasVulnerability ?cve . }
    OPTIONAL { ?cve dkg-cti:isCisaKevListed ?isKev . }
}
"""
for row in g.query(query):
    print(row)
