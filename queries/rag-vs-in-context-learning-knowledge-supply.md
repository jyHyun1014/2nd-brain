---
title: "RAG와 In-Context Learning은 지식을 어떻게 공급하나"
created: "2026-10-19"
updated: "2026-10-19"
type: "query"
tags: ["llm", "retrieval", "prompting"]
sources: ["raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md", "raw/papers/brown-2020-language-models-are-few-shot.md"]
confidence: "high"
contested: false
contradictions: []
---
# RAG와 In-Context Learning은 지식을 어떻게 공급하나

## 질문

[[retrieval-augmented-generation]](RAG)과 [[in-context-learning]]은 답에 필요한 사실
지식을 모델에 어떻게 공급하는가? 같은 과제에서 결과는 어떻게 다른가?

## 짧은 답

- **RAG:** 사실 지식을 **모델 밖의 검색 index**에서 가져온다. 질문마다 관련 문서를
  찾아 입력에 붙이고, 생성기는 그 문서를 근거로 답한다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]
- **In-context learning (GPT-3):** 사실 지식은 **사전학습으로 파라미터에 흡수된 것**을
  쓴다. 프롬프트의 예시는 지식이 아니라 과제의 형식을 알려 준다. GPT-3 논문의
  closed-book QA 평가는 외부 문서를 쓰지 않을 뿐 아니라 QA 데이터셋으로 fine-tuning하는
  것도 허용하지 않는다.^[raw/papers/brown-2020-language-models-are-few-shot.md]

## 비교

| 항목 | RAG | In-context learning (GPT-3) |
| --- | --- | --- |
| 사실 지식의 위치 | 외부 Wikipedia index (non-parametric) + 생성기 파라미터 | 모델 파라미터 |
| 프롬프트·입력에 들어가는 것 | 질문 + 검색한 문서 | 과제 설명 + 예시 몇 개 + 질문 |
| 과제별 학습 | query encoder와 생성기를 fine-tuning | 없음 (가중치 갱신 없음) |
| 지식 갱신 | index를 교체하면 재학습 없이 갱신 | 파라미터를 바꿔야 함 (RAG 논문이 parametric-only 모델의 한계로 지적) |
| 근거 제시 | 검색한 문서를 함께 보여줄 수 있음 | 답의 근거 문서가 없음 |
| 규모 | 학습 파라미터가 훨씬 적음 (생성기 400M) | 175B 파라미터 |

- RAG 논문은 파라미터에만 지식을 저장하는 모델이 기억을 쉽게 넓히거나 고칠 수 없고,
  예측의 근거를 보여주기 어렵고, 환각을 일으킬 수 있다고 지적한다. RAG는 검색 index를
  바꿔 끼워 재학습 없이 지식을 갱신할 수 있음을 보였다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]
- RAG 논문은 비슷한 크기의 parametric-only 모델(T5-large, 770M)이 Natural Questions에서
  28.9 EM에 그친 반면 RAG-Sequence는 44.5를 냈다며, 검색을 섞은 모델이 훨씬 적은 학습
  파라미터로 강한 성능을 낸다고 해석한다. 대신 index는 21M개 문서 벡터(153억 개 값)를
  따로 저장해야 한다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]

## 같은 과제에서의 결과

GPT-3 논문의 open-domain QA 표가 두 방식을 같은 데이터셋에 나란히 둔다(정확도, %).^[raw/papers/brown-2020-language-models-are-few-shot.md]

| 방식 | Natural Questions | WebQuestions | TriviaQA |
| --- | --- | --- | --- |
| RAG (fine-tuning + 검색) | **44.5** | **45.5** | 68.0 |
| GPT-3 zero-shot | 14.6 | 14.4 | 64.3 |
| GPT-3 one-shot | 23.0 | 25.3 | 68.0 |
| GPT-3 few-shot | 29.9 | 41.5 | **71.2** |

- **표 읽는 법:** GPT-3 논문의 RAG 행은 데이터셋마다 두 변형 중 높은 값을 가져왔다.
  RAG 논문 원표로는 NQ는 RAG-Sequence 44.5(RAG-Token 44.1), WebQuestions는 RAG-Token
  45.5(RAG-Sequence 45.2)다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]
- **TriviaQA:** GPT-3는 one-shot에서 RAG와 같고 few-shot에서는 앞선다. 두 논문 모두
  TriviaQA **Wiki 테스트 세트** 기준이라 같은 조건의 비교다. RAG 논문은 표준 open-domain
  테스트 세트 점수(RAG-Sequence 56.8)도 따로 보고하며, TriviaQA에서 최고 성능을 낸 건
  T5와 비교 가능한 Wiki 세트에서뿐이라고 밝힌다.^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]^[raw/papers/brown-2020-language-models-are-few-shot.md]
- **Natural Questions:** RAG가 크게 앞선다. GPT-3 논문은 이 데이터셋의 질문이 Wikipedia의
  아주 세밀한 지식을 묻기 때문에 GPT-3의 용량과 사전학습 분포의 한계를 시험하는 것일 수
  있다고 해석한다.
- **모델 크기:** GPT-3 논문은 세 데이터셋 모두에서 성능이 모델 크기에 따라 매끄럽게 오르며,
  이는 용량이 클수록 더 많은 지식이 파라미터에 흡수된다는 생각과 맞을 수 있다고 본다.
  이 관점은 [[language-model-scaling]]과 이어진다.^[raw/papers/brown-2020-language-models-are-few-shot.md]

## 정리

두 논문은 같은 문제, 즉 사실 지식을 어떻게 모델에 공급할지에 반대 방향으로 답한다.

- **GPT-3:** 모델을 키워 지식을 파라미터 안에 더 많이 담는다.
- **RAG:** 지식을 바깥 index에 두고 필요할 때 꺼내 쓴다. 갱신과 근거 제시가 쉽고 학습
  파라미터가 적다.

결과는 데이터셋마다 달라서 어느 한쪽이 항상 낫다고 할 수 없다. TriviaQA에서는 큰 모델의
파라미터 지식만으로 RAG와 같거나 더 높았고, GPT-3 논문이 "Wikipedia의 아주 세밀한 지식"을
묻는다고 설명한 Natural Questions에서는 검색을 쓰는 RAG가 크게 앞섰다. 지식을 갱신하는 부담과 학습 방식의 차이는
[[fine-tuning-vs-in-context-learning]]에서도 다룬다.^[raw/papers/brown-2020-language-models-are-few-shot.md]^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]

## 주의할 점

- 위 표의 수치는 GPT-3 논문이 정리한 것이다. TriviaQA는 두 논문 모두 Wiki 테스트
  세트를 썼다. 다만 표준 테스트 세트에서는 RAG 점수가 56.8로 낮아지므로, TriviaQA
  비교는 어느 테스트 세트인지와 함께 읽어야 한다.^[raw/papers/brown-2020-language-models-are-few-shot.md]^[raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md]
- 이 위키에는 검색과 in-context learning을 함께 쓰는 방식, 즉 검색한 문서를 큰 모델의
  프롬프트에 넣는 방식을 다룬 원본이 아직 없다. 두 방식의 결합은 열린 질문으로 남긴다.
