import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

class RAGVectorization:
    def __init__(self, collection_name: str = "repo_chunks", chroma_db_path: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=chroma_db_path)
        self.embedding_funstions = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name = collection_name,
            embedding_function=self.embedding_funstions
        )

    def final_chunks(self, f, chunk_size=1500):
        final_chunks = []
        content = f['content']
        if len(content) > chunk_size:
            chunks = content.split("\n\n")

            for chunk in chunks:
                if len(chunk) > chunk_size:
                    lines = chunk.split("\n")

                    current_chunk = ""
                    for line in lines:
                        if len(current_chunk) + len(line) > chunk_size:
                            if current_chunk:
                                final_chunks.append(current_chunk)
                            current_chunk = line + "\n"
                        else:
                            current_chunk += line + "\n"

                    if current_chunk:
                        final_chunks.append(current_chunk)
                else:
                    final_chunks.append(chunk)
        else:
            final_chunks = [content]
        return final_chunks
    
    def index_repo_files(self, files, chunk_size: int = 1500):
        docs = []
        ids = []
        metadatas = []

        for f in files:
            final_chunks = self.final_chunks(f, chunk_size)
            for i, chunk in enumerate(final_chunks):
                if chunk.strip():
                    docs.append(chunk)
                    ids.append(f"{f['path']}-{i}")
                    metadatas.append({
                        "source": f['path'],
                        "total_chunks":len(final_chunks)
                    })
        
        if docs:
            batch_size = 500
            for i in range(0, len(docs), batch_size):
                end = min(i+batch_size, len(docs))
                self.collection.upsert(
                    documents=docs[i:end],
                    metadatas=metadatas[i:end],
                    ids=ids[i:end]
                )
