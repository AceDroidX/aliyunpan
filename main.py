#!/usr/bin/env python3
import click
from click_aliases import ClickAliasedGroup

from aliyunpan.cli.cli import Commander


@click.group(cls=ClickAliasedGroup)
@click.help_option('-h', '--help')
@click.version_option(version='1.1.0')
@click.option('-c', '--config-file', type=click.Path(), help='Specify the configuration file.',
              default='~/.config/aliyunpan.yaml', show_default=True)
@click.option('-t', 'refresh_token', type=str, help='Specify REFRESH_TOKEN.')
@click.option('-u', 'username', type=str, help='Specify USERNAME.')
@click.option('-p', 'password', type=str, help='Specify PASSWORD.')
@click.option('-d', '--depth', type=int, help='File recursion depth.', default=3, show_default=True)
def cli(config_file, refresh_token, username, password, depth):
    if refresh_token:
        commander.init(refresh_token=refresh_token, depth=depth)
    elif username:
        commander.init(username=username, password=password, depth=depth)
    elif config_file:
        commander.init(config_file=config_file, depth=depth)
    else:
        raise FileNotFoundError(f'Configuration file not found.')


@cli.command(aliases=['l', 'list', 'dir'], help='List files.')
@click.help_option('-h', '--help')
@click.argument('path', type=click.Path(), default='root')
@click.option('-l', is_flag=True, help='View details.')
def ls(path, l):
    commander.ls(path, l)


@cli.command(aliases=['delete', 'del'], help='Delete Files.')
@click.help_option('-h', '--help')
@click.argument('path', type=click.Path())
def rm(path):
    commander.rm(path)


@cli.command(aliases=['move'], help='Move files.')
@click.help_option('-h', '--help')
@click.argument('path', type=click.Path())
@click.argument('target_path', type=click.Path())
def mv(path, target_path):
    commander.mv(path, target_path)


@cli.command(aliases=['u'], help='Upload files.')
@click.help_option('-h', '--help')
@click.argument('path', type=click.Path(), default='')
@click.option('-p', '--file', multiple=True, help='Select multiple files.', type=click.Path())
@click.argument('upload_path', default='root')
@click.option('-t', '--time-out', type=float, help='Upload timeout.', default=10.0, show_default=True)
@click.option('-r', '--retry', type=int, help='number of retries.', default=3, show_default=True)
@click.option('-f', '--force', is_flag=True, help='Force overlay file.')
def upload(path, file, upload_path, time_out, retry, force):
    if not path and not file:
        raise click.MissingParameter(param=click.get_current_context().command.params[2])
    else:
        path_list = set((*file, path))
    commander.upload(path_list, upload_path, time_out, retry, force)


@cli.command(aliases=['m'], help='Create folder.')
@click.help_option('-h', '--help')
@click.argument('path', type=click.Path(), default='')
def mkdir(path):
    commander.mkdir(path)


@cli.command(aliases=['d'], help='Download files.')
@click.help_option('-h', '--help')
@click.argument('path', type=click.Path(), default='')
@click.option('-p', '--file', multiple=True, help='Select multiple files.', type=click.Path())
@click.argument('save_path', type=click.Path(), default='')
def download(path, file, save_path):
    if not path and not file:
        raise click.MissingParameter(param=click.get_current_context().command.params[2])
    else:
        file_list = {*file, path}

    commander.download(file_list, save_path)


@cli.command(aliases=['t', 'show'], help='View file tree.')
@click.help_option('-h', '--help')
@click.argument('path', type=click.Path(), default='root')
def tree(path):
    commander.tree(path)


@cli.command(aliases=['s'], help='Share file download link.')
@click.help_option('-h', '--help')
@click.argument('path', type=click.Path(), default='')
@click.option('-f', '--file-id', type=str, default='', help='File id.')
@click.option('-t', '--expire-sec', type=int, default=14400, help='Link expiration time(Max 14400).', show_default=True)
def share(path, file_id, expire_sec):
    if path or file_id:
        commander.share(path, file_id, expire_sec)
    else:
        raise click.MissingParameter(param=click.get_current_context().command.params[1])


if __name__ == '__main__':
    commander = Commander()
    cli()
