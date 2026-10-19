---
title: "Language Model Scaling"
created: "2026-10-13"
updated: "2026-10-19"
type: "concept"
tags: ["llm"]
sources: ["raw/papers/brown-2020-language-models-are-few-shot.md", "raw/papers/wei-2023-chain-of-thought-prompting-elicits.md"]
confidence: "high"
contested: false
contradictions: []
---
# Language Model Scaling

언어 모델의 크기(파라미터 수)를 키울 때 성능과 능력이 어떻게 바뀌는지에 대한
관찰이다. 두 논문이 서로 다른 측면을 보여준다.

## 크기에 따라 매끄럽게 좋아지는 성능 (GPT-3)

- GPT-3 논문은 125M부터 175B 파라미터까지 크기가 세 자릿수 차이 나는 모델 8개를
  학습해 크기의 영향을 측정했다. 가장 큰 모델이 GPT-3이고, 당시 이전의 어떤
  non-sparse 언어 모델보다 10배 컸다.
- 선행 연구를 근거로, 데이터가 충분하면 validation loss가 크기에 대해 대략 매끄러운
  power law를 따를 것이라는 가설을 세우고 이를 검증했다.
- 언어 모델을 키우면 과제에 무관한 few-shot 성능이 크게 오르고, 때로는 기존
  fine-tuning 최고 성능에 근접한다.^[raw/papers/brown-2020-language-models-are-few-shot.md]
- 특히 few-shot 성능은 zero-shot보다 크기에 따라 더 빠르게 올라, 큰 모델일수록
  [[in-context-learning]]을 잘한다.^[raw/papers/brown-2020-language-models-are-few-shot.md]

## 일정 크기에서 갑자기 나타나는 능력 (Chain-of-Thought)

- Chain-of-thought 논문은 추론 능력이 "모델 규모의 emergent ability"라고 본다.
  약 100B 파라미터 모델에서야 효과가 나타나고, 10B보다 작은 대부분의 모델에서는
  오히려 성능이 떨어진다.
- 논문은 이 능력이 작은 모델의 성능을 연장해서는 예측할 수 없다는 점에서
  emergent하다고 설명한다. Chain of thought 없이는 이 추론 과제들의 성능이 모델을
  키워도 거의 오르지 않는 평평한 곡선을 보인다.^[raw/papers/wei-2023-chain-of-thought-prompting-elicits.md]
- 방법 자체는 [[chain-of-thought-prompting]]에 정리했다.

## 두 관찰의 관계

Chain-of-thought 논문이 이 차이를 직접 언급한다. 모델을 키우면 성능과 표본
효율이 좋아진다는 점은 이미 알려져 있지만, chain-of-thought 추론은 작은 모델의
성능을 연장해서는 성공을 예측할 수 없다는 점에서 다르다고 설명한다.^[raw/papers/wei-2023-chain-of-thought-prompting-elicits.md]

따라서 두 관찰은 서로 모순되지 않는다. GPT-3 논문은 42개 벤치마크를 합친 성능과
loss가 크기에 따라 꾸준히 좋아지는 경향을 보이고, chain-of-thought 논문은 특정
추론 방법의 효과가 일정 크기 이상에서만 나타난다는 점을 보인다.^[raw/papers/brown-2020-language-models-are-few-shot.md]^[raw/papers/wei-2023-chain-of-thought-prompting-elicits.md]

## 기반 구조

두 논문이 다루는 모델은 모두 [[transformer]] 기반 언어 모델이다. GPT-3는 GPT-2와
같은 아키텍처를 쓴다.^[raw/papers/brown-2020-language-models-are-few-shot.md]

## 열린 질문

- 큰 모델은 추론 비용이 커서 실제 활용이 어렵다. GPT-3 논문과 chain-of-thought
  논문이 모두 이 점을 한계로 든다.^[raw/papers/brown-2020-language-models-are-few-shot.md]^[raw/papers/wei-2023-chain-of-thought-prompting-elicits.md]
- GPT-3 논문은 언어 모델이 공통으로 사전학습 표본 효율이 낮다는 점도 한계로 든다.^[raw/papers/brown-2020-language-models-are-few-shot.md]

## 관련 개념

- [[in-context-learning]] — 크기에 따라 더 빠르게 좋아지는 능력
- [[chain-of-thought-prompting]] — 일정 크기 이상에서만 효과가 나타나는 방법
- [[transformer]] — 두 논문이 다루는 모델의 구조
