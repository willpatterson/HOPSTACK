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

LAS aims to provide a framework to build software pipelines within. Some fringe cases may not be supported, though one should be able to simulate thoes cases with a combination of standard features. 


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

WorkSpace is a shared directory space between all LASO objects in a metro.

WorkSpace will not be limited to a single implementation. It should be able to work dynamically depeneding on the type of metro and the system it is running on

