import unreal

import unreal_engine_scripts.config as config
import unreal_engine_scripts.service.general_ue as general_ue
import unreal_engine_scripts.src.get_asset as get_asset
import unreal_engine_scripts.service.log as log

import importlib
importlib.reload(config)
importlib.reload(general_ue)
importlib.reload(get_asset)
importlib.reload(log)


def set_assets_properties_in_assets_data(assets_data, new_properties_values = [],
                                         log_path = '', log_title = ''):
    unreal.log(set_assets_properties_in_assets_data.__name__ + '() Started')
    if general_ue.is_not_none_or_empty_lists([assets_data, new_properties_values]):
        process_text = 'Set assets properties in assets_data'
        with unreal.ScopedEditorTransaction(process_text) as ue_transaction:
            with unreal.ScopedSlowTask(len(assets_data), process_text) as slow_task:
                slow_task.make_dialog(True)
                for asset_data in assets_data :
                    if slow_task.should_cancel():
                        break
                    asset = asset_data.get_asset()
                    for new_property_value in new_properties_values:
                        if new_property_value[0] and new_property_value[1] is not None:
                            asset.set_editor_property(new_property_value[0], new_property_value[1])
                    slow_task.enter_progress_frame(1)
    else:
        unreal.log_error(set_assets_properties_in_assets_data.__name__ +
                         '(): assets_data, new_properties_values list must not be None or Empty')

    if log_path is not None and log_path != '':
        log.write_assets_data_log(assets_data, log_path, log_title)
    unreal.log(set_assets_properties_in_assets_data.__name__ + '() Finished')
    return assets_data

## First Finds assets by parameters, then sets new_properties_values
# If there is no parameters, will find ALL assets. Needs more checks for parameters before call.
def set_assets_properties(new_properties_values, package_paths = [], package_names = [], object_paths = [],
                            class_names = [], recursive_classes_exclusion_set = [],
                            recursive_paths = True, recursive_classes = False, include_only_on_disk_assets = False,
                            properties_values = [], is_disjunction = True,
                            log_path = '', log_title = ''):
    assets_data = []
    if general_ue.is_not_none_or_empty(new_properties_values):
        assets_data = get_asset.find_assets_data(package_paths, package_names, object_paths,
                                class_names, recursive_classes_exclusion_set,
                                recursive_paths, recursive_classes, include_only_on_disk_assets,
                                properties_values, is_disjunction)
        assets_data = set_assets_properties_in_assets_data(assets_data, new_properties_values)
        if log_path is not None and log_path != '':
            log.write_assets_data_log(assets_data, log_path, log_title)
    else:
        unreal.log_error(set_assets_properties.__name__ + '(): new_properties_values must not be None or Empty')
    return assets_data

## Set asset properties by values.
def set_assets_properties_in_dir(dir_paths, new_properties_values = [], is_recursive_search = True,
                                 only_on_disk_assets = False, class_names = [],
                                 search_properties_values = [], is_disjunction = True,
                                 log_path = '', log_title = ''):
    assets_data = []
    if general_ue.is_not_none_or_empty_lists(dir_paths):
        assets_data = get_asset.find_assets_data(package_paths = dir_paths, class_names = class_names,
                                                recursive_paths = is_recursive_search,
                                                include_only_on_disk_assets = only_on_disk_assets,
                                                properties_values = search_properties_values, is_disjunction = is_disjunction)
        assets_data = set_assets_properties_in_assets_data(assets_data, new_properties_values)
        if log_path is not None and log_path != '':
            log.write_assets_data_log(assets_data, log_path, log_title)
    else:
        unreal.log_error(set_assets_properties_in_dir.__name__ + '(): dir_paths must not be None or Empty')
    return assets_data

def set_assets_properties_in_object_paths(object_paths, new_properties_values = [], is_recursive_search = True,
                                          only_on_disk_assets = False, class_names = [],
                                          search_properties_values = [], is_disjunction = True,
                                          log_path = '', log_title = ''):
    assets_data = []
    if general_ue.is_not_none_or_empty_lists(object_paths):
        assets_data = get_asset.find_assets_data(object_paths = object_paths, class_names = class_names,
                                                recursive_paths = is_recursive_search,
                                                include_only_on_disk_assets = only_on_disk_assets,
                                                properties_values = search_properties_values, is_disjunction = is_disjunction)
        assets_data = set_assets_properties_in_assets_data(assets_data, new_properties_values)
        if log_path is not None and log_path != '':
            log.write_assets_data_log(assets_data, log_path, log_title)
    else:
        unreal.log_error(set_assets_properties_in_object_paths.__name__ + '(): dir_paths must not be None or Empty')
    return assets_data


#====================================Logs=======================================================

## Consolidate assets with the same name, stored in different dirs
# @param dir_path_assets_to_consolidate_to  - target
# @param dir_path_assets_to_consolidate     - source
def consolidate_assets_by_dir(dir_path_assets_to_consolidate_to, dir_path_assets_to_consolidate):
    assets_data = get_asset.get_assets_by_dir(dir_path_assets_to_consolidate)
    for asset_data in assets_data:
        asset_name = general_ue.Name_to_str(asset_data.get_editor_property('asset_name'))
        path_asset_to_consolidate_to = unreal.Paths.combine([dir_path_assets_to_consolidate_to, asset_name])
        path_asset_to_consolidate = unreal.Paths.combine([dir_path_assets_to_consolidate, asset_name])
        object_asset_to_consolidate_to = unreal.EditorAssetLibrary.load_asset(path_asset_to_consolidate_to)
        objects_assets_to_consolidate = [unreal.EditorAssetLibrary.load_asset(path_asset_to_consolidate)]
        unreal.EditorAssetLibrary.consolidate_assets(object_asset_to_consolidate_to, objects_assets_to_consolidate)

## Deletes all Everything in directory
def delete_all_in_dir(dir_path):
    if general_ue.is_not_none_or_empty(dir_path):
        unreal.EditorAssetLibrary.delete_directory(dir_path)
        unreal.EditorAssetLibrary.make_directory(dir_path)
    else:
        unreal.log_error(delete_all_in_dir.__name__ + '(): dir_path must not be None or Empty')