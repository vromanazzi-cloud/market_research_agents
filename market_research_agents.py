from dataclasses import dataclass
from typing import Dict, Any

# ==============================
# 0. Configurazione Ollama
# ==============================
# Assicurati di avere:
#   1. Ollama installato e in esecuzione
#   2. Il modello corretto già scaricato, ad es.:
#      ollama pull llama3.2:3b-instruct-q8_0
#   3. La libreria Python:
#      pip install ollama
#
import ollama 

OLLAMA_MODEL_ID = "llama3.2:3b-instruct-q8_0"  # aggiorna se il nome del modello è diverso


# =========================
# 1. Configurazione agenti
# =========================

@dataclass
class AgentConfig:
    name: str
    system_prompt: str
    temperature: float


DATA_GATHERER = AgentConfig(
    name="Data Gatherer",
    temperature=0.4,
    system_prompt=(
        "Sei un analista di ricerche di mercato di primo livello.\n"
        "Riceverai un breve 'market brief' dall'utente.\n\n"
        "Compito:\n"
        "- Espandi e struttura le informazioni sul mercato target.\n"
        "- Identifica:\n"
        "  * dimensione e trend generali del mercato (anche qualitativi, non numeri precisi),\n"
        "  * target principale e sotto-segmenti,\n"
        "  * tipologie di competitor e alternative,\n"
        "  * problemi/bisogni che il prodotto vuole risolvere.\n"
        "- Organizza la risposta in sezioni con titoli chiari.\n"
        "- Non dare ancora raccomandazioni strategiche: solo raccolta e sintesi delle informazioni."
    ),
)

ANALYST = AgentConfig(
    name="Analyst",
    temperature=0.3,
    system_prompt=(
        "Sei un analista di mercato senior.\n"
        "Riceverai:\n"
        "- il brief iniziale dell'utente,\n"
        "- un 'research brief' preparato dal Data Gatherer.\n\n"
        "Compito:\n"
        "- Costruisci una vera analisi di mercato strutturata.\n"
        "- In particolare fornisci:\n"
        "  * Segmentazione del mercato (per target / bisogno / canale).\n"
        "  * Insight chiave del target (motivazioni, barriere, driver decisionali).\n"
        "  * Analisi competitor: categorie di competitor, punti di forza/debolezza.\n"
        "- Evidenzia le opportunità e i rischi principali per chi entra in questo mercato.\n"
        "- Non passare ancora a raccomandazioni strategiche di dettaglio."
    ),
)

STRATEGIST = AgentConfig(
    name="Strategist",
    temperature=0.5,
    system_prompt=(
        "Sei un marketing strategist esperto di go-to-market.\n"
        "Riceverai:\n"
        "- il brief dell'utente,\n"
        "- il research brief del Data Gatherer,\n"
        "- l'analisi di mercato dell'Analyst.\n\n"
        "Compito:\n"
        "- Proporre una strategia per entrare nel mercato.\n"
        "- Fornisci:\n"
        "  * Posizionamento proposto (chi siamo, per chi, perché siamo diversi).\n"
        "  * SWOT (Strengths, Weaknesses, Opportunities, Threats).\n"
        "  * 3-5 raccomandazioni operative (es. pricing, canali di acquisizione, feature chiave, partnership).\n"
        "- Sii concreto e coerente con l'analisi precedente."
    ),
)

PRESENTER = AgentConfig(
    name="Presenter",
    temperature=0.6,
    system_prompt=(
        "Sei un consulente che deve preparare un executive summary per slide.\n"
        "Riceverai:\n"
        "- il brief originale,\n"
        "- il research brief,\n"
        "- l'analisi di mercato,\n"
        "- il report strategico.\n\n"
        "Compito:\n"
        "- Crea un output pensato per essere copiato in una presentazione.\n"
        "- Organizza in sezioni:\n"
        "  1. Contesto & obiettivo.\n"
        "  2. Insight di mercato (bullet).\n"
        "  3. Sintesi SWOT.\n"
        "  4. Raccomandazioni chiave (3-5 bullet).\n"
        "- Usa uno stile sintetico, chiaro, con elenchi puntati facili da leggere."
    ),
)


