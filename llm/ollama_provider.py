"""Ollama (내 PC에서 도는 로컬 모델, 무료). 서버: http://localhost:11434
켜기: ollama serve (또는 ollama 앱) · 모델 받기: ollama pull qwen2.5:1.5b
"""

import json
import os

import requests

from .base import Provider, Reply, plain

STOP = {"stop": "end", "length": "length"}
HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


class OllamaProvider(Provider):
    name = "ollama"

    def __init__(self, model):
        self.model = model

    def _body(self, messages, system, max_tokens, stream):
        msgs = ([{"role": "system", "content": system}] if system else []) + plain(messages)
        body = {"model": self.model, "messages": msgs, "stream": stream}
        if max_tokens:
            body["options"] = {"num_predict": max_tokens}
        return body

    def _post(self, body, stream=False):
        try:
            r = requests.post(f"{HOST}/api/chat", json=body, stream=stream, timeout=300)
        except requests.ConnectionError as e:
            raise SystemExit("Ollama 서버가 꺼져 있어요. 켜고 다시 실행하세요 (ollama serve).") from e
        r.raise_for_status()
        return r

    def _reply(self, d, text):
        return Reply(
            text,
            STOP.get(d.get("done_reason"), "other"),
            d.get("prompt_eval_count", 0),
            d.get("eval_count", 0),
            self.name,
            d.get("model", self.model),
            d.get("created_at", ""),
        )

    def chat(self, messages, system=None, max_tokens=None):
        d = self._post(self._body(messages, system, max_tokens, False)).json()
        return self._reply(d, d["message"]["content"])

    def stream(self, messages, system=None, max_tokens=None):
        parts, last = [], {}
        for line in self._post(self._body(messages, system, max_tokens, True), stream=True).iter_lines():
            if not line:
                continue
            d = json.loads(line)
            piece = d.get("message", {}).get("content", "")
            if piece:
                parts.append(piece)
                yield piece
            if d.get("done"):
                last = d
        self.last = self._reply(last, "".join(parts))

    def count_tokens(self, text):
        d = self._post(self._body([{"role": "user", "content": text}], None, 1, False)).json()
        return d.get("prompt_eval_count")
