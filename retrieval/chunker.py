from langchain.schema.document import Document

def calculate_chunk_ids(chunks: list[Document]):
    """
    Calculates and sets the chunk ids for all chunks.
    Chunk id consists of page_id:chunk_number_on_page

    Parameters
    ----------
    chunks: list[Document]
        The list of chunks that need an ID.

    Returns
    -------
    chunks: list[Document]
        The list of chunks with an id added to their metadata.

    """
    current_chunk_index = 0
    last_page_id = None

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        #check if still on same page in the document or not
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks