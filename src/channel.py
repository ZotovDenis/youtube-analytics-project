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
        self.channel_id = channel_id

    def print_info(self):
        """Выводит в консоль информацию о канале в формате JSON с отступами"""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        channel_json = json.dumps(channel, indent=2, ensure_ascii=False)
        print(channel_json)
