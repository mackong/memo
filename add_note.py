#!/usr/bin/python

import click

import common

def add_note(content, date):
    with open(common.get_memo_path(), 'a') as f:
        if content[-1] == '\n':
            content = content[:-1]
        f.write('%d\t%s\t%s\t%s\n' % (common.get_next_memo_id(), 'U', date, content))


def add_note_from_input(input):
    while True:
        line = input.readline()
        if not line:
            break

        add_note(line, common.get_current_date())

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
              default=common.get_current_date(), callback=validate_date,
              help='The note date to add, Default is now.')
@click.argument('input', type=click.File('rb'), required=False, default='-')
def add(content, date, input):
    """Add note from options or stdin."""
    if content:
        add_note(content, date)
    else:
        add_note_from_input(input)
