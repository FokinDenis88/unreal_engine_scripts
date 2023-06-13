import unreal

import unreal_engine_scripts.config as config
import unreal_engine_scripts.service.general as general
import unreal_engine_scripts.service.file as file

import importlib
importlib.reload(config)
importlib.reload(general)
importlib.reload(file)


LOGS_DIR = '\\logs\\'
FINAL_RESULTS = 'Final results: '

LOG_NAME_NO_MIPMAPS = 'no_mipmaps.log'
LOG_NAME_NO_LODS = 'no_lods.log'
LOG_NAME_FIND_ASSETS = 'find_assets.log'
LOG_NAME_SET_PROPERTIES = 'set_properties.log'
LOG_NAME_NO_COLLISION = 'no_collision.log'

LOG_PATH_NO_MIPMAPS = config.WORKING_DIR + LOGS_DIR + LOG_NAME_NO_MIPMAPS
LOG_PATH_NO_LODS = config.WORKING_DIR + LOGS_DIR + LOG_NAME_NO_LODS
LOG_PATH_FIND_ASSETS = config.WORKING_DIR + LOGS_DIR + LOG_NAME_FIND_ASSETS
LOG_PATH_SET_PROPERTIES = config.WORKING_DIR + LOGS_DIR + LOG_NAME_SET_PROPERTIES
LOG_PATH_NO_COLLISION = config.WORKING_DIR + LOGS_DIR + LOG_NAME_NO_COLLISION


def log_print_n_write_file(path, text, open_mode = 'a'):
    if general.is_not_none_lists([path, text]):
        unreal.log(text)
        file.write_text_file(path, str(text) + '\n', open_mode)
    else:
        unreal.log_error(log_print_n_write_file.__name__ + '(): path, text must not be None')

def log_list(list_of_objects):
    if general.is_not_none_or_empty(list_of_objects):
        for object in list_of_objects:
            unreal.log(object)
    else:
        unreal.log_error(log_list.__name__ + '(): list_of_variables must not be None or Empty')


def write_assets_data_log(assets_data, log_path, log_title = 'Assets Data: ', file_open_mode = 'w'):
    if general.is_not_none_or_empty_lists([assets_data, log_path]):
        log_print_n_write_file(log_path, log_title + ': ', file_open_mode)
        for asset_data in assets_data :
            object_path = asset_data.get_editor_property('object_path')
            log_print_n_write_file(log_path, object_path)
        unreal.log('')
    else:
        unreal.log_error(write_assets_data_log.__name__ + '(): assets_data or log_path must not be None or Empty')