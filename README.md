This is a project for running a local LLM that uses Retrieval-Augmented Generation (RAG) to generate answers based on context which is fed to it via PDFs.
The project was done for the chair "Soziotechnisches Systemdesign und Künstliche Intelligenz" (SSKI) at Ruhr-University Bochum.

# SETUP
## for Windows Machines
0. Install Anaconda for managing python environments: https://www.anaconda.com/download/

1. After cloning this git repository, in the root directory of your local repo, install the python env. If you want to modify the path where the env will be installed, open the localRAG_env.yaml file and change the path in the prefix section. Otherwise, the env will be installed to the default directory. Use `conda env create -f localRAG_env.yaml` to install the environment.

2. Activate your env, e.g. via command `conda activate studyproject` or with help of your IDE (CTRL+Shift+P in Visual Studio Code)

3. Install Ollama for accessing open-source LLMs: https://ollama.com/

4. Pull necessary LLMs using Ollama:
     1. `ollama pull llama3`
     2. `ollama pull [name of model for embedding]`
5. Serve local LLM via `ollama serve`. If you receive the error message `Error: listen tcp 127.0.0.1:[port number]: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.` then ollama is probably already running and you can proceed with the next step.

6. In the root directory of your repository, execute `python main.py` to start using our project.


## for Linux Machines

0. Install Anaconda for managing python environments: https://docs.anaconda.com/anaconda/install/linux/

1. Clone the repository and navigate into the root directory 

2. Review localRAG_env.yaml
Ensure the dependencies listed in `localRAG_env.yaml` follow this format:
`- package=1.3`
or simply
`- package`
**Not this format:**
`- package=1.3=h28994`
This ensures compatibility across different operating systems. Remove the build number (`=h28994`) if needed
 -  **Remove Windows-specific dependencies** from the YAML file:
	- `pywin32-ctypes`
	- `win_inet_pton`
	- `cuda-cccl_win-64`
	- `vc`
	- `vs2015_runtime`

3. Modify the `prefix` Path
In `localRAG_env.yaml`, adjust the path under the `prefix` section to specify the location of the environment.

4. Use `conda env create -f localRAG_env.yaml` to install the environment.

5. activate your env, e.g. via command `conda activate studyproject` or with help of your IDE (CTRL+Shift+P in Visual Studio Code)

6. Install Ollama for accessing open-source LLMs: https://ollama.com/

7. Pull necessary LLMs using Ollama:

	1. `ollama pull llama3`

	2. `ollama pull [name of model for embedding]`

8. Serve local LLM via `ollama serve`. If you receive the error message `Error: listen tcp 127.0.0.1:[port number]: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.` then ollama is probably already running and you can proceed with the next step.
	- On systems that use systemd the server job is enabled by default you can stop the process using the command line
		- `systemctl stop ollama`
	- And rerun the server using
		- `ollama serve`

9. In the root directory of your repository, execute `python main.py` to run the project