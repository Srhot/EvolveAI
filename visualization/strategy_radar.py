"""
EvolveAI — Strategy Radar Chart
================================

Her ajanın 6 boyutlu davranış profilini radar (örümcek) grafik olarak gösterir.

BOYUTLAR (config.viz.RADAR_DIMENSIONS):
    1. Aggression       — Saldırı sıklığı
    2. Defense          — Kaçınma davranışı
    3. Resource Greed   — Kaynak toplama önceliği
    4. Exploration      — Yeni alan keşfi
    5. Cooperation      — Aynı tip ajanlardan kaçınma
    6. Risk Tolerance   — Düşük canla saldırma

KULLANIM: Ajanı seç → radar chart üret → strateji tipini tahmin et.
"""

from __future__ import annotations

from typing import Dict, List

try:
    import plotly.graph_objects as go
except ImportError:
    raise ImportError("Plotly yüklü değil.")

from config import CONFIG


class StrategyRadarChart:
    """6 boyutlu strateji radarı."""

    def __init__(self):
        self.dimensions = CONFIG.viz.RADAR_DIMENSIONS

    def compute_profile(self, agent) -> Dict[str, float]:
        """Ajan istatistiklerinden 6 boyutlu profil çıkar.

        TODO[Sonnet]: Implement
            Her boyut için 0-1 arası normalize skor üret:
            {
                "Aggression": agent.kills / max(agent.steps_alive, 1) * 50,  # saldırı oranı
                "Defense": 1 - (damage_taken / max_damage),                  # kaçınma
                "Resource Greed": agent.resources_collected / NUM_RESOURCES,
                "Exploration": len(agent.cells_explored) / total_cells,
                "Cooperation": 1 - same_type_kills / max(1, agent.kills),
                "Risk Tolerance": low_hp_attacks / max(1, agent.kills),
            }
            np.clip her değeri [0, 1]'e
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 12'de doldurulacak")

    def plot_single(self, agent) -> go.Figure:
        """Tek ajan için radar.

        TODO[Sonnet]: Implement
            profile = self.compute_profile(agent)
            fig = go.Figure(data=go.Scatterpolar(
                r=list(profile.values()) + [list(profile.values())[0]],  # kapat
                theta=list(profile.keys()) + [list(profile.keys())[0]],
                fill="toself",
                name=f"Agent {agent.entity_id[:6]} ({agent.strategy_type})"
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])))
            return fig
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 12'de doldurulacak")

    def plot_comparison(self, agents: List, max_agents: int = 4) -> go.Figure:
        """Birden fazla ajanı aynı radar'da karşılaştır.

        TODO[Sonnet]: Implement
            Aynı figürde her ajan için bir Scatterpolar trace ekle.
            En fazla 4 ajan (kalabalık olmasın).
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 12'de doldurulacak")

    def plot_strategy_archetypes(self, population: List) -> go.Figure:
        """Tüm popülasyonu strateji tipine göre grupla, ortalama radar göster.

        TODO[Sonnet]: Implement
            Her strategy_type için ortalama profili hesapla → bir trace.
            Görsel olarak: "Saldırgan tipi nasıl davranır?" sorusunu cevaplar.
        """
        raise NotImplementedError("Sonnet 4.6: HANDOFF Day 12'de doldurulacak")
