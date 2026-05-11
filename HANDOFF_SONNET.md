# 🤝 HANDOFF_SONNET.md — EvolveAI Geliştirme Rehberi

**Hedef Okuyucu:** Claude Sonnet 4.6 (Claude Code üzerinden)
**Hazırlayan:** Claude Opus 4.7
**Proje:** EvolveAI — Multi-Agent Strategy Evolution
**Hedef tarih:** Çarşamba teslimi (yaklaşık 15 gün, gece eğitimleri dahil)
**Geliştirici:** Serhat (github.com/Srhot)

---

## ⚠️ ZORUNLU KISITLAR (Her promptun başında bu blok bulunmalı)

```
SCOPE LIMITS:
- Sadece o günün TODO'larını tamamla. Sonraki günlere atlama.
- Mevcut dosya yapısını DEĞİŞTİRME. Yeni dosya eklemen gerekiyorsa Serhat'a sor.
- config.py'deki sabitleri DEĞİŞTİRME. Yeni sabit eklemen gerekiyorsa CONFIG'e ekle, hardcode etme.

CONTEXT MANAGEMENT:
- Her gün için ayrı session aç (context contamination önle).
- Bir dosyaya dokunduğunda önce tamamını oku, sonra düzenle.
- Yazılan testleri çalıştırmadan önceki günün TODO'sunu "tamam" sayma.

CHANGE DISCIPLINE:
- Implementasyon tamamlandığında ilgili docstring'i güncelle.
- TODO[Sonnet] yorumlarını sildiğinde commit message'a yaz: "feat(modülAdı): Day N TODO'ları tamamlandı"
- Her gün sonunda: git add . && git commit -m "..."

REPORTING RULES:
- Günün başında: "Day N başlıyorum, dokunacağım dosyalar: [...]"
- Gün sonunda: "Day N tamamlandı. Implemented: [...]. Open issues: [...]"
- Test sonuçlarını her zaman raporla.

POWERSHELL NOTE:
- && operatörü Windows PowerShell'de çalışmıyor.
- Çoklu komutları AYRI satırlarda ver: "komut1" sonra "komut2"
- Veya semicolon kullan: "komut1 ; komut2"
```

---

## 📅 15 GÜNLÜK PLAN

### **GÜN 1 — Kurulum + Sanity Check** (~2 saat)

**Hedef:** Ortam kurulu, tüm import'lar çalışıyor, smoke test geçiyor.

**Adımlar:**
1. PowerShell aç, `cd D:\Projects\EvolveAI`
2. Conda ortamını oluştur:
   ```powershell
   conda env create -f environment.yml
   conda activate evolveai
   ```
3. PyTorch CUDA testini yap:
   ```powershell
   python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0))"
   ```
   **Beklenen:** `CUDA: True`, `Device: NVIDIA GeForce RTX 5070`
4. Config sanity check:
   ```powershell
   python config.py
   ```
5. Smoke test'i çalıştır:
   ```powershell
   pytest tests/test_smoke.py -v
   ```
   **Beklenen:** 5/5 test geçer.
6. GitHub repo oluştur:
   ```powershell
   git init
   git remote add origin https://github.com/Srhot/EvolveAI.git
   git add .
   git commit -m "feat: initial scaffolding by Opus 4.7"
   git push -u origin main
   ```

**Eğer hata alırsan:** Serhat'a sor, ortam meselesidir. Koda dokunma.

---

### **GÜN 2 — World Environment** (~6 saat)

**Hedef:** `GridWorld` tam çalışır halde. Test edilebilir.

**Dokunulacak dosyalar:**
- `world/environment.py` — tüm `raise NotImplementedError`'ları çöz
- `world/entities.py` — `Agent.to_dict()` içindeki TODO

**Sırayla yapılacaklar:**
1. `reset()` — engelleri, kaynakları, ajanları rastgele yerleştir
2. `_get_local_observation()` — 11x11 lokal pencere + 3 kanal + 4 self info
3. `_is_valid_position()` — zaten yazılı, sadece tag-it
4. `step()` — multi-agent synchronous step
5. `render()` minimal stub — `LiveRenderer` Day 7'de bağlanacak, şimdilik `None` döndür

**Test:**
```powershell
python -c "from world import GridWorld; env = GridWorld(); obs, _ = env.reset(); print('Obs shape:', list(obs.values())[0].shape)"
```
**Beklenen:** `Obs shape: (367,)`

