import unreal

import unreal_engine_python_scripts.config as config
import unreal_engine_python_scripts.service.general as general
import unreal_engine_python_scripts.service.file as file

import importlib
importlib.reload(config)
importlib.reload(general)
importlib.reload(file)


LOGS_DIR = '\\logs\\'
FINAL_RESULTS = 'Final results: '

LOG_NAME_NO_MIPMAPS = 'no_mipmaps.log'
LOG_NAME_NO_LODS = 'no_lods.log'
LOG_NAME_FIND_ASSETS = 'find_assets.log'
LOG_NAME_SET_PROPERTIES = 'no_lods.log'
LOG_NAME_NO_COLLISION = 'no_collision.log'

LOG_PATH_NO_MIPMAPS = config.WORKING_DIR + LOGS_DIR + LOG_NAME_NO_MIPMAPS
LOG_PATH_NO_LODS = config.WORKING_DIR + LOGS_DIR + LOG_NAME_NO_LODS
LOG_PATH_FIND_ASSETS = config.WORKING_DIR + LOGS_DIR + LOG_NAME_FIND_ASSETS
LOG_PATH_SET_PROPERTIES = config.WORKING_DIR + LOGS_DIR + LOG_NAME_SET_PROPERTIES
LOG_PATH_NO_COLLISION = config.WORKING_DIR + LOGS_DIR + LOG_NAME_NO_COLLISION


def log_print_n_write_file(path, text, open_mode = 'a'):
    unreal.log(text)
    file.write_text_file(path, str(text) + '\n', open_mode)

def log_list(list_of_objects):
    if general.is_not_none_or_empty(list_of_objects):
        for object in list_of_objects:
            unreal.log(object)
    else:
        unreal.log_error(log_list.__name__ + '(): list_of_variables must not be None or Empty')