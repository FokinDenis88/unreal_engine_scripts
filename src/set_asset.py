import unreal

import unreal_scripts.config as config
import unreal_scripts.service.general as general
import unreal_scripts.src.get_asset as get_asset
import unreal_scripts.service.log as log

import importlib
importlib.reload(config)
importlib.reload(general)
importlib.reload(get_asset)
importlib.reload(log)

## Set asset properties by values.
def set_assets_properties_in_folder(target_paths, is_recursive_search = True, only_on_disk_assets = False, class_names = [],
                                    search_properties_values = [], new_properties_values = [], is_disjunction = True):
    unreal.log('set_assets_properties_in_folder() Started')

    if general.is_not_none_or_empty(new_properties_values):
        assets_data = get_asset.find_assets_data(package_paths = target_paths, class_names = class_names,
                                                 recursive_paths = is_recursive_search,
                                                 include_only_on_disk_assets = only_on_disk_assets,
                                                 properties_values = search_properties_values, is_disjunction = is_disjunction)
        if general.is_not_none_or_empty(assets_data):
            process_text = 'Set assets properties in folder'
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
        unreal.log_error('set_assets_properties_in_folder: new_properties_values list ' + config.IS_EMPTY_OR_NONE_TEXT)

    unreal.log('set_assets_properties_in_folder() Finished')
    return assets_data

## Set asset properties by values. Write log of operation to file and console
def set_assets_properties_in_folder_log(log_path, log_title, target_paths, is_recursive_search = True,
                                        only_on_disk_assets = False, class_names = [],
                                        search_properties_values = [], new_properties_values = [], is_disjunction = True):
    log.log_print_n_write_file(log_path, log_title + ': ', 'w')
    assets_data = set_assets_properties_in_folder(target_paths, is_recursive_search,only_on_disk_assets, class_names,
                                                  search_properties_values, new_properties_values, is_disjunction)

    if general.is_not_none_or_empty(assets_data):
        unreal.log(log.FINAL_RESULTS)
        for asset_data in assets_data :
            object_path = asset_data.get_editor_property('object_path')
            log.log_print_n_write_file(log_path, object_path)
    else:
        unreal.log_error('set_assets_properties_in_folder_log: assets_data ' + config.IS_EMPTY_OR_NONE_TEXT)


## Consolidate assets with the same name, stored in different dirs
# @param dir_path_assets_to_consolidate_to  - target
# @param dir_path_assets_to_consolidate     - source
def consolidate_assets_by_dir(dir_path_assets_to_consolidate_to, dir_path_assets_to_consolidate):
    assets_data = get_asset.get_assets_by_dir(dir_path_assets_to_consolidate)
    for asset_data in assets_data:
        asset_name = general.Name_to_str(asset_data.get_editor_property('asset_name'))
        path_asset_to_consolidate_to = unreal.Paths.combine([dir_path_assets_to_consolidate_to, asset_name])
        path_asset_to_consolidate = unreal.Paths.combine([dir_path_assets_to_consolidate, asset_name])
        object_asset_to_consolidate_to = unreal.EditorAssetLibrary.load_asset(path_asset_to_consolidate_to)
        objects_assets_to_consolidate = [unreal.EditorAssetLibrary.load_asset(path_asset_to_consolidate)]
        unreal.EditorAssetLibrary.consolidate_assets(object_asset_to_consolidate_to, objects_assets_to_consolidate)

## Deletes all Everything in directory
def delete_all_in_dir(dir_path):
    if general.is_not_none_or_empty(dir_path):
        unreal.EditorAssetLibrary.delete_directory(dir_path)
        unreal.EditorAssetLibrary.make_directory(dir_path)
    else:
        unreal.log_error(delete_all_in_dir.__name__ + '(): dir_path must not be None or Empty')