---
title: "Masked Language Modeling"
created: "2026-10-13"
updated: "2026-10-13"
type: "concept"
tags: ["nlp", "pretraining"]
sources: ["raw/papers/devlin-2019-bert-pre-training-of-deep.md", "raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Masked Language Modeling (MLM)

입력 토큰 일부를 가리고 가려진 토큰을 맞히도록 학습하는 사전학습 목표다.
BERT가 제안한 방식으로, 문헌에서는 Cloze task라고도 부른다.^[raw/papers/devlin-2019-bert-pre-training-of-deep.md]

## 왜 필요한가

일반적인 언어 모델은 왼쪽에서 오른쪽(또는 반대)으로만 학습할 수 있다. 양방향으로
조건을 주면 각 단어가 간접적으로 "자기 자신을 보게" 되어 다음 단어 예측이
너무 쉬워지기 때문이다. MLM은 토큰을 가려서 이 문제를 피하고, 깊은 양방향
표현을 학습할 수 있게 한다. 이 양방향 구조는 [[transformer]]의 encoder를 그대로
쓴다.^[raw/papers/devlin-2019-bert-pre-training-of-deep.md]

## 구체적인 절차 (BERT)

- 각 시퀀스에서 WordPiece 토큰의 15%를 무작위로 골라 예측 대상으로 삼는다.
- 고른 토큰은 80%는 `[MASK]`로, 10%는 무작위 토큰으로 바꾸고, 10%는 그대로 둔다.
  `[MASK]`는 fine-tuning 때 나오지 않으므로, 사전학습과 fine-tuning 사이의
  불일치를 줄이려는 장치다.
- 입력 전체를 복원하는 denoising auto-encoder와 달리, 가려진 단어만 예측한다.
- BERT는 MLM과 함께 **Next Sentence Prediction(NSP)**도 학습한다. 문장 B가
  문장 A의 실제 다음 문장인지(50%) 무작위 문장인지(50%) 맞히는 과제로, QA와
  NLI에 도움이 된다고 보고한다.^[raw/papers/devlin-2019-bert-pre-training-of-deep.md]

## 결과와 쓰임

- 사전학습한 BERT는 출력층 하나만 추가해 fine-tuning하면 11개 NLP 과제에서
  당시 최고 성능을 냈다(GLUE 80.5%, SQuAD v1.1 Test F1 93.2 등). 이렇게 과제별로
  가중치를 갱신하는 방식은 [[fine-tuning-vs-in-context-learning]]에서 GPT-3의
  방식과 비교한다.^[raw/papers/devlin-2019-bert-pre-training-of-deep.md]
- 사전학습된 BERT는 다른 시스템의 부품으로도 쓰인다. RAG는 retriever의 query
  encoder와 document encoder를 모두 BERT-base 기반으로 구성한다. 자세한 내용은
  [[retrieval-augmented-generation]]에 있다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]

## 근거 수준

MLM 절차 자체는 BERT 논문 한 편에 근거하므로 `confidence: medium`이다.
