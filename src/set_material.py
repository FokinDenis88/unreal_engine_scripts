import re
import unreal

import unreal_engine_python_scripts.config as config
import unreal_engine_python_scripts.service.general as general
import unreal_engine_python_scripts.service.log as log
import unreal_engine_python_scripts.src.get_asset as get_asset
import unreal_engine_python_scripts.src.set_asset as set_asset
import unreal_engine_python_scripts.src.get_material as get_material

import importlib
importlib.reload(config)
importlib.reload(general)
importlib.reload(log)
importlib.reload(get_asset)
importlib.reload(set_asset)
importlib.reload(get_material)


## Transfers data From TextureBase To TextureSampleParameter2D
def from_TextureBase_to_TextureParameter2D(texture_base_node, texture_parameter_node):
    texture_parameter_node.set_editor_property('desc', texture_base_node.get_editor_property('desc'))
    texture_parameter_node.set_editor_property('is_default_meshpaint_texture',
                                               texture_base_node.get_editor_property('is_default_meshpaint_texture'))
    texture_parameter_node.set_editor_property('sampler_type', texture_base_node.get_editor_property('sampler_type'))
    texture_parameter_node.set_editor_property('texture', texture_base_node.get_editor_property('texture'))

## Transfers data From TextureSample To TextureSampleParameter2D
def from_TextureSample_to_TextureParameter2D(texture_sample_node, texture_parameter_node):
    from_TextureBase_to_TextureParameter2D(texture_sample_node, texture_parameter_node)
    texture_parameter_node.set_editor_property('automatic_view_mip_bias',
                                               texture_sample_node.get_editor_property('automatic_view_mip_bias'))
    texture_parameter_node.set_editor_property('const_coordinate', texture_sample_node.get_editor_property('const_coordinate'))
    texture_parameter_node.set_editor_property('const_mip_value', texture_sample_node.get_editor_property('const_mip_value'))
    texture_parameter_node.set_editor_property('mip_value_mode', texture_sample_node.get_editor_property('mip_value_mode'))
    texture_parameter_node.set_editor_property('sampler_source', texture_sample_node.get_editor_property('sampler_source'))

## Transfers data From TextureSampleParameter To TextureSampleParameter2D
def from_TextureParameter_to_TextureParameter2D(texture_parameter_node, texture_parameter2d_node):
    from_TextureSample_to_TextureParameter2D(texture_parameter_node, texture_parameter2d_node)
    texture_parameter2d_node.set_editor_property('channel_names', texture_parameter_node.get_editor_property('channel_names'))
    texture_parameter2d_node.set_editor_property('group', texture_parameter_node.get_editor_property('group'))
    texture_parameter2d_node.set_editor_property('parameter_name', texture_parameter_node.get_editor_property('parameter_name'))
    texture_parameter2d_node.set_editor_property('sort_priority', texture_parameter_node.get_editor_property('sort_priority'))

def from_TextureParameter2D_to_TextureParameter2D(texture_source_node, texture_target_node):
    from_TextureParameter_to_TextureParameter2D(texture_source_node, texture_target_node)

def is_nodes_texture_type(node):
    return

def transfer_texture_node(texture_source_node, texture_target_node):
    if isinstance(texture_source_node, unreal.MaterialExpressionTextureSampleParameter):
        from_TextureParameter_to_TextureParameter2D(texture_source_node, texture_target_node)
    elif isinstance(texture_source_node, unreal.MaterialExpressionTextureSample):
        from_TextureSample_to_TextureParameter2D(texture_source_node, texture_target_node)
    elif isinstance(texture_source_node, unreal.MaterialExpressionTextureBase):
        from_TextureBase_to_TextureParameter2D(texture_source_node, texture_target_node)
    elif isinstance(texture_source_node, unreal.MaterialExpressionTextureSampleParameter2D):
        from_TextureParameter2D_to_TextureParameter2D(texture_source_node, texture_target_node)

    else:
        unreal.log_error(transfer_texture_node.__name__ + '(): nodes are not texture type')

