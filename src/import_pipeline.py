import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(os.path.join(WORKING_DIR, os.pardir), os.pardir)
sys.path.append(os.path.abspath(PARENT_DIR))

import unreal

#import unreal_engine_scripts.config as config
import unreal_engine_scripts.service.general as general
import unreal_engine_scripts.src.get_asset as get_asset
import unreal_engine_scripts.src.set_asset as set_asset
import unreal_engine_scripts.src.asset_library as asset_library
import unreal_engine_scripts.src.material_library as material_library
import unreal_engine_scripts.src.prefix_suffix as prefix_suffix
import unreal_engine_scripts.src.set_material as set_material

import importlib
#importlib.reload(config)
importlib.reload(general)
importlib.reload(get_asset)
importlib.reload(set_asset)
importlib.reload(asset_library)
importlib.reload(material_library)
importlib.reload(prefix_suffix)
importlib.reload(set_material)


## Plugins set used for importing pipeline
IMPORT_PIPELINE_VARIANTS = {'glTF_Importer', 'Datasmith_glTF_Importer', 'Code4Game'}


## @param bake_pivot_in_vertex (bool): [Read-Write] - Experimental - If this option is true the inverse node pivot will be apply to the mesh vertices. The pivot from the DCC will then be the origin of the mesh. This option only work with static meshes.
# @param create_content_folder_hierarchy (bool): [Read-Write] If checked, a folder’s hierarchy will be created under the import asset path. All the created folders will match the actor hierarchy. In case there is more than one actor that links to an asset, the shared asset will be placed at the first actor’s place.
# @param force_front_x_axis (bool): [Read-Write] Whether to force the front axis to be align with X instead of -Y.
# @param hierarchy_type (FBXSceneOptionsCreateHierarchyType): [Read-Write] Choose if you want to generate the scene hierarchy with normal level actors, one actor with multiple components, or one blueprint asset with multiple components.
# @param import_as_dynamic (bool): [Read-Write] If checked, the mobility of all actors or components will be dynamic. If unchecked, they will be static.
# @param import_skeletal_mesh_lo_ds (bool): [Read-Write] If enabled, creates LOD models for Unreal skeletal meshes from LODs in the import file; If not enabled, only the base skeletal mesh from the LOD group is imported.
# @param import_static_mesh_lo_ds (bool): [Read-Write] If enabled, creates LOD models for Unreal static meshes from LODs in the import file; If not enabled, only the base static mesh from the LOD group is imported.
# @param invert_normal_maps
def new_fbx_scene_import_options(bake_pivot_in_vertex = False, create_content_folder_hierarchy = False,
                                 force_front_x_axis = True,
                                 hierarchy_type = None, import_as_dynamic = False,
                                 import_skeletal_mesh_lo_ds = True,
                                 import_static_mesh_lo_ds = True, invert_normal_maps = False):
    import_options = unreal.FbxSceneImportOptions()
    import_options.set_editor_property('bake_pivot_in_vertex',              bake_pivot_in_vertex)
    import_options.set_editor_property('create_content_folder_hierarchy',   create_content_folder_hierarchy)
    import_options.set_editor_property('force_front_x_axis',                force_front_x_axis)
    import_options.set_editor_property('hierarchy_type',                    hierarchy_type)
    import_options.set_editor_property('import_as_dynamic',                 import_as_dynamic)
    import_options.set_editor_property('import_skeletal_mesh_lo_ds',        import_skeletal_mesh_lo_ds)
    import_options.set_editor_property('import_static_mesh_lo_ds',          import_static_mesh_lo_ds)
    import_options.set_editor_property('invert_normal_maps',                invert_normal_maps)
    return import_options



## @param auto_generate_collision (bool): [Read-Write] If checked, collision will automatically be generated (ignored if custom collision is imported or used).
# @param build_adjacency_buffer (bool): [Read-Write] Required for PNT tessellation but can be slow. Recommend disabling for larger meshes.
# @param build_reversed_index_buffer (bool): [Read-Write] Build Reversed Index Buffer
# @param generate_lightmap_u_vs (bool): [Read-Write] Generate Lightmap UVs
# @param normal_generation_method (FBXSceneNormalGenerationMethod): [Read-Write] Use the MikkTSpace tangent space generator for generating normals and tangents on the mesh
# @param normal_import_method (FBXSceneNormalImportMethod): [Read-Write] Enabling this option will read the tangents(tangent,binormal,normal) from FBX file instead of generating them automatically.
# @param one_convex_hull_per_ucx (bool): [Read-Write] If checked, one convex hull per UCX_ prefixed collision mesh will be generated instead of decomposing into multiple hulls
# @param remove_degenerates (bool): [Read-Write] Disabling this option will keep degenerate triangles found. In general you should leave this option on.
# @param vertex_color_import_option (FbxSceneVertexColorImportOption): [Read-Write] Specify how vertex colors should be imported
# @param vertex_override_color (Color): [Read-Write] Specify override color in the case that VertexColorImportOption is set to Override'''
def new_fbx_scene_import_options_static_mesh(auto_generate_collision = True, build_adjacency_buffer = False,
                                             build_reversed_index_buffer = False,
                                             generate_lightmap_u_vs = True,
                                             normal_generation_method = unreal.FBXSceneNormalGenerationMethod.MIKK_T_SPACE,
                                             normal_import_method = unreal.FBXSceneNormalImportMethod.FBX_SCENE_NIM_IMPORT_NORMALS_AND_TANGENTS,
                                             one_convex_hull_per_ucx = False,
                                             remove_degenerates = True,
                                             vertex_color_import_option = None, vertex_override_color = None):
    import_options = unreal.FbxSceneImportOptionsStaticMesh()
    import_options.set_editor_property('auto_generate_collision',       auto_generate_collision)
    import_options.set_editor_property('build_adjacency_buffer',        build_adjacency_buffer)
    import_options.set_editor_property('build_reversed_index_buffer',   build_reversed_index_buffer)
    import_options.set_editor_property('generate_lightmap_u_vs',        generate_lightmap_u_vs)
    import_options.set_editor_property('normal_generation_method',      normal_generation_method)
    import_options.set_editor_property('normal_import_method',          normal_import_method)
    import_options.set_editor_property('one_convex_hull_per_ucx',       one_convex_hull_per_ucx)
    import_options.set_editor_property('remove_degenerates',            remove_degenerates)
    import_options.set_editor_property('vertex_color_import_option',    vertex_color_import_option)
    import_options.set_editor_property('vertex_override_color',         vertex_override_color)
    return import_options



