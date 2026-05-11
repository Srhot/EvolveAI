"""
EvolveAI — DQN Trainer
=======================

DQN eğitim döngüsü. TensorBoard log + checkpoint + early stopping.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from config import CONFIG
from modules.dqn.dqn_agent import DQNAgent


class DQNTrainer:
    """DQN eğitim döngüsü.

    TODO[Sonnet]: Standart RL loop
        for episode in range(NUM_EPISODES):
            obs, _ = env.reset()
            done = False
            total_reward = 0
            while not done:
                action = agent.select_action(obs)
                next_obs, reward, terminated, truncated, _ = env.step(action)
                agent.store_transition(obs, action, reward, next_obs, terminated)
                loss = agent.train_step()
                if agent.training_steps % TARGET_UPDATE_FREQ == 0:
                    agent.update_target()
                obs = next_obs
                total_reward += reward
                done = terminated or truncated
            # Log + checkpoint
    """

    def __init__(self, env=None, agent: Optional[DQNAgent] = None):
        self.config = CONFIG.dqn
        self.env = env
        self.agent = agent or DQNAgent()
        self.episode_rewards: List[float] = []
        self.episode_losses: List[float] = []

    def train(self, num_episodes: Optional[int] = None) -> None:
        """Ana eğitim döngüsü."""
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 5'te doldurulacak")

    def evaluate(self, num_episodes: int = 50) -> dict:
        """Eğitilmiş ajanı epsilon=0 ile değerlendir."""
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 5'te doldurulacak")
