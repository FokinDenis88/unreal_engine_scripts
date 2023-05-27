import unreal

import unreal_scripts.config as config
import unreal_scripts.service.general as general
import unreal_scripts.src.get_asset as get_asset
import unreal_scripts.asset.material_node as material_node
import unreal_scripts.src.get_material as get_material
import unreal_scripts.src.set_material as set_material
import unreal_scripts.src.prefix_suffix as prefix_suffix

import importlib
importlib.reload(config)
importlib.reload(general)
importlib.reload(get_asset)
importlib.reload(material_node)
importlib.reload(get_material)
importlib.reload(set_material)
importlib.reload(prefix_suffix)

## @param bump_texture_link_version there are two versions of linking bump texture to material output
bump_texture_link_version = 1

# There are 3 input parameter nodes types: Scalar, Vector, Texture, StaticSwitch


## Change coordinate of nodes to exclude nodes collision
# Auto align only works for nodes, that have been connected to material output property
def auto_align_material_nodes(material, has_log = True):
    if material is not None:
        # Would not be saved in transaction history
        with unreal.ScopedEditorTransaction(auto_align_material_nodes.__name__ + '()') as ue_transaction:
            if has_log:
                unreal.log(auto_align_material_nodes.__name__ + '() Started: ' + material.get_path_name())
            unreal.MaterialEditingLibrary.layout_material_expressions(material)
    else:
        unreal.log_error(auto_align_material_nodes.__name__ + ': material must not be None')

def auto_align_material_node_data(material_asset_data):
    if material_asset_data is not None:
        auto_align_material_nodes(material_asset_data.get_asset())
    else:
        unreal.log_error(auto_align_material_node_data.__name__ + ': material_asset_data must not be None')
## @param materials_asset_data list of asset data
def auto_align_materials_node_data(materials_asset_data):
    if general.is_not_none_or_empty(materials_asset_data):
        for material_asset_data in materials_asset_data:
            auto_align_material_nodes(material_asset_data.get_asset())
    else:
        unreal.log_error(auto_align_materials_node_data.__name__ + ': materials_asset_data must not be None')
def auto_align_material_nodes_path(object_path):
    if general.is_not_none_or_empty(object_path):
        material = get_asset.get_asset_by_object_path(object_path)
        auto_align_material_nodes(material)
    else:
        unreal.log_error(auto_align_material_nodes_path.__name__ + ': object_path must not be None or empty')
def auto_align_materials_nodes_paths(objects_paths):
    if general.is_not_none_or_empty(objects_paths):
        for object_path in objects_paths:
            material = get_asset.get_asset_by_object_path(object_path)
            auto_align_material_nodes(material)
    else:
        unreal.log_error(auto_align_materials_nodes_paths.__name__ + ': objects_paths must not be None or empty')


## Replaces all TextureSamples with TextureSamplesParameter2D
def replace_texture_sample_to_parameters_in_materials(materials, to_delete_old_node = True):
    if general.is_not_none_or_empty(materials):
        with unreal.ScopedEditorTransaction(replace_texture_sample_to_parameters_in_materials.__name__ + '()') as ue_transaction:
            nodes_types = [unreal.MaterialExpressionTextureSample]
            for material in materials:
                texture_sample_nodes = get_material.find_nodes_in_material(material, nodes_types, is_nodes_types_subclasses = False)
                unreal.log(replace_texture_sample_to_parameters_in_materials.__name__ + '(): List of Texture Sample Nodes to be replaced:')
                unreal.log(texture_sample_nodes)
                if general.is_not_none_or_empty(texture_sample_nodes):
                    for node in texture_sample_nodes:
                        new_node = set_material.new_node_TextureSampleParameter2D_node(material, node)
                        set_material.set_texture_parameter_name(new_node)
                        set_material.from_TextureSample_to_TextureParameter2D(node, new_node)

                        set_material.transfer_connections(material, node, new_node)
                        if to_delete_old_node:
                            unreal.MaterialEditingLibrary.delete_material_expression(material, node)
                    auto_align_material_nodes(material)
                else:
                    material_path = get_asset.get_path_from_object(material)
                    unreal.log(replace_texture_sample_to_parameters_in_materials.__name__ +
                               ': did not find any texture sample node in material: ' + material_path)
    else:
        unreal.log_error(replace_texture_sample_to_parameters_in_materials.__name__ + ': materials must not be None or empty')

