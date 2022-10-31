from kink import inject
from musicdl.common import MusicDLException, BaseFfmpegHelper, BaseResponsibilityChainLink
from musicdl.exec.data import QueryOptions
from musicdl.exec.extensions import has_special_args

@inject
class HasSpecialArgsHandler(BaseResponsibilityChainLink[QueryOptions]):    
    def exec(self, options: QueryOptions) -> bool:
        if (has_special_args(options)):
            return True # Abort check if the options have special args

        return False