from dotenv import load_dotenv
import os


def configure():
    load_dotenv('.env')


configure()
api_key = os.getenv('API_KEY')
