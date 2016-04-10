#!/usr/bin/env python3
import click
from .app import Magerestore


pass_app = click.make_pass_decorator(Magerestore)


@click.group()
@click.pass_context
def main(ctx):
    ctx.obj = Magerestore('magerestore.json')


@click.command()
@pass_app
def restore(app):
    pass


main.add_command(restore)

if __name__ == '__main__':
    main()
