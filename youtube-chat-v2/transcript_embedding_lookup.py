from promptflow import tool
import faiss
import numpy as np
import openai
from promptflow.connections import AzureOpenAIConnection, OpenAIConnection

@tool
def search_segments(connection: OpenAIConnection, query: str, index_path: str, transcripts_ready: bool, similarity_threshold: float = 0.8, num_results: int = 5) -> list:
    api_key = connection.api_key
    openai.api_key = api_key

    # Load the FAISS index
    index_id_map = faiss.read_index(index_path + "/index.faiss")

    # Load the segment info mappings
    segment_id_to_info = np.load(index_path + "/segment_id_to_info.npy", allow_pickle=True).item()
    segment_index_to_id = np.load(index_path + "/segment_index_to_id.npy").tolist()

    # Embed the query using OpenAI's Ada 002 model
    response = openai.embeddings.create(
        input=[query],
        model="text-embedding-ada-002"
    )
    query_embedding = response.data[0].embedding

    # Convert the query embedding to a numpy array
    query_embedding = np.array(query_embedding, dtype=np.float32).reshape(1, -1)

    # Perform the similarity search
    distances, indices = index_id_map.search(query_embedding, num_results)

    # Filter the results based on the similarity threshold
    filtered_indices = [idx for idx, dist in zip(indices[0], distances[0]) if dist <= 1 - similarity_threshold]

    # Retrieve the video ID, video title, start time, and embedded text for the filtered segments
    results = []
    for idx in filtered_indices:
        segment_id = segment_index_to_id[idx]
        segment_info = segment_id_to_info[segment_id]
        video_id = segment_info['video_id']
        video_title = segment_info['video_title']
        start_time = segment_info['start']
        embedded_text = segment_info['text']
        results.append({
            'video_id': video_id,
            'video_title': video_title,
            'start_time': start_time * 100,
            'embedded_text': embedded_text
        })

    return results