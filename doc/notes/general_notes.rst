*****************
General LAS Notes
*****************

LAS General Ideas and goals:
----------------------------
1. Remove programming from software pipelining
2. Be easy for non-techincal/non-programming people to use
3. Recursive modularity for all LASOs
4. software pipeline visualization
5. source managment and build tools for software pipeline dependencies

LAS aims to provide a framework to build software pipelines within. Some 
fringe cases may not be supported, though one should be able to simulate thoes
cases with a combination of standard features. 


LASubway Home (LASH):
---------------------

Would be a user or system-wide directory containing:

1. LAS Metro dependency source installations
2. LAS host list
3. Credentials (database, AWS, etc)

An alternative to LASH could be creating headless container/jail(BSD)/
zone(solaris)-like objects that contain all dependencies for the piece (or
pieces) of the pipeline being run on a machine. These container-like modules 
 would be dropped onto a machine as a precompiled binary wrapped in a disk 
image, then be run as an independent entity by python code piped over ssh.
This would be the preffered way doing things but it might not be possible and 
if it is, it'd definitly not easy.

Different Cluster Frameworks and software to consider interfacing with:
-----------------------------------------------------------------------

1. kubernetes
2. Apache Mesos
3. Hadoop


WorkSpace:
----------

A WorkSpace is a shared file system abstraction allowing two or more LASOs to
share files within a metro. WorkSpaces can be aliken to Volumes in Kubernetes. 
Metros runing inside an other metro cannot share volumes with it's parent.

WorkSpaces will essentially be a hash (rough outline below) that is contains
the filename, and the corrisponding file's location(s).

::
    {'/file/name/': ('user@remote.computer:/file/name', '/local/file/path'),
     '/filename': ('localfile')}

If a metro's LASOs are running on multiple machines, the remote LASO manager 
will synchronize WorkSpace hashes by signaling every machine
running LASOs with access to that WorkSpace when a change is made. Signal
collisions should be expected and delt with some how.

**Different Possible Implimentation Protocols:**

* SSH pipes
* SSH File System (SSHFS)
  - Make sure that the files are not being written by anything else on the 
    host machine
* FTP File System (FTPFS)
* NFS

**Possible Ingetrations:**

* Docker
* Kubernetes 
* Gluster/Lustre
* AWS Elastic Block Storage

Kubernetes has many different volume types that could act as a rough list of
different integrations and implimentations to use for workspaces.

Look into creating virtual file systems with FUSE to act as workspaces on the 
head machine.
Link: FUSE_

.. _FUSE: https://www.stavros.io/posts/python-fuse-filesystem/


LASO Notes:
===========

Different Station Scenarios:
----------------------------

1. Run one command one time with one input
2. Run one command N number of times with one input
3. Run one command for every valid input given
4. Run one command one time with multiple inputs
5. Run one command N number of times with multiple inputs
6. Run one command with one input N number of times sequentailly
7. Run one command with multiple inputs N number of times sequentailly
8. Run one command in a loop until specific output requirement met
