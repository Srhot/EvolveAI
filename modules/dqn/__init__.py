"""DQN module — Stage 3: Deep RL with RTX 5070."""
# PyTorch gerektirir — yoksa graceful fallback
try:
    from modules.dqn.networks import DQNNetwork, DuelingDQN, create_network
    from modules.dqn.dqn_agent import DQNAgent
    from modules.dqn.trainer import DQNTrainer
except ImportError:
    DQNNetwork = DuelingDQN = create_network = None  # type: ignore
    DQNAgent = DQNTrainer = None  # type: ignore

# Replay buffer numpy ile çalışır, bağımsız
from modules.dqn.replay_buffer import ReplayBuffer, PrioritizedReplayBuffer

__all__ = [
    "DQNNetwork", "DuelingDQN", "create_network",
    "ReplayBuffer", "PrioritizedReplayBuffer",
    "DQNAgent", "DQNTrainer",
]
