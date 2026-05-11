"""
EvolveAI — Configuration Module
================================

Bu dosya tüm proje için tek doğruluk kaynağıdır (single source of truth).
Path'ler, hiperparametreler, sabitler ve cihaz ayarları burada toplanmıştır.

KULLANIM:
    from config import CONFIG
    print(CONFIG.GRID_SIZE)
    print(CONFIG.DEVICE)

DEĞİŞİKLİK KURALLARI:
    1. Yeni bir parametre eklerken type hint koyun.
    2. Magic number'ları doğrudan koda yazmak YASAKTIR — buraya ekleyin.
    3. Path'leri os.path.join veya pathlib ile birleştirin (Windows uyumluluğu).
    4. Reproducibility için tüm random seed'ler buradan çekilmelidir.

Yazar: Serhat (github.com/Srhot)
Lisans: MIT
"""

from __future__ import annotations

import os
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple

import numpy as np

# ============================================================================
# REPRODUCIBILITY — Tüm rastgelelik buradan kontrol edilir
# ============================================================================
SEED: int = 42
random.seed(SEED)
np.random.seed(SEED)

# PyTorch seed'i lazy import içinde set edilir (PyTorch yüklü olmayabilir testlerde)
def _set_torch_seed() -> None:
    """PyTorch yüklendiğinde seed'i set et. Lazy import — config.py PyTorch'suz da çalışır."""
    try:
        import torch
        torch.manual_seed(SEED)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(SEED)
            # Deterministic algoritmalar için (yavaşlatır ama kararlı sonuç verir)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass


# ============================================================================
# PATH'LER — Windows + Linux uyumlu
# ============================================================================
PROJECT_ROOT: Path = Path(__file__).resolve().parent
CHECKPOINTS_DIR: Path = PROJECT_ROOT / "checkpoints"
REPLAYS_DIR: Path = PROJECT_ROOT / "replays"
LOGS_DIR: Path = PROJECT_ROOT / "logs"
ASSETS_DIR: Path = PROJECT_ROOT / "assets"
DOCS_DIR: Path = PROJECT_ROOT / "docs"

# Klasörler yoksa oluştur (idempotent)
for _dir in (CHECKPOINTS_DIR, REPLAYS_DIR, LOGS_DIR, ASSETS_DIR):
    _dir.mkdir(parents=True, exist_ok=True)


# ============================================================================
# CIHAZ — RTX 5070 için optimize
# ============================================================================
def _detect_device() -> str:
    """Cihazı otomatik tespit et. RTX 5070 → cuda, yoksa cpu."""
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
    except ImportError:
        pass
    return "cpu"


DEVICE: str = _detect_device()


# ============================================================================
# DÜNYA (WORLD) — Grid environment parametreleri
# ============================================================================
@dataclass(frozen=True)
class WorldConfig:
    """Grid dünya parametreleri. ORTA SEVIYE: 40x40 grid, kaynaklar + engeller."""

    GRID_SIZE: Tuple[int, int] = (40, 40)
    """(satır, sütun) — Orta seviye dünya. RTX 5070 için optimal."""

    NUM_AGENTS_PER_GENERATION: int = 24
    """Her nesilde aynı anda yarışan ajan sayısı. 24 = 2x12 turnuva bracket için ideal."""

    NUM_RESOURCES: int = 30
    """Haritada rastgele dağılmış kaynak (yiyecek/enerji) sayısı."""

    NUM_OBSTACLES: int = 50
    """Engel sayısı. Çevre karmaşıklığını ve strateji çeşitliliğini artırır."""

    MAX_STEPS_PER_EPISODE: int = 500
    """Bir maçın maksimum adım sayısı. Sonsuz döngüleri önler."""

    AGENT_INITIAL_HEALTH: float = 100.0
    AGENT_INITIAL_ENERGY: float = 100.0

    AGENT_VISION_RADIUS: int = 5
    """Ajan kendinden kaç hücre öteyi görür. Partial observability için kritik."""

    RESOURCE_VALUE: float = 20.0
    """Bir kaynak yendiğinde kazanılan enerji."""

    COMBAT_DAMAGE: float = 15.0
    """Çarpışmada kaybedilen can."""

    MOVEMENT_ENERGY_COST: float = 0.5
    """Her hareket için harcanan enerji."""

    # Aksiyon uzayı: 0=yukarı, 1=sağ, 2=aşağı, 3=sol, 4=saldır, 5=bekle
    NUM_ACTIONS: int = 6


# ============================================================================
# Q-LEARNING (Aşama 2) — Tablo tabanlı baseline
# ============================================================================
@dataclass(frozen=True)
class QLearningConfig:
    """Klasik Q-Learning (Watkins, 1989) parametreleri."""

    LEARNING_RATE: float = 0.1  # alpha
    DISCOUNT_FACTOR: float = 0.95  # gamma
    EPSILON_START: float = 1.0  # exploration başlangıç
    EPSILON_END: float = 0.05
    EPSILON_DECAY: float = 0.995  # her bölümde epsilon *= decay
    NUM_EPISODES: int = 2000
    """Q-tablo yakınsaması için yeterli bölüm sayısı."""

    # State discretization (Q-tablo için sürekli uzay → ayrık)
    STATE_BINS: int = 10
    """Her boyut kaç parçaya bölünecek. Tablo boyutu = STATE_BINS^state_dim."""


