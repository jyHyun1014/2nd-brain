---
title: "GraphRAG"
created: "2026-10-22"
updated: "2026-10-22"
type: "concept"
tags: ["llm", "retrieval", "knowledge-graph"]
sources: ["raw/papers/2025-02-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md"]
confidence: "medium"
contested: false
contradictions: []
---
# GraphRAG

LLM이 만든 지식 그래프와 커뮤니티 요약을 색인으로 써서, 말뭉치 전체에 대한 질문에 답하는
[[retrieval-augmented-generation]] 방식이다.^[raw/papers/2025-02-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md]

## 해결하려는 문제

일반적인 벡터 RAG는 질문과 개별적으로 관련 있는 문서 몇 개를 찾아 LLM의 context window에
넣는다. 답이 소수의 레코드에 모여 있는 질문에는 잘 맞지만, "데이터셋의 주요 주제는
무엇인가" 같이 전체에 대한 이해가 필요한 sensemaking 질문에는 맞지 않는다. 이런 질문은
검색 과제가 아니라 질의 중심 요약(QFS) 과제이기 때문이다. 반대로 기존 QFS 방법은 RAG
시스템이 색인하는 분량으로 확장되지 않는다.^[raw/papers/2025-02-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md]

## 파이프라인

1. **색인 시점:** LLM으로 원문에서 엔티티를 노드, 관계를 엣지로 하는 지식 그래프를 만든다.
2. 그래프를 Leiden 알고리즘 등으로 가까운 엔티티의 커뮤니티 계층으로 나누고, 아래에서
   위로 커뮤니티 요약을 미리 생성한다. 상위 요약은 하위 요약을 재귀적으로 포함한다.
3. **질의 시점:** 각 커뮤니티 요약으로 부분 답을 병렬로 만들고(map), 부분 답들을 다시
   요약해 최종 답을 낸다(reduce).^[raw/papers/2025-02-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md]

## 결과

- 약 100만 토큰 규모의 두 데이터셋(팟캐스트 전사, 뉴스 기사)에서 벡터 RAG 대비 답의
  포괄성(comprehensiveness) 승률은 팟캐스트 72~83%, 뉴스 72~80%였고, 다양성 승률은
  각각 75~82%와 62~71%였다. 직접성(directness)에서는 벡터 RAG가 가장 직접적인 답을
  냈다. empowerment 비교는 결과가 엇갈렸다.
- 원문 요약 방식과 비교하면 하위 커뮤니티 요약(C3)은 context 토큰이 26~33% 적고, 루트
  수준(C0)은 97% 넘게 적다. 논문은 C0가 반복 질의에 효율적인 대안이라고 본다.^[raw/papers/2025-02-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md]

## 한계

평가가 약 100만 토큰짜리 두 말뭉치의 sensemaking 질문에 한정된다. 다른 도메인으로의
일반화와 SelfCheckGPT 같은 방법을 쓴 허위 생성 비율 비교는 추가 연구가 필요하다고 밝힌다.^[raw/papers/2025-02-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md]

## 근거 수준

Edge 등의 논문 한 편에 근거하므로 `confidence: medium`이다.

## 관련 개념

- [[retrieval-augmented-generation]] — GraphRAG가 보완하는 벡터 RAG의 기본 구조
- [[self-rag]] — 검색 필요성을 모델이 스스로 판단하는 다른 RAG 변형
- [[in-context-learning]] — context window에 넣을 수 있는 분량의 한계라는 공통 배경
