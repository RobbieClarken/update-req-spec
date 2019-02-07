import click

from .config import Config
from .exceptions import RepinException
from .update import update_file


@click.command()
@click.option("--index-url")
@click.argument("file")
def main(file, index_url):
    cli_options = {"--index-url": index_url} if index_url else {}
    config = Config(cli_options=cli_options)
    try:
        update_file(file, config)
    except RepinException as exc:
        raise SystemExit(str(exc))
