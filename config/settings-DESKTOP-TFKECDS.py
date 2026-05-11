"""
Main Django settings file for Job Portal Backend API.
This file imports environment-specific settings based on the ENVIRONMENT variable.
"""

import os
from pathlib import Path

# Get environment from environment variable
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Import appropriate settings based on environment
if ENVIRONMENT == 'production':
    from .settings_prod import *
else:
    from .settings_dev import *

