import youtube_api_auth as youtube_api_auth
import time


def get_channel_videos(channel_id, api_key):
    youtube = youtube_api_auth.get_authenticated_service(api_key)
    videos = []
    next_page_token = None

    while True:
        try:
            request = youtube.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=3,  # Max videos to collect
                pageToken=next_page_token
            )
            response = request.execute()

            videos += response['items']
            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying after 3 seconds...")
            time.sleep(3)  # Retry after 3 seconds

    return videos
