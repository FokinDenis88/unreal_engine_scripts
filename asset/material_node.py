import unreal

#import unreal_engine_python_scripts.config as config
#import unreal_engine_python_scripts.service.general as general
import unreal_engine_python_scripts.src.get_asset as get_asset
import unreal_engine_python_scripts.src.prefix_suffix as prefix_suffix

import importlib
#importlib.reload(config)
#importlib.reload(general)
importlib.reload(get_asset)
importlib.reload(prefix_suffix)

## Meta data is duplicate of data real node of material
# automatic_view_mip_bias (bool): [Read-Write] Whether the texture should be sampled with per view mip biasing for sharper output with Temporal AA.
#    channel_names (ParameterChannelNames): [Read-Write] Channel Names
#    const_coordinate (uint8): [Read-Write] only used if Coordinates is not hooked up
#    const_mip_value (int32): [Read-Write] only used if MipValue is not hooked up
#    desc (str): [Read-Write] A description that level designers can add (shows in the material editor UI).
#    group (Name): [Read-Write] The name of the parameter Group to display in MaterialInstance Editor. Default is None group
#    is_default_meshpaint_texture (bool): [Read-Write] Is default selected texture when using mesh paint mode texture painting
#    mip_value_mode (TextureMipValueMode): [Read-Write] Defines how the MipValue property is applied to the texture lookup
#    parameter_name (Name): [Read-Write] Parameter Name
#    sampler_source (SamplerSourceMode): [Read-Write] Controls where the sampler for this texture lookup will come from. Choose ‘from texture asset’ to make use of the UTexture addressing settings, Otherwise use one of the global samplers, which will not consume a sampler slot. This allows materials to use more than 16 unique textures on SM5 platforms.
#    sampler_type (MaterialSamplerType): [Read-Write] Sampler Type
#    sort_priority (int32): [Read-Write] Controls where the this parameter is displayed in a material instance parameter list. The lower the number the higher up in the parameter list.
#    texture (Texture): [Read-Write] Texture '''
class MetaDataTextureSampleParameter2D:
    def __init__(self, parameter_name = '', texture = None, desc = '', group = '', automatic_view_mip_bias = False,
                 channel_names = unreal.ParameterChannelNames(),
                 const_coordinate = 0, const_mip_value = 0, is_default_meshpaint_texture = False,
                 mip_value_mode = unreal.TextureMipValueMode.TMVM_NONE,
                 sampler_source = unreal.SamplerSourceMode.SSM_FROM_TEXTURE_ASSET,
                 sampler_type = unreal.MaterialSamplerType.SAMPLERTYPE_COLOR, sort_priority = 0):
        self.automatic_view_mip_bias = automatic_view_mip_bias
        self.channel_names = channel_names
        self.const_coordinate = const_coordinate
        self.const_mip_value = const_mip_value
        self.desc = desc
        self.group = group
        self.is_default_meshpaint_texture = is_default_meshpaint_texture
        self.mip_value_mode = mip_value_mode
        self.parameter_name = parameter_name
        self.sampler_source = sampler_source
        self.sampler_type = sampler_type
        self.sort_priority = sort_priority
        self.texture = texture

    ## Set data DataTextureSampleParameter2D, recieved from loaded node
    # Gets Nodes Data from real node
    def set_meta_data(self, node):
        if node is not None:
            if isinstance(node, unreal.MaterialExpressionTextureSampleParameter2D):
                self.automatic_view_mip_bias =      node.get_editor_property('automatic_view_mip_bias')
                self.channel_names =                node.get_editor_property('channel_names')
                self.const_coordinate =             node.get_editor_property('const_coordinate')
                self.const_mip_value =              node.get_editor_property('const_mip_value')
                self.desc =                         node.get_editor_property('desc')
                self.group =                        node.get_editor_property('group')
                self.is_default_meshpaint_texture = node.get_editor_property('is_default_meshpaint_texture')
                self.mip_value_mode =               node.get_editor_property('mip_value_mode')
                self.parameter_name =               node.get_editor_property('parameter_name')
                self.sampler_source =               node.get_editor_property('sampler_source')
                self.sampler_type =                 node.get_editor_property('sampler_type')
                self.sort_priority =                node.get_editor_property('sort_priority')
                self.texture =                      node.get_editor_property('texture')
            else:
                unreal.log_error(MetaDataTextureSampleParameter2D.__name__ +
                                 ' set_meta_data(): node must be only of type unreal.MaterialExpressionTextureSampleParameter2D')
        else:
            unreal.log_error(MetaDataTextureSampleParameter2D.__name__ + ' set_meta_data(): node must not be None')

    ## Set data DataTextureSampleParameter2D, recieved from loaded node
    def set_node_by_meta_data(self, node):
        if node is not None:
            if isinstance(node, unreal.MaterialExpressionTextureSampleParameter2D):
                node.set_editor_property('automatic_view_mip_bias',         self.automatic_view_mip_bias)
                node.set_editor_property('channel_names',                   self.channel_names)
                node.set_editor_property('const_coordinate',                self.const_coordinate)
                node.set_editor_property('const_mip_value',                 self.const_mip_value)
                node.set_editor_property('desc',                            self.desc)
                node.set_editor_property('group',                           self.group)
                node.set_editor_property('is_default_meshpaint_texture',    self.is_default_meshpaint_texture)
                node.set_editor_property('mip_value_mode',                  self.mip_value_mode)
                node.set_editor_property('parameter_name',                  self.parameter_name)
                node.set_editor_property('sampler_source',                  self.sampler_source)
                node.set_editor_property('sampler_type',                    self.sampler_type)
                node.set_editor_property('sort_priority',                   self.sort_priority)
                if self.texture is not None:
                    node.set_editor_property('texture',                     self.texture)
            else:
                unreal.log_error(MetaDataTextureSampleParameter2D.__name__ +
                                 ' set_node_by_meta_data(): node must be of type unreal.MaterialExpressionTextureSampleParameter2D')
        else:
            unreal.log_error(MetaDataTextureSampleParameter2D.__name__ + ' set_node_by_meta_data(): node must not be None')

