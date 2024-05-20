from promptflow import tool
from youtube_transcript_api import YouTubeTranscriptApi

@tool
def my_python_tool(video_id: str) -> str:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text_segments = [segment['text'] for segment in transcript]
    return ' '.join(text_segments)