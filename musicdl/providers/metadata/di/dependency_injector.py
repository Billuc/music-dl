from kink import di

from musicdl.common import SongList
from musicdl.common.classes import PipelineFactory
from musicdl.providers.metadata.classes import SpotifyTrackMetadataProvider, SpotifyAlbumMetadataProvider, SpotifyPlaylistMetadataProvider
from musicdl.providers.metadata.interfaces import BaseMetadataProvider

def init_di():
    di[BaseMetadataProvider] =  lambda di: (
        PipelineFactory[str, SongList]()
            .add(di[SpotifyTrackMetadataProvider])
            .add(di[SpotifyAlbumMetadataProvider])
            .add(di[SpotifyPlaylistMetadataProvider])
            .build()
    )