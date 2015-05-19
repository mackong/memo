#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time

from termcolor import colored, cprint
import click

from __init__ import __version__

# Default .memo file path.
DEFAULT_MEMO_PATH = os.path.expanduser('~/.memo')

# Default .memorc file path.
DEFAULT_MEMORC_PATH = os.path.expanduser('~/.memorc')

# Default memo file path environment variable.
DEFAULT_MEMO_PATH_ENV = 'MEMO_PATH'

# Default memorc file path environment variable.
DEFAULT_MEMORC_PATH_ENV = 'MEMORC_PATH'


class NoteStatus:
    """The note status."""
    DONE = 'D'
    UNDONE = 'U'
    POSTPONED = 'P'
    

class Note:
    """This representaion a note taken.

    Note have the following properties:
         id: The note id.
         status: The note status. see NoteStatus.
         date: The note taking date, format is yyyy-MM-dd.
         content: The note content.
    """
    def __init__(self, id, status, date, content):
        self.id = id
        self.status = status
        self.date = date
        self.content = content

    def __str__(self):
        return '%d\t%s\t%s\t%s' % (self.id,
                                      self.status,
                                      self.date,
                                      self.content.rstrip('\n'))

    def trim_date(self):
        """Get the note string without date attribute."""
        return '%d\t%s\t%s' % (self.id,
                                 self.status,
                                 self.content.rstrip('\n'))

    
def is_odd(x):
    """Return True if x is odd, False if x is even."""
    return x % 2


def get_current_date():
    """Get current date in format yyyy-MM-dd"""    
    return time.strftime('%Y-%m-%d')    


def get_memorc_path():
    """Get the .memorc file path"""
    return os.getenv(DEFAULT_MEMORC_PATH_ENV, DEFAULT_MEMORC_PATH)


def get_memo_conf_value(prop):
    """Get config value of givin property from .memorc file.

    The .memorc file format is like `prop=value`.
    """
    with open(get_memorc_path(), 'r') as f:
        for line in f.read().splitlines():
            tokens = [x.strip() for x in line.split('=')]
            if tokens[0] == prop:
                return tokens[1]

    return None


def get_memo_path():
    """Get the .memo file path"""
    path = os.getenv(DEFAULT_MEMO_PATH_ENV)
    path = path if path else get_memo_conf_value('MEMO_PATH')
    path = path if path else DEFAULT_MEMO_PATH
    return path


def get_next_memo_id():
    """Get the next new note id."""    
    notes = get_all_notes()
    if not len(notes):
        return 1
    else:
        notes.sort(key=lambda note: note.id)
        return notes[-1].id + 1


def get_all_notes():
    """Get all notes currently taken."""
    with open(get_memo_path(), 'r') as f:
        notes = []
        for line in f:
            tokens = line.split('\t')
            note = Note(int(tokens[0]),
                        tokens[1],
                        tokens[2],
                        '\t'.join(tokens[3:]))
            notes.append(note)

        return notes
    

def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    
    print('Memo version: ' + colored(__version__, 'red'))
    ctx.exit()


