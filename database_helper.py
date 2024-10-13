import os
import shutil
from typing import Any

from langchain_chroma import Chroma

from langchain.schema.document import Document

from chunker import calculate_chunk_ids
from embedding import get_embedding_function


class DatabaseHelper:
    chroma_path: str = "chroma" #folder where chroma db is stored

    def __init__(self,model: str, file_path: str ="./data"):
        self.file_path = file_path
        self.model = model

        if not os.path.exists(self.file_path):
            try:
                os.makedirs(self.file_path)
            except Exception as e:
                print(f"Error creating directory '{self.file_path}': {e}")

    def add_to_chroma(self, chunks: list[Document]) -> None:
        db: Chroma = Chroma(persist_directory=self.chroma_path, embedding_function=get_embedding_function(self.model))

        # Calculate Page IDs.
        chunks_with_ids: chunks = calculate_chunk_ids(chunks)

        # Add or Update the documents.
        existing_items:  dict[str, Any] = db.get(include=[])  # IDs are always included by default
        existing_ids: set = set(existing_items["ids"])
        print(f"Number of existing documents in DB: {len(existing_ids)}")

        # Only add documents that don't exist in the DB.
        new_chunks: list[Document] = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)

        total_new_chunks = len(new_chunks)  # Count new chunks
        if total_new_chunks > 0:
            print(f"Adding new documents: {total_new_chunks}")

            new_chunk_ids: list[Document] = [chunk.metadata["id"] for chunk in new_chunks]

            #debug start_time = time.time()  # Start timing

            for idx, (chunk, chunk_id) in enumerate(zip(new_chunks, new_chunk_ids)):
                db.add_documents([chunk], ids=[chunk_id])  # Add one chunk at a time

                # Print progress
                print(f"Progress: {idx + 1}/{total_new_chunks} chunks added.")

            #debug end_time = time.time()  # End timing
            #debug print(f"Time taken to save documents: {end_time - start_time:.2f} seconds")

    def clear_database(self):
        if os.path.exists(self.chroma_path):
            shutil.rmtree(self.chroma_path)

    def get_db(self) -> Chroma:
        return Chroma(persist_directory=self.chroma_path, embedding_function=get_embedding_function())