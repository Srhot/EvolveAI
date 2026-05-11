"""
EvolveAI — Tournament Bracket (Aşama 5)
=========================================

Şampiyonlar Ligi formatında eleme turnuvası. 16 ajan → 4 round → 1 şampiyon.

NEDEN ÖNEMLİ:
    - GA selection'dan bağımsız bir doğruluk kontrolü
    - Sunum gününde görsel olarak EN ŞOV YAPAN kısım
    - Hoca bracket diagramını hemen anlar (FIFA mantığı)

REFERANSLAR:
    - Elo (1978). "The Rating of Chessplayers, Past and Present"
    - Standart single-elimination bracket
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import numpy as np

from config import CONFIG


@dataclass
class Match:
    """Bir maç (best-of-3 by default)."""
    agent1_id: str
    agent2_id: str
    winner_id: Optional[str] = None
    score: Tuple[int, int] = (0, 0)  # (agent1 wins, agent2 wins)
    round_num: int = 0
    match_replays: list = field(default_factory=list)  # replay'lerin yolları


@dataclass
class Bracket:
    """Turnuva bracket veri yapısı."""
    rounds: List[List[Match]] = field(default_factory=list)
    champion_id: Optional[str] = None


class Tournament:
    """Single-elimination turnuva.

    Kullanım:
        tournament = Tournament(env=env, agents=[a1, a2, ..., a16])
        bracket = tournament.run()
        print(f"Şampiyon: {bracket.champion_id}")
    """

    def __init__(self, env=None, agents: List = None):
        self.config = CONFIG.tournament
        self.env = env
        self.agents = agents or []
        self.bracket = Bracket()

    def seed_agents(self) -> List:
        """Tohumlama — fitness'a göre sırala, en iyi en zayıfla eşleşsin.

        TODO[Sonnet]: Implement
            sorted_agents = sorted(self.agents, key=lambda a: a.fitness, reverse=True)
            n = len(sorted_agents)
            # Standart seeding: 1 vs 16, 2 vs 15, ...
            seeded_pairs = [(sorted_agents[i], sorted_agents[n-1-i]) for i in range(n//2)]
            return seeded_pairs
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 10'da doldurulacak")

    def play_match(self, agent1, agent2, round_num: int = 0) -> Match:
        """İki ajan arasında best-of-N maç oyna.

        TODO[Sonnet]: Implement
            match = Match(agent1.entity_id, agent2.entity_id, round_num=round_num)
            for _ in range(MATCHES_PER_PAIRING):
                # env'i sadece bu iki ajanla başlat
                # bir tarafın diğerini yenmesi veya max step'e kadar oynat
                # winner'a göre score güncelle
            match.winner_id = ... (more wins)
            update_elo(agent1, agent2, match.winner_id)
            return match
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 10'da doldurulacak")

    def update_elo(self, agent1, agent2, winner_id: str) -> None:
        """Elo rating güncelle.

        TODO[Sonnet]: Implement
            K = CONFIG.tournament.ELO_K_FACTOR
            R1, R2 = agent1.elo_rating, agent2.elo_rating
            E1 = 1 / (1 + 10 ** ((R2 - R1) / 400))
            E2 = 1 - E1
            S1 = 1.0 if winner_id == agent1.entity_id else 0.0
            S2 = 1.0 - S1
            agent1.elo_rating = R1 + K * (S1 - E1)
            agent2.elo_rating = R2 + K * (S2 - E2)
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 10'da doldurulacak")

    def run(self) -> Bracket:
        """Tam turnuvayı yürüt.

        TODO[Sonnet]: Implement
            seeded_pairs = self.seed_agents()
            current_round = [a for pair in seeded_pairs for a in pair]
            round_num = 0
            while len(current_round) > 1:
                matches = []
                next_round = []
                for i in range(0, len(current_round), 2):
                    match = self.play_match(current_round[i], current_round[i+1], round_num)
                    matches.append(match)
                    winner = ... (find agent by winner_id)
                    next_round.append(winner)
                self.bracket.rounds.append(matches)
                current_round = next_round
                round_num += 1
            self.bracket.champion_id = current_round[0].entity_id
            return self.bracket
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 10'da doldurulacak")

    def to_visualization_data(self) -> dict:
        """Plotly/Mermaid bracket diagramı için veri hazırla.

        TODO[Sonnet]: Implement
            {
                "rounds": [
                    {
                        "round_num": 0,
                        "matches": [{"a1": "id1", "a2": "id2", "winner": "id1", "score": "2-1"}, ...]
                    },
                    ...
                ],
                "champion": "agent_id"
            }
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 10'da doldurulacak")
