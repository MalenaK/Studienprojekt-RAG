This is a project for running a local LLM that uses Retrieval-Augmented Generation (RAG) to generate answers based on context which is fed to it via PDFs.
The project was done for the chair "Soziotechnisches Systemdesign und Künstliche Intelligenz" (SSKI, https://sski.ruhr-uni-bochum.de/) at Ruhr-University Bochum (https://www.ruhr-uni-bochum.de/en).

# SETUP
## for Windows Machines
0. Install Anaconda for managing python environments: https://www.anaconda.com/download/

1.  Clone the repository and navigate into the root directory 

2. Set the path where the env will be installed by opening the localRAG_env.yaml file and changing the path in the prefix section.

4. Use `conda env create -f localRAG_env.yaml` to install the environment.
If you receive the error "Microsoft Visual Studio C++ is required" then proceed with installing it. Open Visual Studio and go to the tap "individual components". Here, select "MSVC v143 - VS 2022 C++ x64/x86 build tools (latest)" and "Windows [your windows version] SDK" with the latest version. Let these components install and try executing the conda create command again.

5. Activate your env, e.g. via command `conda activate studyproject` or with help of your IDE (CTRL+Shift+P in Visual Studio Code)

6. Install Ollama for accessing open-source LLMs: https://ollama.com/

7. Pull necessary models using Ollama (as specified inside config/settings.py):
     1. `ollama pull llama3.1`
     2. `ollama pull mxbai-embed-large`
8. Serve local LLM via `ollama serve`.
If you receive the error message `Error: listen tcp 127.0.0.1:[port number]: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.` then ollama is probably already running and you can proceed with the next step.

10. In the root directory of your repository, execute `python main.py` to run the project.


## for Linux Machines

0. Install Anaconda for managing python environments: https://docs.anaconda.com/anaconda/install/linux/

1. Clone the repository and navigate into the root directory 

2. Review localRAG_env.yaml
Ensure the dependencies listed in `localRAG_env.yaml` follow this format:\
`- package=1.3`\
or simply\
`- package`\
**Not this format:**\
`- package=1.3=h28994`\
This ensures compatibility across different operating systems. Remove the build number (`=h28994`) if needed
 -  **Remove Windows-specific dependencies** from the YAML file:
	- `pywin32-ctypes`
	- `win_inet_pton`
	- `cuda-cccl_win-64`
	- `vc`
	- `vs2015_runtime`
	- `pthreads-win32`
	- `ucrt`

3. Modify the `prefix` Path
In `localRAG_env.yaml`, adjust the path under the `prefix` section to specify the location of the environment.

4. Use `conda env create -f localRAG_env.yaml` to install the environment.

5. activate your env, e.g. via command `conda activate studyproject` or with help of your IDE (CTRL+Shift+P in Visual Studio Code)

6. Install Ollama for accessing open-source LLMs: https://ollama.com/

7. Pull necessary models using Ollama (as specified inside config/settings.py):
     1. `ollama pull llama3.1`
     2. `ollama pull mxbai-embed-large`

8. Serve local LLM via `ollama serve`. If you receive the error message `Error: listen tcp 127.0.0.1:[port number]: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.` then ollama is probably already running and you can proceed with the next step.
	- On systems that use systemd the server job is enabled by default you can stop the process using the command line
		- `systemctl stop ollama`
	- And rerun the server using
		- `ollama serve`

9. In the root directory of your repository, execute `python main.py` to run the project

# USAGE
The command for running our project: `python main.py [-d path/to/data/dir] [-ra] [-rc]`
| Command            | Description                                       |
|--------------------|---------------------------------------------------|
| `-d` / `--pdf_dir` | Specifies the directory containing PDF files. The directory should contain only PDFs. Defaults to `./data/data_basic`. |
| `-ra` / `--reset_all` | Resets all collections in the database. This deletes all contents in the database. **Use with caution!** Defaults to `False`. |
| `-rc` / `--reset_collection` | Resets only the collection specified via `-d`. Defaults to `False`. |

Further Hints: 
- Please remember to clear the database after changing the embedding model (using `-rc`).
- The database will add the new chunks if you add new PDFs to your data directory.
Please note: The warnings arising during start-up regarding BetterTransformers do not originate from our project but from an external library used. This usage of our system will not be restricted.


