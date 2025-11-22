import gradio as gr
from market_research_agents import run_market_research_pipeline


def run_pipeline_ui(brief: str):
    brief = (brief or "").strip()
    if not brief:
        msg = (
            "Per favore inserisci un brief di mercato.\n"
            "Esempio: 'Voglio lanciare una app di fitness per studenti universitari in Europa...'"
        )
        return msg, "", "", ""

    results = run_market_research_pipeline(brief)

    final_presentation = results.get("final_presentation", "")
    research_brief = results.get("research_brief", "")
    market_analysis = results.get("market_analysis", "")
    strategy_report = results.get("strategy_report", "")

    return final_presentation, research_brief, market_analysis, strategy_report


CUSTOM_CSS = """
.summary-box {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 0.95rem;
    line-height: 1.6;
}
.detail-box {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 0.85rem;
    line-height: 1.5;
}
"""

with gr.Blocks(theme="soft", css=CUSTOM_CSS) as demo:
    gr.Markdown(
        """
# 💼 Market Research Multi-Agent (Ollama)

Inserisci un breve *market brief* (in italiano o inglese) e il sistema eseguirà:

1. **Data Gatherer** → raccoglie e organizza le informazioni sul mercato  
2. **Analyst** → costruisce un'analisi di mercato strutturata  
3. **Strategist** → propone strategia, SWOT e raccomandazioni  
4. **Presenter** → genera un executive summary pronto per le slide
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            brief_input = gr.Textbox(
                label="Brief di mercato",
                placeholder=(
                    "Esempio:\n"
                    "Voglio lanciare una app mobile di fitness per studenti universitari in Europa.\n"
                    "L'app offre allenamenti brevi, gamification e sconti con palestre partner...\n"
                ),
                lines=8,
            )
            run_button = gr.Button("Esegui analisi multi-agent", variant="primary")

        with gr.Column(scale=1):
            final_summary = gr.Markdown(
                label="Executive summary (Presenter)",
                value="Qui apparirà il riepilogo finale pronto per le slide.",
                elem_classes=["summary-box"],
            )

    gr.Markdown("### 🔍 Dettaglio degli step (opzionale)")

    with gr.Tab("Research Brief (Data Gatherer)"):
        research_out = gr.Markdown(
            label="Research brief",
            value="Output del Data Gatherer.",
            elem_classes=["detail-box"],
        )

    with gr.Tab("Analisi di mercato (Analyst)"):
        analysis_out = gr.Markdown(
            label="Analisi di mercato",
            value="Output dell'Analyst.",
            elem_classes=["detail-box"],
        )

    with gr.Tab("Strategia (Strategist)"):
        strategy_out = gr.Markdown(
            label="Report strategico",
            value="Output dello Strategist.",
            elem_classes=["detail-box"],
        )

    run_button.click(
        fn=run_pipeline_ui,
        inputs=brief_input,
        outputs=[final_summary, research_out, analysis_out, strategy_out],
    )

if __name__ == "__main__":
    demo.launch()