## @param animation_length (FBXAnimationLengthImportType): [Read-Write] Type of asset to import from the FBX file
# @param create_physics_asset (bool): [Read-Write] If checked, create new PhysicsAsset if it doesn’t have it
# @param custom_sample_rate (int32): [Read-Write] Sample fbx animation data at the specified sample rate, 0 find automaticaly the best sample rate
# @param delete_existing_custom_attribute_curves (bool): [Read-Write] If true, all previous custom attribute curves will be deleted when doing a re-import.
# @param delete_existing_morph_target_curves (bool): [Read-Write] Type of asset to import from the FBX file
# @param delete_existing_non_curve_custom_attributes (bool): [Read-Write] If true, all previous non-curve custom attributes will be deleted when doing a re-import.
# @param frame_import_range (Int32Interval): [Read-Write] Frame range used when Set Range is used in Animation Length
# @param import_animations (bool): [Read-Write] True to import animations from the FBX File
# @param import_custom_attribute (bool): [Read-Write] Import if custom attribute as a curve within the animation *
# @param import_meshes_in_bone_hierarchy (bool): [Read-Write] If checked, meshes nested in bone hierarchies will be imported instead of being converted to bones.
# @param import_morph_targets (bool): [Read-Write] If enabled, creates Unreal morph objects for the imported meshes
# @param morph_threshold_position (float): [Read-Write] Threshold to compare vertex position equality when computing morph target deltas.
# @param preserve_local_transform (bool): [Read-Write] Type of asset to import from the FBX file
# @param preserve_smoothing_groups (bool): [Read-Write] If checked, triangles with non-matching smoothing groups will be physically split.
# @param threshold_position (float): [Read-Write] Threshold to compare vertex position equality.
# @param threshold_tangent_normal (float): [Read-Write] Threshold to compare normal, tangent or bi-normal equality.
# @param threshold_uv (float): [Read-Write] Threshold to compare UV equality.
# @param update_skeleton_reference_pose (bool): [Read-Write] If enabled, update the Skeleton (of the mesh being imported)’s reference pose.
# @param use_default_sample_rate (bool): [Read-Write] If enabled, samples all animation curves to 30 FPS'''
def new_fbx_scene_import_options_skeletal_mesh(animation_length = None, create_physics_asset = True, custom_sample_rate = 0,
                                               delete_existing_custom_attribute_curves = True,
                                               delete_existing_morph_target_curves = True,
                                               delete_existing_non_curve_custom_attributes = True,
                                               frame_import_range = None, import_animations = True,
                                               import_custom_attribute = True, import_meshes_in_bone_hierarchy = True,
                                               import_morph_targets = True, morph_threshold_position = 0,
                                               preserve_local_transform = False,
                                               preserve_smoothing_groups = False, threshold_position = 0,
                                               threshold_tangent_normal = 0, threshold_uv = 0,
                                               update_skeleton_reference_pose = True, use_default_sample_rate = False):
    import_options = unreal.FbxSceneImportOptionsSkeletalMesh()
    import_options.set_editor_property('animation_length',                              animation_length)
    import_options.set_editor_property('create_physics_asset',                          create_physics_asset)
    import_options.set_editor_property('custom_sample_rate',                            custom_sample_rate)
    import_options.set_editor_property('delete_existing_custom_attribute_curves',       delete_existing_custom_attribute_curves)
    import_options.set_editor_property('delete_existing_morph_target_curves',           delete_existing_morph_target_curves)
    import_options.set_editor_property('delete_existing_non_curve_custom_attributes',   delete_existing_non_curve_custom_attributes)
    import_options.set_editor_property('frame_import_range',                            frame_import_range)
    import_options.set_editor_property('import_animations',                             import_animations)
    import_options.set_editor_property('import_custom_attribute',                       import_custom_attribute)
    import_options.set_editor_property('import_meshes_in_bone_hierarchy',               import_meshes_in_bone_hierarchy)
    import_options.set_editor_property('import_morph_targets',                          import_morph_targets)
    import_options.set_editor_property('morph_threshold_position',                      morph_threshold_position)
    import_options.set_editor_property('preserve_local_transform',                      preserve_local_transform)
    import_options.set_editor_property('preserve_smoothing_groups',                     preserve_smoothing_groups)
    import_options.set_editor_property('threshold_position',                            threshold_position)
    import_options.set_editor_property('threshold_tangent_normal',                      threshold_tangent_normal)
    import_options.set_editor_property('threshold_uv',                                  threshold_uv)
    import_options.set_editor_property('update_skeleton_reference_pose',                update_skeleton_reference_pose)
    import_options.set_editor_property('use_default_sample_rate',                       use_default_sample_rate)
    return import_options


