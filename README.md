### Introduction
This is a set of resources for experimenting with customized chatbots as I talk about in my MacSysAdmin 2023 presentation.

The download contains a complete Python 3.10.11 distribution with all the Python requirements pre-installed.

### Requirements
These should run on any Apple silicon Mac. There is (currently) no support for Intel Macs or other OSes.

LLMs are large. You'll need some disk space.
llama-2-7b-chat.Q4_0.gguf is almost 4GB; llama-2-13b-chat.Q4_0.gguf is almost 7GB.
Embedding models can also take up signifcant disk space, though usually they are much smaller than the LLMs they augment.

### Getting started
Don't bother git cloning this directory. Instead download the release zip file, which includes the Python.framework.
Copy any text-based documents into the documents folder. Plain text files, Markdown files, and even PDFs are known to work. Be sure to remove the default README.txt file from the documents folder.

There are example documents for Munki and AutoPkg in the example_docs folder.

Ensure the index_storage directory is empty any time you change the contents of the documents folder or you change the embedding engine.

Run the `run_local_chatbot.sh` script to start up a local chatbot. The first time you do this, it will take several minutes to download an LLM model file, an embeddings model file, and to process and embed the documents into an index. Subsequent launches will use cached files and will be much faster.

### Known issues
Lots!
The script prints a few (harmless) warnings when started.
The chatbot prints weird messages when first started up.
The script doesn't exit cleanly.
The accuracy of the chatbot repsonses varies widely.
Think of this as a starting point for experimentation, not a complete tool.

### Support
None! This is a quick-and-dirty proof-of-concept and is not really intended to be something that is maintained and refined. The hope is this will be a relatively easy introduction, and then you can start your own projects with what you learn.