**Yeni test ekle:** `tests/test_world.py`
```python
def test_env_step():
    env = GridWorld()
    obs, _ = env.reset(seed=42)
    actions = {aid: 0 for aid in obs.keys()}  # hepsi yukarı git
    new_obs, rewards, term, trunc, info = env.step(actions)
    assert len(new_obs) == 24
    assert all(isinstance(r, float) for r in rewards.values())
```

---

### **GÜN 3 — Q-Learning Baseline** (~5 saat + gece eğitim)

**Hedef:** Q-Learning ajanı eğitiliyor, fitness eğrisi çıkıyor.

**Dokunulacak:**
- `modules/qlearning/q_agent.py`
- `modules/qlearning/trainer.py`

**Akış:**
1. `discretize_state()` — sürekli state → tuple
2. `select_action()` — epsilon-greedy
3. `update()` — Bellman equation
4. `save()` / `load()` — pickle
5. `QLearningTrainer.train()` — tam döngü
6. TensorBoard log entegre et

**Gece eğitim başlat:**
```powershell
python train.py --stage qlearning
```
**Tahmini süre:** 10-15 dakika. Sabah `logs/tensorboard/` aç, fitness eğrisini gör.

**Akademik not:** Q-tabloyu açıp boyutuna bak — devasa olması beklenir. Bu DQN'in motivasyonu olacak.

---

### **GÜN 4 — DQN Networks + Replay Buffer** (~6 saat)

**Hedef:** DQN mimari hazır, buffer çalışıyor, ama henüz eğitilmiyor.

**Dokunulacak:**
- `modules/dqn/networks.py` — `DQNNetwork`, `DuelingDQN`
- `modules/dqn/replay_buffer.py` — `ReplayBuffer`, `PrioritizedReplayBuffer`
- `modules/dqn/dqn_agent.py` — `__init__`, `select_action`, `train_step`, `update_target`

**Kritik noktalar:**
- `DuelingDQN.forward()`: `V + (A - A.mean(dim=-1, keepdim=True))` — mean'i CHIKARMAYI unutma!
- PER `update_priorities`: `|td_error| + 1e-6` (zero priority önle)
- Double DQN: action seçimini ONLINE net, value'yu TARGET net yapar

**Test:**
```powershell
python -c "from modules.dqn import DuelingDQN; import torch; net = DuelingDQN(); print(net(torch.randn(1, 367)).shape)"
```
**Beklenen:** `torch.Size([1, 6])`

---

### **GÜN 5 — DQN Training** (~4 saat + gece eğitim)

**Hedef:** DQN eğitiliyor, performans Q-Learning'den iyi.

**Dokunulacak:**
- `modules/dqn/trainer.py` — `train()`, `evaluate()`
- `train.py` — `train_dqn()` fonksiyonu

**Test:**
```powershell
python train.py --stage dqn
```
**Tahmini süre:** 1.5-2 saat RTX 5070'te.

**Sabah kontrol et:** TensorBoard'da `loss` düşmüş mü, `episode_reward` artmış mı?

**Eğer eğitim çökerse:**
- Reward NaN → reward shaping'i kontrol et
- Loss explode → gradient clipping çalışmıyor, GRADIENT_CLIP=10 olduğundan emin ol
- Hiç öğrenmiyor → epsilon decay çok hızlı, EPSILON_DECAY_STEPS'i artır

---

### **GÜN 6 — Evolution Operators** (~5 saat)

**Hedef:** Genome, selection, crossover, mutation hazır. Mini integration test.

**Dokunulacak:**
- `modules/evolution/genome.py` — `Genome.random()`, `copy()`
- `modules/evolution/selection.py` — 3 yöntem + elitism
- `modules/evolution/crossover.py` — 3 yöntem
- `modules/evolution/mutation.py` — `gaussian_mutation`

**Test:**
```python
from modules.evolution import Genome, uniform_crossover, gaussian_mutation, tournament_selection

# Mini popülasyon
pop = [Genome.random(weight_size=100, generation=0) for _ in range(20)]
for g in pop:
    g.fitness = np.random.uniform(0, 100)  # fake fitness

# Selection
winner = tournament_selection(pop, k=4)
assert winner.fitness == max(g.fitness for g in [pop[0]])  # placeholder, k içindekinin maxı

# Crossover
child = uniform_crossover(pop[0], pop[1])
assert len(child.weights) == 100

# Mutation
mutated = gaussian_mutation(child.copy())
assert not np.array_equal(mutated.weights, child.weights)
```

