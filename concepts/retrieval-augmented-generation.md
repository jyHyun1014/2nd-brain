---
title: "Retrieval-Augmented Generation"
created: "2026-10-13"
updated: "2026-10-13"
type: "concept"
tags: ["nlp", "retrieval"]
sources: ["raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Retrieval-Augmented Generation (RAG)

사전학습된 생성 모델(parametric memory)에 외부 문서 검색(non-parametric memory)을
결합해, 검색한 문서를 근거로 답을 생성하는 방법이다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]

## 해결하려는 문제

큰 사전학습 언어 모델은 파라미터 안에 사실 지식을 저장하지만, 그 지식에 정확히
접근하고 다루는 능력은 제한적이다. 그래서 지식 집약적 과제에서는 과제 전용
구조보다 뒤처진다. 또 답의 출처를 제시하거나 지식을 갱신하는 일도 풀리지 않은
문제로 남아 있다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]

## 구성

- **Retriever (non-parametric memory):** Wikipedia를 dense vector index로 만들고,
  query encoder와 document encoder로 관련 문서를 찾는다. 두 encoder 모두 BERT-base
  기반이며, DPR의 사전학습된 bi-encoder로 초기화한다. BERT의 사전학습 방식은
  [[masked-language-modeling]]에 있다.
- **Generator (parametric memory):** BART-large, 즉 400M 파라미터의 사전학습된
  seq2seq [[transformer]]다. 입력과 검색된 문서를 이어 붙여 생성한다.
- **학습:** document encoder와 index는 고정하고, query encoder와 BART generator만
  fine-tuning한다. 논문은 document encoder까지 갱신하지 않아도 성능이 좋았다고 보고한다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]

## 두 가지 변형

- **RAG-Sequence:** 검색한 같은 문서 하나로 전체 출력 시퀀스를 생성하고, 상위 K개
  문서에 대해 확률을 합산(marginalize)한다.
- **RAG-Token:** 출력 토큰마다 다른 문서를 쓸 수 있어, 여러 문서의 내용을 섞어
  답을 만들 수 있다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]

## 결과

- 세 개의 open-domain QA 과제에서 당시 최고 성능을 냈고, parametric-only seq2seq
  모델과 과제 전용 retrieve-and-extract 구조를 모두 앞섰다.
- 생성 과제에서는 parametric-only 기준선보다 더 구체적이고 다양하며 사실에 맞는
  문장을 생성했다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]

## 다른 접근과의 관계

RAG는 지식을 프롬프트가 아니라 검색 결과로 공급하고, 모델 일부를 fine-tuning한다.
가중치 갱신 없이 프롬프트만 쓰는 방식과의 차이는
[[fine-tuning-vs-in-context-learning]]을 참고한다.

## 근거 수준

Lewis 논문 한 편에 근거하므로 `confidence: medium`이다.
