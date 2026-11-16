---
name: browser-use
description: "Autonomous web browsing and agentic web automation using browser-use and Playwright. Enables AI agents to interact with websites, fill forms, execute multi-tab workflows, and extract structured data using vision and DOM tree parsing."
metadata:
  category: automation
  origin: browser-use
---

# Browser Use — Autonomous Web Automation & Scraping

`browser-use` enables AI agents to autonomously control and interact with real web browsers. It connects Large Language Models (LLMs) with Playwright and Chrome DevTools Protocol (CDP) to perceive web pages via accessibility/DOM trees and screenshots, executing actions like clicking, typing, scrolling, multi-tab switching, and structured extraction.

---

## When to Use

- **Autonomous Web Workflows**: When a task requires navigating complex dynamic websites (SPAs, React/Vue/Angular apps, infinite scroll).
- **Interactive Form Filling & RPA**: Logging into portals, filling multi-step questionnaires, or submitting reports.
- **Deep Web Data Extraction**: Extracting structured data from web pages that have anti-scraping protections or lack public APIs.
- **Visual E2E Verification & Audit**: Validating layout rendering, visual states, and user journeys across real browser sessions.
- **Multi-Tab Research**: Opening search results in background tabs, comparing prices/specs, and aggregating results.

---

## Prerequisites & Installation

To run `browser-use` scripts, ensure Python 3.11+ is installed along with browser dependencies:

```bash
# Install core library and playwright
pip install browser-use playwright langchain-openai langchain-google-genai pydantic

# Install browser binaries
playwright install
```

---

## Architecture & Core Concepts

1. **`Agent`**: The central orchestrator that receives a natural-language task prompt, executes the loop (observe -> reason -> act -> verify), and returns the final result.
2. **`Browser` / `BrowserConfig`**: Controls the Chromium instance (headless vs. headed, proxy, user-agent, viewport, persistent session context).
3. **`Controller`**: Registry for built-in browser actions (click, type, open tab, scroll) and custom user-defined tools (`@controller.action`).
4. **DOM Extraction & Vision**: Uses a lightweight accessibility/DOM indexing algorithm to assign index labels to interactable elements, combined with screenshot vision analysis.

---

## Recommended Patterns

### 1. Basic Autonomous Task
```python
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def main():
    agent = Agent(
        task="Navigate to news.ycombinator.com, find the top 3 stories, and return their titles and URLs.",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    history = await agent.run()
    print(history.final_result())

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Structured Output with Pydantic
Extract typed data directly into structured schemas:

```python
import asyncio
from pydantic import BaseModel, Field
from typing import List
from browser_use import Agent
from langchain_openai import ChatOpenAI

class ProductItem(BaseModel):
    name: str = Field(description="Name or title of the product")
    price: str = Field(description="Price including currency symbol")
    rating: str = Field(description="Customer rating score if available", default="")

class ProductList(BaseModel):
    products: List[ProductItem]

async def main():
    agent = Agent(
        task="Go to amazon.com, search for 'mechanical keyboard wireless', and extract the first 5 results.",
        llm=ChatOpenAI(model="gpt-4o"),
        controller_output_model=ProductList,
    )
    history = await agent.run()
    result = history.final_result()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Custom Controller Actions (Injecting Tools)
Extend the agent with domain-specific Python functions:

```python
import asyncio
from browser_use import Agent, Controller
from langchain_openai import ChatOpenAI

controller = Controller()

@controller.action("Save extracted content to a local markdown file")
def save_to_file(filename: str, content: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Saved successfully to {filename}"

async def main():
    agent = Agent(
        task="Visit python.org, extract the latest news headline, and save it to 'python_news.md'.",
        llm=ChatOpenAI(model="gpt-4o"),
        controller=controller,
    )
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### 4. Browser Session Persistence & Headless Control
```python
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI

browser = Browser(
    config=BrowserConfig(
        headless=False,                 # Set True for CI/CD or background runs
        user_data_dir="./.browser_data", # Persist login cookies and session cache
    )
)

agent = Agent(
    task="Check dashboard metrics on staging.example.com",
    llm=ChatOpenAI(model="gpt-4o"),
    browser=browser,
)
```

---

## Safety & Operational Guardrails

1. **Read-Only by Default**:
   - For production websites, avoid mutating operations (e.g., checkout buttons, delete actions, account modifications) unless explicitly instructed with verified test credentials.
2. **Credential Redaction**:
   - Never hardcode API keys or user passwords into prompts or agent scripts. Load them via environment variables (`.env`).
   - Ensure screenshots or DOM dumps generated during tasks do not expose auth tokens or PII.
3. **Execution Limits**:
   - Always set `max_steps` (default typically 100, recommended 15-25 for focused tasks) to prevent infinite navigation loops or runaway token usage.
4. **Anti-Bot & Rate Limits**:
   - Use reasonable delays between actions if needed and run with persistent browser profiles when interacting with sites requiring continuous sessions.

---

## Workspace Runner Helper

A reusable CLI helper script is available at:
`scripts/run_browser_task.py`

Run tasks directly:
```bash
python .agents/skills/browser-use/scripts/run_browser_task.py --task "Search Google for latest LangChain release" --headless
```
