"""
DXF Auto - Laser CNC Manufacturing Analysis Tool

A professional tool for analyzing DXF files and extracting metrics
needed for laser CNC manufacturing price calculations.
"""

__version__ = '1.0.0'
__author__ = 'Expert Software Architect'

from .dxf_analyzer import DXFAnalyzer
from .entity_calculator import EntityCalculator
from .metrics import DXFMetrics, EntityMetrics
from .formatter import ConsoleFormatter

__all__ = [
    'DXFAnalyzer',
    'EntityCalculator',
    'DXFMetrics',
    'EntityMetrics',
    'ConsoleFormatter',
]
