#!/usr/bin/env python3
import click
from magerestore.config import Config


@click.group()
@click.pass_context
def main(ctx):
    ctx.config = Config().from_json('magerestore.json')


@click.command()
@click.pass_context
def restore(ctx):
    pass


main.add_command(restore)

if __name__ == '__main__':
    main()
