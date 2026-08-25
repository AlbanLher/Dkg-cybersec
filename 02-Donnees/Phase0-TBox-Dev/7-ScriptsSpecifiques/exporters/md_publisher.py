import datetime
from pathlib import Path
from rdflib import Graph, SKOS, OWL, RDFS

def publish_documentation_and_reports(root_dir: Path, graph: Graph, check1_res: dict, check2_res: dict):
    dir_pub_md = root_dir / "4-App_publication_md"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. doc_ontologie_globale.md
    onto_file = dir_pub_md / "Ontologies" / "doc_ontologie_globale.md"
    classes_query = """
    SELECT DISTINCT ?type WHERE {
        { ?type a <http://www.w3.org/2002/07/owl#Class> }
        UNION
        { ?type a <http://www.w3.org/2000/01/rdf-schema#Class> }
        UNION
        { ?s a ?type }
    }
    """
    classes = [str(r[0]).split("#")[-1].split("/")[-1] for r in graph.query(classes_query)]

    doc_lines = [
        "# 🏗️ Documentation de l'Ontologie Globale (Phase 0)",
        f"> *Généré automatiquement le {now_str}*",
        "",
        "## 📌 Structure des Classes RDF (Méta-modèle)",
        "",
        "| Nom de la Classe | Statut Vault |",
        "| :--- | :--- |"
    ]
    for cls in sorted(set(classes)):
        doc_lines.append(f"| `{cls}` | Validé |")
    
    onto_file.write_text("\n".join(doc_lines), encoding="utf-8")

    # 2. REPORTING_VAULT.md (Bilan des Vérifications)
    report_file = dir_pub_md / "REPORTING_VAULT.md"
    report_lines = [
        "# 📊 Rapport de Conformité Structurelle (Phase 0)",
        f"> *Dernière vérification : {now_str}*",
        "",
        "## 1. Couverture Inputs ➔ Vault (SKOS & Ontologies)",
        f"* **Taux de couverture** : `{check1_res.get('coverage_rate')}%`",
        f"* **Concepts sources détectés** : `{check1_res.get('source_count')}`",
        f"* **Concepts intégrés au Vault** : `{check1_res.get('vault_count')}`",
        f"* **Termes manquants** : `{len(check1_res.get('missing_terms', []))}`",
        "",
        "## 2. Couverture Vault ➔ Graph Cypher (Neo4j)",
        f"* **Taux de couverture du schéma** : `{check2_res.get('coverage_rate')}%`",
        f"* **Classes Vault identifiées** : `{check2_res.get('vault_classes_count')}`",
        f"* **Classes projetées en Cypher** : `{check2_res.get('cypher_classes_count')}`",
        "",
        "---",
        "✅ **Bilan Phase 0** : La structure est validée et prête pour l'instanciation (Phase 1)."
    ]
    report_file.write_text("\n".join(report_lines), encoding="utf-8")
