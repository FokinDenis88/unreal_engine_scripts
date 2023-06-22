import os

import unreal

import unreal_engine_scripts.config as config
import unreal_engine_scripts.service.general_ue as general_ue
import unreal_engine_scripts.service.log as log

import importlib
importlib.reload(config)
importlib.reload(general_ue)
importlib.reload(log)

def load_asset(object_path):
    if general_ue.is_not_none_or_empty(object_path):
        if unreal.EditorAssetLibrary.does_asset_exist(object_path):
            return unreal.EditorAssetLibrary.load_asset(object_path)
        else:
            unreal.log_error(load_asset.__name__ + ': there is no asset by object_path: ' + object_path)
            return
    else:
        unreal.log_error(load_asset.__name__ + ': object_path must not be None or empty')
        return

def get_asset_data_str_property(asset_data, property_name):
    if asset_data is not None and property_name is not '':
        return general_ue.Name_to_str(asset_data.get_editor_property(property_name))
    else:
        unreal.log_error(get_asset_data_str_property.__name__ + '(): asset_data and property_name must not be None or Empty')
        return None

## @return full path to object
def get_path_from_object(object):
    if object is not None:
        if issubclass(type(object), unreal.Object):
            #return unreal.SystemLibrary.get_path_name(object)
            return object.get_path_name()
        else:
            unreal.log_error(get_path_from_object.__name__ + ': object is not subclass of unreal.Object')
            return ''
    else:
        unreal.log_error(get_path_from_object.__name__ + ': object is empty')
        return ''

def get_paths_from_objects(objects_list):
    if general_ue.is_not_none_or_empty(objects_list):
        paths = []
        for object in objects_list:
            paths.append(get_path_from_object(object))
        return paths
    else:
        unreal.log_error(get_paths_from_objects.__name__ + ': objects_list must not be Empty or None')
        return []

def get_paths_from_assets_data(assets_data):
    if general_ue.is_not_none_or_empty(assets_data):
        paths = []
        for asset_data in assets_data:
            paths.append(get_path_from_object(asset_data.get_asset()))
        return paths
    else:
        unreal.log_error(get_paths_from_objects.__name__ + ': assets_data must not be Empty or None')
        return []

def get_path_from_asset_data(asset_data):
    get_paths_from_assets_data([asset_data])

def get_object_path_from_asset_data(asset_data):
    return general_ue.Name_to_str(asset_data.get_editor_property('object_path'))

def get_objects_paths_from_assets_data(assets_data):
    if general_ue.is_not_none_or_empty(assets_data):
        paths = []
        for asset_data in assets_data:
            paths.append(get_object_path_from_asset_data(asset_data))
        return paths
    else:
        unreal.log_error(get_objects_paths_from_assets_data.__name__ + ': assets_data must not be Empty or None')
        return []


# @param object_path    type = Name
# @return_type str
def get_asset_name_no_extension(object_path):
    if object_path is not None:
        return unreal.Paths.get_base_filename(object_path)
    else:
        unreal.log_error(get_asset_name_no_extension.__name__ + ': object_path must not be None')
        return ''

# @param object_path    type = Name
# @return_type str
def get_asset_name_no_extension_in_data_asset(data_asset):
    if data_asset is not None:
        return get_asset_name_no_extension(get_object_path_from_asset_data(data_asset))
    else:
        unreal.log_error(get_asset_name_no_extension_in_data_asset.__name__ + ': data_asset must not be None')
        return ''

# @param object_path    type = Name
# @return_type str
# Deprecated
def get_asset_name_no_extension_n(object_path):
    if object_path != None and object_path != unreal.Name(''):
        path_str = general_ue.Name_to_str(object_path)
        base_name = os.path.basename(path_str)
        asset_name_no_extension = os.path.splitext(base_name)[0]
        return asset_name_no_extension
    else:
        unreal.log_error(get_asset_name_no_extension_n.__name__ + ': object_path is empty')
        return ''

## @return object path to asset, from asset_data.
def get_asset_data_object_path(asset_data):
    if asset_data is not None:
        return general_ue.Name_to_str(asset_data.get_editor_property('object_path'))
    else:
        return ''

