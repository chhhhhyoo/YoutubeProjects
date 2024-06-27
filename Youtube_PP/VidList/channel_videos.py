import youtube_api_auth
from googleapiclient.errors import HttpError
from util.yt_api_calls import execute_with_retries


def get_channel_videos(channel_id, api_key):
    youtube = youtube_api_auth.get_authenticated_service(api_key)
    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        )
        try:
            response = execute_with_retries(request)
        except HttpError as e:
            print(f"Failed to fetch videos: {e}")
            break

        if response:
            videos += response['items']
            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break
        else:
            break

    return videos
