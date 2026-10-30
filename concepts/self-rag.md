---
title: "Self-RAG"
created: "2026-10-22"
updated: "2026-10-22"
type: "concept"
tags: ["llm", "retrieval"]
sources: ["raw/papers/2023-10-self-rag-learning-to-retrieve-generate-and-critique-through-self-reflection.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Self-RAG (Self-Reflective Retrieval-Augmented Generation)

모델이 필요할 때만 검색하고, 검색한 문서와 자신의 출력을 **reflection token**으로 스스로
평가하게 학습시키는 [[retrieval-augmented-generation]] 변형이다. 임의의 언어 모델 하나를
end-to-end로 학습한다.^[raw/papers/2023-10-self-rag-learning-to-retrieve-generate-and-critique-through-self-reflection.md]

## 해결하려는 문제

기존 RAG는 검색이 도움이 되는지와 상관없이 고정된 개수의 문서를 무차별로 붙인다. 논문은
이것이 모델의 범용성을 해치고 무관한 문서가 품질 낮은 생성으로 이어질 수 있다고 본다.
또 모델이 제공된 근거를 따르도록 명시적으로 학습되지 않아 출력이 검색 문서와 일치한다는
보장도 없다고 지적한다.^[raw/papers/2023-10-self-rag-learning-to-retrieve-generate-and-critique-through-self-reflection.md]

## Reflection token

reflection token은 검색 토큰과 비평(critique) 토큰으로 나뉘며 네 종류를 쓴다.^[raw/papers/2023-10-self-rag-learning-to-retrieve-generate-and-critique-through-self-reflection.md]

| 토큰 | 판단 대상 | 값 |
| --- | --- | --- |
| Retrieve | 검색이 필요한가 | yes / no / continue |
| ISREL | 검색 문서가 질문과 관련 있는가 | relevant / irrelevant |
| ISSUP | 출력이 문서로 뒷받침되는가 | fully / partially / no support |
| ISUSE | 출력이 질문에 유용한가 | 5~1점 |

## 추론과 학습

- **추론:** 매 세그먼트(실험에서는 한 문장)마다 검색 토큰으로 검색 필요성을 판단한다.
  필요 없으면 일반 언어 모델처럼 다음 세그먼트를 생성하고, 필요하면 여러 문서를 병렬로
  처리하며 비평 토큰으로 관련성과 근거 여부를 평가해 최선의 출력을 고른다. 이
  토큰으로 추론 시점에 모델의 행동을 과제에 맞게 조절할 수 있다.
- **학습:** critic 모델이 말뭉치에 reflection token을 오프라인으로 삽입하고, 생성기는 어휘를
  확장한 일반 언어 모델링 목표로 학습한다. critic은 GPT-4를 프롬프트해 모은 데이터로
  지도학습하며, 이 덕분에 학습 중 critic을 띄울 필요가 없다.^[raw/papers/2023-10-self-rag-learning-to-retrieve-generate-and-critique-through-self-reflection.md]

## 결과

7B와 13B 모델이 open-domain QA, 추론, 사실 검증 과제에서 ChatGPT와 검색을 붙인
Llama2-chat을 앞섰고, 긴 글 생성에서는 사실성과 인용 정확도가 크게 좋아졌다고 보고한다.^[raw/papers/2023-10-self-rag-learning-to-retrieve-generate-and-critique-through-self-reflection.md]

## 근거 수준

Asai 등의 논문 한 편에 근거하므로 `confidence: medium`이다.

## 관련 개념

- [[retrieval-augmented-generation]] — Self-RAG가 개선하는 기본 RAG 구조
- [[graph-rag]] — 검색 단위를 그래프 요약으로 바꾼 또 다른 RAG 변형
- [[ragas]] — ISREL·ISSUP 비평이 겨냥하는 품질을 참조 없이 채점하는 평가 틀
- [[marginal-viewpoint-utility]] — 고정 개수 문서를 붙이는 관행을 토큰 예산으로 대체하는 접근
- [[reinforcement-learning-from-human-feedback]] — reflection token이 영감을 받았다고 밝힌 reward model 계열 기법
