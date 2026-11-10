"""02. 스트리밍 대화: 답이 조금씩 오는 걸 보고, 대화가 길어질수록 입력 토큰이 쌓이는 걸 확인한다.

핵심: API는 기억이 없다(stateless). 매번 지난 대화 전체를 다시 보낸다.
실행: python 02_stream_chat.py          (빈 줄 입력 시 종료)
      python 02_stream_chat.py --demo   (정해진 질문 3개로 자동 진행)
"""

import sys

from _setup import llm, show_usage

DEMO = ["REST가 뭐야? 한 줄로", "그럼 GraphQL은? 한 줄로", "둘 중 뭘 써야 해? 한 줄로"]
auto = "--demo" in sys.argv or llm.name == "offline"
history = []
for i in range(len(DEMO) if auto else 10**9):
    user = DEMO[i] if auto else input("나> ").strip()
    if auto:
        print(f"나> {user}")
    if not user:
        break
    history.append({"role": "user", "content": user})
    print("AI> ", end="")
    for piece in llm.stream(history):
        print(piece, end="", flush=True)
    print()
    r = llm.last
    history.append(r.as_message())  # 다음 요청에 이번 답을 붙인다
    show_usage(r)
    print(f"[대화 길이] 메시지 {len(history)}개 → 다음 요청은 이걸 전부 다시 보냄\n")
