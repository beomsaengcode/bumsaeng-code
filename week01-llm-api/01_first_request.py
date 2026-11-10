"""01. 첫 요청: 질문 하나 보내고, 답·멈춘 이유·토큰·비용을 본다.

실행: python 01_first_request.py "HTTP 403이랑 404 차이를 한 줄로"
공급자 바꾸기: LLM_PROVIDER=openai|claude|offline  ·  모델 바꾸기: LLM_MODEL=...
"""

import sys

from _setup import llm, show_usage

question = sys.argv[1] if len(sys.argv) > 1 else "HTTP 403이랑 404 차이를 한 줄로 알려줘"
r = llm.chat([{"role": "user", "content": question}])
print(r.text)
print(f"\n[멈춘 이유] {r.stop}   [요청 ID] {r.request_id}")
if r.stop == "refusal":
    print("※ 모델이 답을 거절했어요.")
if r.stop == "length":
    print("※ 최대 토큰에 걸려 답이 잘렸어요.")
show_usage(r)
