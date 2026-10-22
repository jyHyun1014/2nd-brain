---
title: "Retrieval-Augmented Generation"
created: "2026-10-13"
updated: "2026-10-22"
type: "concept"
tags: ["nlp", "retrieval"]
sources: ["raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md", "raw/papers/2024-03-retrieval-augmented-generation-for-large-language-models-a-survey.md"]
confidence: "high"
contested: false
contradictions: []
---
# Retrieval-Augmented Generation (RAG)

사전학습된 생성 모델(parametric memory)에 외부 문서 검색(non-parametric memory)을
결합해, 검색한 문서를 근거로 답을 생성하는 방법이다.^[raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md]

## 해결하려는 문제

큰 사전학습 언어 모델은 파라미터 안에 사실 지식을 저장하지만, 그 지식에 정확히
접근하고 다루는 능력은 제한적이다. 그래서 지식 집약적 과제에서는 과제 전용
구조보다 뒤처진다. 또 답의 출처를 제시하거나 지식을 갱신하는 일도 풀리지 않은
문제로 남아 있다.^[raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md]

## 구성

- **Retriever (non-parametric memory):** Wikipedia를 dense vector index로 만들고,
  query encoder와 document encoder로 관련 문서를 찾는다. 두 encoder 모두 BERT-base
  기반이며, DPR의 사전학습된 bi-encoder로 초기화한다. BERT의 사전학습 방식은
  [[masked-language-modeling]]에 있다.
- **Generator (parametric memory):** BART-large, 즉 400M 파라미터의 사전학습된
  seq2seq [[transformer]]다. 입력과 검색된 문서를 이어 붙여 생성한다.
- **학습:** document encoder와 index는 고정하고, query encoder와 BART generator만
  fine-tuning한다. 논문은 document encoder까지 갱신하지 않아도 성능이 좋았다고 보고한다.^[raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md]

## 두 가지 변형

- **RAG-Sequence:** 검색한 같은 문서 하나로 전체 출력 시퀀스를 생성하고, 상위 K개
  문서에 대해 확률을 합산(marginalize)한다.
- **RAG-Token:** 출력 토큰마다 다른 문서를 쓸 수 있어, 여러 문서의 내용을 섞어
  답을 만들 수 있다.^[raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md]

## 결과

- 세 개의 open-domain QA 과제에서 당시 최고 성능을 냈고, parametric-only seq2seq
  모델과 과제 전용 retrieve-and-extract 구조를 모두 앞섰다.
- 생성 과제에서는 parametric-only 기준선보다 더 구체적이고 다양하며 사실에 맞는
  문장을 생성했다.^[raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md]

## 다른 접근과의 관계

RAG는 지식을 프롬프트가 아니라 검색 결과로 공급하고, 모델 일부를 fine-tuning한다.
가중치 갱신 없이 프롬프트만 쓰는 방식과의 차이는
[[fine-tuning-vs-in-context-learning]]을 참고한다.

## 이후 발전: Naive, Advanced, Modular RAG

2024년 서베이는 RAG가 환각, 오래된 지식, 추적 불가능한 추론 같은 LLM의 문제를 외부 데이터베이스의
지식으로 줄이는 방법이라고 정리하고, 연구 흐름을 세 단계로 나눈다.^[raw/papers/2024-03-retrieval-augmented-generation-for-large-language-models-a-survey.md]

- **Naive RAG:** 색인, 검색, 생성의 "Retrieve-Read" 틀이다. 색인은 PDF, HTML 같은 다양한 형식의
  원자료를 정제해 평문으로 바꾸고, 언어 모델의 context 제한에 맞춰 chunk로 나눠 만든다.
- **Advanced RAG:** 검색 품질을 높이려고 검색 전·후 전략을 쓰고, 색인도 슬라이딩 윈도우, 세밀한
  분할, 메타데이터로 다듬는다.
- **Modular RAG:** 앞 두 방식의 사슬 구조보다 유연하다. 예컨대 Rewrite-Retrieve-Read는 LLM이
  검색 질의를 다시 쓰는 모듈을 둔다.

RAG의 개선은 추론 단계에 머물지 않고 LLM fine-tuning과 결합하는 쪽으로 넓어졌다. 서베이는 연구
단계를 사전학습, fine-tuning, 추론으로 구분한다.^[raw/papers/2024-03-retrieval-augmented-generation-for-large-language-models-a-survey.md]
이 위키에서 검색 여부를 모델이 스스로 판단하도록 학습하는 변형은 [[self-rag]]에, 검색 단위를
그래프 요약으로 바꾼 변형은 [[graph-rag]]에 정리했다.

## 평가

서베이는 RAG 평가를 검색 품질과 생성 품질로 나눈다. 핵심 지표는 context relevance(검색된 context의
정밀도), answer faithfulness(답이 context에 충실한가), answer relevance다. 능력 측면에서는
noise robustness, negative rejection(근거가 없을 때 답을 삼가는 능력), information integration(여러
문서의 정보를 종합), counterfactual robustness(문서 속 알려진 오류를 무시하는 능력)를 든다.
RAGAS, ARES, TruLens 같은 도구는 LLM으로 품질 점수를 매긴다.^[raw/papers/2024-03-retrieval-augmented-generation-for-large-language-models-a-survey.md]

## 근거 수준

Lewis 논문(원 구조)과 2024년 서베이(이후 분류와 평가)가 서로 다른 시기와 측면을 다루며
모순되지 않으므로 `confidence: high`로 올린다.

## 열린 질문

- **검색 붕괴(retrieval collapse):** 이야기 생성 같은 일부 과제에서는 검색기가
  입력과 상관없이 같은 문서만 가져오도록 학습되고, 그러면 생성기가 문서를 무시해
  BART와 같은 성능이 된다. 논문은 원인을 사실 지식이 덜 필요한 과제이거나 출력이
  길어 검색기 학습 신호가 약하기 때문일 수 있다고 추정만 한다.^[raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md]
- **지식 갱신:** 논문은 검색 index만 바꿔 끼우면(hot-swap) 재학습 없이 지식을
  갱신할 수 있다고 보였다. 다만 이 위키의 원본은 Wikipedia index 실험 하나뿐이다.^[raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md]

## 관련 개념

- [[transformer]] — 생성기 BART의 구조
- [[masked-language-modeling]] — 검색기 encoder로 쓰인 BERT의 사전학습
- [[fine-tuning-vs-in-context-learning]] — 모델 일부를 fine-tuning하는 위치
- [[rag-vs-in-context-learning-knowledge-supply]] — GPT-3와 같은 QA 과제에서의 지식 공급 방식 비교
- [[self-rag]] — 검색 필요성과 근거를 모델이 스스로 판단하는 변형
- [[graph-rag]] — 지식 그래프와 커뮤니티 요약으로 전체 질문에 답하는 변형
- [[sglang]] — RAG 파이프라인을 포함한 다중 호출 워크로드의 실행 시스템
