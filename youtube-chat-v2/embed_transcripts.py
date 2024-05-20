from promptflow import tool
import openai
import os
import faiss
import numpy as np
from promptflow.connections import AzureOpenAIConnection, OpenAIConnection

@tool
def embed_transcripts(connection: OpenAIConnection, video_transcripts: dict, index_path: str, chunk_size: int = 500) -> bool:
    # Get the OpenAI API key from the environment variable
    api_key = connection.api_key
    openai.api_key = api_key

    # Initialize the FAISS index
    d = 1536  # Dimension of Ada 002 embeddings
    index = faiss.IndexFlatL2(d)

    # Check if the index and segment info mappings exist
    if os.path.exists(index_path + "/segment_id_to_info.npy"):
        segment_id_to_info = np.load(index_path + "/segment_id_to_info.npy", allow_pickle=True).item()
        segment_index_to_id = np.load(index_path + "/segment_index_to_id.npy").tolist()
    else:
        segment_id_to_info = {}
        segment_index_to_id = []

    embeddings = []  # List to store all the embeddings

    for video_id, video_data in video_transcripts.items():
        # Check if the video ID is already in the segment info mappings
        if video_id in [info['video_id'] for info in segment_id_to_info.values()]:
            #print(f"Video ID {video_id} is already in the index. Skipping embedding.")
            continue

        video_title = video_data["title"]
        segments = video_data["transcript"]

        chunk_text = ""
        chunk_start = None
        chunk_duration = 0

        for segment in segments:
            segment_text = segment['text']
            if len(chunk_text.split()) + len(segment_text.split()) <= chunk_size:
                chunk_text += " " + segment_text
                chunk_duration += segment['duration']
                if chunk_start is None:
                    chunk_start = segment['start']
            else:
                try:
                    response = openai.embeddings.create(
                        input=[chunk_text.strip()],
                        model="text-embedding-ada-002"
                    )
                    embedding = response.data[0].embedding
                    embeddings.append(embedding)  # Append the embedding to the list
                    segment_info = {
                        'video_id': video_id,
                        'video_title': video_title,
                        'start': chunk_start,
                        'duration': chunk_duration,
                        'text': chunk_text.strip()
                    }
                    segment_id_to_info[len(segment_index_to_id)] = segment_info
                    segment_index_to_id.append(len(segment_index_to_id))
                except Exception as e:
                    print(f"Error processing segment: {chunk_text.strip()}")
                    print(e)
                chunk_text = segment_text
                chunk_start = segment['start']
                chunk_duration = segment['duration']

        # Process the last chunk for the current video
        if chunk_text.strip():
            try:
                response = openai.embeddings.create(
                    input=[chunk_text.strip()],
                    model="text-embedding-ada-002"
                )
                embedding = response.data[0].embedding
                embeddings.append(embedding)  # Append the last embedding to the list
                segment_info = {
                    'video_id': video_id,
                    'video_title': video_title,
                    'start': chunk_start,
                    'duration': chunk_duration,
                    'text': chunk_text.strip()
                }
                segment_id_to_info[len(segment_index_to_id)] = segment_info
                segment_index_to_id.append(len(segment_index_to_id))
            except Exception as e:
                print(f"Error processing segment: {chunk_text.strip()}")
                print(e)

    # Check if there are any new embeddings to add
    if len(embeddings) > 0:
        # Create the embeddings matrix
        embeddings_matrix = np.array(embeddings, dtype=np.float32)

        # Check if the FAISS index exists
        if os.path.exists(index_path + "/index.faiss"):
            # Load the existing index
            index_id_map = faiss.read_index(index_path + "/index.faiss")
        else:
            # Create an IndexIDMap using the empty index
            index_id_map = faiss.IndexIDMap(index)

        # Add the embeddings and IDs to the index_id_map
        index_id_map.add_with_ids(embeddings_matrix, np.array(segment_index_to_id[-len(embeddings):], dtype=np.int64))

        # Save the FAISS index and the segment info mappings to disk
        faiss.write_index(index_id_map, index_path + "/index.faiss")
        np.save(index_path + "/segment_id_to_info.npy", segment_id_to_info, allow_pickle=True)
        np.save(index_path + "/segment_index_to_id.npy", segment_index_to_id)
    else:
        #print("All videos are already indexed. No new embeddings to add.")
        True
    return True