from VidList import channel_videos
from VidItem import video_spec
from dotenv import load_dotenv
import os
import pandas as pd


def configure():
    load_dotenv('.env')


if __name__ == '__main__':
    configure()
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API_KEY not found in environment variables.")

    channel_id = os.getenv('CHANNEL_ID')
    if not channel_id:
        raise ValueError("CHANNEL_ID not found in environment variables.")

    videos = channel_videos.get_channel_videos(channel_id, api_key)

    all_comments = []
    for video in videos:
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']
        print(f"Fetching comments for video: {video_title}")

        comments = video_spec.get_video_comments(video_id, api_key)
        all_comments.extend(comments)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(all_comments)
    print(df.shape)
    print(df.head())
    df['date'] = pd.to_datetime(df['publishedAt'], errors='coerce')
    df['just_date'] = df['date'].dt.date
    df.to_csv('./tinas_comments.csv', index=False)
