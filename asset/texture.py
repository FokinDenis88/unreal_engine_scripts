from enum import Enum

import unreal

import unreal_engine_scripts.service.general_ue as general_ue
import unreal_engine_scripts.src.get_asset as get_asset

import importlib
importlib.reload(general_ue)
importlib.reload(get_asset)

from unreal_engine_scripts.src.get_asset import get_asset_by_object_path

## X = Width. Y = Height
class ImportSizeMode(Enum):
    X = 0
    Y = 1
    XY = 3

## Get texture imported size
# if is_axis_x = True return import texture size of x axis
def get_texture_imported_size(texture, include_only_on_disk_assets = False, mode = ImportSizeMode.X):
    imported_size_x, imported_size_y = 0.0, 0.0
    with unreal.ScopedEditorTransaction('get_texture_imported_size()') as ue_transaction:
        origin_max_texture_size = texture.get_editor_property('max_texture_size')
        origin_downscale = texture.get_editor_property('downscale')
        origin_downscale_default = origin_downscale.get_editor_property('default')
        origin_downscale_per_platform = origin_downscale.get_editor_property('per_platform').copy()
        origin_power_of_two = texture.get_editor_property('power_of_two_mode')

        texture.set_editor_property('max_texture_size', 0.0)
        texture.set_editor_property('downscale', unreal.PerPlatformFloat())
        texture.set_editor_property('power_of_two_mode', unreal.TexturePowerOfTwoSetting.NONE)

        if mode == ImportSizeMode.X:
            imported_size_x = texture.blueprint_get_size_x()
        elif mode == ImportSizeMode.Y:
            imported_size_y = texture.blueprint_get_size_y()
        elif mode == ImportSizeMode.XY:
            imported_size_x = texture.blueprint_get_size_x()
            imported_size_y = texture.blueprint_get_size_y()

        texture.set_editor_property('power_of_two_mode', origin_power_of_two)
        texture.set_editor_property('downscale', origin_downscale)
        origin_downscale.set_editor_property('default', origin_downscale_default)
        origin_downscale.set_editor_property('per_platform', origin_downscale_per_platform)
        texture.set_editor_property('max_texture_size', origin_max_texture_size)

    if mode == ImportSizeMode.X:
        return imported_size_x
    elif mode == ImportSizeMode.Y:
        return imported_size_y
    elif mode == ImportSizeMode.XY:
        return imported_size_x, imported_size_y

    return

def get_texture_imported_size_by_path(object_path, include_only_on_disk_assets = False, mode = ImportSizeMode.X):
    texture = get_asset_by_object_path(object_path, include_only_on_disk_assets)
    get_texture_imported_size(texture, include_only_on_disk_assets, mode)

def get_texture_imported_size_x(object_path, include_only_on_disk_assets = False):
    return get_texture_imported_size(object_path, include_only_on_disk_assets, ImportSizeMode.X)

def get_texture_imported_size_y(object_path, include_only_on_disk_assets = False):
    return get_texture_imported_size(object_path, include_only_on_disk_assets, ImportSizeMode.Y)

def get_texture_imported_size_x_y(object_path, include_only_on_disk_assets = False):
    return get_texture_imported_size(object_path, include_only_on_disk_assets, ImportSizeMode.XY)

## Find textures in directory by imported size
# Useful for optimization. To find, what texture needs to be reimport with lesser size
def find_textures_by_imported_size(dir_path, search_texture_size, is_bigger_or_equal = True,
                                   is_recursive_search = False, only_on_disk_assets = False):
    found_textures = []
    if general_ue.is_not_none_or_empty(dir_path):
        textures_data = get_asset.get_textures_data_by_dir(dir_path, is_recursive_search, only_on_disk_assets)
        if textures_data is not None:
            for texture_data in textures_data:
                texture_imported_size = get_texture_imported_size(texture_data.get_asset(), only_on_disk_assets)
                if is_bigger_or_equal and texture_imported_size >= search_texture_size:
                    found_textures.append(texture_data.get_asset())
                elif (not is_bigger_or_equal) and texture_imported_size <= search_texture_size:
                    found_textures.append(texture_data.get_asset())

        else:
            unreal.log(find_textures_by_imported_size.__name__ + ': there is no textures in dir')
    else:
        unreal.log_error(find_textures_by_imported_size.__name__ + ': dir_path must not be Empty or None')

    return found_textures


def set_maximum_texture_size(texture, value):
    texture.set_editor_property('max_texture_size', value)

def set_maximum_textures_size_in_dir(dir_path, value):
    if general_ue.is_not_none_or_empty(dir_path):
        textures_data = get_asset.get_textures_data_by_dir(dir_path)
        if textures_data is not None:
            for texture_data in textures_data:
                set_maximum_texture_size(texture_data.get_asset(), value)
        else:
            unreal.log(set_maximum_textures_size_in_dir.__name__ + ': there is no textures in dir')
    else:
        unreal.log_error(set_maximum_textures_size_in_dir.__name__ + ': dir_path must not be Empty or None')