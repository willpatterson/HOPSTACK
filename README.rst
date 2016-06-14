.. _README.rst

***************
LASubway README
***************

LASubway (LAS) is a software pipeliner/workflow managment system in active development. I started the LASubway project because I have experienced profound discontinuity in the way computational analyses are documented, written, and exectued in the acedemic community. This discontinuity makes computational research difficult to reproduce adding a lot of overhead work for researchers simply to reproduce results. LASubway aims to address these problems with a comprehensive set of tools to create, document, run and distriubte standarized software pipelines on UNIX-like computers and clusters.

LASubway is named after Los Angeles' 1990's metro system for two resasons:

1. Subway systems provide a rough metaphor for software pipelining, providing easy names for features and concepts
2. The LA subway is an ambitious project, is incomplete, and has low rider-ship -- all parrallel with the LASubway software suite in its current state.

**General Goals of LASubway:**

- Remove programming from software pipelining
- Provide a simple interface and tools working with software pipelines
- Create a standard for modular, container-like software pipelines (metros) that run everywhere on Unix-like platforms

**Planned Features of LASubway:**

- Tools to create, execute, and document standardized, recusively modular software pipelines (metros)
- Software pipeline visualization
- Packaging software pipelines into linux containers (docker)
- Interfaces to cloud services (AWS, Azure, etc)
- Interfaces to popular sechudulers (Slurm, SGE)
- Ad-hoc clustering with SSH

As the LASubway project evolves, these planned features will likely evolve with it. This documentation will updated continuously as LAS is developed.

Overview of Basic Structure:
============================

In it's current state of development and planning there are three types of LASubway Objects (``LASOs``): ``stations``, ``metro lines`` and ``metros``, each comprised of the previous in the list. All LAS data objects are defined with ``YAML`` files inside a metro base directory. All LAS objects are linked together with LASubway's ``data interpreter`` LASDI. LASDI and the LAS objects are described more below.

Stations:
---------

``Station`` objects are the most basic LAS object. A station defines one shell command or LAS module and the type of input and output data expected. Stations are the building blocks of all other LAS objects. ``Stations`` are linked together with LASDI in ``metro lines`` to provide a simple way of pipeing data between different shell commands and or LAS modules.

Metro Lines:
------------

``Metro lines`` are the next object layer above ``stations``. ``Metro lines`` are simply a linear set of ``stations`` that pipe data from one end to the other. 

Metros:
-------

``Metros`` are the highest layer of LAS objects. ``Metros`` link linear ``metro lines`` together to provide a unidirectional (and potentially parallel) graph. In the future I plan on implementing conditional control flow to ``metros`` to allow for dynamic 'smart' ``metros``. 

The ``metro`` format is the software pipeline standard that LASubway intends to provide, however, ``stations`` and ``metro lines`` can be run independenly from ``metros``.


LAS Data Interpreter (LASDI):
==========================================
The LAS Data Interpreter is one of LASubway's key abstractions. LASDI's main function is to fetch/prepare data for the start of a pipeline as well as pipe data between different parts of the pipeline. At it's most basic level, LASDI takes a string as input, attempts to find verified data files with it, downloads and prepares data if nessesary, and then outputs every verified file path found with the input string. This may sound complex but in the contex of UNIX, where everything is a string it acutally makes a lot of sense. You pass LASDI a path to a directory in the file system, LASDI will return every file inside that directory. Pass LASDI the URL of a tar.gz file, LASDI will download the tar.gz file into a tmp direcotry, decompress and untar the archive and return the true file paths of every file inside the archive. 

LASDI Can also take any LAS object as input. LASDI will run the LAS object provided as input and pipe it's data into an existing pipeline.

Strings LASDI can decode:

- Unix Paths

  - Directory File Paths
  - Tar Files
  - Compressed Files (bz2, gz, zip)
  - Other LASOs (metro, metro line, station)

- URLs
- SSH/SCP + Path 

Protocols (Soon to be) Supported:

- FTP
- FSTP
- SSH
- HTTP/s

LASDI is currently under development.

LAS Data Interpreter Statement Syntax (DISS):
------------------------------------------

The strings decoded by LASDI are called LAS Data Statements (LASDS). LASDSs are generally comprised of two individual peices: ``Data Strings`` and ``Data Parameters``. Data Strings, which are briefly described above, can be a unix file path, a URL, or a SSH/SCP login, that LASDI attempts to turn into a list of file paths that are behind that string (if any). Data Parameters will filter the output file paths generated by LASDI using a Data String. Combined, these to strings make a LAS Data Statement that can be passed to LASDI.

Data Strings:
-------------

(Coming soon)

Data Parameters:
----------------

Data Parameters can be used to filter or alter the output of Data Strings passed to LASDI.

Data Parameters are denoted by appending a Data String with a parameter statement.

Example Data parameter statement:

.. code-block:: sh

    `parameter-type`parameters`

Data  must accompany a Data String to be valid.

**All Data Parameters Types can take a list of parameters:**
Example of valid lists:

.. code-block:: sh 

    "/datastring/`e`.fasta,.log,.etc`"

    "/datastring/`e`.fasta .log .etc`"

    "/datastring/`e`.fasta, .log, .etc`"


**Use Multiple Parameters Types on One Data String:**
Example:

.. code-block:: sh 

    "/datasrting/`e`.fasta`r`75-94`"

    "/datasrting/`r`25-30`ru`50-80`"


**Parameter Types:**

- Filter with Python Regular Expressions:

.. code-block:: sh 

    "/datastring/`re`python-regex`"

- Filter by file extention:

.. code-block:: sh 

    "/datastring/`e`.fasta`"

- Filter by filenames or substrings:

.. code-block:: sh 

    "/datastring/`s`subtring, substring1`

- Filter by ranges (looks for a complete numbers in file names):

.. code-block:: sh 

    "/datasrting/`r`0-100`"

- Filter by unique ranges (throws error or prompt user if not more than one file in range):

.. code-block:: sh 

    "/datasrting/`ru`0-100`"

- Filter with lists of file names using station in files (.sin file should be located in the station directory):

.. cod-block:: sh

    "/datasrting/`sin`sin_file_name.sin`


Getting Involved:
=================

If you want to get involved in developing LASubway please let me know. You can reach me at wpatt2 (at) pdx.edu. Currently most of the project is planned but not implemented so there is A LOT to do. I am a busy, working college student with little time to work on personal projects.


