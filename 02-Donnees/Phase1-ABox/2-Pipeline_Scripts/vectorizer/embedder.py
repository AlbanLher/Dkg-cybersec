import os
from typing import List, Dict, Any
from neo4j import GraphDatabase
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

class Neo4jVectorIndexer:
    """Indexation et vectorisation 100% LOCALE via Hugging Face pour Neo4j."""

    def __init__(
        self,
        uri: str = os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user: str = os.getenv("NEO4J_USER", "neo4j"),
        password: str = os.getenv("NEO4J_PASSWORD", "password"),
        # Modèle local BGE-M3 ou MiniLM optimisé pour la RAM (16 Go)
        model_name: str = "BAAI/bge-small-en-v1.5"
    ):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
        print(f"📦 Chargement du modèle d'embedding Hugging Face local : {model_name}...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},  # Utilise le CPU (ou 'cuda' si ROCm configuré)
            encode_kwargs={'normalize_embeddings': True}
        )
        # BGE-small-en-v1.5 génère des vecteurs de dimension 384 (très peu gourmand en mémoire)
        self.embedding_dimension = 384

    def close(self):
        self.driver.close()

    def setup_indexes(
        self,
        label: str = "DocumentChunk",
        text_property: str = "text",
        embedding_property: str = "embedding",
        vector_index_name: str = "chunk_vector_index",
        fulltext_index_name: str = "chunk_fulltext_index"
    ):
        """Crée l'index vectoriel (Cosine) et l'index fulltext (Lucene) dans Neo4j."""
        with self.driver.session() as session:
            session.run(f"""
            CREATE VECTOR INDEX `{vector_index_name}` IF NOT EXISTS
            FOR (n:`{label}`) ON (n.`{embedding_property}`)
            OPTIONS {{
              indexConfig: {{
                `vector.dimensions`: {self.embedding_dimension},
                `vector.similarity_function`: 'cosine'
              }}
            }}
            """)

            session.run(f"""
            CREATE FULLTEXT INDEX `{fulltext_index_name}` IF NOT EXISTS
            FOR (n:`{label}`) ON EACH [n.`{text_property}`]
            """)

    def embed_and_store(
        self,
        documents: List[Document],
        label: str = "DocumentChunk",
        text_property: str = "text",
        embedding_property: str = "embedding"
    ):
        """Génère les embeddings localement et enregistre dans Neo4j."""
        if not documents:
            return

        texts = [doc.page_content for doc in documents]
        embeddings_vectors = self.embeddings.embed_documents(texts)

        nodes_data = []
        for doc, vector in zip(documents, embeddings_vectors):
            nodes_data.append({
                "id": doc.metadata.get("id", str(hash(doc.page_content))),
                "text": doc.page_content,
                "embedding": vector,
                "metadata": doc.metadata
            })

        query = f"""
        UNWIND $batch AS row
        MERGE (n:`{label}` {{id: row.id}})
        SET n.`{text_property}` = row.text,
            n.`{embedding_property}` = row.embedding,
            n += row.metadata
        """
        
        with self.driver.session() as session:
            session.run(query, batch=nodes_data)

    def hybrid_search(
        self,
        query_text: str,
        top_k: int = 5,
        alpha: float = 0.5,
        vector_index_name: str = "chunk_vector_index",
        fulltext_index_name: str = "chunk_fulltext_index"
    ) -> List[Dict[str, Any]]:
        """Recherche hybride Vector + Fulltext locale."""
        query_vector = self.embeddings.embed_query(query_text)

        hybrid_cypher = """
        CALL db.index.vector.queryNodes($vector_index, $top_k, $query_vector) 
        YIELD node AS v_node, score AS v_score
        WITH collect({node: v_node, score: v_score}) AS vector_results, collect(v_node) AS v_nodes

        CALL db.index.fulltext.queryNodes($fulltext_index, $query_text, {limit: $top_k}) 
        YIELD node AS ft_node, score AS ft_score
        WITH vector_results, v_nodes, collect({node: ft_node, score: ft_score}) AS ft_results, collect(ft_node) AS ft_nodes

        WITH vector_results, ft_results, [n IN v_nodes + ft_nodes WHERE n IS NOT NULL | n] AS all_nodes
        UNWIND all_nodes AS node
        WITH DISTINCT node, vector_results, ft_results

        WITH node,
             [i IN range(0, size(vector_results)-1) WHERE vector_results[i].node = node | i + 1][0] AS v_rank,
             [i IN range(0, size(ft_results)-1) WHERE ft_results[i].node = node | i + 1][0] AS ft_rank

        WITH node,
             coalesce(1.0 / (60.0 + v_rank), 0.0) AS v_rrf,
             coalesce(1.0 / (60.0 + ft_rank), 0.0) AS ft_rrf
        WITH node, (v_rrf * $alpha) + (ft_rrf * (1.0 - $alpha)) AS final_score

        RETURN node.id AS id, node.text AS text, final_score
        ORDER BY final_score DESC
        LIMIT $top_k
        """

        with self.driver.session() as session:
            result = session.run(
                hybrid_cypher,
                vector_index=vector_index_name,
                fulltext_index=fulltext_index_name,
                query_vector=query_vector,
                query_text=query_text,
                top_k=top_k,
                alpha=alpha
            )
            return [record.data() for record in result]