def get_assets_data_object_paths(assets_data):
    paths = []
    if general_ue.is_not_none_or_empty(assets_data):
        for asset_data in assets_data:
            paths.append(get_asset_data_object_path(asset_data))
    else:
        unreal.log_error(get_assets_data_object_paths.__name__ + ': assets_data must not be Empty or None')
    return paths

## @param object_path    type = Name
# @param new_name       type = str
# @return_type Name
def get_asset_path_with_new_name(object_path, new_name):
    if object_path != None and object_path != unreal.Name('') and new_name != '':
        path_str = general_ue.Name_to_str(object_path)
        dir_name = os.path.dirname(path_str)
        new_name_extension = new_name + '.' + new_name
        new_path_str = os.path.join(dir_name, new_name_extension)
        return unreal.Name(new_path_str)
    else:
        unreal.log_error(get_asset_path_with_new_name.__name__ + '(): object_path or new_name must not be empty')
        return unreal.Name('')


def get_asset_class_name_str(asset):
    return str(asset.get_editor_property('asset_class'))

## Getting asset data by object path
def get_asset_data_by_object_path(object_path, include_only_on_disk_assets = False):
    if general_ue.is_not_none_or_empty(object_path):
        if unreal.EditorAssetLibrary.does_asset_exist(object_path):
            asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
            assets_data = asset_registry.get_asset_by_object_path(object_path, include_only_on_disk_assets)
            return assets_data

        else:
            unreal.log_error(get_asset_data_by_object_path.__name__ + ': there is no asset by path: ' + object_path)
    else:
        unreal.log_error(get_asset_data_by_object_path.__name__ + ': object_path must not be empty or None')
        return

## Getting asset data by object
def get_asset_data_by_object(object):
    if object is not None:
        object_path = object.get_path_name()
        return unreal.EditorAssetLibrary.find_asset_data(object_path)
    else:
        unreal.log_error(get_asset_data_by_object.__name__ + ': object must not be None')
        return

## Getting asset UObject by object path
def get_asset_by_object_path(object_path, include_only_on_disk_assets = False):
    asset_data = get_asset_data_by_object_path(object_path, include_only_on_disk_assets)
    if asset_data is not None:
        return asset_data.get_asset()
    else:
        unreal.log_error(get_asset_by_object_path.__name__ + ': did not find any asset by path: object_path')
        return

def get_object_paths_by_data(data_assets):
    object_paths = []
    for data_asset in data_assets:
        object_paths.append(data_asset.get_editor_property('object_path'))
    return object_paths

def get_assets_from_assets_data(assets_data):
    assets = []
    if general_ue.is_not_none_or_empty(assets_data):
        for asset_data in assets_data:
            assets.append(asset_data.get_asset())
    else:
        unreal.log(get_assets_from_assets_data.__name__ + ': did not find any asset in assets_data')
    return assets


# Getting assets data by folder path
def get_assets_by_dir(package_path, is_recursive = False, include_only_on_disk_assets = False):
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    assets_data = asset_registry.get_assets_by_path(package_path, is_recursive, include_only_on_disk_assets)
    return assets_data

## Getting assets data by folder path
def get_assets_by_dirs(package_paths, is_recursive = False, include_only_on_disk_assets = False):
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    ue_filter = unreal.ARFilter(package_paths = package_paths, recursive_paths = is_recursive,
                                include_only_on_disk_assets = include_only_on_disk_assets)
    assets_data = asset_registry.get_assets(ue_filter)
    return assets_data

## Stay only assets of specified class name
# No return value
def assets_filter_by_class(assets_data, class_name):
    for asset_data in assets_data:
        if get_asset_class_name_str(asset_data) != str(class_name):
            assets_data.remove(asset_data)

## Stay only assets of specified class name
# Has return value
def assets_filter_by_class_r(assets_data, class_name):
    filtered_assets_data = assets_data.copy()
    assets_filter_by_class(filtered_assets_data, class_name)
    return filtered_assets_data