## Extension of MetaDataTextureSampleParameter2D class
class MetaDataTextureSampleParameter2DExt(MetaDataTextureSampleParameter2D):
    def __init__(self, meta_data = MetaDataTextureSampleParameter2D()):
        super().__init__(meta_data.parameter_name, meta_data.texture, meta_data.desc, meta_data.group, meta_data.automatic_view_mip_bias,
                         meta_data.channel_names, meta_data.const_coordinate, meta_data.const_mip_value, meta_data.is_default_meshpaint_texture,
                         meta_data.mip_value_mode, meta_data.sampler_source, meta_data.sampler_type, meta_data.sort_priority)
        self.update_texture_path_n_type(meta_data.texture)

    def set_meta_data(self, node):
        if node is not None:
            if isinstance(node, unreal.MaterialExpressionTextureSampleParameter2D):
                super().set_meta_data(node)
                self.update_texture_path_n_type(node.get_editor_property('texture'))
            else:
                unreal.log_error(MetaDataTextureSampleParameter2DExt.__name__ +
                                 ' set_meta_data(): node must be only of type unreal.MaterialExpressionTextureSampleParameter2D')
        else:
            unreal.log_error(MetaDataTextureSampleParameter2DExt.__name__ + ' set_meta_data(): node must not be None')

    def set_node_by_meta_data(self, node):
        super().set_node_by_meta_data(node)

    def update_texture_path_n_type(self, texture):
        if texture is not None:
            self.texture_path = get_asset.get_path_from_object(texture)
            self.texture_type = prefix_suffix.get_texture_type_by_prefix_suffix(self.texture_path)
        else:
            self.texture_path = ''
            self.texture_type = ''