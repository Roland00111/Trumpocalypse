.. Trumpocalypse documentation master file, created by
   sphinx-quickstart on Mon Mar 13 22:39:39 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Trumpocalypse's documentation!
=========================================

Documentation
=============
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   code

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

To make this documentation...
-----------------------------

::

 # Create a venv and activate it.

 $ virtualenv venv && source ../venv/bin/activate

 # Clone github project and cd into it.

 $ git clone https://github.com/Roland00111/Trumpocalypse

 $ cd ./Trumpocalypse

 # Mock is for sphinx to work with pygame.
 # See: https://github.com/ntasfi/PyGame-Learning-Environment/blob/master/docs/conf.py
 # And: https://github.com/rtfd/readthedocs.org/issues/2511

 $ pip install pygame sphinx mock

 # If this is the first run of sphinx, make a docs folder and run quickstart.
 # Otherwise, jump ahead to the section "sphinx-build" below.

 $ mkdir docs && cd docs

 # Run sphinx-quickstart.

 $ ../../venv/bin/sphinx-quickstart

+----------------------------------------------------------------------------------------+--------------+ 
|Prompt	                                                                                 | Choice       |
+========================================================================================+==============+
|> Root path for the documentation [.]:	                                                 | <ENTER>      |
+----------------------------------------------------------------------------------------+--------------+ 
|> Separate source and build directories (y/N) [n]:	                                 | y            |
+----------------------------------------------------------------------------------------+--------------+ 
|> Name prefix for templates and static dir [_]:	                                 | <ENTER>      |
+----------------------------------------------------------------------------------------+--------------+ 
|> Project name:	                                                                 | Trumpocalypse|
+----------------------------------------------------------------------------------------+--------------+ 
|> Author name(s):	                                                                 | RNJDM        |
+----------------------------------------------------------------------------------------+--------------+ 
|> Project version:	                                                                 | 1.0          |
+----------------------------------------------------------------------------------------+--------------+ 
|> Project release [0.0.1]:	                                                         | <ENTER>      |
+----------------------------------------------------------------------------------------+--------------+ 
|> Source file suffix [.rst]:	                                                         | <ENTER>      |
+----------------------------------------------------------------------------------------+--------------+ 
|> Name of your master document (without suffix) [index]:	                         | <ENTER>      |
+----------------------------------------------------------------------------------------+--------------+ 
|> autodoc: automatically insert docstrings from modules (y/N) [n]:	                 | y            |
+----------------------------------------------------------------------------------------+--------------+ 
|> doctest: automatically test code snippets in doctest blocks (y/N) [n]:	         | n            |
+----------------------------------------------------------------------------------------+--------------+ 
|> intersphinx: link between Sphinx documentation of different projects (y/N) [n]:	 | y            |
+----------------------------------------------------------------------------------------+--------------+ 
|> todo: write “todo” entries that can be shown or hidden on build (y/N) [n]:	         | n            |
+----------------------------------------------------------------------------------------+--------------+ 
|> coverage: checks for documentation coverage (y/N) [n]:	                         | n            |
+----------------------------------------------------------------------------------------+--------------+ 
|> pngmath: include math, rendered as PNG images (y/N) [n]:	                         | n            |
+----------------------------------------------------------------------------------------+--------------+ 
|> jsmath: include math, rendered in the browser by JSMath (y/N) [n]:	                 | n            |
+----------------------------------------------------------------------------------------+--------------+ 
|> ifconfig: conditional inclusion of content based on config values (y/N) [n]:	         | y            |
+----------------------------------------------------------------------------------------+--------------+ 
|> Create Makefile? (Y/n) [y]:	                                                         | n            |
+----------------------------------------------------------------------------------------+--------------+ 
|> Create Windows command file? (Y/n) [y]:	                                         | n            |
+----------------------------------------------------------------------------------------+--------------+ 

| # To conf.py add parent folder containing the code to document.
| # Also add mock.

::

 import os
 import sys
 import pygame
 from mock import Mock
 sys.modules['pygame'] = Mock()
 sys.modules['pygame.constants'] = Mock()
 sys.path.insert(0, os.path.abspath('../UI/'))

| # Add code.rst with the following modules to document:

::

  Code Documentation
  ==================

  .. automodule:: Trumpocalypse
     :members:
     :undoc-members:
  
  .. automodule:: PygameUI
     :members:
     :undoc-members:
  
  .. automodule:: TextWrap
     :members:
     :undoc-members:
  
  .. automodule:: colors
     :members:
     :undoc-members:

| # Then add the rst file code.rst to index.rst.

::

 Documentation
 =============
 .. toctree::
    :maxdepth: 2
    :caption: Contents: 

    code

sphinx-build
------------

| # In Trumpocalypse.py comment out any reference to the game initializer
| # outside of `if __name__ == '__main__':`.
| # Outside of `__main__` there should be no instantiation of a class that
| # would normally signify the start of the program.
| # Build with sphinx-build, deactivate the virtualenv, and push.

::

 $ ../../venv/bin/sphinx-build -b html . ./_build

 $ deactivate

 $ git add -A; git commit -m ''; git push;

| # Finally, visit readthedocs.io to build the documentation there.

