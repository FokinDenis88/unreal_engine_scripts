import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(os.path.join(WORKING_DIR, os.pardir), os.pardir)
sys.path.append(os.path.abspath(PARENT_DIR))

import unreal

import unreal_scripts.service.log as log
import unreal_scripts.src.import_pipeline as import_pipeline
import unreal_scripts.tasks.import_pipeline_tasks_ini as import_pipeline_tasks_ini

#import unreal_scripts.config as config
#import unreal_scripts.service.general as general
#import unreal_scripts.src.get_asset as get_asset
#import unreal_scripts.src.asset_library as asset_library
#import unreal_scripts.src.material_library as material_library
#import unreal_scripts.src.prefix_suffix as prefix_suffix
#import unreal_scripts.src.set_material as set_material
#import unreal_scripts.src.get_static_mesh as get_static_mesh

import importlib
importlib.reload(log)
importlib.reload(import_pipeline)
importlib.reload(import_pipeline_tasks_ini)

#importlib.reload(config)
#importlib.reload(general)
#importlib.reload(get_asset)
#importlib.reload(asset_library)
#importlib.reload(material_library)
#importlib.reload(prefix_suffix)
#importlib.reload(set_material)
#importlib.reload(get_static_mesh)

from unreal_scripts.tasks.import_pipeline_tasks_ini import *


def main():
    if IMPORT_METHOD == 'Hybrid':
        unreal.log('import_pipeline.py: Hybrid Started.')
        #fbx_paths, glb_paths, subobjects_paths = prepare_paths_datasmith(IMPORT_DIRS, FBX_FILE_NAMES, GLB_FILE_NAMES,
                                                                         #SUBOBJECTS_DIR_NAME, SUBOBJECTS_NAMES)
        fbx_paths, gltf_paths, subobjects_paths = import_pipeline.prepare_paths_gltf(IMPORT_DIRS, FBX_FILE_NAMES, GLTF_FILE_NAMES,
                                                                                     SUBOBJECTS_DIR_NAME, SUBOBJECTS_NAMES)
        log.log_list(['fbx paths: ', fbx_paths])
        log.log_list(['gltf paths: ', gltf_paths])
        log.log_list(['subobjects_paths paths: ', subobjects_paths])
        import_pipeline.import_assets_pipeline_hybrid(fbx_paths, gltf_paths, DESTINATION_DIRS, subobjects_paths,
                                                      AUTOMATED, TO_RECOMPILE, TO_IMPORT_FBX_MATERIAL_INSTANCE_FILE)

    elif IMPORT_METHOD == 'glTF_Importer':
        unreal.log('import_pipeline.py: glTF_Importer Started.')
        fbx_paths, gltf_paths, subobjects_paths = import_pipeline.prepare_paths_gltf(IMPORT_DIRS, FBX_FILE_NAMES, GLTF_FILE_NAMES,
                                                                                    SUBOBJECTS_DIR_NAME, SUBOBJECTS_NAMES)
        log.log_list(['fbx paths: ', fbx_paths])
        log.log_list(['gltf paths: ', gltf_paths])
        log.log_list(['subobjects_paths paths: ', subobjects_paths])
        import_pipeline.import_assets_pipeline(fbx_paths, gltf_paths, DESTINATION_DIRS, subobjects_paths,
                                               ONLY_ON_DISK_ASSETS, TO_REPLACE_TEXTURE_SAMPLES)

    elif IMPORT_METHOD == 'Datasmith_glTF_Importer':
        unreal.log('import_pipeline.py: Datasmith_glTF_Importer Started.')
        fbx_paths, glb_paths, subobjects_paths = import_pipeline.prepare_paths_datasmith(IMPORT_DIRS, FBX_FILE_NAMES, GLB_FILE_NAMES,
                                                                                         SUBOBJECTS_DIR_NAME, SUBOBJECTS_NAMES)
        log.log_list(['fbx paths: ', fbx_paths])
        log.log_list(['glb paths: ', glb_paths])
        log.log_list(['subobjects_paths paths: ', subobjects_paths])
        import_pipeline.import_assets_pipeline_datasmith(fbx_paths, glb_paths, DESTINATION_DIRS, subobjects_paths, ONLY_ON_DISK_ASSETS)

    elif IMPORT_METHOD == 'Datasmith_glTF_Importer_Factory':
        unreal.log('import_pipeline.py: Datasmith_glTF_Importer_Factory Started.')
        fbx_paths, glb_paths, subobjects_paths = import_pipeline.prepare_paths_datasmith(IMPORT_DIRS, FBX_FILE_NAMES, GLB_FILE_NAMES,
                                                                                         SUBOBJECTS_DIR_NAME, SUBOBJECTS_NAMES)
        log.log_list(['fbx paths: ', fbx_paths])
        log.log_list(['glb paths: ', glb_paths])
        log.log_list(['subobjects_paths paths: ', subobjects_paths])
        import_pipeline.import_assets_pipeline_datasmith_factory(fbx_paths, glb_paths, DESTINATION_DIRS, subobjects_paths, ONLY_ON_DISK_ASSETS)

    elif IMPORT_METHOD == 'Code4Game':
        import_pipeline.import_assets_pipeline_code4game(fbx_paths, gltf_paths, DESTINATION_DIRS, subobjects_paths, ONLY_ON_DISK_ASSETS)


