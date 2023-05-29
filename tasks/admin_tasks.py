import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(os.path.join(WORKING_DIR, os.pardir), os.pardir)
# Folder, that stores unreal_engine_python_scripts package
sys.path.append(os.path.abspath(PARENT_DIR))

import unreal

import importlib
import unreal_engine_python_scripts.tasks.admin_tasks_ini as admin_tasks_ini
importlib.reload(admin_tasks_ini)

import unreal_engine_python_scripts.src.get_asset as get_asset
import unreal_engine_python_scripts.src.set_asset as set_asset
import unreal_engine_python_scripts.src.set_material as set_material
import unreal_engine_python_scripts.src.lod as lod
import unreal_engine_python_scripts.src.collision as collision
import unreal_engine_python_scripts.src.material_library as material_library
import unreal_engine_python_scripts.service.log as log

# To apply changes in modules

importlib.reload(get_asset)
importlib.reload(set_asset)
importlib.reload(set_material)
importlib.reload(lod)
importlib.reload(collision)
importlib.reload(material_library)
importlib.reload(log)

from unreal_engine_python_scripts.tasks.admin_tasks_ini import *

## Can call one of functions: lod.find_no_mipmap_textures_log, lod.find_no_lods_meshes_log,
# get_asset.find_assets_data_log, set_asset.set_assets_properties_in_folder_log,
# lod.activate_textures_gen_mipmaps_log, lod.activate_meshes_gen_lods_log,
# collision.find_no_collision_assets, set_material.set_materials_two_sided
# get_asset.get_materials_data_two_sided_console, material_library.auto_align_materials_nodes_paths
def main():
    if COMMAND == 'NoMipMap':
        lod.find_no_mipmap_textures_log(TARGET_PATHS, IS_RECURSIVE_SEARCH, ONLY_ON_DISK_ASSETS)
    elif COMMAND == 'NoLods':
        lod.find_no_lods_meshes_log(TARGET_PATHS, IS_RECURSIVE_SEARCH, ONLY_ON_DISK_ASSETS)
    elif COMMAND == 'Find':
        get_asset.find_assets_data_log(log.LOG_PATH_FIND_ASSETS, 'Find Assets', package_paths = TARGET_PATHS,
                                       class_names = TARGET_CLASS_NAMES,
                                       recursive_paths = IS_RECURSIVE_SEARCH,
                                       include_only_on_disk_assets = ONLY_ON_DISK_ASSETS,
                                       properties_values = SEARCH_PROPERTIES_VALUES, is_disjunction = IS_DISJUNCTION)
    elif COMMAND == 'SetProperties':
        set_asset.set_assets_properties_in_folder_log(log.LOG_PATH_SET_PROPERTIES,'Set assets properties',
                                                      TARGET_PATHS, IS_RECURSIVE_SEARCH,
                                                      ONLY_ON_DISK_ASSETS, TARGET_CLASS_NAMES,
                                                      SEARCH_PROPERTIES_VALUES, NEW_PROPERTIES_VALUES)
    elif COMMAND == 'activate_textures_gen_mipmaps':
        lod.activate_textures_gen_mipmaps_log(TARGET_PATHS, IS_RECURSIVE_SEARCH,
                                              ONLY_ON_DISK_ASSETS, SEARCH_PROPERTIES_VALUES, IS_DISJUNCTION)
    elif COMMAND == 'activate_meshes_gen_lods':
        lod.activate_meshes_gen_lods_log(TARGET_PATHS, IS_RECURSIVE_SEARCH,
                                         ONLY_ON_DISK_ASSETS, SEARCH_PROPERTIES_VALUES, IS_DISJUNCTION)
    elif COMMAND == 'NoCollision':
        collision.find_no_collision_assets(TARGET_PATHS, log.LOG_PATH_NO_COLLISION, IS_RECURSIVE_SEARCH, ONLY_ON_DISK_ASSETS)
    elif COMMAND == 'MaterialTwoSided':
        set_material.set_materials_two_sided(TARGET_PATHS, MATERIAL_TWO_SIDED, IS_RECURSIVE_SEARCH,
                                             ONLY_ON_DISK_ASSETS, SEARCH_PROPERTIES_VALUES, IS_DISJUNCTION)
    elif COMMAND == 'GetMaterialTwoSided':
        get_asset.get_materials_data_two_sided_console(TARGET_PATHS, MATERIAL_TWO_SIDED)
    elif COMMAND == 'LayoutMaterialNodes':
        material_library.auto_align_materials_nodes_paths(TARGET_PATHS)

main()