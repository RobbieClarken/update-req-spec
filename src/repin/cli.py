import click

from .repin import Config, repin_file


@click.command()
@click.option("--index-url")
@click.argument("file")
def main(file, index_url):
    config = Config(cli_options={"--index-url": index_url})
    repin_file(file, config)
