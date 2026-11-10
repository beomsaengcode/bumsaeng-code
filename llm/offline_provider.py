"""키가 없을 때: fixtures/ 의 예시 응답을 돌려준다(실측 아님)."""
import json
from pathlib import Path

from .base import Provider, Reply


class OfflineProvider(Provider):
    name, model = "offline", "offline-example"

    def __init__(self, fixtures_dir):
        self.dir = Path(fixtures_dir)
        self.turn = 0

    def _load(self, name):
        return json.loads((self.dir / name).read_text(encoding="utf-8"))

    def chat(self, messages, system=None, max_tokens=None):
        data = self._load("chat.json")
        single = data.get("single", {}).get(messages[-1]["content"]) if len(messages) == 1 else None
        turns = data["turns"]
        t = single or turns[min(self.turn, len(turns) - 1)]
        self.turn += 1
        return Reply(t["assistant"], "end", t["input_tokens"], t["output_tokens"], self.name, self.model, "offline-%d" % self.turn)

    def stream(self, messages, system=None, max_tokens=None):
        reply = self.chat(messages, system, max_tokens)
        self.last = reply
        for ch in reply.text:
            yield ch

    def count_tokens(self, text):
        counts = self._load("token_counts.json")["counts"]
        return counts.get(text)
