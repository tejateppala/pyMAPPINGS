#import pyMAPPINGS as pymap
#import numpy as np
#import glob
import os
import subprocess
#import random
import time
#import re

class InputModel(object):
    """Object used to create and write input files for MAPPINGS V photoionization models.
    
    The InputModel class provides a comprehensive interface for configuring and generating
    MAPPINGS V input files. It handles all model parameters including abundance files,
    depletion patterns, dust properties, stellar spectra, and physical conditions.
    
    Attributes:
        model_name (str): Name used for input and output files.
        calling (str): Identifier for the calling class.
    """
    def __init__(self, model_name = None):
        """Initialize InputModel instance.
        
        Args:
            model_name (str, optional): Used to name the input and output files of MAPPINGS.
                Must be a non-empty string.
                
        Raises:
            ValueError: If model_name is None or empty.
            TypeError: If model_name is not a string.
        """
        self.calling = 'InputModel'
        self.model_name = model_name
        self._validate_model_name()
        self.init_params()
        
    def _validate_model_name(self):
        """Validate the model name.
        
        Raises:
            ValueError: If model_name is None or empty string.
            TypeError: If model_name is not a string.
        """
        if self.model_name is None:
            raise ValueError("model_name is required!")
        if not isinstance(self.model_name, str):
            raise TypeError("model_name must be a string!")
        if not self.model_name.strip():
            raise ValueError("model_name cannot be empty!")
        
    def init_params(self):
        """Initialize model parameters with default values.
        
        Sets up default values for all MAPPINGS V model parameters including:
        physical conditions, dust properties, file paths, and numerical settings.
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
        """"""Set abundance file path.
        
        Args:
            path (str, optional): Path to abundance file. If None, uses MAPPINGS default.
                File must exist if specified.
            
        Raises:
            FileNotFoundError: If specified file does not exist.
        """
        if path is not None and not os.path.exists(path):
            raise FileNotFoundError(f"Abundance file not found: {path}")
        self._abund = path
        
    def get_abund(self):
        """Get current abundance file path.
        
        Returns:
            str or None: Current abundance file path, or None if using default.
        """
        return self._abund
        
    def set_depl(self, path=None):
        """Set depletion file path.
        
        Args:
            path (str, optional): Path to depletion file. If None, uses MAPPINGS default.
                File must exist if specified.
            
        Raises:
            FileNotFoundError: If specified file does not exist.
        """
        if path is not None and not os.path.exists(path):
            raise FileNotFoundError(f"Depletion file not found: {path}")
        self._depl = path
        
    def get_depl(self):
        """Get current depletion file path.
        
        Returns:
            str or None: Current depletion file path, or None if using default.
        """
        return self._depl
        
    def set_dust(self, include_dust=True, depl_path=None, pah_fraction=None, pah_switch_value=None, 
                 eval_dust_temp=None, graphite_cospatial=None, allow_grain_destruction=None, 
                 grain_distribution=None):
        """Configure dust settings.
        
        Comprehensive method to configure all dust-related parameters in one call.
        
        Args:
            include_dust (bool, optional): Whether to include dust. Defaults to True.
            depl_path (str, optional): Path to dust depletion file. Required if include_dust=True
                and no previous dust depletion path has been set.
            pah_fraction (float, optional): Fraction of Carbon Dust Depletion in PAHs. 
                Must be between 0 and 1. Defaults to 0.3.
            pah_switch_value (str, optional): PAH switch on value. Defaults to "4e2".
            eval_dust_temp (bool, optional): Evaluate dust temperatures and IR flux. 
                Defaults to False.
            graphite_cospatial (bool, optional): Graphite grains cospatial with PAHs. 
                Defaults to False.
            allow_grain_destruction (bool, optional): Allow grain destruction. Defaults to False.
            grain_distribution (str, optional): Grain size distribution - 'M' for MRN, 
                'P' for Power law N(a) = k a^alpha, 'S' for Grain Shattering Profile. Defaults to 'M'.
            
        Raises:
            ValueError: If include_dust=True but no depletion path is provided, or if
                PAH fraction is not between 0 and 1, or if grain_distribution is invalid.
            FileNotFoundError: If dust depletion file does not exist.
            TypeError: If boolean parameters are not boolean type.
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
            valid_distributions = {'M', 'P', 'S'}
            if not isinstance(grain_distribution, str) or grain_distribution.upper() not in valid_distributions:
                raise ValueError(f"grain_distribution must be one of {valid_distributions} (M=MRN, P=Powerlaw, S=Grain Shattering Profile)")
            self._grain_distribution = grain_distribution.upper()
    
    def enable_dust(self, depl_path, pah_fraction=0.3, pah_switch_value="4e2", 
                    eval_dust_temp=False, graphite_cospatial=False, allow_grain_destruction=False,
                    grain_distribution="M"):
        """Enable dust with specified depletion file and optional parameters.
        
        Convenience method that calls set_dust with include_dust=True.
        
        Args:
            depl_path (str): Path to dust depletion file. Must exist.
            pah_fraction (float, optional): Fraction of Carbon Dust Depletion in PAHs. 
                Defaults to 0.3.
            pah_switch_value (str, optional): PAH switch on value. Defaults to "4e2".
            eval_dust_temp (bool, optional): Evaluate dust temperatures and IR flux. 
                Defaults to False.
            graphite_cospatial (bool, optional): Graphite grains cospatial with PAHs. 
                Defaults to False.
            allow_grain_destruction (bool, optional): Allow grain destruction. Defaults to False.
            grain_distribution (str, optional): Grain size distribution - 'M' for MRN, 
                'P' for Power law N(a) = k a^alpha, 'S' for Grain Shattering Profile. Defaults to 'M'.
            
        Raises:
            ValueError: If PAH fraction invalid or grain distribution invalid.
            FileNotFoundError: If dust depletion file does not exist.
            TypeError: If boolean parameters are not boolean type.
        """
        return self.set_dust(True, depl_path, pah_fraction, pah_switch_value, 
                           eval_dust_temp, graphite_cospatial, allow_grain_destruction, 
                           grain_distribution)
    
    def disable_dust(self):
        """Disable dust inclusion."""
        return self.set_dust(False)
    
    def set_grain_destruction(self, allow=False):
        """Set grain destruction option.
        
        Args:
            allow (bool, optional): Whether to allow grain destruction. Defaults to False.
            
        Raises:
            TypeError: If allow is not a boolean.
        """
        if not isinstance(allow, bool):
            raise TypeError("allow_grain_destruction must be a boolean")
        self._allow_grain_destruction = allow
    
    def set_grain_distribution(self, distribution="M"):
        """Set grain size distribution.
        
        Args:
            distribution (str, optional): Grain size distribution type. Options are:
                'M' for MRN (Mathis, Rumpl & Nordsieck)
                'P' for Power law N(a) = k a^alpha
                'S' for Grain Shattering Profile
                Defaults to 'M'.
            
        Raises:
            ValueError: If distribution is not one of the valid options.
        """
        valid_distributions = {'M', 'P', 'S'}
        if not isinstance(distribution, str) or distribution.upper() not in valid_distributions:
            raise ValueError(f"grain_distribution must be one of {valid_distributions} (M=MRN, P=Powerlaw, S=Grain Shattering Profile)")
        self._grain_distribution = distribution.upper()
    
    def get_dust_settings(self):
        """Get current dust configuration as a dictionary.
        
        Returns:
            dict: Dictionary containing all current dust settings with keys:
                'include_dust', 'depl_path', 'pah_fraction', 'pah_switch_value',
                'eval_dust_temp', 'graphite_cospatial', 'allow_grain_destruction',
                'grain_distribution'.
        """
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
        """Set spectrum file path.
        
        Args:
            path (str, optional): Path to spectrum file. If None, uses MAPPINGS default.
                File must exist if specified.
            
        Raises:
            FileNotFoundError: If specified file does not exist.
        """
        if path is not None and not os.path.exists(path):
            raise FileNotFoundError(f"Spectrum file not found: {path}")
        self._spec = path
        
    def get_spec(self):
        """Get current spectrum file path.
        
        Returns:
            str or None: Current spectrum file path, or None if using default.
        """
        return self._spec

    def set_age(self, index=None):
        """Set age index for stellar population.
        
        The age in Myr is calculated as (index-1) * 0.5 Myr.
        
        Args:
            index (int, optional): Age index. Must be non-negative integer. 
                Defaults to 9 (corresponding to 4.0 Myr).
            
        Raises:
            TypeError: If index is not an integer.
            ValueError: If index is negative.
        """
        if index is not None:
            if not isinstance(index, int):
                raise TypeError("Age index must be an integer")
            if index < 0:
                raise ValueError("Age index must be non-negative")
        self._age_index = index if index is not None else 9
        
    def get_age(self):
        """Get current age index.
        
        Returns:
            int: Current age index.
        """
        return self._age_index

    def set_geometry(self, geo=None):
        """Set model geometry.
        
        Args:
            geo (str, optional): Geometry type. Options are:
                'S' for spherical geometry
                'P' for plane-parallel geometry
                Defaults to 'S'.
            
        Raises:
            ValueError: If geometry is not 'S' or 'P'.
        """
        if geo is None:
            self._geometry = "S"
        elif isinstance(geo, str) and geo.upper() in {"S", "P"}:
            self._geometry = geo.upper()
        else:
            raise ValueError("Geometry must be 'S' (spherical) or 'P' (plane-parallel)")
        
    def get_geometry(self):
        """Get current geometry setting.
        
        Returns:
            str: Current geometry ('S' or 'P').
        """
        return self._geometry
            
    def set_pressure(self, logp=None):
        """Set log pressure (p/k).
        
        Args:
            logp (float, optional): Log pressure in units of p/k. Defaults to 6.00.
        """
        self._pressure = f"{logp:.2f}" if logp is not None else "6.00"

    def get_pressure(self):
        """Get current log pressure as float.
        
        Returns:
            float: Current log pressure.
        """
        return float(self._pressure)

    def set_temperature(self, logTe=None):
        """Set starting electron temperature.
        
        Note:
            Electron temperature is a free parameter, not a fixed input parameter 
            for the model. This sets the initial guess value.
        
        Args:
            logTe (float, optional): Log electron temperature in K. Defaults to 4.00.
            
        Raises:
            TypeError: If logTe is not a number.
        """
        if logTe is not None:
            if not isinstance(logTe, (int, float)):
                raise TypeError("Temperature must be a number")
        self._temperature = f"{logTe:.2f}" if logTe is not None else "4.00"
        
    def get_temperature(self):
        """Get starting electron temperature as float.
        
        Returns:
            float: Starting electron temperature (log K).
        """
        return float(self._temperature)

    def set_filling_factor(self, ff=None):
        """Set filling factor.
        
        Args:
            ff (float, optional): Filling factor, must be between 0 and 1. 
                Represents the volume fraction filled by ionized gas. Defaults to 1.0.
            
        Raises:
            TypeError: If ff is not a number.
        """
        if ff is not None:
            if not isinstance(ff, (int, float)):
                raise TypeError("Filling factor must be a number")
        self._filling_factor = f"{ff:.2f}" if ff is not None else "1.0"
            
    def get_filling_factor(self):
        """Get current filling factor.
        
        Returns:
            str: Current filling factor as string.
        """
        return self._filling_factor

    def set_ionization_param(self, logq=None):
        """Set log ionization parameter.
        
        The ionization parameter is defined as the ratio of ionizing photon 
        density to hydrogen density.
        
        Args:
            logq (float, optional): Log ionization parameter. Defaults to 8.00.
            
        Returns:
            InputModel: Returns self for method chaining.
            
        Raises:
            TypeError: If logq is not a number.
        """
        if logq is not None:
            if not isinstance(logq, (int, float)):
                raise TypeError("Ionization parameter must be a number")
        self._logq = f"{logq:.2f}" if logq is not None else "8.00"
        
    def get_ionization_param(self):
        """Get current ionization parameter as float.
        
        Returns:
            float: Current log ionization parameter.
        """
        return float(self._logq)

    def set_step_size(self, step=None):
        """Set step size for photon absorption fraction.
        
        Args:
            step (float, optional): Step value of the photon absorption fraction.
                Must be positive. Defaults to 0.02.
            
        Raises:
            TypeError: If step is not a number.
            ValueError: If step is not positive.
        """
        if step is not None:
            if not isinstance(step, (int, float)):
                raise TypeError("Step size must be a number")
            if step <= 0:
                raise ValueError("Step size must be positive")
        self._step_size = f"{step:.4f}" if step is not None else "0.02"
    
    def get_step_size(self):
        """Get current step size as float.
        
        Returns:
            float: Current step size.
        """
        return float(self._step_size)

    def set_luminosity(self, logL=None):
        """Set log bolometric luminosity.
        
        Args:
            logL (float, optional): Log bolometric source luminosity in erg/s. 
                Defaults to 40.00.

        Raises:
            TypeError: If logL is not a number.
        """
        if logL is not None:
            if not isinstance(logL, (int, float)):
                raise TypeError("Luminosity must be a number")
        self._luminosity = f"{logL:.2f}" if logL is not None else "40.00"
        
    def get_luminosity(self):
        """Get current luminosity as float.
        
        Returns:
            float: Current log luminosity in erg/s.
        """
        return float(self._luminosity)

    def set_output(self, path=None):
        """Set output path for model results.
        
        Args:
            path (str, optional): Output directory path. Directory will be created
                if it doesn't exist.
        """
        if path is not None:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(path), exist_ok=True)
        self._output_path = path
        
    def get_output(self):
        """Get current output path.
        
        Returns:
            str or None: Current output path, or None if not set.
        """
        return self._output_path
        
    def summary(self):
        """Print a summary of current parameter settings.
        
        Displays all current model parameters in a formatted table for easy review.
        """
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
        """Validate all current parameters for consistency and file existence.
        
        Returns:
            bool: True if all parameters are valid.
            
        Raises:
            ValueError: If any parameter validation fails, with details of all errors.
        """
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
        """String representation of the InputModel.
        
        Returns:
            str: Formal string representation suitable for debugging.
        """
        return f"InputModel(model_name='{self.model_name}')"
    
    def __str__(self):
        """User-friendly string representation.
        
        Returns:
            str: Human-readable description of the model.
        """
        return f"MAPPINGS InputModel: {self.model_name}"
    
    def write_input_file(self, filename=None, id_string=None):
        """Generate and write the MAPPINGS input file as .mv format.
        
        Creates a complete MAPPINGS V input file based on current parameter settings
        and writes it to the specified location.
        
        Args:
            filename (str, optional): Output filename. Defaults to {model_name}.mv.
            id_string (str, optional): Custom ID string for the model. If None,
                auto-generates based on model parameters.
                
        Returns:
            str: Path to the created input file.
            
        Raises:
            IOError: If file cannot be written.
            
        Example:
            >>> model = InputModel("test_model")
            >>> model.set_pressure(6.5)
            >>> filepath = model.write_input_file()
            Input file written to: ~/mappings520/lab/test_model.mv
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
        """Generate a default ID string based on model parameters.
        
        Returns:
            str: Auto-generated ID string incorporating key model parameters.
        """
        # Extract key parameters for ID
        geo = "SPH" if self._geometry == "S" else "PP"
        age_str = f"t{self._age_index}"
        pressure_str = f"Pk{self._pressure}"
        logq_str = f"Q{self._logq.replace('.', '')}"
        
        return f"{geo}_{self.model_name}_{logq_str}_{pressure_str}_{age_str}"
    
    def _build_input_content(self, id_string):
        """Build the complete input file content.
        
        Args:
            id_string (str): ID string to include in the input file.
            
        Returns:
            str: Complete input file content formatted for MAPPINGS V.
        """
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
        """Preview the input file content without writing to disk.
        
        Useful for checking the generated input file content before committing to disk.
        
        Args:
            id_string (str, optional): Custom ID string for the model. If None,
                auto-generates based on model parameters.
                
        Returns:
            str: The input file content that would be written.
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
        """Run the MAPPINGS V executable on the given input .mv file.

        Executes the MAPPINGS V photoionization code using the current model
        configuration. Requires that MAPPINGS V is properly installed.

        Args:
            input_file (str, optional): Path to the input .mv file. If None, 
                uses default path ~/mappings520/lab/{model_name}.mv
                
        Raises:
            FileNotFoundError: If MAPPINGS executable or input file not found.
            RuntimeError: If MAPPINGS execution fails.
            
        Note:
            This method requires MAPPINGS V to be installed in ~/mappings520/lab/
            with the executable named 'map52'.
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
            
        # Run MAPPINGS
        try:
            start_time = time.time()
            print(f"Running MAPPINGS model '{self.model_name}'...")
            result = subprocess.run(
                [exe_path],
                input=open(input_file, 'r').read(),
                text=True,
                cwd=lab_dir,
                capture_output=True
            )
            
            end_time = time.time()
            elapsed = end_time - start_time
            minutes, seconds = divmod(elapsed, 60)

            print(f"MAPPINGS model '{self.model_name}' successfully run in {int(minutes)}m {seconds:.2f}s")

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
