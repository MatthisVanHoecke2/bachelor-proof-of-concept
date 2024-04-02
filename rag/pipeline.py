from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.settings import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from langchain.tools import Tool
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_community.chat_models.ollama import ChatOllama
import chromadb

def load_documents(docs_path):
    documents = SimpleDirectoryReader(docs_path, required_exts=[".txt"]).load_data()
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
    chroma_collection = chroma_client.get_or_create_collection("iollama")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context, embed_model=embedding)

    return index

def build_chain(llm: ChatOllama, index: VectorStoreIndex):
    tools = [
        Tool.from_function(
            name="LlamaIndex",
            func=lambda q: str(index.as_query_engine().query(q).response),
            description="useful for when you want to answer questions about the author.",
            return_direct=True
        )
    ]

    prompt = hub.pull("hwchase17/react-chat")
    agent = create_react_agent(tools=tools, llm=llm, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, max_iterations=5)
    return agent_executor

def build_rag_pipeline(llm):

    print("Building index...")
    documents = load_documents("data")
    index = build_index(llm, documents)

    print("Building chain")
    executor = build_chain(llm, index)

    return executor
  