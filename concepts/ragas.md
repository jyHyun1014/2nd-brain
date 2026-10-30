---
title: "RAGAS"
created: "2026-10-30"
updated: "2026-10-30"
type: "concept"
tags: ["nlp", "retrieval"]
sources: ["raw/papers/2025-04-ragas-automated-evaluation-of-retrieval-augmented-generation.md"]
confidence: "medium"
contested: false
contradictions: []
---
# RAGAS (Retrieval Augmented Generation Assessment)

[[retrieval-augmented-generation]] 파이프라인을 사람이 만든 정답 라벨 없이 평가하는 프레임워크다.
핵심 착상은 사람이 직접 만든 중간 정답(ground-truth)에 인색한 설정, 즉 도메인 특화 데이터셋이나
정답이 없는 소수 라벨만 있는 상황을 전제로 삼는다는 것이다. LLM을 심판으로 세워 참조 정답 없이
품질을 채점한다.^[raw/papers/2025-04-ragas-automated-evaluation-of-retrieval-augmented-generation.md]

## 세 가지 무참조 지표

- **Faithfulness:** 답변에 나온 주장(claim)이 검색된 문맥에 의해 뒷받침되는 비율. 답변에서 주장
  목록을 뽑은 뒤, 각 주장을 문맥만 보고 판정할 수 있는지 LLM에 묻는다. `|문맥으로 뒷받침된 주장| / |전체 주장|`로
  계산한다.
- **Answer Relevance:** 답변이 원래 질문에 적합한지를 잰다. 답변에서 역으로 질문을 생성한 뒤,
  원 질문과 생성된 질문들의 임베딩 유사도(코사인) 평균을 낸다. 불완전하거나 중복된 정보가 많은
  답변은 점수가 낮다.
- **Context Relevance:** 검색된 문맥 중 실제로 질문에 필요한 문장의 비율. 문맥에서 관련 문장만
  뽑게 해 `|추출된 관련 문장| / |전체 문맥 문장|`로 계산한다. 관련 문장이 많을수록 정밀도가 낮다.^[raw/papers/2025-04-ragas-automated-evaluation-of-retrieval-augmented-generation.md]

## 사람 평가와의 일치

WikiEval 데이터셋(위키백과 문서에서 만든 50개 질문·문맥·답변)에 사람이 지은 관련성·사실성 점수를
붙이고, 세 지표가 그 점수와 얼마나 맞는지 상관계수로 비교한다.

- 사실성 지표는 사람의 사실성 점수와 유의하게 상관했다. 답변 관련성과 문맥 관련성도 사람 관련성
  점수와 유의하게 상관했다.
- 참조 기반 지표(ROUGE-L, BLEU)를 함께 비교하면, RAGAS가 사람 판단에 더 잘 맞고 화제가 바뀌는
  질문에도 덜 민감했다. 논문은 이 결과가 RAGAS가 correctness 지표와 어느 정도 직교함을 시사한다고
  해석한다.^[raw/papers/2025-04-ragas-automated-evaluation-of-retrieval-augmented-generation.md]

## 잠재적 편향과 대응

- **불필요한 주장:** LLM 심판이 답변에 그럴듯해 보이는 주장을 스스로 덧붙이면 Faithfulness가
  낮아진다.
- **지표의 미세한 차이에 둔감:** LLM이 문장 순서와 무관하게 문맥을 모두 같은 것으로 보면, 관련
  문장과 무관한 문장을 잘 구분하지 못할 수 있다.
- **자가 일관성(답변-문맥 관련성):** 답변 관련성이 높은 답변을 억지로 점수에 반영하려는 경향.
- 논문은 위 결과가 아직 예비적이라고 스스로 밝히고, 세 지표가 지닌 잠재적 교란 요인을 지표별로
  점검하는 절차를 제안한다.^[raw/papers/2025-04-ragas-automated-evaluation-of-retrieval-augmented-generation.md]

## 지위와 한계

RAGAS는 무참조 평가의 대표적 출발점이지만, 저자들은 세 지표를 쓰는 여러 가지 변형을 검증하지
않았다는 점과 WikiEval 규모가 작다는 점을 한계로 든다. 심판 LLM 자체의 편향도 배제하지 못한다.
[[self-rag]]처럼 검색 품질을 학습으로 끌어올리는 접근과는 달리, RAGAS는 관측과 진단에 집중한다.

## 근거 수준

Es 등의 논문 한 편에 근거하고, 저자 스스로 결과가 예비적이라고 밝히므로 `confidence: medium`이다.

## 관련 개념

- [[retrieval-augmented-generation]] — RAGAS가 평가 대상으로 삼는 파이프라인
- [[self-rag]] — 같은 RAG 개선 문제를 학습 기반 자기반성으로 접근하는 대응
- [[react]] — 근거 없는 주장(환각)을 행동·관측으로 줄이려는 또 다른 접근
