from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.core.settings import Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from langchain.tools import Tool
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from llama_index.core.langchain_helpers.agents import (
    IndexToolConfig,
    LlamaIndexTool,
)
import chromadb

template = """
Assistant is a large language model trained by OpenAI.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

TOOLS:
------

Assistant has access to the following tools:

{tools}

Always use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: {tool_names}
Action Input: the input to the action, should be '{input}' or something similar
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
"""

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
    tool_config = IndexToolConfig(
        query_engine=index.as_query_engine(),
        name=f"LlamaIndex",
        description=f"useful for when you want to answer queries about the author",
        tool_kwargs={"return_direct": True},
    )

    tool = LlamaIndexTool.from_tool_config(tool_config)

    tools = [tool]

    prompt = ChatPromptTemplate.from_template(template)
    agent = create_react_agent(tools=tools, llm=llm, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors="Check your output and make sure it conforms! Do not output an action and a final answer at the same time.", 
        max_iterations=5
    )
    return agent_executor

def build_rag_pipeline(llm):

    print("Building index...")
    documents = load_documents("data")
    index = build_index(llm, documents)

    print("Building chain")
    executor = build_chain(llm, index)

    return executor
  