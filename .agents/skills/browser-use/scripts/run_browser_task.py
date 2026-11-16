"""
Browser-Use Automation CLI Runner.
Provides a standardized CLI runner to execute natural language web tasks via browser-use.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an autonomous browser automation task using browser-use."
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="Natural language instruction for the browser agent.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (default: False / visible browser).",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=25,
        help="Maximum action steps before terminating (default: 25).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("BROWSER_USE_MODEL", "gpt-4o"),
        help="Model name to use (default: gpt-4o or BROWSER_USE_MODEL env).",
    )
    parser.add_argument(
        "--user-data-dir",
        type=str,
        default=None,
        help="Path to store persistent browser session data/cookies.",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=None,
        help="Path to save the final task result as text/markdown.",
    )
    return parser.parse_args()


async def execute_task(args: argparse.Namespace) -> str:
    try:
        from browser_use import Agent, Browser, BrowserConfig
    except ImportError:
        print(
            "Error: 'browser-use' is not installed in the active environment.\n"
            "Please install it using:\n"
            "  pip install browser-use playwright langchain-openai\n"
            "  playwright install",
            file=sys.stderr,
        )
        sys.exit(1)

    # Initialize LLM based on environment
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if openai_key or not gemini_key:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model=args.model)
    else:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        except ImportError:
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model=args.model)

    browser_config = BrowserConfig(
        headless=args.headless,
        user_data_dir=args.user_data_dir,
    )
    browser = Browser(config=browser_config)

    print(f"[*] Starting agent with task: {args.task}")
    print(f"[*] Headless: {args.headless} | Max steps: {args.max_steps}")

    agent = Agent(
        task=args.task,
        llm=llm,
        browser=browser,
        max_actions_per_step=1,
    )

    history = await agent.run(max_steps=args.max_steps)
    final_output = history.final_result() or "Task completed without text summary."
    return str(final_output)


def main() -> None:
    args = parse_args()
    result = asyncio.run(execute_task(args))

    print("\n" + "=" * 50)
    print("Agent Execution Completed")
    print("=" * 50)
    print(result)

    if args.output_file:
        out_path = Path(args.output_file)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(result, encoding="utf-8")
        print(f"\n[*] Output saved to: {out_path.resolve()}")


if __name__ == "__main__":
    main()
