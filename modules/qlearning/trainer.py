"""
EvolveAI — Q-Learning Trainer
==============================

Q-tabloyu eğitim döngüsünde günceller, log'ları yazar, checkpoint kaydeder.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import numpy as np

from config import CONFIG
from modules.qlearning.q_agent import QAgent


class QLearningTrainer:
    """Q-Learning eğitim döngüsü.

    Kullanım:
        trainer = QLearningTrainer()
        trainer.train(num_episodes=2000)
        trainer.evaluate(num_episodes=100)
    """

    def __init__(self, env=None, agent: Optional[QAgent] = None):
        self.config = CONFIG.qlearning
        self.env = env  # GridWorld instance, dependency injection
        self.agent = agent or QAgent()
        self.episode_rewards: List[float] = []
        self.episode_lengths: List[int] = []

    def train(self, num_episodes: Optional[int] = None) -> None:
        """Ana eğitim döngüsü.

        TODO[Sonnet]: Implement
            for ep in range(NUM_EPISODES):
                obs, _ = env.reset()
                total_reward = 0
                done = False
                while not done:
                    action = agent.select_action(obs)
                    next_obs, reward, terminated, truncated, _ = env.step(action)
                    agent.update(obs, action, reward, next_obs, terminated)
                    obs = next_obs
                    total_reward += reward
                    done = terminated or truncated
                agent.decay_epsilon()
                episode_rewards.append(total_reward)
                if ep % LOG_EVERY_N == 0:
                    log to TensorBoard
                if ep % CHECKPOINT_EVERY_N == 0:
                    agent.save(...)

        NOT: Multi-agent için her ajan kendi Q-tablosunu tutar (independent learners).
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 3'te doldurulacak")

    def evaluate(self, num_episodes: int = 100, render: bool = False) -> dict:
        """Eğitilmiş ajanı değerlendir (epsilon=0, no exploration)."""
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 3'te doldurulacak")
