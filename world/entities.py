"""
EvolveAI — World Entities
==========================

Grid dünyada yer alan tüm varlıkların sınıf tanımları.

Hierarchy:
    Entity (abstract)
    ├── Agent       — yapay zeka ajanı (RL + GA tarafından kontrol)
    ├── Resource    — pasif, ajanlar topladıkça yok olur
    └── Obstacle    — pasif, hareket engeli

REFERANSLAR:
    - Composition over inheritance (Gang of Four, 1994)
    - Entity-Component pattern (game dev best practice)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import uuid

from config import CONFIG


@dataclass
class Entity:
    """Tüm dünya varlıklarının base sınıfı."""

    x: int
    y: int
    entity_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def position(self) -> tuple[int, int]:
        return (self.x, self.y)


@dataclass
class Agent(Entity):
    """RL + GA ile kontrol edilen yapay zeka ajanı.

    Attributes:
        health: Can puanı (0 = ölü)
        energy: Enerji (0 = ölü, hareket için harcar)
        strategy_type: Evrim sonucu ortaya çıkan tip ("aggressive", "defensive", ...)
        genome: GA'nın kullandığı strateji DNA'sı (config.evolution.GENOME_SIZE)
        fitness: Bu nesilde aldığı toplam skor
        kills: Öldürdüğü ajan sayısı
        resources_collected: Topladığı kaynak sayısı
        steps_alive: Hayatta kaldığı adım sayısı
        elo_rating: Turnuva sıralaması için Elo puanı

    Stratejik tip otomatik olarak post-hoc analizle belirlenir
    (analysis/strategy_classifier.py). Sabit değildir, evrim ile değişir.
    """

    health: float = field(default_factory=lambda: CONFIG.world.AGENT_INITIAL_HEALTH)
    energy: float = field(default_factory=lambda: CONFIG.world.AGENT_INITIAL_ENERGY)
    strategy_type: Optional[str] = None
    genome: Optional[Any] = None  # np.ndarray, lazy import to avoid circular
    generation: int = 0
    parent_ids: tuple = field(default_factory=tuple)

    # Performans metrikleri (fitness hesaplama için)
    fitness: float = 0.0
    kills: int = 0
    resources_collected: int = 0
    steps_alive: int = 0
    cells_explored: set = field(default_factory=set)
    energy_spent_total: float = 0.0

    # Turnuva metrikleri
    elo_rating: float = 1200.0  # Standart başlangıç Elo
    tournament_wins: int = 0
    tournament_losses: int = 0

    @property
    def is_alive(self) -> bool:
        return self.health > 0 and self.energy > 0

    def take_damage(self, damage: float) -> None:
        self.health = max(0.0, self.health - damage)

    def consume_energy(self, amount: float) -> None:
        self.energy = max(0.0, self.energy - amount)
        self.energy_spent_total += amount

    def gain_energy(self, amount: float) -> None:
        self.energy = min(CONFIG.world.AGENT_INITIAL_ENERGY * 1.5, self.energy + amount)

    def to_dict(self) -> Dict[str, Any]:
        """Replay/serializasyon için dict'e çevir.

        TODO[Sonnet]: genome'u liste olarak ekle (np.ndarray JSON serializable değil)
        """
        return {
            "entity_id": self.entity_id,
            "position": self.position(),
            "health": self.health,
            "energy": self.energy,
            "strategy_type": self.strategy_type,
            "generation": self.generation,
            "fitness": self.fitness,
            "kills": self.kills,
            "resources_collected": self.resources_collected,
            "elo_rating": self.elo_rating,
        }


@dataclass
class Resource(Entity):
    """Toplandığında ajana enerji veren pasif kaynak."""

    value: float = field(default_factory=lambda: CONFIG.world.RESOURCE_VALUE)
    consumed: bool = False


@dataclass
class Obstacle(Entity):
    """Hareketi engelleyen pasif engel."""

    pass
