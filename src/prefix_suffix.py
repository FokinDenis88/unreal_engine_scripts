import re

import unreal

import unreal_scripts.config as config
import unreal_scripts.service.general as general
import unreal_scripts.src.get_asset as get_asset
import unreal_scripts.src.naming_convention as convention

import importlib
importlib.reload(config)
importlib.reload(general)
importlib.reload(get_asset)
importlib.reload(convention)

IS_WORKING_TEXT = ' is Working.'


# \/:*?"<>|+
WINDOWS_RESTRICTED_CHARS = '\\/:*?\"<>|+'
# In the end of file name: space and .

WINDOWS_RESTRICTED_CHARS_END = ' .'
UNIX_RESTRICTED_CHARS = '/\\0'
REGEX_WINDOWS_RESTRICTED_CHARS = '[' + WINDOWS_RESTRICTED_CHARS + ']'
REGEX_WINDOWS_RESTRICTED_CHARS_END = '[' + WINDOWS_RESTRICTED_CHARS_END + ']\\Z'

NO_TEXTURE_TYPE = 'None'

PREFIX_REGEX = '^[^_]+_'
SUFFIX_REGEX = '_[^_]+\\Z'


def has_restricted_chars_for_os(str, show_log = False):
    if str != '':
        if re.search(REGEX_WINDOWS_RESTRICTED_CHARS, str) == None:
            if re.search(REGEX_WINDOWS_RESTRICTED_CHARS_END, str) == None:
                return False
            elif show_log:
                unreal.log_error(has_restricted_chars_for_os.__name__ + '(): file name must not end on chars: space or .')
                return True
        elif show_log:
            unreal.log_error(has_restricted_chars_for_os.__name__ + '(): file name must not has chars: \\/:*?"<>|+')
            return True
    else:
        return False

def get_prefix(text):
    match_object = re.search(PREFIX_REGEX, text)
    if match_object is not None:
        return match_object[0]
    else:
        return ''

def get_suffix(text):
    match_object = re.search(SUFFIX_REGEX, text)
    if match_object is not None:
        return match_object[0]
    else:
        return ''

## @return (str) name of asset without prefix and suffix, without extension.
def get_asset_name_without_prefix_suffix(object_path):
    if general.is_not_none_or_empty(object_path):
        file_name_no_extension = unreal.Paths.get_base_filename(object_path)
        # (?<=^[^_]+_).+(?=_[^_]+)
        #regex_pattern = '(?<=^[^_]+_).+(?=_[^_]+)'  # '\\Z'
        regex_pattern = '^[^_]+_(?P<name>.+)_[^_]+'     # \\Z
        match_object = re.search(regex_pattern, file_name_no_extension)
        if match_object is not None:
            return match_object.group('name')
        else:
            unreal.log(get_asset_name_without_prefix_suffix.__name__ + ': regex did not find any name without prefix or suffix')
            return file_name_no_extension
    else:
        unreal.log_error(get_asset_name_without_prefix_suffix.__name__ + ': object_path must not be None or empty')
        return ''

def get_asset_name_without_prefix_suffix_data(data_asset):
    if data_asset is not None:
        return get_asset_name_without_prefix_suffix(get_asset.get_asset_data_object_path(data_asset))
    else:
        return ''

## @param file_name without extension: T_Texture_Diff
# @return tuple (prefix, suffix)
def get_asset_prefix_suffix_by_name(file_name_no_extension):
    prefix, suffix = '', ''
    if file_name_no_extension != '':
        prefix_regex = PREFIX_REGEX
        match_object = re.search(prefix_regex, file_name_no_extension)
        if match_object != None:
            prefix = match_object[0]

        suffix_regex = SUFFIX_REGEX
        match_object = re.search(suffix_regex, file_name_no_extension)
        if match_object != None:
            suffix = match_object[0]
    else:
        unreal.log_error(get_asset_prefix_suffix_by_name.__name__ + '(): file_name is empty. ' + file_name_no_extension)

    return prefix, suffix

def get_asset_prefix_suffix_by_path(object_path):
    return get_asset_prefix_suffix_by_name(get_asset.get_asset_name_no_extension(object_path))

