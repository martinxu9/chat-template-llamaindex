# Chat with Reflex Docs

This is a demo app made using the [Chat template](https://github.com/reflex-dev/reflex-chat) from [Reflex](https://github.com/reflex-dev/reflex), [Llama Index](https://docs.llamaindex.ai/en/stable/examples/vector_stores/WeaviateIndexDemo/), [LangChain](https://python.langchain.com/docs/modules/data_connection/), [Weaviate](https://weaviate.io/developers/weaviate), [Traceloop](https://www.traceloop.com/docs/openllmetry/getting-started-python) and OpenAI.

## Prerequisites

- OpenAI API key: the app uses OpenAI embedding and chat functionality.
- Traceloop API key: the app traces the function call to OpenAI and export to Traceloop dashboard.
- Weaviate: create a free 14-day cluster and gets the URL and API key to create connection client.

## Requirements

```bash
reflex>=0.4.7
langchain-text-splitters
llama-index
llama-index-vector-stores-weaviate
traceloop-sdk
```

## Steps to Run

### Environment Variables

```bash
export TRACELOOP_API_KEY=12345yourkey
export OPENAI_API_KEY=sk-your-key
export WCS_URL=https://your-index-random-numbers.weaviate.network
export WCS_API_KEY=your-key
```

### Set up the remote vector DB

This demo uses the free 14-day vector database cluster. Go to their website and create an account. After creating the cluster, note the connection information (the URL and the API key).

Set the `OPENAI_API_KEY`, `WC_URL`, `WC_API_KEY` as environment variables, then run the `scripts/setup_wcs.py`. The `setup_wcs.py` scripts ingest a directory of markdown files and create an index in the remote Weaviate cluster. In this demo, the folder contains all the markdown files for (a subset of) the [reflex documentation](https://reflex.dev/docs/).

### Run the Reflex App

This app is based on [Reflex](https://github.com/reflex-dev/reflex) framework. In the top level directory (this directory has a file named `rxconfig.py`), run the following commands to run the app:

```bash
reflex init
reflex run
```

Then go to `https://localhost:3000` or another URL shown in the terminal when the app is running. Chat and get the results based on the reflex documentation.

### Monitor Your App on Traceloop

Go to the traceloop dashboard, you can see stats such as the tokens and models used for OpenAI calls.