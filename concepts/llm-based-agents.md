---
title: "LLM-based Agents"
created: "2026-10-22"
updated: "2026-10-22"
type: "concept"
tags: ["llm"]
sources: ["raw/papers/2023-09-the-rise-and-potential-of-large-language-model-based-agents-a-survey.md", "raw/papers/2025-10-agentbench-evaluating-llms-as-agents.md"]
confidence: "medium"
contested: false
contradictions: []
---
# LLM-based Agents

환경을 인지하고 결정을 내려 행동하는 에이전트의 핵심 두뇌로 대규모 언어 모델을 쓰는 접근이다.
서베이는 개념 틀을, AgentBench는 실제 능력의 측정을 다룬다.

## 개념 틀: brain, perception, action

서베이는 LLM 기반 에이전트를 세 구성요소로 나눈다.^[raw/papers/2023-09-the-rise-and-potential-of-large-language-model-based-agents-a-survey.md]

- **Brain:** 자연어 상호작용, 지식, 기억, 추론과 계획, 전이와 일반화를 담당한다.
- **Perception:** 텍스트뿐 아니라 시각, 청각 등 다른 입력으로 인지 공간을 넓힌다.
- **Action:** 텍스트 출력, 도구 사용, 구현된(embodied) 행동으로 환경과 상호작용한다.

응용은 단일 에이전트, 다중 에이전트, 사람과 에이전트의 협업으로 나뉜다. 에이전트 사회의
행동과 성격, 거기서 나타나는 사회 현상도 다룬다. 열린 문제로는 LLM 기반 에이전트가 AGI로
가는 길인지에 대한 논쟁, 에이전트 수 확장 등을 든다.^[raw/papers/2023-09-the-rise-and-potential-of-large-language-model-based-agents-a-survey.md]

## 능력 측정: AgentBench

AgentBench는 LLM의 추론·의사결정 능력을 상호작용 환경에서 평가하는 다차원 벤치마크다.
환경은 8개이며 세 종류의 grounding으로 묶인다.^[raw/papers/2025-10-agentbench-evaluating-llms-as-agents.md]

| 분류 | 환경 |
| --- | --- |
| Code | Operating System, Database, Knowledge Graph |
| Game | Digital Card Game, Lateral Thinking Puzzles, House-Holding |
| Web | Web Shopping, Web Browsing |

## AgentBench 결과

- API 기반과 오픈소스 LLM 29개를 시험했다. GPT-4 같은 최상위 모델은 다양한 실제 과제를 처리할
  잠재력을 보였지만, 상용 최상위 모델과 70B 이하 오픈소스 모델 사이에 큰 성능 격차가 있다.
- 가장 큰 실패 원인은 정해진 최대 상호작용 횟수를 넘기는 Task Limit Exceeded로, 약한 추론과
  의사결정 능력을 보여준다. 그 밖에 출력 형식 위반(Invalid Format)과 유효하지 않은 행동
  선택(Invalid Action)도 주요 실패 유형이다.
- 개선 방향으로 지시 따르기 강화와 고품질 정렬 데이터를 든다. 코드 학습은 일부 에이전트
  과제를 개선하고 다른 과제는 해치는 양날의 검이라고 분석한다.
- 가장 강한 모델조차 실용적인 에이전트로는 부족하다고 결론짓는다.^[raw/papers/2025-10-agentbench-evaluating-llms-as-agents.md]

## 두 원본의 관계

서베이(2023-09)는 가능성과 구조를, AgentBench는 실제 모델 비교를 다룬다. 서베이의 낙관적
전망과 AgentBench의 "실용 수준 미달" 결론이 충돌하는 주장은 아니다. 서로 다른 질문에 답하기
때문이며, 그래서 `contested: false`로 둔다.

## 근거 수준

서로 다른 측면을 다룬 두 원본이므로 `confidence: medium`이다.

## 관련 개념

- [[chain-of-thought-prompting]] — AgentBench가 가장 쉽고 흔한 에이전트 배포 방식으로 든 CoT
- [[llama-2]] — AgentBench가 평가한 오픈소스 모델 중 하나
- [[sglang]] — 에이전트 제어를 워크로드로 시험한 다중 호출 실행 시스템
