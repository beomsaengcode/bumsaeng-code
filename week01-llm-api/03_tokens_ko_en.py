"""03. 실험: 같은 뜻이면 한국어와 영어 중 토큰이 더 많이 드는 쪽은?

실행: python 03_tokens_ko_en.py
※ 토큰을 세는 방법은 공급자마다 다르다(Claude: 무료 count_tokens / OpenAI: 아주 짧은 요청의 입력 토큰).
※ 모델마다 토크나이저가 달라서 숫자도 다르다. 비교는 같은 모델 안에서만.
"""
from _setup import llm

PAIRS = [
    ("환불 규정을 알려주세요.", "Please tell me the refund policy."),
    ("주문이 저장됐는데 결제 이벤트가 사라졌어요.", "The order was saved but the payment event disappeared."),
    ("이 함수가 왜 느린지 설명해 주세요.", "Please explain why this function is slow."),
]

rows = [(ko, en, llm.count_tokens(ko), llm.count_tokens(en)) for ko, en in PAIRS]
print(f"모델: {llm.model}\n")
for ko, en, a, b in rows:
    if a is None or b is None:
        print(f"{ko} / {en}: 이 공급자는 토큰 세기를 지원하지 않아요")
        continue
    print(f"한국어 {a:>3} | 영어 {b:>3} | {a / b:.2f}배   {ko}")
print("\n※ 토큰 수에는 메시지 형식에 드는 기본 토큰이 조금 포함돼요.")
