---
title: "In-Context Learning"
created: "2026-10-13"
updated: "2026-10-19"
type: "concept"
tags: ["llm", "prompting"]
sources: ["raw/papers/brown-2020-language-models-are-few-shot.md", "raw/papers/wei-2023-chain-of-thought-prompting-elicits.md"]
confidence: "high"
contested: false
contradictions: []
---
# In-Context Learning

모델의 가중치를 바꾸지 않고, 입력 텍스트(프롬프트) 안에 과제 설명이나 예시를
넣는 것만으로 새 과제를 수행하게 하는 방식이다.

## 정의

GPT-3 논문은 언어 모델이 사전학습 중에 폭넓은 기술과 패턴 인식 능력을 익히고,
추론 시점에 이를 이용해 원하는 과제에 빠르게 적응한다고 본다. 이 과정의 안쪽
루프, 즉 각 시퀀스의 forward pass 안에서 일어나는 적응을 "in-context learning"
이라고 부른다.^[raw/papers/brown-2020-language-models-are-few-shot.md]

## 설정 구분 (GPT-3)

- **Few-Shot:** 추론 시점에 과제 예시 몇 개를 조건으로 주되 가중치 갱신은 하지 않는다.
- **One-Shot, Zero-Shot:** 예시를 하나만 주거나, 자연어 과제 설명만 준다.
- GPT-3는 모든 과제를 gradient 갱신이나 fine-tuning 없이 텍스트 상호작용만으로
  수행했다. 이 방식과 기존 fine-tuning의 차이는
  [[fine-tuning-vs-in-context-learning]]에 정리했다.^[raw/papers/brown-2020-language-models-are-few-shot.md]

## 모델 크기와의 관계

GPT-3 논문에서 zero-shot 성능은 모델 크기에 따라 꾸준히 오르지만, few-shot
성능은 더 빠르게 오른다. 논문은 이를 "큰 모델일수록 in-context learning에 더
능숙하다"는 근거로 든다. 이 경향은 [[language-model-scaling]]에서 더 다룬다.^[raw/papers/brown-2020-language-models-are-few-shot.md]

## 확장: 예시에 추론 과정을 넣기

Chain-of-thought 논문은 기준선으로 "Brown et al.(2020)이 널리 알린 standard
few-shot prompting"을 쓴다. 입력-출력 쌍을 in-context 예시로 주고 바로 답을 내게
하는 방식이다. 여기에 예시마다 중간 추론 단계를 넣은 것이
[[chain-of-thought-prompting]]이다.^[raw/papers/wei-2023-chain-of-thought-prompting-elicits.md]

## 기반 구조

GPT-3는 GPT-2와 같은 [[transformer]] 기반 자기회귀 언어 모델이다.^[raw/papers/brown-2020-language-models-are-few-shot.md]

## 열린 질문과 논쟁

- GPT-3 논문은 few-shot 학습이 추론 시점에 새 과제를 "처음부터" 배우는 것인지,
  사전학습 때 본 과제를 알아보는 것뿐인지 분명하지 않다고 스스로 한계로 든다.
  "meta-learning"이라는 용어도 두 가능성을 모두 포함하도록 일부러 넓게 정의했다.^[raw/papers/brown-2020-language-models-are-few-shot.md]
- GPT-3 규모의 모델은 추론 비용이 크고 다루기 불편해 실제 활용이 어렵다고 밝힌다.^[raw/papers/brown-2020-language-models-are-few-shot.md]

## 관련 개념

- [[chain-of-thought-prompting]] — few-shot 예시에 추론 단계를 더한 확장
- [[language-model-scaling]] — 모델 크기와 in-context learning 능력의 관계
- [[fine-tuning-vs-in-context-learning]] — 가중치를 갱신하는 방식과의 비교
- [[transformer]] — GPT-3의 기반 구조
- [[rag-vs-in-context-learning-knowledge-supply]] — 검색 없이 파라미터 지식만 쓰는 closed-book QA와 RAG 비교
