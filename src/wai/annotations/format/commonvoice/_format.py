"""
Defines the external CommonVoice format.
"""
from typing import Optional

from ...domain.audio import AudioInfo


class CommonVoiceFormat:
    def __init__(self,
                 file: AudioInfo,
                 client_id: str,
                 sentence: str,
                 up_votes: int,
                 down_votes: int,
                 age: Optional[int],
                 gender: Optional[str],
                 accent: Optional[str],
                 locale: str,
                 segment: str):
        self._file: AudioInfo = file
        self._client_id: str = client_id
        self._sentence: str = sentence
        self._up_votes: int = up_votes
        self._down_votes: int = down_votes
        self._age: Optional[int] = age
        self._gender: Optional[str] = gender
        self._accent: Optional[str] = accent
        self._locale: str = locale
        self._segment: str = segment

    @property
    def file(self) -> AudioInfo:
        return self._file

    @property
    def client_id(self) -> str:
        return self._client_id

    @property
    def sentence(self) -> str:
        return self._sentence

    @property
    def up_votes(self) -> int:
        return self._up_votes

    @property
    def down_votes(self) -> int:
        return self._down_votes

    @property
    def age(self) -> Optional[int]:
        return self._age

    @property
    def gender(self) -> Optional[str]:
        return self._gender

    @property
    def accent(self) -> Optional[str]:
        return self._accent

    @property
    def locale(self) -> str:
        return self._locale

    @property
    def segment(self) -> str:
        return self._segment
