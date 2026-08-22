import os
import re
from pathlib import Path
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, SKOS, DCTERMS

EX = Namespace("http://example.org/dkg/ontology#")

class DKGOrchestrator:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.dir_input = base_dir / "1_input_interne"
        self.dir_vault = base_dir / "3_app_referential_vault"
        self.dir_exposition = base_dir / "4_exposition_md"
        
        # Initialisation des répertoires de sortie
        self.dir_vault.mkdir(parents=True, exist_ok=True)
        (self.dir_exposition / "Lexiques").mkdir(parents=True, exist_ok=True)
        (self.dir_exposition / "Ontologies" / "par_domaines").mkdir(parents=True, exist_ok=True)

    def build_vault_from_inputs(self) -> Graph:
        """Parse les fichiers Markdown d'entrée et génère le TTL unifié dans le Vault."""
        print("⚡ [STEP 1] Building Vault TTL from Inputs...")
        global_graph = Graph()
        global_graph.bind("skos", SKOS)
        global_graph.bind("ex", EX)

        md_files = list(self.dir_input.rglob("src_*.md"))
        for md_file in md_files:
            print(f"  └─ Parsing input: {md_file.name}")
            content = md_file.read_text(encoding="utf-8")
            blocks = re.split(r'\n(?=###?\s+)', content)
            
            for block in blocks:
                lines = [l.strip() for l in block.split('\n') if l.strip()]
                if not lines or not lines[0].startswith('#'):
                    continue
                
                term_label = re.sub(r'^###?\s+', '', lines[0]).strip()
                term_id = re.sub(r'[^a-zA-Z0-9_]', '_', term_label)
                concept_uri = EX[f"Concept_{term_id}"]
                
                global_graph.add((concept_uri, RDF.type, SKOS.Concept))
                global_graph.add((concept_uri, SKOS.prefLabel, Literal(term_label, lang="fr")))
                
                for line in lines[1:]:
                    if "**Définition**" in line:
                        definition = re.sub(r'^[*|-]\s*\*\*Définition\*\*\s*:\s*', '', line)
                        global_graph.add((concept_uri, SKOS.definition, Literal(definition, lang="fr")))

        vault_file = self.dir_vault / "vault_dkg_global.ttl"
        global_graph.serialize(destination=str(vault_file), format="turtle")
        print(f"✅ Vault unifié créé : {vault_file.name}")
        return global_graph

    def generate_exposition_docs(self, graph: Graph):
        """Régénère la documentation Markdown lisible (doc_*.md)."""
        print("⚡ [STEP 2] Generating Exposition Markdown Documents...")
        
        # 1. Génération du Lexique d'Exposition
        lexicon_doc = self.dir_exposition / "Lexiques" / "doc_lexique_public_complet.md"
        doc_lines = [
            "# 📖 Lexique Global d'Exposition DKG\n",
            "*Ce document est généré automatiquement depuis le Vault. Ne pas modifier directement.*\n"
        ]
        
        for s, p, o in graph.triples((None, SKOS.prefLabel, None)):
            if o.language == "fr":
                doc_lines.append(f"### {o.value}")
                defs = list(graph.objects(s, SKOS.definition))
                if defs:
                    doc_lines.append(f"* **Définition :** {defs[0].value}\n")
        
        lexicon_doc.write_text("\n".join(doc_lines), encoding="utf-8")
        print(f"  └─ Généré : {lexicon_doc.name}")

        # 2. Génération d'une fiche Domaine avec schéma Mermaid
        domain_doc = self.dir_exposition / "Ontologies" / "par_domaines" / "doc_domain_infrastructure.md"
        mermaid_template = (
            "# 🛡️ Ontologie - Domaine Infrastructure\n\n"
            "```mermaid\n"
            "graph TD\n"
            "    Host[\"Host (Serveur/VM)\"] -->|CONNECTED_TO| Network[\"Réseau\"]\n"
            "    Host -->|HAS_VULN| Vulnerability[\"Vulnérabilité\"]\n"
            "```\n\n"
            "*Fichier de restitution mis à jour automatiquement.*"
        )
        domain_doc.write_text(mermaid_template, encoding="utf-8")
        print(f"  └─ Généré : {domain_doc.name}")

if __name__ == "__main__":
    root_path = Path(__file__).resolve().parents[2] / "LexiquesOntologie"
    orchestrator = DKGOrchestrator(root_path)
    g = orchestrator.build_vault_from_inputs()
    orchestrator.generate_exposition_docs(g)
