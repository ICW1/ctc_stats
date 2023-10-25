import os
import pandas as pd
import requests

from pytube import Channel
from tqdm import tqdm
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

def get_video_description(api_key, video_url):
    video_id = video_url.split("=")[-1]
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"

    response = requests.get(url)
    response_json = response.json()

    video_description = response_json["items"][0]["snippet"]["description"]

    return video_description


def get_youtube_videos_dataset_by_channel(channel_url, api_key):
    c = Channel(channel_url)

    index=0
    results = {}
    print(f"Getting video descriptions and captions... for YouTube channel: {c.channel_name}")
    videos = c.videos
    for vid in tqdm(videos):
        vid_id = vid.video_id
        vid_url = f"https://www.youtube.com/watch?v={vid_id}"
        vid_date = vid.publish_date

        vid_desc = get_video_description(api_key, vid_url)

        try:
            captions = YouTubeTranscriptApi.get_transcript(vid_id)
        except TranscriptsDisabled:
            captions = []
            
        vid_captions = (' ').join([item['text'] for item in captions])

        results[index] = {
            "video_id": vid_id,
            "date": vid_date,
            "description": vid_desc,
            "captions": vid_captions
        }
        index+=1

    print("Done!")

    return results


def get_youtube_videos_dataset_by_channel_to_csv(channel_url, api_key, output_dir="./data"):
    results = get_youtube_videos_dataset_by_channel(channel_url, api_key)
    df = pd.DataFrame.from_dict(results, orient='index')
    df.to_csv(os.path.join(output_dir, "youtube_videos.csv"), index=False)


if __name__ == "__main__":
    API_KEY = os.environ["YOUTUBE_API_KEY"]
    CHANNEL_URL = "https://www.youtube.com/c/CrackingTheCryptic"
    get_youtube_videos_dataset_by_channel_to_csv(CHANNEL_URL, API_KEY)