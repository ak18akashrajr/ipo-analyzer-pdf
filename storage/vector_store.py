import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
import os

class IPOVectorStore:
    def __init__(self, persist_dir="chroma_db"):
        self.persist_dir = persist_dir
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        
        # Use Sentence Transformers for local, free embeddings
        # This keeps the "Retail-Safe" design cost-effective and private
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="ipo_documents",
            embedding_function=self.embedding_fn
        )

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """
        Adds parsed chunks to the Vector DB.
        """
        if not chunks:
            return
            
        ids = [f"id_{i}" for i in range(len(chunks))]
        documents = [c['text'] for c in chunks]
        
        # Prepare metadata: Ensure all values are strings or numbers (flat dict)
        metadatas = []
        for c in chunks:
            meta = {
                "section": c.get("section", "Unknown"),
                "page": str(c.get("page", 0)),
                "source": c.get("source", "RHP")
            }
            metadatas.append(meta)

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Indexed {len(chunks)} chunks into ChromaDB at {self.persist_dir}")

    def query(self, query_text: str, n_results=5, section_filter=None) -> List[Dict[str, Any]]:
        """
        Semantic search for the query text.
        Optionally filter by section (e.g., only search "Risk Factors").
        """
        where_filter = {}
        if section_filter:
            where_filter = {"section": section_filter}
        
        # If section_filter is None, pass None to 'where'
        args = {
            "query_texts": [query_text],
            "n_results": n_results
        }
        if section_filter:
            args["where"] = where_filter

        results = self.collection.query(**args)
        
        # Simplify output structure
        structured_results = []
        if results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][i]
                structured_results.append({
                    "text": doc,
                    "metadata": meta
                })
                
        return structured_results

if __name__ == "__main__":
    # Test stub
    pass
