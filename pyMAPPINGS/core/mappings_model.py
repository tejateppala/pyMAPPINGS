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
        """
        Initiallize InputModel instance.
        
        Parameters:
        - model_name (str): Used to name the input and output files of MAPPINGS.
        """
        self.log_ = pymap.log_
        self.calling = 'InputModel'
        self.model_name = model_name
        self._validate_model_name()
        self.init_params()
        
    def _validate_model_name(self):
        """Validate the model name."""
        if self.model_name is None:
            raise ValueError("model_name is required!")
        if not isinstance(self.model_name, str):
            raise TypeError("model_name must be a string!")
        if not self.model_name.strip():
            raise ValueError("model_name cannot be empty!")
        
    def init_params(self):
        """
        Initialize model parameters with default values.
        """
        self._abund = None
        self._spec = None
        self._age_index = 9
        self._geometry = "S"
        self._pressure = "6.00"
        self._temperature = "4.00"
        self._filling_factor = "1.0"
        self._logq = "8.00"
        self._step_size = "0.0200"
        self._luminosity = "40.00"
        self._output_path = None
        # Dust parameters
        self._include_dust = True
        self._dust_depl_path = None
        self._pah_fraction = 0.3
        self._pah_switch_value = "4e2"
        self._eval_dust_temp = False
        self._graphite_cospatial = False

    def set_abund(self, path=None):
        """
        Set abundance file path.
        """
        if path is not None and not os.path.exists(path):
            raise FileNotFoundError(f"Abundance file not found: {path}")
        self._abund = path
        return self
        
    def get_abund(self):
        """
        Get current abundance file path.
        """
        return self._abund
        
    def set_dust(self, include_dust=True, depl_path=None, pah_fraction=None, pah_switch_value=None, 
                 eval_dust_temp=None, graphite_cospatial=None):
        """
        Configure dust settings.
        
        Parameters:
        - include_dust (bool): Whether to include dust (default: True)
        - depl_path (str): Path to dust depletion file (required if include_dust=True)
        - pah_fraction (float): Fraction of Carbon Dust Depletion in PAHs (default: 0.3)
        - pah_switch_value (str): PAH switch on value (default: "4e2")
        - eval_dust_temp (bool): Evaluate dust temperatures and IR flux (default: False)
        - graphite_cospatial (bool): Graphite grains cospatial with PAHs (default: False)
        """
        self._include_dust = include_dust
        
        if include_dust and depl_path is None and self._dust_depl_path is None:
            raise ValueError("Dust depletion file path is required when including dust")
        
        if depl_path is not None:
            if not os.path.exists(depl_path):
                raise FileNotFoundError(f"Dust depletion file not found: {depl_path}")
            self._dust_depl_path = depl_path
            
        if pah_fraction is not None:
            if not isinstance(pah_fraction, (int, float)) or not (0 <= pah_fraction <= 1):
                raise ValueError("PAH fraction must be a number between 0 and 1")
            self._pah_fraction = pah_fraction
            
        if pah_switch_value is not None:
            self._pah_switch_value = str(pah_switch_value)
        
        if eval_dust_temp is not None:
            if not isinstance(eval_dust_temp, bool):
                raise TypeError("eval_dust_temp must be a boolean")
            self._eval_dust_temp = eval_dust_temp
        
        if graphite_cospatial is not None:
            if not isinstance(graphite_cospatial, bool):
                raise TypeError("graphite_cospatial must be a boolean")
            self._graphite_cospatial = graphite_cospatial
            
        return self
    
    def enable_dust(self, depl_path, pah_fraction=0.3, pah_switch_value="4e2", 
                    eval_dust_temp=False, graphite_cospatial=False):
        """
        Enable dust with specified depletion file.
        
        Parameters:
        - depl_path (str): Path to dust depletion file
        - pah_fraction (float): Fraction of Carbon Dust Depletion in PAHs (default: 0.3)
        - pah_switch_value (str): PAH switch on value (default: "4e2")
        - eval_dust_temp (bool): Evaluate dust temperatures and IR flux (default: False)
        - graphite_cospatial (bool): Graphite grains cospatial with PAHs (default: False)
        """
        return self.set_dust(True, depl_path, pah_fraction, pah_switch_value, 
                           eval_dust_temp, graphite_cospatial)
    
    def disable_dust(self):
        """Disable dust inclusion."""
        return self.set_dust(False)
    
    def get_dust_settings(self):
        """Get current dust configuration."""
        return {
            'include_dust': self._include_dust,
            'depl_path': self._dust_depl_path,
            'pah_fraction': self._pah_fraction,
            'pah_switch_value': self._pah_switch_value,
            'eval_dust_temp': self._eval_dust_temp,
            'graphite_cospatial': self._graphite_cospatial
        }

    def set_spec(self, path=None):
        """
        Set spectrum file path.
        """
        if path is not None and not os.path.exists(path):
            raise FileNotFoundError(f"Spectrum file not found: {path}")
        self._spec = path
        return self
        
    def get_spec(self):
        """
        Get current spectrum file path.
        """
        return self._spec

    def set_age(self, index=None):
        """
        Set age index.
        
        Parameters:
        - index (int): Age index (default: 9)
        """
        if index is not None:
            if not isinstance(index, int):
                raise TypeError("Age index must be an integer")
            if index < 0:
                raise ValueError("Age index must be non-negative")
        self._age_index = index if index is not None else 9
        return self
        
    def get_age(self):
        """
        Get current age index.
        """
        return self._age_index

    def set_geometry(self, geo=None):
        """
        Set geometry.
        
        Parameters:
        - geo (str): 'S' for spherical, 'P' for plane-parallel (default: 'S')
        """
        if geo is None:
            self._geometry = "S"
        elif isinstance(geo, str) and geo.upper() in {"S", "P"}:
            self._geometry = geo.upper()
        else:
            raise ValueError("Geometry must be 'S' (spherical) or 'P' (plane-parallel)")
        return self
        
    def get_geometry(self):
        """
        Get current geometry.
        """
        return self._geometry
            
    def set_pressure(self, logp=None):
        self._pressure = f"{logp:.2f}" if logp is not None else "6.00"

    def set_temperature(self, logTe=None):
        """
        Set starting electron temperature.
        Electron temperature is a free parameter, not an input parameter for the model.
        
        Parameters:
        - logTe (float): Log electron temperature (default: 4.00)
        """
        if logTe is not None:
            if not isinstance(logTe, (int, float)):
                raise TypeError("Temperature must be a number")
        self._temperature = f"{logTe:.2f}" if logTe is not None else "4.00"
        return self
        
    def get_temperature(self):
        """
        Get starting electron temperature as float.
        """
        return float(self._temperature)

    def set_filling_factor(self, ff=None):
        """
        Set filling factor.
        
        Parameter(s):
        - ff (float): Single value (default: 1.0)
        """
        if ff is not None:
            if not isinstance(ff, (int, float)):
                raise TypeError("Filling factor must be a number")
        self._filling_factor = f"{ff:.2f}" if ff is not None else "1.0"
        return self
            
    def get_filling_factor(self):
        """
        Get current filling factor.
        """
        return self._filling_factor

    def set_ionization_param(self, logq=None):
        self._logq = f"{logq:.2f}" if logq is not None else "8.00"

    def set_step_size(self, step=None):
        """
        Set step size.
        
        Parameters:
        - step (float): Step size (default: 0.02)
        """
        if step is not None:
            if not isinstance(step, (int, float)):
                raise TypeError("Step size must be a number")
            if step <= 0:
                raise ValueError("Step size must be positive")
        self._step_size = f"{step:.4f}" if step is not None else "0.02"
        return self
    
    def set_luminosity(self, logL=None):
        self._luminosity = f"{logL:.2f}" if logL is not None else "40.00"

    def set_output(self, path=None):
        self._output_path = path
        
class MappingsModel(object):
    """
    Read MAPPINGS outputs into a MappingsModel object.
    Output parameters can be accessed by methods. 
    """
    
def run_MAPPINGS():
    """
    Run a MAPPINGS model.
    """
    
def load_models(model_name=None):
    """
    Load outputs of MAPPINGS models.
    """
