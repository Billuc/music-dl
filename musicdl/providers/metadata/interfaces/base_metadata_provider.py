from musicdl.common import SongList, BasePipeline


# TODO : what I could do is use composition rather than inheritance
# BaseMetadataProvider would then have an implentation which has
# a dependency on BasePipeline[str, SongList] and the Pipeline
# would be injected. We then provide an exec method to execute
# the pipeline.
class BaseMetadataProvider(BasePipeline[str, SongList]):
    def __init__(self) -> None:
        super().__init__()
