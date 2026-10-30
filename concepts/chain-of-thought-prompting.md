---
title: "Chain-of-Thought Prompting"
created: "2026-10-13"
updated: "2026-10-30"
type: "concept"
tags: ["llm", "prompting"]
sources: ["raw/papers/2023-01-chain-of-thought-prompting-elicits-reasoning-in-large-language-models.md", "raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Chain-of-Thought Prompting

Few-shot 프롬프트의 예시에 **최종 답만이 아니라 중간 추론 단계(chain of thought)**까지
적어 넣어, 큰 언어 모델이 복잡한 추론을 하도록 이끄는 방법이다.^[raw/papers/2023-01-chain-of-thought-prompting-elicits-reasoning-in-large-language-models.md]

## 방법

- 기준선인 standard prompting은 질문-답 쌍을 in-context 예시로 주고 모델이 바로
  답을 내게 한다. 이 방식은 [[in-context-learning]]에 정리했다.
- Chain-of-thought prompting은 같은 few-shot 구조에서 예시의 답 앞에 단계별
  추론을 함께 적는다.
- 별도 학습 없이, 충분히 큰 기성 언어 모델에 이런 예시를 넣는 것만으로 추론
  능력을 끌어낼 수 있다고 보고한다.^[raw/papers/2023-01-chain-of-thought-prompting-elicits-reasoning-in-large-language-models.md]

## 결과

- 세 종류의 대형 언어 모델에서 산술, 상식, 기호 추론 과제 성능이 올랐다.
- 540B 파라미터 모델(PaLM)에 chain-of-thought 예시 8개만 주었을 때 수학 문장제
  벤치마크 GSM8K에서 당시 최고 정확도를 냈고, verifier를 붙여 fine-tuning한
  GPT-3보다도 높았다. 프롬프트만 쓴 방식이 fine-tuning을 넘은 사례로,
  [[fine-tuning-vs-in-context-learning]]에서 비교한다.^[raw/papers/2023-01-chain-of-thought-prompting-elicits-reasoning-in-large-language-models.md]

## 모델 크기에 따라 나타나는 능력

논문은 chain-of-thought 추론을 "모델 규모의 emergent ability"라고 부른다.

- 작은 모델에서는 성능을 올리지 못하고, 약 100B 파라미터 모델에서야 효과가 나타난다.
- 10B보다 작은 대부분의 모델에서는 오히려 성능을 떨어뜨린다.
- 따라서 효과를 작은 모델의 성능을 연장해서 예측할 수 없다.

모델 크기와 능력의 관계는 [[language-model-scaling]]에서 함께 다룬다.^[raw/papers/2023-01-chain-of-thought-prompting-elicits-reasoning-in-large-language-models.md]

## 이후 발전: 행동과의 결합

CoT 추론은 정적이라서 모델 내부 표현에만 의존하고 외부 세계에 grounded되지 않는다. 그래서
사실 환각과 오류 전파가 생긴다. [[react]]는 CoT를 기준선으로 삼아, 추론 흔적에 환경을 바꾸는
행동과 그 관측을 끼워 넣는다. HotpotQA에서 CoT의 최대 실패 유형은 환각(56%)이지만, ReAct는
추론·행동·관측을 번갈아 넣는 구조 제약 때문에 환각은 0%가 되고 대신 추론 오류(47%)가 주된
실패가 된다. 지식 집약 과제에서도 CoT(EM 29.4)보다 ReAct(EM 27.4)가 약간 낮은 대신, 둘을
번갈아 쓰면 34~35까지 올라간다.^[raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md]

## 근거 수준

이 방법 자체는 Wei 논문 한 편에 근거하므로 `confidence: medium`이다.

## 열린 질문

논문이 직접 밝힌 한계는 다음과 같다.^[raw/papers/2023-01-chain-of-thought-prompting-elicits-reasoning-in-large-language-models.md]

- 사람의 사고 과정을 흉내 내지만, 신경망이 실제로 "추론"을 하는지는 답하지 않고
  열린 질문으로 남긴다.
- 추론 과정이 맞다는 보장이 없어 맞는 답과 틀린 답이 모두 나올 수 있다.
- 큰 모델에서만 효과가 나타나 실제 서비스 비용이 크다. 작은 모델에서 추론을
  끌어내는 방법은 후속 연구 과제다.
- few-shot에서는 예시에 추론을 직접 적는 비용이 작지만, fine-tuning용 데이터를
  만들 때는 이 비용이 커질 수 있다.

## 관련 개념

- [[in-context-learning]] — 기준이 되는 standard few-shot prompting
- [[language-model-scaling]] — 효과가 나타나는 모델 크기
- [[fine-tuning-vs-in-context-learning]] — 프롬프트만으로 fine-tuning을 넘은 사례
- [[self-consistency]] — 여러 추론 경로를 뽑아 다수결로 답을 고르는 후속 디코딩 방법
- [[react]] — CoT에 행동·관측을 결합해 외부 자원에 grounded시키는 후속 패러다임
- [[llm-based-agents]] — CoT를 에이전트 배포 방식으로 쓰는 맥락
