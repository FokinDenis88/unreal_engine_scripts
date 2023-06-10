import unreal
import unreal_engine_scripts.config as config

import importlib
importlib.reload(config)

#====================================Ini Section=======================================
# Commands: Add, Delete, Replace, Correct, DeleteGLBIndex
COMMAND = 'Correct'

# No '/' in the end of the path
TARGET_PATHS = ['/Game/ThirdPerson/Military/Vehicle/Modern/Land/Tank/T-90_02/Textures/Test']
#TARGET_PATHS = ['/Game/ThirdPerson/Military/Vehicle/Modern/Land/Tank/T-90_02/Textures']
#TARGET_PATHS = ['/Game/ThirdPerson']

# Write all prefix, suffix With Separator underscore _
PREFIX = 'SM_'
SUFFIX = ''

# For Replace Command
NEW_PREFIX = ''
NEW_SUFFIX = ''

# Assets will be find in all sub dirs
IS_RECURSIVE_SEARCH = True
ONLY_ON_DISK_ASSETS = False

#======================================================================================