"""
pyMAPPINGS is a Python library for the [MAPPINGS V](https://mappings.anu.edu.au/) photoionization and shock modeling code. It simplifies the process of running models, parsing output, and visualizing results — all from Python.

teja.teppala@gmail.com
"""
__all__ = ['analysis', 'core']

from .version import __version__

import sys
__pyversion__ = sys.version_info[0]

from .utils.Config import _Config
config = _Config()
log_ = _Config.log_
log_.message('Starting pyMAPPINGS.', calling = 'PyMAPPINGS init')

# from XX import YY, ZZ
from .core import *
from .analysis import *

log_.message('pyMAPPINGS ready.', calling = 'PyMAPPINGS init')