## Replaces all TextureSamples with TextureSamplesParameter2D
def replace_texture_sample_to_parameters_in_material(material):
    replace_texture_sample_to_parameters_in_materials([material])
def replace_texture_sample_to_parameters_by_data_list(materials_data):
    if materials_data is not None:
        for material_data in materials_data:
            replace_texture_sample_to_parameters_in_material(material_data.get_asset())
    else:
        unreal.log_error(replace_texture_sample_to_parameters_by_data_list.__name__ + ': materials_data must not be None')

def replace_texture_sample_to_parameters_by_paths(materials_paths):
    materials = []
    for material_path in materials_paths:
        materials.append(get_asset.load_asset(material_path))
    replace_texture_sample_to_parameters_in_materials(materials)

def replace_texture_sample_to_parameters_by_path(material_path):
    replace_texture_sample_to_parameters_by_paths([material_path])
def replace_texture_sample_to_parameters_by_datas(materials_data):
    if general.is_not_none_or_empty(materials_data):
        materials = []
        for material_data in materials_data:
            materials.append(material_data.get_asset())
        replace_texture_sample_to_parameters_in_materials(materials)
    else:
        unreal.log_error(replace_texture_sample_to_parameters_by_datas.__name__ + ': materials_data must not be None')

def replace_texture_sample_to_parameters_by_dirs(material_dirs, is_recursive_search = False, only_on_disk_assets = False):
    materials_data = get_asset.get_materials_data_by_dirs(material_dirs, is_recursive_search, only_on_disk_assets)
    for material_data in materials_data:
        path = get_asset.get_asset_data_object_path(material_data)
        replace_texture_sample_to_parameters_by_path(path)


## Add default expressions/nodes to empty parts of material
# TODO:
def auto_fill_material():
    with unreal.ScopedEditorTransaction(auto_fill_material.__name__ + '()') as ue_transaction:
        # loop all input nodes, add what is empty
        #get_material_property_input_node
        a = 0


## Generates Group of connected nodes: Texture, Texture_Factor(Scalar_Parameter), Multiply
# @return tuple of node_texture_factor, node_multiply
def generate_texture_factor_multiply(material, texture_node, texture_type, connection_results, texture_node_output = 'RGB'):
    node_texture_factor = set_material.new_node_ScalarParameter_texture_factor(material, texture_type)
    node_multiply = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionMultiply)
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(texture_node, texture_node_output, node_multiply, 'A'))
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(node_texture_factor, '', node_multiply, 'B'))
    return node_texture_factor, node_multiply

## Generates nodes chain for: Metallic, Specular, Roughness
# Chain is connected to output
def generate_texture_factor_chain(material, texture_node, texture_type, connection_results, output_property, texture_node_output = 'RGB'):
    node_texture_factor, node_multiply = generate_texture_factor_multiply(material, texture_node, texture_type,
                                                                          connection_results, texture_node_output)
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_property(node_multiply, '', output_property))

def generate_texture_factor_chain_plugin(material, texture_node, texture_type, connection_results,
                                         output_property, texture_node_output = 'RGB'):
    node_texture_factor, node_multiply = generate_texture_factor_multiply(material, texture_node, texture_type,
                                                                          connection_results, texture_node_output)
    connection_results.append(unreal.PythonMaterialLib.connect_material_property(node_multiply, '', output_property))

