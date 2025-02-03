import os
import shutil
from chromadb import PersistentClient
from typing import Any
from langchain_chroma import Chroma
from langchain.schema.document import Document
from retrieval.chunker import calculate_chunk_ids
from models.embedding import get_embedding_function
from config.settings import CHROMA_FOLDER


class DatabaseHelper:
    """A helper class for managing a Chroma database, handling document storage, retrieval, and deletion."""

    chroma_path: str = CHROMA_FOLDER #folder where chroma db is stored

    def __init__(self, model: str):
        """
        Initializes the DatabaseHelper with the specified embedding model.

        Parameters
        ----------
        model: str
            The name of the embedding model to be used.
        """
        self.model = model
        self.collection_name = ""

    def add_to_chroma(self, chunks: list[Document]) -> None:
        """
        Adds chunks to the current collection. Only adds chunks that are not yet contained inside the collection.

        Parameters
        ----------
        chunks: list[Document]
            The chunks the collection should contain.

        Raises
        ----------
        Exception
            this exception indicates that you tried to update a collection without having selected one. This indicates an error in the logical flow of your program.
        """
        if not self.collection_name:
            raise Exception("collection name for db was not set. This is an error in your code. Fix by setting collection name before calling add to chroma.")
        db: Chroma = Chroma(persist_directory=self.chroma_path, embedding_function=get_embedding_function(self.model), collection_name=self.collection_name)

        # Calculate Page IDs.
        chunks_with_ids: list[Document] = calculate_chunk_ids(chunks)

        # Add or Update the documents.
        existing_items:  dict[str, Any] = db.get(include=[])  # IDs are always included by default
        existing_ids: set = set(existing_items["ids"])
        print(f"Number of existing documents in DB collection {self.collection_name}: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks: list[Document] = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        total_new_chunks = len(new_chunks)  # Count new chunks
        if total_new_chunks > 0:
            print(f"Adding new documents: {total_new_chunks}")

            new_chunk_ids: list[Document] = [chunk.metadata["id"] for chunk in new_chunks]

            for idx, (chunk, chunk_id) in enumerate(zip(new_chunks, new_chunk_ids)):
                db.add_documents([chunk], ids=[chunk_id])  # Add one chunk at a time

                print(f"Progress: {idx + 1}/{total_new_chunks} chunks added.")

        else:
            print("No new documents detected - no changes to db are made.")

    def clear_database(self):
        """
        Deletes all the content of the database. USE WITH CAUTION!
        """
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)
            print("Cleared the whole DB")
        else:
            print("DB already empty")
    
    def get_db_for_collection(self) -> Chroma:
        """
        Selects the collection specified by the current collection name.
        Requires the embedding to be specified inside /models/embedding.

        Returns
        ----------
        collection: Chroma
            The current collection.
        """
        return Chroma(persist_directory=self.chroma_path, embedding_function=get_embedding_function(), collection_name=self.collection_name)
    
    def clear_collection(self, collection_name):
        """
        Deletes the specified collection

        Parameters
        ----------
        collection_name: str
            The name of the collection to be deleted.

        Raises
        ----------
        Exception
            this exception indicates that the collection could not be deleted beacuse it does not exist.
        """
        try:
            db_client = PersistentClient(path=self.chroma_path)
            db_client.delete_collection(collection_name)
            print(f"Collection {collection_name} deleted successfully.")
        except Exception as e:
            raise Exception(f"Unable to delete collection: {e}")
        
    def set_collection_name (self, collection_name: str):
        """
        Sets the name of the current collection.

         Parameters
        ----------
        collection_name: str
            The name of the current collection.

        """
        self.collection_name = collection_name