## @return assets data of specified type in path folder using ARFilter
def get_assets_data_by_dirs_n_classes(dir_paths, class_names, is_recursive_search = False,
                                       only_on_disk_assets = False, has_log = False):
    if has_log: unreal.log(dir_paths); unreal.log(class_names)

    if general_ue.is_not_none_or_empty(dir_paths) and general_ue.is_not_none_or_empty(class_names):
        for dir_path in dir_paths:
            if not dir_path.startswith(config.PATH_ASSETS_START):
                unreal.log_error(get_assets_data_by_dirs_n_classes.__name__ + ': path must be started from: /Game/')
                return
            if only_on_disk_assets and not unreal.EditorAssetLibrary.does_directory_exist(dir_path):
                unreal.log_error(get_assets_data_by_dirs_n_classes.__name__ + ': there is no such dir: ' + dir_path)
                return
        for class_name in class_names:
            if class_name == '':
                unreal.log_error(get_assets_data_by_dirs_n_classes.__name__ + ': class_name_p must be not empty')
                return

        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
        ue_filter = unreal.ARFilter(package_paths = dir_paths, class_names = class_names, recursive_paths = is_recursive_search,
                                    include_only_on_disk_assets = only_on_disk_assets, recursive_classes = True)
        if has_log: unreal.log(get_assets_data_by_dirs_n_classes.__name__ + ': Starts Searching')
        assets_data = asset_registry.get_assets(ue_filter)

        if has_log and (not general_ue.is_not_none_or_empty(assets_data)):
            unreal.log(get_assets_data_by_dirs_n_classes.__name__ + ': did not find any asset')
        return assets_data
    else:
        unreal.log_error(get_assets_data_by_dirs_n_classes.__name__ + ': paths or class_names must not be empty or None')
        return

