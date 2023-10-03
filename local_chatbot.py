from langchain.embeddings import HuggingFaceEmbeddings
from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
    set_global_service_context,
    StorageContext,
    load_index_from_storage,
    set_global_handler
)
from llama_index.llms import LlamaCPP
from llama_index.llms.llama_utils import messages_to_prompt, completion_to_prompt
from llama_index.memory import ChatMemoryBuffer

##############################################################################
# turn on llama_index debug output by uncommenting the next line
##############################################################################
#set_global_handler("simple")

##############################################################################
# set the model URL
##############################################################################

# more accurate model, but larger and uses more RAM
#model_url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf"

# more lightweight model
model_url = "https://huggingface.co/TheBloke/Llama-2-7B-chat-GGUF/resolve/main/llama-2-7b-chat.Q4_0.gguf"


##############################################################################
# embedding models Uncomment the one you want to use; comment out the rest
##############################################################################

# uses default local embedding model
embed_model="local"

# uses default OpenAI embedding model
#import openai
#openai.api_key = "<your OpenAI API key goes here>"

# uses sentence-transformers/all-mpnet-base-v2 as embedding model
#embed_model = HuggingFaceEmbeddings(
#    model_name="sentence-transformers/all-mpnet-base-v2"
#)

# uses hkunlp/instructor-large" as embedding model
#from llama_index.embeddings import InstructorEmbedding
#embed_model = InstructorEmbedding(model_name="hkunlp/instructor-large")

# uses BAAI/bge-small-en as embedding model
#from llama_index.embeddings import HuggingFaceEmbedding
#embed_model = HuggingFaceEmbedding()

# uses BAAI/bge-small-en-v1.5 as embedding model
#from llama_index.embeddings import HuggingFaceEmbedding
#embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5")


##############################################################################
# prompt customization
##############################################################################

SYSTEM_PROMPT = (
    "You are a trusted, expert Q&A system.\n"
    "Always answer the query using the provided context information, "
    "and not prior knowledge.\n"
    "Some rules to follow:\n"
    "1. Never directly reference the given context in your answer.\n"
    "2. Avoid statements like 'Based on the context, ...' or "
    "'The context information ...' or anything similar."
)
CONTEXT_TEMPLATE = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query.\n"
)


llm = LlamaCPP(
    # You can pass in the URL to a GGML model to download it automatically
    model_url=model_url,
    # optionally, you can set the path to a pre-downloaded model instead of model_url
    model_path=None,
    # Adjusts randomness of outputs, greater than 1 is random and 0 is deterministic, 0.75 is a good starting value.
    temperature=0.75,
    # controls how much text is generated. a token is aprrox 3/4th of a word
    max_new_tokens=500,
    # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
    context_window=3900,
    # kwargs to pass to __call__()
    generate_kwargs={},
    # kwargs to pass to __init__()
    # set n_gpu_layers to at least 1 to use GPU
    model_kwargs={"n_gpu_layers": 1},
    # transform inputs into Llama2 format
    messages_to_prompt=messages_to_prompt,
    completion_to_prompt=completion_to_prompt,
    verbose=False,
)

service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
set_global_service_context(service_context)
STORAGE_DIR = "index_storage"

try:
    index = load_index_from_storage(
        StorageContext.from_defaults(persist_dir=STORAGE_DIR))
except:
    documents = SimpleDirectoryReader('documents', recursive=True).load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index.storage_context.persist(STORAGE_DIR)

memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

chat_engine = index.as_chat_engine(
    context_template=CONTEXT_TEMPLATE,
    system_prompt=SYSTEM_PROMPT,
    similarity_top_k=5,
    chat_mode="context",
    memory=memory,
)

response = chat_engine.chat("Hello!")
print(response)

while True:
    prompt = input("> ")
    if prompt:
        response = chat_engine.chat(prompt)
        print(response)
        print
    else:
        break