## Create new Task for import Asset.
# @param automated (bool): [Read-Write] Avoid dialogs
# @param destination_name (str): [Read-Write] Optional custom name to import as
# @param destination_path (str): [Read-Write] Path where asset will be imported to
# @param factory (Factory): [Read-Write] Optional factory to use
# @param filename (str): [Read-Write] Filename to import
# @param imported_object_paths (Array(str)): [Read-Write] Paths to objects created or updated after import
# @param options (Object): [Read-Write] Import options specific to the type of asset
# @param replace_existing (bool): [Read-Write] Overwrite existing assets
# @param replace_existing_settings (bool): [Read-Write] Replace existing settings when overwriting existing assets
# @param result (Array(Object)): [Read-Write] Imported objects
# @param save (bool): [Read-Write] Save after importing '''
def new_asset_import_task(filename, destination_path, automated = False, save = False,
                          replace_existing = False, replace_existing_settings = False, options = None,
                          factory = None, imported_object_paths = [], destination_name = '', result = []):
    asset_task = unreal.AssetImportTask()
    asset_task.set_editor_property('automated', automated)
    asset_task.set_editor_property('destination_name', destination_name)
    asset_task.set_editor_property('destination_path', destination_path)
    asset_task.set_editor_property('factory', factory)
    asset_task.set_editor_property('filename', filename)
    asset_task.set_editor_property('imported_object_paths', imported_object_paths)
    asset_task.set_editor_property('options', options)
    asset_task.set_editor_property('replace_existing', replace_existing)
    asset_task.set_editor_property('replace_existing_settings', replace_existing_settings)
    asset_task.set_editor_property('result', result)
    asset_task.set_editor_property('save', save)
    return asset_task

def new_gltf_options(generate_lightmap_u_vs = True, import_scale = 100.0):
    options = unreal.GLTFImportOptions()
    options.set_editor_property('generate_lightmap_u_vs', generate_lightmap_u_vs)
    options.set_editor_property('import_scale', import_scale)
    return options

    #FbxSceneImportOptions
    #FbxSceneImportOptionsStaticMesh
    #FbxSceneImportOptionsSkeletalMesh

    #unreal.DatasmithStaticMeshImportOptions
    #unreal.DatasmithGLTFImportOptions

## Making import of asset executing list of import_asset_tasks
def exec_import_asset_tasks(import_asset_tasks, asset_tools = None):
    if (import_asset_tasks is not None) and (import_asset_tasks != []):
        if asset_tools is None: asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        asset_tools.import_asset_tasks(import_asset_tasks)
    else:
        unreal.log_error(exec_import_asset_tasks.__name__ + ': import_asset_tasks list must not be empty')

## Checks if there is some objects in import result
def are_import_tasks_succeed(import_asset_tasks, import_fail_help_info = 'did not imported file'):
    if general.is_not_none_or_empty(import_asset_tasks):
        failed_tasks = []
        for import_asset_task in import_asset_tasks:
            destination_dir = import_asset_task.get_editor_property('destination_path')
            imported_assets_data = get_asset.get_material_texture_mesh_data_by_dir(destination_dir, is_recursive_search = True)
            if not general.is_not_none_or_empty(imported_assets_data):
                failed_tasks.append(import_asset_task)
            #if not unreal.EditorAssetLibrary.does_directory_have_assets(destination_dir, recursive = True):
                #failed_tasks.append(import_asset_task)

        len_failed_tasks = len(failed_tasks)
        if len_failed_tasks == 0:
            return True
        else:
            unreal.log_error(are_import_tasks_succeed.__name__ + '(): ' + import_fail_help_info)
            unreal.log_error('Failed Import Tasks count: ' + str(len_failed_tasks))
            unreal.log_error('Failed Import Tasks destination_paths:')
            for fail_task in failed_tasks:
                unreal.log_error(fail_task.get_editor_property('destination_path'))
            return False

    else:
        unreal.log_error(are_import_tasks_succeed.__name__ + '(): import_asset_tasks must not be None or Empty')
        return False

## Options: unreal.FbxSceneImportOptionsStaticMesh | unreal.DatasmithStaticMeshImportOptions | unreal.FbxSceneImportOptionsSkeletalMesh
def make_import_asset_tasks(import_asset_tasks, asset_tools = None, import_fail_help_info = '(): did not imported file'):
    if asset_tools is None:
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks(import_asset_tasks)
    return are_import_tasks_succeed(import_asset_tasks, import_fail_help_info)

