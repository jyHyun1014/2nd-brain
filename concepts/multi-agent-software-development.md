---
title: "Multi-Agent Software Development"
created: "2026-10-30"
updated: "2026-10-30"
type: "concept"
tags: ["llm", "workflow"]
sources: ["raw/papers/2024-06-chatdev-communicative-agents-for-software-development.md"]
confidence: "medium"
contested: false
contradictions: []
---
# 다중 에이전트 소프트웨어 개발 (Multi-Agent Software Development)

여러 LLM 에이전트에 역할을 나눠 부여하고 대화로 협업시켜 소프트웨어를 생성하는 접근이다.
ChatDev 연구를 중심으로 정리한다. 단일 에이전트가 한 번에 코드를 뱉는 방식과 달리, 요구 분석부터
설계·코딩·테스트까지를 역할별 대화로 쪼개 진행한다.^[raw/papers/2024-06-chatdev-communicative-agents-for-software-development.md]

## 동기

소프트웨어 개발은 본래 여러 역할이 협업하는 공정이다. 사람 팀의 워터폴(waterfall) 모델처럼
단계를 나눠 진행하면 각 단계에서 검증과 피드백이 끼어들 여지가 생긴다. 이 구조를 LLM 에이전트
협업으로 옮기면 단일 프롬프트로는 놓치기 쉬운 설계·리뷰·테스트가 대화 과정에서 명시적으로
다뤄진다.^[raw/papers/2024-06-chatdev-communicative-agents-for-software-development.md]

## ChatDev 구조

- **chat chain:** 하나의 개발 과제를 순차적 하위 과제로 쪼개고, 각 하위 과제를 두 역할의 대화로
  처리한다. 대화가 끝나면 결론(예: 생성된 코드나 설계)을 내고, 그 결론이 다음 단계로 전달된다.
- **역할:** 임원(CEO·CTO)과 실무자(instructor, programmer, reviewer, tester)를 나눠 부여한다.
  한 하위 과제는 코드 변경이 두 번 연속 없거나 대화가 10라운드에 이르면 종료된다.
- **communicative dehallucination:** 코드 완성·리뷰·테스트 단계에서 작동한다. 한 에이전트가
  불확실한 내용을 확정적으로 요구하면, 상대 에이전트가 근거를 요구해 환각을 줄인다.
- **dual agreement:** 두 에이전트가 역할을 뒤집어 대화를 반복해, 서로 다른 관점에서 합의에
  이르게 한다.^[raw/papers/2024-06-chatdev-communicative-agents-for-software-development.md]

## 성능

GPT-Engineer, MetaGPT 같은 단일·다중 에이전트 기준선과 비교한다.

| 방법 | Completeness | Executability | Consistency | Quality |
| --- | --- | --- | --- | --- |
| GPT-Engineer | 0.502 | 0.358 | 0.789 | 0.142 |
| MetaGPT | 0.483 | 0.415 | 0.760 | 0.152 |
| ChatDev | 0.560 | 0.880 | 0.802 | 0.395 |

- Completeness는 자리표시(placeholder) 코드 없이 소프트웨어를 완성한 비율, Executability는 컴파일
  되어 바로 실행되는 비율, Consistency는 요구사항 텍스트와 생성 코드 임베딩의 코사인 거리,
  Quality는 세 지표의 곱이다.
- 쌍대 비교에서 ChatDev는 GPT-Engineer를 심판(LLM) 기준 77%, 사람 기준 90%에서 이겼고,
  MetaGPT도 심판 기준 57%에서 앞선다.
- 비용은 MetaGPT보다 낮다. 소프트웨어 1건당 ChatDev는 약 148초, 22,949 토큰, 4.39개 파일,
  144줄을 쓰고, MetaGPT는 약 154초, 29,279 토큰을 썼다.^[raw/papers/2024-06-chatdev-communicative-agents-for-software-development.md]

## 해석과 한계

- 성능 개선의 상당 부분은 대화 구조 자체보다 **역할 분할과 반복 검증**에서 나온다. 완성도와
  실행 가능성은 크게 올랐지만, Consistency는 기준선 대비 개선 폭이 작아 요구사항과 코드의
  의미적 정합성은 남은 문제다.
- 실험은 ChatGPT-3.5(온도 0.2)와 Python-3.11.4를 쓴 단일 설정이라, 더 강한 모델이나 다른
  언어로 일반화되는지는 검증되지 않았다.
- ChatDev 이후 이 계열은 MacNet처럼 확장된 조직 구조로 이어지지만, 다중 에이전트 협업의 평가
  기준 자체는 아직 정착되지 않았다.^[raw/papers/2024-06-chatdev-communicative-agents-for-software-development.md]

## 관련 개념

- [[llm-based-agents]] — 역할 부여와 대화 협업이라는 상위 틀
- [[react]] — 행동·관측을 번갈아 생성하는 단일 에이전트 대응
- [[chain-of-thought-prompting]] — 단계별 추론을 명시화한다는 공통 발상
