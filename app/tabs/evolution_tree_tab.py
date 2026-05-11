"""Evolution Tree Tab — Fitness eğrisi + soy ağacı + strateji dağılımı."""
import gradio as gr

def build():
    """TODO[Sonnet] HANDOFF Day 13:
    Components:
        - Generation range slider
        - 3 plot: fitness_curve, strategy_distribution, lineage_tree
        - Refresh butonu (eğitim devam ederken güncel veriyi çek)
        - Download butonu (PDF/PNG export)
    """
    gr.Markdown("### 🌳 Evolution Tree & Fitness Analysis")
    with gr.Row():
        fitness_plot = gr.Plot(label="Fitness Curve")
        strategy_plot = gr.Plot(label="Strategy Distribution")
    with gr.Row():
        lineage_plot = gr.Plot(label="Lineage Tree")
    refresh_btn = gr.Button("🔄 Refresh Data")
    # TODO: load_evolution_history() → visualization.EvolutionTreeVisualizer
