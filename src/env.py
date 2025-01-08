#----------------------------------------------------------
# Import
#----------------------------------------------------------
# Standard library
import os
import distutils.util

# Additional library

# Original library

# Other module


#----------------------------------------------------------
# Init
#----------------------------------------------------------


#----------------------------------------------------------
# Get env
#----------------------------------------------------------
TOKEN = os.getenv('TOKEN', None)
GUILD_ID = os.getenv('GUILD_ID', None)
GENERATOR_VC_ID = os.getenv('GENERATOR_VC_ID', None)
VC_NAME = os.getenv('VC_NAME', None)

DEBUG = os.getenv('DEBUG', 'false')


#----------------------------------------------------------
# Validation
#----------------------------------------------------------
if None in (TOKEN, GUILD_ID, GENERATOR_VC_ID, VC_NAME):
    raise Exception('envs was not defined')


#----------------------------------------------------------
# Cast
#----------------------------------------------------------
GUILD_ID = int(GUILD_ID)
GENERATOR_VC_ID = int(GENERATOR_VC_ID)
DEBUG = distutils.util.strtobool(DEBUG)
