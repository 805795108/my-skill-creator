"""Shared utilities for skill-creator scripts."""

import os
import subprocess
from pathlib import Path


def detect_platform() -> str:
    """Detect the current runtime environment."""
    if os.environ.get("CLAUDECODE"):
        return "claude-code"
    if os.environ.get("CURSOR_SESSION_ID"):
        return "cursor"
    return "generic"


def _call_llm_claude_cli(prompt: str, model: str | None, timeout: int) -> str:
    """Call LLM via the claude CLI (claude -p)."""
    cmd = ["claude", "-p", "--output-format", "text"]
    if model:
        cmd.extend(["--model", model])
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    result = subprocess.run(
        cmd, input=prompt, capture_output=True, text=True,
        env=env, timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"claude -p exited {result.returncode}\nstderr: {result.stderr}"
        )
    return result.stdout


def _call_llm_anthropic_sdk(prompt: str, model: str | None, timeout: int) -> str:
    """Call LLM via the Anthropic Python SDK (requires ANTHROPIC_API_KEY)."""
    try:
        import anthropic
    except ImportError:
        raise RuntimeError(
            "anthropic package is required for SDK-based LLM calls. "
            "Install it with: pip install anthropic"
        )

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY environment variable is required for "
            "Anthropic SDK calls. Set it before running this script."
        )

    client = anthropic.Anthropic(api_key=api_key, timeout=timeout)
    message = client.messages.create(
        model=model or "claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def call_llm(prompt: str, model: str | None = None, timeout: int = 300) -> str:
    """Unified LLM invocation entry point. Selects the call method based on platform.

    Supported platforms:
    - claude-code / generic: uses claude CLI (claude -p)
    - cursor: uses Anthropic Python SDK (requires ANTHROPIC_API_KEY),
              falls back to claude CLI if SDK is unavailable
    """
    platform = detect_platform()

    if platform in ("claude-code", "generic"):
        return _call_llm_claude_cli(prompt, model, timeout)

    if platform == "cursor":
        if os.environ.get("ANTHROPIC_API_KEY"):
            return _call_llm_anthropic_sdk(prompt, model, timeout)
        return _call_llm_claude_cli(prompt, model, timeout)

    raise NotImplementedError(
        f"Platform '{platform}' does not yet support automatic LLM calls. "
        f"Add an adapter in scripts/utils.py call_llm()."
    )



def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Parse a SKILL.md file, returning (name, description, full_content)."""
    content = (skill_path / "SKILL.md").read_text()
    lines = content.split("\n")

    if lines[0].strip() != "---":
        raise ValueError("SKILL.md missing frontmatter (no opening ---)")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise ValueError("SKILL.md missing frontmatter (no closing ---)")

    name = ""
    description = ""
    frontmatter_lines = lines[1:end_idx]
    i = 0
    while i < len(frontmatter_lines):
        line = frontmatter_lines[i]
        if line.startswith("name:"):
            name = line[len("name:"):].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            value = line[len("description:"):].strip()
            # Handle YAML multiline indicators (>, |, >-, |-)
            if value in (">", "|", ">-", "|-"):
                continuation_lines: list[str] = []
                i += 1
                while i < len(frontmatter_lines) and (frontmatter_lines[i].startswith("  ") or frontmatter_lines[i].startswith("\t")):
                    continuation_lines.append(frontmatter_lines[i].strip())
                    i += 1
                description = " ".join(continuation_lines)
                continue
            else:
                description = value.strip('"').strip("'")
        i += 1

    return name, description, content
