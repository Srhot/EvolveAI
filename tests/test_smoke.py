"""
Smoke tests — Sonnet 4.6 ilk gün hemen çalıştırsın.
Bu testler %100 çalışmalı, aksi halde temel mimari bozuk demektir.
"""
import sys
from pathlib import Path

# Project root'u sys.path'e ekle
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest


def test_config_loads():
    """config.py import edilebilir mi?"""
    from config import CONFIG
    assert CONFIG.SEED == 42
    assert CONFIG.world.GRID_SIZE == (40, 40)
    assert CONFIG.world.NUM_AGENTS_PER_GENERATION == 24


def test_config_dirs_exist():
    """Tüm klasörler oluşturulmuş mu?"""
    from config import CONFIG
    assert CONFIG.CHECKPOINTS_DIR.exists()
    assert CONFIG.LOGS_DIR.exists()
    assert CONFIG.REPLAYS_DIR.exists()


def test_state_dim():
    """State boyutu hesabı doğru mu?"""
    from config import get_state_dim
    # vision_radius=5 → (11x11) * 3 channels + 4 extras = 367
    assert get_state_dim() == 367


def test_entities_creatable():
    """Entity sınıfları çalışıyor mu?"""
    from world.entities import Agent, Resource, Obstacle
    a = Agent(x=5, y=10)
    assert a.health == 100.0
    assert a.is_alive

    r = Resource(x=0, y=0)
    assert r.value == 20.0

    o = Obstacle(x=1, y=1)
    assert o.position() == (1, 1)


def test_imports():
    """Tüm public API import edilebiliyor mu?"""
    from world import GridWorld, Agent
    from modules.qlearning import QAgent
    from modules.dqn import DQNAgent, ReplayBuffer
    from modules.evolution import Genome, EvolutionLoop
    from tournament import Tournament
    # Bunlar TODO halinde olsa da import edilebilir olmalı


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