def make_import_asset_task(import_asset_task, asset_tools = None, import_fail_help_info = '(): did not imported file'):
    return make_import_asset_tasks([import_asset_task], asset_tools, import_fail_help_info)


## Default variant of importing fbx file
def import_fbx_default(fbx_path, destination_dir, fbx_import_options = None,
                       automated = False, save = False, replace_existing = False):
    if fbx_path != '' and destination_dir != '':
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        fbx_import_options = None   # unreal.FbxSceneImportOptionsStaticMesh | unreal.DatasmithStaticMeshImportOptions | unreal.FbxSceneImportOptionsSkeletalMesh
        fbx_asset_task = new_asset_import_task(fbx_path, destination_dir, automated = automated,
                                                save = save, replace_existing = replace_existing,
                                               options = fbx_import_options)
        if not make_import_asset_task(fbx_asset_task, asset_tools, 'No assets are imported to fbx full scene'):
            return
    else:
        unreal.log_error(import_fbx_default.__name__ + ': fbx_path, destination_dir must not be Empty')

def import_fbx_with_gltf_materials(fbx_path, destination_dir, glb_materials_dir_path, is_automated = False):
    if fbx_path != '' and destination_dir != '' and glb_materials_dir_path != '':
        import_fbx_default(fbx_path, glb_materials_dir_path, automated = is_automated)

        fbx_assets = get_asset.get_static_skeletal_meshes_data_by_dir(glb_materials_dir_path)
        if general.is_not_none_or_empty(fbx_assets):
            asset_library.move_assets(fbx_assets, destination_dir)
        else:
            unreal.log_error(import_fbx_with_gltf_materials.__name__ + ': No assets are imported by fbx file')
    else:
        unreal.log_error(import_fbx_with_gltf_materials.__name__ + ': fbx_path, destination_dir, glb_materials_dir_path must not be Empty')

def import_fbx_subobjects_with_gltf_materials(subobjects_path, destination_dir, glb_materials_dir_path, is_automated = False):
    if subobjects_path != '' and destination_dir != '' and glb_materials_dir_path != '':
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        fbx_subobjects_import_options = None
        fbx_subobjects_asset_task = new_asset_import_task(subobjects_path, glb_materials_dir_path, automated = is_automated,
                                                            save = False, replace_existing = False,
                                                            options = fbx_subobjects_import_options)
        if not make_import_asset_task(fbx_subobjects_asset_task, asset_tools, 'No assets are imported to subobjects'):
            return

        fbx_subobjects_assets = get_asset.get_static_skeletal_meshes_data_by_dir(glb_materials_dir_path)
        if general.is_not_none_or_empty(fbx_subobjects_assets):
            subobjects_dir_path = unreal.Paths.combine([destination_dir, 'Subobjects'])
            unreal.EditorAssetLibrary.make_directory(subobjects_dir_path)
            asset_library.move_assets(fbx_subobjects_assets, subobjects_dir_path)
        else:
            unreal.log_error(import_fbx_subobjects_with_gltf_materials.__name__ + ': No subobjects assets are imported by fbx file')
    else:
        unreal.log_error(import_fbx_subobjects_with_gltf_materials.__name__ + ': subobjects_path, destination_dir, glb_materials_dir_path must not be Empty')

## @materials_dir_path directory, to which fbx files will be first import. Ditectory with proper materials(imported from glb)
def import_fbx_scene_n_subobjects(fbx_path, destination_dir, subobjects_path, glb_materials_dir_path, is_automated = False):
    import_fbx_with_gltf_materials(fbx_path, destination_dir, glb_materials_dir_path, False)
    import_fbx_subobjects_with_gltf_materials(subobjects_path, destination_dir, glb_materials_dir_path, True)


## Import asset mesh, animation from fbx file. Import materials settings and textures from gltf file. Only one path, not loop.
# @param is_loop indicates if import_one_asset_pipeline was called by import_assets_pipeline. Needs for transactions.
# @param subobjects_paths if 3d model consists subobjects, import them separately.
# Plugins must be on: 'Datasmith glTF Importer', 'glTF Importer'
# Window Two Options, when import: Generate Lightmap UVs, Import uniform Scale
def import_one_asset_pipeline_datasmith(fbx_path, glb_path, destination_dir, subobjects_path = '',
                                        include_only_on_disk_assets = False):
    if general.is_not_none_or_empty_lists([fbx_path, glb_path, destination_dir]):
        with unreal.ScopedEditorTransaction(import_one_asset_pipeline_datasmith.__name__ + '()') as ue_transaction:
            textures_dir_name = 'Textures'
            materials_dir_name = 'Materials'
            if not unreal.EditorAssetLibrary.does_directory_exist(destination_dir):
                unreal.EditorAssetLibrary.make_directory(destination_dir)

            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            glb_import_options = new_gltf_options()  # unreal.DatasmithGLTFImportOptions | unreal.GLTFImportOptions
            gltf_import_factory = unreal.GLTFImportFactory()
            glb_asset_task = new_asset_import_task(glb_path, destination_dir, automated = True, factory = gltf_import_factory,
                                                   save = False, replace_existing = False, options = glb_import_options)
            if not make_import_asset_task(glb_asset_task, asset_tools, 'did not imported glb file'):
                return
            glb_destination_dir_path = unreal.Paths.combine([destination_dir, unreal.Paths.get_base_filename(glb_path)])

            textures_dest_dir_path = unreal.Paths.combine([destination_dir, textures_dir_name])
            glb_textures_dir_path = unreal.Paths.combine([glb_destination_dir_path, textures_dir_name])
            unreal.EditorAssetLibrary.make_directory(textures_dest_dir_path)
            asset_library.move_assets_in_dir(glb_textures_dir_path, textures_dest_dir_path)
            prefix_suffix.delete_glb_texture_prefix_in_dir(textures_dest_dir_path)

            materials_dest_dir_path = unreal.Paths.combine([destination_dir, materials_dir_name])
            glb_materials_dir_path = unreal.Paths.combine([glb_destination_dir_path, materials_dir_name])
            unreal.EditorAssetLibrary.make_directory(materials_dest_dir_path)
            asset_library.move_assets_in_dir(glb_materials_dir_path, materials_dest_dir_path)
            set_material.replace_parameters_space_to_underscore_in_dir(materials_dest_dir_path)

            unreal.EditorAssetLibrary.delete_directory(glb_destination_dir_path)
            import_fbx_scene_n_subobjects(fbx_path, destination_dir, subobjects_path, materials_dest_dir_path)


