"""
EvolveAI — Main Training Script
=================================

Komut satırı tek giriş noktası. Tüm eğitim aşamalarını çağırır.

KULLANIM:
    python train.py --stage qlearning    # Aşama 2
    python train.py --stage dqn          # Aşama 3
    python train.py --stage evolution    # Aşama 4
    python train.py --stage tournament   # Aşama 5
    python train.py --stage all          # Hepsi sırayla

GECE EĞİTİM ÖNERİSİ:
    python train.py --stage all > logs/overnight_$(date +%Y%m%d).log 2>&1

    Tahmini süre RTX 5070'te:
    - Q-Learning: 10 dk
    - DQN:         2 saat
    - Evolution:   5 saat (50 nesil x 24 ajan)
    - Tournament:  20 dk
    TOPLAM:        ~7.5 saat (bir gece yetiyor)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure project root in path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import CONFIG, print_summary


def train_qlearning():
    """Aşama 2 — Q-Learning baseline.

    TODO[Sonnet]: Implement
        from world import GridWorld
        from modules.qlearning import QLearningTrainer
        env = GridWorld(render_mode="headless")
        trainer = QLearningTrainer(env=env)
        trainer.train()
        trainer.agent.save(CONFIG.CHECKPOINTS_DIR / "qlearning_final.pkl")
    """
    print("\n=== STAGE 2: Q-Learning ===")
    raise NotImplementedError("Sonnet 4.6: HANDOFF Day 3")


def train_dqn():
    """Aşama 3 — DQN.

    TODO[Sonnet]: Implement
        from world import GridWorld
        from modules.dqn import DQNTrainer
        env = GridWorld(render_mode="headless")
        trainer = DQNTrainer(env=env)
        trainer.train()
        trainer.agent.save(CONFIG.CHECKPOINTS_DIR / "dqn_final.pt")
    """
    print("\n=== STAGE 3: DQN ===")
    raise NotImplementedError("Sonnet 4.6: HANDOFF Day 5")


def train_evolution():
    """Aşama 4 — Genetik algoritma evrim.

    TODO[Sonnet]: Implement
        from world import GridWorld
        from modules.evolution import EvolutionLoop
        from modules.dqn import DQNAgent
        env = GridWorld(render_mode="headless")
        weight_size = sum(p.numel() for p in DQNAgent().online_net.parameters())
        evo = EvolutionLoop(env=env, weight_size=weight_size)
        evo.run()
        evo.save_history(CONFIG.LOGS_DIR / "evolution_history.json")
    """
    print("\n=== STAGE 4: Evolution ===")
    raise NotImplementedError("Sonnet 4.6: HANDOFF Day 9")


def run_tournament():
    """Aşama 5 — Turnuva.

    TODO[Sonnet]: Implement
        Top-16 ajanı evolution sonucundan yükle.
        Tournament().run()
        Bracket'i logs/tournament_bracket.json'a kaydet.
    """
    print("\n=== STAGE 5: Tournament ===")
    raise NotImplementedError("Sonnet 4.6: HANDOFF Day 10")


def main():
    parser = argparse.ArgumentParser(description="EvolveAI Training")
    parser.add_argument(
        "--stage", type=str, default="all",
        choices=["qlearning", "dqn", "evolution", "tournament", "all"],
    )
    parser.add_argument("--seed", type=int, default=None, help="Override seed")
    args = parser.parse_args()

    print_summary()

    if args.stage == "qlearning" or args.stage == "all":
        train_qlearning()
    if args.stage == "dqn" or args.stage == "all":
        train_dqn()
    if args.stage == "evolution" or args.stage == "all":
        train_evolution()
    if args.stage == "tournament" or args.stage == "all":
        run_tournament()


if __name__ == "__main__":
    main()
