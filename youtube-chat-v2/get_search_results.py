import re
import json
import bs4
import requests
from urllib.parse import quote
from promptflow.core import tool
from youtube_transcript_api import YouTubeTranscriptApi

def decode_str(string):
    return string.encode().decode("unicode-escape").encode("latin1").decode("utf-8")

def remove_nested_parentheses(string):
    pattern = r"\([^()]*\)"
    while re.search(pattern, string):
        string = re.sub(pattern, "", string)
    return string

@tool
def get_youtube_videos(searchString: str, count=10):
    # URL encode the search string
    encoded_search_string = quote(searchString)
    
    # Send a request to the URL
    url = f"https://au.youtube.com/results?search_query={encoded_search_string}"
    video_list = []
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = bs4.BeautifulSoup(response.text, "html.parser")

            # Find the script containing the ytInitialData
            script_tag = soup.find("script", text=lambda t: t and "ytInitialData" in t)
            if script_tag:
                script_content = script_tag.string
                # Extract the JSON data from the script
                json_data = json.loads(script_content[script_content.index("{"):script_content.rindex("}") + 1])

                # Find the videoRenderer objects in the JSON data
                video_renderers = find_video_renderers(json_data)
                for renderer in video_renderers[:count]:
                    video_id = renderer["videoId"]
                    video_title = decode_str(renderer["title"]["runs"][0]["text"])
                    video_title = remove_nested_parentheses(video_title)
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    video_length = renderer["lengthText"]["simpleText"] if "lengthText" in renderer else "N/A"
                    published_time = renderer["publishedTimeText"]["simpleText"] if "publishedTimeText" in renderer else "N/A"
                    video_list.append({
                        "title": video_title,
                        "url": video_url,
                        "videoId": video_id,
                        "length": video_length,
                        "publishedTime": published_time
                    })
            else:
                print("Script containing ytInitialData not found.")
        else:
            msg = (
                f"Get YouTube videos failed with status code {response.status_code}.\nURL: {url}\nResponse: "
                f"{response.text[:100]}"
            )
            print(msg)
    except Exception as e:
        print("Get YouTube videos failed with error: {}".format(e))
    return video_list

def find_video_renderers(json_data):
    if isinstance(json_data, dict):
        if "videoRenderer" in json_data:
            return [json_data["videoRenderer"]]
        video_renderers = []
        for value in json_data.values():
            video_renderers.extend(find_video_renderers(value))
        return video_renderers
    elif isinstance(json_data, list):
        video_renderers = []
        for item in json_data:
            video_renderers.extend(find_video_renderers(item))
        return video_renderers
    return []