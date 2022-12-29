from kink import di

# from musicdl.providers.audio.classes import YoutubeDLClientProvider
from musicdl.providers.audio.interfaces import BaseAudioProvider

def init_di():
    di[BaseAudioProvider] = di[]