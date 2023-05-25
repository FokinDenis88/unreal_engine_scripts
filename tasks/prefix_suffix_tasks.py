import os
import sys
WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.join(os.path.join(WORKING_DIR, os.pardir), os.pardir)
# Folder, that stores unreal_scripts package
sys.path.append(os.path.abspath(PARENT_DIR))


#import unreal_scripts.config as config
import unreal_scripts.src.prefix_suffix as prefix_suffix
import unreal_scripts.tasks.prefix_suffix_tasks_ini as prefix_suffix_tasks_ini

import importlib
#importlib.reload(config)
importlib.reload(prefix_suffix)
importlib.reload(prefix_suffix_tasks_ini)

from unreal_scripts.tasks.prefix_suffix_tasks_ini import *


def main():
    if COMMAND == 'Add':
        prefix_suffix.add_prefix_suffix_folder(TARGET_PATHS, PREFIX, SUFFIX, IS_RECURSIVE_SEARCH, ONLY_ON_DISK_ASSETS)
    elif COMMAND == 'Delete':
        prefix_suffix.delete_prefix_suffix_folder(TARGET_PATHS, PREFIX, SUFFIX, IS_RECURSIVE_SEARCH, ONLY_ON_DISK_ASSETS)
    elif COMMAND == 'Replace':
        prefix_suffix.replace_prefix_suffix_folder(TARGET_PATHS, PREFIX, SUFFIX, NEW_PREFIX, NEW_SUFFIX,
                                                   IS_RECURSIVE_SEARCH, ONLY_ON_DISK_ASSETS)
    elif COMMAND == 'Correct':
        prefix_suffix.correct_prefix_suffix_folder(TARGET_PATHS, IS_RECURSIVE_SEARCH, ONLY_ON_DISK_ASSETS)
    elif COMMAND == 'DeleteGLBIndex':
        prefix_suffix.delete_glb_texture_prefix_folder(TARGET_PATHS, IS_RECURSIVE_SEARCH, ONLY_ON_DISK_ASSETS)


main()

#unreal.log(os.path.basename('/Game/ThirdPerson/Military/Vehicle/Modern/Land/Tank/T-90_02/Textures/T_s35-703.T_s35-703'))
#base_name = os.path.basename('/Game/ThirdPerson/Military/Vehicle/Modern/Land/Tank/T-90_02/Textures/application.exe')
#unreal.log(base_name)
#unreal.log(os.path.splitext(base_name)[0])
#unreal.log(os.path.dirname('/Game/ThirdPerson/Military/Vehicle/Modern/Land/Tank/T-90_02/Textures/T_s35-703.T_s35-703'))