import random
import logging
from typing import Sequence, List
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain_community.retrievers import WebResearchRetriever
from langchain_core.tools import Tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.utilities import GoogleSearchAPIWrapper
from llm_core.models import ModelConfigType


def bulk_search(queries: Sequence[str], model: ModelConfigType) -> List[str]:
    result = []
    for query in queries:
        # use one of 2 available methods, pure web search is faster, but less precise
        result.append(answer_query_qa(query, model))
    return result


def answer_query_qa(query, model: ModelConfigType, web_search_probability=0.1):
    """
    Answers a query using a QA model with a vector store and optional web search retrieval.

    Enhancements:
    - Periodically triggers web search even if vector store has results.
    - Handles API errors (e.g., Google 429 Too Many Requests).
    - Logs errors instead of failing the pipeline.

    Params:
    - query: The input question.
    - model: LLM configuration.
    - web_search_probability: Probability (0 to 1) of always performing a web search.

    Returns:
    - The LLM-generated response.
    """

    model = model.get_model()
    vectorstore = Chroma(
        embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db_oai"
    )

    retriever = vectorstore.as_retriever()
    retrieved_docs = retriever.get_relevant_documents(query)

    # Decide whether to perform a web search
    force_web_search = random.random() < web_search_probability

    if retrieved_docs and not force_web_search:
        qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
            model, retriever=retriever
        )
        result = qa_chain({"question": query})
        return result["answer"]

    # Web search fallback (or forced by probability)
    try:
        search = GoogleSearchAPIWrapper()
        # Only google search api for this retriever
        web_search_retriever = WebResearchRetriever.from_llm(
            vectorstore=vectorstore, llm=model, search=search, allow_dangerous_requests=True
        )
        qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
            model, retriever=web_search_retriever
        )
        result = qa_chain({"question": query})
        return result["answer"]

    except Exception as e:
        logging.warning("Web search failed: %s", e)
        # If web search fails, fall back to the vector store results
        if retrieved_docs:
            qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
                model, retriever=retriever
            )
            result = qa_chain({"question": query})
            return result["answer"]

        return "I couldn't retrieve any relevant information at this time."


def answer_query_google(query):
    """
    Answers a query using Google Search API with error handling.

    Pros:
    - Retrieves the most recent and up-to-date information from the web.
    - Does not require a pre-existing knowledge base.

    Cons:
    - No AI reasoning, only direct search results.
    - Quality depends on the search query's effectiveness.
    - Can return irrelevant or biased results.
    - May fail due to API rate limits or connectivity issues.

    Returns:
    - Raw search results from Google if available.
    - An error message if the API request fails.
    """
    try:
        # you can use any other web search api, e.g. duckduckgo
        search = GoogleSearchAPIWrapper()
        tool = Tool(
            name="google_search",
            description="Search Google for recent results.",
            func=search.run,
        )
        return tool.run(query)

    except Exception as e:
        logging.warning("Web search failed: %s", e)
        return "I couldn't retrieve search results at this time."
