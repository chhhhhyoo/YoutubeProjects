import youtube_api_auth
from util.yt_api_calls import execute_with_retries


def get_video_comments(video_id, api_key):
    youtube = youtube_api_auth.get_authenticated_service(api_key)
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,  # Adjust as needed
            pageToken=next_page_token
        )
        response = execute_with_retries(request, wait_time=30)

        if response:
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
        else:
            break

    return comments
