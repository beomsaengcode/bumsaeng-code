"""공급자 고르기.

LLM_PROVIDER = claude | openai | ollama | offline   (비우면 키가 있는 쪽을 자동 선택, 없으면 offline)
LLM_MODEL    = 모델 이름 (비우면 공급자 기본값)
"""
import os
from pathlib import Path

from .base import Provider, Reply  # noqa: F401
from .prices import cost  # noqa: F401

DEFAULT_MODEL = {"claude": "claude-opus-5-5", "openai": "gpt-5-mini", "ollama": "qwen2.5:1.5b"}


def get_provider(fixtures_dir=None) -> Provider:
    name = os.environ.get("LLM_PROVIDER", "").lower()
    if not name:
        name = "claude" if os.environ.get("ANTHROPIC_API_KEY") else "openai" if os.environ.get("OPENAI_API_KEY") else "offline"
    model = os.environ.get("LLM_MODEL") or DEFAULT_MODEL.get(name, "")
    if name == "ollama":
        from .ollama_provider import OllamaProvider
        return OllamaProvider(model)
    if name == "openai":
        from .openai_provider import OpenAIProvider
        return OpenAIProvider(model)
    if name == "claude":
        try:
            from .claude_provider import ClaudeProvider
        except ImportError:
            raise SystemExit("Claude 공급자는 실제 API로 검증한 뒤 추가됩니다(검증 대기). LLM_PROVIDER=openai 또는 offline을 쓰세요.")
        return ClaudeProvider(model)
    from .offline_provider import OfflineProvider
    return OfflineProvider(fixtures_dir or Path.cwd() / "fixtures")