## Transfers connection between two nodes. Transfer all inputs and outputs of node_source to node_target.
# node_target will be connected the same as node_source.
def transfer_connections(material, node_source, node_target, all_nodes = None):
    if general.are_list_objects_not_None([material, node_source, node_target]):
        with unreal.ScopedEditorTransaction(transfer_connections.__name__ + '()') as ue_transaction:
            if all_nodes is None:
                all_nodes = unreal.PythonMaterialLib.get_material_expressions(material)

            node_source_input_connections, node_source_output_connections = get_material.find_connections_of_node(material, node_source)
            #from_expression, from_output_name, to_expression, to_input_name
            for connection in node_source_input_connections:
                from_expression = all_nodes[connection.left_expression_index]
                from_output_name = connection.left_output_name
                to_input_name = connection.right_expression_input_name
                unreal.MaterialEditingLibrary.connect_material_expressions(from_expression, from_output_name, node_target, to_input_name)

            for connection in node_source_output_connections:
                if connection.right_expression_index > 0:   # link to another node
                    from_output_name = connection.left_output_name
                    to_expression = all_nodes[connection.right_expression_index]
                    to_input_name = connection.right_expression_input_name
                    unreal.MaterialEditingLibrary.connect_material_expressions(node_target, from_output_name, to_expression, to_input_name)
                else:   # link to material output property
                    #from_expression, from_output_name, property
                    from_output_name = connection.left_output_name
                    property_name = connection.right_expression_input_name
                    unreal.PythonMaterialLib.connect_material_property(node_target, from_output_name, property_name)

    else:
        unreal.log_error(transfer_connections.__name__ + ': material, node_source, node_target must not be None')

## Sets correct texture parameter name by texture type
def set_texture_parameter_name(node):
    if node is not None:
        parameter_name = get_material.get_texture_parameter_name_node(node)
        if parameter_name != '':
            node.set_editor_property('parameter_name', parameter_name)
    else:
        unreal.log_error(set_texture_parameter_name.__name__ + ': node must not be None')
        return ''

## Creates TextureSampleParameter2D node with data from node_data
# @node_data (DataTextureSampleParameter2D) wrapper object for node
def new_node_TextureSampleParameter2D(material, node_meta_data = None, node_pos_x = 0, node_pos_y = 0):
    if material is not None:
        texture_node = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionTextureSampleParameter2D,
                                                                                node_pos_x, node_pos_y)
        node_meta_data.set_node_by_meta_data(texture_node)
        if node_meta_data is not None and node_meta_data.texture is not None:
            texture_node.set_editor_property('parameter_name', get_material.get_texture_parameter_name_texture(node_meta_data.texture))
        return texture_node
    else:
        unreal.log_error(new_node_TextureSampleParameter2D.__name__ + ': material must not be None')
        return None

def new_node_TextureSampleParameter2D_path(material_path, node_data = None, node_pos_x=0, node_pos_y=0):
    if general.is_not_none_or_empty(material_path):
        material = get_asset.get_asset_by_object_path(material_path)
        return new_node_TextureSampleParameter2D(material, node_data, node_pos_x, node_pos_y)
    else:
        unreal.log_error(new_node_TextureSampleParameter2D_path.__name__ + ': material_path must not be None')
        return None

def new_node_TextureSampleParameter2D_node(material, node = None, node_pos_x = 0, node_pos_y = 0):
    if material is not None:
        texture_node = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionTextureSampleParameter2D,
                                                                                node_pos_x, node_pos_y)
        if node is not None:
            transfer_texture_node(node, texture_node)
        else:
            unreal.log_error(new_node_TextureSampleParameter2D_node.__name__ + ': node must not be None')
        return texture_node
    else:
        unreal.log_error(new_node_TextureSampleParameter2D_node.__name__ + ': material must not be None')
        return None

## Creates Vector node
# TODO: Add more editor_properties
def new_node_Vector(material, parameter_name, default_color):
    if material is not None:
        node_base_color = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionVectorParameter)
        node_base_color.set_editor_property('parameter_name', parameter_name)
        node_base_color.set_editor_property('default_value', default_color)
        return node_base_color

    else:
        unreal.log_error(new_node_BaseColorVector.__name__ + ': material must not be None')
        return None