## @param file_name File name without extension, without path
def has_file_name_prefix(file_name,  prefix, has_logs = False):
    if file_name != '':
        if prefix != '':
            prefix_regex = '^' + prefix
            if re.search(prefix_regex, file_name) != None:
                return True
            else:
                return False

        elif has_logs:
            unreal.log(has_file_name_prefix.__name__ + '(): prefix is empty')
    elif has_logs:
        unreal.log_error(has_file_name_prefix.__name__ + '(): file_name is empty. ' + file_name)

## @param file_name File name without extension, without path
def has_file_name_suffix(file_name, suffix, has_logs = False):
    if file_name != '':
        if suffix != '':
            suffix_regex = suffix + '\\Z'
            if re.search(suffix_regex, file_name) != None:
                return True
            else:
                return False

        elif has_logs:
            unreal.log(has_file_name_suffix.__name__ + '(): suffix is empty')
    elif has_logs:
        unreal.log_error(has_file_name_suffix.__name__ + '(): file_name is empty. ' + file_name)

## @param file_name File name without extension, without path
def add_prefix_suffix_in_name(file_name,  prefix = '', suffix = ''):
    if file_name != '':
        if prefix != '' or suffix != '':
            new_name = file_name
            # Add prefix or suffix, if file name doesn't contain this prefix or suffix
            if not has_file_name_prefix(new_name, prefix):
                new_name = prefix + new_name
            if not has_file_name_suffix(new_name, suffix):
                new_name = new_name + suffix

            return new_name
        else:
            unreal.log_error(add_prefix_suffix_in_name.__name__ + '(): prefix or suffix are empty. ' + file_name)
    else:
        unreal.log_error(add_prefix_suffix_in_name.__name__ + '(): file_name is empty')

