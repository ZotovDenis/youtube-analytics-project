import datetime
import os

import isodate
from googleapiclient.discovery import build

from src.video import Video


class PlayList:
    """Класс для плейлиста YouTube-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        """Инициилизируемся по id плейлиста"""
        self.playlist_id = playlist_id

        playlist_response = self.youtube.playlists().list(part='snippet', id=playlist_id).execute()
        playlist_items = playlist_response['items']
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]

        self.title = playlist_items[0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        """Обрабатываем все видео в плейлисте и возвращаем длительность плейлиста"""

        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()
        total_duration = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            durations = isodate.parse_duration(iso_8601_duration)
            total_duration += durations

        return total_duration

    def show_best_video(self):
        """Определяем в плейлисте видео с самым большим количеством лайков и выводим ссылку на него"""

        best_video = 0
        url_best_video = ''
        for video_id in self.video_ids:
            video = Video(video_id)
            if int(video.like_count) >= best_video:
                best_video = int(video.like_count)
                url_best_video = video.video_url
        return url_best_video