## Import asset mesh, animation from fbx file. Import materials settings and textures from gltf file. Loop call to import assets.
# @param subobjects_paths if 3d model consists subobjects, import them separately.
# Plugins must be on: 'Datasmith glTF Importer', 'glTF Importer'
# Window Two Options, when import: Generate Lightmap UVs, Import uniform Scale
def import_assets_pipeline_datasmith(fbx_paths, glb_paths, destination_dirs, subobjects_paths = [],
                                     include_only_on_disk_assets = False):
    unreal.log(import_assets_pipeline_datasmith.__name__ + '() has Started')
    if general.are_lists_equal_length([fbx_paths, glb_paths, subobjects_paths, destination_dirs], True):
        for i in range(len(destination_dirs)):
            import_one_asset_pipeline_datasmith(fbx_paths[i], glb_paths[i], destination_dirs[i],
                                                subobjects_paths[i], include_only_on_disk_assets)

    unreal.log(import_assets_pipeline_datasmith.__name__ + '() has Finished'); unreal.log('...')


## Import asset mesh, animation from fbx file. Import materials settings and textures from gltf file. Only one path, not loop.
# @param is_loop indicates if import_one_asset_pipeline was called by import_assets_pipeline. Needs for transactions.
# @param subobjects_paths if 3d model consists subobjects, import them separately.
# Plugins must be off: 'Datasmith glTF Importer', 'glTF Importer'
# Window 4 Options, when import: Merge Meshes, Apply World Transform, Import Materials, Import in New Folder
def import_one_asset_pipeline(fbx_path, gltf_path, destination_dir, subobjects_path = '',
                              include_only_on_disk_assets = False, to_replace_texture_samples = False):
    if general.is_not_none_or_empty_lists([fbx_path, gltf_path, destination_dir]):
        with unreal.ScopedEditorTransaction(import_one_asset_pipeline.__name__ + '()') as ue_transaction:
            if not unreal.EditorAssetLibrary.does_directory_exist(destination_dir):
                unreal.EditorAssetLibrary.make_directory(destination_dir)
            gltf_destination_dir_path = unreal.Paths.combine([destination_dir, 'glTF'])
            if not unreal.EditorAssetLibrary.does_directory_exist(gltf_destination_dir_path):
                unreal.EditorAssetLibrary.make_directory(gltf_destination_dir_path)     # Make temp directory for deleting trash assets

            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            gltf_import_options = None  # unreal.DatasmithGLTFImportOptions | unreal.GLTFImportOptions
            gltf_asset_task = new_asset_import_task(gltf_path, gltf_destination_dir_path, automated = False,
                                                    save = False, replace_existing = False, options = gltf_import_options)
            #asset_tools.import_asset_tasks([gltf_asset_task])
            if not make_import_asset_task(gltf_asset_task, asset_tools, 'did not imported gtf file'):
                return

            textures_data = get_asset.get_textures_data_by_dir(gltf_destination_dir_path)
            textures_dir_path = unreal.Paths.combine([destination_dir, 'Textures'])
            unreal.EditorAssetLibrary.make_directory(textures_dir_path)
            asset_library.move_assets(textures_data, textures_dir_path)

            materials_data = get_asset.get_materials_data_by_dir(gltf_destination_dir_path)
            materials_dir_path = unreal.Paths.combine([destination_dir, 'Materials'])
            unreal.EditorAssetLibrary.make_directory(materials_dir_path)
            asset_library.move_assets(materials_data, materials_dir_path)
            materials_data = get_asset.get_materials_data_by_dir(materials_dir_path, is_recursive_search = True)    # Update actual data
            material_library.auto_align_materials_node_data(materials_data)
            if to_replace_texture_samples:
                material_library.replace_texture_sample_to_parameters_by_datas(materials_data)

            unreal.EditorAssetLibrary.delete_directory(gltf_destination_dir_path)
            import_fbx_scene_n_subobjects(fbx_path, destination_dir, subobjects_path, materials_dir_path)

