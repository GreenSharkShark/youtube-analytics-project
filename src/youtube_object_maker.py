import os

from googleapiclient.discovery import build


class YouTubeObjectMaker:
    def __init__(self):
        self.api_key = os.getenv('YouTube_API')  # API key for YouTube

    def make_youtube_object(self):
        youtube_object = build('youtube', 'v3', developerKey=self.api_key)
        return youtube_object
