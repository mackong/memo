#!/usr/bin/python


from termcolor import colored, cprint
import click

import common


def get_line_color(is_odd_line):
    """Get the color of LINE_COLOR or ODD_LINE_COLOR in .memorc.

    Return None if USE_COLORS is set to false.
    """
    use_colors = common.get_memo_conf_value('USE_COLORS')
    
    if not use_colors or use_colors == 'no':
        return None

    color = common.get_memo_conf_value('ODD_LINE_COLOR' if is_odd_line else 'LINE_COLOR')
    if not color:
        color = 'blue' if is_odd_line else 'magenta' # default color

    return color


def dump_note(note, is_odd_line):
    cprint(note, get_line_color(is_odd_line))


def dump_organized(date, notes, is_odd_line):
    color = get_line_color(is_odd_line)
    cprint(date, color)
    for note in notes:
        cprint('\t%s\t%s\t%s' % (common.get_note_id(note),
                                 common.get_note_status(note),
                                 common.get_note_content(note)),
               color)
    

def show_notes():
    notes = common.get_all_notes()
    if len(notes):
        for i, note in enumerate(notes):
            dump_note(note, common.is_odd(i))
    else:
        cprint('You don\'t have any notes currently.', 'red')

def show_latest(n):
    notes = common.get_all_notes()
    if len(notes):
        for i, note in enumerate(notes[n + 1:]):
            dump_note(note, common.is_odd(i))
    else:
        cprint('You don\'t have any notes currently.', 'red')
            
def show_organized():
    notes = common.get_all_notes()
    if len(notes):
        organized = {}
        for note in notes:
            date = common.get_note_date(note)
            if date in organized:
                organized[date].append(note)
            else:
                organized[date] = [note]

        for i, key in enumerate(organized):
            dump_organized(key, organized[key], common.is_odd(i))

            
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
        print('Show unpostponed')
    elif undone:
        print('Show undone')
    else:
        show_notes()
