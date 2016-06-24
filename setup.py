"""
Mostly Blank Setup script
"""

from setuptools import setup, find_packages
from setuptools.command.install import install

setup(name="LASubway",
      version="0.0.0",
      description="Software Pipelining Suite"
      license="MIT",
      author="William Patterson",
      packages=find_packages(),
      package_data={} #TODO Fill in
      install_requires=['PyYaml'],
      entry_points={}) #TODO Fill in
