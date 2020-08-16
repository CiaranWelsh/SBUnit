.. SBUnit documentation master file, created by
   sphinx-quickstart on Sun Aug 16 13:57:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SBUnit's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

SBUnit is a prototype for unit testing models encoded in SBML.


Installing
==========

SBunit is not available on pip: it is too early days for that. Instead you
should clone the sources:

.. code-block:: bash

   git clone https://github.com/CiaranWelsh/SBUnit.git
   cd SBUnit

And run `setup.py`

.. code-block:: bash

   python setup.py install

This will install SBUnit into the `site-packages` directory of the currently active
Python environment.

Examples
========

.. literalinclude:: example_scripts/test_simple_model.py
   :linenos:
   :language: python
   :caption: Create a single annotation in Python




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
