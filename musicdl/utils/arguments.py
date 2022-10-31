
class SmartFormatter(argparse.HelpFormatter):
    """
    Class that overrides the default help formatter.
    """

    def _split_lines(self, text: str, width: int) -> List[str]:
        """
        Split the text in multiple lines if a line starts
        with a N|
        """

        if text.startswith("N|"):
            return text[2:].splitlines()

        text = self._whitespace_matcher.sub(" ", text).strip()

        return textwrap.wrap(text, width)


def parse_arguments() -> Namespace:
    """
    Parse arguments from the command line.

    ### Returns
    - A Namespace object containing the parsed arguments.
    """

    # Initialize argument parser
    parser = ArgumentParser(
        prog="spotdl",
        description="Download your Spotify playlists and songs along with album art and metadata",
        formatter_class=SmartFormatter,
        epilog=(
            "For more information, visit https://spotdl.github.io/spotify-downloader/ "
            "or join our Discord server: https://discord.com/invite/xCa23pwJWY"
        ),
    )