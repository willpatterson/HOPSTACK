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


Different Cluster Frameworks and software to consider interfacing with:
-----------------------------------------------------------------------

1. kubernetes
2. Apache Mesos
3. Hadoop


WorkSpace:
----------

WorkSpaces are directories shared between LASOs in a metro.
WorkSpaces can be given different access groups and levels allowing sharing 
between set groups and or different types of LASOs.
WorkSpaces can be aliken to Volumes in Kubernetes. 
WorkSpaces can be implemented with different protocols and file systems to 
allow workspaces to be deployed on many different types of systems.
Metros runing inside a metro cannot share volumes with it's parent metro.


**Different Possible Implimentation Protocols:**

* SSH pipes
* SSH File System (SSHFS)
* FTP File System (FTPFS)
* NFS

**Possible Ingetrations:**

* Docker
* Kubernetes 
* Gluster/Lustre
* AWS Elastic Block Storage

Kubernetes has many different volume types that could act as a rough list of
different integrations and implimentations to use for workspaces.


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
