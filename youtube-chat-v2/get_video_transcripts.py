from promptflow import tool
from youtube_transcript_api import YouTubeTranscriptApi

@tool
def get_video_transcripts(video_list: list) -> dict:
    video_transcripts = {}
    for video in video_list:
        video_id = video["videoId"]
        video_title = video["title"]  # Get the video title from the video dictionary
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            video_transcripts[video_id] = {
                "title": video_title,  # Add the video title to the dictionary
                "transcript": transcript
            }
        except:
            pass
    return video_transcripts