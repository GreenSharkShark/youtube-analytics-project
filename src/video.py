import os


from googleapiclient.discovery import build


# API key for YouTube
api_key: str = os.getenv('YouTube_API')

# специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)

# комментарии к этому коду будут излишни, я считаю.
class Video:
    def __init__(self, video_id):
        self.response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()
        self.name = self.response['items'][0]['snippet']['title']
        self.link = f'https://www.youtube.com/watch?v=9lO06Zxhu88{video_id}'
        self.view_count = self.response['items'][0]['statistics']['viewCount']
        self.likes = self.response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.name


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.play = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails', maxResults=50,).execute()

    def __str__(self):
        return self.name
