from kink import di

from musicdl.common import ResponsibilityChainFactory
from musicdl.downloader.classes.metadata_embedders import (
    FLACMetadataEmbedder,
    M4AMetadataEmbedder,
    MP3MetadataEmbedder,
    OGGMetadataEmbedder,
    OpusMetadataEmbedder,
)
from musicdl.downloader.interfaces import BaseMetadataEmbedder, BaseProgressLogger
from musicdl.downloader.progress_handler import ProgressLoggerProxy
from musicdl.providers.audio import init_di as add_audio_providers


def init_di():
    add_audio_providers()

    di[BaseProgressLogger] = ProgressLoggerProxy
    di[BaseMetadataEmbedder] = lambda di: (
        ResponsibilityChainFactory()
        .add(di[MP3MetadataEmbedder])
        .add(di[M4AMetadataEmbedder])
        .add(di[FLACMetadataEmbedder])
        .add(di[OGGMetadataEmbedder])
        .add(di[OpusMetadataEmbedder])
        .build()
    )
