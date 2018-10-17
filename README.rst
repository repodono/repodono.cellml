repodono.cellml
===============

Helpers for interacting with CellML for the repodono framework.

Installation
------------

This package depends on a Python package that links to a C++ library
through a custom interface, this makes the installation process a lot
more difficult.  In order to simplify this process, any package that
require this will need to make use of ``zc.buildout`` on the accompanied
``buildout.cfg`` file to build the cellml-api, and then use a separate
process to install the ``cgrspy`` package which this package depends
upon.

Roughly speaking, this may be done inside a virtualenv like so:

.. code:: console

    $ virtualenv env
    Running virtualenv with interpreter /usr/bin/python3.6
    Using base prefix '/usr'
    ...
    $ source env/bin/activate
    $ pip install zc.buildout
    Collecting zc.buildout
    ...
    Successfully installed zc.buildout-2.12.2
    $ buildout
    ...
    Installing cellml-api.
    ...
    $ pip install -I \
        --global-option="build_ext" \
        --global-option="-I$(pwd)/parts/cellml-api/include" \
        --global-option="-L$(pwd)/parts/cellml-api/lib:$(pwd)/parts/cellml-api/lib/cgrs_modules" \
        --global-option="-R$(pwd)/parts/cellml-api/lib:$(pwd)/parts/cellml-api/lib/cgrs_modules" \
        cgrspy
    Collecting cgrspy
    ...
    Skipping bdist_wheel for cgrspy, due to binaries being disabled for it.
    Installing collected packages: cgrspy
      Running setup.py install for cgrspy ... done
    Successfully installed cgrspy-1.2.0

The final ``pip install`` step must pass the ``build_ext`` options using
the ``--global-option`` of ``pip`` such that the compilation process
will produce the correct shared object files so that cgrspy will
function correctly inside the virtual environment using the libraries
compiled using ``zc.buildout``.

Demo
----

Given the brand new state of this library without anything implemented,
this is mostly a testbed for ideas on how a standalone Python <-> CellML
API (legacy version) can be integrated without too much external and/or
unrelated dependencies.  To show that the built ``cgrspy`` will function
as expected, try:

.. code:: console

    $ pip install requests
    ...
    $ python

Inside the Python shell the following imports and code should function
like so:

.. code:: python

    >>> import requests
    >>> import cgrspy.bootstrap
    >>> modelstr = requests.get('https://models.physiomeproject.org/workspace/beeler_reuter_1977/@@rawfile/cb090c96a2ce627457b14def4910ac39219b8340/beeler_reuter_1977.cellml').text
    >>> cgrspy.bootstrap.loadGenericModule('cgrs_cellml')
    >>> cellml_bootstrap = cgrspy.bootstrap.fetch('CreateCellMLBootstrap')
    >>> cgrspy.bootstrap.loadGenericModule('cgrs_celedsexporter')
    >>> celedsexporter_bootstrap = cgrspy.bootstrap.fetch(
    ...     'CreateCeLEDSExporterBootstrap')
    >>> exporter = celedsexporter_bootstrap.createExporterFromText(requests.get(
    ...     'https://raw.githubusercontent.com/PMR2/cellml.api.pmr2/master/cellml/api/pmr2/resource/celeds/Python.xml').text)
    >>> model = cellml_bootstrap.modelLoader.createFromText(modelstr)
    >>> src = exporter.generateCode(model)
    >>> len(src)
    10900
    >>> print(src[0:220])
    # Size of variable arrays:
    sizeAlgebraic = 18
    sizeStates = 8
    sizeConstants = 10
    from math import *
    from numpy import *

    def createLegends():
        legend_states = [""] * sizeStates
        legend_rates = [""] * sizeStates