## Generates nodes chain for: Metallic, Specular, Roughness
def generate_basecolor_vector_chain(material, texture_node, connection_results, texture_node_output = 'RGB'):
    node_multiply = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionMultiply)
    node_base_color = set_material.new_node_BaseColorVector(material)
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(texture_node, texture_node_output, node_multiply, 'A'))
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(node_base_color, '', node_multiply, 'B'))
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_property(node_multiply, '', unreal.MaterialProperty.MP_BASE_COLOR))

## Generates nodes chain for: Metallic, Specular, Roughness
def generate_gloss_texture_chain(material, texture_node, texture_type, connection_results, texture_node_output = 'RGB'):
    node_one_minus = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionOneMinus)
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(texture_node, texture_node_output, node_one_minus, ''))
    node_multiply = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionMultiply)
    node_texture_factor = set_material.new_node_ScalarParameter_texture_factor(material, texture_type)
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(node_one_minus, '', node_multiply, 'A'))
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(node_texture_factor, '', node_multiply, 'B'))
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_property(node_multiply, '', unreal.MaterialProperty.MP_ROUGHNESS))

## Basecolor map(Base V3) + Concave/Convex map(Blend V3) -> Blend_overlay node -> Basecolor
def generate_convex_concave_chain(material, convex_concave_node, connection_results, texture_node_output = 'RGB'):
    blend_overlay_node = set_material.new_blend_overlay_node(material)
    search_nodes = get_material.find_nodes_in_material(material, nodes_types = [unreal.MaterialExpressionTextureSampleParameter2D],
                                                             properties_values = [('parameter_name', 'BaseColor_Map')])

    if general.is_not_none_or_empty(search_nodes):
        node_basecolor_map = search_nodes[0]
        connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(node_basecolor_map, texture_node_output,
                                                                                             blend_overlay_node, 'Base'))
        connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(convex_concave_node, 'RGB',
                                                                                             blend_overlay_node, 'Blend'))
        connection_results.append(unreal.MaterialEditingLibrary.connect_material_property(blend_overlay_node, 'Result',
                                                                                          unreal.MaterialProperty.MP_BASE_COLOR))
    else:
        unreal.log_error(generate_convex_concave_chain.__name__ +
                         '(): did not find any basecolor texture map for blend_overlay convex/concave texture')

## First variant of realisation of linking bump map or height map
# Simple connection with World Position Offset
def generate_bump_height_chain_v1(material, node_bump_map, texture_type, connection_results):
    node_texture_factor, node_multiply  = generate_texture_factor_multiply(material, node_bump_map, texture_type,
                                                                          connection_results, 'RGB')
    connection_results.append(unreal.PythonMaterialLib.connect_material_property(node_multiply, '', 'MP_WorldPositionOffset'))

## Second variant of realisation of linking bump map or height map
# https://docs.unrealengine.com/4.27/en-US/RenderingAndGraphics/Materials/HowTo/BumpOffset/
def generate_bump_height_chain_v2(material, node_bump_map, texture_type, connection_results, node_output_bump_map = 'R'):
    texture_nodes_for_linking = get_material.find_nodes_in_material_by_types(material, config.TEXTURE_NODES_TYPES)
    if texture_nodes_for_linking.count(node_bump_map) > 0:
        texture_node_index = texture_nodes_for_linking.index(node_bump_map)
        texture_nodes_for_linking.pop(texture_node_index)

    # bump_map would not be connected to displacement map, because of errors
    i = 0
    while i < len(texture_nodes_for_linking):
        texture_type = get_material.get_texture_type_by_prefix_suffix_node(texture_nodes_for_linking[i])
        if texture_type is 'Displacement':
            texture_nodes_for_linking.pop(i)
        i += 1

    node_bump_offset = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionBumpOffset)
    connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(node_bump_map, node_output_bump_map,
                                                                                             node_bump_offset, 'Height'))
    for node in texture_nodes_for_linking:
        connection_results.append(unreal.MaterialEditingLibrary.connect_material_expressions(node_bump_offset, '', node, 'UVs'))

