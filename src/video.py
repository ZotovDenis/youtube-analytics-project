import os

from googleapiclient.discovery import build


class Video:
    """Инициализацию реальными данными атрибутов экземпляра класса Video"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        try:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id
                                                    ).execute()
            self.video_title: str = video_response['items'][0]['snippet']['title']
            self.video_url: str = f'https://youtu.be/{self.video_id}'
            self.view_count: int = video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = video_response['items'][0]['statistics']['likeCount']
        except Exception:
            self.video_title = self.video_url = self.video_url = self.view_count = self.like_count = None

    def __str__(self):
        """Возвращаем название видео"""
        return self.video_title


class PLVideo(Video):
    """Инициализацию реальными данными атрибутов экземпляра класса PLVideo, наследника класса Video"""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