## Creates Base color vector useful for multiplying with diffuse map or albedo
def new_node_BaseColorVector(material):
    return new_node_Vector(material, 'BaseColor', unreal.LinearColor.WHITE)

## Creates Base color vector useful for multiplying with diffuse map or albedo
def new_node_ScalarParameter_texture_factor(material, texture_type):
    if material is not None and general.is_not_none_or_empty(texture_type):
        node_scalar_texture_factor = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionScalarParameter)
        node_scalar_texture_factor.set_editor_property('parameter_name', texture_type + '_Factor')
        node_scalar_texture_factor.set_editor_property('default_value', 1.0)
        return node_scalar_texture_factor

    else:
        unreal.log_error(new_node_ScalarParameter_texture_factor.__name__ + ': material and texture_typ must not be None or empty')
        return None

## Creates material expression/node of blend_overlay material function call
def new_blend_overlay_node(material):
    # MaterialFunction'/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_Overlay.Blend_Overlay'
    blend_overlay_function = get_asset.load_asset('/Engine/Functions/Engine_MaterialFunctions03/Blends/Blend_Overlay.Blend_Overlay')
    node_blend_overlay = unreal.MaterialEditingLibrary.create_material_expression(material, unreal.MaterialExpressionMaterialFunctionCall)
    node_blend_overlay.set_material_function(blend_overlay_function)
    return node_blend_overlay


def delete_trash_suffix(parameter_name):
    #   \s\(\d+\)\Z
    regex_pattern = '\\s\\(\\d+\\)\\Z'
    match_object = re.search(regex_pattern, parameter_name)
    clean_parameter_name = parameter_name
    if match_object is not None:
        trash_suffix = match_object[0]
        clean_parameter_name = clean_parameter_name[:len(parameter_name)-len(trash_suffix)]

    return clean_parameter_name

def delete_nodes_trash_suffix(material):
    if material is not None:
        with unreal.ScopedEditorTransaction(delete_nodes_trash_suffix.__name__ + '()') as ue_transaction:
            all_parameter_nodes = get_material.find_nodes_in_material(material, config.PARAMETER_NODE_TYPES)
            for node in all_parameter_nodes:
                parameter_name = general.Name_to_str(node.get_editor_property('parameter_name'))
                node.set_editor_property('parameter_name', delete_trash_suffix(parameter_name))

            #material_path = get_asset.get_path_from_object(material)
            #unreal.EditorAssetLibrary.save_asset(material_path)
            #unreal.MaterialEditingLibrary.recompile_material(material)
    else:
        unreal.log_error(delete_nodes_trash_suffix.__name__ + ': material must not be None')

def delete_nodes_trash_suffix_in_dir(dir_path):
    if general.is_not_none_or_empty(dir_path):
        materials_data = get_asset.get_materials_data_by_dir(dir_path)
        if materials_data is not None:
            with unreal.ScopedEditorTransaction(delete_nodes_trash_suffix_in_dir.__name__ + '()') as ue_transaction:
                for material_data in materials_data:
                    delete_nodes_trash_suffix(material_data.get_asset())

        else:
            unreal.log_error(delete_nodes_trash_suffix_in_dir.__name__ + ': did not find any material in dir: ' + dir_path)
    else:
        unreal.log_error(delete_nodes_trash_suffix_in_dir.__name__ + ': dir_path must not be None or Empty')


def replace_space_to_underscore(parameter_name):
    #   \s\(\d+\)\Z
    regex_pattern = '\\s\\(\\d+\\)\\Z'
    match_object = re.search(regex_pattern, parameter_name)
    clean_parameter_name = parameter_name
    if match_object is not None:
        trash_suffix = match_object[0]
        clean_parameter_name = clean_parameter_name[:len(parameter_name)-len(trash_suffix)]

    return clean_parameter_name

