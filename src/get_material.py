import unreal

#import unreal_scripts.config as config
import unreal_scripts.service.general as general
import unreal_scripts.src.get_asset as get_asset
import unreal_scripts.src.prefix_suffix as prefix_suffix

import importlib
#importlib.reload(config)
importlib.reload(general)
importlib.reload(get_asset)
importlib.reload(prefix_suffix)

# @return Texture type object
def get_texture_asset_from_node(node):
    if node is not None:
        return node.get_editor_property('texture')
    else:
        unreal.log_error(get_texture_asset_from_node.__name__ + ': node must not be None')
        return

# Find texture source path by node of type inhereted by unreal.MaterialExpression
def get_texture_node_source_path(node):
    if node is not None:
        return get_asset.get_path_from_object(get_texture_asset_from_node(node))
    else:
        unreal.log_error(get_texture_node_source_path.__name__ + ': node must not be None')

# Reads prefix and suffix of texture asset and returns type of texture by convention
def get_texture_type_by_prefix_suffix_node(node):
    texture_path = get_texture_node_source_path(node)
    if general.is_not_none_or_empty(texture_path):
        return prefix_suffix.get_texture_type_by_prefix_suffix(texture_path)
    else:
        unreal.log(get_texture_type_by_prefix_suffix_node.__name__ + '(): did not find any texture source in node')
        return

# Standardize Texture Parameter Name
def get_texture_parameter_name(texture_type):
    return texture_type + '_Map'

def get_texture_parameter_name_texture(texture):
    texture_path = get_asset.get_path_from_object(texture)
    texture_type = prefix_suffix.get_texture_type_by_prefix_suffix(texture_path)
    return get_texture_parameter_name(texture_type)

def get_texture_parameter_name_node(node):
    if node is not None:
        if issubclass(type(node), unreal.MaterialExpressionTextureBase):
            texture_path = get_asset.get_path_from_object(node.get_editor_property('texture'))
            texture_type = prefix_suffix.get_texture_type_by_prefix_suffix(texture_path)
            return get_texture_parameter_name(texture_type)
        else:
            unreal.log_error(get_texture_parameter_name_node.__name__ + ': node must be of subclass unreal.MaterialExpressionTextureBase')
            return ''
    else:
        unreal.log_error(get_texture_parameter_name_node.__name__ + ': node must not be None')
        return ''

# @return gets all nodes/expressions of input material
# If you delete some nodes, they will be saved in memory. And get_material_all_nodes will show ghosty results. You need to relaunch Unreal Engine.
def get_material_all_nodes_python(material):
    if material is not None:
        all_nodes = []
        material_path = material.get_path_name()
        object_iterator = unreal.ObjectIterator()
        for object in object_iterator:
          if isinstance(object, unreal.MaterialExpression) and object.get_path_name().startswith(material_path):
              all_nodes.append(object)
        return all_nodes
    else:
        unreal.log_error(get_material_all_nodes_python.__name__ + ': node must not be None')
        return

# Getting all material nodes using TAPython plugin
# https://github.com/cgerchenhp/UE_TAPython_Plugin_Release
def get_material_all_nodes_tapython(material):
    if material is not None:
        return unreal.PythonMaterialLib.get_material_expressions(material)

    else:
        unreal.log_error(get_material_all_nodes_tapython.__name__ + ': material must not be None')
        return

# Wrapper for more correct function
def get_material_all_nodes(material):
    return get_material_all_nodes_tapython(material)

def get_material_all_nodes_by_path(material_object_path):
    if general.is_not_none_or_empty(material_object_path):
        material = unreal.EditorAssetLibrary.load_asset(material_object_path)
        return get_material_all_nodes(material)
    else:
        unreal.log_error(get_material_all_nodes_by_path.__name__ + ': object_path must not be None or empty')
        return

''' left_expression_index
    left_output_index
    left_output_name
    right_expression_index
    right_expression_input_index
    right_expression_input_name
    Index are indexes of unreal.PythonMaterialLib.get_material_expressions(material) list'''
# return list of all connections in material
def get_material_connections(material):
    if material is not None:
        return unreal.unreal.PythonMaterialLib.get_material_connections(material)
    else:
        unreal.log_error(get_material_connections.__name__ + ': material must not be None')
        return

# Find connections of node
# @return tuple of connections.
def find_connections_of_node(material, node, all_nodes = None, all_connections = None):
    if all_nodes is None:
        all_nodes = unreal.PythonMaterialLib.get_material_expressions(material)
    if all_connections is None:
        all_connections = unreal.PythonMaterialLib.get_material_connections(material)

    node_index = None
    if all_nodes.count(node) > 0:
        node_index = all_nodes.index(node)

    input_node_connections, output_node_connections = [], []
    for connection in all_connections:
        if connection.right_expression_index == node_index: # input_node_connections
            input_node_connections.append(connection)
        if connection.left_expression_index == node_index:  # output_node_connections
            output_node_connections.append(connection)
    return input_node_connections, output_node_connections


