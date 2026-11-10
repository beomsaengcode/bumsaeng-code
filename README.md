# bumsaeng-code

[범생코드](https://beomsaengcode.github.io) 영상에 나온 코드를 직접 돌려 보는 저장소입니다.
매주 AI 주제 하나와 개발 기초 하나를 구조도로 보고, 여기서 실행하고, 실습으로 손에 익힙니다.

## AI 엔지니어 10주

| 주 | AI | 개발 기초 | 폴더 |
|---|---|---|---|
| 01 | LLM API | API · HTTP | [week01-llm-api](week01-llm-api) |
| 02 | RAG 기본 | 임베딩 | |
| 03 | RAG 품질 | DB 인덱스 | |
| 04 | 도구 호출 | JSON 스키마 | |
| 05 | 에이전트 | 상태 기계 | |
| 06 | MCP | 프로토콜 | |
| 07 | 평가 | 테스트 · CI | |
| 08 | 관측 · 비용 | MSA | |
| 09 | 인젝션 방어 | 보안 | |
| 10 | 배포 · 캡스톤 | Docker | |

폴더는 그 주 코드를 실제로 돌려 본 뒤에 올립니다. 돌려 본 공급자와 날짜는 [TESTED.md](TESTED.md)에 남깁니다.

## 시작

```bash
git clone https://github.com/beomsaengcode/bumsaeng-code
cd bumsaeng-code
pip install -r requirements.txt
python week01-llm-api/01_first_request.py "HTTP 403이랑 404 차이를 한 줄로"
```

API 키가 없으면 예시 응답(오프라인)으로 돌아가서 흐름을 끝까지 따라갈 수 있어요.

| 공급자 | 켜는 법 | 비용 |
|---|---|---|
| offline | 키 없이 그대로 | 없음 (예시 응답, 실측 아님) |
| openai | `OPENAI_API_KEY` | 유료 |
| ollama | [Ollama](https://ollama.com) 설치 후 `ollama pull qwen2.5:1.5b`, `LLM_PROVIDER=ollama` | 없음 (내 컴퓨터) |

직접 고르려면 `LLM_PROVIDER=offline|openai|ollama`, 모델은 `LLM_MODEL`로 바꿉니다.

## 구조

```
llm/                 공급자를 몰라도 되게 감싼 공통 인터페이스
  base.py            Reply(답, 멈춘 이유, 입력·출력 토큰), Provider
  prices.py          모델별 백만 토큰당 가격 (확인한 날짜와 함께)
  *_provider.py      openai · ollama · offline
weekNN-주제/
  README.md          그 주에 알게 되는 것, 실행, 실습, 면접 질문
  01_*.py ...        번호 순서대로 돌리면 이야기가 이어짐
  fixtures/          오프라인 예시 응답
```

주차 코드는 `llm`의 `chat`, `stream`, `count_tokens`만 부릅니다. 공급자를 바꿔도 주차 코드는 그대로입니다.

## 작업 규칙

**코드**
- Python 3.10 이상, [ruff](https://docs.astral.sh/ruff/)로 검사와 정렬 (`ruff check . && ruff format .`)
- 파일은 `NN_무엇을_하는지.py`, 폴더는 `weekNN-주제`
- 주석과 출력 문구는 한국어, 이름(변수·함수)은 영어
- 키와 토큰은 `.env`에만 둡니다. 커밋하지 않습니다.

**커밋 메시지**

```
<종류>(<범위>): <무엇을 바꿨는지 한 줄>
```

| 종류 | 언제 |
|---|---|
| feat | 새 예제, 새 주차 |
| fix | 동작이 틀린 것을 고침 |
| docs | README, 설명만 바꿈 |
| refactor | 동작은 같고 구조만 바꿈 |
| test | 테스트, 예시 응답 |
| chore | 설정, 의존성 |

범위는 `week01`, `llm`처럼 폴더 이름을 씁니다. 예: `feat(week02): 청크 크기별 검색 결과 비교`

## 라이선스

MIT
