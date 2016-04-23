#!/usr/bin/env python3
# use absolute imports to allow pycharm to run/debug
import click
import sys
from magerestore.app import Magerestore


pass_app = click.make_pass_decorator(Magerestore)


def validate_resource_name(ctx, param, value):
    names = ctx.obj.resources.names()
    if value not in names:
        raise click.BadParameter("Invalid resource name `{value}` ({names})".format(value=value, names=', '.join(names)))
    return value


@click.group()
@click.pass_context
@click.option('--debug', is_flag=True)
@click.option('--config', type=click.Path(dir_okay=False, exists=True))
def main(ctx, debug, config):
    print(config)
    try:
        ctx.obj = Magerestore('magerestore.json')
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
    resource = app.resources.find(resource)
    for step in resource.steps:
        click.secho(step['title'], fg='green')
        step['method']()


main.add_command(restore)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# use absolute imports to allow pycharm to run/debug
import click
import sys
from magerestore.app import Magerestore


pass_app = click.make_pass_decorator(Magerestore)


def validate_resource_name(ctx, param, value):
    names = ctx.obj.resources.names()
    if value not in names:
        raise click.BadParameter("Invalid resource name `{value}` ({names})".format(value=value, names=', '.join(names)))
    return value


@click.group()
@click.pass_context
@click.option('--debug', is_flag=True)
@click.option('--config', type=click.Path(dir_okay=False, exists=True), default='magerestore.json', help="Config file to use ")
def main(ctx, debug, config):
    print(config)
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
    resource = app.resources.find(resource)
    for step in resource.steps:
        click.secho(step['title'], fg='green')
        step['method']()


main.add_command(restore)

if __name__ == '__main__':
    main()