# ============================================================================
# DQN (Aşama 3) — RTX 5070 burada devreye giriyor
# ============================================================================
@dataclass(frozen=True)
class DQNConfig:
    """Deep Q-Network (Mnih et al., 2015) parametreleri."""

    # Mimari
    HIDDEN_LAYERS: Tuple[int, ...] = (256, 256, 128)
    USE_DUELING: bool = True
    """Dueling DQN — value + advantage ayrımı, %15 daha iyi yakınsama."""

    USE_DOUBLE_DQN: bool = True
    """Double DQN — Q-value overestimation'ı azaltır."""

    USE_PRIORITIZED_REPLAY: bool = True
    """Prioritized Experience Replay — önemli örnekleri daha sık örnekler."""

    # Hyperparameters
    LEARNING_RATE: float = 1e-4
    BATCH_SIZE: int = 128
    REPLAY_BUFFER_SIZE: int = 100_000
    TARGET_UPDATE_FREQUENCY: int = 1000
    """Target network'ün online network'e kopyalandığı adım aralığı."""

    GAMMA: float = 0.99

    # Training
    NUM_EPISODES: int = 5000
    WARMUP_STEPS: int = 5000
    """Buffer dolana kadar eğitim başlamaz (cold start sorunu)."""

    GRADIENT_CLIP: float = 10.0
    """Patlayan gradient'leri kontrol altında tutar."""

    # Epsilon schedule
    EPSILON_START: float = 1.0
    EPSILON_END: float = 0.05
    EPSILON_DECAY_STEPS: int = 50_000


# ============================================================================
# EVOLUTION (Aşama 4) — Genetik Algoritma katmanı
# ============================================================================
@dataclass(frozen=True)
class EvolutionConfig:
    """Strateji evrimi parametreleri. Bu projenin imza özelliği."""

    POPULATION_SIZE: int = 24  # WorldConfig.NUM_AGENTS_PER_GENERATION ile uyumlu
    NUM_GENERATIONS: int = 50

    # Selection
    SELECTION_METHOD: str = "tournament"  # "tournament" | "roulette" | "rank"
    TOURNAMENT_SIZE: int = 4
    ELITISM_RATIO: float = 0.10
    """En iyi %10 doğrudan sonraki nesle aktarılır (genetik kayıp önleme)."""

    # Crossover
    CROSSOVER_RATE: float = 0.7
    CROSSOVER_METHOD: str = "uniform"  # "uniform" | "single_point" | "two_point"

    # Mutation
    MUTATION_RATE: float = 0.05
    MUTATION_STRENGTH: float = 0.1
    """Bir gen mutasyona uğradığında değerin ne kadar değişeceği (Gaussian noise)."""

    # Strateji genom boyutu (DQN ağırlıkları + davranış parametreleri)
    GENOME_SIZE: int = 64
    """Bu sayı hem DQN katman boyutuna hem de davranış parametre sayısına bağlı."""

    # Fitness skoru ağırlıkları
    FITNESS_WEIGHTS: dict = field(default_factory=lambda: {
        "survival_time": 0.30,
        "resources_collected": 0.25,
        "combat_wins": 0.20,
        "exploration": 0.15,
        "energy_efficiency": 0.10,
    })


# ============================================================================
# TURNUVA (Aşama 5) — Bracket sistemi
# ============================================================================
@dataclass(frozen=True)
class TournamentConfig:
    """Turnuva parametreleri. Şampiyonlar Ligi formatı."""

    BRACKET_SIZE: int = 16  # 2^n olmalı (8, 16, 32)
    NUM_ROUNDS: int = 4  # log2(BRACKET_SIZE)

    MATCHES_PER_PAIRING: int = 3
    """Best-of-3 — şans faktörünü azaltır."""

    SEEDING_METHOD: str = "fitness"  # "fitness" | "random" | "elo"
    USE_ELO_RATING: bool = True
    ELO_K_FACTOR: int = 32  # Standart satranç K-factor


