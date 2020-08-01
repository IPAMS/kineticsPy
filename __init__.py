"""
Analysis, automatization and helper modules for chemical kinetics simulations

Modules:
  * analysis_other: Simulation result analysis modules for other kinetics codes (besides cantera)

"""

from . import cantera
from .cantera import *
__all__ = ['cantera']