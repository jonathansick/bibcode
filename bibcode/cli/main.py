"""Command line entrypoint for ``bibcode``.
"""

__all__ = ('main',)

import click

from .entry import entry

# Add -h as a help shortcut option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--token',
    envvar='ADS_KEY',
    help='Your ADS API token. You can also set this the $ADS_KEY environment '
         'variable.'
)
@click.pass_context
def main(ctx, token):
    """bibcode helps you work with NASA/SAO ADS bibcodes from the command line.
    """
    # Subcommands should use the click.pass_obj decorator to get this
    # ctx.obj object as the first argument.
    ctx.obj = {
        'token': token
    }


@main.command()
@click.argument('topic', default=None, required=False, nargs=1)
@click.pass_context
def help(ctx, topic, **kw):
    """Show help for any command.
    """
    # The help command implementation is taken from
    # https://www.burgundywall.com/post/having-click-help-subcommand
    if topic is None:
        click.echo(ctx.parent.get_help())
    else:
        click.echo(main.commands[topic].get_help(ctx))


main.add_command(entry)
