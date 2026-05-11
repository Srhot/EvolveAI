"""
EvolveAI — DQN Networks (Aşama 3)
==================================

Deep Q-Network mimari tanımları. Dueling + Double DQN destekli.

REFERANSLAR:
    - Mnih et al. (2015), "Human-level control through deep reinforcement learning"
      → Vanilla DQN
    - Wang et al. (2016), "Dueling Network Architectures for Deep RL"
      → Dueling DQN
    - van Hasselt et al. (2016), "Deep Reinforcement Learning with Double Q-Learning"
      → Double DQN

MIMARI KARARI: MLP (CNN değil) — observation zaten flatten edilmiş 367-d vektör.
                CNN için raw pixel (örn. 40x40x3) input gerekirdi; bu projede
                lokal pencere zaten önişlenmiş feature vektörü.
"""

from __future__ import annotations

from typing import Tuple

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:
    raise ImportError("PyTorch yüklü değil. environment.yml'i kullanın.")

from config import CONFIG, get_state_dim


class DQNNetwork(nn.Module):
    """Vanilla DQN — referans/baseline mimari.

    Input:  state vector (367-d)
    Output: Q-values for each action (6-d)
    """

    def __init__(self, state_dim: int = None, action_dim: int = None,
                 hidden_layers: Tuple[int, ...] = None):
        super().__init__()
        state_dim = state_dim or get_state_dim()
        action_dim = action_dim or CONFIG.world.NUM_ACTIONS
        hidden_layers = hidden_layers or CONFIG.dqn.HIDDEN_LAYERS

        # TODO[Sonnet]: Implement
        # Layers oluştur: state_dim → hidden[0] → hidden[1] → ... → action_dim
        # Her katmanda ReLU activation, son katman raw Q-values (no activation)
        # nn.Sequential kullan, modüler olsun
        self.net = None  # placeholder
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class DuelingDQN(nn.Module):
    """Dueling DQN — Value ve Advantage stream'leri ayrı.

    Q(s,a) = V(s) + A(s,a) − mean(A(s,·))

    Bu ayrım hangi state'lerin önemli olduğunu öğrenmeyi kolaylaştırır.
    Ablation çalışmaları %15+ performans artışı gösterir (Wang et al. 2016).
    """

    def __init__(self, state_dim: int = None, action_dim: int = None,
                 hidden_layers: Tuple[int, ...] = None):
        super().__init__()
        state_dim = state_dim or get_state_dim()
        action_dim = action_dim or CONFIG.world.NUM_ACTIONS
        hidden_layers = hidden_layers or CONFIG.dqn.HIDDEN_LAYERS

        # TODO[Sonnet]: Implement Dueling architecture
        # 1. Shared feature extractor: state_dim → hidden[0] → hidden[1]
        # 2. Value stream: hidden[1] → hidden[2] → 1
        # 3. Advantage stream: hidden[1] → hidden[2] → action_dim
        # 4. forward: shared → split → V + (A - A.mean(dim=-1, keepdim=True))
        self.feature_layer = None
        self.value_stream = None
        self.advantage_stream = None
        self.action_dim = action_dim
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass — Q(s,a) = V(s) + A(s,a) − mean(A)."""
        # TODO[Sonnet]:
        # features = self.feature_layer(x)
        # value = self.value_stream(features)        # shape: (B, 1)
        # advantage = self.advantage_stream(features) # shape: (B, action_dim)
        # return value + advantage - advantage.mean(dim=-1, keepdim=True)
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 4'te doldurulacak")


def create_network(use_dueling: bool = True) -> nn.Module:
    """Factory function — config'e göre network seç."""
    if use_dueling:
        return DuelingDQN()
    return DQNNetwork()
