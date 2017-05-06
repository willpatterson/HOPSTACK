"""
Mostly Blank Setup script
"""

from setuptools import setup, find_packages
from setuptools.command.install import install

setup(name="HOPSTACK",
      version="0.0.0",
      description="Self Provisioning Ad Hoc Cluster Tool Kit",
      license="MIT",
      author="William Patterson",
      install_requires=['PyYaml'],
      packages=find_packages(),
      package_data={}, #TODO Fill in
      entry_points={}) #TODO Fill in
