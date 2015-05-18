#!/usr/bin/python

import sys
from termcolor import colored, cprint
import click

import common
import add_note
import show_note

__VERSION__ = '1.6'


def setup():
    """Setup the environment"""
    memo_path = common.get_memo_path()
    try:
        open(memo_path)
    except IOError:
        open(memo_path, 'w')


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    
    print('Memo version: ' + colored(__VERSION__, 'red'))
    ctx.exit()


def print_memo_path(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    print('Memo path: ' + colored(common.get_memo_path(), 'red'))
    ctx.exit()    


# Context setting for Click command.
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Show memo version and exit.')
@click.option('--memopath', '-p', is_flag=True, callback=print_memo_path,
              expose_value=False, is_eager=True,
              help='Show current memo file path.')
def main():
    """Python tool to take notes in command line."""
    setup()


main.add_command(add_note.add)
main.add_command(show_note.show)


if __name__ == '__main__':
    main()
