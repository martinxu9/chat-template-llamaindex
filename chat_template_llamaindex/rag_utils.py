import os

import weaviate

from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.weaviate import WeaviateVectorStore


_query_engine: BaseQueryEngine

# Set these environment variables
WCS_URL = os.getenv("WCS_URL")
WCS_APIKEY = os.getenv("WCS_API_KEY", "")

INDEX_NAME = "ReflexLlamaindexTraceloopDemo"


def load_remote_vector_store():
    global _query_engine
    client = weaviate.Client(
        url=WCS_URL, auth_client_secret=weaviate.AuthApiKey(api_key=WCS_APIKEY)
    )
    llm = OpenAI(model="gpt-4-0125-preview")
    service_context = ServiceContext.from_defaults(llm=llm)
    vector_store = WeaviateVectorStore(
        weaviate_client=client,
        index_name=INDEX_NAME,
    )
    loaded_index = VectorStoreIndex.from_vector_store(
        vector_store, service_context=service_context
    )
    _query_engine = loaded_index.as_query_engine()


def get_engine():
    return _query_engine
