import json
import re
import datetime
import subprocess
import sys
from pathlib import Path
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, SKOS, RDFS

EX = Namespace("http://example.org/dkg/ontology#")

class Phase0Orchestrator:
    def __init__(self, phase0_dir: Path):
        self.root = phase0_dir
        
        # Chemins basés sur l'arborescence du projet
        self.dir_lexique = self.root / "1-Lexique"
        self.dir_ontologie = self.root / "2-Ontologie"
        self.dir_vault = self.root / "3-App_Referential_Vault"
        self.dir_pub_md = self.root / "4-App_publication_md"
        self.dir_graphe = self.root / "6-Graphe"
        self.dir_scripts = self.root / "7-ScriptsSpecifiques"

        # Structuration des répertoires de sortie
        (self.dir_pub_md / "Lexiques").mkdir(parents=True, exist_ok=True)
        (self.dir_pub_md / "Ontologies" / "par_domaines").mkdir(parents=True, exist_ok=True)
        self.dir_vault.mkdir(parents=True, exist_ok=True)
        self.dir_graphe.mkdir(parents=True, exist_ok=True)

    def process_all_inputs(self) -> Graph:
        """Consolide l'ensemble des inputs (Lexiques MD, RDF/TTL, JSON Inventory) dans le Vault."""
        print("⚡ [1/3] Consolidation globale des Inputs dans le Vault...")
        graph = Graph()
        graph.bind("skos", SKOS)
        graph.bind("ex", EX)
        graph.bind("rdfs", RDFS)

        # -------------------------------------------------------------
        # 1. Ingestion de TOUS les lexiques Markdown (Internes et Externes)
        # -------------------------------------------------------------
        md_files = list(self.dir_lexique.rglob("*.md"))
        for md_file in md_files:
            print(f"  └─ Ingestion Lexique MD : {md_file.relative_to(self.root)}")
            content = md_file.read_text(encoding="utf-8")
            blocks = re.split(r'\n(?=#{1,6}\s+)', content)
            
            for block in blocks:
                lines = [l.strip() for l in block.split('\n') if l.strip()]
                if not lines or not lines[0].startswith('#'):
                    continue
                
                term_label = re.sub(r'^#{1,6}\s+', '', lines[0]).strip()
                term_id = re.sub(r'[^a-zA-Z0-9_]', '_', term_label)
                concept_uri = EX[f"Concept_{term_id}"]
                
                graph.add((concept_uri, RDF.type, SKOS.Concept))
                graph.add((concept_uri, SKOS.prefLabel, Literal(term_label, lang="fr")))
                
                def_lines = []
                for line in lines[1:]:
                    if re.search(r'(synonyme|synonymes|altlabel|termes? alternatifs?)', line, re.IGNORECASE):
                        syn_text = re.sub(r'^[*|-]\s*', '', line)
                        syn_text = re.sub(r'^\*\*(Synonymes?|skos:altLabel|Termes? alternatifs?)\*\*\s*:\s*', '', syn_text, flags=re.IGNORECASE)
                        syn_text = re.sub(r'^(Synonymes?|skos:altLabel|Termes? alternatifs?)\s*:\s*', '', syn_text, flags=re.IGNORECASE)
                        for syn in syn_text.split(','):
                            if syn.strip():
                                graph.add((concept_uri, SKOS.altLabel, Literal(syn.strip(), lang="fr")))
                    
                    elif "**définition**" in line.lower() or "définition :" in line.lower() or line.startswith("- ") or line.startswith("* "):
                        cleaned_line = re.sub(r'^[*|-]\s*', '', line)
                        cleaned_line = re.sub(r'^\*\*Définition\*\*\s*:\s*', '', cleaned_line, flags=re.IGNORECASE)
                        cleaned_line = re.sub(r'^Définition\s*:\s*', '', cleaned_line, flags=re.IGNORECASE)
                        if cleaned_line.strip():
                            def_lines.append(cleaned_line.strip())
                
                if def_lines:
                    graph.add((concept_uri, SKOS.definition, Literal(" ".join(def_lines), lang="fr")))



        # -------------------------------------------------------------
        # 2. Ingestion des fichiers JSON (inventory.json, etc.)
        # -------------------------------------------------------------
        json_files = list(self.root.rglob("*.json"))
        for json_file in json_files:
            print(f"  └─ Ingestion Inventaire JSON : {json_file.relative_to(self.root)}")
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                
                # Fonction récursive pour extraire TOUS les objets équipements
                def extract_assets(obj):
                    extracted = []
                    if isinstance(obj, dict):
                        # Si l'objet ressemble à un équipement/hôte
                        if any(k in obj for k in ["hostname", "name", "ip", "ip_address", "mac", "device_type", "type"]):
                            extracted.append(obj)
                        for v in obj.values():
                            extracted.extend(extract_assets(v))
                    elif isinstance(obj, list):
                        for item in obj:
                            extracted.extend(extract_assets(item))
                    return extracted

                raw_assets = extract_assets(data)
                
                # Dédoublonnage basé sur le nom ou l'ID
                unique_assets = {}
                for idx, item in enumerate(raw_assets):
                    asset_id = item.get("hostname") or item.get("name") or item.get("id") or f"asset_{idx}"
                    unique_assets[str(asset_id)] = item

                for asset_id, item in unique_assets.items():
                    clean_id = re.sub(r'[^a-zA-Z0-9_]', '_', asset_id)
                    asset_uri = EX[f"Asset_{clean_id}"]
                    
                    # Déclaration de la classe Équipement
                    graph.add((asset_uri, RDF.type, EX.Equipment))
                    graph.add((asset_uri, RDFS.label, Literal(asset_id)))
                    
                    # Ajout de toutes les propriétés de l'équipement
                    for key, val in item.items():
                        clean_key = re.sub(r'[^a-zA-Z0-9_]', '_', key)
                        prop_uri = EX[clean_key]
                        
                        if isinstance(val, (str, int, float, bool)):
                            graph.add((asset_uri, prop_uri, Literal(val)))
                        elif isinstance(val, list):
                            for sub_val in val:
                                if isinstance(sub_val, (str, int, float, bool)):
                                    graph.add((asset_uri, prop_uri, Literal(sub_val)))

            except Exception as e:
                print(f"     ⚠️ Erreur lors du parsing de {json_file.name}: {e}")


        # -------------------------------------------------------------
        # 3. Ingestion des données RDF Externes (CVE_data.ttl, etc.)
        # -------------------------------------------------------------
        rdf_files = list(self.root.rglob("*.ttl"))
        for rdf_file in rdf_files:
            if "LEXIQUE_COMPATIBLE" not in rdf_file.name and "VAULT_CONSOLIDE" not in rdf_file.name:
                print(f"  └─ Fusion Triples RDF : {rdf_file.relative_to(self.root)}")
                try:
                    graph.parse(location=str(rdf_file), format="turtle")
                except Exception as e:
                    print(f"     ⚠️ Impossible de parser {rdf_file.name}: {e}")

        # Export Vault Unique Consolidé
        vault_file = self.dir_vault / "VAULT_CONSOLIDE.ttl"
        graph.serialize(destination=str(vault_file), format="turtle")
        print(f"✅ Vault consolidé mis à jour : {vault_file.name}")
        
        # Génération du Markdown et Reporting
        self._generate_publication_md(graph)
        self.generate_reporting(graph)
        return graph



    def _generate_publication_md(self, graph: Graph):
        """Génère la documentation du Lexique ET le fichier doc_ontologie_globale.md."""
        
        # -------------------------------------------------------------
        # 1. Génération de PUBLICATION_LEXIQUE_GLOBAL.md
        # -------------------------------------------------------------
        doc_pub = self.dir_pub_md / "Lexiques" / "PUBLICATION_LEXIQUE_GLOBAL.md"
        doc_lines = [
            "# 📖 Lexique Global d'Exposition (Phase 0)",
            "",
            "> *Document généré automatiquement à partir du Vault consolidé (Lexiques, Ontologies, CVE, Inventory).*",
            "",
            "---",
            ""
        ]
        
        terms = []
        for s, p, o in graph.triples((None, SKOS.prefLabel, None)):
            if getattr(o, 'language', None) == 'fr' or not getattr(o, 'language', None):
                label = str(o.value)
                defs = list(graph.objects(s, SKOS.definition))
                definition = str(defs[0].value) if defs else "Aucune définition renseignée."
                alts = [str(alt.value) for alt in graph.objects(s, SKOS.altLabel)]
                terms.append((label, definition, alts))
        
        terms.sort(key=lambda x: x[0].lower())

        for label, definition, alts in terms:
            doc_lines.append(f"## {label}")
            doc_lines.append("")
            doc_lines.append(f"**Définition :** {definition}")
            if alts:
                doc_lines.append("")
                doc_lines.append(f"**Synonymes :** {', '.join(alts)}")
            doc_lines.append("")
            doc_lines.append("---")
            doc_lines.append("")

        doc_pub.write_text("\n".join(doc_lines), encoding="utf-8")
        print(f"✅ Publication Lexique mise à jour : {doc_pub.relative_to(self.root)}")

        # -------------------------------------------------------------
        # 2. Génération de Ontologies/doc_ontologie_globale.md
        # -------------------------------------------------------------
        doc_onto = self.dir_pub_md / "Ontologies" / "doc_ontologie_globale.md"
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Requête SPARQL pour recenser les types/classes présentes
        classes_query = """
        SELECT DISTINCT ?type (COUNT(?s) AS ?count) WHERE {
            ?s a ?type .
        } GROUP BY ?type ORDER BY DESC(?count)
        """
        class_results = graph.query(classes_query)

        onto_lines = [
            "# 🏗️ Documentation de l'Ontologie Globale (Phase 0)",
            "",
            f"> *Généré automatiquement par l'Orchestrateur le {now_str}*",
            "",
            "---",
            "",
            "## 📌 Vue d'Ensemble des Classes RDF et Entités",
            "",
            "| Classe / Type URI | Nombre d'instances | Description |",
            "| :--- | :---: | :--- |"
        ]

        for row in class_results:
            cls_uri = str(row[0])
            count = row[1].value
            # Formate proprement le nom de la classe
            cls_name = cls_uri.split("#")[-1].split("/")[-1]
            onto_lines.append(f"| `{cls_name}` (`{cls_uri}`) | `{count}` | Instances identifiées dans le Vault |")

        onto_lines.extend([
            "",
            "---",
            "",
            "## 💻 Équipements & Inventaires Consolidés",
            "",
            "Liste des équipements et composants extraits des sources d'inventaire :",
            ""
        ])

        # Requête pour lister les équipements et leurs propriétés
        equipments_query = """
        PREFIX ex: <http://example.org/dkg/ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?eq ?label WHERE {
            ?eq a ex:Equipment .
            OPTIONAL { ?eq rdfs:label ?label }
        }
        """
        equipments = graph.query(equipments_query)

        for eq in equipments:
            eq_uri = eq[0]
            eq_name = str(eq[1]) if eq[1] else str(eq_uri).split("_")[-1]
            onto_lines.append(f"### 🖥️ Équipement : {eq_name}")
            onto_lines.append("")
            onto_lines.append("| Propriété | Valeur |")
            onto_lines.append("| :--- | :--- |")
            
            for p, o in graph.predicate_objects(eq_uri):
                p_name = str(p).split("#")[-1].split("/")[-1]
                if p_name not in ["type"]:
                    onto_lines.append(f"| **{p_name}** | `{o}` |")
            
            onto_lines.append("")

        doc_onto.write_text("\n".join(onto_lines), encoding="utf-8")
        print(f"✅ Documentation Ontologie générée : {doc_onto.relative_to(self.root)}")


    def generate_reporting(self, graph: Graph):
        """Génère un rapport détaillé des entités consolidées et l'enregistre dans 4-App_publication_md."""
        print("\n📊 ==================== RAPPORT DE CONSOLIDATION VAULT ====================")
        
        total_triples = len(graph)
        
        # 1. Décompte des concepts SKOS (Lexique)
        concepts_query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT (COUNT(DISTINCT ?s) AS ?count) WHERE {
            ?s a skos:Concept .
        }
        """
        concept_count = list(graph.query(concepts_query))[0][0]

        # 2. Décompte des synonymes (skos:altLabel)
        synonyms_query = """
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT (COUNT(?o) AS ?count) WHERE {
            ?s skos:altLabel ?o .
        }
        """
        synonym_count = list(graph.query(synonyms_query))[0][0]

        # 3. Décompte des CVEs (Vulnérabilités)
        cve_query = """
        SELECT (COUNT(DISTINCT ?s) AS ?count) WHERE {
            { ?s a <http://example.org/dkg/ontology#CVE> }
            UNION
            { ?s a <http://scap.nist.gov/schema/vulnerability/0.4#Vulnerability> }
            UNION
            { ?s ?p ?o . FILTER(regex(str(?s), "CVE-", "i")) }
        }
        """
        cve_count = list(graph.query(cve_query))[0][0]

        # 4. Décompte des Équipements / Composants d'Inventaire
        inventory_query = """
        PREFIX ex: <http://example.org/dkg/ontology#>
        SELECT (COUNT(DISTINCT ?s) AS ?count) WHERE {
            { ?s a ex:Equipment }
            UNION
            { ?s a ex:Asset }
            UNION
            { ?s a ex:Host }
            UNION
            { ?s a ex:Device }
        }
        """
        inventory_count = list(graph.query(inventory_query))[0][0]

        # Affichage Console
        print(f"  🔹 Total de triplets RDF dans le Vault : {total_triples}")
        print(f"  📖 Concepts (Lexique SKOS)            : {concept_count}")
        print(f"  🏷️  Synonymes (skos:altLabel)          : {synonym_count}")
        print(f"  🛡️  Vulnérabilités (CVEs)              : {cve_count}")
        print(f"  🖥️  Équipements (Inventaire)           : {inventory_count}")
        print("=========================================================================\n")

        # 5. Génération du fichier Markdown REPORTING_VAULT.md
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_file = self.dir_pub_md / "REPORTING_VAULT.md"
        
        md_content = [
            "# 📊 Rapport de Consolidation du Vault (Phase 0)",
            "",
            f"> *Généré automatiquement par l'Orchestrateur le {now_str}*",
            "",
            "---",
            "",
            "## 📈 Métriques Globales",
            "",
            "| Indicateur | Quantité | Description |",
            "| :--- | :---: | :--- |",
            f"| **Triplets RDF** | `{total_triples}` | Nombre total d'affirmations dans le Vault |",
            f"| **Concepts SKOS** | `{concept_count}` | Entrées de lexiques identifiées |",
            f"| **Synonymes** | `{synonym_count}` | Termes alternatifs (`skos:altLabel`) |",
            f"| **Vulnérabilités** | `{cve_count}` | Identifiants CVE / Fiches de vulnérabilité |",
            f"| **Équipements** | `{inventory_count}` | Actifs et composants d'inventaire |",
            "",
            "---",
            "",
            "## 📁 Fichiers Sources Consolidés",
            "",
            "* **Lexiques Markdown** : Restitués dans `4-App_publication_md/Lexiques/PUBLICATION_LEXIQUE_GLOBAL.md`",
            "* **Triples RDF Consolidés** : Stockés dans `3-App_Referential_Vault/VAULT_CONSOLIDE.ttl`",
            "* **Graphe Neo4j (Cypher)** : Exporté dans `6-Graphe/`",
            ""
        ]
        
        report_file.write_text("\n".join(md_content), encoding="utf-8")
        print(f"✅ Fichier de reporting généré : {report_file.relative_to(self.root)}")

    def generate_cypher_graph(self):
        """Exécute ttl_to_cypher.py sur le Vault consolidé."""
        print("⚡ [3/3] Conversion Vault Consolidé -> Cypher pour Neo4j...")
        
        ttl_input = self.dir_vault / "VAULT_CONSOLIDE.ttl"
        script_ttl_to_cypher = self.dir_scripts / "ttl_to_cypher.py"
        
        if not script_ttl_to_cypher.exists() or not ttl_input.exists():
            print("⚠️ Fichier source ou script manquant pour l'étape Cypher.")
            return

        try:
            cmd = [sys.executable, str(script_ttl_to_cypher), str(ttl_input)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("✅ Conversion Cypher effectuée.")

            today_str = datetime.datetime.now().strftime("%Y%m%d")
            generated_cyphers = list(self.dir_scripts.glob("*.cypher")) + list(self.root.glob("*.cypher")) + list(self.dir_vault.glob("*.cypher"))
            
            for cypher_file in generated_cyphers:
                target_file = self.dir_graphe / f"graphe-global_{today_str}.cypher"
                cypher_file.replace(target_file)
                print(f"✅ Graphe Cypher exporté : {target_file.relative_to(self.root)}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur ttl_to_cypher : {e.stderr or e.stdout}")

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    phase0_dir = script_dir.parent
    
    orchestrator = Phase0Orchestrator(phase0_dir)
    graph = orchestrator.process_all_inputs()
    orchestrator.generate_cypher_graph()