def get_assets_data_by_dir_n_classes(dir_path, class_names, is_recursive_search = False,
                                       only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dirs_n_classes([dir_path], class_names, is_recursive_search, only_on_disk_assets, has_log)
def get_assets_by_dirs_n_classes(dir_paths, class_names, is_recursive_search = False,
                                 only_on_disk_assets = False, has_log = False):
    assets_data = get_assets_data_by_dirs_n_classes(dir_paths, class_names, is_recursive_search, only_on_disk_assets, has_log)
    return get_assets_from_assets_data(assets_data)
def get_assets_by_dir_n_classes(dir_path, class_names, is_recursive_search = False,
                                 only_on_disk_assets = False, has_log = False):
    return get_assets_by_dirs_n_classes([dir_path], class_names, is_recursive_search, only_on_disk_assets, has_log)


## Trim asset from list if not all of property_value pairs are True
# No return value
# Logical AND
def filter_assets_by_properties_conj(assets_data, properties_values, asset_data_index):
    asset = assets_data[asset_data_index].get_asset()
    all_properies_are_valid = True
    i = 0
    while all_properies_are_valid and i < len(properties_values):
        # if value is None, any value of property is valid
        if general_ue.is_not_none_or_empty(properties_values[i]):
            if (properties_values[i][1] is not None) and (asset.get_editor_property(properties_values[i][0]) != properties_values[i][1]):
                all_properies_are_valid = False
        else:
            unreal.log_error('filter_assets_by_properties_conj: Error in filter_assets_by_properties_conj. properties_values tuple must not be empty.')
        i += 1
    if not all_properies_are_valid:
        assets_data.remove(assets_data[asset_data_index])
        # When remove element. Next element will have current index. Len decreased
    else:
        asset_data_index += 1

    return asset_data_index

## Trim asset from list if not all of property_value pairs are True
# No return value
# Logical OR
def filter_assets_by_properties_disj(assets_data, properties_values, asset_data_index):
    asset = assets_data[asset_data_index].get_asset()
    no_one_properties_are_valid = True
    i = 0
    while no_one_properties_are_valid and i < len(properties_values):
        # if value is None, any value of property is valid
        if general_ue.is_not_none_or_empty(properties_values[i]):
            if properties_values[i][1] is None or asset.get_editor_property(properties_values[i][0]) == properties_values[i][1]:
                no_one_properties_are_valid = False
        else:
            unreal.log_error('filter_assets_by_properties_disj: Error in filter_assets_by_properties_disj. properties_values tuple must not be empty.')
        i += 1
    if no_one_properties_are_valid:
        assets_data.remove(assets_data[asset_data_index])
        # When remove element. Next element will have current index. Len decreased
    else:
        asset_data_index += 1

    return asset_data_index

## Trim asset from list if not all of property_value pairs are True
# Has return value
def filter_assets_by_properties_conj_r(assets_data, properties_values):
    new_assets_data = assets_data.copy()
    filter_assets_by_properties_conj(new_assets_data, properties_values)
    return new_assets_data

## Trim asset from list if not all of property_value pairs are True
# Has return value
def filter_assets_by_properties_disj_r(assets_data, properties_values):
    new_assets_data = assets_data.copy()
    filter_assets_by_properties_disj(new_assets_data, properties_values)
    return new_assets_data


## Trim asset from list if not all of property_value pairs are True
# No return value
def filter_assets_by_properties(assets_data, properties_values, is_disjunction):
    if general_ue.is_not_none_or_empty(assets_data) and general_ue.is_not_none_or_empty(properties_values):
        with unreal.ScopedSlowTask(len(assets_data), 'Applying filter by property values disjunction to assets') as slow_task:
            slow_task.make_dialog(True)
            asset_data_index = 0
            while asset_data_index < len(assets_data):
                if slow_task.should_cancel():
                    break
                if is_disjunction:
                    asset_data_index = filter_assets_by_properties_disj(assets_data, properties_values, asset_data_index)
                else:
                    asset_data_index = filter_assets_by_properties_conj(assets_data, properties_values, asset_data_index)

                slow_task.enter_progress_frame(1)


## Return assets of specified type in path folder
# properties_values is list of tuple [('property', value)]
# is_disjunction_p (^) = True will find asset,  if one of the property_value pair has been found. Disjunction is OR.
# is_disjunction_p (v) = False will find asset, if all of the property_value pair has been found. Conjunction is AND.
# If old value is None, all values will be valid and included in find results
# If there is no parameters, will find ALL assets. Needs more checks for parameters before call.
def find_assets_data(package_paths = [], package_names = [], object_paths = [], class_names = [], recursive_classes_exclusion_set = [],
                     recursive_paths = True, recursive_classes = False, include_only_on_disk_assets = False,
                     properties_values = [], is_disjunction = True, log_path = '', log_title = ''):
    assets_data = []
    if general_ue.is_not_none_lists([package_paths, package_names, object_paths, class_names, recursive_classes_exclusion_set,
                                  recursive_paths, recursive_classes, include_only_on_disk_assets, properties_values, is_disjunction]):
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
        ue_filter = unreal.ARFilter(package_names = package_names, package_paths = package_paths, object_paths = object_paths,
                                    class_names = class_names, recursive_classes_exclusion_set = recursive_classes_exclusion_set,
                                    recursive_paths = recursive_paths, recursive_classes = recursive_classes,
                                    include_only_on_disk_assets = include_only_on_disk_assets)
        unreal.log(find_assets_data.__name__ + '(): Start searching assets')
        assets_data = asset_registry.get_assets(ue_filter)
        if general_ue.is_not_none_or_empty(assets_data):
            unreal.log(find_assets_data.__name__ + '(): Assets without property filter count: ' + str(len(assets_data)) )
            if general_ue.is_not_none_or_empty(properties_values):
                filter_assets_by_properties(assets_data, properties_values, is_disjunction)
                unreal.log(find_assets_data.__name__ + '(): Property Filtered Assets count: ' + str(len(assets_data)) )
            else:
                unreal.log(find_assets_data.__name__ + '(): There is no properties_values for applying to filter assets.')
        else:
            unreal.log_error(find_assets_data.__name__ + '(): assets_data ' + config.IS_EMPTY_OR_NONE_TEXT)
    else:
        unreal.log_error(find_assets_data.__name__ + '(): input data must not be None')
    if log_path is not None and log_path != '':
        log.write_assets_data_log(assets_data, log_path, log_title)
    return assets_data

def find_assets(package_paths = [], package_names = [], object_paths = [], class_names = [], recursive_classes_exclusion_set = [],
                recursive_paths = True, recursive_classes = False, include_only_on_disk_assets = False,
                properties_values = [], is_disjunction = True, log_path = '', log_title = ''):
    assets_data = find_assets_data(package_paths, package_names, object_paths, class_names, recursive_classes_exclusion_set,
                                   recursive_paths, recursive_classes, include_only_on_disk_assets, properties_values,
                                   is_disjunction, log_path, log_title)
    return get_assets_from_assets_data(assets_data)


def get_textures_data_by_dirs(dir_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dirs_n_classes(dir_paths, [config.CLASS_NAME_TEXTURE, config.CLASS_NAME_TEXTURE_TWO_D],
                                             is_recursive_search, only_on_disk_assets, has_log)
def get_textures_data_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dir_n_classes(dir_path, [config.CLASS_NAME_TEXTURE, config.CLASS_NAME_TEXTURE_TWO_D],
                                            is_recursive_search, only_on_disk_assets, has_log)
def get_textures_by_dirs(dir_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dirs_n_classes(dir_paths, [config.CLASS_NAME_TEXTURE, config.CLASS_NAME_TEXTURE_TWO_D],
                                        is_recursive_search, only_on_disk_assets, has_log)
def get_textures_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dir_n_classes(dir_path, [config.CLASS_NAME_TEXTURE, config.CLASS_NAME_TEXTURE_TWO_D],
                                       is_recursive_search, only_on_disk_assets, has_log)


def get_materials_data_by_dirs(dir_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dirs_n_classes(dir_paths, [config.CLASS_NAME_MATERIAL], is_recursive_search, only_on_disk_assets, has_log)
def get_materials_data_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dir_n_classes(dir_path, [config.CLASS_NAME_MATERIAL], is_recursive_search, only_on_disk_assets, has_log)
def get_materials_by_dirs(dir_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dirs_n_classes(dir_paths, [config.CLASS_NAME_MATERIAL], is_recursive_search, only_on_disk_assets, has_log)
def get_materials_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dir_n_classes(dir_path, [config.CLASS_NAME_MATERIAL], is_recursive_search, only_on_disk_assets, has_log)

def get_static_mesh_data_by_dirs(dir_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dirs_n_classes(dir_paths, [config.CLASS_NAME_STATIC_MESH], is_recursive_search, only_on_disk_assets, has_log)
def get_static_mesh_data_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dir_n_classes(dir_path, [config.CLASS_NAME_STATIC_MESH], is_recursive_search, only_on_disk_assets, has_log)
def get_static_mesh_by_dirs(dir_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dirs_n_classes(dir_paths, [config.CLASS_NAME_STATIC_MESH], is_recursive_search, only_on_disk_assets, has_log)
def get_static_mesh_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dir_n_classes(dir_path, [config.CLASS_NAME_STATIC_MESH], is_recursive_search, only_on_disk_assets, has_log)

def get_skeletal_mesh_data_by_dirs(dir_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dirs_n_classes(dir_paths, [config.CLASS_NAME_SKELETAL_MESH], is_recursive_search, only_on_disk_assets, has_log)
def get_skeletal_mesh_data_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dir_n_classes(dir_path, [config.CLASS_NAME_SKELETAL_MESH], is_recursive_search, only_on_disk_assets, has_log)
def get_skeletal_mesh_by_dirs(dir_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dirs_n_classes(dir_paths, [config.CLASS_NAME_SKELETAL_MESH], is_recursive_search, only_on_disk_assets, has_log)
def get_skeletal_mesh_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dir_n_classes(dir_path, [config.CLASS_NAME_SKELETAL_MESH], is_recursive_search, only_on_disk_assets, has_log)


# Return list of static meshes and skeletal meshes
def get_static_skeletal_meshes_data_by_dirs(dir_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dirs_n_classes(dir_paths, [config.CLASS_NAME_STATIC_MESH, config.CLASS_NAME_SKELETAL_MESH],
                                             is_recursive_search, only_on_disk_assets, has_log)
def get_static_skeletal_meshes_data_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dir_n_classes(dir_path, [config.CLASS_NAME_STATIC_MESH, config.CLASS_NAME_SKELETAL_MESH],
                                            is_recursive_search, only_on_disk_assets, has_log)
def get_static_skeletal_meshes_by_dirs(dir_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dirs_n_classes(dir_paths, [config.CLASS_NAME_STATIC_MESH, config.CLASS_NAME_SKELETAL_MESH],
                                             is_recursive_search, only_on_disk_assets, has_log)
def get_static_skeletal_meshes_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dir_n_classes(dir_path, [config.CLASS_NAME_STATIC_MESH, config.CLASS_NAME_SKELETAL_MESH],
                                            is_recursive_search, only_on_disk_assets, has_log)


def get_material_texture_mesh_data_by_dirs(dirs_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_data_by_dirs_n_classes(dirs_paths,
                                            [config.CLASS_NAME_MATERIAL, config.CLASS_NAME_STATIC_MESH,
                                             config.CLASS_NAME_TEXTURE_TWO_D, config.CLASS_NAME_SKELETAL_MESH],
                                            is_recursive_search, only_on_disk_assets, has_log)
def get_material_texture_mesh_data_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_material_texture_mesh_data_by_dirs([dir_path], is_recursive_search, only_on_disk_assets, has_log)
def get_material_texture_mesh_by_dirs(dirs_paths, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_assets_by_dirs_n_classes(dirs_paths,
                                            [config.CLASS_NAME_MATERIAL, config.CLASS_NAME_STATIC_MESH,
                                             config.CLASS_NAME_TEXTURE_TWO_D, config.CLASS_NAME_SKELETAL_MESH],
                                            is_recursive_search, only_on_disk_assets, has_log)
def get_material_texture_mesh_by_dir(dir_path, is_recursive_search = False, only_on_disk_assets = False, has_log = False):
    return get_material_texture_mesh_by_dirs([dir_path], is_recursive_search, only_on_disk_assets, has_log)



def get_materials_data_two_sided(target_dirs, is_two_sided = False, is_recursive_search = True, only_on_disk_assets = False):
    materials_data = find_assets_data(package_paths = target_dirs, class_names = [config.CLASS_NAME_MATERIAL],
                                      recursive_paths = is_recursive_search,
                                      include_only_on_disk_assets = only_on_disk_assets,
                                      properties_values = [('two_sided', is_two_sided)])
    return materials_data

def get_materials_data_two_sided_log(log_path, log_title, target_dirs, is_two_sided = False, is_recursive_search = True,
                                     only_on_disk_assets = False):
    materials_data = find_assets_data(package_paths = target_dirs, class_names = [config.CLASS_NAME_MATERIAL],
                                        recursive_paths = is_recursive_search,
                                        include_only_on_disk_assets = only_on_disk_assets,
                                        properties_values = [('two_sided', is_two_sided)],
                                        log_path = log_path, log_title = log_title)
    return materials_data

def get_paths_of_materials_data_two_sided(target_dirs, is_two_sided = False, is_recursive_search = True, only_on_disk_assets = False):
    return get_paths_from_assets_data(get_materials_data_two_sided(target_dirs, is_two_sided, is_recursive_search, only_on_disk_assets))
def get_paths_of_materials_data_two_sided_log(log_path, log_title, target_dirs, is_two_sided = False, is_recursive_search = True, only_on_disk_assets = False):
    return get_paths_from_assets_data(get_materials_data_two_sided_log(log_path, log_title, target_dirs, is_two_sided,
                                                                       is_recursive_search, only_on_disk_assets))

def get_materials_data_two_sided_console(target_dirs, is_two_sided = False, is_recursive_search = True, only_on_disk_assets = False):
    paths_two_sided = get_paths_of_materials_data_two_sided(target_dirs, is_two_sided, is_recursive_search, only_on_disk_assets)
    for path in paths_two_sided:
        unreal.log(path)