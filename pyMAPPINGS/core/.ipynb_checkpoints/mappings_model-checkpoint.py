import pyMAPPINGS as pymap
import numpy as np
import glob
import os
import subprocess
import random
import time
import re

class InputModel(object):
    """
    Object used to create and write input file for MAPPINGS.
    """
    def __init__(self, model_name = None):
        self.calling = 'InputModel'
        self.model_name = model_name
        self.init_params()
        
    def init_params(self):
        self.set_abund()
        self.set_depl()
        self.set_spec()
        self.set_age()
        self.set_geometry()
        self.set_pressure()
        self.set_temperature()
        self.set_filling_factor()
        self.set_ionization_param()
        self.set_step_size()
        self.set_luminosity()
        self.set_output()

    def set_abund(self, path=None):
        self._abund = path

    def set_depl(self, path=None):
        self._depl = path

    def set_spec(self, path=None):
        self._spec = path

    def set_age(self, index=None):
        self._age_index = index if index is not None else 9

    def set_geometry(self, geo=None):
        if geo is None:
            self._geometry = "S"
        elif geo.upper() in {"S", "P"}:
            self._geometry = geo.upper()
        else:
            raise ValueError("Geometry must be 'S' (spherical) or 'P' (plane-parallel)")
            
    def set_pressure(self, logp=None):
        self._pressure = f"{logp:.2f}" if logp is not None else "6.00"

    def set_temperature(self, logTe=None):
        self._temperature = f"{logTe:.2f}" if logTe is not None else "4.00"

    def set_filling_factor(self, ff=None):
        if ff is None:
            self._filling_factor = "1.0"
        elif isinstance(ff, (tuple, list)):
            self._filling_factor = f"{ff[0]:.2f} {ff[1]:.2f}"
        else:
            self._filling_factor = f"{ff:.2f}"

    def set_ionization_param(self, logq=None):
        self._logq = f"{logq:.2f}" if logq is not None else "8.00"

    def set_step_size(self, step=None):
        self._step_size = f"{step:.4f}" if step is not None else "0.0200"
    
    def set_luminosity(self, logL=None):
        self._luminosity = f"{logL:.2f}" if logL is not None else "40.00"

    def set_output(self, path=None):
        self._output_path = path
        
class MappingsModel(object):
    """
    Read MAPPINGS outputs into a MappingsModel object.
    """
    
def run_MAPPINGS():
    """
    Run a MAPPINGS model.
    """
    
def load_models(model_name=None):
    """
    Load outputs of MAPPINGS models.
    """
