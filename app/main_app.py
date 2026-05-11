"""
EvolveAI — Gradio Main Application
====================================

Demo gününün tek tıkla başlatma noktası.

SEKMELER:
    1. Live Battle       — Canlı simülasyon (Pygame embed veya video stream)
    2. Evolution Tree    — Fitness eğrisi + soy ağacı + strateji dağılımı
    3. Tournament        — 16'lı bracket görselleştirme
    4. Strategy Analysis — Radar charts, K-Means clustering, archetypes
    5. Replay Player     — Önceki maçları seç ve oynat

KULLANIM:
    python -m app.main_app
    → http://127.0.0.1:7860 aç
"""

from __future__ import annotations

try:
    import gradio as gr
except ImportError:
    raise ImportError("Gradio yüklü değil: pip install gradio==4.19.2")

from config import CONFIG
from app.tabs import (
    live_battle_tab,
    evolution_tree_tab,
    tournament_tab,
    strategy_analysis_tab,
    replay_player_tab,
)


def build_app() -> gr.Blocks:
    """Gradio uygulamasını oluştur.

    TODO[Sonnet]: Implement
        with gr.Blocks(theme=gr.themes.Soft(), title="EvolveAI") as app:
            gr.Markdown("# EvolveAI — Multi-Agent Strategy Evolution")
            gr.Markdown("RL + Genetic Algorithm hybrid for emergent strategy discovery")

            with gr.Tabs():
                with gr.Tab("🎮 Live Battle"):
                    live_battle_tab.build()
                with gr.Tab("🌳 Evolution Tree"):
                    evolution_tree_tab.build()
                with gr.Tab("🏆 Tournament"):
                    tournament_tab.build()
                with gr.Tab("📊 Strategy Analysis"):
                    strategy_analysis_tab.build()
                with gr.Tab("⏯️ Replay Player"):
                    replay_player_tab.build()

        return app
    """
    raise NotImplementedError("Sonnet 4.6: HANDOFF Day 13'te doldurulacak")


def main():
    """Uygulamayı başlat."""
    app = build_app()
    app.launch(
        server_name=CONFIG.app.SERVER_NAME,
        server_port=CONFIG.app.SERVER_PORT,
        share=CONFIG.app.SHARE,
    )


if __name__ == "__main__":
    main()
