import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для YouTube-канала"""

    api_key: str = os.getenv('YT_API_KEY')

    # Создаем специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется по id канала."""
        self.__channel_id = channel_id
        channel_info = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel_info['items'][0]['snippet']['title']
        self.description = channel_info['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.subscribers_count = channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count = channel_info['items'][0]['statistics']['videoCount']
        self.view_count = channel_info['items'][0]['statistics']['viewCount']

    def print_info(self):
        """Выводит в консоль информацию о канале в формате JSON-строки с отступами"""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        channel_json = json.dumps(channel, indent=2, ensure_ascii=False)
        print(channel_json)

    @classmethod
    def get_service(cls):
        """Возвращает экземпляр класса для работы с API"""
        return cls.youtube

    @property
    def channel_id(self):
        """Возвращает id канала"""
        return self.__channel_id

    def to_json(self, filename):
        """Создаем JSON-файл со внесением значений атрибутов экземпляра"""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.__dict__, file, ensure_ascii=False)
