---
title: "Chain-of-Thought Prompting"
created: "2026-10-13"
updated: "2026-10-19"
type: "concept"
tags: ["llm", "prompting"]
sources: ["raw/papers/wei-2023-chain-of-thought-prompting-elicits.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Chain-of-Thought Prompting

Few-shot 프롬프트의 예시에 **최종 답만이 아니라 중간 추론 단계(chain of thought)**까지
적어 넣어, 큰 언어 모델이 복잡한 추론을 하도록 이끄는 방법이다.^[raw/papers/wei-2023-chain-of-thought-prompting-elicits.md]

## 방법

- 기준선인 standard prompting은 질문-답 쌍을 in-context 예시로 주고 모델이 바로
  답을 내게 한다. 이 방식은 [[in-context-learning]]에 정리했다.
- Chain-of-thought prompting은 같은 few-shot 구조에서 예시의 답 앞에 단계별
  추론을 함께 적는다.
- 별도 학습 없이, 충분히 큰 기성 언어 모델에 이런 예시를 넣는 것만으로 추론
  능력을 끌어낼 수 있다고 보고한다.^[raw/papers/wei-2023-chain-of-thought-prompting-elicits.md]

## 결과

- 세 종류의 대형 언어 모델에서 산술, 상식, 기호 추론 과제 성능이 올랐다.
- 540B 파라미터 모델(PaLM)에 chain-of-thought 예시 8개만 주었을 때 수학 문장제
  벤치마크 GSM8K에서 당시 최고 정확도를 냈고, verifier를 붙여 fine-tuning한
  GPT-3보다도 높았다. 프롬프트만 쓴 방식이 fine-tuning을 넘은 사례로,
  [[fine-tuning-vs-in-context-learning]]에서 비교한다.^[raw/papers/wei-2023-chain-of-thought-prompting-elicits.md]

## 모델 크기에 따라 나타나는 능력

논문은 chain-of-thought 추론을 "모델 규모의 emergent ability"라고 부른다.

- 작은 모델에서는 성능을 올리지 못하고, 약 100B 파라미터 모델에서야 효과가 나타난다.
- 10B보다 작은 대부분의 모델에서는 오히려 성능을 떨어뜨린다.
- 따라서 효과를 작은 모델의 성능을 연장해서 예측할 수 없다.

모델 크기와 능력의 관계는 [[language-model-scaling]]에서 함께 다룬다.^[raw/papers/wei-2023-chain-of-thought-prompting-elicits.md]

## 근거 수준

이 방법 자체는 Wei 논문 한 편에 근거하므로 `confidence: medium`이다.

## 열린 질문

논문이 직접 밝힌 한계는 다음과 같다.^[raw/papers/wei-2023-chain-of-thought-prompting-elicits.md]

- 사람의 사고 과정을 흉내 내지만, 신경망이 실제로 "추론"을 하는지는 답하지 않고
  열린 질문으로 남긴다.
- 추론 과정이 맞다는 보장이 없어 맞는 답과 틀린 답이 모두 나올 수 있다.
- 큰 모델에서만 효과가 나타나 실제 서비스 비용이 크다. 작은 모델에서 추론을
  끌어내는 방법은 후속 연구 과제다.
- few-shot에서는 예시에 추론을 직접 적는 비용이 작지만, fine-tuning용 데이터를
  만들 때는 이 비용이 커질 수 있다.

## 관련 개념

- [[in-context-learning]] — 기준이 되는 standard few-shot prompting
- [[language-model-scaling]] — 효과가 나타나는 모델 크기
- [[fine-tuning-vs-in-context-learning]] — 프롬프트만으로 fine-tuning을 넘은 사례
