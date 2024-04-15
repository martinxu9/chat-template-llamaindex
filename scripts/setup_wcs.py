import weaviate
import os

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.weaviate import WeaviateVectorStore

from llama_index.core.node_parser import LangchainNodeParser, MarkdownNodeParser
from llama_index.core.ingestion import IngestionPipeline

from langchain_text_splitters import MarkdownHeaderTextSplitter


# Set these environment variables
WCS_URL = os.getenv("WCS_URL")
WCS_APIKEY = os.getenv("WCS_API_KEY", "")

DATA_DIRECTORY: str = "/Users/martinxu9/code/reflex/examples/reflex-web"
# Note: Index name is CamelCase.
INDEX_NAME = "ReflexLlamaindexTraceloopDemo"

client = weaviate.Client(
    url=WCS_URL, auth_client_secret=weaviate.AuthApiKey(api_key=WCS_APIKEY)
)


documents = SimpleDirectoryReader(
    input_dir=DATA_DIRECTORY, recursive=True, required_exts=[".md"]
).load_data()

print(f"Read number of docs from {DATA_DIRECTORY}: {len(documents)}")

vector_store = WeaviateVectorStore(
    weaviate_client=client,
    index_name=INDEX_NAME,
)


# Use markdown splitter from LangChain instead of the defaults.
headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
langchain_parser = LangchainNodeParser(
    MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
)
pipeline = IngestionPipeline(
    transformations=[langchain_parser],
    vector_store=vector_store,
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
