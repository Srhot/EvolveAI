# EvolveAI — Multi-Agent Strategy Evolution

> **Pekiştirmeli öğrenme + genetik algoritma hibrit yaklaşımıyla, oyun ajanlarının nesiller boyunca yarışarak farklı stratejileri "doğal seçilim" ile keşfetmesi.**

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)]()
[![PyTorch 2.1](https://img.shields.io/badge/pytorch-2.1-red.svg)]()
[![CUDA 12.1](https://img.shields.io/badge/CUDA-12.1-green.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

---

## 🎯 Proje Özeti

**EvolveAI**, klasik tek-ajanlı pekiştirmeli öğrenmenin (RL) ötesine geçerek, bir grid dünyada **24 yapay zeka ajanını eş zamanlı yarıştırır**. Her ajan kendi içinde DQN ile öğrenirken, **genetik algoritma katmanı nesiller arası strateji aktarımını** yönetir. Sonuç: kimse ona "saldırgan ol" demediği halde **kendiliğinden ortaya çıkan dört farklı strateji arketipi** (saldırgan, savunmacı, kaçak, fırsatçı).

### Bu projenin akademik özgünlüğü

| Klasik RL | EvolveAI |
|---|---|
| Tek ajan, sabit ortam | 24 ajan, birbirine karşı |
| Tek tip strateji yakınsar | Çoklu strateji eş zamanlı evrim |
| Strateji önceden tanımlanmış | Strateji POST-HOC K-Means ile çıkar |
| Statik fitness | Multi-objective (5 boyutlu) |

---

## 🏗️ Mimari

Beş aşamalı pipeline:

```
Aşama 1: Grid Dünya          → world/ (Gymnasium uyumlu environment)
Aşama 2: Q-Learning Baseline → modules/qlearning/ (tablo tabanlı, "neden DQN gerekli?")
Aşama 3: DQN (RTX 5070)      → modules/dqn/ (Dueling + Double + PER)
Aşama 4: Evolution Loop      → modules/evolution/ (selection + crossover + mutation)
Aşama 5: Tournament Bracket  → tournament/ (Elo + best-of-3 + bracket)
```

### Modüler tasarım

Her modül **bağımsız** — başka projelere taşınabilir:

```python
from modules.dqn import DQNAgent       # Soulingo'da kullanabilirsin
from modules.evolution import Genome   # Trading bot'ta kullanabilirsin
```

---

## 🚀 Kurulum

### Önkoşullar
- Windows 10/11 (Linux/macOS da çalışır)
- Anaconda veya Miniconda
- RTX 5070 / RTX 3060+ (CUDA destekli GPU önerilir)
- 16 GB RAM, 5 GB disk alanı

### Adım adım

```powershell
# 1. Repoyu klonla
git clone https://github.com/Srhot/EvolveAI.git
cd EvolveAI

# 2. Conda ortamı oluştur
conda env create -f environment.yml
conda activate evolveai

# 3. Sanity check
python config.py
python -m pytest tests/test_smoke.py -v

# 4. Eğitimi başlat (tüm aşamalar)
python train.py --stage all

# 5. Gradio arayüzünü aç
python -m app.main_app
# → http://127.0.0.1:7860
```

---

## 📊 Görsel Arayüz

5 sekmeli Gradio paneli:

| Sekme | İçerik |
|---|---|
| 🎮 **Live Battle** | Pygame ile gerçek zamanlı simülasyon, renk kodlu ajanlar |
| 🌳 **Evolution Tree** | Fitness eğrisi + strateji dağılımı + soy ağacı (Plotly) |
| 🏆 **Tournament** | 16'lı bracket diagramı + Elo leaderboard |
| 📊 **Strategy Analysis** | 6 boyutlu radar chart + K-Means archetypes |
| ⏯️ **Replay Player** | Önceki maçları seç, oynat, MP4 export |

---

## 🧪 Teknik Detaylar

### Reinforcement Learning katmanı
- **Algoritma**: Dueling Double DQN with Prioritized Experience Replay
- **State**: 367 boyutlu (11x11 lokal görüş x 3 kanal + 4 self info)
- **Action**: 6 (yukarı, sağ, aşağı, sol, saldır, bekle)
- **Reward shaping**: Multi-objective (kaynak, hayatta kalma, savaş, keşif)

### Evolutionary katman
- **Genome**: Neural weights (~10k boyut) + 6 boyutlu behavior params
- **Selection**: Tournament (k=4) + %10 elitism
- **Crossover**: Uniform (0.7 olasılık)
- **Mutation**: Gaussian (rate=0.05, strength=0.1)

### Performans hedefleri
| Metrik | Hedef |
|---|---|
| DQN yakınsaması | <2 saat (RTX 5070) |
| 50 nesil evrim | <5 saat |
| Episode başına FPS (render off) | >500 |
| Toplam pipeline | <8 saat |

---

## 📚 Referanslar

- Mnih et al. (2015). *Human-level control through deep reinforcement learning.* Nature 518.
- Wang et al. (2016). *Dueling Network Architectures for Deep Reinforcement Learning.* ICML.
- van Hasselt et al. (2016). *Deep Reinforcement Learning with Double Q-Learning.* AAAI.
- Schaul et al. (2016). *Prioritized Experience Replay.* ICLR.
- Salimans et al. (2017). *Evolution Strategies as a Scalable Alternative to RL.* OpenAI.
- Sutton & Barto (2018). *Reinforcement Learning: An Introduction.* MIT Press.
- Eiben & Smith (2015). *Introduction to Evolutionary Computing.* Springer.

---

## 👤 Yazar

**Serhat** — Yazılım Mühendisliği son sınıf, AI/ML araştırmacısı
GitHub: [@Srhot](https://github.com/Srhot)

---

## 📄 Lisans

MIT License — eğitim ve araştırma amaçlı serbestçe kullanılabilir.