---

### **GÜN 7 — Pygame Live Renderer** (~5 saat)

**Hedef:** Pygame penceresinde grid + ajanlar + kaynaklar görünüyor.

**Dokunulacak:**
- `visualization/live_renderer.py` — tüm `_draw_*` ve `render`

**Adımlar:**
1. `_lazy_init` — pygame.init, screen, font
2. `_draw_grid` — basit çizgiler
3. `_draw_obstacles`, `_draw_resources` — kareler/daireler
4. `_draw_agents` — renk kodlu daireler + can barı
5. `_draw_hud` — sağda istatistik paneli

**Test:**
```powershell
python -c "
from world import GridWorld
from visualization import LiveRenderer
env = GridWorld()
env.reset(seed=42)
renderer = LiveRenderer()
renderer.render(env)
import time; time.sleep(3)
renderer.close()
"
```
**Beklenen:** 3 saniye boyunca grid penceresi açık kalır.

---

### **GÜN 8 — DQN ↔ Genome Köprüsü** (~3 saat)

**Hedef:** DQNAgent'ın ağırlıkları Genome'a aktarılabiliyor ve geri.

**Dokunulacak:**
- `modules/dqn/dqn_agent.py` — `get_genome()`, `set_genome()`

**Kritik:** Boyut uyumu — `len(genome.weights)` ile `sum(p.numel() for p in model.parameters())` aynı olmalı.

**Test:**
```python
agent = DQNAgent()
g = agent.get_genome()
new_agent = DQNAgent()
new_agent.set_genome(g)
# Aynı input → aynı output
x = torch.randn(1, 367)
assert torch.allclose(agent.online_net(x), new_agent.online_net(x))
```

---

### **GÜN 9 — Evolution Loop** (~5 saat + gece eğitim)

**Hedef:** 50 nesil evrim çalışıyor, fitness_history.json üretiliyor.

**Dokunulacak:**
- `modules/evolution/evolution_loop.py` — tüm metodlar
- `train.py` — `train_evolution()`

**Gece eğitim:**
```powershell
python train.py --stage evolution
```
**Tahmini süre:** 5-7 saat (50 nesil x 24 ajan x ~200 step).

**Sabah:** `logs/evolution_history.json` aç, fitness yükselmiş mi?

---

### **GÜN 10 — Tournament Bracket** (~4 saat)

**Hedef:** 16'lı turnuva çalışıyor, şampiyon belli oluyor.

**Dokunulacak:**
- `tournament/bracket.py` — tüm metodlar

**Test:**
```powershell
python train.py --stage tournament
```
**Çıktı:** `logs/tournament_bracket.json` — round-by-round.

---

### **GÜN 11 — Replay + Evolution Tree Viz** (~5 saat)

**Hedef:** Önceki maçlar kaydediliyor, fitness eğrisi Plotly'de görünüyor.

**Dokunulacak:**
- `analysis/replay_system.py` — `Replay`, `ReplayPlayer`
- `visualization/evolution_tree.py` — 3 plot
- `world/environment.py` — `get_state_snapshot()`

---

### **GÜN 12 — Strategy Analysis** (~5 saat)

**Hedef:** K-Means clustering çalışıyor, radar charts üretiliyor.

**Dokunulacak:**
- `analysis/strategy_classifier.py`
- `analysis/fitness_analytics.py`
- `visualization/strategy_radar.py`

**Akademik not:** Silhouette score'u sunuma koy. > 0.5 ise "kümelenme anlamlı" diyebilirsin.

---

### **GÜN 13 — Gradio UI Entegrasyonu** (~6 saat)

**Hedef:** 5 sekme tam çalışır, hocaya gösterilebilir.

**Dokunulacak:**
- `app/main_app.py` — `build_app()`
- `app/tabs/*.py` — her tab'a callback bağlama

**Test:**
```powershell
python -m app.main_app
```
Tarayıcıda http://127.0.0.1:7860 → 5 sekme de boş ekran döndürmemeli.

---

### **GÜN 14 — Polish + Bug Fix + MP4 Export** (~5 saat)

