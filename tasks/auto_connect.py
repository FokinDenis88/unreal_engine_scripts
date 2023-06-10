# Use for Auto_connect Textures files and nodes to material output node

import os
import sys
from tkinter import COMMAND
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(os.path.join(WORKING_DIR, os.pardir), os.pardir)
sys.path.append(os.path.abspath(PARENT_DIR))

import unreal

import unreal_engine_scripts.config as config
#import unreal_engine_scripts.src.get_asset as get_asset
import unreal_engine_scripts.src.get_material as get_material
#import unreal_engine_scripts.src.prefix_suffix as prefix_suffix
import unreal_engine_scripts.src.material_library as material_library
import unreal_engine_scripts.tasks.auto_connect_ini as auto_connect_ini
#import unreal_engine_scripts.asset.material_node as material_node

import importlib
importlib.reload(config)
#importlib.reload(get_asset)
importlib.reload(get_material)
#importlib.reload(prefix_suffix)
importlib.reload(material_library)
importlib.reload(auto_connect_ini)
#importlib.reload(material_node)

from unreal_engine_scripts.tasks.auto_connect_ini import *

## Can call one of functions: material_library.connect_by_association_texture_file_dirs,
# material_library.connect_texture_files_packs, material_library.connect_textures_files_to_materials
# material_library.connect_free_texture_nodes_in_materials_by_dirs, material_library.auto_align_material_nodes_path
# material_library.replace_texture_sample_to_parameters_by_dirs
def main():
    material_library.bump_texture_link_version = LINK_VERSION_BUMP_TEXTURE
    if COMMAND == 'ConnectByAssociation':
        material_library.connect_by_association_texture_file_dirs(MATERIAL_ASSOCIATION_DIRS, TEXTURE_ASSOCIATION_DIRS, RECOMPILE, AUTO_ALIGN)
    if COMMAND == 'ConnectTexturePacks':
        material_library.connect_texture_files_packs(MATERIAL_PATHS, TEXTURE_PATHS_PACKS, RECOMPILE, AUTO_ALIGN, 0, 0)
    elif COMMAND == 'ConnectTextureFiles':
        material_library.connect_textures_files_to_materials(MATERIAL_FILES, TEXTURE_FILES, RECOMPILE, AUTO_ALIGN, 0, 0)
    elif COMMAND == 'ConnectFreeNodes':
        material_library.connect_free_texture_nodes_in_materials_by_dirs(MATERIALS_DIRS_FREE_NODES)
    elif COMMAND == 'AutoAlign':
        material_library.auto_align_material_nodes_path(MATERIAL_FILES)
    elif COMMAND == 'ReplaceTextureSamples':
        material_library.replace_texture_sample_to_parameters_by_dirs(MATERIAL_REPLACE_DIRS)


main()