---
title: "Marginal Viewpoint Utility"
created: "2026-10-30"
updated: "2026-10-30"
type: "concept"
tags: ["retrieval", "llm"]
sources: ["raw/papers/2026-10-learning-marginal-viewpoint-utility-for-budgeted-evidence-selection-in-rag.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Marginal Viewpoint Utility (LMVU)

[[retrieval-augmented-generation]]에서 검색 결과에서 어떤 문서를 골라 넣을지를, 문서 개수가 아니라
토큰 예산 제약 아래에서 정하는 기준이다. 후보 문서를 "관측 지점(viewpoint)"으로 보고, 질의응답에
얼마나 도움이 되는지를 이미 뽑힌 문서 집합 대비 한계 기여(marginal gain)로 측정한다.^[raw/papers/2026-10-learning-marginal-viewpoint-utility-for-budgeted-evidence-selection-in-rag.md]

## 동기

RAG 파이프라인은 보통 고정된 top-k를 가져온다. 하지만 문서 길이가 제각각이고, 겹치는 문서가 많으면
개수 기준 선택은 토큰을 낭비하거나 정보를 놓친다. LMVU는 선택을 토큰 예산 문제로 다시 세운다.
같은 정보를 반복하는 문서는 두 번째부터 기여가 거의 없고, 서로 다른 관측 지점을 채우는 문서는
작아도 기여가 크다.^[raw/papers/2026-10-learning-marginal-viewpoint-utility-for-budgeted-evidence-selection-in-rag.md]

## 방법

- **한계 효용 점수:** 각 후보 문서가 이미 선택된 집합에 더했을 때 답변 품질을 얼마나 올리는지
  추정한다. 문서의 절대적 관련성이 아니라 한계 기여를 본다는 점이 reranking과 다르다.
- **예산 제약:** 문서 길이를 토큰 비용으로 환산해, 문맥 창에 들어갈 수 있는 예산 안에서 효용이
  큰 순서로 고른다. 짧고 정보가 독립적인 문서가 긴 중복 문서보다 우선될 수 있다.
- **관측 지점 관점:** 여러 문서를 서로 다른 각도에서 본 하나의 관측으로 취급해, 집합이 얼마나
  다양한 관점을 덮는지를 유용성으로 환산한다.^[raw/papers/2026-10-learning-marginal-viewpoint-utility-for-budgeted-evidence-selection-in-rag.md]

## 기존 접근과의 관계

- **reranking:** 관련도 점수 순으로 정렬하는 방식은 문서 간 중복을 보지 않는다. LMVU는 집합
  수준에서 중복을 벌점으로 반영한다.
- **top-k:** 개수 고정은 예산 고정과 다르다. LMVU는 같은 토큰 예산에서 더 나은 정보 조합을
  겨냥한다.
- **self-RAG 계열:** 검색 여부와 문서 선별을 스스로 판단하는 학습 기반 접근과 방향은 같지만,
  LMVU는 유용성을 명시적 한계 효용 값으로 계산하는 쪽에 무게를 둔다.^[raw/papers/2026-10-learning-marginal-viewpoint-utility-for-budgeted-evidence-selection-in-rag.md]

## 근거 수준

단일 논문에 근거하므로 `confidence: medium`이다. 회색 문헌 성격이 강하고 표준 벤치마크에서의
폭넓은 재현 결과가 아직 확인되지 않았으므로, [[ragas]] 같은 평가 체계로 검증할 여지가 남아 있다.

## 관련 개념

- [[retrieval-augmented-generation]] — LMVU가 개선하려는 파이프라인
- [[ragas]] — 예산 하 선별이 답변 품질에 미치는 영향을 측정할 평가 틀
- [[graph-rag]] — 그래프 구조로 검색 대상을 조직하는 대안적 검색 전략
- [[self-rag]] — 검색과 선별을 스스로 결정하는 학습 기반 대응
