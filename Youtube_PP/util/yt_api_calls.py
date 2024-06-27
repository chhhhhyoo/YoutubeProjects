import time
from googleapiclient.errors import HttpError


def execute_with_retries(api_request, max_retries=5, wait_time=10):
    retries = 0
    while retries < max_retries:
        try:
            response = api_request.execute()
            return response
        except HttpError as e:
            error_message = e._get_reason()
            if 'quotaExceeded' in error_message:
                print("Quota exceeded. Exiting...")
                raise e
            retries += 1
            if retries >= max_retries:
                print("Maximum retry limit reached. Exiting...")
                raise e
            print(f"An error occurred: {e}")
            print(f"Retrying after {wait_time} seconds...")
            time.sleep(wait_time)
    return None
