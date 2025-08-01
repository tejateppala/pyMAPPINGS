"""
pyMAPPINGS

teja.teppala@gmail.com
"""
__all__ = ['analysis', 'core', 'io', 'utils']

from .version import __version__

import sys
__pyversion__ = sys.version_info[0]

from .utils.Config import _Config
config = _Config()
log_ = _Config.log_
log_.message('Starting pyMAPPINGS.', calling = 'PyMAPPINGS init')

# from XX import YY, ZZ

log_.message('pyMAPPINGS ready.', calling = 'PyMAPPINGS init')
