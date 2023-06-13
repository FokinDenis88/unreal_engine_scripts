import unreal_engine_scripts.config as config
import unreal_engine_scripts.src.get_asset as get_asset
import unreal_engine_scripts.src.set_asset as set_asset
import unreal_engine_scripts.service.log as log

import unreal

# To apply changes in modules
import importlib
importlib.reload(config)
importlib.reload(get_asset)
importlib.reload(set_asset)
importlib.reload(log)


NO_MIPMAP_HEADER = 'Textures without mipmaps: '

## Find all textures not in Power of two mode. If texture is not standart, lod can't be generated
def find_no_mipmap_textures_log(target_paths, is_recursive_search, only_on_disk_assets):
    return get_asset.find_assets_data(package_paths = target_paths,
                                        class_names = [config.CLASS_NAME_TEXTURE], recursive_classes = True,
                                        recursive_paths = is_recursive_search,
                                        include_only_on_disk_assets = only_on_disk_assets,
                                        properties_values = [(config.PROPERTY_MIPMAP_GEN, config.SETTING_NO_MIPMAPS)],
                                        log_path = log.LOG_PATH_NO_MIPMAPS, log_title = 'No Mipmap Textures')

## Find all meshes without lod groups
def find_no_lods_meshes_log(target_paths, is_recursive_search, only_on_disk_assets):
    return get_asset.find_assets_data(package_paths = target_paths,
                                      class_names = [config.CLASS_NAME_STATIC_MESH],
                                      recursive_paths = is_recursive_search,
                                      include_only_on_disk_assets = only_on_disk_assets,
                                      properties_values = [(config.PROPERTY_LOD_GROUP, config.SETTING_NO_LOD_GROUP)],
                                      log_path = log.LOG_PATH_NO_LODS, log_title = 'No Lods Static Meshes')

#================================Mipmaps===========================================================

## Sets textures mipmap generation setting to new_value
# @param texture_paths object_paths of texture assets
def set_textures_mipmap_gen_settings_log(texture_paths, new_value = config.SETTING_DEFAULT_MIPMAPS,
                                         is_recursive_search = True, only_on_disk_assets = False,
                                         search_properties_values = [], is_disjunction = True):
    new_properties_values = [(config.PROPERTY_MIPMAP_GEN, new_value)]
    return set_asset.set_assets_properties_in_object_paths(texture_paths, new_properties_values, is_recursive_search,
                                                           only_on_disk_assets, [config.CLASS_NAME_TEXTURE, config.CLASS_NAME_TEXTURE_TWO_D],
                                                           search_properties_values, is_disjunction,
                                                           log_path = log.LOG_PATH_SET_PROPERTIES,
                                                           log_title = 'set_textures_mipmap_gen_settings_log')

## Sets textures mipmap generation setting to new_value
# @param dirs_paths paths to dirs with texture assets
def set_textures_mipmap_gen_settings_dirs(dirs_paths, new_value = config.SETTING_DEFAULT_MIPMAPS,
                                         is_recursive_search = True, only_on_disk_assets = False,
                                         search_properties_values = [], is_disjunction = True):
    assets_data = get_asset.get_textures_data_by_dirs(dirs_paths, is_recursive_search, only_on_disk_assets)
    object_paths = get_asset.get_assets_data_object_paths(assets_data)
    return set_textures_mipmap_gen_settings_log(object_paths, new_value,
                                                is_recursive_search, only_on_disk_assets,
                                                search_properties_values, is_disjunction)

## Sets textures with no mipmap gen settings to generate mipmaps new_value. Writing logs.
# @param dirs_paths paths to dirs with texture assets
def set_textures_with_no_mipmap_gen_settings_dirs(dirs_paths, new_value = config.SETTING_DEFAULT_MIPMAPS,
                                                 is_recursive_search = True, only_on_disk_assets = False,
                                                 search_properties_values = [], is_disjunction = True):
    assets_data = find_no_mipmap_textures_log(dirs_paths, is_recursive_search, only_on_disk_assets)
    object_paths = get_asset.get_assets_data_object_paths(assets_data)
    return set_textures_mipmap_gen_settings_log(object_paths, new_value,
                                                 is_recursive_search, only_on_disk_assets,
                                                 search_properties_values, is_disjunction)

#================================Lod===========================================================

## Sets textures with no mipmap gen settings to generate mipmaps new_value. Writing logs.
# @param dirs_paths paths to dirs with texture assets
def set_meshes_lod_group_log(mesh_paths, new_value = config.SETTING_DEFAULT_LOD_GROUP,
                            is_recursive_search = True, only_on_disk_assets = False,
                            search_properties_values = [], is_disjunction = True):
    new_properties_values = [(config.PROPERTY_LOD_GROUP, new_value)]
    return set_asset.set_assets_properties_in_object_paths(mesh_paths, new_properties_values, is_recursive_search,
                                                           only_on_disk_assets, [config.CLASS_NAME_STATIC_MESH],
                                                           search_properties_values, is_disjunction,
                                                           log_path = log.LOG_PATH_SET_PROPERTIES,
                                                           log_title = 'set_meshes_lod_group_log')

def set_meshes_lod_group_dirs(dirs_paths, new_value = config.SETTING_DEFAULT_LOD_GROUP,
                            is_recursive_search = True, only_on_disk_assets = False,
                            search_properties_values = [], is_disjunction = True):
    assets_data = get_asset.get_static_mesh_data_by_dirs(dirs_paths, is_recursive_search, only_on_disk_assets)
    object_paths = get_asset.get_assets_data_object_paths(assets_data)
    return set_meshes_lod_group_log(object_paths, new_value,
                                     is_recursive_search, only_on_disk_assets,
                                     search_properties_values, is_disjunction)

## Sets lod group to meshes with no lod group in dirs. Writing logs.
def set_meshes_with_no_lods_group_dirs(dirs_paths, new_value = config.SETTING_DEFAULT_LOD_GROUP,
                                        is_recursive_search = True, only_on_disk_assets = False,
                                        search_properties_values = [], is_disjunction = True):
    assets_data = find_no_lods_meshes_log(dirs_paths, is_recursive_search, only_on_disk_assets)
    object_paths = get_asset.get_assets_data_object_paths(assets_data)
    return set_meshes_lod_group_log(object_paths, new_value,
                                     is_recursive_search, only_on_disk_assets,
                                     search_properties_values, is_disjunction)

def set_mipmaps_n_lod_group_to_no_lods_dirs(dirs_paths,
                                            new_value_mipmaps = config.SETTING_DEFAULT_MIPMAPS,
                                            new_value_lod_group = config.SETTING_DEFAULT_LOD_GROUP,
                                            is_recursive_search = True, only_on_disk_assets = False,
                                            search_properties_values = [], is_disjunction = True):
    assets_data_no_mipmaps = set_textures_with_no_mipmap_gen_settings_dirs(dirs_paths, new_value_mipmaps,
                                                                        is_recursive_search, only_on_disk_assets,
                                                                        search_properties_values, is_disjunction)
    unreal.log('')
    assets_data_no_lods = set_meshes_with_no_lods_group_dirs(dirs_paths, new_value_lod_group,
                                                            is_recursive_search, only_on_disk_assets,
                                                            search_properties_values, is_disjunction)
    unreal.log('')
    return assets_data_no_mipmaps, assets_data_no_lods

# Set lod count