---
title: "ReAct"
created: "2026-10-30"
updated: "2026-10-30"
type: "concept"
tags: ["llm", "prompting"]
sources: ["raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md"]
confidence: "medium"
contested: false
contradictions: []
---
# ReAct (Reason + Act)

LLM이 추론 흔적(reasoning trace)과 과제별 행동(action)을 번갈아 생성하게 해서, 추론과 행동을
한 흐름에서 결합하는 프롬프트 패러다임이다. 추론은 행동 계획을 세우고 갱신하며 예외를 처리하게
돕고, 행동은 위키백과 API나 환경 같은 외부 자원에서 정보를 가져오게 한다.^[raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md]

## 동기

[[chain-of-thought-prompting]] 추론은 정적 블랙박스라서 모델 내부 표현만 쓰고 외부 세계에
grounded되지 않는다. 그래서 사실 환각과 오류 전파가 생긴다. 반대로 행동만 학습하는 접근은 고수준
목표를 추상적으로 추론하거나 작업 기억을 유지하지 못한다. ReAct는 이 둘을 하나로 묶는다.^[raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md]

## 방법

- 에이전트의 행동 공간을 `A ∪ L`로 확장한다. `L`은 언어 공간이고, 그 안의 행동을 thought 또는
  reasoning trace라고 부른다. thought는 환경을 바꾸지 않으므로 관측(observation) 피드백이 없고,
  문맥에만 추가되어 이후 추론과 행동을 돕는다.
- 프롬프트에는 사람이 만든 소수의 예시 궤적(thought–action–observation)을 넣는다. HotpotQA는 6개,
  FEVER는 3개 예시를 썼다.
- 추론이 중요한 과제에서는 thought와 action을 번갈아 생성하고, 행동이 많은 의사결정 과제에서는
  thought를 궤적의 가장 관련 있는 위치에 드물게 두도록 모델이 스스로 정하게 한다.
- 실험의 기본 모델은 frozen PaLM-540B이며, 가중치 갱신 없이 프롬프트만 쓴다.^[raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md]

## 지식 집약 과제 결과

간단한 위키백과 API(search, lookup, finish)로 상호작용한다.

| 방법 | HotpotQA (EM) | Fever |
| --- | --- | --- |
| Standard | 28.7 | 57.1 |
| CoT | 29.4 | 56.3 |
| Act | 25.7 | 58.9 |
| ReAct | 27.4 | 60.9 |
| CoT-SC → ReAct | 34.2 | 64.6 |
| ReAct → CoT-SC | 35.1 | 62.0 |

- ReAct는 Act보다 두 과제 모두에서 낫다. 추론이 행동을 이끄는 가치, 특히 최종 답을 종합하는
  단계에서의 가치를 보여준다.^[raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md]

## 실패 유형 분석 (HotpotQA)

- CoT의 최대 실패 유형은 환각으로 56%를 차지한다. ReAct는 환각이 0%지만, 추론·행동·관측을
  번갈아 넣는 구조 제약 때문에 추론 오류는 47%로 CoT(16%)보다 많다. 반복 생성 루프에 갇히는
  패턴이 대표적이다.
- 검색 실패도 23%를 차지한다. 정보가 없는 검색 결과가 추론을 탈선시키면 회복하기 어렵다.^[raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md]

## 의사결정 과제 결과

- **ALFWorld:** 최고 ReAct 시행이 평균 성공률 71%로 Act(45%), BUTLER(37%)를 앞섰고, 최악의
  ReAct 시행(48%)조차 두 방법의 최고 시행보다 높았다. 내부 추론 없이 외부 피드백만 쓰는
  ReAct-IM(53%)보다도 크게 높다.
- **WebShop:** one-shot Act가 이미 모방학습 수준이었고, 여기에 희소 추론을 더한 ReAct는 성공률에서
  절대 10%포인트 개선해 40.0%를 기록했다. 사람 전문가(59.6%)와는 아직 차이가 크다.
- 두 과제 모두 1~2개 in-context 예시만으로 수만 개 과제로 학습한 모방·강화학습 방법을 앞섰다.^[raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md]

## 미세조정과 해석 가능성

- ReAct가 만든 정답 궤적 3,000개로 작은 모델(PaLM-8/62B)을 학습하면 프롬프트만 쓸 때와 순위가
  뒤집힌다. 미세조정한 PaLM-8B ReAct가 모든 PaLM-62B 프롬프트 방법을, PaLM-62B ReAct가 모든
  540B 프롬프트 방법을 앞선다.
- 추론 흔적을 사람이 읽고 수정할 수 있다는 점을 활용해, 사람이 환각 문장 하나를 지우고 힌트를
  추가하는 것만으로 실패 궤적을 성공으로 바꾸는 human-in-the-loop 실험을 보인다.^[raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md]

## 한계

- 행동 공간이 큰 복잡한 과제는 더 많은 예시가 필요한데, in-context 학습의 입력 길이 한계에
  걸린다. 그래서 미세조정을 대안으로 제시한다.
- 백본이 PaLM이라 재현성에 제약이 있다. 논문은 프롬프트 전체와 GPT-3 실험을 부록에 공개한다.
- 지식 집약 QA에서는 최신 기법들과 프롬프트만으로는 여전히 격차가 있어, 사람이 쓴 데이터로
  미세조정하는 길을 남은 과제로 든다.^[raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md]

## 근거 수준

Yao 등의 논문 한 편에 근거하므로 `confidence: medium`이다.

## 관련 개념

- [[chain-of-thought-prompting]] — ReAct가 행동·관측을 덧붙이는 기준선
- [[self-consistency]] — ReAct와 결합해 최고 성능을 낸 다수결 디코딩
- [[llm-based-agents]] — 서베이가 다중 에이전트와 함께 논의하는 행동·추론 결합 틀
- [[retrieval-augmented-generation]] — 위키백과 API 상호작용이 검색-생성 루프와 닮은 점
