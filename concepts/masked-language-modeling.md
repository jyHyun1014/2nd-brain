---
title: "Masked Language Modeling"
created: "2026-10-13"
updated: "2026-10-21"
type: "concept"
tags: ["nlp", "pretraining"]
sources: ["raw/papers/2019-05-bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md", "raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md", "raw/papers/2021-06-an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Masked Language Modeling (MLM)

입력 토큰 일부를 가리고 가려진 토큰을 맞히도록 학습하는 사전학습 목표다.
BERT가 제안한 방식으로, 문헌에서는 Cloze task라고도 부른다.^[raw/papers/2019-05-bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md]

## 왜 필요한가

일반적인 언어 모델은 왼쪽에서 오른쪽(또는 반대)으로만 학습할 수 있다. 양방향으로
조건을 주면 각 단어가 간접적으로 "자기 자신을 보게" 되어 다음 단어 예측이
너무 쉬워지기 때문이다. MLM은 토큰을 가려서 이 문제를 피하고, 깊은 양방향
표현을 학습할 수 있게 한다. 이 양방향 구조는 [[transformer]]의 encoder를 그대로
쓴다.^[raw/papers/2019-05-bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md]

## 구체적인 절차 (BERT)

- 각 시퀀스에서 WordPiece 토큰의 15%를 무작위로 골라 예측 대상으로 삼는다.
- 고른 토큰은 80%는 `[MASK]`로, 10%는 무작위 토큰으로 바꾸고, 10%는 그대로 둔다.
  `[MASK]`는 fine-tuning 때 나오지 않으므로, 사전학습과 fine-tuning 사이의
  불일치를 줄이려는 장치다.
- 입력 전체를 복원하는 denoising auto-encoder와 달리, 가려진 단어만 예측한다.
- BERT는 MLM과 함께 **Next Sentence Prediction(NSP)**도 학습한다. 문장 B가
  문장 A의 실제 다음 문장인지(50%) 무작위 문장인지(50%) 맞히는 과제로, QA와
  NLI에 도움이 된다고 보고한다.^[raw/papers/2019-05-bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md]

## 결과와 쓰임

- 사전학습한 BERT는 출력층 하나만 추가해 fine-tuning하면 11개 NLP 과제에서
  당시 최고 성능을 냈다(GLUE 80.5%, SQuAD v1.1 Test F1 93.2 등). 이렇게 과제별로
  가중치를 갱신하는 방식은 [[fine-tuning-vs-in-context-learning]]에서 GPT-3의
  방식과 비교한다.^[raw/papers/2019-05-bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md]
- 사전학습된 BERT는 다른 시스템의 부품으로도 쓰인다. RAG는 retriever의 query
  encoder와 document encoder를 모두 BERT-base 기반으로 구성한다. 자세한 내용은
  [[retrieval-augmented-generation]]에 있다.^[raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md]

## 근거 수준

MLM 절차 자체는 BERT 논문 한 편에 근거하므로 `confidence: medium`이다.

## 이미지로의 응용

Vision Transformer 논문은 이 목표를 본떠 마스크된 이미지 패치를 예측하는 자기지도
사전학습을 예비 실험했다. 자세한 결과는 [[vision-transformer]]에 있다.^[raw/papers/2021-06-an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md]

## 열린 질문

- `[MASK]` 토큰은 fine-tuning 때 나타나지 않아 사전학습과 fine-tuning 사이에
  불일치가 생긴다. BERT는 80/10/10 치환으로 이를 줄이지만, 논문 스스로 이 방식의
  단점으로 이 불일치를 든다.^[raw/papers/2019-05-bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md]

## 관련 개념

- [[transformer]] — BERT가 쓰는 encoder 구조
- [[fine-tuning-vs-in-context-learning]] — MLM 사전학습 뒤 fine-tuning하는 방식의 위치
- [[retrieval-augmented-generation]] — BERT 기반 encoder를 검색기에 재사용한 예
- [[vision-transformer]] — 마스크 예측을 이미지 패치에 적용한 예비 실험