def print_memo_path(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    print('Memo path: ' + colored(get_memo_path(), 'red'))
    ctx.exit()    


def organize_notes(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return

    ctx.exit()


def add_note(content, date):
    with open(get_memo_path(), 'a') as f:
        note = Note(get_next_memo_id(), NoteStatus.UNDONE, date, content)
        f.write(note)


def add_note_from_input(input):
    while True:
        line = input.readline()
        if not line:
            break

        add_note(line, get_current_date())


def validate_date(ctx, param, value):
    """Validate the date format.

    the date format must be in format yyyy-MM-dd, ex. 2014-12-01.
    """
    error_msg = 'date must be in format yyyy-MM-dd'
    
    try:
        tokens = [int(x) for x in value.split('-')]
        if len(tokens) != 3:
            raise click.BadParameter(error_msg)

        (year, month, day) = tokens
        day_count = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if year % 400 == 0 or (year % 100 != 0 and year % 4 == 0):
            day_count[1] = 29;

        if month < 13 and month > 0:
            if day < day_count[month - 1]:
                return value
            else:
                raise click.BadParameter(error_msg)
        else:
            raise click.BadParameter(error_msg)
    except ValueError:
        raise click.BadParameter(error_msg)
            

@click.command()
@click.option('--content', '-c', metavar='content',
              help='The note content to add.')
@click.option('--date', '-d', metavar='yyyy-MM-dd',
              default=get_current_date(), callback=validate_date,
              help='The note date to add, Default is now.')
@click.argument('input', type=click.File('rb'), required=False, default='-')
def add(content, date, input):
    """Add note from options or stdin."""
    if content:
        add_note(content, date)
    else:
        add_note_from_input(input)


def get_line_color(is_odd_line):
    """Get the color of LINE_COLOR or ODD_LINE_COLOR in .memorc.

    Return None if USE_COLORS is set to false.
    """
    use_colors = get_memo_conf_value('USE_COLORS')
    
    if not use_colors or use_colors == 'no':
        return None

    color = get_memo_conf_value('ODD_LINE_COLOR' if is_odd_line else 'LINE_COLOR')
    if not color:
        color = 'blue' if is_odd_line else 'magenta' # default color

    return color


def dump_note(note, is_odd_line):
    cprint(note, get_line_color(is_odd_line))


def dump_organized(date, notes, is_odd_line):
    color = get_line_color(is_odd_line)
    cprint(date, color)
    for note in notes:
        cprint('\t%s' % note.trim_date(), color)
    

def show_notes():
    notes = get_all_notes()
    if len(notes):
        for i, note in enumerate(notes):
            dump_note(note, is_odd(i))
    else:
        cprint('You don\'t have any notes currently.', 'red')

def show_latest(n):
    notes = get_all_notes()
    if len(notes):
        for i, note in enumerate(notes[n + 1:]):
            dump_note(note, is_odd(i))
    else:
        cprint('You don\'t have any notes currently.', 'red')
            
def show_organized():
    notes = get_all_notes()
    if len(notes):
        organized = {}
        for note in notes:
            if note.date in organized:
                organized[note.date].append(note)
            else:
                organized[note.date] = [note]

        for i, key in enumerate(organized):
            dump_organized(key, organized[key], is_odd(i))
    else:
        cprint('You don\'t have any notes currently.', 'red')

def show_unpostponed():
    notes = get_all_notes()
    if len(notes):
        for i, note in enumerate(notes):
            if note.status != NoteStatus.POSTPONED:
                dump_note(note, is_odd(i))
    else:
        cprint('You don\'t have any notes currently.', 'red')

def show_undone():
    notes = get_all_notes()
    if len(notes):
        for i, note in enumerate(notes):
            if note.status == NoteStatus.UNDONE:
                dump_note(note, is_odd(i))
    else:
        cprint('You don\'t have any notes currently.', 'red')
        
            
@click.command()
@click.option('--latest', '-l', default=0, metavar='n',
              help='Show latest n notes.')
@click.option('--organized', '-o', is_flag=True,
              help='Show all notes organized by date.')
@click.option('--unpostponed', '-s', is_flag=True,
              help='Show all notes except postponed.')
@click.option('--undone', '-u', is_flag=True,
              help='Show only undone notes.')
def show(latest, organized, unpostponed, undone):
    """Show the notes already taken."""
    if latest:
        show_latest(latest)
    elif organized:
        show_organized()
    elif unpostponed:
        show_unpostponed()
    elif undone:
        show_undone()
    else:
        show_notes()

@click.command()
@click.option('--all', '-a', is_flag=True,
              help='Delete all notes.')
@click.argument('id', required=False)
def delete(all, id):
    """Delete note by id or delete all notes."""
    print(all, id)

# Context setting for Click command.
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True,
              help='Show memo version and exit.')
@click.option('--memopath', '-p', is_flag=True, callback=print_memo_path,
              expose_value=False, is_eager=True,
              help='Show current memo file path.')
@click.option('--organize', '-o', is_flag=True, callback=organize_notes,
              expose_value=False, is_eager=True,
              help='Reorder and organize note id codes.')
def main():
    """Python tool to take notes in command line."""
    memo_path = get_memo_path()
    try:
        open(memo_path)
    except IOError:
        open(memo_path, 'w')


main.add_command(add)
main.add_command(show)
main.add_command(delete)

if __name__ == '__main__':
    main()