def generate_texture_displacement_chain(material, texture_node, texture_type, connection_results):
    # World Displacement + Tesseletion Multiplier; Tesselation = Turn On
    # MTM_FLAT_TESSELLATION     MTM_PN_TRIANGLES
    material.set_editor_property('d3d11_tessellation_mode', unreal.MaterialTessellationMode.MTM_PN_TRIANGLES)
    generate_texture_factor_chain_plugin(material, texture_node, texture_type, connection_results,
                                            'MP_WorldDisplacement', texture_node_output = 'RGB')
    node_tessellation_multiplier = set_material.new_node_ScalarParameter_texture_factor(material, 'TessellationMultiplier')
    connection_results.append(unreal.PythonMaterialLib.connect_material_property(node_tessellation_multiplier, '', 'MP_TessellationMultiplier'))

## Generate nodes, needed for texture type, and link them to material output
# @param material is material Object. Is needed to change material properties like translucent
def generate_support_nodes_n_link(material, texture_node, texture_type):
    if material is not None and texture_node is not None and general.is_not_none_or_empty(texture_type):
        connection_results = []
        # Simple
        if texture_type == 'BaseColor' or texture_type == 'Albedo':
            generate_basecolor_vector_chain(material, texture_node, connection_results)
        elif texture_type == 'Metallic':
            generate_texture_factor_chain(material, texture_node, texture_type, connection_results, unreal.MaterialProperty.MP_METALLIC)
        elif texture_type == 'Specular':
            generate_texture_factor_chain(material, texture_node, texture_type, connection_results, unreal.MaterialProperty.MP_SPECULAR)
        elif texture_type == 'Roughness':
            generate_texture_factor_chain(material, texture_node, texture_type, connection_results, unreal.MaterialProperty.MP_ROUGHNESS)
        elif texture_type == 'Gloss':
            generate_gloss_texture_chain(material, texture_node, texture_type, connection_results)
        elif texture_type == 'Normal':
            generate_texture_factor_chain(material, texture_node, texture_type, connection_results, unreal.MaterialProperty.MP_NORMAL)
        elif texture_type == 'Height':
            # There are two variants. 1) Bump map -> uv of all unput texture. 2) World Position Offset
            generate_bump_height_chain_v1(material, texture_node, texture_type, connection_results)
            # MP_NORMAL
        elif texture_type == 'Bump':
            # There are two variants. 1) Bump map -> uv of all unput texture. 2) World Position Offset
            if bump_texture_link_version == 2:
                generate_bump_height_chain_v2(material, texture_node, texture_type, connection_results)
            else:
                generate_bump_height_chain_v1(material, texture_node, texture_type, connection_results)
            # MP_NORMAL
        elif texture_type == 'Displacement':
            generate_texture_displacement_chain(material, texture_node, texture_type, connection_results)
        elif texture_type == 'Emissive':
            generate_texture_factor_chain(material, texture_node, texture_type, connection_results, unreal.MaterialProperty.MP_EMISSIVE_COLOR)
        elif texture_type == 'AmbientOcclusion':
            generate_texture_factor_chain(material, texture_node, texture_type, connection_results, unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
        elif texture_type == 'Alpha/Opacity':
            generate_texture_factor_chain(material, texture_node, texture_type, connection_results, unreal.MaterialProperty.MP_OPACITY)
            material.set_editor_property('blend_mode', unreal.BlendMode.BLEND_TRANSLUCENT)
        elif texture_type == 'OpacityMask':
            connection_results.append(unreal.MaterialEditingLibrary.connect_material_property(texture_node, '', unreal.MaterialProperty.MP_OPACITY_MASK))
            material.set_editor_property('blend_mode', unreal.BlendMode.BLEND_MASKED)
        elif texture_type == 'Convex/Concave':
            generate_convex_concave_chain(material, texture_node, connection_results)
        elif texture_type == 'LightMap':
            # MP_BASE_COLOR
            a = 0
        elif texture_type == 'FUZZ':
            # MP_BASE_COLOR
            a = 0

        # Complex
        elif texture_type == 'OcclusionRoughnessMetallic':
            generate_texture_factor_chain(material, texture_node, 'Occlusion', connection_results, unreal.MaterialProperty.MP_AMBIENT_OCCLUSION, 'R')
            generate_texture_factor_chain(material, texture_node, 'Roughness', connection_results, unreal.MaterialProperty.MP_ROUGHNESS, 'G')
            generate_texture_factor_chain(material, texture_node, 'Metallic', connection_results, unreal.MaterialProperty.MP_METALLIC, 'B')
        elif texture_type == 'SpecularGlossiness':
            generate_texture_factor_chain(material, texture_node, 'Specular', connection_results, unreal.MaterialProperty.MP_SPECULAR, 'A')
            generate_gloss_texture_chain(material, texture_node, 'Gloss', connection_results, 'RGB')

        # Rare
        elif texture_type == 'FlowMap':
            # MP_BASE_COLOR
            a = 0
        elif texture_type == 'Packed':
            # MP_BASE_COLOR
            a = 0
        elif texture_type == 'TextureCube':
            # MP_BASE_COLOR
            a = 0
        elif texture_type == 'MediaTexture':
            # MP_BASE_COLOR
            a = 0
        elif texture_type == 'RenderTarget':
            # MP_BASE_COLOR
            a = 0
        elif texture_type == 'CubeRenderTarget':
            # MP_BASE_COLOR
            a = 0
        elif texture_type == 'TextureLightProfile':
            # MP_BASE_COLOR
            a = 0

        if general.has_false_value(connection_results):
            unreal.log_error(generate_support_nodes_n_link.__name__ + '(): not all support nodes connection process succeed')
    else:
        unreal.log_error(generate_support_nodes_n_link.__name__ + ': material, texture_node and texture_type must not be None or empty')
''' unreal.MaterialProperty.:
    MP_AMBIENT_OCCLUSION
    MP_ANISOTROPY
    MP_BASE_COLOR
    MP_EMISSIVE_COLOR
    MP_METALLIC
    MP_NORMAL
    MP_OPACITY
    MP_OPACITY_MASK
    MP_REFRACTION
    MP_ROUGHNESS
    MP_SPECULAR
    MP_SUBSURFACE_COLOR
    MP_TANGENT  '''

## Links texture node to result node/material output node. Depends on texture type. May add more support expressions/nodes
# @param textures_types is the type of texture, f.e. Diffuse, Normal, Metallic. View in naming_convention.py
def link_textures_nodes_to_result_node(material, textures_nodes, textures_types = None, to_align = False):
    if general.is_not_none_or_empty(textures_nodes):
        if (textures_types is None) or (textures_types is not None and general.are_lists_equal_length([textures_nodes, textures_types])):
            with unreal.ScopedEditorTransaction(link_textures_nodes_to_result_node.__name__ + '()') as ue_transaction:
                for i in range(len(textures_nodes)):
                    texture_path = get_material.get_texture_node_source_path(textures_nodes[i])
                    texture_type = ''
                    if textures_types is not None:
                        texture_type = textures_types[i]
                    else:
                        texture_type = prefix_suffix.get_texture_type_by_prefix_suffix(texture_path)
                    generate_support_nodes_n_link(material, textures_nodes[i], texture_type)
                if to_align:
                    auto_align_material_nodes(material)

        else:
            unreal.log_error(link_textures_nodes_to_result_node.__name__ + ': textures_nodes and textures_types must have equal length')
    else:
        unreal.log_error(link_textures_nodes_to_result_node.__name__ + ': textures_nodes must not be empty or None')


## Links texture node to result node. Depends on texture type. May add more support expressions/nodes
def link_texture_node_to_result_node(material, texture_node, texture_type = None, to_align = False):
    if texture_type is not None:
        link_textures_nodes_to_result_node(material, [texture_node], [texture_type], to_align)
    else:
        link_textures_nodes_to_result_node(material, [texture_node], None, to_align)


## Connect free unlinked texture_nodes in material with material output
# You can add textures nodes inside material in material editor. Then autolink them all.
def connect_free_texture_nodes_in_materials(materials):
    if general.is_not_none_or_empty(materials):
        with unreal.ScopedEditorTransaction(connect_free_texture_nodes_in_materials.__name__ + '()') as ue_transaction:
            unreal.log(connect_free_texture_nodes_in_materials.__name__ + ' is Started')
            for material in materials:
                free_texture_nodes = get_material.find_unlinked_texture_nodes(material)
                #unreal.log(free_texture_nodes)
                if general.is_not_none_or_empty(free_texture_nodes):
                    link_textures_nodes_to_result_node(material, free_texture_nodes, None, True)
                else:
                    unreal.log(connect_free_texture_nodes_in_materials.__name__ + ': did not find any free nodes in material: ')
                    unreal.log(material)

    else:
        unreal.log_error(connect_free_texture_nodes_in_materials.__name__ + ': materials must not be empty or None')

## Connect free unlinked texture_nodes in material with material output
# You can add texture node inside material in material editor. Then autolink them all. Expression = Node
def connect_free_texture_nodes_in_material(material):
    connect_free_texture_nodes_in_materials([material])

def connect_free_texture_nodes_in_materials_by_paths(materials_paths):
    if general.is_not_none_or_empty(materials_paths):
        materials = []
        for material_path in materials_paths:
            materials.append(get_asset.load_asset(material_path))
        if general.is_not_none_or_empty(materials):
            connect_free_texture_nodes_in_materials(materials)
        else:
            unreal.log_error(connect_free_texture_nodes_in_materials_by_paths.__name__ + ': No materials are loaded')
    else:
        unreal.log_error(connect_free_texture_nodes_in_materials_by_paths.__name__ + ': materials_paths must not be empty or None')
def connect_free_texture_nodes_in_material_by_path(material_path):
    connect_free_texture_nodes_in_materials_by_paths([material_path])
def connect_free_texture_nodes_in_materials_data(materials_data):
    if materials_data is not None:
        for material_data in materials_data:
            connect_free_texture_nodes_in_material(material_data.get_asset())
    else:
        unreal.log_error(connect_free_texture_nodes_in_materials_data.__name__ + ': materials_data must not be empty or None')

def connect_free_texture_nodes_in_materials_by_dirs(dirs_paths):
    if general.is_not_none_or_empty_lists(dirs_paths):
        materials_data = get_asset.get_materials_data_by_dirs(dirs_paths)
        if materials_data is not None:
            with unreal.ScopedEditorTransaction(connect_free_texture_nodes_in_materials_by_dirs.__name__ + '()') as ue_transaction:
                for material_data in materials_data:
                    connect_free_texture_nodes_in_material(material_data.get_asset())

        else:
            unreal.log_error(connect_free_texture_nodes_in_materials_by_dirs.__name__ + '(): did not find any material in dir: ' + dirs_paths)
    else:
        unreal.log_error(connect_free_texture_nodes_in_materials_by_dirs.__name__ + '(): dirs_paths each must not be None or Empty')

def connect_free_texture_nodes_in_materials_by_dir(dir_path):
    connect_free_texture_nodes_in_materials_by_dirs([dir_path])

## Creates expressions/nodes inside material from textures files and links nodes to material output
# Many textures files added to Many materials. Many - Many
def connect_textures_files_to_materials(materials_paths, textures_paths,
                                        to_recompile_material = False, to_align = False,
                                        node_pos_x = 0, node_pos_y = 0):
    if general.is_not_none_or_empty_lists([textures_paths, materials_paths]):
        with unreal.ScopedEditorTransaction(connect_textures_files_to_materials.__name__ + '()') as ue_transaction:
            for material_path in materials_paths:
                material = get_asset.get_asset_by_object_path(material_path)
                for texture_path in textures_paths:
                    texture = get_asset.get_asset_by_object_path(texture_path)
                    texture_type = prefix_suffix.get_texture_type_by_prefix_suffix(texture_path)
                    texture_node_name = get_material.get_texture_parameter_name(texture_type)
                    node_meta_data = material_node.MetaDataTextureSampleParameter2D(parameter_name = texture_node_name,
                                                                                    texture = texture)
                    texture_node = set_material.new_node_TextureSampleParameter2D(material, node_meta_data, node_pos_x, node_pos_y)

                    link_texture_node_to_result_node(material, texture_node, texture_type, to_align)

                if to_recompile_material:
                   unreal.MaterialEditingLibrary.recompile_material(material)

    else:
        unreal.log_error(connect_texture_file_to_materials.__name__ + ': texture_path and materials_paths must not be empty or None')

## Creates expressions/nodes inside material from textures files and links nodes to material output
# Many texture file added to One materials. Many - One
def connect_textures_files_to_material(material_path, textures_paths,
                                       to_recompile_material = False, to_align = False,
                                       node_pos_x = 0, node_pos_y = 0):
    connect_textures_files_to_materials([material_path], textures_paths, to_recompile_material, to_align, node_pos_x, node_pos_y)

## Creates expressions/nodes inside material from textures files and links nodes to material output
# One texture file added to Many materials. One - Many
def connect_texture_file_to_materials(materials_paths, texture_path,
                                      to_recompile_material = False, to_align = False,
                                      node_pos_x = 0, node_pos_y = 0):
    connect_textures_files_to_materials(materials_paths, [texture_path], to_recompile_material, to_align, node_pos_x, node_pos_y)

## Creates expressions/nodes inside material from textures files and links nodes to material output
# One texture file added to One materials. One - One
def connect_texture_file_to_material(material_path, texture_path,
                                     to_recompile_material = False, to_align = False,
                                     node_pos_x = 0, node_pos_y = 0):
    connect_textures_files_to_materials([material_path], [texture_path], to_recompile_material, to_align, node_pos_x, node_pos_y)


## Connects textures lists in texture_pack_paths to material_paths
# @param texture_pack_paths is list of lists of texture paths. [[texture_1, texture_2],[texture_3]]
#        Every texture_path in texture_pack_paths[i] must be connected with material_paths[i]
def connect_texture_files_packs(material_paths, texture_paths_packs,
                                to_recompile_material = False, to_align = False,
                                node_pos_x = 0, node_pos_y = 0):
    if general.is_not_none_or_empty_lists([material_paths, texture_paths_packs]):
        if general.are_lists_equal_length([material_paths, texture_paths_packs]):
            for i in range(len(material_paths)):
                connect_textures_files_to_material(material_paths[i], texture_paths_packs[i],
                                                   to_recompile_material, to_align, node_pos_x, node_pos_y)

        else:
            unreal.log_error(connect_texture_files_packs.__name__ + ': material_paths or texture_paths_packs must equal length')
    else:
        unreal.log_error(connect_texture_files_packs.__name__ + ': material_paths or texture_paths_packs must not be empty')

## Connects all textures from texture_paths_pack with material in material_path
# @param texture_paths_pack is list of texture_path
def connect_texture_files_pack(material_path, texture_paths_pack,
                               to_recompile_material = False, to_align = False,
                               node_pos_x = 0, node_pos_y = 0):
    connect_texture_files_packs([material_path], [texture_paths_pack], to_recompile_material, to_align, node_pos_x, node_pos_y)


## Find same name without prefix suffix in materials and textures
# @return list of lists with textures. materials_data[i] is associated with associated_textures_paths[i]
def associate_textures_with_materials(materials_data, textures_data):
    associated_textures_paths_packs = []
    if general.is_not_none_or_empty_lists([materials_data, textures_data]):
        material_names_no_prefix_suffix = []
        for material_data in materials_data:
            material_names_no_prefix_suffix.append(prefix_suffix.get_asset_name_without_prefix_suffix_data(material_data))
            associated_textures_paths_packs.append([])

        for texture_data in textures_data:
            texture_name = prefix_suffix.get_asset_name_without_prefix_suffix_data(texture_data)
            if material_names_no_prefix_suffix.count(texture_name) > 0:
                material_index = material_names_no_prefix_suffix.index(texture_name)
                associated_textures_paths_packs[material_index].append(get_asset.get_asset_data_object_path(texture_data))

    else:
        unreal.log_error(associate_textures_with_materials.__name__ + ': materials_data or textures_data must not be empty')
    return associated_textures_paths_packs

## Connects textures from textures_dirs inside material in material editor from many directories, packs
# Connects textures with the same file name without prefix-suffix with material
# Connects all unlinked texture nodes inside material
# Using, when importing from many 3d model project
# FIX: Adding Convex_Concave map. Doesnt understand, that connected Convex_Concave map is used by material -> reconnect, duplicate overlay node
# problem in unreal.MaterialEditingLibrary.get_used_textures(material) function
def connect_by_association_texture_file_dirs(materials_dirs, textures_dirs, to_recompile_material = False, to_align = False):
    unreal.log(connect_by_association_texture_file_dirs.__name__ + ' Started')
    if general.is_not_none_or_empty_lists([textures_dirs, materials_dirs]):
        if general.are_lists_equal_length([textures_dirs, materials_dirs]):
            with unreal.ScopedEditorTransaction(connect_by_association_texture_file_dirs.__name__ + '()') as ue_transaction:
                for i in range(len(textures_dirs)):
                    textures_data = get_asset.get_textures_data_by_dir(textures_dirs[i])
                    materials_data = get_asset.get_materials_data_by_dir(materials_dirs[i])
                    if general.is_not_none_or_empty_lists([textures_data, materials_data]):
                        # [[textures], [textures], [textures]] each list is associated with element of materials_data
                        associated_textures_paths_packs = associate_textures_with_materials(materials_data, textures_data)
                        #unreal.log(associated_textures_paths_packs)
                        for i in range(len(materials_data)):
                            material_path = get_asset.get_asset_data_object_path(materials_data[i])
                            unreal.log(connect_by_association_texture_file_dirs.__name__ + '(): Is working with material: ' + material_path)
                            if len(associated_textures_paths_packs[i]) > 0:
                                # Doesn't need to be recompiled
                                connect_textures_files_to_material(material_path, associated_textures_paths_packs[i], False, False, 0, 0)

                            replace_texture_sample_to_parameters_by_data_list([materials_data[i]])

                            # Searching unconnected textures nodes inside materials and link them.
                            # If user manually add textures to material and not link them to output of material
                            if to_recompile_material:
                                # To fix problems with not actual material data
                                unreal.MaterialEditingLibrary.recompile_material(materials_data[i].get_asset())
                            connect_free_texture_nodes_in_materials_data([materials_data[i]])
                            if to_align:
                                auto_align_material_node_data(materials_data[i])
                            if to_recompile_material:
                                unreal.MaterialEditingLibrary.recompile_material(materials_data[i].get_asset())

        else:
            unreal.log_error(connect_by_association_texture_file_dirs.__name__ + ': textures_dirs and materials_dirs lists must be equal length, dimension')
    else:
        unreal.log_error(connect_by_association_texture_file_dirs.__name__ + ': textures_dir and materials_dir must not be empty or None')
    unreal.log(connect_by_association_texture_file_dirs.__name__ + ' Finished')

## Connects textures from textures_dir inside material in material editor from one directory, pack.
# Connects textures with the same file name without prefix-suffix with material
# Connects all unlinked texture nodes inside material
# Using, when importing from one 3d model project
def connect_by_association_texture_file_dir(materials_dir, textures_dir, to_recompile_material = False, to_align = False):
    connect_by_association_texture_file_dirs([materials_dir], [textures_dir], to_recompile_material, to_align)