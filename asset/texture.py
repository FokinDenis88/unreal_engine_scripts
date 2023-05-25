from enum import Enum

import unreal

from unreal_scripts.src.get_asset import get_asset_by_object_path


class ImportSizeMode(Enum):
    X = 0
    Y = 1
    XY = 3

# if is_axis_x = True return import texture size of x axis
def get_texture_imported_size(object_path, include_only_on_disk_assets=False, mode = ImportSizeMode.X):
    imported_size_x, imported_size_y = 0.0, 0.0
    with unreal.ScopedEditorTransaction('get_texture_imported_size()') as ue_transaction:
        asset = get_asset_by_object_path(object_path, include_only_on_disk_assets).get_asset()
        origin_max_texture_size = asset.get_editor_property('max_texture_size')
        origin_downscale = asset.get_editor_property('downscale')
        origin_downscale_default = origin_downscale.get_editor_property('default')
        origin_downscale_per_platform = origin_downscale.get_editor_property('per_platform').copy()
        origin_power_of_two = asset.get_editor_property('power_of_two_mode')

        asset.set_editor_property('max_texture_size', 0.0)
        asset.set_editor_property('downscale', unreal.PerPlatformFloat())
        asset.set_editor_property('power_of_two_mode', unreal.TexturePowerOfTwoSetting.NONE)

        if mode == ImportSizeMode.X:
            imported_size_x = asset.blueprint_get_size_x()
        elif mode == ImportSizeMode.Y:
            imported_size_y = asset.blueprint_get_size_y()
        elif mode == ImportSizeMode.XY:
            imported_size_x = asset.blueprint_get_size_x()
            imported_size_y = asset.blueprint_get_size_y()

        asset.set_editor_property('power_of_two_mode', origin_power_of_two)
        asset.set_editor_property('downscale', origin_downscale)
        origin_downscale.set_editor_property('default', origin_downscale_default)
        origin_downscale.set_editor_property('per_platform', origin_downscale_per_platform)
        asset.set_editor_property('max_texture_size', origin_max_texture_size)

    if mode == ImportSizeMode.X:
        return imported_size_x
    elif mode == ImportSizeMode.Y:
        return imported_size_y
    elif mode == ImportSizeMode.XY:
        return imported_size_x, imported_size_y

    return


def get_texture_imported_size_x(object_path, include_only_on_disk_assets=False):
    return get_texture_imported_size(object_path, include_only_on_disk_assets, ImportSizeMode.X)

def get_texture_imported_size_y(object_path, include_only_on_disk_assets=False):
    return get_texture_imported_size(object_path, include_only_on_disk_assets, ImportSizeMode.Y)

def get_texture_imported_size_x_y(object_path, include_only_on_disk_assets=False):
    return get_texture_imported_size(object_path, include_only_on_disk_assets, ImportSizeMode.XY)