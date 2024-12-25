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
    chroma_path: str = CHROMA_FOLDER #folder where chroma db is stored

    def __init__(self, model: str):
        self.model = model

    def add_to_chroma(self, chunks: list[Document], collection_name: str) -> None:
        db: Chroma = Chroma(persist_directory=self.chroma_path, embedding_function=get_embedding_function(self.model), collection_name=collection_name)

        # Calculate Page IDs.
        chunks_with_ids: list[Document] = calculate_chunk_ids(chunks)

        # Add or Update the documents.
        existing_items:  dict[str, Any] = db.get(include=[])  # IDs are always included by default
        existing_ids: set = set(existing_items["ids"])
        print(f"Number of existing documents in DB collection {collection_name}: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks: list[Document] = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        total_new_chunks = len(new_chunks)  # Count new chunks
        if total_new_chunks > 0:
            print(f"Adding new documents: {total_new_chunks}")

            new_chunk_ids: list[Document] = [chunk.metadata["id"] for chunk in new_chunks]

            # start_time = time.time()  # Start timing
            for idx, (chunk, chunk_id) in enumerate(zip(new_chunks, new_chunk_ids)):
                db.add_documents([chunk], ids=[chunk_id])  # Add one chunk at a time

                # Print progress
                print(f"Progress: {idx + 1}/{total_new_chunks} chunks added.")

            # end_time = time.time()  # End timing
            # print(f"Time taken to save documents: {end_time - start_time:.2f} seconds")
        else:
            print("No new documents detected - no changes to db are made.")

    def clear_database(self):
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)
            print("Cleared the whole DB")
        else:
            print("DB already empty")

    def get_collection(self, collection_name) -> Chroma:
        db = Chroma(persist_directory=self.chroma_path, embedding_function=get_embedding_function(), collection_name=collection_name)

        return db
    
    def clear_collection(self, collection_name):
        try:
            db_client = PersistentClient(path=self.chroma_path)
            db_client.delete_collection(collection_name)
            print(f"Collection {collection_name} deleted successfully.")
        except Exception as e:
            raise Exception(f"Unable to delete collection: {e}")