## Import asset mesh, animation from fbx file. Import materials settings and textures from gltf file. Loop call to import assets.
# @param subobjects_paths if 3d model consists subobjects, import them separately.
# Plugins must be off: 'Datasmith glTF Importer', 'glTF Importer'
# Window 4 Options, when import: Merge Meshes, Apply World Transform, Import Materials, Import in New Folder
def import_assets_pipeline(fbx_paths, gltf_paths, destination_dirs, subobjects_paths = [],
                           include_only_on_disk_assets = False, to_replace_texture_samples = False):
    unreal.log(import_assets_pipeline.__name__ + '() has Started')
    if general.are_lists_equal_length([fbx_paths, gltf_paths, subobjects_paths, destination_dirs], True):
        for i in range(len(destination_dirs)):
            import_one_asset_pipeline(fbx_paths[i], gltf_paths[i], destination_dirs[i],
                                      subobjects_paths[i], include_only_on_disk_assets, to_replace_texture_samples)

    unreal.log(import_assets_pipeline.__name__ + '() has Finished'); unreal.log('...')


## Window Options 10: like in import_one_asset_pipeline_datasmith + Geometry, Materials & Textures, Lights, Cameras...
def import_asset_pipeline_datasmith_factory(fbx_path, glb_path, destination_dir, subobjects_path = '',
                                             include_only_on_disk_assets = False):
    if general.is_not_none_or_empty_lists([fbx_path, glb_path, destination_dir]):
        with unreal.ScopedEditorTransaction(import_asset_pipeline_datasmith_factory.__name__ + '()') as ue_transaction:
            textures_dir_name = 'Textures'
            materials_dir_name = 'Materials'
            materials_subdir_name = 'Master'
            if not unreal.EditorAssetLibrary.does_directory_exist(destination_dir):
                unreal.EditorAssetLibrary.make_directory(destination_dir)

            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            glb_import_options = new_gltf_options()
            datasmith_import_factory = unreal.DatasmithImportFactory()
            glb_asset_task = new_asset_import_task(glb_path, destination_dir, automated = False, factory = datasmith_import_factory,
                                                   save = False, replace_existing = False, options = glb_import_options)
            if not make_import_asset_task(glb_asset_task, asset_tools, 'did not imported glb file'):
                return
            glb_destination_dir_path = unreal.Paths.combine([destination_dir, unreal.Paths.get_base_filename(glb_path)])

            textures_dest_dir_path = unreal.Paths.combine([destination_dir, textures_dir_name])
            glb_textures_dir_path = unreal.Paths.combine([glb_destination_dir_path, textures_dir_name])
            unreal.EditorAssetLibrary.make_directory(textures_dest_dir_path)
            asset_library.move_assets_in_dir(glb_textures_dir_path, textures_dest_dir_path)
            prefix_suffix.delete_glb_texture_prefix_in_dir(textures_dest_dir_path)

            materials_dest_dir_path = unreal.Paths.combine([destination_dir, materials_dir_name])
            glb_materials_dir_path = unreal.Paths.combine([glb_destination_dir_path, materials_dir_name])
            glb_materials_subdir_path = unreal.Paths.combine([glb_materials_dir_path, materials_subdir_name])
            set_material.delete_nodes_trash_suffix_in_dir(glb_materials_subdir_path)
            unreal.EditorAssetLibrary.make_directory(materials_dest_dir_path)
            asset_library.move_assets_in_dir(glb_materials_dir_path, materials_dest_dir_path,
                                             is_recursive = True, include_only_on_disk_assets = False, is_save_dir_structure = True)

            unreal.EditorAssetLibrary.delete_directory(glb_destination_dir_path)
            import_fbx_scene_n_subobjects(fbx_path, destination_dir, subobjects_path, materials_dest_dir_path)

            # Delete M_ prefix before material instances. Add MI_ prefix
            materials_instances_data = get_asset.get_assets_by_dir(materials_dest_dir_path, is_recursive = False)
            prefix_suffix.delete_prefix_suffix_datas(materials_instances_data, 'M_')
            prefix_suffix.correct_prefix_suffix_dirs([materials_dest_dir_path])


## Window Options 10: like in import_one_asset_pipeline_datasmith + Geometry, Materials & Textures, Lights, Cameras...
def import_assets_pipeline_datasmith_factory(fbx_paths, glb_paths, destination_dirs, subobjects_paths = '',
                                             include_only_on_disk_assets = False):
    if general.is_not_none_or_empty_lists([fbx_paths, glb_paths, destination_dirs, subobjects_paths]):
        if general.are_lists_equal_length([fbx_paths, glb_paths, destination_dirs, subobjects_paths]):
            i = 0
            while i < len(fbx_paths):
                import_asset_pipeline_datasmith_factory(fbx_paths[i], glb_paths[i], destination_dirs[i], subobjects_paths[i],
                                                        include_only_on_disk_assets)
                i += 1

        else:
            unreal.log_error(import_assets_pipeline_datasmith_factory.__name__ + '(): fbx_paths, glb_paths, destination_dirs, subobjects_paths must be equal length')
    else:
        unreal.log_error(import_assets_pipeline_datasmith_factory.__name__ + '(): fbx_paths, glb_paths, destination_dirs, subobjects_paths must not be None or Empty')



