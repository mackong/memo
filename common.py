#!/usr/bin/python

import os
import time


# Default .memo file path.
DEFAULT_MEMO_PATH = os.path.expanduser('~/.memo')

# Default .memorc file path.
DEFAULT_MEMORC_PATH = os.path.expanduser('~/.memorc')

# Default memo file path environment variable.
DEFAULT_MEMO_PATH_ENV = 'MEMO_PATH'

# Default memorc file path environment variable.
DEFAULT_MEMORC_PATH_ENV = 'MEMORC_PATH'

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

def get_note_id(note):
    return note.split('\t')[0]

def get_note_status(note):
    return note.split('\t')[1]    

def get_note_date(note):
    return note.split('\t')[2]

def get_note_content(note):
    return '\t'.join(note.split('\t')[3:])

def get_next_memo_id():
    notes = get_all_notes()
    ids = [int(get_note_id(note)) for note in notes]
    if not len(ids):
        return 1
    else:
        ids.sort()
        return ids[-1] + 1

def get_all_notes():
    with open(get_memo_path(), 'r') as f:
        notes = f.read().splitlines()
    return notes
