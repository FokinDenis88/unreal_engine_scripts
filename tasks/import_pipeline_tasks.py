import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(os.path.join(WORKING_DIR, os.pardir), os.pardir)
sys.path.append(os.path.abspath(PARENT_DIR))

import unreal

import unreal_engine_scripts.service.log as log
import unreal_engine_scripts.src.import_pipeline as import_pipeline
import unreal_engine_scripts.tasks.import_pipeline_tasks_ini as import_pipeline_tasks_ini

#import unreal_engine_scripts.config as config
#import unreal_engine_scripts.service.general_ue as general_ue
#import unreal_engine_scripts.src.get_asset as get_asset
#import unreal_engine_scripts.src.asset_library as asset_library
#import unreal_engine_scripts.src.material_library as material_library
#import unreal_engine_scripts.src.prefix_suffix as prefix_suffix
#import unreal_engine_scripts.src.set_material as set_material
#import unreal_engine_scripts.src.get_static_mesh as get_static_mesh

import importlib
importlib.reload(log)
importlib.reload(import_pipeline)
importlib.reload(import_pipeline_tasks_ini)

#importlib.reload(config)
#importlib.reload(general_ue)
#importlib.reload(get_asset)
#importlib.reload(asset_library)
#importlib.reload(material_library)
#importlib.reload(prefix_suffix)
#importlib.reload(set_material)
#importlib.reload(get_static_mesh)

from unreal_engine_scripts.tasks.import_pipeline_tasks_ini import *

## Modes of import pipeline: Hybrid, glTF_Importer, Datasmith_glTF_Importer, Datasmith_glTF_Importer_Factory, Code4Game
# It is recommend to use only Hybrid pipeline
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