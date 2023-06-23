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

## Write to console what old and new file name
def rename_asset(old_path, new_path, has_log = True):
    if (old_path is not None and new_path is not None and
        old_path != '' and new_path != ''):
        if unreal.EditorAssetLibrary.does_asset_exist(old_path):
            if not unreal.EditorAssetLibrary.does_asset_exist(new_path):
                unreal.EditorAssetLibrary.rename_asset(old_path, new_path)
                if has_log:
                    unreal.log(Name_to_str(old_path) + ' -> ' + Name_to_str(new_path))
            else:
                unreal.log_error(rename_asset.__name__ + '(): there is asset in new_path')
        else:
            unreal.log_error(rename_asset.__name__ + '(): old_path asset does not exists')
    else:
        unreal.log_error(rename_asset.__name__ + '(): old_path, new_path must not be None or Empty')