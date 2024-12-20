from models.ollama_model import Model
from retrieval.document_handler import DocumentHandler
from retrieval.database_helper import DatabaseHelper
from config import config_model, config_embedding

#Instantiate Required Objects
llm_model: Model = Model(model=config_model)  # Idk why it says that we are getting None here in pycharm, it returns an object
db_helper = DatabaseHelper(model=config_embedding)
doc_handler = DocumentHandler()