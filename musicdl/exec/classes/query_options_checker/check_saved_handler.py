from kink import inject
from musicdl.common import MusicDLException, BaseResponsibilityChainLink
from musicdl.exec.data import QueryOptions

@inject
class CheckSavedHandler(BaseResponsibilityChainLink[QueryOptions]):
    def exec(self, options: QueryOptions) -> bool:
        if options.query and "saved" in options.query and not options.user_auth:
            raise MusicDLException(
                "You must be logged in to use the saved query. "
                "Log in by adding the --user-auth flag"
            )

        return False