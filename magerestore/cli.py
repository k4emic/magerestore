#!/usr/bin/env python3
# use absolute imports to allow pycharm to run/debug
import click
import sys
from magerestore.app import Magerestore


pass_app = click.make_pass_decorator(Magerestore)


def validate_resource_name(ctx, param, value):
    names = ctx.obj.resource_manager.names()
    if value not in names:
        raise click.BadParameter("Invalid resource name `{value}` ({names})".format(value=value, names=', '.join(names)))
    return value


@click.group()
@click.pass_context
@click.option('--debug', is_flag=True)
@click.option('--config', type=click.Path(dir_okay=False, exists=True), default='magerestore.json', help="Config file to use")
def main(ctx, debug, config):
    try:
        ctx.obj = Magerestore(config)
    except Exception as e:
        click.secho("Error: %s" % str(e).strip('\''), err=True, fg='white', bg='red')
        if debug:
            raise e
        else:
            sys.exit(1)


@click.command()
@pass_app
@click.argument('resource', callback=validate_resource_name)
def restore(app, resource):
    resource = app.resource_manager.find(resource)
    resource.get_resource(get_resource_callback)
    # resource.import_resource()
    # resource.cleanup()


def get_resource_callback(got, total_size):
    func = get_resource_callback
    if not hasattr(func, 'progressbar'):
        func.progressbar = click.progressbar(length=total_size, label="Getting resource file")
        func.last_got = 0

    progress = got - func.last_got
    func.last_got = got
    func.progressbar.update(progress)

main.add_command(restore)

if __name__ == '__main__':
    main()
