import os
import openai
from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
    set_global_service_context,
    StorageContext,
    load_index_from_storage,
    set_global_handler
)

##############################################################################
# turn on llama_index debug output by uncommenting the next line
##############################################################################
#set_global_handler("simple")

openai.api_key = "<your OpenAI API key goes here>"
if openai.api_key == "<your OpenAI API key goes here>":
    print("No OpenAI API key provided.")
    print("Please edit the %s script and insert your OpenAPI key."
          % os.path.basename(__file__))
    exit(-1)

service_context = ServiceContext.from_defaults()
set_global_service_context(service_context)
STORAGE_DIR = "index_storage"

try:
    index = load_index_from_storage(
        StorageContext.from_defaults(persist_dir=STORAGE_DIR))
except:
    documents = SimpleDirectoryReader('documents', recursive=True).load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index.storage_context.persist(STORAGE_DIR)

chat_engine = index.as_chat_engine(chat_mode="openai")
response = chat_engine.chat("Hello!")
print(response)

while True:
    prompt = input("> ")
    if prompt:
        response = chat_engine.chat(
            prompt,
            function_call="query_engine_tool",
        )
        print(response)
        print
    else:
        break
