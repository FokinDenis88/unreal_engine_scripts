#import unreal
import unreal_engine_python_scripts.config as config

import importlib
importlib.reload(config)

#===================================Info Section==================================================================
# ConnectByAssociation - connects textures in packs to materials. texture_paths_packs[i] links to material_paths[i]
# ConnectTexturePacks - connects textures in dir packs to materials in dirs by association in file names. T_Root_Metallic -> M_Root
# ConnectTextureFiles - direct connection of textures to materials.
# ConnectFreeNodes - finds unlinked nodes in material and liks them to material output
# AutoAlign - align nodes in grid order in material
# AutoFill - standartize material nodes. F.e if there is only diffuse map, connected to base color output of material
    # adds BaseColor Vector and multiply diffuse color * BaseColor Vector. Fill empty parts of material.
# ReplaceTextureSamples - replace TextureSamples by TextureSamplesParameters2D. TextureSamples can not be accessed by blueprints

#====================================Ini Section===================================================================

# ConnectByAssociation, ConnectTexturePacks, ConnectTextureFiles, ConnectFreeNodes, AutoAlign, ReplaceTextureSamples
COMMAND = 'ConnectFreeNodes'
# TODO: AutoFill

# For connect_by_association_texture_file_dirs()
# No '/' in the end of the path
MATERIAL_ASSOCIATION_DIRS = ['/Game/Test/Auto/Materials']
# No '/' in the end of the path
TEXTURE_ASSOCIATION_DIRS = ['/Game/Test/Auto/Textures']

# For connect_texture_files_packs()
# No '/' in the end of the path
MATERIAL_PATHS = ['/Game/Test/Auto/Materials/Test.Test']
# No '/' in the end of the path. [[T_Texture_Diff]]
TEXTURE_PATHS_PACKS = [['/Game/Test/Auto/Textures/T_Test_Diff.T_Test_Diff',
                        '/Game/Test/Auto/Textures/T_Test_MetalRough.T_Test_MetalRough',
                        '/Game/Test/Auto/Textures/T_Test_Normal.T_Test_Normal']]

# For connect_textures_files_to_materials()
# No '/' in the end of the path
#MATERIAL_FILES = ['/Game/Test/Auto/Materials/Test.Test']
MATERIAL_FILES = ['/Game/ThirdPerson/Military/Weapon/Modern/Ranged/Firearms/MachineGun/Submachine/Scorpion_61/Materials']
# No '/' in the end of the path
TEXTURE_FILES = ['/Game/Test/Auto/Textures/T_EnglishLavender_Bump.T_EnglishLavender_Bump']

# replace_texture_sample_to_parameters_by_dirs()
# No '/' in the end of the path
MATERIAL_REPLACE_DIRS = ['/Game/Test/Auto/Materials/Replace']

# After all operations done call unreal.MaterialEditingLibrary.recompile_material()
RECOMPILE = False
# After all operations done call unreal.MaterialEditingLibrary.layout_material_expressions()
AUTO_ALIGN = True

LINK_VERSION_BUMP_TEXTURE = 1

MATERIALS_DIRS_FREE_NODES = ['/Game/ThirdPerson/Military/Weapon/Modern/Ranged/Firearms/MachineGun/Submachine/Scorpion_61/Materials']

#======================================================================================