## Replace all white space chars in parameter names in material
def replace_parameters_space_to_underscore(material):
    if material is not None:
        with unreal.ScopedEditorTransaction(replace_parameters_space_to_underscore.__name__ + '()') as ue_transaction:
            all_parameter_nodes = get_material.find_nodes_in_material(material, config.PARAMETER_NODE_TYPES)
            for node in all_parameter_nodes:
                parameter_name = general.Name_to_str(node.get_editor_property('parameter_name'))
                #node.set_editor_property('parameter_name', replace_space_to_underscore(parameter_name))
                node.set_editor_property('parameter_name', parameter_name.replace(' ', '_'))
    else:
        unreal.log_error(replace_parameters_space_to_underscore.__name__ + ': material must not be None')

def replace_parameters_space_to_underscore_in_dir(dir_path):
    if general.is_not_none_or_empty(dir_path):
        materials_data = get_asset.get_materials_data_by_dir(dir_path)
        if materials_data is not None:
            with unreal.ScopedEditorTransaction(replace_parameters_space_to_underscore_in_dir.__name__ + '()') as ue_transaction:
                for material_data in materials_data:
                    replace_parameters_space_to_underscore(material_data.get_asset())

        else:
            unreal.log_error(replace_parameters_space_to_underscore_in_dir.__name__ + ': did not find any material in dir: ' + dir_path)
    else:
        unreal.log_error(replace_parameters_space_to_underscore_in_dir.__name__ + ': dir_path must not be None or Empty')


## Replace all white space chars in parameter names in material
def correct_normal_map_map(material):
    if material is not None:
        with unreal.ScopedEditorTransaction(replace_parameters_space_to_underscore.__name__ + '()') as ue_transaction:
            all_parameter_nodes = get_material.find_nodes_in_material(material, config.PARAMETER_NODE_TYPES)
            for node in all_parameter_nodes:
                parameter_name = general.Name_to_str(node.get_editor_property('parameter_name'))
                suffix = '_Map'
                if parameter_name.endswith(suffix + suffix):
                    new_parameter_name = parameter_name[:-len(suffix)]
                    node.set_editor_property('parameter_name', new_parameter_name)
    else:
        unreal.log_error(replace_parameters_space_to_underscore.__name__ + ': material must not be None')

def correct_normal_map_map_in_dir(dir_path):
    if general.is_not_none_or_empty(dir_path):
        materials_data = get_asset.get_materials_data_by_dir(dir_path)
        if materials_data is not None:
            with unreal.ScopedEditorTransaction(correct_normal_map_map_in_dir.__name__ + '()') as ue_transaction:
                for material_data in materials_data:
                    correct_normal_map_map(material_data.get_asset())

        else:
            unreal.log_error(replace_parameters_space_to_underscore_in_dir.__name__ + ': did not find any material in dir: ' + dir_path)
    else:
        unreal.log_error(replace_parameters_space_to_underscore_in_dir.__name__ + ': dir_path must not be None or Empty')

def set_materials_two_sided(target_paths, new_value = False, is_recursive_search = True, only_on_disk_assets = False,
                            search_properties_values = [], is_disjunction = True):
    set_asset.set_assets_properties_in_folder_log(log.LOG_PATH_SET_PROPERTIES, 'set_materials_two_sided',
                                                    target_paths, is_recursive_search,
                                                    only_on_disk_assets, [config.CLASS_NAME_MATERIAL],
                                                    search_properties_values, [('two_sided', new_value)], is_disjunction)


## Recompile all materials in dir_paths after changes in material
def recompile_material_in_dirs(dirs_paths):
    if general.is_not_none_or_empty_lists(dirs_paths):
        materials_data = get_asset.get_materials_data_by_dirs(dirs_paths)
        if materials_data is not None:
            with unreal.ScopedEditorTransaction(recompile_material_in_dirs.__name__ + '()') as ue_transaction:
                for material_data in materials_data:
                    unreal.MaterialEditingLibrary.recompile_material(material_data.get_asset())

        else:
            unreal.log_error(recompile_material_in_dirs.__name__ + '(): did not find any material in dir: ' + dirs_paths)
    else:
        unreal.log_error(recompile_material_in_dirs.__name__ + '(): dirs_paths each must not be None or Empty')

def recompile_material_in_dir(dir_path):
    recompile_material_in_dirs([dir_path])