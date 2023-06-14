import unreal
import unreal_engine_scripts.config as config

import importlib
importlib.reload(config)

#=====================================Ini Section=============================================
# Commands: NoMipMap, NoLods, Find, SetProperties, set_textures_mipmap_gen,
# set_meshes_lod_group, NoCollision, MaterialTwoSided, GetMaterialTwoSided, LayoutMaterialNodes
# set_textures_with_no_mipmap_gen_settings_dirs, set_meshes_with_no_lods_group_dirs, set_mipmaps_n_lod_group_to_no_lods_dirs
# change_number_of_lod_in_dirs
COMMAND = 'change_number_of_lod_in_dirs'

# No '/' in the end of the path
#TARGET_PATHS = ['/Game/ThirdPerson/Military/Vehicle/Modern/Land/Tank/T-90_02/Materials']
#TARGET_PATHS = ['/Game/ThirdPerson/Military/Weapon/Modern/Ranged/Firearms/1/Pack_1']
TARGET_PATHS = ['/Game/Test/Lod']
#TARGET_PATHS = ['/Game/ThirdPerson']

# Assets will be find in all sub dirs
IS_RECURSIVE_SEARCH = True
ONLY_ON_DISK_ASSETS = False

# Texture2D, Material, StaticMesh, SkeletalMesh
#TARGET_CLASS_NAMES = [config.CLASS_NAME_TEXTURE]
TARGET_CLASS_NAMES = [config.CLASS_NAME_STATIC_MESH]

# Disjunction = OR. Conjunction = AND.
IS_DISJUNCTION = False

SEARCH_PROPERTIES_VALUES = []
#SEARCH_PROPERTIES_VALUES = [(config.PROPERTY_MIPMAP_GEN, config.SETTING_NO_MIPMAPS), (config.PROPERTY_POWER_OF_TWO_MODE, config.SETTING_POWER_OF_TWO_PAD_POWER)]


# PROPERTY_MIPMAP_GEN = SETTING_NO_MIPMAPS, SETTING_DEFAULT_MIPMAPS | PROPERTY_LOD_GROUP = SETTING_NO_LOD_GROUP, SETTING_DEFAULT_LOD_GROUP
NEW_PROPERTIES_VALUES = []
#NEW_PROPERTIES_VALUES = [(config.PROPERTY_MIPMAP_GEN, config.SETTING_NO_MIPMAPS)]

MATERIAL_TWO_SIDED = True

MIPMAPS_SETTING = config.SETTING_DEFAULT_MIPMAPS
LOD_GROUP_SETTING = config.SETTING_DEFAULT_LOD_GROUP

NUMBER_OF_LOD = 8
#==============================================================================================