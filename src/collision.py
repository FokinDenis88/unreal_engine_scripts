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

## There are two types of collision. Simple and Complex. Complex is often one of lods.
# Check if asset has simple collision
def has_simple_collision(asset_data):
    asset = asset_data.get_asset()
    body_setup = asset.get_editor_property('body_setup')
    geometry = body_setup.get_editor_property('agg_geom')

    if general.is_not_none_or_empty(geometry.get_editor_property('box_elems')):
        return True
    if general.is_not_none_or_empty(geometry.get_editor_property('convex_elems')):
        return True
    if general.is_not_none_or_empty(geometry.get_editor_property('sphere_elems')):
        return True
    if general.is_not_none_or_empty(geometry.get_editor_property('sphyl_elems')):
        return True
    if general.is_not_none_or_empty(geometry.get_editor_property('tapered_capsule_elems')):
        return True

    return False

## Find No Collider assets
def find_no_collision_assets(folder_paths, log_path = log.LOG_PATH_NO_COLLISION, recursive_paths = True,
                             include_only_on_disk_assets = False):
    log.log_print_n_write_file(log_path, find_no_collision_assets.__name__ + '(): ', 'w')

    assets_data = get_asset.find_assets_data(package_paths = folder_paths,
                                             class_names = [config.ClassName.STATIC_MESH], recursive_paths = recursive_paths,
                                             include_only_on_disk_assets = include_only_on_disk_assets)
    if general.is_not_none_or_empty(assets_data):
        unreal.log(log.FINAL_RESULTS)
        for asset_data in assets_data:
            if not has_simple_collision(asset_data):
                log.log_print_n_write_file(log_path, asset_data.get_editor_property('object_path'))
    else:
        unreal.log(find_no_collision_assets.__name__ + '(): Did not find any static mesh.')


def get_simple_collision_count(static_mesh):
    if static_mesh is not None:
        return unreal.EditorStaticMeshLibrary.get_simple_collision_count(static_mesh)
    else:
        unreal.log_error(get_simple_collision_count.__name__ + '(): static_mesh must not be None')
        return -1

def get_simple_collision_count_by_data(asset_data):
    if asset_data is not None:
        static_mesh = asset_data.get_asset()
        return unreal.EditorStaticMeshLibrary.get_simple_collision_count(static_mesh)
    else:
        unreal.log_error(get_simple_collision_count_by_data.__name__ + '(): asset_data must not be None')
        return -1

## Second Variant of finding no simple collisions assets
def find_no_collision_assets_v2(folder_paths, log_path = log.LOG_PATH_NO_COLLISION, recursive_paths = True,
                                include_only_on_disk_assets = False):
    log.log_print_n_write_file(log_path, find_no_collision_assets.__name__ + '(): ', 'w')

    assets_data = get_asset.find_assets_data(package_paths = folder_paths,
                                             class_names = [config.ClassName.STATIC_MESH], recursive_paths = recursive_paths,
                                             include_only_on_disk_assets = include_only_on_disk_assets)
    if general.is_not_none_or_empty(assets_data):
        unreal.log(log.FINAL_RESULTS)
        for asset_data in assets_data:
            if get_simple_collision_count_by_data(asset_data) == 0:
                log.log_print_n_write_file(log_path, asset_data.get_editor_property('object_path'))
    else:
        unreal.log(find_no_collision_assets.__name__ + '(): Did not find any static mesh.')
