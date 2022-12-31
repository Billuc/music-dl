from typing import Dict
from kink import di

from musicdl.common import PipelineFactory
from musicdl.providers.audio.data import DownloadSongCommand
from musicdl.providers.audio.classes import SavedSongAudioProvider, YoutubeMusicAudioProvider, YoutubeAudioProvider
from musicdl.providers.audio.interfaces import BaseAudioProvider

def init_di():
    di[BaseAudioProvider] = lambda di: (
        PipelineFactory[DownloadSongCommand, Dict]()
            .add(di[SavedSongAudioProvider])
            .add(di[YoutubeMusicAudioProvider])
            .add(di[YoutubeAudioProvider])
            .build()
    )