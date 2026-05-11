"""
EvolveAI — Replay Buffer
=========================

Experience Replay (Lin, 1992) — RL'in stabilite çekirdeği.
Prioritized variant (Schaul et al., 2016) opsiyonel.

NEDEN ÖNEMLİ:
    - Ardışık örnekler korelasyonlu → IID varsayımını ihlal eder
    - Önemli örnekler nadir görülür → öğrenme yavaşlar
    - PER bu iki sorunu çözer: TD-error ile öncelik

REFERANSLAR:
    - Lin, L.-J. (1992). "Self-Improving Reactive Agents Based on Reinforcement Learning"
    - Schaul et al. (2016). "Prioritized Experience Replay" (ICLR)
"""

from __future__ import annotations

from collections import deque, namedtuple
from typing import List, Tuple

import numpy as np

from config import CONFIG

Experience = namedtuple("Experience", ["state", "action", "reward", "next_state", "done"])


class ReplayBuffer:
    """Uniform replay buffer — baseline."""

    def __init__(self, capacity: int = None):
        capacity = capacity or CONFIG.dqn.REPLAY_BUFFER_SIZE
        self.buffer: deque = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done) -> None:
        self.buffer.append(Experience(state, action, reward, next_state, done))

    def sample(self, batch_size: int) -> Tuple[np.ndarray, ...]:
        """Rastgele batch örnekle.

        TODO[Sonnet]: Implement
            1. random.sample(self.buffer, batch_size)
            2. Her alanı ayrı array'e topla (states, actions, rewards, next_states, dones)
            3. np.array'lere dönüştür (float32 / int64 / bool uygun)
            4. Tuple döndür
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def __len__(self) -> int:
        return len(self.buffer)


class PrioritizedReplayBuffer:
    """Prioritized Experience Replay (PER).

    Önemli örnekleri (yüksek TD-error) daha sık örnekler.
    Bias düzeltmesi için importance sampling weight'leri uygular.
    """

    def __init__(self, capacity: int = None, alpha: float = 0.6, beta: float = 0.4):
        """
        Args:
            alpha: Önceliklendirme şiddeti (0=uniform, 1=tam priority)
            beta: Bias düzeltme şiddeti (0=düzeltme yok, 1=tam düzeltme)
        """
        self.capacity = capacity or CONFIG.dqn.REPLAY_BUFFER_SIZE
        self.alpha = alpha
        self.beta = beta
        self.buffer: List = []
        self.priorities = np.zeros(self.capacity, dtype=np.float32)
        self.position: int = 0

    def push(self, state, action, reward, next_state, done) -> None:
        """Yeni örneği max priority ile ekle (yeni örnek mutlaka örneklenir).

        TODO[Sonnet]: Implement
            - max_prio = self.priorities.max() if buffer doluysa, yoksa 1.0
            - Eğer buffer < capacity: append, else: buffer[position] = exp
            - self.priorities[position] = max_prio
            - position = (position + 1) % capacity
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def sample(self, batch_size: int) -> Tuple[np.ndarray, ...]:
        """Öncelik tabanlı örnekleme.

        TODO[Sonnet]: Implement
            1. probs = priorities^alpha / sum(priorities^alpha)
            2. indices = np.random.choice(len, batch_size, p=probs)
            3. samples = [buffer[i] for i in indices]
            4. weights = (len * probs[indices])^(-beta), normalize by max
            5. Return: states, actions, rewards, next_states, dones, indices, weights
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def update_priorities(self, indices: np.ndarray, td_errors: np.ndarray) -> None:
        """TD-error'a göre öncelikleri güncelle.

        TODO[Sonnet]: priority = |td_error| + epsilon (küçük sabit, 1e-6)
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def __len__(self) -> int:
        return len(self.buffer)
