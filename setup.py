"""Setup script for sprint-workflow LangGraph implementation."""

from setuptools import setup, find_packages

setup(
    name="sprint-workflow-graph",
    version="1.0.0",
    packages=find_packages(include=['graph', 'graph.*']),
    python_requires='>=3.9',
)
