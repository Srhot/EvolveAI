"""
EvolveAI — DQN Agent (Aşama 3)
================================

Deep Q-Network ajanı. RTX 5070 burada devreye giriyor.

KOMPONENTLER:
    - Online network (öğrenen)
    - Target network (kararlı hedefler için, her N adımda kopyalanır)
    - Replay buffer (uniform veya prioritized)
    - Epsilon-greedy exploration with decay
    - Double DQN target hesabı (overestimation azaltma)
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
except ImportError:
    raise ImportError("PyTorch yüklü değil.")

from config import CONFIG
from modules.dqn.networks import create_network
from modules.dqn.replay_buffer import ReplayBuffer, PrioritizedReplayBuffer


class DQNAgent:
    """Deep Q-Network ajanı.

    Özellikler (config.dqn'den okur):
        - USE_DUELING: True → DuelingDQN
        - USE_DOUBLE_DQN: True → action selection online net, value target net
        - USE_PRIORITIZED_REPLAY: True → PER buffer

    Yöntem:
        agent = DQNAgent()
        action = agent.select_action(state)
        agent.store_transition(s, a, r, s', done)
        agent.train_step()  # batch sample + gradient update
        if step % TARGET_UPDATE_FREQ == 0: agent.update_target()
    """

    def __init__(self):
        self.config = CONFIG.dqn
        self.device = torch.device(CONFIG.DEVICE)

        # Networks
        self.online_net = create_network(self.config.USE_DUELING).to(self.device)
        self.target_net = create_network(self.config.USE_DUELING).to(self.device)
        # TODO[Sonnet]: target_net.load_state_dict(online_net.state_dict()) ve target_net.eval()

        # Optimizer
        # TODO[Sonnet]: self.optimizer = optim.Adam(online_net.parameters(), lr=LEARNING_RATE)
        self.optimizer = None

        # Replay buffer
        if self.config.USE_PRIORITIZED_REPLAY:
            self.replay_buffer = PrioritizedReplayBuffer()
        else:
            self.replay_buffer = ReplayBuffer()

        # Epsilon schedule
        self.epsilon: float = self.config.EPSILON_START
        self.training_steps: int = 0

    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """Epsilon-greedy aksiyon seçimi.

        TODO[Sonnet]: Implement
            if training and random < self.epsilon:
                return random action
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
                q_values = self.online_net(state_tensor)
                return q_values.argmax(dim=-1).item()
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def store_transition(self, state, action, reward, next_state, done) -> None:
        """Buffer'a deneyim ekle."""
        self.replay_buffer.push(state, action, reward, next_state, done)

    def train_step(self) -> Optional[float]:
        """Bir gradient adımı.

        TODO[Sonnet]: Implement
            1. Buffer < WARMUP_STEPS ise None döndür (henüz eğitme)
            2. Batch sample (PER ise weights ve indices de gelir)
            3. Tensor'a çevir (.to(device))
            4. Q(s,a) hesapla: online_net(states).gather(1, actions)
            5. Target hesapla:
               - Double DQN: a* = online_net(next).argmax(); Q_target = target_net(next)[a*]
               - Vanilla:    Q_target = target_net(next).max()
               - target = reward + gamma * Q_target * (1 - done)
            6. Loss: PER ise weighted MSE, değilse F.smooth_l1_loss (Huber)
            7. optimizer.zero_grad(); loss.backward(); clip_grad_norm; optimizer.step()
            8. PER ise update_priorities(indices, td_errors)
            9. self._decay_epsilon()
            10. training_steps += 1
            11. return loss.item()
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def update_target(self) -> None:
        """Target network'ü online network ile senkronize et."""
        # TODO[Sonnet]: self.target_net.load_state_dict(self.online_net.state_dict())
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def _decay_epsilon(self) -> None:
        """Linear epsilon decay."""
        # TODO[Sonnet]: linear interpolation between EPSILON_START → EPSILON_END
        # over EPSILON_DECAY_STEPS
        progress = min(1.0, self.training_steps / self.config.EPSILON_DECAY_STEPS)
        self.epsilon = self.config.EPSILON_START + progress * (
            self.config.EPSILON_END - self.config.EPSILON_START
        )

    def save(self, path: Path) -> None:
        """Checkpoint kaydet."""
        # TODO[Sonnet]:
        # torch.save({
        #     "online_net": self.online_net.state_dict(),
        #     "target_net": self.target_net.state_dict(),
        #     "optimizer": self.optimizer.state_dict(),
        #     "training_steps": self.training_steps,
        #     "epsilon": self.epsilon,
        # }, path)
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def load(self, path: Path) -> None:
        """Checkpoint yükle."""
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def get_genome(self) -> np.ndarray:
        """Network ağırlıklarını düz vektör olarak çıkar (GA için).

        TODO[Sonnet]: Implement
            params = []
            for p in self.online_net.parameters():
                params.append(p.data.cpu().numpy().flatten())
            return np.concatenate(params)
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 8'de doldurulacak")

    def set_genome(self, genome: np.ndarray) -> None:
        """Düz vektörü network ağırlıklarına yerleştir (GA için).

        TODO[Sonnet]: Implement
            idx = 0
            for p in self.online_net.parameters():
                size = p.numel()
                p.data = torch.tensor(genome[idx:idx+size], dtype=torch.float32, device=device).reshape(p.shape)
                idx += size
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 8'de doldurulacak")
