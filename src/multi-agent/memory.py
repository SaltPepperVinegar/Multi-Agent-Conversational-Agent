from collections import deque
from typing import Deque, Dict, Any, List

class SharedMemory:
    def __init__(self, max_chars: int = 4000):
        self.max_chars = max_chars
        self.turns: Deque[Dict[str, Any]] = deque()  # [{"role": "user"/"agent", "agent": name, "content": text}]

    def add_user(self, text: str):
        self.turns.append({"role": "user", "agent": "user", "content": text})
        self._trim()

    def add_agent(self, agent_name: str, text: str):
        self.turns.append({"role": "agent", "agent": agent_name, "content": text})
        self._trim()

    def add_tool_event(self, tool_name: str, args: Any = None, output: Any = None):
        # Optional: record tool usage for transparency/debug
        self.turns.append({"role": "tool", "agent": tool_name, "content": f"args={args!r} | output={output!r}"})
        self._trim()

    def render_context(self) -> str:
        """Render a compact rolling context string for the next prompt."""
        lines: List[str] = ["[Conversation Context] (most recent first)"]
        for t in list(self.turns)[-20:]:  # last N turns; adjust if you like
            role = t["role"]
            who = t["agent"]
            content = t["content"].strip()
            if role == "user":
                lines.append(f"User: {content}")
            elif role == "agent":
                lines.append(f"{who}: {content}")
            elif role == "tool":
                lines.append(f"Tool[{who}]: {content}")
        return "\n".join(lines)

    def _trim(self):
        while len(self._all_text()) > self.max_chars and self.turns:
            self.turns.popleft()

    def _all_text(self) -> str:
        return "\n".join(f'{t["role"]}:{t["agent"]}:{t["content"]}' for t in self.turns)
