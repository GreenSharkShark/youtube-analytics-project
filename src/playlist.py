from src.youtube_object_maker import YouTubeObjectMaker
from datetime import timedelta


import isodate


class PlayList:
    def __init__(self, playlist_id):
        self.__youtube = YouTubeObjectMaker().make_youtube_object()
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.playlists_info = self.__youtube.playlists().list(part='snippet', id=self.playlist_id).execute()
        self.title = self.playlists_info['items'][0]['snippet']['title']
        self.playlists_videos = self.__youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                                    maxResults=50, ).execute()

    def return_video_ids_in_playlist(self):
        """
        Метод нужен только для избежания дублирования кода внутри класса
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlists_videos['items']]
        return video_ids

    @property
    def total_duration(self):
        video_ids = self.return_video_ids_in_playlist()
        video_response = self.__youtube.videos().list(part='contentDetails,statistics',
                                                      id=','.join(video_ids)).execute()

        durations = []
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            durations.append(duration)
        total_duration = sum(durations, timedelta())
        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на видео из плейлиста с наибольшим количеством лайков
        """
        video_ids = self.return_video_ids_in_playlist()
        videos_response = self.__youtube.videos().list(part='statistics', id=','.join(video_ids),
                                                       maxResults=50).execute()
        video_likes = [(item['id'], int(item['statistics']['likeCount'])) for item in videos_response['items']]
        video_likes_sorted = sorted(video_likes, key=lambda x: x[1], reverse=True)
        return f'https://youtu.be/{video_likes_sorted[0][0]}'
