from promptflow import tool
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

@tool
def get_video_transcripts(video_list: list) -> list:
    video_transcripts = []
    for video in video_list:
        video_id = video["videoId"]
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text_segments = [segment['text'] for segment in transcript]
            video_transcript = ' '.join(text_segments)
            video["transcript"] = video_transcript
            video_transcripts.append(video)
        except TranscriptsDisabled:
            # Skip appending this video if transcripts are disabled
            continue
    return video_transcripts
