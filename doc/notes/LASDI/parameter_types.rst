*********************
LASDIR Paramter Types
*********************

This page is the offcial (and incomplete) list of LASDR paramter types. Code and other documentation might not match the information in this file

Python Regex Filter Parameter
-----------------------------

+------------------+-------------+------+-----------------+
| Type Name        | Obriviation | List | File References |
+==================+=============+======+=================+
| regex_filter     | ref         | yes  | yes             |
+------------------+-------------+------+-----------------+

**Example(s):**

::

    `ref`

Python Regex Substring Parameter
--------------------------------


+-----------+-------------+------+-----------------+
| Type Name | Obriviation | List | File References |
+===========+=============+======+=================+
| regex_sub | res         | yes  | yes             |
+-----------+-------------+------+-----------------+

**Example(s):**

::
    
    `res`

Substring Filter Paramter
-------------------------

Strings are only vailid if they contain listed substrings.

+-----------+-------------+------+----------------------+---------------+-----------------+
| Type Name | Obriviation | List | Declaration Settings | Type Settings | File References |
+===========+=============+======+======================+===============+=================+
| substring | s           | yes  | yes                  | yes           | yes             |
+-----------+-------------+------+----------------------+---------------+-----------------+

**Example(s):**

::
    `s`substring`

Range Filter Parameter
----------------------

+-----------+-------------+------+-----------------+
| Type Name | Obriviation | List | File References |
+===========+=============+======+=================+
| range     | r           | yes  | yes             |
+-----------+-------------+------+-----------------+

**Example(s):**

::

    `r`1-50`

Range Required Parameter
------------------------

+----------------+-------------+------+-----------------+
| Type Name      | Obriviation | List | File References |
+================+=============+======+=================+
| range_required | rr          | yes  | yes             |
+----------------+-------------+------+-----------------+

**Example(s):**

::

    `rr`1-10`

Extention Filter Paramter
-------------------------

+-----------+-------------+------+----------------------+---------------+-----------------+
| Type Name | Obriviation | List | Declaration Settings | Type Settings | File References |
+===========+=============+======+======================+===============+=================+
| extention | e           | yes  | yes                  | yes           | yes             |
+-----------+-------------+------+----------------------+---------------+-----------------+

**Example(s):**

:: 
    
    `e`.fasta`




Template:
=========

Parameter Name
--------------

+-----------+-------------+------+----------------------+---------------+-----------------+
| Type Name | Obriviation | List | Declaration Settings | Type Settings | File References |
+===========+=============+======+======================+===============+=================+
|           |             |      |                      |               |                 |
+-----------+-------------+------+----------------------+---------------+-----------------+

**Example(s):**

:: 
    
    ```