def import_asset_pipeline_hybrid(fbx_path, glb_path, destination_dir, subobjects_path = '',
                                 is_automated = False, to_recompile = True, to_import_fbx_material_instance_file = False):
    if general.is_not_none_or_empty_lists([fbx_path, glb_path, destination_dir]):
        with unreal.ScopedEditorTransaction(import_asset_pipeline_datasmith_factory.__name__ + '()') as ue_transaction:
            textures_dir_name = 'Textures'
            materials_dir_name = 'Materials'
            material_instances_dir_name = 'MInstances'
            materials_subdir_name = 'Master'
            temp_dir_name = 'temp'
            if not unreal.EditorAssetLibrary.does_directory_exist(destination_dir):
                unreal.EditorAssetLibrary.make_directory(destination_dir)
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

            # Import Material Instances
            # DatasmithImportFactory and GLTFImportFactory import occlusion_metal_roughness texture incorrect (in gray color, not in purple/yellow)
            # Use for import of textures standard import, not factory
            datasmith_import_factory = unreal.DatasmithImportFactory()
            glb_import_options = new_gltf_options()
            glb_asset_task = new_asset_import_task(glb_path, destination_dir, automated = False, factory = datasmith_import_factory,
                                                   save = False, replace_existing = False, options = glb_import_options)
            if not make_import_asset_task(glb_asset_task, asset_tools, 'did not imported glb file'):
                return

            # Generate Paths
            glb_file_name = unreal.Paths.get_base_filename(glb_path)
            glb_destination_dir_path = unreal.Paths.combine([destination_dir, glb_file_name])
            glb_textures_dir_path = unreal.Paths.combine([glb_destination_dir_path, textures_dir_name])
            glb_materials_dir_path = unreal.Paths.combine([glb_destination_dir_path, materials_dir_name])
            glb_materials_subdir_path = unreal.Paths.combine([glb_materials_dir_path, materials_subdir_name])
            if not unreal.EditorAssetLibrary.does_directory_exist(glb_materials_subdir_path):
                unreal.EditorAssetLibrary.make_directory(glb_materials_subdir_path)

            # Import Materials & Textures
            temp_dir_path = unreal.Paths.combine([glb_destination_dir_path, temp_dir_name])
            unreal.EditorAssetLibrary.make_directory(temp_dir_path)
            gltf_import_factory = unreal.GLTFImportFactory()
            glb_asset_task = new_asset_import_task(glb_path, temp_dir_path, automated = True, factory = gltf_import_factory,
                                                   save = True, replace_existing = False, options = glb_import_options)
            if not make_import_asset_task(glb_asset_task, asset_tools, 'did not imported glb file'):
                return

            # Create Materials dir From Temp to Glb Folder
            temp_glb_materials_dir_path = unreal.Paths.combine([temp_dir_path, glb_file_name, materials_dir_name])
            # Materials in glb_materials_subdir_path will be replaced by redirectors
            set_asset.consolidate_assets_by_dir(temp_glb_materials_dir_path, glb_materials_subdir_path)
            set_asset.delete_all_in_dir(glb_materials_subdir_path)
            # Can Freeze, because of material compilation. F.e. transparent material
            asset_library.move_assets_in_dir(temp_glb_materials_dir_path, glb_materials_subdir_path)

            # Create Textures dir From Temp to Glb Folder
            textures_dest_dir_path = unreal.Paths.combine([destination_dir, textures_dir_name])
            temp_glb_textures_dir_path = unreal.Paths.combine([temp_dir_path, glb_file_name, textures_dir_name])
            unreal.EditorAssetLibrary.make_directory(textures_dest_dir_path)
            asset_library.move_assets_in_dir(temp_glb_textures_dir_path, textures_dest_dir_path)
            prefix_suffix.delete_glb_texture_prefix_in_dir(textures_dest_dir_path)

            # Move Materials & Material Instances From Glb Folder To Destination
            materials_dest_dir_path = unreal.Paths.combine([destination_dir, materials_dir_name])
            material_instances_dest_dir_path = unreal.Paths.combine([destination_dir, material_instances_dir_name])
            unreal.EditorAssetLibrary.make_directory(materials_dest_dir_path)
            # Move Material Instances
            asset_library.move_assets_in_dir(glb_materials_dir_path, material_instances_dest_dir_path,
                                             is_recursive = False, include_only_on_disk_assets = False, is_save_dir_structure = False)
            # Move Materials
            asset_library.move_assets_in_dir(glb_materials_subdir_path, materials_dest_dir_path,
                                             is_recursive = False, include_only_on_disk_assets = False, is_save_dir_structure = False)

            # Correct Materials
            #set_material.delete_nodes_trash_suffix_in_dir(glb_materials_subdir_path)
            set_material.replace_parameters_space_to_underscore_in_dir(materials_dest_dir_path)
            set_material.correct_normal_map_map_in_dir(materials_dest_dir_path)
            if to_recompile:
                set_material.recompile_material_in_dir(materials_dest_dir_path)

            # Import FBX Ojbects
            unreal.EditorAssetLibrary.delete_directory(glb_destination_dir_path)
            import_fbx_scene_n_subobjects(fbx_path, destination_dir, subobjects_path, materials_dest_dir_path, is_automated = True)
            # Import fbx file consolidated with material instances
            if to_import_fbx_material_instance_file:
                import_fbx_default(fbx_path, material_instances_dest_dir_path, automated = True)

            # Delete M_ prefix before material instances. Add MI_ prefix
            materials_instances_data = get_asset.get_assets_by_dir(material_instances_dest_dir_path, is_recursive = False)
            prefix_suffix.delete_prefix_suffix_datas(materials_instances_data, 'M_')
            prefix_suffix.correct_prefix_suffix_dirs([material_instances_dest_dir_path])


