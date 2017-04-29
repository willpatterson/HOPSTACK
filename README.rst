.. _README.rst

********
LASubway
********

LASubway (LAS) is a software pipeliner/workflow managment system that scales 
into a distributed cluster managament and job scheduling system. The LASubway 
project was initally started because there are no effective tools or methods 
used by scientists and journalists to document, write, and exectue 
computational analyses. This discontinuity makes computational research
difficult to reproduce, often adding significant overhead to researchers 
workloads. LASubway aims to address these problems with a comprehensive set of
tools to create, document, run and distriubte standarized software pipelines 
across UNIX-like computers and clusters.

LASubway is named after Los Angeles' 1990's metro system for two resasons:

1. Subway systems provide a rough metaphor for software pipelining, providing 
   easy names for features and concepts
2. The LA subway is an incomplete, ambitious project -- both parrallel with the 
   LASubway software suite in its current state.

**General Goals of LASubway:**

- Remove programming from software pipelining
- Provide a simple interface and tools for working with software pipelines
- Create a standard for modular, container-like software pipelines (metros)
  that run everywhere on Unix-like platforms
- Create a 'user-grid' system that allows users to connect all resources
  they have access to and utilize it to run pipelines

**Planned Features of LASubway:**

- Tools to create, execute, and document standardized, recusively modular
  software pipelines (metros)
- Software pipeline visualization
- Packaging software pipelines into linux containers (docker)
- Interfaces to cloud services (AWS, Azure, etc)
- Interfaces to popular sechudulers (Slurm, SGE)
- Ad-hoc clustering with SSH

As the LASubway project evolves, these planned features will likely evolve with
it. This documentation will updated continuously as LAS is developed.

Overview of Basic Structure:
============================

In it's current state of development and planning LASubway defines three
distinct object types (called ``LASOs`` for LASubway Objects): ``stations``,
``metro lines`` and ``metros``, each comprised of the previous in the list. All
LAS data objects are defined with ``YAML`` files inside a metro's base
directory. All LAS objects are linked together with LASubway's ``data 
interpreter`` LASDI. LASDI and the LAS objects are described more below.

Stations:
---------

``Stations`` are the most basic of the LASOs. A station defines one shell
command or LAS module and the type of input and output data expected. Stations
are the building blocks of all other LAS objects. ``Stations`` are linked 
together using ``LASDI`` in ``metro lines`` to provide a simple way of pipeing 
data between different shell commands and or LAS modules.

Metro Lines:
------------

``Metro lines``, the next object layer above ``stations``, are simply a linear
set of ``stations`` that pipe data from one end to the other using ``LASDI``. 

Metros:
-------

``Metros``, the highest layer of the LASOs, link linear ``metro lines`` 
together to provide a unidirectional (and potentially parallel) graph. In the 
future I plan on implementing conditional control flow to ``metros`` to allow
for dynamic 'smart' ``metros``. 

The ``metro`` format is the software pipeline standard that LASubway intends
to provide, however, ``stations`` and ``metro lines`` can be run independenly
from ``metros``.


LAS Data Interpreter (LASDI):
==========================================
The LAS Data Interpreter is one of LASubway's key abstractions. LASDI's main 
function is to fetch/prepare data for the start of a pipeline as well as pipe
data between different parts of the pipeline. At it's most basic level, LASDI 
takes a string as input, attempts to find verified data files with it, 
downloads and prepares data if nessesary, and then outputs (optionally) 
formatted and filtered filepaths or raw data. You pass LASDI an URL that points
to a directory in the file system, LASDI will return every file inside that 
directory. Pass LASDI the URL of a tar.gz file on the Web, LASDI will download 
the tar.gz file into a tmp direcotry, decompress and untar the archive and 
return the true file paths of every file inside the archive. 

LASDI Can also take any LAS object as input. LASDI will run the LAS object 
provided as input and pipe it's data into an existing pipeline.

Protocols (Soon to be) Supported:

- (S)FTP
- HTTP(S)
- SSH

LASDI is currently under development.

LAS Data Interpreter References (LASDIRs):
------------------------------------------

Strings decoded by LASDI are called ``LAS Data Interpreter References
(LASDIRS)``, or ``Data References`` for short. LASDIR syntax could be 
considered an extention of traditional URL syntax, adding a few new schemes,
utilizing Parameters to parse and filter data, and allowing raw data to be 
valid under certain schemes. LASDIRs are comprised of two individual peices: A 
``URL`` or raw data sring, and variable combinations of ``Paramters``. 

LASDIR Schemes:
---------------

LASDIR syntax provides several custom URL schemes that allow for interaction 
with higher-level LASubway processes:

**Previous LASO object output:** The base of the file path is the output 
directory of the previous LASubway Object in the pipeline

::

    prelaso:/path/to/file/in/previous/LASO

**Workspace:** The base directory of the file path in the URL is the current 
Metro's shared space directory (called Workspace)

::

    workspace:/path/to/file/in/Workspace

**Raw Data:** Raw data can be passed as the urls path:

::

    raw:ACGGGTAAAACGTAACGGTAAAAAA


Parameters:
----------

Parameters can be used to filter and format the output of LASDI.

In Data References, Parameters are appened to URLs and surrounded by backticks

Example Parameter statement:

.. code-block:: sh

    `filter-type`filter parameters`

Parameters must accompany a URL to be valid.

**All Data Filter Types can take a list of parameters:**
Example of valid lists:

.. code-block:: sh 

    "`e`.fasta,.log,.etc`"

    "`e`.fasta .log .etc`"

    "`e`.fasta, .log, .etc`"


**Use Multiple Filters on One Data String:**
Example:

.. code-block:: sh 

    "`e`.fasta`r`75-94`"

    "`r`25-30`ru`50-80`"


**Parameter Types:**

- Filter with Python Regular Expressions:

.. code-block:: sh 

    "`r`python-regex`"

- Filter by file extention:

.. code-block:: sh 

    "`e`.fasta`"

- Filter by filenames or substrings:

.. code-block:: sh 

    "`s`subtring, substring1`

- Filter by ranges (looks for a complete numbers in file names):

.. code-block:: sh 

    "`r`0-100`"

- Filter by unique ranges (throws error or prompt user if not more than one 
  file in range):

.. code-block:: sh 

    "`ru`0-100`"

- Filter with lists of file names using station in files (.sin file should be 
  located in the station directory):

.. code-block:: sh

    "`sin`sin_file_name.sin`


Getting Involved:
=================

If you want to get involved in developing LASubway please let me know. You can
reach me at wpatt2 (at) pdx.edu. Currently most of the project is planned but
not implemented so there is A LOT to do. I am a busy, working college student 
with little time to work on personal projects.
