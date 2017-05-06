************************************
HOPSTACK WorkSpace Abstraction (WSA)
************************************

The WorkSpace Abstraction is similar to the Resilient Distributed Dataset (RDD)
implemented in apache spark.

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


