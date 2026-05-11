"""
EvolveAI — Selection (Doğal Seçilim)
=====================================

Üç klasik selection yöntemi. config.evolution.SELECTION_METHOD ile seçilir.

REFERANSLAR:
    - Goldberg (1989). "Genetic Algorithms in Search, Optimization, and Machine Learning"
    - Eiben & Smith (2015). "Introduction to Evolutionary Computing" Chapter 5
"""

from __future__ import annotations

from typing import List

import numpy as np

from config import CONFIG
from modules.evolution.genome import Genome


def tournament_selection(population: List[Genome], k: int = None) -> Genome:
    """Turnuva seçimi — k rastgele birey arasından en iyiyi seç.

    EN POPULER YÖNTEM. Selection pressure kontrolü kolay (k arttıkça artar).

    TODO[Sonnet]: Implement
        k = k or CONFIG.evolution.TOURNAMENT_SIZE
        contestants = random.sample(population, k)
        return max(contestants, key=lambda g: g.fitness)
    """
    raise NotImplementedError("Sonnet 4.6: HANDOFF Day 6'da doldurulacak")


def roulette_selection(population: List[Genome]) -> Genome:
    """Rulet (fitness proportional) selection.

    Negatif fitness destekler (shift + epsilon ile).

    TODO[Sonnet]: Implement
        fitness = np.array([g.fitness for g in population])
        fitness = fitness - fitness.min() + 1e-6  # ensure positive
        probs = fitness / fitness.sum()
        return np.random.choice(population, p=probs)
    """
    raise NotImplementedError("Sonnet 4.6: HANDOFF Day 6'da doldurulacak")


def rank_selection(population: List[Genome]) -> Genome:
    """Rank-based selection — fitness yerine sıralama kullanır.

    Outlier fitness değerlerinin baskın olmasını önler.

    TODO[Sonnet]: Implement
        sorted_pop = sorted(population, key=lambda g: g.fitness)
        ranks = np.arange(1, len(population) + 1)
        probs = ranks / ranks.sum()
        return np.random.choice(sorted_pop, p=probs)
    """
    raise NotImplementedError("Sonnet 4.6: HANDOFF Day 6'da doldurulacak")


def elitism(population: List[Genome], ratio: float = None) -> List[Genome]:
    """En iyi %ratio'yu sonraki nesle direkt aktar.

    TODO[Sonnet]: Implement
        ratio = ratio or CONFIG.evolution.ELITISM_RATIO
        n_elite = max(1, int(len(population) * ratio))
        return sorted(population, key=lambda g: g.fitness, reverse=True)[:n_elite]
    """
    raise NotImplementedError("Sonnet 4.6: HANDOFF Day 6'da doldurulacak")


def select(population: List[Genome], method: str = None) -> Genome:
    """Dispatch — config'e göre seçim yöntemini seç."""
    method = method or CONFIG.evolution.SELECTION_METHOD
    if method == "tournament":
        return tournament_selection(population)
    elif method == "roulette":
        return roulette_selection(population)
    elif method == "rank":
        return rank_selection(population)
    raise ValueError(f"Bilinmeyen selection method: {method}")
