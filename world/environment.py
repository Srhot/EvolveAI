"""
EvolveAI — World Environment
=============================

OpenAI Gymnasium uyumlu grid environment. Tüm RL ajanları bu env üzerinde eğitilir.

API ÖZET:
    env = GridWorld()
    obs, info = env.reset(seed=42)
    obs, reward, terminated, truncated, info = env.step(action)
    env.render()  # Pygame ile görselleştirir
    env.close()

REFERANSLAR:
    - Sutton & Barto (2018), "Reinforcement Learning: An Introduction" Chapter 3
    - Gymnasium API: https://gymnasium.farama.org/

KAPSAM:
    - 40x40 grid (config.py'den)
    - Multi-agent: aynı env'de 24 ajan paralel
    - Partial observability: her ajan VISION_RADIUS=5 hücre görür
    - Aksiyon: 6 (yukarı, sağ, aşağı, sol, saldır, bekle)
    - Reward shaping: kaynak +20, hayatta kalma +0.1/adım, ölüm -50
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:
    raise ImportError("Gymnasium yüklü değil: pip install gymnasium==0.29.1")

from config import CONFIG, get_state_dim
from world.entities import Agent, Resource, Obstacle


class GridWorld(gym.Env):
    """Multi-agent grid environment.

    State (her ajan için):
        - Local view: (2*vision+1)^2 hücre x 3 kanal (agent, resource, obstacle)
        - Self info: [health, energy, x_norm, y_norm]
        - Toplam boyut: get_state_dim() = 367 (orta seviye config için)

    Action space (Discrete 6):
        0: Yukarı  | 1: Sağ  | 2: Aşağı  | 3: Sol  | 4: Saldır  | 5: Bekle

    Reward (per agent, per step):
        +20.0   kaynak yerse
        +5.0    çarpışmada kazanırsa
        -5.0    çarpışmada kaybederse
        +0.1    hayatta kalma (her adım)
        -0.5    geçersiz hareket (engele/duvara çarpma)
        -50.0   ölüm (terminal)
    """

    metadata = {"render_modes": ["human", "rgb_array", "headless"], "render_fps": 30}

    def __init__(self, render_mode: Optional[str] = "headless"):
        super().__init__()

        self.config = CONFIG.world
        self.render_mode = render_mode

        # Action ve observation space (her ajan için aynı)
        self.action_space = spaces.Discrete(self.config.NUM_ACTIONS)
        self.observation_space = spaces.Box(
            low=-1.0, high=1.0, shape=(get_state_dim(),), dtype=np.float32
        )

        # State containers
        self.agents: List[Agent] = []
        self.resources: List[Resource] = []
        self.obstacles: List[Obstacle] = []
        self.step_count: int = 0
        self.episode_count: int = 0

        # Pygame renderer (lazy init)
        self._renderer = None

    # ------------------------------------------------------------------
    # CORE GYM API
    # ------------------------------------------------------------------
    def reset(
        self, seed: Optional[int] = None, options: Optional[dict] = None
    ) -> Tuple[Dict[int, np.ndarray], Dict[str, Any]]:
        """Environment'ı başlangıç durumuna sıfırla.

        TODO[Sonnet]: Implement
            1. RNG'yi seed ile başlat (super().reset(seed=seed))
            2. Engelleri rastgele yerleştir (NUM_OBSTACLES kadar, çakışmasız)
            3. Kaynakları rastgele yerleştir (engellerden uzak)
            4. NUM_AGENTS_PER_GENERATION kadar ajan yerleştir
            5. step_count = 0
            6. Her ajan için ilk gözlemi hesapla → dict {agent_id: obs}
            7. info dict'i: {"step": 0, "alive_agents": N}

        Returns:
            observations: {agent_id: np.ndarray} her ajan için lokal gözlem
            info: ek metadata
        """
        super().reset(seed=seed)
        # TODO: Implementation
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 2'de doldurulacak")

    def step(
        self, actions: Dict[int, int]
    ) -> Tuple[Dict[int, np.ndarray], Dict[int, float], Dict[int, bool], Dict[int, bool], Dict[str, Any]]:
        """Tüm ajanlar aynı anda aksiyon alır (synchronous multi-agent).

        TODO[Sonnet]: Implement
            1. Her ajan için aksiyonu uygula:
               - 0-3: Hareket et (sınır/engel kontrolü, MOVEMENT_ENERGY_COST düş)
               - 4: Saldır (komşu ajan varsa COMBAT_DAMAGE uygula)
               - 5: Bekle (enerji rejenerasyonu +1)
            2. Çarpışma çözümlemesi (aynı hücreye iki ajan)
            3. Kaynak toplama (ajan kaynağa basarsa enerji +20, kaynağı sil)
            4. Reward hesapla (yukarıdaki tabloya göre)
            5. Ölü ajanları işaretle (health <= 0 veya energy <= 0)
            6. step_count += 1, MAX_STEPS_PER_EPISODE'a ulaştıysa truncated
            7. Yeni gözlemleri hesapla
            8. info: {"alive": [...], "deaths_this_step": [...], "resources_left": N}

        Args:
            actions: {agent_id: action_int}

        Returns:
            observations, rewards, terminated (her ajan), truncated, info
        """
        # TODO: Implementation
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 2'de doldurulacak")

    def render(self) -> Optional[np.ndarray]:
        """Pygame ile görselleştir.

        TODO[Sonnet]: Implement
            - render_mode == "human": ekrana çiz
            - render_mode == "rgb_array": np.array döndür (replay için)
            - render_mode == "headless": None döndür
            - visualization/live_renderer.py'deki Renderer sınıfını kullan
        """
        if self.render_mode == "headless":
            return None
        # TODO: Lazy renderer init + render call
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 7'de doldurulacak")

    def close(self) -> None:
        """Kaynakları serbest bırak."""
        if self._renderer is not None:
            self._renderer.close()

    # ------------------------------------------------------------------
    # YARDIMCI METHODLAR
    # ------------------------------------------------------------------
    def _get_local_observation(self, agent: Agent) -> np.ndarray:
        """Ajanın lokal gözlemini hesapla.

        TODO[Sonnet]: Implement
            1. Agent'ın etrafında (2*VISION_RADIUS+1)^2 pencere oluştur
            2. 3 kanal:
               - Channel 0: diğer ajanlar (1.0 = ajan var, 0.0 = boş)
               - Channel 1: kaynaklar
               - Channel 2: engeller + sınır (luç dışı = -1.0)
            3. Düz vektöre çevir (flatten)
            4. Self info ekle: [health/100, energy/100, x/grid_w, y/grid_h]
            5. np.float32'ye dönüştür
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 2'de doldurulacak")

    def _is_valid_position(self, x: int, y: int) -> bool:
        """Pozisyon grid içinde mi ve engel yok mu?"""
        if not (0 <= x < self.config.GRID_SIZE[0]):
            return False
        if not (0 <= y < self.config.GRID_SIZE[1]):
            return False
        for obs in self.obstacles:
            if obs.x == x and obs.y == y:
                return False
        return True

    def get_state_snapshot(self) -> Dict[str, Any]:
        """Replay sistemi için anlık state snapshot'ı.

        TODO[Sonnet]: Implement
            - Tüm ajanların pozisyon, can, enerji, strateji tipi
            - Tüm kaynak ve engel pozisyonları
            - step_count
            - Bunu replays/{episode_id}.json'a yazmak için kullanılacak
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 11'de doldurulacak")