def use_nodes_types_filter(filtered_nodes, nodes_types, is_nodes_types_subclasses):
    i = 0
    while i < len(filtered_nodes):
        is_not_in_types = (not is_nodes_types_subclasses) and (not general.is_in_types(filtered_nodes[i], nodes_types))
        is_not_in_subclasses = is_nodes_types_subclasses and (not general.is_in_subclasses(filtered_nodes[i], nodes_types))
        if is_not_in_types or is_not_in_subclasses:
            filtered_nodes.pop(i)
        else:
            i += 1

# Compares Unreal Engine object(nodes in material f.e.)
def compare_properites_values(ue_object, properties_values):
    comparation_results = []
    for property_value in properties_values:
        try:
            gotten_property = ue_object.get_editor_property(property_value[0])
            comparation_results.append(gotten_property == property_value[1])
        except:
            unreal.log(compare_properites_values.__name__ + '(): There is no such property')
    return comparation_results

def is_node_in_properties_values(node, properties_values, is_disjunction):
    comparation_results = compare_properites_values(node, properties_values)
    if general.is_not_none_or_empty(comparation_results):
        if is_disjunction:
            return general.disjunction_of_conditions(comparation_results)
        else: # Conjunction
            return general.conjunction_of_conditions(comparation_results)
    else:   # No properties found
        return False

def use_properties_values_filter(filtered_nodes, properties_values, is_disjunction):
    i = 0
    while i < len(filtered_nodes):
        if not is_node_in_properties_values(filtered_nodes[i], properties_values, is_disjunction):
            filtered_nodes.pop(i)
        else:
            i += 1

# Use filter if node has subclass of MaterialExpressionTextureBase. And if node linked to material output property by nodes chain or direct
# Doesn't pop nodes any class except MaterialExpressionTextureBase and its subclasses. Using filter only on Textures nodes.
def use_linked_textures_to_output_filter(material, filtered_nodes, is_linked_to_output):
    # all nodes with baseclass linked to material output property
    used_textures = unreal.MaterialEditingLibrary.get_used_textures(material)
    #unreal.log(used_textures)
    i = 0
    while i < len(filtered_nodes):
        # Is current node texture type node/expression
        if issubclass(type(filtered_nodes[i]), unreal.MaterialExpressionTextureBase):
            texture = get_texture_asset_from_node(filtered_nodes[i])
            if is_linked_to_output:
                if not used_textures.count(texture) > 0:
                    filtered_nodes.pop(i)
                else:
                    i += 1
            else: # Node is unlinked to output
                if used_textures.count(texture) > 0:
                    filtered_nodes.pop(i)
                else:
                    i += 1
        else:
            i += 1

''' Filters input nodes list by some specific conditions
    @param nodes is list of node
    @param nodes_types is filter list of node types, like unreal.MaterialExpression
    @param nodes_types is filter list of node types, like unreal.MaterialExpression
    @param nodes_types is filter list of node types, like unreal.MaterialExpression
    @param is_disjunction is trigger means if comparation of properties_values must be disjunction
    Disjunction = OR; Conjunction = AND
    You can not to use any of Filters: nodes_types, properties_values, is_linked_to_output '''
def filter_nodes_of_material(material, nodes,
                             nodes_types = None, properties_values = None, is_linked_to_output = None,      # filters
                             is_disjunction = True, is_nodes_types_subclasses = False):                     # triggers
    unreal.log(filter_nodes_of_material.__name__ + ' Started')
    if general.is_not_none_or_empty(nodes):
        filtered_nodes = nodes.copy()
        unreal.log('Nodes count before filtering : ' + str(len(filtered_nodes)))
        if nodes_types is not None:
            use_nodes_types_filter(filtered_nodes, nodes_types, is_nodes_types_subclasses)
            unreal.log('Nodes count after use_nodes_types_filter filtering: ' + str(len(filtered_nodes)))
        if general.is_not_none_or_empty(properties_values):
            use_properties_values_filter(filtered_nodes, properties_values, is_disjunction)
            unreal.log('Nodes count after use_properties_values_filter filtering: ' + str(len(filtered_nodes)))
        if is_linked_to_output is not None:
            use_linked_textures_to_output_filter(material, filtered_nodes, is_linked_to_output)
            unreal.log('Nodes count after use_linked_textures_to_output_filter filtering: ' + str(len(filtered_nodes)))
        return filtered_nodes

    else:
        unreal.log_error(filter_nodes_of_material.__name__ + ': nodes must not be None')
        return

