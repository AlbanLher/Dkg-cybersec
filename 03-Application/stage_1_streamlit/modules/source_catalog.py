# [EXG-MODULE] Catalogue des sources CTI (Structurées / Non Structurées)
SOURCES_CATALOG = [
    {
        "source_id": "SRC_NVD_API",
        "name": "NVD National Vulnerability Database",
        "type": "Structured",
        "format": "JSON / API REST",
        "status": "Actif",
        "description": "Catalogue officiel des CVE (Structuré)."
    },
    {
        "source_id": "SRC_GITHUB_ADVISORY",
        "name": "GitHub Security Advisories",
        "type": "Structured",
        "format": "GraphQL / JSON",
        "status": "Actif",
        "description": "Vulnérabilités logicielles et écosystèmes open-source."
    },
    {
        "source_id": "SRC_VENDOR_RSS",
        "name": "Avis de Sécurité Éditeurs (Blogs & RSS)",
        "type": "Unstructured",
        "format": "Flux RSS / HTML text",
        "description": "Bulletins de sécurité non structurés publiés par les éditeurs."
    },
    {
        "source_id": "SRC_CERT_FR_FEED",
        "name": "Bulletins d'alerte CERT-FR",
        "type": "Unstructured",
        "format": "Flux ATOM / Texte brut",
        "description": "Avis et recommandations institutionnels français."
    }
]
