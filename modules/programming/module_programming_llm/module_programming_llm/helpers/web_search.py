from typing import Sequence, List

from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain

from langchain_community.retrievers import WebResearchRetriever
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.vectorstores import Chroma
from langchain_core.tools import Tool
from langchain_openai import OpenAIEmbeddings

from llm_core.models import ModelConfigType


def bulk_search(queries: Sequence[str], model: ModelConfigType) -> List[str]:
    result = []
    for query in queries:
        # use one of 2 available methods, web search is faster, but less precise
        result.append(answer_query_qa(query, model))
    return result


def answer_query_qa(query, model: ModelConfigType):
    """
    Answers a query using a QA model with a vector store and web search retrieval.

    Pros:
    - Uses a vector database (`chroma_db_oai`) to retrieve relevant information.
    - Provides more context-aware responses.
    - Improves response quality for complex queries.

    Cons:
    - Requires a pre-populated vector database.
    - Can be slower due to retrieval and processing time.

    Returns:
    - The LLM-generated response with sources.
    """
    model = model.get_model()  # Initialize the model
    vectorstore = Chroma(
        embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db_oai"
    )

    retriever = vectorstore.as_retriever()  # Retrieve similar entries
    retrieved_docs = retriever.get_relevant_documents(query)

    # This is an optimization - probably should sometimes invalidate the store though
    if retrieved_docs:  # If relevant data is found, use it
        qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
            model, retriever=retriever
        )
        result = qa_chain({"question": query})

        return result["answer"]

    # Initialize Google Search wrapper
    search = GoogleSearchAPIWrapper()

    # Create a retriever that uses both vector search and web search
    web_search_retriever = WebResearchRetriever.from_llm(
        vectorstore=vectorstore, llm=model, search=search, allow_dangerous_requests=True
    )

    # Create a QA chain that retrieves relevant sources before answering
    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
        model, retriever=web_search_retriever
    )

    # Generate an answer with contextual retrieval
    result = qa_chain({"question": query})

    return result["answer"]


def answer_query_google(query):
    """
    Answers a query using Google Search API.

    Pros:
    - Retrieves the most recent and up-to-date information from the web.
    - Does not require a pre-existing knowledge base.

    Cons:
    - No AI reasoning, only direct search results.
    - Quality depends on the search query's effectiveness.
    - Can return irrelevant or biased results.

    Returns:
    - Raw search results from Google.
    """
    search = GoogleSearchAPIWrapper()

    tool = Tool(
        name="google_search",
        description="Search Google for recent results.",
        func=search.run,
    )

    return tool.run(query)
