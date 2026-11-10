"""주차 코드 공통 준비: 저장소 루트의 llm 패키지를 불러오고 공급자를 고른다."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))

from llm import cost, get_provider  # noqa: E402

llm = get_provider(HERE / "fixtures")
if llm.name == "offline":
    print("※ 오프라인 모드: API 키가 없어 fixtures/의 예시 응답을 씁니다(실측 아님).\n")
else:
    print(f"※ 공급자: {llm.name} · 모델: {llm.model}\n")


def show_usage(r):
    c = cost(r.model, r.input_tokens, r.output_tokens)
    print(f"\n[토큰] 입력 {r.input_tokens} · 출력 {r.output_tokens}")
    print(f"[비용] ${c:.6f}" if c is not None else "[비용] 가격표에 없는 모델 (llm/prices.py에 추가)")
