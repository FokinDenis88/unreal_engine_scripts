import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(os.path.join(WORKING_DIR, os.pardir), os.pardir)
sys.path.append(os.path.abspath(PARENT_DIR))

import unreal

import unreal_engine_scripts.external.python_library.src.general as general

import importlib
importlib.reload(general)
from unreal_engine_scripts.external.python_library.src.general import *


def Name_to_str(name_text):
    return unreal.StringLibrary.build_string_name('', '', name_text, '')