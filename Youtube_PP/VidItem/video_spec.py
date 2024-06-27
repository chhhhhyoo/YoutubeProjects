import youtube_api_auth as youtube_api_auth
import time


def get_video_comments(video_id, api_key):
    youtube = youtube_api_auth.get_authenticated_service(api_key)
    comments = []
    next_page_token = None

    while True:
        try:
            request = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=3,  # Max comments to collect
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'videoId': video_id,
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'publishedAt': comment['publishedAt']
                })

            next_page_token = response.get('nextPageToken')

            if not next_page_token:
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying after 3 seconds...")
            time.sleep(3)  # Retry after 3 seconds

    return comments