# ==================================
# 2. Funzione generica per un agent
# ==================================

def call_llm(system_prompt: str, user_prompt: str, temperature: float) -> str:
    """
    Chiama il modello locale Ollama (OLLAMA_MODEL_ID)
    usando system_prompt come messaggio di sistema e user_prompt
    come input utente. La temperatura viene passata nelle options.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    response = ollama.chat(
        model=OLLAMA_MODEL_ID,
        messages=messages,
        options={"temperature": float(temperature)},
    )

    content = response.get("message", {}).get("content", "")
    return content.strip()


def run_agent(agent: AgentConfig, user_prompt: str) -> str:
    print(f"\n=== {agent.name} in esecuzione... ===")
    result = call_llm(
        system_prompt=agent.system_prompt,
        user_prompt=user_prompt,
        temperature=agent.temperature,
    )
    print(f"\n--- Output {agent.name} ---\n{result}\n")
    return result


# =============================
# 3. Orchestrazione multi-agent
# =============================

def run_market_research_pipeline(user_brief: str) -> Dict[str, Any]:
    """
    Esegue la pipeline di Market Research:
    1) Data Gatherer
    2) Analyst
    3) Strategist
    4) Presenter
    Restituisce un dizionario con tutti gli output intermedi.
    """

    # 1) Data Gatherer
    dg_prompt = (
        "Brief di mercato fornito dall'utente:\n\n"
        f"{user_brief}\n\n"
        "Preparare ora un 'research brief' strutturato come richiesto."
    )
    research_brief = run_agent(DATA_GATHERER, dg_prompt)

    # 2) Analyst
    analyst_prompt = (
        "Brief iniziale dell'utente:\n\n"
        f"{user_brief}\n\n"
        "Research brief preparato dal Data Gatherer:\n\n"
        f"{research_brief}\n\n"
        "Ora produci l'analisi di mercato come da istruzioni."
    )
    market_analysis = run_agent(ANALYST, analyst_prompt)

    # 3) Strategist
    strategist_prompt = (
        "Brief iniziale dell'utente:\n\n"
        f"{user_brief}\n\n"
        "Research brief del Data Gatherer:\n\n"
        f"{research_brief}\n\n"
        "Analisi di mercato dell'Analyst:\n\n"
        f"{market_analysis}\n\n"
        "Ora proponi la strategia come da istruzioni."
    )
    strategy_report = run_agent(STRATEGIST, strategist_prompt)

    # 4) Presenter
    presenter_prompt = (
        "Brief iniziale dell'utente:\n\n"
        f"{user_brief}\n\n"
        "Research brief (Data Gatherer):\n\n"
        f"{research_brief}\n\n"
        "Analisi di mercato (Analyst):\n\n"
        f"{market_analysis}\n\n"
        "Report strategico (Strategist):\n\n"
        f"{strategy_report}\n\n"
        "Ora genera un executive summary pronto da copiare in slide."
    )
    final_presentation = run_agent(PRESENTER, presenter_prompt)

    return {
        "research_brief": research_brief,
        "market_analysis": market_analysis,
        "strategy_report": strategy_report,
        "final_presentation": final_presentation,
    }


# ============
# 4. Main CLI
# ============

if __name__ == "__main__":
    print("🔹 Multi-Agent Market Research (Ollama)")
    print("Scrivi il tuo brief di mercato (più righe).")
    print("Quando hai finito, premi INVIO su una riga vuota.\n")

    lines = []
    try:
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
    except EOFError:
        # fine input (es. CTRL+D)
        pass

    user_brief = "\n".join(lines).strip()

    if not user_brief:
        print("Nessun brief inserito. Uscita.")
    else:
        print("\n✅ Brief ricevuto, avvio la pipeline multi-agent...\n")
        results = run_market_research_pipeline(user_brief)
        print("\n===== EXECUTIVE SUMMARY =====\n")
        print(results["final_presentation"])