"""Live Battle Tab — Canlı simülasyon görüntüleme."""
import gradio as gr

def build():
    """TODO[Sonnet] HANDOFF Day 13: Live battle UI
    Components:
        - Start/Stop/Reset butonları
        - Generation seçici (slider)
        - Speed kontrolü (0.5x - 4x)
        - Live image output (her step'te güncellenen Pygame frame)
        - Stats panel: alive agents, step count, leading strategy
    Use gr.Image for live frame stream, gr.Button for controls.
    """
    with gr.Row():
        gr.Markdown("### 🎮 Live Battle Arena")
    with gr.Row():
        start_btn = gr.Button("▶️ Başlat", variant="primary")
        stop_btn = gr.Button("⏸️ Durdur")
        reset_btn = gr.Button("🔄 Sıfırla")
    with gr.Row():
        with gr.Column(scale=3):
            frame_display = gr.Image(label="Live Simulation", interactive=False)
        with gr.Column(scale=1):
            stats = gr.JSON(label="Live Stats")
    # TODO: callback'leri bağla