# ============================================================================
# GÖRSELLEŞTIRME (Pygame + Plotly + Gradio)
# ============================================================================
@dataclass(frozen=True)
class VizConfig:
    """Görselleştirme parametreleri."""

    # Pygame
    CELL_SIZE_PX: int = 16  # 40x40 grid * 16px = 640x640px pencere
    FPS: int = 30

    # Renk paleti — strateji tipi → renk
    STRATEGY_COLORS: dict = field(default_factory=lambda: {
        "aggressive": (220, 50, 50),     # Kırmızı — saldırgan
        "defensive": (50, 100, 220),     # Mavi — savunmacı
        "evasive": (50, 200, 100),       # Yeşil — kaçak
        "opportunist": (240, 200, 50),   # Sarı — fırsatçı
        "explorer": (180, 100, 220),     # Mor — kâşif (bonus tip)
    })

    # Genel UI
    BACKGROUND_COLOR: Tuple[int, int, int] = (25, 25, 30)
    GRID_LINE_COLOR: Tuple[int, int, int] = (60, 60, 70)
    RESOURCE_COLOR: Tuple[int, int, int] = (100, 220, 100)
    OBSTACLE_COLOR: Tuple[int, int, int] = (80, 80, 80)

    # Replay
    REPLAY_FORMAT: str = "json"  # "json" | "pickle"
    MAX_REPLAY_SIZE_MB: int = 50

    # Strategy radar
    RADAR_DIMENSIONS: Tuple[str, ...] = (
        "Aggression",      # Saldırı sıklığı
        "Defense",         # Kaçınma davranışı
        "Resource Greed",  # Kaynak toplama önceliği
        "Exploration",     # Yeni alan keşfi
        "Cooperation",     # Aynı tip ajanlardan kaçınma
        "Risk Tolerance",  # Düşük canla saldırma
    )


# ============================================================================
# GRADIO UYGULAMA
# ============================================================================
@dataclass(frozen=True)
class AppConfig:
    """Gradio uygulama parametreleri."""

    SERVER_NAME: str = "127.0.0.1"
    SERVER_PORT: int = 7860
    SHARE: bool = False  # True yapılırsa public link verir (sunum için kullanışlı)
    THEME: str = "soft"

    # Sekmeler
    TABS: Tuple[str, ...] = (
        "Live Battle",
        "Evolution Tree",
        "Tournament",
        "Strategy Analysis",
        "Replay Player",
    )


# ============================================================================
# LOGGING
# ============================================================================
@dataclass(frozen=True)
class LoggingConfig:
    """Log seviyeleri ve TensorBoard."""

    LOG_LEVEL: str = "INFO"  # DEBUG | INFO | WARNING | ERROR
    USE_TENSORBOARD: bool = True
    TENSORBOARD_LOG_DIR: Path = LOGS_DIR / "tensorboard"
    LOG_EVERY_N_EPISODES: int = 10
    SAVE_CHECKPOINT_EVERY_N_EPISODES: int = 100


# ============================================================================
# ANA KONFIG — Hepsini birleştir
# ============================================================================
@dataclass(frozen=True)
class Config:
    """Tüm alt konfigürasyonları birleştiren ana sınıf."""

    SEED: int = SEED
    DEVICE: str = DEVICE
    PROJECT_ROOT: Path = PROJECT_ROOT
    CHECKPOINTS_DIR: Path = CHECKPOINTS_DIR
    REPLAYS_DIR: Path = REPLAYS_DIR
    LOGS_DIR: Path = LOGS_DIR

    world: WorldConfig = field(default_factory=WorldConfig)
    qlearning: QLearningConfig = field(default_factory=QLearningConfig)
    dqn: DQNConfig = field(default_factory=DQNConfig)
    evolution: EvolutionConfig = field(default_factory=EvolutionConfig)
    tournament: TournamentConfig = field(default_factory=TournamentConfig)
    viz: VizConfig = field(default_factory=VizConfig)
    app: AppConfig = field(default_factory=AppConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)


# Singleton instance — her yerde aynısı kullanılır
CONFIG = Config()
_set_torch_seed()


# ============================================================================
# YARDIMCI FONKSIYONLAR
# ============================================================================
def get_state_dim() -> int:
    """Ajan'ın gözlemlediği state vektörünün boyutu.

    Vision radius * 2 + 1 = local grid kenarı.
    Her hücre için 3 kanal: agent_id, resource, obstacle.
    + 4 ek özellik: kendi can, enerji, x, y.
    """
    r = CONFIG.world.AGENT_VISION_RADIUS
    local_grid_cells = (2 * r + 1) ** 2
    channels = 3
    extras = 4
    return local_grid_cells * channels + extras


def print_summary() -> None:
    """Konfigürasyonun özetini bastır. Eğitim öncesi sanity check için."""
    print("=" * 60)
    print("EvolveAI — Configuration Summary")
    print("=" * 60)
    print(f"Seed:              {CONFIG.SEED}")
    print(f"Device:            {CONFIG.DEVICE}")
    print(f"Grid Size:         {CONFIG.world.GRID_SIZE}")
    print(f"Agents/Gen:        {CONFIG.world.NUM_AGENTS_PER_GENERATION}")
    print(f"State Dimension:   {get_state_dim()}")
    print(f"Action Space:      {CONFIG.world.NUM_ACTIONS}")
    print(f"DQN Episodes:      {CONFIG.dqn.NUM_EPISODES}")
    print(f"Evolution Gens:    {CONFIG.evolution.NUM_GENERATIONS}")
    print(f"Population Size:   {CONFIG.evolution.POPULATION_SIZE}")
    print(f"Tournament Size:   {CONFIG.tournament.BRACKET_SIZE}")
    print(f"Project Root:      {CONFIG.PROJECT_ROOT}")
    print("=" * 60)


if __name__ == "__main__":
    print_summary()