## Window Options 10: like in import_one_asset_pipeline_datasmith + Geometry, Materials & Textures, Lights, Cameras...
def import_assets_pipeline_hybrid(fbx_paths, glb_paths, destination_dirs, subobjects_paths = '',
                                  is_automated = False, to_recompile = True, to_import_fbx_material_instance_file = False):
    if general.is_not_none_or_empty_lists([fbx_paths, glb_paths, destination_dirs, subobjects_paths]):
        if general.are_lists_equal_length([fbx_paths, glb_paths, destination_dirs, subobjects_paths]):
            with unreal.ScopedEditorTransaction(import_assets_pipeline_hybrid.__name__ + '()') as ue_transaction:
                i = 0
                while i < len(fbx_paths):
                    import_asset_pipeline_hybrid(fbx_paths[i], glb_paths[i], destination_dirs[i], subobjects_paths[i],
                                                 is_automated, to_recompile, to_import_fbx_material_instance_file)
                    i += 1

        else:
            unreal.log_error(import_assets_pipeline_hybrid.__name__ + '(): fbx_paths, glb_paths, destination_dirs, subobjects_paths must be equal length')
    else:
        unreal.log_error(import_assets_pipeline_hybrid.__name__ + '(): fbx_paths, glb_paths, destination_dirs, subobjects_paths must not be None or Empty')


# TODO:
def import_assets_pipeline_code4game(fbx_paths, gltf_paths, DESTINATION_DIRS, subobjects_paths, ONLY_ON_DISK_ASSETS):
    a = 0


def prepare_paths_gltf(import_dirs, fbx_file_names, gltf_file_names, subobjects_dir_name, subobjects_names):
    if general.is_not_none_or_empty_lists([import_dirs, fbx_file_names, gltf_file_names, subobjects_names]):
        if general.are_lists_equal_length([import_dirs, fbx_file_names, gltf_file_names, subobjects_names]):
            fbx_paths, gltf_paths, subobjects_paths = [], [], []
            i = 0
            while i < len(import_dirs):
                fbx_paths.append(unreal.Paths.combine([import_dirs[i], fbx_file_names[i]]))
                fbx_paths[i] = unreal.Paths.set_extension(fbx_paths[i], 'fbx')

                gltf_paths.append(unreal.Paths.combine([import_dirs[i], gltf_file_names[i]]))
                gltf_paths[i] = unreal.Paths.set_extension(gltf_paths[i], 'gltf')

                if subobjects_names[i] != '':
                    subobjects_paths.append(unreal.Paths.combine([import_dirs[i], subobjects_dir_name, subobjects_names[i]]))
                    subobjects_paths[i] = unreal.Paths.set_extension(subobjects_paths[i], 'fbx')
                else:
                    subobjects_paths.append('')
                i += 1

            return fbx_paths, gltf_paths, subobjects_paths
        else:
            unreal.log_error(prepare_paths_gltf.__name__ + '(): import_dirs, fbx_file_names, gltf_file_names, subobjects_names must be equal length')
    else:
        unreal.log_error(prepare_paths_gltf.__name__ + '(): import_dirs, fbx_file_names, gltf_file_names, subobjects_names must not be None or Empty')

def prepare_paths_datasmith(import_dirs, fbx_file_names, glb_file_names, subobjects_dir_name, subobjects_names):
    if general.is_not_none_or_empty_lists([import_dirs, fbx_file_names, glb_file_names, subobjects_names]):
        if general.are_lists_equal_length([import_dirs, fbx_file_names, glb_file_names, subobjects_names]):
            fbx_paths, glb_paths, subobjects_paths = [], [], []
            i = 0
            while i < len(import_dirs):
                fbx_paths.append(unreal.Paths.combine([import_dirs[i], fbx_file_names[i]]))
                fbx_paths[i] = unreal.Paths.set_extension(fbx_paths[i], 'fbx')

                glb_paths.append(unreal.Paths.combine([import_dirs[i], glb_file_names[i]]))
                glb_paths[i] = unreal.Paths.set_extension(glb_paths[i], 'glb')

                if subobjects_names[i] != '':
                    subobjects_paths.append(unreal.Paths.combine([import_dirs[i], subobjects_dir_name, subobjects_names[i]]))
                    subobjects_paths[i] = unreal.Paths.set_extension(subobjects_paths[i], 'fbx')
                else:
                    subobjects_paths.append('')
                i += 1

            return fbx_paths, glb_paths, subobjects_paths
        else:
            unreal.log_error(prepare_paths_datasmith.__name__ + '(): import_dirs, fbx_file_names, glb_paths, subobjects_names must be equal length')
    else:
        unreal.log_error(prepare_paths_datasmith.__name__ + '(): import_dirs, fbx_file_names, glb_paths, subobjects_names must not be None or Empty')
