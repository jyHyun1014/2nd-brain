---
title: "SGLang"
created: "2026-10-22"
updated: "2026-10-22"
type: "concept"
tags: ["llm"]
sources: ["raw/papers/2024-06-sglang-efficient-execution-of-structured-language-model-programs.md"]
confidence: "medium"
contested: false
contradictions: []
---
# SGLang

여러 번의 LLM 호출과 제어 흐름으로 이뤄진 "LM program"을 쉽게 쓰고 효율적으로 실행하게 하는
시스템이다. 프런트엔드 언어와 런타임으로 구성된다.^[raw/papers/2024-06-sglang-efficient-execution-of-structured-language-model-programs.md]

## 해결하려는 문제

LLM 활용이 few-shot, [[self-consistency]], tree-of-thought 같은 프롬프트 기법, 에이전트
제어, 멀티모달 입력으로 넓어지면서 서로 의존하는 생성 호출을 여러 번 하는 구조가 흔해졌다.
논문은 이런 프로그램을 표현하고 효율적으로 실행하는 기존 시스템이 부족하다고 본다.^[raw/papers/2024-06-sglang-efficient-execution-of-structured-language-model-programs.md]

## 구성

- **프런트엔드:** Python에 내장된 언어로 생성(extend, gen, select)과 병렬 제어(fork, join)
  기본 요소를 준다. Python의 제어 흐름과 라이브러리와 호환돼 복잡한 프롬프트 워크플로를
  Python 문법으로 쓸 수 있다.
- **런타임 최적화 세 가지:**
  - **RadixAttention:** 모든 요청의 KV cache를 radix tree에 담은 LRU cache로 관리해, 여러 호출이
    공통 접두사를 재사용한다. 캐시 적중률을 높이는 cache-aware 스케줄링과 LRU 교체를 쓴다.
    continuous batching, paged attention, tensor parallelism과 함께 쓸 수 있다.
  - **압축 유한 상태 기계:** 구조화된 출력(JSON 등)의 제약 디코딩을 빠르게 한다. 기존 시스템은
    다음 토큰 하나만 마스킹으로 제약해 비효율적이라고 지적한다.
  - **API speculative execution:** GPT-4 같은 API 전용 모델에서 다중 호출 프로그램을 최적화한다.^[raw/papers/2024-06-sglang-efficient-execution-of-structured-language-model-programs.md]

## 결과

Llama 7B/70B, Mixtral 8x7B, LLaVA 같은 모델에서 에이전트 제어, 논리 추론, few-shot 벤치마크,
JSON 디코딩, [[retrieval-augmented-generation]] 파이프라인, 멀티턴 채팅을 시험했다. Guidance,
vLLM, LMQL 등 기존 시스템보다 처리량이 최대 6.4배 높았다고 보고한다.^[raw/papers/2024-06-sglang-efficient-execution-of-structured-language-model-programs.md]

## 근거 수준

SGLang 논문 한 편에 근거하므로 `confidence: medium`이다.

## 관련 개념

- [[self-consistency]] — 같은 접두사를 공유하는 다중 샘플 호출의 대표 사례
- [[retrieval-augmented-generation]] — 시험 대상 워크로드 중 하나
- [[llm-based-agents]] — 에이전트 제어가 시험 워크로드에 포함됨
