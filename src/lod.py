import unreal_scripts.config as config
import unreal_scripts.src.get_asset as get_asset
import unreal_scripts.src.set_asset as set_asset
import unreal_scripts.service.log as log

# To apply changes in modules
import importlib
importlib.reload(config)
importlib.reload(get_asset)
importlib.reload(set_asset)
importlib.reload(log)


NO_MIPMAP_HEADER = 'Textures without mipmaps: '

## Find all textures not in Power of two mode. If texture is not standart, lod can't be generated
def find_no_mipmap_textures_log(target_paths, is_recursive_search, only_on_disk_assets):
    return get_asset.find_assets_data_log(log.LOG_PATH_NO_MIPMAPS, 'No Mipmap Textures', package_paths = target_paths,
                                           class_names = [config.CLASS_NAME_TEXTURE],
                                           recursive_paths = is_recursive_search,
                                           include_only_on_disk_assets = only_on_disk_assets,
                                           properties_values = [(config.PROPERTY_MIPMAP_GEN, config.SETTING_NO_MIPMAPS)])

## Find all meshes without lod groups
def find_no_lods_meshes_log(target_paths, is_recursive_search, only_on_disk_assets):
    return get_asset.find_assets_data_log(log.LOG_PATH_NO_LODS, 'No Lods Static Meshes', package_paths = target_paths,
                                           class_names = [config.CLASS_NAME_STATIC_MESH],
                                           recursive_paths = is_recursive_search,
                                           include_only_on_disk_assets = only_on_disk_assets,
                                           properties_values = [(config.PROPERTY_LOD_GROUP, config.SETTING_NO_LOD_GROUP)])


def set_textures_mipmap_gen_settings_log(texture_paths, new_value = config.SETTING_DEFAULT_MIPMAPS,
                                         is_recursive_search = True, only_on_disk_assets = False,
                                         search_properties_values = [], is_disjunction = True):
    new_properties_values = [(config.PROPERTY_MIPMAP_GEN, new_value)]
    set_asset.set_assets_properties_in_folder_log(log.LOG_PATH_SET_PROPERTIES, 'set_textures_gen_mipmaps_log',
                                                  texture_paths, is_recursive_search,
                                                  only_on_disk_assets, [config.CLASS_NAME_TEXTURE],
                                                  search_properties_values, new_properties_values, is_disjunction)

def set_textures_mipmap_gen_settings_dirs(dirs_paths, new_value = config.SETTING_DEFAULT_MIPMAPS,
                                         is_recursive_search = True, only_on_disk_assets = False,
                                         search_properties_values = [], is_disjunction = True):
    assets_data = get_asset.get_textures_data_by_dirs(dirs_paths, is_recursive_search, only_on_disk_assets)
    object_paths = get_asset.get_assets_data_object_paths(assets_data)
    set_textures_mipmap_gen_settings_log(object_paths, new_value,
                                         is_recursive_search, only_on_disk_assets,
                                         search_properties_values, is_disjunction)

def set_meshes_lod_group_log(mesh_paths, new_value = config.SETTING_DEFAULT_LOD_GROUP,
                            is_recursive_search = True, only_on_disk_assets = False,
                            search_properties_values = [], is_disjunction = True):
    new_properties_values = [(config.PROPERTY_LOD_GROUP, new_value)]
    set_asset.set_assets_properties_in_folder_log(log.LOG_PATH_SET_PROPERTIES, 'set_meshes_gen_lods_log',
                                                  mesh_paths, is_recursive_search,
                                                  only_on_disk_assets, [config.CLASS_NAME_STATIC_MESH],
                                                  search_properties_values, new_properties_values, is_disjunction)

def set_meshes_lod_group_dirs(dirs_paths, new_value = config.SETTING_DEFAULT_LOD_GROUP,
                            is_recursive_search = True, only_on_disk_assets = False,
                            search_properties_values = [], is_disjunction = True):
    assets_data = get_asset.get_static_mesh_data_by_dirs(dirs_paths, is_recursive_search, only_on_disk_assets)
    object_paths = get_asset.get_assets_data_object_paths(assets_data)
    set_meshes_lod_group_log(object_paths, new_value,
                             is_recursive_search, only_on_disk_assets,
                             search_properties_values, is_disjunction)


def activate_textures_gen_mipmaps_log(target_paths, is_recursive_search = True, only_on_disk_assets = False,
                                      search_properties_values = [], is_disjunction = True):
    set_textures_mipmap_gen_settings_log(target_paths, config.SETTING_DEFAULT_MIPMAPS, is_recursive_search, only_on_disk_assets,
                                 search_properties_values, is_disjunction)
def activate_textures_gen_mipmaps_on_dirs(dirs_paths, is_recursive_search = True, only_on_disk_assets = False,
                                      search_properties_values = [], is_disjunction = True):
    set_textures_mipmap_gen_settings_dirs(dirs_paths, config.SETTING_DEFAULT_MIPMAPS, is_recursive_search, only_on_disk_assets,
                                          search_properties_values, is_disjunction)

def activate_meshes_gen_lods_log(target_paths, is_recursive_search = True, only_on_disk_assets = False,
                                 search_properties_values = [], is_disjunction = True):
    set_meshes_lod_group_log(target_paths, config.SETTING_DEFAULT_LOD_GROUP, is_recursive_search, only_on_disk_assets,
                            search_properties_values, is_disjunction)
def activate_meshes_gen_lods_on_dirs(dirs_paths, is_recursive_search = True, only_on_disk_assets = False,
                                    search_properties_values = [], is_disjunction = True):
    set_meshes_lod_group_dirs(dirs_paths, config.SETTING_DEFAULT_LOD_GROUP, is_recursive_search, only_on_disk_assets,
                              search_properties_values, is_disjunction)