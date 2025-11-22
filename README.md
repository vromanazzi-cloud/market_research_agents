# 🧠 Multi-Agent Market Research (Ollama)

A **multi-agent** market research pipeline that runs locally using **Ollama**.  
It takes a free-form market brief as input and processes it through several specialized agents
(data gathering, analysis, strategy, and presentation).

---

## ✨ Features

- **Multi-agent architecture** with 4 distinct roles:
  1. **Data Gatherer** – expands and structures the market brief.
  2. **Analyst** – builds a structured market analysis (segments, target, competitors, risks/opportunities).
  3. **Strategist** – proposes a go-to-market strategy and actionable recommendations.
  4. **Presenter** – generates an executive summary ready to paste into slides or documents.

- Runs entirely **locally** using:
  - [Ollama](https://ollama.com/) to host the LLM.
  - A configurable model (default: `llama3.2:2.2-instruct-q8`).

---

## 🧱 Code Architecture

Main file: `market_research_agents.py` (or your preferred script name).

Key components:

- `AgentConfig` (`@dataclass`)
  - `name`: human-readable agent name (e.g., `"Data Gatherer"`).
  - `system_prompt`: role-specific instructions.
  - `temperature`: creativity/variability level for that agent.

- **Agents defined:**
  - `DATA_GATHERER`
  - `ANALYST`
  - `STRATEGIST`
  - `PRESENTER`

- `call_llm(system_prompt, user_prompt, temperature)`
  - Generic function wrapping `ollama.chat(...)`:
    - `system_prompt` is sent as a system message.
    - `user_prompt` is sent as a user message.
    - `temperature` is passed via `options`.

- `run_agent(agent: AgentConfig, user_prompt: str) -> str`
  - Logs which agent is running.
  - Calls `call_llm` with the agent configuration.
  - Prints the agent output to the console.

- `run_market_research_pipeline(user_brief: str) -> Dict[str, Any]`
  - Orchestrates the full pipeline:
    1. `Data Gatherer` → `research_brief`
    2. `Analyst` → `market_analysis`
    3. `Strategist` → `strategy_report`
    4. `Presenter` → `final_presentation`
  - Returns a dictionary containing all intermediate results.

- `if __name__ == "__main__":`
  - Simple **CLI** interface:
    - Reads the user brief from stdin (multiple lines).
    - Runs the full multi-agent pipeline.
    - Prints the final **EXECUTIVE SUMMARY** to stdout.

---

## 🛠 Requirements

- **Python** 3.9 or newer (recommended)
- **Ollama** installed and running
- A supported model available in Ollama, e.g.:

```bash
ollama pull llama3.2:2.2-instruct-q8