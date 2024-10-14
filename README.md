#TODO -> Improve this READ ME

This is a project for running a local LLM that uses Retrieval-Augmented Generation (RAG) to generate answers based on context which is fed to it via PDFs.
The project was done for the chair "Soziotechnisches Systemdesign und Künstliche Intelligenz" (SSKI) at Ruhr-University Bochum.

# SETUP
## on Windows Machines
0. install Anaconda for managing python environments: https://www.anaconda.com/download/
1. after cloning this git repository, in the root directory of your local repo, install the python env. If you want to modify the path where the env will be installed, open the localRAG_env.yaml file and change the path in the prefix section. Otherwise, the env will be installed to the default directory. Use "conda env create -f localRAG_env.yaml" to install the environment.
2. activate your env, e.g. via command "conda activate studyproject" or with help of your IDE (ctrl+shift+p in vs code)
3. Install Ollama for accessing open-source LLMs: https://ollama.com/
4. Pull necessary LLMs using Ollama:
     1. "ollama pull llama3"
     2. "ollama pull [name of model for embedding]"
5. serve local LLM via "ollama serve". If you receive the error message "Error: listen tcp 127.0.0.1:[port number]: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted." then ollama is probably already running and you can proceed with the next step.
6. in the root directory of your repository, execute "python main.py" to start using our project.
