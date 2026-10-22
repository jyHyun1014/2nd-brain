---
title: "Reinforcement Learning from Human Feedback"
created: "2026-10-22"
updated: "2026-10-22"
type: "concept"
tags: ["llm"]
sources: ["raw/papers/2022-03-training-language-models-to-follow-instructions-with-human-feedback.md", "raw/papers/2023-07-llama-2-open-foundation-and-fine-tuned-chat-models.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Reinforcement Learning from Human Feedback (RLHF)

사람의 선호를 보상 신호로 삼아 사전학습된 언어 모델을 사용자의 의도에 맞게 정렬하는
fine-tuning 절차다. 두 논문이 같은 뼈대를 쓰되 세부가 다르다.

## 정렬이 필요한 이유

InstructGPT 논문은 다음 토큰 예측으로 학습한 큰 언어 모델이 거짓이거나 해로운 출력, 또는
사용자에게 도움이 되지 않는 출력을 낼 수 있어 사용자 의도와 "정렬"되지 않는다고 본다.
프롬프트 설계만으로 푸는 [[in-context-learning]]과 달리, 사람 피드백으로 가중치를 갱신해
이를 해결한다.^[raw/papers/2022-03-training-language-models-to-follow-instructions-with-human-feedback.md]

## InstructGPT의 세 단계

1. **SFT:** 라벨러가 입력 프롬프트에 대한 바람직한 출력을 직접 작성하고, 이로 지도학습
   기준 모델을 만든다.
2. **보상 모델(RM):** 같은 프롬프트에 대한 모델 출력들을 라벨러가 비교해 선호를 표시하고, 어떤
   출력을 선호할지 예측하는 RM을 학습한다.
3. **PPO:** RM을 보상 함수로 삼아 SFT 모델을 PPO로 fine-tuning한다.

라벨링에는 약 40명의 계약자를 썼다.^[raw/papers/2022-03-training-language-models-to-follow-instructions-with-human-feedback.md]

## InstructGPT의 결과

- 1.3B InstructGPT 출력이 파라미터가 100배 이상 많은 175B GPT-3 출력보다 선호됐다. GPT-3에
  few-shot 프롬프트를 붙여도 결과는 같았다.
- TruthfulQA에서 진실하고 유익한 답을 GPT-3보다 약 두 배 자주 냈고, 독성 출력도 줄었다.
- PPO만 쓰면 공개 NLP 데이터셋 성능이 떨어지는 "alignment tax"가 생긴다. 사전학습 분포의
  log likelihood를 올리는 업데이트를 PPO와 섞는 PPO-ptx로 이 퇴보를 크게 줄이면서 라벨러
  선호 점수는 유지했다.
- 이 정렬은 넓은 의미의 "인간 가치"가 아니라 주로 라벨러와 연구자라는 특정 집단의 선호에
  맞춘 것이다. 모델은 여전히 지시를 따르지 못하거나 사실을 지어내는 단순한 실수를 한다.^[raw/papers/2022-03-training-language-models-to-follow-instructions-with-human-feedback.md]

## Llama 2-Chat의 변형

[[llama-2]]의 chat 모델은 SFT 뒤에 RLHF를 여러 번 반복해 적용한다.^[raw/papers/2023-07-llama-2-open-foundation-and-fine-tuned-chat-models.md]

- 도움됨과 안전이 서로 긴장 관계라 한 RM으로는 둘 다 잘하기 어렵다고 보고, 도움됨 RM과
  안전 RM을 따로 학습한다. 두 RM은 사전학습된 chat 모델 체크포인트에서 초기화한다.
- 알고리즘은 PPO와 rejection sampling fine-tuning 두 가지다. rejection sampling은 가장 큰 70B
  모델에서만 수행하고, 더 작은 모델은 70B가 만든 rejection sampling 데이터로 fine-tuning한다.
- 여러 턴에 걸쳐 초기 지시를 유지하도록 fine-tuning 데이터를 조작하는 Ghost Attention을
  제안하고, 안전 선프롬프트를 붙여 만든 응답으로 다시 학습하는 safety context distillation도 쓴다.^[raw/papers/2023-07-llama-2-open-foundation-and-fine-tuned-chat-models.md]

## 두 접근의 차이

| 항목 | InstructGPT | Llama 2-Chat |
| --- | --- | --- |
| 보상 모델 | 선호를 예측하는 RM 하나 | 도움됨 RM과 안전 RM 둘 |
| 최적화 | PPO (PPO-ptx로 퇴보 완화) | PPO와 rejection sampling, 반복 적용 |
| 기반 모델 | GPT-3 | Llama 2 |

## 근거 수준

두 논문이 같은 3단계 뼈대를 공유하지만 서로 다른 모델과 데이터로 보고한 것이므로
`confidence: medium`으로 둔다.

## 관련 개념

- [[llama-2]] — RLHF로 chat 모델을 만든 공개 모델
- [[in-context-learning]] — 가중치 갱신 없이 프롬프트로 적응하는 대비되는 방식
- [[self-rag]] — reflection token의 착상을 reward model에서 얻었다고 밝힌 방법
