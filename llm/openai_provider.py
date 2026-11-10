"""OpenAI (Chat Completions). 키: OPENAI_API_KEY."""

from .base import Provider, Reply, plain

STOP = {"stop": "end", "length": "length", "content_filter": "refusal"}


class OpenAIProvider(Provider):
    name = "openai"

    def __init__(self, model):
        from openai import OpenAI

        self.client, self.model = OpenAI(), model

    def _msgs(self, messages, system):
        return ([{"role": "system", "content": system}] if system else []) + plain(messages)

    def chat(self, messages, system=None, max_tokens=None):
        r = self.client.chat.completions.create(
            model=self.model, messages=self._msgs(messages, system), max_completion_tokens=max_tokens or 4096
        )
        c = r.choices[0]
        return Reply(
            c.message.content or "",
            STOP.get(c.finish_reason, "other"),
            r.usage.prompt_tokens,
            r.usage.completion_tokens,
            self.name,
            r.model,
            r.id,
        )

    def stream(self, messages, system=None, max_tokens=None):
        parts, finish, usage, rid, model = [], None, None, "", self.model
        for chunk in self.client.chat.completions.create(
            model=self.model,
            messages=self._msgs(messages, system),
            max_completion_tokens=max_tokens or 4096,
            stream=True,
            stream_options={"include_usage": True},
        ):
            rid, model = chunk.id, chunk.model
            if chunk.usage:
                usage = chunk.usage
            if chunk.choices:
                d = chunk.choices[0]
                if d.delta.content:
                    parts.append(d.delta.content)
                    yield d.delta.content
                finish = d.finish_reason or finish
        self.last = Reply(
            "".join(parts),
            STOP.get(finish, "other"),
            usage.prompt_tokens if usage else 0,
            usage.completion_tokens if usage else 0,
            self.name,
            model,
            rid,
        )

    def count_tokens(self, text):
        # 토큰만 세는 공식 엔드포인트가 없어서, 1토큰짜리 요청을 보내 입력 토큰을 읽는다(아주 적은 비용 발생)
        r = self.client.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": text}], max_completion_tokens=16
        )
        return r.usage.prompt_tokens
