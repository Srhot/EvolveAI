"""Replay Player Tab — Önceki maçları seç ve oynat."""
import gradio as gr

def build():
    """TODO[Sonnet] HANDOFF Day 13:
    Components:
        - Replay dosyası seçici (Dropdown - replays/ klasöründen)
        - Play/Pause/Stop kontrolleri
        - Speed slider (0.25x - 4x)
        - Progress bar
        - Frame display
        - Metadata panel (generation, episode, winner, duration)
        - Export to MP4 butonu (sunum yedeği için)
    """
    gr.Markdown("### ⏯️ Replay Player")
    with gr.Row():
        replay_select = gr.Dropdown(label="Select Replay", choices=[])
        load_btn = gr.Button("📂 Load")
    with gr.Row():
        with gr.Column(scale=3):
            replay_display = gr.Image(label="Playback", interactive=False)
        with gr.Column(scale=1):
            metadata_display = gr.JSON(label="Match Info")
    with gr.Row():
        play_btn = gr.Button("▶️")
        pause_btn = gr.Button("⏸️")
        speed = gr.Slider(0.25, 4.0, value=1.0, step=0.25, label="Speed")
    with gr.Row():
        export_mp4 = gr.Button("📥 Export MP4 (sunum yedeği)")