main()

'''
1) Разобраться, что лучше material vs material instance
2) Удалить суффиксы из нодов
3) Попробовать повлиять на настройки импорта фабрики, найти другие фабрики импорта
'''


'''
assets_data = get_asset.get_assets_by_dir('/Game/Import/glb/Materials/', True)
unreal.log(assets_data)
unreal.log(assets_data[0].get_editor_property('asset_name'))
'''

'''
assets_data = get_asset.get_assets_by_dir('/Game/Import/Materials')
for asset_data in assets_data:
    asset_class = general.Name_to_str(asset_data.get_editor_property('asset_class'))
    unreal.log(asset_class)
'''

'''
path = '/Game/M_Staff_04'
material = unreal.EditorAssetLibrary.load_asset(path)
set_material.delete_nodes_trash_suffix(material)
'''

#unreal.EditorAssetLibrary.save_asset(path)
#unreal.MaterialEditingLibrary.recompile_material(material)


'''
path = '/Game/Import/glb/Materials/Master'
materials_data = get_asset.get_materials_data_by_dir(path)
unreal.log(materials_data)
'''

'''
path = '/Game/Import/Materials/Master'
materials_data = get_asset.get_materials_data_by_dir(path)
unreal.log(materials_data)
#set_material.delete_nodes_trash_suffix_in_dir(path)
'''

'''
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
glb_import_options = None  # unreal.DatasmithGLTFImportOptions | unreal.GLTFImportOptions
gltf_import_factory = unreal.GLTFImportFactory()
glb_path = 'K:/!Development K/Projects/3D Models/!!Assets For Commercial/3D/!!3D Models For Commercial/Military/!Vehicle/Modern/Water/Ship/Samidare destroyer___sketchfab/export/glb.glb'
destination_dir = '/Game/Import'
glb_asset_task = new_asset_import_task(glb_path, destination_dir, automated = False, factory = gltf_import_factory,
                                        save = False, replace_existing = False, options = glb_import_options)
if not make_import_asset_task(glb_asset_task, asset_tools, 'did not imported glb file'):
    unreal.log_error('import fail')
'''


'''
static_mesh_path = '/Game/Test/SM_SamidareDestroyer'
static_mesh = get_asset.load_asset(static_mesh_path)

#unreal.log(get_static_mesh.get_static_mesh_triangles_count(static_mesh))
lod_index = 0
#sections_count = static_mesh.get_num_sections(lod_index)
sections_count = 1
unreal.log(sections_count)
triangles_count = 0
for section_index in range(sections_count):
    triangles = unreal.ProceduralMeshLibrary.get_section_from_static_mesh(static_mesh, lod_index, section_index)[1]
    triangles_count += len(triangles)

unreal.log(triangles_count)
'''

'''
# Check Two Sided
assets_path = '/Game/ThirdPerson/Military/Weapon'
get_asset.get_materials_data_two_sided_console([assets_path], True)
'''