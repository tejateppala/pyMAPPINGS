#import pyMAPPINGS as pymap
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
        #self.log_ = pymap.log_
        self.calling = 'InputModel'
        self.model_name = model_name
        self._validate_model_name()
        self.init_params()
        
    def _validate_model_name(self):
        """
        Validate the model name.
        """
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
        self._depl = None
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
        self._allow_grain_destruction = False
        self._grain_distribution = "M"

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
        
    def set_depl(self, path=None):
        """
        Set depletion file path.
        """
        if path is not None and not os.path.exists(path):
            raise FileNotFoundError(f"Depletion file not found: {path}")
        self._depl = path
        return self
        
    def get_depl(self):
        """
        Get current depletion file path.
        """
        return self._depl
        
    def set_dust(self, include_dust=True, depl_path=None, pah_fraction=None, pah_switch_value=None, 
                 eval_dust_temp=None, graphite_cospatial=None, allow_grain_destruction=None, 
                 grain_distribution=None):
        """
        Configure dust settings.
        
        Parameters:
        - include_dust (bool): Whether to include dust (default: True)
        - depl_path (str): Path to dust depletion file (required if include_dust=True)
        - pah_fraction (float): Fraction of Carbon Dust Depletion in PAHs (default: 0.3)
        - pah_switch_value (str): PAH switch on value (default: "4e2")
        - eval_dust_temp (bool): Evaluate dust temperatures and IR flux (default: False)
        - graphite_cospatial (bool): Graphite grains cospatial with PAHs (default: False)
        - allow_grain_destruction (bool): Allow grain destruction (default: False)
        - grain_distribution (str): Grain size distribution - 'M' for MRN, 'K' for KMH, 'W' for WD, 'U' for user-defined (default: 'M')
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
        
        if allow_grain_destruction is not None:
            if not isinstance(allow_grain_destruction, bool):
                raise TypeError("allow_grain_destruction must be a boolean")
            self._allow_grain_destruction = allow_grain_destruction
            
        if grain_distribution is not None:
            valid_distributions = {'M', 'K', 'W', 'U'}
            if not isinstance(grain_distribution, str) or grain_distribution.upper() not in valid_distributions:
                raise ValueError(f"grain_distribution must be one of {valid_distributions} (M=MRN, K=KMH, W=WD, U=user-defined)")
            self._grain_distribution = grain_distribution.upper()
            
        return self
    
    def enable_dust(self, depl_path, pah_fraction=0.3, pah_switch_value="4e2", 
                    eval_dust_temp=False, graphite_cospatial=False, allow_grain_destruction=False,
                    grain_distribution="M"):
        """
        Enable dust with specified depletion file.
        
        Parameters:
        - depl_path (str): Path to dust depletion file
        - pah_fraction (float): Fraction of Carbon Dust Depletion in PAHs (default: 0.3)
        - pah_switch_value (str): PAH switch on value (default: "4e2")
        - eval_dust_temp (bool): Evaluate dust temperatures and IR flux (default: False)
        - graphite_cospatial (bool): Graphite grains cospatial with PAHs (default: False)
        - allow_grain_destruction (bool): Allow grain destruction (default: False)
        - grain_distribution (str): Grain size distribution - 'M' for MRN, 'K' for KMH, 'W' for WD, 'U' for user-defined (default: 'M')
        """
        return self.set_dust(True, depl_path, pah_fraction, pah_switch_value, 
                           eval_dust_temp, graphite_cospatial, allow_grain_destruction, 
                           grain_distribution)
    
    def disable_dust(self):
        """Disable dust inclusion."""
        return self.set_dust(False)
    
    def set_grain_destruction(self, allow=False):
        """
        Set grain destruction option.
        
        Parameters:
        - allow (bool): Whether to allow grain destruction (default: False)
        """
        if not isinstance(allow, bool):
            raise TypeError("allow_grain_destruction must be a boolean")
        self._allow_grain_destruction = allow
        return self
    
    def set_grain_distribution(self, distribution="M"):
        """
        Set grain size distribution.
        
        Parameters:
        - distribution (str): 'M' for MRN, 'K' for KMH, 'W' for WD, 'U' for user-defined (default: 'M')
        """
        valid_distributions = {'M', 'K', 'W', 'U'}
        if not isinstance(distribution, str) or distribution.upper() not in valid_distributions:
            raise ValueError(f"grain_distribution must be one of {valid_distributions} (M=MRN, K=KMH, W=WD, U=user-defined)")
        self._grain_distribution = distribution.upper()
        return self
    
    def get_dust_settings(self):
        """Get current dust configuration."""
        return {
            'include_dust': self._include_dust,
            'depl_path': self._dust_depl_path,
            'pah_fraction': self._pah_fraction,
            'pah_switch_value': self._pah_switch_value,
            'eval_dust_temp': self._eval_dust_temp,
            'graphite_cospatial': self._graphite_cospatial,
            'allow_grain_destruction': self._allow_grain_destruction,
            'grain_distribution': self._grain_distribution
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
        """
        Set log ionization parameter.
        
        Parameters:
        - logq (float): Log ionization parameter (default: 8.00)
        """
        if logq is not None:
            if not isinstance(logq, (int, float)):
                raise TypeError("Ionization parameter must be a number")
        self._logq = f"{logq:.2f}" if logq is not None else "8.00"
        return self
        
    def get_ionization_param(self):
        """Get current ionization parameter as float."""
        return float(self._logq)

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
        """
        Set log luminosity.
        
        Parameters:
        - logL (float): Log luminosity (default: 40.00)
        """
        if logL is not None:
            if not isinstance(logL, (int, float)):
                raise TypeError("Luminosity must be a number")
        self._luminosity = f"{logL:.2f}" if logL is not None else "40.00"
        return self
        
    def get_luminosity(self):
        """
        Get current luminosity as float.
        """
        return float(self._luminosity)

    def set_output(self, path=None):
        """
        Set output path.
        """
        if path is not None:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
        self._output_path = path
        return self
        
    def get_output(self):
        """
        Get current output path.
        """
        return self._output_path
        
    def summary(self):
        """Print a summary of current parameter settings."""
        print(f"MAPPINGS Model: {self.model_name}")
        print(f"  Age index: {self._age_index}")
        print(f"  Geometry: {self._geometry}")
        print(f"  Log Pressure: {self._pressure}")
        print(f"  Log Temperature: {self._temperature}")
        print(f"  Filling Factor: {self._filling_factor}")
        print(f"  Log Ionization Parameter: {self._logq}")
        print(f"  Step Size: {self._step_size}")
        print(f"  Log Luminosity: {self._luminosity}")
        print(f"  Abundance file: {self._abund}")
        print(f"  Depletion file: {self._depl}")
        print(f"  Spectrum file: {self._spec}")
        print(f"  Include dust: {self._include_dust}")
        if self._include_dust:
            print(f"    Dust depletion file: {self._dust_depl_path}")
            print(f"    Allow grain destruction: {self._allow_grain_destruction}")
            print(f"    Grain distribution: {self._grain_distribution}")
            print(f"    PAH fraction: {self._pah_fraction}")
            print(f"    PAH switch value: {self._pah_switch_value}")
            print(f"    Evaluate dust temperatures: {self._eval_dust_temp}")
            print(f"    Graphite grains cospatial: {self._graphite_cospatial}")
        print(f"  Output path: {self._output_path}")
        
    def validate_params(self):
        """Validate all current parameters."""
        errors = []
        
        # Check required files exist if specified
        for attr, name in [('_abund', 'abundance'), ('_depl', 'depletion'), ('_spec', 'spectrum')]:
            path = getattr(self, attr)
            if path is not None and not os.path.exists(path):
                errors.append(f"{name.capitalize()} file not found: {path}")
        
        # Add more validation as needed
        if errors:
            raise ValueError("Parameter validation failed:\n" + "\n".join(errors))
        
        return True
    
    def __repr__(self):
        """String representation of the InputModel."""
        return f"InputModel(model_name='{self.model_name}')"
    
    def __str__(self):
        """User-friendly string representation."""
        return f"MAPPINGS InputModel: {self.model_name}"
    
    def write_input_file(self, filename=None, id_string=None):
        """
        Generate and write the MAPPINGS input file as .mv.
        
        Parameters:
        - filename (str): Output filename (default: {model_name}.mv)
        - id_string (str): Custom ID string for the model (default: auto-generated)
        
        Returns:
        - str: Path to the created input file
        """
        # Define the base directory for saving .mv files
        base_dir = os.path.expanduser("~/mappings520/lab/")
        
        # Set default filename
        if filename is None:
            filename = f"{self.model_name}.mv"
            
        # Full path inside ~/mappings520/lab/
        full_path = os.path.join(base_dir, filename)
        
        # Generate ID string if not provided
        if id_string is None:
            id_string = self._generate_id_string()
        
        # Build the input file content
        content = self._build_input_content(id_string)
        
        # Write to file
        try:
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"Input file written to: {full_path}")
            return full_path
        except IOError as e:
            raise IOError(f"Failed to write input file: {e}")
    
    def _generate_id_string(self):
        """Generate a default ID string based on model parameters."""
        # Extract key parameters for ID
        geo = "SPH" if self._geometry == "S" else "PP"
        age_str = f"t{self._age_index}"
        pressure_str = f"Pk{self._pressure}"
        logq_str = f"Q{self._logq.replace('.', '')}"
        
        return f"{geo}_{self.model_name}_{logq_str}_{pressure_str}_{age_str}"
    
    def _build_input_content(self, id_string):
        """Build the complete input file content."""
        lines = []
        
        # Abundance section
        if self._abund is not None:
            lines.extend([
                "yes   : change abundance",
                self._abund,
                "no    : no more changes"
            ])
        else:
            lines.append("no    : use default abundance")
        
        lines.extend([
            "no    : no offsets",
            "yes   : include dust" if self._include_dust else "no    : include dust"
        ])
        
        if self._include_dust:
            # Depletion section
            if self._depl is not None:
                lines.extend([
                    "yes   : change depletions",
                    self._depl + "\\",
                    "no    : no more changes"
                ])
            else:
                lines.extend([
                    "no    : use default depletions"
                ])
            
            # Grain destruction
            grain_destruction_text = "yes   : allow grain destruction" if self._allow_grain_destruction else "no    : allow grain destruction"
            lines.append(grain_destruction_text)
            
            # Grain distribution
            distribution_map = {
                'M': 'M     : MRN distribution'
                }
            lines.append(distribution_map[self._grain_distribution])
            
            lines.extend([
                "yes   : Include PAH molecules?",
                f"{self._pah_fraction}   : fraction of Carbon Dust Depletion in PAHs",
                "Q     : PAH switch on QHDH < Value",
                f"{self._pah_switch_value}   : PAH switch on Value",
                "yes   : graphite grains to be cospatial with PAHs" if self._graphite_cospatial else "no    : graphite grains to be cospatial with PAHs",
                "yes   : Evaluate dust temperatures and IR flux?" if self._eval_dust_temp else "no    : Evaluate dust temperatures and IR flux?"
            ])
        
        lines.extend([
            "P6    : the main Mappings model to use",
            "D     : Default ionisation values",
            "H     : Input spectral energy distribution data (usually Starburst99)"
        ])
        
        # Spectrum section
        if self._spec is not None:
            lines.append(self._spec)
        else:
            lines.append("Q/inputs/cont_a05t23isp_vm802.spectrum  : default spectrum")
        
        lines.extend([
            f"{self._age_index}     : Age of the HII region. Age = (n-1)*0.5 Myr",
            "X     : eXit with current source"
        ])
        
        # Geometry section
        geo_desc = "Spherical Geometry" if self._geometry == "S" else "Plane parallel geometry"
        lines.append(f"{self._geometry}     : {geo_desc}. (For Plane parallel, 'P', different options)")
        
        lines.extend([
            "L     : Source by Luminosity",
            "T     : Total or Ionising Luminosity",
            f"{self._luminosity}    : bolometric source luminosity (log erg/s)",
            "B     : isoBaric, (const pressure)",
            f"{self._pressure} :  Pressure regime (p/k, <10 as log)",
            f"{self._temperature}     : log(Initial temperature)",
            f"{self._filling_factor}     : filling factor (0<f<=1)",
            "q     : Give initial radius in terms of distance or Q(N) (d/q) ***nb old  options",
            f"{self._logq} :   Q at inner radius (< 100 as log)",
            "y     : Volume integration over the whole sphere? (y/n)",
            "E     : Equilibrium ionization balance.",
            f"{self._step_size}  : Step value of the photon absorption fraction  *******",
            "A     : Ionisation bounded, 99% neutral **********",
            "A   : Standard output",
            f"{id_string} : ID string",
            "X   : end model"
        ])
        
        return '\n'.join(lines) + '\n'
    
    def preview_input_file(self, id_string=None):
        """
        Preview the input file content without writing to disk.
        
        Parameters:
        - id_string (str): Custom ID string for the model (default: auto-generated)
        
        Returns:
        - str: The input file content
        """
        if id_string is None:
            id_string = self._generate_id_string()
        
        content = self._build_input_content(id_string)
        print("Input file preview:")
        print("-" * 50)
        print(content)
        print("-" * 50)
        return content
        
    def run_mappings(self, input_file=None):
        """
        Run the MAPPINGS V executable on the given input .mv file.

        Parameters:
        - input_file (str): Path to the input .mv file. If None, will use default from ~/mappings520/lab/{model_name}.mv
        """
        lab_dir = os.path.expanduser("~/mappings520/lab/")
        exe_path = os.path.join(lab_dir, "map52")
        
        if not os.path.isfile(exe_path):
            raise FileNotFoundError(f"MAPPINGS executable not found: {exe_path}")

        # If no input file specified, use default in lab_dir
        if input_file is None:
            input_file = os.path.join(lab_dir, f"{self.model_name}.mv")
        
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
            
        # Run MAPPINGS with input redirection
        try:
            result = subprocess.run(
                [exe_path],
                input=open(input_file, 'r').read(),
                text=True,
                cwd=lab_dir,
                capture_output=True
            )
        except Exception as e:
            raise RuntimeError(f"Error running MAPPINGS: {e}")

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
