"""
EvolveAI World Module
======================

Public API:
    from world import GridWorld, Agent, Resource, Obstacle

Bu modül başka projelere de taşınabilir (NeuroType modüler mimari prensibi).
"""

from world.entities import Agent, Resource, Obstacle, Entity

# GridWorld gymnasium gerektirir — yüklü değilse graceful fallback
try:
    from world.environment import GridWorld
except ImportError:
    GridWorld = None  # type: ignore

__all__ = ["GridWorld", "Agent", "Resource", "Obstacle", "Entity"]
