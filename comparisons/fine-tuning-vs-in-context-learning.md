---
title: "Fine-Tuning vs In-Context Learning"
created: "2026-10-13"
updated: "2026-10-20"
type: "comparison"
tags: ["comparison", "llm", "pretraining", "prompting"]
sources: ["raw/papers/2019-05-bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md", "raw/papers/2020-07-language-models-are-few-shot-learners.md", "raw/papers/2023-01-chain-of-thought-prompting-elicits-reasoning-in-large-language-models.md"]
confidence: "high"
contested: false
contradictions: []
---
# Fine-Tuning vs In-Context Learning

사전학습한 모델을 새 과제에 맞추는 두 가지 방식을 비교한다. Fine-tuning은
가중치를 갱신하고, in-context learning은 프롬프트만 바꾼다.

## 정의

- **Fine-tuning:** 사전학습된 모델의 가중치를 과제 전용 지도학습 데이터로 다시
  학습해 갱신한다. 보통 수천에서 수십만 개의 라벨된 예시를 쓴다.^[raw/papers/2020-07-language-models-are-few-shot-learners.md]
- **In-context learning (few-shot):** 추론 시점에 과제 예시 몇 개를 조건으로만
  주고, 가중치는 갱신하지 않는다. 자세한 내용은 [[in-context-learning]]에 있다.^[raw/papers/2020-07-language-models-are-few-shot-learners.md]

## 비교

| 항목 | Fine-tuning (BERT) | In-context learning (GPT-3) |
| --- | --- | --- |
| 가중치 갱신 | 과제마다 함 | 하지 않음 |
| 과제별 필요 데이터 | 라벨된 데이터셋 (수천~수십만 개) | 프롬프트 속 예시 몇 개 또는 설명 |
| 과제 적응 방식 | 출력층 하나를 추가하고 전체를 학습 | 텍스트로 과제와 예시를 제시 |
| 대표 근거 | 11개 NLP 과제에서 당시 최고 성능 | 키운 모델이 일부 과제에서 fine-tuning 최고 성능에 근접 |

- BERT는 [[masked-language-modeling]]으로 사전학습한 뒤, 출력층 하나만 추가해
  fine-tuning하면 큰 구조 변경 없이 다양한 과제에서 최고 성능을 냈다.^[raw/papers/2019-05-bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md]
- GPT-3 논문은 fine-tuning이 구조는 과제와 무관해도 여전히 과제별 데이터셋을
  요구한다는 점을 한계로 든다. 사람은 예시 몇 개나 간단한 지시만으로 새 언어
  과제를 해내는데, 기존 NLP 시스템은 그러지 못한다는 것이다. GPT-3는 모든 과제를
  gradient 갱신 없이 수행했다.^[raw/papers/2020-07-language-models-are-few-shot-learners.md]

## 프롬프트 방식이 fine-tuning을 넘은 사례

Chain-of-thought 논문에서는 PaLM 540B에 [[chain-of-thought-prompting]] 예시 8개를
준 것만으로, GSM8K에서 verifier를 붙여 fine-tuning한 GPT-3보다 높은 정확도를
냈다.^[raw/papers/2023-01-chain-of-thought-prompting-elicits-reasoning-in-large-language-models.md]

## 정리

- **Fine-tuning:** 라벨된 데이터와 과제마다 별도의 학습이 필요하지만, BERT 크기
  (110M~340M)의 모델로도 높은 성능을 낸다.^[raw/papers/2019-05-bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md]
- **In-context learning:** 과제마다 학습할 필요가 없지만, 성능이 모델 크기에 크게
  좌우된다. 이 부분은 [[language-model-scaling]]을 참고한다.^[raw/papers/2020-07-language-models-are-few-shot-learners.md]
- 두 방식은 같은 시기 논문 안에서 대립하는 주장이 아니라 서로 다른 설정이다.
  그래서 `contested: false`로 둔다.
