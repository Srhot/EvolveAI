"""
EvolveAI — Genome (Strateji DNA'sı)
====================================

Genetik Algoritmanın kullandığı ajan strateji temsili.

İKİ KATMANLI GENOME:
    1. Neural weights: DQN ağ ağırlıkları (devam eden öğrenme)
    2. Behavioral params: Saldırganlık, kaynak öncelik vb. (yumuşak yönlendirme)

NEDEN BU YAPI:
    Saf weight evolution (Neuroevolution) ile saf parametre evolution arasındaki
    hibrit yaklaşım. RL gradyenı içsel öğrenmeyi sağlar, GA ise stratejik
    çeşitlilik ve nesil-aşırı genel bilgi aktarımı sağlar.

REFERANSLAR:
    - Stanley & Miikkulainen (2002). "Evolving Neural Networks through Augmenting Topologies" (NEAT)
    - Salimans et al. (2017). "Evolution Strategies as a Scalable Alternative to RL" (OpenAI)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import uuid

import numpy as np

from config import CONFIG


@dataclass
class Genome:
    """Bir ajanın strateji DNA'sı.

    Attributes:
        weights: DQN ağırlıklarının düz vektörü (büyük, ~10k-100k boyutlu)
        behavior_params: Yumuşak davranış parametreleri (küçük, 6 boyut)
            - aggression: Saldırı olasılığını çarpan
            - resource_priority: Kaynak yönüne çekim kuvveti
            - exploration: Yeni hücre tercih ağırlığı
            - risk_tolerance: Düşük canla saldırı eşiği
            - cooperation: Aynı tip ajanlardan kaçınma
            - efficiency: Enerji kullanımına dikkat
        genome_id: Soy ağacı takibi için unique ID
        parent_ids: Ebeveyn genome_id'leri (1=mutation, 2=crossover)
        generation: Hangi nesilde oluştu
        fitness: Bu nesilde aldığı skor (selection için)
    """

    weights: Optional[np.ndarray] = None
    behavior_params: np.ndarray = field(default_factory=lambda: np.random.uniform(0, 1, 6))

    genome_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    parent_ids: tuple = field(default_factory=tuple)
    generation: int = 0
    fitness: float = 0.0

    @classmethod
    def random(cls, weight_size: int, generation: int = 0) -> Genome:
        """Rastgele bir genome üret (ilk nesil için).

        TODO[Sonnet]: Implement
            - weights: np.random.randn(weight_size) * 0.1 (Xavier-benzeri init)
            - behavior_params: np.random.uniform(0, 1, 6)
            - generation parametresini kullan
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 6'da doldurulacak")

    def copy(self) -> Genome:
        """Derin kopya. TODO[Sonnet]: np.copy() kullan, yeni genome_id ata."""
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 6'da doldurulacak")

    def __len__(self) -> int:
        """Toplam gen sayısı."""
        w = len(self.weights) if self.weights is not None else 0
        return w + len(self.behavior_params)
