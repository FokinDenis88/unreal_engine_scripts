import os

import unreal

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_ASSETS_START = '/Game/'

IS_EMPTY_OR_NONE_TEXT = 'is Empty or None'
IS_WORKING_TEXT = ' is Working.'


#================= Assets class names===================================
CLASS_NAME_TEXTURE = 'Texture'
CLASS_NAME_TEXTURE_TWO_D = 'Texture2D'
CLASS_NAME_MATERIAL = 'Material'
CLASS_NAME_STATIC_MESH = 'StaticMesh'
CLASS_NAME_SKELETAL_MESH = 'SkeletalMesh'

class ClassName:
    TEXTURE = 'Texture2D'
    MATERIAL = 'Material'
    STATIC_MESH = 'StaticMesh'
    SKELETAL_MESH = 'SkeletalMesh'

##class alias
TextureNode = unreal.MaterialExpressionTextureSampleParameter2D
TextureBase = unreal.MaterialExpressionTextureBase

PARAMETER_NODE_TYPES = [unreal.MaterialExpressionScalarParameter, unreal.MaterialExpressionVectorParameter,
                        unreal.MaterialExpressionTextureSampleParameter2D, unreal.MaterialExpressionStaticSwitchParameter]

## All texture node/expression not abstract types
TEXTURE_NODES_TYPES = [unreal.MaterialExpressionTextureSample, unreal.MaterialExpressionTextureSampleParameter2D]
#=======================================================================

## Property names and values
class PropertyTexture:
    MIPMAP_GEN = 'mip_gen_settings'
    LOD_GROUP = 'lod_group'
    POWER_OF_TWO_MODE = 'power_of_two_mode'

class SettingTexture:
    DEFAULT_MIPMAPS = unreal.TextureMipGenSettings.TMGS_FROM_TEXTURE_GROUP
    NO_MIPMAPS = unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS

    DEFAULT_LOD_GROUP = unreal.Name('SmallProp')
    NO_LOD_GROUP = 'None'

    SETTING_POWER_OF_TWO_NO = unreal.TexturePowerOfTwoSetting.NONE
    SETTING_POWER_OF_TWO_PAD_POWER = unreal.TexturePowerOfTwoSetting.PAD_TO_POWER_OF_TWO


#'''
PROPERTY_MIPMAP_GEN = 'mip_gen_settings'
PROPERTY_LOD_GROUP = 'lod_group'
PROPERTY_POWER_OF_TWO_MODE = 'power_of_two_mode'

SETTING_NO_MIPMAPS = unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS
SETTING_DEFAULT_MIPMAPS = unreal.TextureMipGenSettings.TMGS_FROM_TEXTURE_GROUP
SETTING_NO_LOD_GROUP = 'None'
SETTING_DEFAULT_LOD_GROUP = unreal.Name('SmallProp')
SETTING_POWER_OF_TWO_NO = unreal.TexturePowerOfTwoSetting.NONE
SETTING_POWER_OF_TWO_PAD_POWER = unreal.TexturePowerOfTwoSetting.PAD_TO_POWER_OF_TWO
#'''

#=========================================================================