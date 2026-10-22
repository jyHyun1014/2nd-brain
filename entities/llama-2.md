---
title: "Llama 2"
created: "2026-10-22"
updated: "2026-10-22"
type: "entity"
tags: ["llm"]
sources: ["raw/papers/2023-07-llama-2-open-foundation-and-fine-tuned-chat-models.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Llama 2

Meta가 공개한 사전학습 언어 모델 계열과, 이를 대화용으로 fine-tuning한 Llama 2-Chat이다.^[raw/papers/2023-07-llama-2-open-foundation-and-fine-tuned-chat-models.md]

## 모델 개요

- 공개 데이터 2조 토큰으로 사전학습했다. Llama 1보다 말뭉치가 40% 커지고 context 길이가
  두 배(2k에서 4k)가 됐으며, 큰 모델의 추론 확장성을 위해 grouped-query attention을 썼다.
- 크기는 7B, 13B, 70B를 공개했다. 34B도 학습했으나 공개하지 않았고 논문에서만 보고한다.
- fine-tuning 데이터에는 공개 instruction 데이터와 새로 만든 사람 주석 예시 100만 건
  이상이 들어 있다.^[raw/papers/2023-07-llama-2-open-foundation-and-fine-tuned-chat-models.md]

## Llama 2-Chat

SFT로 초기 모델을 만든 뒤 [[reinforcement-learning-from-human-feedback]]로 반복 개선한다.
도움됨과 안전 보상 모델을 따로 두는 점, Ghost Attention으로 다중 턴 지시 유지를 돕는 점이
특징이다. 안전 개선을 위해 안전 전용 주석, 레드팀, 반복 평가도 쓴다.^[raw/papers/2023-07-llama-2-open-foundation-and-fine-tuned-chat-models.md]

## 평가 요약

논문은 약 4천 개 프롬프트에 대한 사람 평가와 GPT-4를 심판으로 쓴 평가에서 Llama 2-Chat이
ChatGPT 등과 경쟁한다고 보고한다. 보상 모델을 심판으로 쓴 평가는 자기 모델에 유리할 수
있어, GPT-4 심판 결과는 승률 차이가 줄어도 60%를 넘는다고 적는다. 또한 오픈소스 chat
모델을 대부분의 벤치마크에서 앞서며 사람 평가에서는 비공개 모델의 대안이 될 수 있다고
주장한다.^[raw/papers/2023-07-llama-2-open-foundation-and-fine-tuned-chat-models.md]

## 위키 내 활용

이 위키의 다른 원본에서는 Self-RAG의 기반 모델과 AgentBench의 평가 대상으로 등장한다.
더 자세한 내용은 [[self-rag]]와 [[llm-based-agents]]를 본다.

## 근거 수준

Llama 2 논문 한 편에 근거하므로 `confidence: medium`이다.

## 관련 개념

- [[reinforcement-learning-from-human-feedback]] — Llama 2-Chat의 정렬 절차
- [[language-model-scaling]] — 모델·데이터 규모를 키우는 흐름
- [[self-rag]] — Llama 2 7B와 13B를 생성기 기반으로 쓴 RAG 변형