# @param nodes list of node
# @param nodes_types list of node types, like unreal.MaterialExpression
# @param all_nodes if you already search for all nodes then input them to function
def find_nodes_in_material(material,
                           nodes_types = None, properties_values = [], is_linked_to_output = None,      # filters
                           is_disjunction = True,  is_nodes_types_subclasses = False, all_nodes = None):
    if all_nodes is None:
       all_nodes = get_material_all_nodes(material)
    if general.is_not_none_or_empty(all_nodes):
        return filter_nodes_of_material(material, all_nodes, nodes_types, properties_values, is_linked_to_output,
                                        is_disjunction, is_nodes_types_subclasses)
    else:
        unreal.log_error(find_nodes_in_material.__name__ + ': get_material_all_nodes did not find any node in material')
        unreal.log_error('material path: ' + get_asset.get_path_from_object(material))
        return

# @param nodes list of node
# @param nodes_types list of node types, like unreal.MaterialExpression
# @param all_nodes if you already search for all nodes input them to function
# @return tuple of (material, found_nodes)
def find_nodes_in_material_by_path(material_object_path,
                                   nodes_types = None, properties_values = [], is_linked_to_output = None,      # filters
                                   is_disjunction = True, is_nodes_types_subclasses = False, all_nodes = None):
    if general.is_not_none_or_empty(material_object_path):
        material = get_asset.load_asset(material_object_path)
        find_results = find_nodes_in_material(material, nodes_types, properties_values, is_linked_to_output,
                                              is_disjunction, is_nodes_types_subclasses, all_nodes)
        return find_results, material
    else:
        unreal.log_error(find_nodes_in_material_by_path.__name__ + ': material_object_path must be empty or None')
        return

def find_nodes_in_material_by_types(material, nodes_types = None):
    return find_nodes_in_material(material, nodes_types, is_nodes_types_subclasses = False)

# Search free texture node
# If proper material output for free node has already been connected, doesn't link or relink.
def find_unlinked_texture_nodes(material):
    return find_nodes_in_material(material, [unreal.MaterialExpressionTextureSample, unreal.MaterialExpressionTextureSampleParameter2D],
                                  is_nodes_types_subclasses = False, is_linked_to_output = False)

def get_material_connections(material):
    a = 0

# @return list of material output properties that must be connected by adding texture of some type. T_Example_Diff -> unreal.MaterialProperty.MP_BASE_COLOR
def get_material_outputs_by_texture_type(texture_type):
    if general.is_not_none_or_empty(texture_type):
        if texture_type == 'BaseColor':
            return [unreal.MaterialProperty.MP_BASE_COLOR]
        elif texture_type == 'Albedo':
            return [unreal.MaterialProperty.MP_BASE_COLOR]
        elif texture_type == 'AmbientOcclusion':
            return [unreal.MaterialProperty.MP_AMBIENT_OCCLUSION]
        elif texture_type == 'Roughness':
            return [unreal.MaterialProperty.MP_ROUGHNESS]
        elif texture_type == 'Gloss':
            return [unreal.MaterialProperty.MP_ROUGHNESS]
        elif texture_type == 'Specular':
            return [unreal.MaterialProperty.MP_SPECULAR]
        elif texture_type == 'Metallic':
            return [unreal.MaterialProperty.MP_METALLIC]
        elif texture_type == 'Normal':
            return [unreal.MaterialProperty.MP_NORMAL]
        elif texture_type == 'Height':
            # World Position Offset
            return
        elif texture_type == 'Bump':
            # World Position Offset
            return
        elif texture_type == 'Displacement':
            # World Displacement + Tesseletion Multiplier
            return
        elif texture_type == 'Emissive':
            return [unreal.MaterialProperty.MP_EMISSIVE_COLOR]
        elif texture_type == 'Alpha/Opacity':
            return [unreal.MaterialProperty.MP_OPACITY]
        elif texture_type == 'OpacityMask':
            return [unreal.MaterialProperty.MP_OPACITY_MASK]
        elif texture_type == 'LightMap':
            return None
        elif texture_type == 'OcclusionRoughnessMetallic':
            return [unreal.MaterialProperty.MP_AMBIENT_OCCLUSION,
                    unreal.MaterialProperty.MP_ROUGHNESS,
                    unreal.MaterialProperty.MP_METALLIC,]
        elif texture_type == 'SpecularGlossiness':
            return [unreal.MaterialProperty.MP_SPECULAR,
                    unreal.MaterialProperty.MP_ROUGHNESS]
        elif texture_type == 'Convex/Concave':
            return [unreal.MaterialProperty.MP_BASE_COLOR]
        elif texture_type == 'FUZZ':
            return None
        elif texture_type == 'FlowMap':
            return None
        elif texture_type == 'Packed':
            return None
        elif texture_type == 'TextureCube':
            return None
        elif texture_type == 'MediaTexture':
            return None
        elif texture_type == 'RenderTarget':
            return None
        elif texture_type == 'CubeRenderTarget':
            return None
        elif texture_type == 'TextureLightProfile':
            return None
    else:
        unreal.log_error(get_material_outputs_by_texture_type.__name__ + ': texture_type must not be empty or None')

# TODO:
def is_node_linked_to_property(property_name):
    a = 0

# TODO:
def find_nodes_linked_to_property():
    a = 0

# TODO:
def find_texture_nodes_linked_to_property():
    a = 0