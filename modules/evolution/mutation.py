"""
EvolveAI — Mutation
====================

Genoma rastgele küçük değişiklikler ekler — yerel optimumdan kaçışı sağlar.

REFERANS:
    Eiben & Smith (2015), Chapter 4. Gaussian mutation neural genome için standart.
"""

from __future__ import annotations

import numpy as np

from config import CONFIG
from modules.evolution.genome import Genome


def gaussian_mutation(genome: Genome, rate: float = None, strength: float = None) -> Genome:
    """Her geni rate olasılıkla N(0, strength) gürültüsü ile değiştir.

    TODO[Sonnet]: Implement
        rate = rate or CONFIG.evolution.MUTATION_RATE
        strength = strength or CONFIG.evolution.MUTATION_STRENGTH

        # Weights mutation
        mask_w = np.random.rand(len(genome.weights)) < rate
        noise_w = np.random.normal(0, strength, len(genome.weights))
        genome.weights = genome.weights + mask_w * noise_w

        # Behavior params mutation (clip to [0, 1])
        mask_b = np.random.rand(len(genome.behavior_params)) < rate
        noise_b = np.random.normal(0, strength, len(genome.behavior_params))
        genome.behavior_params = np.clip(genome.behavior_params + mask_b * noise_b, 0, 1)

        return genome
    """
    raise NotImplementedError("Sonnet 4.6: HANDOFF Day 6'da doldurulacak")


def adaptive_mutation(genome: Genome, fitness_history: list) -> Genome:
    """Stagnasyon tespit edersen mutation strength'i artır.

    TODO[Sonnet] (BONUS, opsiyonel):
        Son 5 nesilde fitness improvement < threshold ise strength *= 2.
        Bu local optima'dan kaçışı hızlandırır.
    """
    raise NotImplementedError("Sonnet 4.6: BONUS — zaman kalırsa")
