Getting Started
===============

Downloading and Installing MAPPINGS V
-------------------------------------

To use **pyMAPPINGS**, you will need a working installation of the 
`MAPPINGS V <https://mappings.anu.edu.au/>`_ photoionization code.

Download the Source Code
------------------------

You can download the current release (v5.2.1) directly from the 
`ANU MAPPINGS archive <https://mappings.anu.edu.au/code/mappings_V-521.zip>`_:

.. code-block:: bash

    wget https://mappings.anu.edu.au/code/mappings_V-521.zip

Unzip the archive:

.. code-block:: bash

    unzip mappings_V-521.zip

Build the Executable
--------------------

Navigate into the extracted folder and run:

.. code-block:: bash

    cd mappings_V-521
    make build

This will compile the MAPPINGS executable (``map52``) in the 
``lab/`` directory.

Test the Build
--------------

To confirm that MAPPINGS has built correctly, run:

.. code-block:: bash

    cd ~/mappings_V-520/lab
    ./map52

If the build was successful, you should see the MAPPINGS interactive prompt.

.. note::
   - You will need a working Fortran compiler (e.g., ``gfortran``) installed on your system.

Installing pyMAPPINGS
---------------------

You can install **pyMAPPINGS** using ``pip``:

.. code-block:: bash

    pip install pymappings

To upgrade to the latest version:

.. code-block:: bash

    pip install --upgrade pymappings


Requirements
------------

- Python 3.8+
- `MAPPINGS V <https://mappings.anu.edu.au/>`_
- `numpy <https://numpy.org/>`_, `pandas <https://pandas.pydata.org/>`_, 
  `matplotlib <https://matplotlib.org/>`_, `scipy <https://scipy.org/>`_, 
  `astropy <https://www.astropy.org/>`_

These dependencies are installed automatically when you install via ``pip``.

