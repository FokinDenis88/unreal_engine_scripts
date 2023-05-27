# Use for Auto_connect Textures files and nodes to material output node

import os
import sys
from tkinter import COMMAND
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(os.path.join(WORKING_DIR, os.pardir), os.pardir)
sys.path.append(os.path.abspath(PARENT_DIR))

import unreal

import unreal_scripts.config as config
#import unreal_scripts.src.get_asset as get_asset
import unreal_scripts.src.get_material as get_material
#import unreal_scripts.src.prefix_suffix as prefix_suffix
import unreal_scripts.src.material_library as material_library
import unreal_scripts.tasks.auto_connect_ini as auto_connect_ini
#import unreal_scripts.asset.material_node as material_node

import importlib
importlib.reload(config)
#importlib.reload(get_asset)
importlib.reload(get_material)
#importlib.reload(prefix_suffix)
importlib.reload(material_library)
importlib.reload(auto_connect_ini)
#importlib.reload(material_node)

from unreal_scripts.tasks.auto_connect_ini import *

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


'''
#material_library.auto_align_material_nodes(get_asset.get_asset_by_object_path('/Game/Test/Materials/M_Staff_03.M_Staff_03'))
material_path = '/Game/Test/Materials/Test.Test'
material = get_asset.get_asset_by_object_path(material_path)
unreal.log('Material:')
unreal.log(material)

textures = unreal.MaterialEditingLibrary.get_used_textures(material)
unreal.log('Textures:')
unreal.log(textures)

unreal.log('Used textures:')

for texture in textures:
    unreal.log(texture)

texture_param_names = unreal.MaterialEditingLibrary.get_texture_parameter_names(material)
unreal.log('texture_param_names:')
unreal.log(texture_param_names)

unreal.log('get_scalar_parameter_names')
unreal.log(unreal.MaterialEditingLibrary.get_scalar_parameter_names(material))

unreal.log('get_num_material_expressions')
unreal.log(unreal.MaterialEditingLibrary.get_num_material_expressions(material))

unreal.log('get_path_from_object')
unreal.log(get_asset.get_path_from_object(material))

unreal.EditorAssetLibrary.load_asset(material_path)
#texture_node = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionAdd)
#texture_node = unreal.MaterialEditingLibrary.create_material_expression(material, config.TextureNode)

material_test = get_asset.get_asset_by_object_path('/Game/Test/Materials/M_Staff_04.M_Staff_04')
material_library.auto_align_material_nodes(material_test)


unreal.EditorAssetLibrary.load_asset(material_path)
with unreal.ScopedEditorTransaction('Transaction 1') as ue_transaction:
    unreal.log('Transaction 1')
    texture_node = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionAdd)
    with unreal.ScopedEditorTransaction('Transaction 2') as ue_transaction:
        unreal.log('Transaction 2')
        texture_node = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionAdd)
'''

'''
material_path = '/Game/Test/Auto/Materials/Test.Test'
#material_path = '/Game/Test/Auto/Materials/NodesCount.NodesCount'

material = unreal.EditorAssetLibrary.load_asset(material_path)

#material_data = get_asset.get_asset_data_by_object(material)
#material_library.auto_align_material_node_data(material_data)
#material_library.auto_align_material_nodes(material)
unreal.MaterialEditingLibrary.layout_material_expressions(material)

#unreal.log(get_material.get_material_all_nodes_by_path('/Game/Test/Auto/Materials/Test.Test'))

#material, found_nodes = get_material.find_nodes_in_material_by_path(material_path)
#material, found_nodes = get_material.find_nodes_in_material_by_path(material_path, [unreal.MaterialExpressionMultiply])
#material, found_nodes = get_material.find_nodes_in_material_by_path(material_path, [unreal.MaterialExpressionTextureBase], is_nodes_types_subclasses = True)
#material, found_nodes = get_material.find_nodes_in_material_by_path(material_path, is_linked_to_output = True)
#material, found_nodes = get_material.find_nodes_in_material_by_path(material_path, properties_values = [('parameter_name', 'Metallic Factor')])


#found_nodes = unreal.PythonMaterialLib.get_material_expressions(material)

#unreal.log(material)
#unreal.log(found_nodes)
#unreal.log(len(found_nodes))
'''

'''
material_path = '/Game/Test/Auto/Materials/Replace/ReplaceSample.ReplaceSample'
material = unreal.EditorAssetLibrary.load_asset(material_path)
texture_sample_nodes = get_material.find_nodes_in_material(material, [unreal.MaterialExpressionTextureSample, unreal.MaterialExpressionTextureSampleParameter2D])
#texture_sample_nodes = get_material.find_nodes_in_material(material, [unreal.MaterialExpressionTextureSample])
unreal.log(texture_sample_nodes)
#unreal.log(issubclass(unreal.MaterialExpressionTextureSampleParameter2D, unreal.MaterialExpressionTextureSampleParameter2D))


a = material_node.MetaDataTextureSampleParameter2DExt()
b = material_node.MetaDataTextureSampleParameter2D()
unreal.log(isinstance(a, type(b)))
unreal.log(issubclass(type(b), type(a)))
unreal.log(type(a) == material_node.MetaDataTextureSampleParameter2DExt)
unreal.log(type(a) is material_node.MetaDataTextureSampleParameter2DExt)
'''

'''
material_path = '/Game/Test/Auto/Materials/Test.Test'
material = unreal.EditorAssetLibrary.load_asset(material_path)

unlinked_nodes = get_material.find_unlinked_texture_nodes(material)
unreal.log(unlinked_nodes)
'''