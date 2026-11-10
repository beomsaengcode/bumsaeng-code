"""모든 공급자가 따르는 공통 모양.

주차 코드는 이 파일의 Reply와 Provider만 안다. 어느 회사 모델인지는 몰라도 된다.
"""
from dataclasses import dataclass, field
from typing import Any, Iterator, Optional


@dataclass
class Reply:
    text: str
    stop: str                 # end | length | refusal | other  (공급자마다 다른 이름을 통일)
    input_tokens: int
    output_tokens: int
    provider: str
    model: str
    request_id: str = ""
    native: Any = field(default=None, repr=False)   # 같은 공급자에게 다시 보낼 원래 응답 내용

    def as_message(self):
        """대화 기록에 붙일 assistant 메시지. 같은 공급자면 원래 내용을 그대로 다시 보낸다."""
        return {"role": "assistant", "content": self.text, "_native": self.native, "_provider": self.provider}


class Provider:
    name = "base"
    model = ""

    def chat(self, messages, system: Optional[str] = None, max_tokens: Optional[int] = None) -> Reply:
        raise NotImplementedError

    def stream(self, messages, system: Optional[str] = None, max_tokens: Optional[int] = None) -> Iterator[str]:
        """글자를 조금씩 내보내고, 다 끝나면 self.last 에 Reply를 남긴다."""
        reply = self.chat(messages, system, max_tokens)
        self.last = reply
        yield reply.text

    def count_tokens(self, text: str) -> Optional[int]:
        """입력 토큰 수. 셀 방법이 없는 공급자는 None."""
        return None


def plain(messages):
    """공통 메시지 → {role, content} 만 남긴 목록."""
    return [{"role": m["role"], "content": m["content"]} for m in messages]
