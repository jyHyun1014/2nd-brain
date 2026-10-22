---
title: "Self-Consistency"
created: "2026-10-22"
updated: "2026-10-22"
type: "concept"
tags: ["llm", "prompting"]
sources: ["raw/papers/2023-03-self-consistency-improves-chain-of-thought-reasoning-in-language-models.md", "raw/papers/2024-06-sglang-efficient-execution-of-structured-language-model-programs.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Self-Consistency

[[chain-of-thought-prompting]]의 greedy decoding을 대체하는 디코딩 전략이다. 추론 경로를
여러 개 샘플링한 뒤, 경로를 주변화(marginalize)해 가장 일관된 최종 답을 고른다.^[raw/papers/2023-03-self-consistency-improves-chain-of-thought-reasoning-in-language-models.md]

## 방법

논문은 어려운 추론 문제일수록 정답에 이르는 사고 경로가 여러 가지라는 직관에서 출발한다.
절차는 세 단계다.^[raw/papers/2023-03-self-consistency-improves-chain-of-thought-reasoning-in-language-models.md]

1. chain-of-thought 예시로 모델에 프롬프트를 준다.
2. greedy 디코딩 대신 디코더에서 샘플링해 다양한 추론 경로를 만든다.
3. 경로마다 나온 최종 답을 모아, 가장 많이 나온(가장 일관된) 답을 고른다.

추가 verifier나 re-ranker를 학습하는 기존 방법과 달리 전적으로 비지도이며, 추가 학습·보조
모델·fine-tuning·사람 주석이 필요 없다. 여러 모델을 학습하는 앙상블과도 달리 하나의
언어 모델 위에서 동작하는 "self-ensemble"에 가깝다.^[raw/papers/2023-03-self-consistency-improves-chain-of-thought-reasoning-in-language-models.md]

## 결과

- UL2-20B, GPT-3-175B, LaMDA-137B, PaLM-540B 네 모델에서 산술·상식 추론 과제 정확도가
  chain-of-thought 대비 올랐다. 초록은 GSM8K +17.9%, SVAMP +11.0%, AQuA +12.2%,
  StrategyQA +6.4%, ARC-challenge +3.9%를 보고한다.
- 이미 정확도가 높은 GPT-3와 PaLM-540B에서도 AQuA·GSM8K에서 절대 +12~18%p의 추가
  이득이 있었다. 이득은 모델이 클수록 커져, UL2-20B는 +3~6%p인 반면 LaMDA-137B와
  GPT-3는 +9~23%p였다. 이 경향은 [[language-model-scaling]]과 같은 방향이다.
- 사람이 만든 프롬프트에 사소한 실수가 있어 greedy 정확도가 떨어져도(17.1에서 14.9로)
  self-consistency는 이를 상당 부분 메운다.
- 최종 답과 일치하는 디코딩의 비율(일관성)이 정확도와 강하게 상관해, 불확실성 추정에도
  쓸 수 있다고 논문은 말한다.^[raw/papers/2023-03-self-consistency-improves-chain-of-thought-reasoning-in-language-models.md]

## 한계

- 계산 비용이 커진다. 논문은 경로 5~10개만으로도 이득 대부분을 얻는 경우가 많고 성능이
  빠르게 포화한다고 제안한다.
- 모델이 틀리거나 말이 안 되는 추론 경로를 낼 수 있어, 추론의 근거 확보는 후속 과제로 남는다.^[raw/papers/2023-03-self-consistency-improves-chain-of-thought-reasoning-in-language-models.md]

## 시스템 관점

SGLang 논문은 self-consistency를 few-shot, tree-of-thought 등과 함께 "여러 번의 LLM 호출과
제어 흐름으로 이뤄진 LM program"의 예로 든다. 이런 프로그램은 같은 접두사를 공유하는
호출이 많아 KV cache 재사용 여지가 크며, 이를 다루는 시스템이 [[sglang]]이다.^[raw/papers/2024-06-sglang-efficient-execution-of-structured-language-model-programs.md]

## 근거 수준

방법과 수치는 Wang 등의 논문 한 편에 근거하므로 `confidence: medium`이다.

## 관련 개념

- [[chain-of-thought-prompting]] — self-consistency가 개선하는 기반 프롬프트 방식
- [[language-model-scaling]] — 모델 크기에 따라 이득이 커지는 경향
- [[sglang]] — 다중 호출 프로그램의 효율적 실행 시스템
