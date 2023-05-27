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

## Moves assets by there asset_data to destination folder
# Will compile unsaved material
def move_assets(assets_data, destination_dir, is_save_dir_structure = False, source_dir = ''):
    if general.is_not_none_or_empty(assets_data):
        if (destination_dir is not None) and (destination_dir != ''):
            if not unreal.EditorAssetLibrary.does_directory_exist(destination_dir):
                unreal.EditorAssetLibrary.make_directory(destination_dir)
            for asset_data in assets_data:
                asset_path = general.Name_to_str(asset_data.get_editor_property('object_path'))
                asset_dir = unreal.Paths.get_path(asset_path)
                asset_destination_path = ''
                asset_name = general.Name_to_str(asset_data.get_editor_property('asset_name'))
                if is_save_dir_structure and source_dir != '' and len(asset_dir) > len(source_dir):
                    sub_dirs = asset_dir[len(source_dir):]
                    asset_destination_path = unreal.Paths.combine([destination_dir, sub_dirs, asset_name])
                else:
                    asset_destination_path = unreal.Paths.combine([destination_dir, asset_name])

                unreal.EditorAssetLibrary.rename_asset(asset_path, asset_destination_path)
                #unreal.log('asset_destination_path: ' + asset_destination_path)

        else:
            unreal.log_error(move_assets.__name__ + ': destination_dir is empty or does not exists')
    else:
        unreal.log_error(move_assets.__name__ + ': assets_data is empty')

def move_assets_in_dir(source_dir, destination_dir, is_recursive = False,
                      include_only_on_disk_assets = False, is_save_dir_structure = False):
    assets_data = get_asset.get_assets_by_dir(source_dir, is_recursive, include_only_on_disk_assets)
    move_assets(assets_data, destination_dir, is_save_dir_structure, source_dir)

def move_assets_in_dirs(source_dirs, destination_dirs, is_recursive = False,
                        include_only_on_disk_assets = False, is_save_dir_structure = False):
    if general.is_not_none_or_empty_lists([source_dirs, destination_dirs]):
        i = 0; len_lists = len(source_dirs)
        while i < len_lists:
            move_assets_in_dir(source_dirs[i], destination_dirs[i], is_recursive, include_only_on_disk_assets, is_save_dir_structure)
            i += 1
    else:
        unreal.log_error(move_assets_in_dirs.__name__ + ': source_dirs, destination_dirs must not be None or Empty')

## Deletes assets by assets_data
def delete_assets(assets_data):
    if general.is_not_none_or_empty(assets_data):
        for asset_data in assets_data:
            unreal.EditorAssetLibrary.delete_asset(asset_data.get_editor_property('object_path'))

    else:
        unreal.log_error(move_assets.__name__ + ': assets_data is empty')