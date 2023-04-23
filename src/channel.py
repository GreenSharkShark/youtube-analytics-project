import os
import json


from googleapiclient.discovery import build


# API key for YouTube
api_key: str = os.getenv('YouTube_API')

# специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['localized']['description']
        self.url = channel['items'][0]['snippet']['customUrl']
        self.subscribers_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']


    @classmethod
    def get_service(cls):
        """
        Создает экземпляр класса
        """
        object = build('youtube', 'v3', developerKey=api_key)
        return object

    @property
    def channel_id(self):
        """
        Геттер для атрибута channel_id
        :return:
        """
        return self.__channel_id


    @property
    def to_json(self):
        """
        Функция для записи инфрмации о канале в json файле. Функция генерирует название файла
        автоматически из названия канала.
        """
        obj = Channel.get_service()
        content = obj.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        with open(f'{self.title}.json', 'w') as file:
            json.dump(content, file)



    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        # print(channel)
        return channel