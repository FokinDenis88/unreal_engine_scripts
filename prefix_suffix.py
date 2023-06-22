import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(os.path.join(WORKING_DIR, os.pardir), os.pardir)
sys.path.append(os.path.abspath(PARENT_DIR))

import python_library.src.general as general

import importlib
importlib.reload(general)

import re


PREFIX_REGEX = '^[^_]+_'
SUFFIX_REGEX = '_[^_]+\\Z'

def get_prefix(text):
    if general.is_not_none_or_empty(text):
        match_object = re.search(PREFIX_REGEX, text)
        if match_object is not None:
            return match_object[0]
    return ''

def get_suffix(text):
    if general.is_not_none_or_empty(text):
        match_object = re.search(SUFFIX_REGEX, text)
        if match_object is not None:
            return match_object[0]
    return ''

def add_prefix(text, prefix):
    if (general.is_not_none_or_empty_lists([text, prefix]) and
        not text.startswith(prefix)):
        text = prefix + text
    return text

def add_suffix(text, suffix):
    if (general.is_not_none_or_empty_lists([text, suffix]) and
        not text.endswith(suffix)):
        text = text + suffix
    return text