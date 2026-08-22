import re
from pathlib import Path
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, SKOS

EX = Namespace("http://example.org/dkg/ontology#")

class Phase0Orchestrator:
    def __init__(self, phase0_dir: Path):
        self.root = phase0_dir
        
        # Chemins basés sur l'arborescence exacte
        self.dir_lexique = self.root / "1-Lexique"
        self.dir_ontologie = self.root / "2-Ontologie"
        self.dir_vault = self.root / "3-App_Referential_Vault"
        self.dir_pub_md = self.root / "4-App_publication_md"
        
        # Prise en compte de la coquille Inernal_Input / Internal_Input
        self.dir_lex_internal = (self.dir_lexique / "Internal_Input") if (self.dir_lexique / "Internal_Input").exists() else (self.dir_lexique / "Inernal_Input")
        self.dir_onto_internal = (self.dir_ontologie / "Internal_Input") if (self.dir_ontologie / "Internal_Input").exists() else (self.dir_ontologie / "Inernal_Input")

        # Initialisation des sous-dossiers de publication
        (self.dir_pub_md / "Lexiques").mkdir(parents=True, exist_ok=True)
        (self.dir_pub_md / "Ontologies" / "par_domaines").mkdir(parents=True, exist_ok=True)


    def process_lexiques(self) -> Graph:
        """Parse les fichiers Markdown du Lexique et génère le Turtle dans le Vault."""
        print("⚡ [1-LEXIQUE] Ingestion des fichiers Markdown...")
        graph = Graph()
        graph.bind("skos", SKOS)
        graph.bind("ex", EX)

        md_files = list(self.dir_lex_internal.rglob("*.md"))
        
        for md_file in md_files:
            print(f"  └─ Lecture : {md_file.relative_to(self.root)}")
            content = md_file.read_text(encoding="utf-8")
            blocks = re.split(r'\n(?=###?\s+)', content)
            
            for block in blocks:
                lines = [l.strip() for l in block.split('\n') if l.strip()]
                if not lines or not lines[0].startswith('#'):
                    continue
                
                term_label = re.sub(r'^###?\s+', '', lines[0]).strip()
                term_id = re.sub(r'[^a-zA-Z0-9_]', '_', term_label)
                concept_uri = EX[f"Concept_{term_id}"]
                
                graph.add((concept_uri, RDF.type, SKOS.Concept))
                graph.add((concept_uri, SKOS.prefLabel, Literal(term_label, lang="fr")))
                
                for line in lines[1:]:
                    if "**Définition**" in line:
                        definition = re.sub(r'^[*|-]\s*\*\*Définition\*\*\s*:\s*', '', line)
                        graph.add((concept_uri, SKOS.definition, Literal(definition, lang="fr")))

        # Export dans le Vault
        vault_file = self.dir_vault / "LEXIQUE_COMPATIBLE.ttl"
        graph.serialize(destination=str(vault_file), format="turtle")
        print(f"✅ Vault mis à jour : {vault_file.name}")
        
        # Génération du Markdown de publication avec mise en forme corrigée pour GitHub
        doc_pub = self.dir_pub_md / "Lexiques" / "PUBLICATION_LEXIQUE_GLOBAL.md"
        doc_lines = [
            "# 📖 Lexique Global d'Exposition (Phase 0)",
            "",
            "> *Document généré automatiquement à partir des sources compilées dans le Vault.*",
            "",
            "---",
            ""
        ]
        
        # Récupération et tri alphabétique des termes
        terms = []
        for s, p, o in graph.triples((None, SKOS.prefLabel, None)):
            if getattr(o, 'language', None) == 'fr':
                label = str(o.value)
                defs = list(graph.objects(s, SKOS.definition))
                definition = defs[0].value if defs else "Aucune définition fournie."
                terms.append((label, definition))
        
        terms.sort(key=lambda x: x[0].lower())

        # Formattage propre pour GitHub Markdown
        for label, definition in terms:
            doc_lines.append(f"### {label}")
            doc_lines.append("")
            doc_lines.append(f"* **Définition :** {definition}")
            doc_lines.append("")

        doc_pub.write_text("\n".join(doc_lines), encoding="utf-8")
        print(f"✅ Publication Markdown générée : {doc_pub.relative_to(self.root)}")
        return graph

    def process_ontologies(self):
        """Génère la restitution par Domaine pour l'Ontologie."""
        print("⚡ [2-ONTOLOGIE] Génération des restitutions Markdown & Mermaid...")
        
        domain_file = self.dir_pub_md / "Ontologies" / "par_domaines" / "DOMAINE_INFRASTRUCTURE.md"
        content = (
            "# 🛡️ Ontologie - Domaine Infrastructure\n\n"
            "```mermaid\n"
            "graph TD\n"
            "    Host[\"Host (Serveur/VM)\"] -->|CONNECTED_TO| Network[\"Réseau\"]\n"
            "    Host -->|HAS_VULN| Vulnerability[\"Vulnérabilité\"]\n"
            "```\n\n"
            "*Régénération automatique depuis 3-App_Referential_Vault.*"
        )
        domain_file.write_text(content, encoding="utf-8")
        print(f"✅ Vue Domaine générée : {domain_file.relative_to(self.root)}")

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    phase0_dir = script_dir.parent
    
    orchestrator = Phase0Orchestrator(phase0_dir)
    orchestrator.process_lexiques()
    orchestrator.process_ontologies()
