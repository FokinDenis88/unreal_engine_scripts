#====================================Ini Section=======================================
# Plugins must be on and work properly: 'Datasmith glTF Importer', 'glTF Importer'
# Hybrid, Datasmith_glTF_Importer, glTF_Importer, Code4Game, Datasmith_glTF_Importer_Factory     | Default = Hybrid
IMPORT_METHOD = 'Hybrid'

# No '\\' in the end of the path
# Path to fbx and glb files to import
# IMPORT_DIRS, FBX_FILE_NAMES, GLTF_FILE_NAMES, SUBOBJECTS_NAMES - lists must be equal length
# FBX_FILE_NAMES: Name of fbx file without extension

IMPORT_DIRS = [r'K:\!Development K\Projects\3D Models\!!Assets For Commercial\3D\!!3D Models For Commercial\Military\!Weapon\Modern\Ranged\!Firearms\Handgun, Pistol\!Colt\!M1911\Colt M1911___sketchfab\export']
FBX_FILE_NAMES = ['SM_M1911']
#FBX_FILE_NAMES = ['SM']

SUBOBJECTS_NAMES = ['']
#SUBOBJECTS_NAMES = ['SM']
GLTF_FILE_NAMES = ['gltf']


GLB_FILE_NAMES = ['glb']

# Where asset will be stored in unreal project structure
DESTINATION_DIRS = ['/Game/Import']


# Assets will be find in all sub dirs
IS_RECURSIVE_SEARCH = True
ONLY_ON_DISK_ASSETS = False
AUTOMATED = False
SUBOBJECTS_DIR_NAME = 'Subobjects'
#==========================Hybrid pipeline
TO_IMPORT_FBX_MATERIAL_INSTANCE_FILE = False
#HAS_MATERIAL_INSTANCE = False

#===========================================

# Replacing texture samples to texture parameters in Default glTF_Importer import pipeline method
# Many Errors if True
TO_REPLACE_TEXTURE_SAMPLES = False

# Is unnecessary parameter. All compilation is done, when moving folders
TO_RECOMPILE = True

#======================================================================================