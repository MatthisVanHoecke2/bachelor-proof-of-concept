from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.settings import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

def load_documents(docs_path):
    documents = SimpleDirectoryReader(docs_path, required_exts=[".json"]).load_data()
    print(f"Loaded {len(documents)} documents")
    print(f"First document: {documents[0]}")
    return documents

def load_embedding_model(model_name):
    embeddings = OllamaEmbedding(model_name=model_name)
    return embeddings

def build_index(llm, documents):
    embedding = load_embedding_model("llama2")

    Settings.llm = llm
    Settings.embed_model = embedding

    chroma_client = chromadb.EphemeralClient()
    chroma_collection = chroma_client.create_collection("iollama")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, embed_model=embedding)

    return index

def build_rag_pipeline(llm):

    print("Building index...")
    documents = load_documents("data")
    index = build_index(llm, documents)

    print("Constructing query engine...")

    query_engine = index.as_query_engine(similarity_top_k=3)

    return query_engine
  