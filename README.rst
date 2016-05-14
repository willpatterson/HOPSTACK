.. _README.rst

***************
LASubway README
***************

LASubway (LAS) is a software pipeliner in active development. I started the LASubway project because I have exprienced profound discontinuity in the way computational analyses are documented, written and exectued in the acedemic community. This discontinuity makes computatoinal research difficult to reproduce adding a lot of overhead to researchers. LASubway aims to address these problems with a comprehensive set of tools to create, document, run and distriubte standarized software pipelines on UNIX-like computers and clusters.

LASubway is named after Los Angeles' 1990's metro system for two resasons:

1. Subway systems provide a rough metaphor for software pipelining, providing easy names for features and concepts
2. Nobody uses the Los Angeles Metro Rail

Planned Features of LASubway:

- Tools to create, execute and document standardized, recusively modular software pipelines (metros)
- Tools to package software pipelines (metros) into linux containers (docker)
- Tools to run and or distribute software pipelines (metros) on cloud services (AWS, Azure, etc)
- Tools to interface software pipelines (metros) with popular sechudulers (Slurm, SGE)
- Tools to distribue software pipelines (metros) over ad-hoc clusters with SSH

Overview of Basic Structure:
============================

In it's current state of development and planning LASubway has three different object types: ``stations``, ``metro lines`` and ``metros``, each comprised of the previous in the list. All LAS objects are linked together with LASubway's ``data interpreter`` LASDI. LASDI and the LAS objects are described more below.

Stations:
---------

``Station`` objects are the most basic LAS object. A station defines one shell command or LAS module and the type of input and output data expected. Stations are the building blocks of all other LAS objects. ``Stations`` are linked together with LASDI in ``metro lines`` to provide a simple way of pipeing data between different shell commands and or LAS modules.

Metro Lines:
------------

``Metro lines`` are the next object layer above ``stations``. ``Metro lines`` are simply a linear set of stations that pipe data from one end to the other. 

Metros:
-------

Metros are the highest layer of LAS objects. Metros link linear ``metro lines`` together to provide a unidirectional and potentially parallel graph. In the future I plan on implementing conditional control flow to ``metros`` to allow for dynamic 'smart' metros. 

The ``metro`` format software pipeline standard that LASubway intends to provide. However, ``stations`` and ``metro lines`` can be run independenly from ``metros``.


LAS Data Interpreter (LASDI):
-----------------------------
The LAS Data Interpreter is one of LASubway's key abstractions. LASDI's main function is to fetch/prepare data for the start of a pipeline as well as pipe data between different parts of the pipeline. At it's most basic level, LASDI takes a string as input, attempts to find verified data files with it, downloads and prepares data if nessesary, and then outputs every verified file path found with the input string. This may sound complex but in the contex of UNIX, where everything is a string it acutally makes a lot of sense. You pass LASDI a path to a directory in the file system, LASDI will return every file inside that directory. Pass LASDI the URL of a tar.gz file, LASDI will download the tar.gz file into a tmp direcotry, decompress and untar the archive and return the true file paths of every file inside the archive. 

LASDI Can also take any LAS object as input. LASDI will run the LAS object provided as input and pipe it's data into existing pipeline.

Strings LASDI can decode:

- File Paths
- Dirctory File Paths
- Tar Files
- Compressed Files (bz2, gz, zip)
- IP addresses
- URLs

Protocols Supported:

- FTP
- FSTP
- SSH
- HTTP/s

LASDI is curretnly being developed.

Getting Involved:
=================

If you want get involved in developing LASubway please let me know. You can reach me at wpatt2 (at) pdx.edu. Currently most of the project is planned but not implemented so there is A LOT to do. I am a busy, working college student with little time to work on personal projects.


