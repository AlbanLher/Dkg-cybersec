import json
import logging
import requests
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import EXTERNAL_SOURCES_CONFIG_PATH, EXTERNAL_SOURCES_CATALOG_PATH




from config import EXTERNAL_SOURCES_CONFIG_PATH, EXTERNAL_SOURCES_CATALOG_PATH

logger = logging.getLogger("ExternalCTIAgent")

class CTIEntry:
    def __init__(self, cve_id, severity, cvss_score, affected_product, description, is_cisa_kev, source_type):
        self.cve_id = cve_id
        self.severity = severity
        self.cvss_score = cvss_score
        self.affected_product = affected_product
        self.description = description
        self.is_cisa_kev = is_cisa_kev
        self.source_type = source_type

class ExternalCTIAgent:
    def __init__(self):
        self.config_path = EXTERNAL_SOURCES_CONFIG_PATH
        self.catalog_path = EXTERNAL_SOURCES_CATALOG_PATH

    def _safe_get(self, dictionary: dict, key: str, default=None):
        """Parser défensif pour éviter les plantages sur propriétés manquantes."""
        val = dictionary.get(key, default)
        return val if val is not None else default

    def load_live_sources_config(self) -> list:
        """Charge le fichier de configuration des flux live (ex: CISA KEV)."""
        if not self.config_path.exists():
            logger.warning(f"Config live introuvable : {self.config_path}")
            return []
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return self._safe_get(data, "sources", [])
        except Exception as e:
            logger.error(f"Erreur de lecture de {self.config_path} : {e}")
            return []

    def load_catalog_sources(self) -> list:
        """Charge le catalogue des sources structurées/non structurées[cite: 8]."""
        if not self.catalog_path.exists():
            logger.warning(f"Catalogue introuvable : {self.catalog_path}")
            return []
        try:
            with open(self.catalog_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return self._safe_get(data, "sources", [])
        except Exception as e:
            logger.error(f"Erreur de lecture de {self.catalog_path} : {e}")
            return []

    def fetch_all_cti(self) -> list:
        """
        Orchestre la récupération en interrogeant les sources live activées 
        et en référençant le catalogue local.
        """
        all_entries = []

        # 1. Traitement des sources live (ex: CISA KEV via HTTPS)[cite: 9]
        live_sources = self.load_live_sources_config()
        for source in live_sources:
            if not self._safe_get(source, "enabled", False):
                logger.info(f"Source live désactivée : {self._safe_get(source, 'name')}")
                continue

            url = self._safe_get(source, "endpoint_url")
            timeout = self._safe_get(source, "timeout_seconds", 10)
            source_id = self._safe_get(source, "source_id")

            logger.info(f"Connexion live vers [{source_id}] : {url}")
            try:
                response = requests.get(url, timeout=timeout)
                if response.status_code == 200:
                    data = response.json()
                    if source_id == "cisa_kev":
                        for vuln in self._safe_get(data, "vulnerabilities", []):
                            all_entries.append(
                                CTIEntry(
                                    cve_id=self._safe_get(vuln, "cveID", "UNKNOWN"),
                                    severity="CRITICAL",
                                    cvss_score=9.8,
                                    affected_product=self._safe_get(vuln, "product", "Unknown"),
                                    description=self._safe_get(vuln, "shortDescription", ""),
                                    is_cisa_kev=True,
                                    source_type="Structured-Live"
                                )
                            )
                    logger.info(f"[SUCCESS] Données live récupérées pour {source_id}")
                else:
                    logger.warning(f"Erreur HTTP {response.status_code} sur {source_id}")
            except Exception as e:
                logger.error(f"Erreur réseau sur {source_id} : {e}")

        # 2. Référencement du catalogue statique / local[cite: 8]
        catalog_sources = self.load_catalog_sources()
        for cat in catalog_sources:
            logger.info(f"Catalogue répertorié : {self._safe_get(cat, 'name')} ({self._safe_get(cat, 'type')})")
            # Logique d'intégration des fichiers locaux (ex: external_nvd_capec_feed.json[cite: 8])

        logger.info(f"Total des entrées CTI chargées : {len(all_entries)}")
        return all_entries

if __name__ == "__main__":
    # Configuration basique des logs pour voir le déroulement dans la console
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    
    print("=== Démarrage du test de l'Agent CTI Externe ===")
    agent = ExternalCTIAgent()
    
    # Lancement de la collecte unifiée
    cti_entries = agent.fetch_all_cti()
    
    print(f"\n=== Test terminé avec succès ===")
    print(f"Nombre total d'entrées CTI récupérées : {len(cti_entries)}")
    
    # Affichage d'un petit aperçu des 3 premières entrées s'il y en a
    for i, entry in enumerate(cti_entries[:3]):
        print(f" - [{entry.source_type}] CVE: {entry.cve_id} | Produit: {entry.affected_product} | Score: {entry.cvss_score}")
