---
title: "LoRA"
created: "2026-10-22"
updated: "2026-10-22"
type: "concept"
tags: ["llm", "pretraining"]
sources: ["raw/papers/2021-10-lora-low-rank-adaptation-of-large-language-models.md"]
confidence: "medium"
contested: false
contradictions: []
---
# LoRA (Low-Rank Adaptation)

사전학습 가중치는 얼리고, 각 층에 학습 가능한 저랭크 분해 행렬을 주입해 하위 과제에
적응하는 parameter-efficient 방법이다.^[raw/papers/2021-10-lora-low-rank-adaptation-of-large-language-models.md]

## 해결하려는 문제

전체 fine-tuning은 과제마다 원 모델과 같은 크기의 파라미터 집합을 새로 만든다. GPT-3 175B
같은 모델에서는 이를 과제별로 저장·배포하기가 현실적으로 어렵다. 어댑터 층은 모델 깊이를
늘려 추론 지연을 키우고, 프롬프트 계열 방식은 쓸 수 있는 시퀀스 길이를 줄이며, 둘 다
fine-tuning 기준선에 못 미치는 경우가 많다고 논문은 지적한다. 이 비교는 [[fine-tuning-vs-in-context-learning]]의
"가중치를 갱신한다"는 쪽 안에서의 효율 문제다.^[raw/papers/2021-10-lora-low-rank-adaptation-of-large-language-models.md]

## 방법

- 가중치 W0의 적응 중 변화량 ΔW를 저랭크 분해 BA(B는 d×r, A는 r×k, r이 d·k보다 훨씬
  작음)로 표현한다. W0은 얼리고 A와 B만 학습하며, 출력은 W0x + BAx다.
- A는 가우시안, B는 0으로 초기화해 학습 시작 시 ΔW가 0이다. ΔW x는 α/r로 스케일해 r을
  바꿀 때 하이퍼파라미터를 다시 맞출 필요를 줄인다.
- 배포할 때는 BA를 W0에 합칠 수 있어, 구성상 전체 fine-tuning 모델과 추론 지연이 같다.
- 가설은 "적응 중 가중치 변화는 낮은 intrinsic rank를 가진다"이다. 논문은 [[transformer]]의
  self-attention 가중치(Wq, Wk, Wv, Wo)만 대상으로 삼는다.^[raw/papers/2021-10-lora-low-rank-adaptation-of-large-language-models.md]

## 결과

- GPT-3 175B 기준 학습 가능한 파라미터가 1만 배, GPU 메모리가 3배 줄고(학습 VRAM
  1.2TB에서 350GB), r=4로 query·value 행렬만 적응하면 체크포인트가 350GB에서 약 35MB로
  준다. 과제를 바꿀 때는 LoRA 가중치만 교체하면 된다.
- RoBERTa, DeBERTa, GPT-2, GPT-3에서 fine-tuning과 비슷하거나 더 나은 품질을 보였다.
- 파라미터 예산 18M에서는 Wq와 Wv를 함께 적응하는 설정이 가장 좋았다. 이 두 행렬에서는
  rank 1로도 WikiSQL과 MultiNLI에서 경쟁력 있는 결과가 나와, ΔW의 intrinsic rank가 매우
  낮다는 해석을 뒷받침한다.^[raw/papers/2021-10-lora-low-rank-adaptation-of-large-language-models.md]

## 한계

- 추론 지연을 없애려고 A, B를 W에 합치면, 서로 다른 과제의 입력을 한 배치로 처리하기 어렵다.
  합치지 않고 샘플별로 모듈을 고르는 방법이 있지만 지연이 중요한 경우에는 부적합하다.
- 논문의 적응 실험은 self-attention 가중치에만 적용했고 MLP 모듈은 얼렸다. 간단함과 파라미터
  효율을 이유로 든 선택이다.^[raw/papers/2021-10-lora-low-rank-adaptation-of-large-language-models.md]

## 근거 수준

Hu 등의 논문 한 편에 근거하므로 `confidence: medium`이다.

## 관련 개념

- [[fine-tuning-vs-in-context-learning]] — 가중치를 갱신하는 적응과 프롬프트 적응의 비교
- [[transformer]] — LoRA를 주입하는 self-attention 가중치의 구조
- [[language-model-scaling]] — 모델이 커져 전체 fine-tuning이 부담스러워진 배경
