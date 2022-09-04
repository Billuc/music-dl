from musicdl.exec.classes import QueryOptions


def init_command(options: QueryOptions) -> None:
    if options.has_special_args():
        #skip config stuff
        #skip ffmpeg check
        #skip saved in query check
        return None