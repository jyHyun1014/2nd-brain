---
title: "Vision Transformer"
created: "2026-10-21"
updated: "2026-10-30"
type: "concept"
tags: ["pretraining"]
sources: ["raw/papers/2021-06-an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md", "raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md", "raw/papers/2026-10-recurrent-vision-transformers-for-event-based-spacecraft-pose-estimation-under-slow-relative-motions.md", "raw/papers/2026-10-the-explainability-illusion-must-vits-exhibit-patch-decoding-interpretability.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Vision Transformer (ViT)

이미지를 패치 시퀀스로 바꿔 NLP의 표준 [[transformer]] encoder에 그대로 넣는
이미지 분류 모델이다. 논문은 CNN에 기대지 않아도 순수 Transformer가 이미지
분류에서 잘 작동한다고 보이며, 이미지 고유의 inductive bias를 패치 추출 단계
외에는 넣지 않았다고 밝힌다.^[raw/papers/2021-06-an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md]

## 구조

- 이미지를 평탄화한 2D 패치 시퀀스로 바꾸고, 학습되는 linear projection으로 D차원
  패치 임베딩을 만든다. 패치는 NLP의 토큰처럼 취급되고, 패치 수가 Transformer의
  입력 시퀀스 길이가 된다.
- [[masked-language-modeling]]의 BERT가 쓰는 `[class]` 토큰처럼 학습되는 임베딩을
  시퀀스 앞에 붙이고, 그 출력 상태를 이미지 표현으로 쓴다. 위치 정보는 표준 1D
  학습형 position embedding으로 준다. 2D를 고려한 임베딩은 의미 있는 향상이 없었다.
- encoder는 multi-head self-attention과 MLP 블록을 번갈아 쌓은 원 Transformer
  구조를 가능한 한 그대로 따른다.
- 모델 크기는 ViT-Base(86M), Large(307M), Huge(632M)이며 Base와 Large는 BERT의
  설정을 그대로 가져왔다.
- 사전학습 후 파인튜닝하며, 더 높은 해상도로 파인튜닝할 때는 패치 크기를 유지해
  시퀀스를 늘리고 position embedding을 2D 보간한다.^[raw/papers/2021-06-an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md]

## 규모와 데이터

- ImageNet 같은 중간 규모 데이터로만 학습하면 비슷한 크기의 ResNet보다 몇 퍼센트
  포인트 낮다. 논문은 Transformer에 translation equivariance와 locality 같은 CNN의
  inductive bias가 없어서라고 해석한다.
- 14M~300M 이미지로 사전학습하면 결과가 뒤집히며, 논문은 "대규모 학습이
  inductive bias를 이긴다"고 요약한다. JFT-300M으로 사전학습한 ViT-H/14는
  ImageNet 88.55%, CIFAR-100 94.55%, VTAB 19개 과제 77.63%를 보고한다.
- ViT-L/16(JFT)은 BiT-L보다 모든 보고 과제에서 앞서면서 사전학습 비용이
  0.68k TPUv3-core-days로, BiT-L의 9.9k보다 훨씬 적다. 통제된 실험에서는 같은
  성능에 ResNet보다 약 2~4배 적은 연산이 들었고, 시험한 범위에서 포화하지 않았다.
  모델·데이터를 키울수록 나아지는 이 경향은 언어 쪽의 [[language-model-scaling]]과
  같은 방향이다.^[raw/papers/2021-06-an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md]

## 자기지도 사전학습

BERT의 마스크 언어 모델을 본떠 마스크된 패치를 예측하는 자기지도 사전학습을
예비 실험했다. ViT-B/16은 ImageNet 79.9%로 처음부터 학습한 경우보다 2% 좋지만
지도 사전학습보다는 4% 낮다.^[raw/papers/2021-06-an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md]

DINO는 이 방향을 이어받아 ViT를 라벨 없이 자기 증류로 학습한다. 라벨 없이 학습해도
마지막 블록 attention에 의미적 분할 정보가 나타나고, 파인튜닝 없이 k-NN 분류만으로
경쟁력 있는 성능을 낸다. 특히 k-NN이 linear 평가에 근접하는 성질은 DINO를 ViT에
썼을 때만 나타난다.^[raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md]
학습 방법과 결과는 [[self-supervised-vision-pretraining]]에 정리했다.

## 열린 질문

논문은 detection·segmentation 같은 다른 비전 과제, 자기지도 사전학습 방법의
추가 탐색, 더 큰 규모로의 확장을 남은 과제로 든다.^[raw/papers/2021-06-an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md]

## 후속 연구와 해석

- **계층형 변형:** [[swin-transformer]]는 이동 윈도우로 attention을 지역화해 dense prediction에
  쓸 수 있는 계층형 백본을 만든다.
- **시간축 확장:** 우주선 자세 추정 논문은 recurrent vision transformer(RVT)로 희소한 이벤트 카메라
  데이터의 장기 정보를 순환 메모리에 담는다. 상대 운동이 느릴수록 이벤트 발생률이 떨어져 신호 대
  잡음비가 낮아지는 문제를 겨냥한다. RVT 기반 히트맵 회귀기로 2D-3D 대응점을 만들고 PnP로 자세를
  구한다. 실제 이벤트 카메라로 모은 데이터에서 프레임 단위 방법과 고정 시간 창 변형보다 정확하고
  안정적이었다고 보고한다.^[raw/papers/2026-10-recurrent-vision-transformers-for-event-based-spacecraft-pose-estimation-under-slow-relative-motions.md]
- **패치 토큰 해석 가능성:** ViT 분류기의 개별 패치 토큰을 디코딩하면 사람이 이해할 만한 결과가
  나온다고 흔히 가정한다. 최근 논문은 이것이 구조의 고유한 성질이 아님을 보인다. 실제 모델 중 일부는
  디코딩 결과가 이미지 의미와 정렬되지만(aligned), 다른 모델은 설명 맵이 뒤집혀 있거나(inverted)
  이미지 의미와 아예 상관이 없다(unexplainable). CLIP, SigLIP 같은 대조 학습 비전-언어 모델은
  대체로 뒤집혀 있다. 같은 구조도 조건에 따라 영역이 바뀌며, 이 성질은 가정하지 말고 모델마다
  확인해야 한다고 결론짓는다.^[raw/papers/2026-10-the-explainability-illusion-must-vits-exhibit-patch-decoding-interpretability.md]

## 관련 개념

- [[swin-transformer]] — 계층형 특징 맵과 이동 윈도우 attention으로 확장한 백본
- [[transformer]] — ViT가 입력만 바꿔 재사용하는 원 구조
- [[masked-language-modeling]] — 마스크된 패치 예측의 모델이 된 사전학습 목표
- [[self-supervised-vision-pretraining]] — 라벨 없이 ViT를 학습하는 DINO 계열 접근
- [[language-model-scaling]] — 규모에 따른 성능 향상이라는 대응 관찰
