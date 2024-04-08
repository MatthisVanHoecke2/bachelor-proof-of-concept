from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.settings import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from llama_index.core.langchain_helpers.agents import (
    IndexToolConfig,
    LlamaIndexTool,
)
import chromadb
from template import template

# Method for loading custom data into the model
def load_documents(docs_path):
    documents = SimpleDirectoryReader(docs_path, required_exts=[".txt"]).load_data()
    print(f"Loaded {len(documents)} documents")
    print(f"First document: {documents[0]}")
    return documents

# Method for loading the correct embeddings
def load_embedding_model(model_name):
    embeddings = OllamaEmbedding(model_name=model_name)
    return embeddings

# Method for building the LlamaIndex index
def build_index(llm, documents):
    embedding = load_embedding_model("llama2") # Get the embeddings by model name

    # Set LangChain settings
    Settings.llm = llm
    Settings.embed_model = embedding

    # Create an vector database client and collection
    chroma_client = chromadb.EphemeralClient()
    chroma_collection = chroma_client.get_or_create_collection("iollama")

    # Create an in-memory vector database
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # Generate storage context from database
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create vector index for retrieving data from the vector store
    index = VectorStoreIndex.from_documents(documents=documents, storage_context=storage_context, embed_model=embedding)

    return index

# Method for building the LangChain AgentExecutor (Creates a more natural response)
def build_agent_executor(llm: ChatOllama, index: VectorStoreIndex):
    tool_config = IndexToolConfig(
        query_engine=index.as_query_engine(),
        name=f"LlamaIndex",
        description=f"useful for when you want to answer queries about the author",
        tool_kwargs={"return_direct": True},
    )

    # Create a tool so the llm can access the index and add it to the list of tools
    tool = LlamaIndexTool.from_tool_config(tool_config)
    tools = [tool]

    # Add custom prompt so the llm knows when to use the tool
    prompt = ChatPromptTemplate.from_template(template)
    agent = create_react_agent(tools=tools, llm=llm, prompt=prompt)

    # Create agent executor from agent and tools
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, # Display logs in console
        handle_parsing_errors="Check your output and make sure it conforms to the given format! Do not output an action and a final answer at the same time.", # Specify how the llm should handle errors
        max_iterations=5 # The maximum allowed iterations when encountering an error, default to 15
    )
    return agent_executor

def build_rag_pipeline(llm):

    print("Building index...")
    documents = load_documents("data") # Load the custom data
    index = build_index(llm, documents) # Pass llm instance and data to method and build index

    print("Building chain")
    executor = build_agent_executor(llm, index) # Pass llm instance and index to method and build the executor

    return executor
  