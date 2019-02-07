import click

from .exceptions import RepinException
from .repin import Config, repin_file


@click.command()
@click.option("--index-url")
@click.argument("file")
def main(file, index_url):
    cli_options = {"--index-url": index_url} if index_url else {}
    config = Config(cli_options=cli_options)
    try:
        repin_file(file, config)
    except RepinException as exc:
        raise SystemExit(str(exc))
