---
title: "Transformer"
created: "2026-10-13"
updated: "2026-10-13"
type: "concept"
tags: ["nlp", "llm"]
sources: ["raw/papers/vaswani-2023-attention-is-all-you-need.md", "raw/papers/devlin-2019-bert-pre-training-of-deep.md", "raw/papers/brown-2020-language-models-are-few-shot.md", "raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md"]
confidence: "high"
contested: false
contradictions: []
---
# Transformer

RNN이나 convolution 없이 **attention만으로** 입력과 출력의 표현을 계산하는
sequence transduction 아키텍처다. 원 논문은 이를 "self-attention에 전적으로
의존하는 최초의 transduction 모델"이라고 설명한다.^[raw/papers/vaswani-2023-attention-is-all-you-need.md]

## 핵심 구성

- **Scaled Dot-Product Attention:** query와 key의 내적을 key 차원의 제곱근으로
  나눈 뒤 softmax를 거쳐 value에 가중합을 한다.
- **Multi-Head Attention:** 여러 attention 층을 병렬로 실행해 서로 다른 표현
  공간의 정보를 함께 본다.
- **Encoder-decoder 구조:** 원 논문은 번역을 위해 encoder와 decoder를 모두 쓴다.
- 순환 구조가 없어 병렬화가 쉽고, 원 논문은 WMT 2014 영독 번역 28.4 BLEU,
  영불 번역 41.8 BLEU를 8개 GPU로 3.5일 학습해 달성했다고 보고한다.^[raw/papers/vaswani-2023-attention-is-all-you-need.md]

## 이후 모델들이 쓰는 방식

같은 Transformer 블록을 어떤 방향의 attention으로 쓰느냐에 따라 갈린다.

- **Encoder만 사용 (양방향):** BERT는 "Vaswani et al.(2017)의 원래 구현을
  기반으로 한 다층 양방향 Transformer encoder"이며, 구현이 원본과 거의 같다고
  밝힌다. BERT는 모든 토큰이 양쪽 문맥을 보는 bidirectional self-attention을
  쓴다. 이 구조를 학습시키는 방법은 [[masked-language-modeling]]에 정리했다.^[raw/papers/devlin-2019-bert-pre-training-of-deep.md]
- **Decoder만 사용 (왼쪽 문맥만):** BERT 논문은 GPT 계열이 "각 토큰이 왼쪽
  문맥만 볼 수 있는 제한된 self-attention"을 쓴다고 대비한다. GPT-3는 GPT-2와
  같은 모델·아키텍처에 dense와 sparse attention 패턴을 번갈아 쓰는 Transformer다.^[raw/papers/devlin-2019-bert-pre-training-of-deep.md]^[raw/papers/brown-2020-language-models-are-few-shot.md]
  이 구조를 키웠을 때 나타나는 성질은 [[language-model-scaling]]과
  [[in-context-learning]]에 있다.
- **Encoder-decoder 재사용:** RAG의 generator인 BART-large는 400M 파라미터의
  사전학습된 seq2seq Transformer이고, retriever의 query·document encoder는
  BERT-base 기반이다. 자세한 내용은 [[retrieval-augmented-generation]]에 있다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]

## 메모

- Vaswani 레코드의 `year: 2023`은 Zotero에 저장된 arXiv 최신 버전 날짜다.
  BERT 논문은 이 논문을 "Vaswani et al.(2017)"로 인용한다.^[raw/papers/devlin-2019-bert-pre-training-of-deep.md]
