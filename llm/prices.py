"""백만 토큰당 달러 (입력, 출력). 모르는 모델은 None → 비용 대신 토큰만 보여 준다.
출처: 각 회사 공식 가격표. 값을 넣을 때 확인한 날짜를 같이 적는다.
"""

PRICES = {
    "claude-opus-5-5": (4.00, 20.00),  # Anthropic, 2026-11
    "gpt-5-mini": (0.25, 2.00),  # OpenAI 공식 가격표, 2026-11-10 확인
    "qwen2.5:1.5b": (0.0, 0.0),  # Ollama 로컬 실행: API 비용 없음(전기·PC 자원만)
    "offline-example": (4.00, 20.00),  # 오프라인 예시는 opus-5-5 단가로 계산
}


def cost(model, input_tokens, output_tokens):
    # 응답의 모델 이름엔 날짜가 붙기도 한다(예: gpt-5-mini-2025-08-07) → 앞부분으로도 찾는다
    p = PRICES.get(model) or next((v for k, v in PRICES.items() if model.startswith(k + "-")), None)
    if not p:
        return None
    return input_tokens / 1e6 * p[0] + output_tokens / 1e6 * p[1]
