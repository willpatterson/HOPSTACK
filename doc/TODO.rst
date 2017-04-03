.. TODO.rst

LASDI:
======

- Test
- Implement network protocols
- Implement DISS parameters
- Implement Raw data interpretation
  * pipes and redirects
  * raw strings via command line
  * Address file path regex filtering vs file content regex filtering
- Build modules for parsing and interpreting JSON/YAML strings

LAS Output Formatter LASOF:
===========================

Not sure if this is going to be nessesary.

LASubway:
=========

General:
--------

- Create definite metro structure
- Create mechinism to run pipeline
  - with installed LASubway scripts
  - with standalone .sh script created by LASubway when building Metro

- Define, Outline and Document the Station Input (sin) file format

Documentation:
--------------

- Create a project wiki on github and move techincal from README

Text Structure Representation:
------------------------------

- Write resize fucntion for Box class
- Build structure that can hold multiple boxes
- Design and implement grid that can connect multiple Structures and Boxes in a matrix
- Implement text structure for each LASO
  - Metro's text structure will be a Grid
  
Pipeline Building Tools:
------------------------

This will come later when the structure is determined

- station, line, metro creation commandline-tool/python-library
- metro visulaizer

LAS Source Manager (LASSM):
---------------------------

Source manager for LASubway

- Create station LASO for installing software from source
- Create local source manager (~/.las/software)
- Create metro-local source manager (/metro_base/software)


