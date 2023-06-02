import json


class Channel:
    """Класс для YouTube-канала"""

    import os
    from googleapiclient.discovery import build

    api_key: str = os.getenv('YT_API_KEY')

    # Создаем специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется по id канала."""
        self.__channel_id = channel_id
        self.title = None
        self.description = None
        self.url = None
        self.subscribers_count = None
        self.video_count = None
        self.view_count = None

        # Вызываем метод для присвоения новых данных атрибутам
        self.assign_data()

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

    def get_channel_self(self):
        """Метод для получения URL канала"""
        return f'https://www.youtube.com/channel/{self.channel_id}'

    def assign_data(self):
        """Возвращает информацию о канале и присваивает значения атрибутам экземпляра"""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = self.get_channel_self()
        self.subscribers_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def to_json(self, filename):
        """Создаем JSON-файл со внесением значений атрибутов экземпляра"""
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.__dict__, file, ensure_ascii=False)
