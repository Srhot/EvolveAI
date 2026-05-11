"""
EvolveAI — Q-Learning Agent (Aşama 2)
======================================

Klasik tablo tabanlı Q-Learning. Baseline olarak kullanılır,
DQN ile karşılaştırılarak "deep" katkısı kanıtlanır.

REFERANS:
    Watkins, C. J. C. H. (1989). "Learning from Delayed Rewards" (PhD Thesis)
    Sutton & Barto (2018), Chapter 6: Temporal-Difference Learning

ALGORITMA:
    Q(s,a) ← Q(s,a) + α [r + γ max_a' Q(s',a') − Q(s,a)]

NOT: Sürekli state uzayını ayrıklaştırmak gerekir (config.qlearning.STATE_BINS).
     Bu Q-tabloyu çok büyütür — tam da DQN'in neden gerekli olduğunu gösterir!
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict

import numpy as np

from config import CONFIG


class QAgent:
    """Tablo tabanlı Q-Learning ajanı.

    Q-tablo: dict[state_tuple, np.ndarray(NUM_ACTIONS)]

    State'i ayrıklaştırma kararı:
        Sürekli observation vector'ünü STATE_BINS^N tabloya sığdırmak için
        her boyutu STATE_BINS parçaya böleriz. Akademik motivasyon: "curse of
        dimensionality" sorununu somut göstermek.
    """

    def __init__(self, num_actions: int = None):
        self.config = CONFIG.qlearning
        self.num_actions = num_actions or CONFIG.world.NUM_ACTIONS
        self.q_table: Dict[tuple, np.ndarray] = defaultdict(
            lambda: np.zeros(self.num_actions, dtype=np.float32)
        )
        self.epsilon: float = self.config.EPSILON_START
        self.training_steps: int = 0

    def discretize_state(self, obs: np.ndarray) -> tuple:
        """Sürekli gözlemi ayrık state tuple'ına çevir.

        TODO[Sonnet]: Implement
            1. obs'u (-1, 1) aralığına clip et
            2. Her boyutu STATE_BINS parçaya böl: bin_idx = int((obs_i + 1) / 2 * STATE_BINS)
            3. tuple(bin_idx_list) döndür (dict key olarak kullanılacak)

        DİKKAT: 367 boyutlu state için STATE_BINS=10 → 10^367 olası state!
                Pratikte sadece ziyaret edilen state'ler tabloda yer alır
                (defaultdict sayesinde). Yine de bu Q-Learning'in limitini
                somutlaştırır — DQN'e geçişin akademik gerekçesi.
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 3'te doldurulacak")

    def select_action(self, obs: np.ndarray, training: bool = True) -> int:
        """Epsilon-greedy aksiyon seçimi.

        TODO[Sonnet]: Implement
            - training=True ve random < epsilon: rastgele aksiyon (exploration)
            - aksi halde: argmax(Q[state]) (exploitation)
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 3'te doldurulacak")

    def update(
        self, obs: np.ndarray, action: int, reward: float,
        next_obs: np.ndarray, done: bool
    ) -> float:
        """Q-değerini güncelle.

        Q(s,a) ← Q(s,a) + α [r + γ max Q(s',a') − Q(s,a)]

        Returns:
            TD error (debug/log için)
        """
        # TODO[Sonnet]: Implement Bellman update
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 3'te doldurulacak")

    def decay_epsilon(self) -> None:
        """Her bölüm sonunda epsilon'u azalt."""
        self.epsilon = max(self.config.EPSILON_END, self.epsilon * self.config.EPSILON_DECAY)

    def save(self, path: str) -> None:
        """Q-tabloyu pickle olarak kaydet."""
        # TODO[Sonnet]: pickle.dump(dict(self.q_table), open(path, "wb"))
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 3'te doldurulacak")

    def load(self, path: str) -> None:
        """Q-tabloyu yükle."""
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 3'te doldurulacak")