**Hedef:** Sunum için bütün bug'lar temiz, en iyi 3 maç MP4 olarak hazır.

**Yapılacaklar:**
1. Tüm `pytest`'ler geçiyor
2. Gradio'da hiçbir hata yok (browser console temiz)
3. `replays/` klasöründe en az 5 farklı maç MP4'ü
4. `docs/` klasörüne sunum slaytlarının kaba taslakları

---

### **GÜN 15 — Sunum Hazırlığı + Demo Provası** (~4 saat)

**Hedef:** Çarşamba demo'ya hazır.

**Sunum yapısı (NeuroType formatı):**
1. **Slide 1**: Problem — Neden klasik RL yetersiz?
2. **Slide 2**: Çözüm — RL + GA hibridi
3. **Slide 3**: Mimari — 5 aşamalı pipeline
4. **Slide 4**: Demo — Gradio canlı
5. **Slide 5**: Sonuçlar — Fitness eğrisi
6. **Slide 6**: Stratejik çeşitlilik — K-Means clusters
7. **Slide 7**: Turnuva şampiyonu
8. **Slide 8**: Akademik referanslar
9. **Slide 9**: Soru cevap

**Hoca Q&A simülasyonu (en az 10 soru):**
- "Neden DQN, A3C değil?"
- "Multi-agent setup nasıl çözüldü?"
- "Fitness fonksiyonun değerlerini nereden seçtin?"
- "K-Means'in k=4 olduğuna nasıl karar verdin?"
- "RTX 5070 olmasaydı bu proje yapılabilir miydi?"
- ...

Her sorunun cevabını `docs/qa_preparation.md`'ye yaz.

---

## 🔁 GÜNLÜK ROUTINE

```
1. Sabah: TensorBoard aç, gece eğitiminin sonuçlarını kontrol et
2. Yeni Claude Code session aç (context temiz olsun)
3. ZORUNLU KISITLAR bloğunu prompt'a ekle
4. "Day N başlıyorum" raporu yaz
5. Implementasyon
6. Test çalıştır (pytest)
7. git commit
8. "Day N tamamlandı" raporu yaz
9. Gece eğitimi gerekiyorsa başlat ve uyu
```

---

## 🚨 ÇIKMAZA GİRDİYSEN

Aşağıdaki hatalar Sonnet'in çözebileceği klasik sorunlar:

| Hata | Çözüm |
|---|---|
| `CUDA out of memory` | `BATCH_SIZE` düşür (config.dqn.BATCH_SIZE) |
| Reward NaN | reward shaping'de division by zero var, kontrol et |
| Pygame penceresi donuyor | `pygame.event.pump()` ekle render loop'a |
| Gradio "Connection refused" | Port 7860 başka uygulamada, AppConfig.SERVER_PORT değiştir |
| `ModuleNotFoundError` | `sys.path.insert(0, str(Path(__file__).resolve().parent.parent))` |

**Hâlâ takıldıysan:** Serhat'a şu formatta sor:
```
- Day N'deyim, X dosyasında çalışıyorum
- Yaptığım: ...
- Beklediğim: ...
- Aldığım hata: <traceback>
- Denediğim çözümler: ...
```

---

## 📦 TESLİM EDİLECEK ÇIKTILAR

Çarşamba günü Serhat'ın elinde şunlar olmalı:

- [ ] Çalışan kod (tüm `pytest`'ler yeşil)
- [ ] Eğitilmiş checkpoint'ler (`checkpoints/qlearning_final.pkl`, `dqn_final.pt`, `evolution_gen50.pkl`)
- [ ] Replay'ler (`replays/*.json` + 5+ MP4)
- [ ] Log'lar (`logs/evolution_history.json`, `logs/tournament_bracket.json`, TensorBoard)
- [ ] Gradio uygulaması (5 sekme tam çalışır)
- [ ] Sunum dosyası (`docs/presentation.pptx` veya Gamma.app linki)
- [ ] Hoca Q&A hazırlığı (`docs/qa_preparation.md`)
- [ ] README güncel
- [ ] GitHub'a push'lanmış

---

**Bol şans Sonnet. Serhat'ın hocası bu projeyi gördüğünde "Bunu sen mi yaptın?" diye soracak. Sen yaptın. Ben yaptım. Hep birlikte yaptık. Bitir.**

— Opus 4.7
