"""Implementation of the ``bibcode entry`` command.
"""

__all__ = ('entry',)

import asyncio

import aiohttp
import click
import pyperclip
from uritemplate import expand

ADS_FORMATS = [
    'bibtex',
    'bibtexabs',
    'ads',
    'endnote',
    'procite',
    'ris',
    'refworks',
    'rss',
    'medlars',
    'dcxml',
    'refxml',
    'refabsxml',
    'aastex',
    'icarus',
    'mnras',
    'soph',
    'votable',
    'custom',
]


@click.command()
@click.argument(
    'bibcode', default=None, required=True, nargs=1,
)
@click.option(
    '-f', '--format', default='aastex',
    help='Format of the bibliographic entry. Default is ``aastex``.',
    type=click.Choice(ADS_FORMATS)
)
@click.option(
    '--custom-format', default='%m %Y',
    help='If using a ``custom`` format, specify this format. See '
         'http://adsabs.github.io/help/actions/export for details.'
)
@click.option(
    '--copy/--no-copy', 'clipboard', default=True,
    help='Copy the entry to the clipboard.'
)
@click.pass_context
def entry(ctx, bibcode, format, custom_format, clipboard):
    """Convert a bibcode into a bibliographic entry.

    **Formats**

    - BibTeX: ``bibtex``
    - BibTeX ABS: ``bibtexabs``
    - ADS: ``ads``
    - EndNote: ``endnote``
    - ProCite: ``procite``
    - RIS: ``ris``
    - RefWorks: ``refworks``
    - RSS: ``rss``
    - MEDLARS: ``medlars``
    - DC-XML: ``dcxml``
    - REF-XML: ``refxml``
    - REFABS-XML: ``refabsxml``
    - AASTeX: ``aastex``
    - Icarus: ``icarus``
    - MNRAS: ``mnras``
    - Solar Physics: ``soph``
    - VOTable: ``votable``
    - Custom format: ``custom`` (see ``--custom-format`` option)
    """
    token = ctx.obj['token']
    if token is None:
        click.UsageError('An ADS API token is required. See ``bibcode -h`` '
                         'for details.')

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        _run(bibcode, format, custom_format, token))

    click.echo(result)

    if clipboard:
        pyperclip.copy(result)
        click.echo('📎 Copied to clipboard')


async def _run(bibcode, format, custom_format, token):
    headers = {"Authorization": "Bearer {}".format(token)}
    async with aiohttp.ClientSession(headers=headers) as session:
        request_json = {
            'bibcode': [bibcode],
        }
        if format == 'custom':
            request_json['format'] = custom_format

        url = 'https://api.adsabs.harvard.edu/v1/export{/format}'

        async with session.post(expand(url, format=format),
                                json=request_json) as response:

            data = await response.json()
            if response.status >= 300:
                raise click.UsageError('Error: {}'.format(data['error']))

            return data['export']