def get_path_with_prefix_suffix(object_path,  prefix = '', suffix = ''):
    if object_path != '':
        if prefix != '' or suffix != '':
            origin_name = get_asset.get_asset_name_no_extension(object_path)
            new_name = origin_name
            new_name = add_prefix_suffix_in_name(new_name, prefix, suffix)

            if new_name != origin_name:
                return get_asset.get_asset_path_with_new_name(object_path, new_name)
            else:
                return object_path

        else:
            unreal.log_error(get_path_with_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(get_path_with_prefix_suffix.__name__ + '(): object_path is empty')

## @param file_name File name without extension, without path
def delete_prefix_suffix_in_name(file_name,  prefix = '', suffix = ''):
    if file_name != '':
        if prefix != '' or suffix != '':
            new_name = file_name
            # Add prefix or suffix, if file name doesn't contain this prefix or suffix
            if has_file_name_prefix(new_name, prefix):
                new_name = new_name[len(prefix) :]
            if has_file_name_suffix(new_name, suffix):
                new_name = new_name[: len(new_name) - len(suffix)]

            return new_name
        else:
            unreal.log_error(delete_prefix_suffix_in_name.__name__ + '(): prefix or suffix are empty. ' + file_name)
    else:
        unreal.log_error(delete_prefix_suffix_in_name.__name__ + '(): file_name is empty')

## Get name without prefix or suffix
def get_path_without_prefix_suffix(object_path,  prefix = '', suffix = ''):
    if object_path != '':
        if prefix != '' or suffix != '':
            origin_name = get_asset.get_asset_name_no_extension(object_path)
            new_name = origin_name
            new_name = delete_prefix_suffix_in_name(new_name, prefix, suffix)

            if new_name != origin_name:
                return get_asset.get_asset_path_with_new_name(object_path, new_name)
            else:
                return object_path

        else:
            unreal.log_error(get_path_without_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(get_path_without_prefix_suffix.__name__ + '(): object_path is empty')



## Get path for replace_prefix_suffix() function
def get_path_replaced_by_prefix_suffix(object_path,  prefix = '', suffix = '',
                                       new_prefix = '', new_suffix = ''):
    if object_path != '':
        if prefix != '' or suffix != '':
            origin_name = get_asset.get_asset_name_no_extension(object_path)
            new_name = origin_name
            # Add prefix or suffix, if file name doesn't contain this prefix or suffix
            new_name = delete_prefix_suffix_in_name(new_name, prefix, suffix)
            new_name = new_prefix + new_name + new_suffix
            return get_asset.get_asset_path_with_new_name(object_path, new_name)

        else:
            unreal.log_error(get_path_replaced_by_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(get_path_replaced_by_prefix_suffix.__name__ + '(): object_path is empty')


## @param is_folder_operation    indicates if it is adding prefix_suffix for many files in folder
def add_prefix_suffix(object_path, prefix = '', suffix = '', is_folder_operation = False,
                      include_only_on_disk_assets = False):
    if object_path != '':
        if prefix != '' or suffix != '':
            if (not has_restricted_chars_for_os(prefix)) and (not has_restricted_chars_for_os(suffix)):
                new_path = get_path_with_prefix_suffix(object_path, prefix, suffix)
                if new_path != object_path:
                    # When prefix suffix is applying to many files in folder, there mustn't be transaction on each file
                    if not is_folder_operation:
                        with unreal.ScopedEditorTransaction(add_prefix_suffix.__name__) as ue_transaction:
                            unreal.EditorAssetLibrary.rename_asset(object_path, new_path)
                    else:
                        unreal.EditorAssetLibrary.rename_asset(object_path, new_path)

                else:
                    unreal.log(add_prefix_suffix.__name__ + '(): asset file already has prefix or suffix. ' + general.Name_to_str(object_path))
            else:
                unreal.log_error(add_prefix_suffix.__name__ + '(): prefix or suffix has restricted chars')
        else:
            unreal.log_error(add_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(add_prefix_suffix.__name__ + '(): object_path is empty')

## @param is_folder_operation    indicates if it is adding prefix_suffix for many files in folder
def delete_prefix_suffix(object_path, prefix = '', suffix = '', is_folder_operation = False,
                         include_only_on_disk_assets = False):
    if object_path != '':
        if prefix != '' or suffix != '':
            new_path = get_path_without_prefix_suffix(object_path, prefix, suffix)
            if new_path != object_path:
                # When prefix suffix is applying to many files in folder, there mustn't be transaction on each file
                if not is_folder_operation:
                    with unreal.ScopedEditorTransaction(delete_prefix_suffix.__name__) as ue_transaction:
                        unreal.EditorAssetLibrary.rename_asset(object_path, new_path)
                else:
                    unreal.EditorAssetLibrary.rename_asset(object_path, new_path)

            else:
                unreal.log(delete_prefix_suffix.__name__ + '(): asset file already has no prefix or suffix. ' + general.Name_to_str(object_path))
        else:
            unreal.log_error(delete_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(delete_prefix_suffix.__name__ + '(): object_path is empty')

def delete_prefix_suffix_data(asset_data, prefix = '', suffix = '', is_folder_operation = False,
                         include_only_on_disk_assets = False):
    delete_prefix_suffix(asset_data.get_editor_property('object_path'), prefix, suffix, is_folder_operation,
                         include_only_on_disk_assets)

def delete_prefix_suffix_datas(assets_data, prefix = '', suffix = '', is_folder_operation = False,
                               include_only_on_disk_assets = False):
    for asset_data in assets_data:
        delete_prefix_suffix(asset_data.get_editor_property('object_path'), prefix, suffix, is_folder_operation,
                             include_only_on_disk_assets)

## @param is_folder_operation    indicates if it is adding prefix_suffix for many files in folder
def replace_prefix_suffix(object_path, prefix = '', suffix = '', new_prefix = '', new_suffix = '',
                          is_folder_operation = False, include_only_on_disk_assets = False):
    if object_path != '':
        if prefix != '' or suffix != '':
            if (not has_restricted_chars_for_os(prefix)) and (not has_restricted_chars_for_os(suffix)) and (
                not has_restricted_chars_for_os(new_prefix)) and (not has_restricted_chars_for_os(new_suffix)):

                new_path = get_path_replaced_by_prefix_suffix(object_path, prefix, suffix, new_prefix, new_suffix)
                if new_path != object_path:
                    # When prefix suffix is applying to many files in folder, there mustn't be transaction on each file
                    if not is_folder_operation:
                        with unreal.ScopedEditorTransaction(replace_prefix_suffix.__name__) as ue_transaction:
                            unreal.EditorAssetLibrary.rename_asset(object_path, new_path)
                    else:
                        unreal.EditorAssetLibrary.rename_asset(object_path, new_path)

                else:
                    unreal.log(replace_prefix_suffix.__name__ + '(): asset file already has no prefix or suffix. ' + general.Name_to_str(object_path))

            else:
                unreal.log_error(replace_prefix_suffix.__name__ + '(): prefix, suffix, new_prefix or new_suffix has restricted chars')
        else:
            unreal.log_error(replace_prefix_suffix.__name__ + '(): prefix and suffix are empty')
    else:
        unreal.log_error(replace_prefix_suffix.__name__ + '(): object_path is empty')


def add_prefix_suffix_folder(folder_paths, prefix = '', suffix = '',
                             recursive = False, include_only_on_disk_assets = False):
    with unreal.ScopedEditorTransaction(add_prefix_suffix_folder.__name__) as ue_transaction:
        assets_data = get_asset.get_assets_by_dirs(folder_paths, recursive, include_only_on_disk_assets)

        progress_bar_text = add_prefix_suffix_folder.__name__ + IS_WORKING_TEXT
        with unreal.ScopedSlowTask(len(assets_data), progress_bar_text) as slow_task:
            slow_task.make_dialog(True)

            for asset_data in assets_data:
                if slow_task.should_cancel():
                    break
                object_path = asset_data.get_editor_property('object_path')
                add_prefix_suffix(object_path, prefix, suffix, True, include_only_on_disk_assets)

            slow_task.enter_progress_frame(1)


## @param is_folder_operation    indicates if it is adding prefix_suffix for many files in folder
def delete_prefix_suffix_folder(folder_paths, prefix = '', suffix = '',
                                recursive = False, include_only_on_disk_assets = False):
    with unreal.ScopedEditorTransaction(delete_prefix_suffix_folder.__name__) as ue_transaction:
        assets_data = get_asset.get_assets_by_dirs(folder_paths, recursive, include_only_on_disk_assets)

        progress_bar_text = delete_prefix_suffix_folder.__name__ + IS_WORKING_TEXT
        with unreal.ScopedSlowTask(len(assets_data), progress_bar_text) as slow_task:
            slow_task.make_dialog(True)

            for asset_data in assets_data:
                if slow_task.should_cancel():
                    break
                object_path = asset_data.get_editor_property('object_path')
                delete_prefix_suffix(object_path, prefix, suffix, True, include_only_on_disk_assets)

            slow_task.enter_progress_frame(1)

## @param is_folder_operation    indicates if it is adding prefix_suffix for many files in folder
def replace_prefix_suffix_folder(folder_paths, prefix = '', suffix = '', new_prefix = '', new_suffix = '',
                                 recursive = False, include_only_on_disk_assets = False):
    with unreal.ScopedEditorTransaction(replace_prefix_suffix_folder.__name__) as ue_transaction:
        assets_data = get_asset.get_assets_by_dirs(folder_paths, recursive, include_only_on_disk_assets)

        progress_bar_text = replace_prefix_suffix_folder.__name__ + IS_WORKING_TEXT
        with unreal.ScopedSlowTask(len(assets_data), progress_bar_text) as slow_task:
            slow_task.make_dialog(True)

            for asset_data in assets_data:
                if slow_task.should_cancel():
                    break
                object_path = asset_data.get_editor_property('object_path')
                replace_prefix_suffix(object_path, prefix, suffix, new_prefix, new_suffix, True, include_only_on_disk_assets)

            slow_task.enter_progress_frame(1)


def correct_prefix_suffix(object_path, is_folder_operation = False, asset_data = None,
                          include_only_on_disk_assets = False):
    if asset_data == None:
        asset_data = get_asset.get_asset_data_by_object_path(object_path, include_only_on_disk_assets)

    if asset_data != None:
        asset_class = general.Name_to_str(asset_data.get_editor_property('asset_class'))
        #unreal.log(asset_class)
        prefix_for_class = convention.AssetsPrefixConventionTable[asset_class]
        if prefix_for_class != None and prefix_for_class != '':
            if is_folder_operation:
                # If function was called by correct_prefix_suffix_folder, it has one transaction with all assets in folder
                add_prefix_suffix(object_path, prefix = prefix_for_class, is_folder_operation = False,
                                  include_only_on_disk_assets = include_only_on_disk_assets)
            else:
                with unreal.ScopedEditorTransaction(correct_prefix_suffix.__name__) as ue_transaction:
                    add_prefix_suffix(object_path, prefix = prefix_for_class, is_folder_operation = False,
                                      include_only_on_disk_assets = include_only_on_disk_assets)

        else:
            unreal.log_error(correct_prefix_suffix.__name__ + '(): Did not find prefix for asset class - ' + asset_class)
    else:
        unreal.log_error(correct_prefix_suffix.__name__ + '(): Did not find asset_data from object_path')

## Add correct prefix and suffix. Depends on asset type.
def correct_prefix_suffix_dirs(dir_paths, recursive = False, include_only_on_disk_assets = False):
    with unreal.ScopedEditorTransaction(correct_prefix_suffix_dirs.__name__) as ue_transaction:
        assets_data = get_asset.get_assets_by_dirs(dir_paths, recursive, include_only_on_disk_assets)

        progress_bar_text = correct_prefix_suffix_dirs.__name__ + IS_WORKING_TEXT
        with unreal.ScopedSlowTask(len(assets_data), progress_bar_text) as slow_task:
            slow_task.make_dialog(True)

            for asset_data in assets_data:
                if slow_task.should_cancel():
                    break
                object_path = asset_data.get_editor_property('object_path')
                correct_prefix_suffix(object_path, True, asset_data, include_only_on_disk_assets)

            slow_task.enter_progress_frame(1)


def delete_glb_texture_prefix(object_path):
    new_name = get_asset.get_asset_name_no_extension(object_path)
    # regex: ^\d+_
    match_object = re.search('^\\d+_', new_name)
    if match_object:
        new_name = new_name[len(match_object[0]) :]
        new_path = get_asset.get_asset_path_with_new_name(object_path, new_name)
        unreal.EditorAssetLibrary.rename_asset(object_path, new_path)
        return True
    else:
        unreal.log_error(delete_glb_texture_prefix.__name__ + '(): There is no glb texture prefix in: ' + general.Name_to_str(object_path))
        return False

## delete indexes in names of imported glb textures
def delete_glb_texture_prefix_in_dirs(dir_paths, recursive = False, include_only_on_disk_assets = False):
    unreal.log(delete_glb_texture_prefix_in_dirs.__name__ + ' Started')
    with unreal.ScopedEditorTransaction(delete_glb_texture_prefix_in_dirs.__name__) as ue_transaction:
        assets_data = get_asset.get_assets_by_dirs(dir_paths, recursive, include_only_on_disk_assets)
        if general.is_not_none_or_empty(assets_data):
            progress_bar_text = delete_glb_texture_prefix_in_dirs.__name__ + IS_WORKING_TEXT
            with unreal.ScopedSlowTask(len(assets_data), progress_bar_text) as slow_task:
                slow_task.make_dialog(True)

                for asset_data in assets_data:
                    if slow_task.should_cancel():
                        break
                    object_path = asset_data.get_editor_property('object_path')
                    delete_glb_texture_prefix(object_path)

                slow_task.enter_progress_frame(1)

    unreal.log('_')

def delete_glb_texture_prefix_in_dir(dir_path, recursive = False, include_only_on_disk_assets = False):
    delete_glb_texture_prefix_in_dirs([dir_path], recursive, include_only_on_disk_assets)

## Reads prefix and suffix of texture asset and returns type of texture by convention
# Converts all text to lower case
def get_texture_type_by_prefix_suffix(object_path, include_only_on_disk_assets = False):
    prefix = get_asset_prefix_suffix_by_path(object_path)
    suffix = prefix[1]
    prefix = prefix[0]

    texture_types = convention.TextureTypesCustom
    texture_types_keys = list(convention.TextureTypesCustom.keys())
    is_type_found = False
    type_indx = 0
    key = ''
    while (not is_type_found) and type_indx < len(texture_types_keys):
        key = texture_types_keys[type_indx]
        if texture_types[key][0].casefold() == prefix.casefold():     # check prefix
            is_suffix_found = False
            suffix_indx = 0
            while (not is_suffix_found) and suffix_indx < len(texture_types[key][1]):
                if texture_types[key][1][suffix_indx].casefold() == suffix.casefold():    # check suffix in suffix list
                    is_type_found = True
                    is_suffix_found = True
                else:
                    suffix_indx +=1
        type_indx += 1

    if not is_type_found:
        key = NO_TEXTURE_TYPE
    return key

def get_texture_type_by_prefix_suffix_d(asset_data, include_only_on_disk_assets = False):
    object_path = asset_data.get_editor_property('object_path')
    return get_texture_type_by_prefix_suffix(object_path, include_only_on_disk_assets)