"""Tournament Tab — 16'lı bracket görselleştirme."""
import gradio as gr

def build():
    """TODO[Sonnet] HANDOFF Day 13:
    Components:
        - Tournament başlat butonu
        - Bracket diagram (Plotly veya custom HTML/CSS)
        - Round-by-round match details (table)
        - Champion celebration UI
        - Elo leaderboard
    """
    gr.Markdown("### 🏆 Tournament Bracket")
    with gr.Row():
        start_tournament = gr.Button("🏁 Turnuvayı Başlat", variant="primary")
    with gr.Row():
        bracket_display = gr.Plot(label="Bracket Diagram")
    with gr.Row():
        with gr.Column():
            matches_table = gr.Dataframe(label="Match Results", headers=["Round", "Agent 1", "Agent 2", "Score", "Winner"])
        with gr.Column():
            leaderboard = gr.Dataframe(label="Elo Leaderboard", headers=["Rank", "Agent", "Elo Rating", "W/L"])
