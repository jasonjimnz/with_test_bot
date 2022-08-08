import os
from typing import List, NamedTuple, Text
from urllib.parse import quote, urljoin
from httpx import Client

API_BASE = os.getenv("API_BASE", "https://framex-dev.wadrid.net/api/")
VIDEO_NAME = os.getenv(
    "VIDEO_NAME", "Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c"
)


class Video(NamedTuple):
    """
    That's a video from the API
    """

    name: Text
    width: int
    height: int
    frames: int
    frame_rate: List[int]
    url: Text
    first_frame: Text
    last_frame: Text


class VideoUtils(object):
    video = VIDEO_NAME
    BASE_URL = API_BASE

    def __init__(self):
        pass

    @classmethod
    def get_client(cls, timeout: int = 90) -> Client:
        """
        Returns a HttpClient instance
        :param timeout: Timeout in seconds for the HTTP Request
        :return:
        """
        return Client(timeout=timeout)

    @classmethod
    def video_frame(cls, frame: int) -> bytes:
        """
        Returns video frame binary bytes
        :param frame: Frame that should be returned from the video
        :return:
        """
        r = cls.get_client().get(
            urljoin(
                cls.BASE_URL,
                f'video/{quote(cls.video)}/frame/{quote(f"{frame}")}/'
            )
        )
        r.raise_for_status()
        return r.content

    @classmethod
    def video_frame_url(cls, frame: int) -> str:
        """
        Returns the url of the video frame
        :param frame: Frame that should be returned from the video
        :return:
        """
        return urljoin(
            cls.BASE_URL,
            f'video/{quote(cls.video)}/frame/{quote(f"{frame}")}/'
        )

    @classmethod
    def get_video(cls) -> Video:
        """
        Returns a Video instance object with the metadata
        of the file
        :return:
        """
        r = cls.get_client().get(
            urljoin(
                cls.BASE_URL,
                f"video/{quote(cls.video)}/"
            )
        )
        r.raise_for_status()
        return Video(**r.json())
