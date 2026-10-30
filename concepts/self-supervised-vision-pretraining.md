---
title: "Self-Supervised Vision Pretraining"
created: "2026-10-30"
updated: "2026-10-30"
type: "concept"
tags: ["pretraining"]
sources: ["raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md"]
confidence: "medium"
contested: false
contradictions: []
---
# 자기지도 비전 사전학습 (Self-Supervised Vision Pretraining)

라벨 없이 시각 특징을 학습해, 파인튜닝 없이도 쓸 수 있는 특징을 얻는 접근이다. [[vision-transformer]]를
무라벨로 학습했을 때 나타나는 성질을 다룬 DINO 연구를 중심으로 정리한다.^[raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md]

## 개념

기존 비전 사전학습은 큰 데이터로 먼저 학습한 뒤 과제 데이터로 파인튜닝하는 전략을 따르는데,
이때 supervision이 이미지가 담은 풍부한 정보를 미리 정의된 몇 천 개 범주 중 하나로 줄여버린다.
자기지도 학습은 이 문제를 라벨 대신 이미지 자체에서 만든 pretext task로 대체한다. 언어 쪽에서
masked language modeling 같은 목표가 준 풍부한 학습 신호를 비전에 옮기려는 시도다.^[raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md]

## 무라벨 ViT에서 나타나는 두 가지 성질

- **명시적인 장면 구조:** 자기지도 ViT의 특징은 이미지의 의미적 분할(segmentation) 정보를 포함한다.
  마지막 블록 self-attention의 `[CLS]` 토큰을 보면 라벨 없이도 클래스별 영역에 주목하는 지도가
  만들어진다. 이 성질은 지도 학습 ViT나 CNN에서는 그렇게 분명하게 나타나지 않는다.
- **강한 k-NN 분류기:** 파인튜닝도 linear classifier도 데이터 증강 없이, 학습 특징에 대한 최근접
  이웃 분류만으로 작은 ViT가 ImageNet top-1 78.3%를 낸다. 저자들은 이 k-NN 성능이 momentum
  encoder와 multi-crop 증강을 함께 쓸 때만 나온다고 밝힌다.^[raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md]

## 방법 DINO

DINO는 라벨 없는 자기 증류(self-distillation)로 해석되는 자기지도 방법이다.
student 네트워크가 momentum encoder로 만든 teacher 네트워크의 출력을 예측하도록 표준 cross-entropy
손실로 학습한다. teacher 파라미터는 student의 지수이동평균으로 갱신한다.^[raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md]

- **붕괴 방지:** 별도의 predictor, 고급 정규화, contrastive loss 없이 teacher 출력의 centering과
  sharpening만으로 collapse를 막는다. centering은 한 차원이 지배하는 것을 막는 대신 균일 분포로
  가게 하고, sharpening은 반대 효과를 내므로 둘을 함께 써서 균형을 맞춘다.
- **multi-crop:** 224 해상도의 global view 2개와 작은 영역을 덮는 96 해상도 local view 여러 개를
  쓴다. local은 student에만 통과시켜 local-to-global 대응을 학습한다.
- **패치 크기:** ViT에서는 더 작은 패치가 특징 품질을 크게 높인다. 패치를 줄이면 파라미터는 늘지
  않지만 처리량이 떨어진다.^[raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md]

## 결과

- ViT-Base/8로 ImageNet linear 평가 80.1% top-1, k-NN으로 77.4%를 보고하며, 이전 최고보다
  파라미터가 10배 적고 실행이 1.4배 빨랐다. ResNet-50에서도 당시 최고 수준에 도달해 CNN에서도
  작동함을 확인한다.
- ViT-small에서 linear 77.0% 대비 k-NN 74.5%로 두 평가가 거의 비슷한데, 이 성질은 DINO를 ViT에
  쓸 때만 나타나고 다른 자기지도 방법이나 ResNet-50에서는 나타나지 않는다.
- 학습 비용도 보고한다. ViT-S/16 DINO는 8-GPU 서버 두 대로 3일 동안 학습해 ImageNet linear
  76.1%를 냈다. ViT-Base/8은 linear 80.1% top-1을 냈다.
- **적은 라벨로의 전이:** ImageNet 라벨이 10%뿐일 때 DINO ViT-S/16 특징은 동결 상태에서 k-NN 69.1%,
  linear 72.2%를 낸다. 1% 라벨에서는 k-NN 61.3%, linear 64.5%다. 같은 DINO로 학습한 ResNet-50과
  비교하면 ViT-S가 대부분 앞서고 특히 k-NN에서 격차가 크지만, Places205 linear 평가에서는 ViT-S가
  조금 낮아 우위가 도메인에 따라 갈린다.^[raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md]

## 파생 능력

- **객체 분할:** 학습 목표나 구조가 dense task를 겨냥하지 않았는데도, 파인튜닝 없이 연속 프레임
  최근접 이웃만으로 DAVIS-2017 비디오 인스턴스 분할에서 경쟁력 있는 성능을 낸다. 작은 패치 변형이
  더 좋았다.
- **이미지 검색:** Oxford/Paris 재방문 데이터셋에서 DINO 특징이 ImageNet 라벨로 학습한 특징보다
  좋았고, 라벨이 필요 없어 랜드마크 검색용 데이터셋(GLDv2)으로도 학습할 수 있음을 보였다.^[raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md]

## 근거 수준

DINO 논문 한 편에 근거하므로 `confidence: medium`이다. 자기지도 사전학습 자체의 잠재력은
[[vision-transformer]]가 인용한 ViT 논문의 마스크 패치 예비 실험에서도 언급되지만, 그 실험에서는
지도 사전학습보다 낮았다.

## 관련 개념

- [[vision-transformer]] — DINO가 라벨 없이 학습한 백본
- [[language-model-scaling]] — 사전학습 규모와 데이터가 성능을 좌우한다는 같은 전제
- [[in-context-learning]] — 라벨 없이 얻은 표현이 소량 라벨 과제로 전이되는 방식의 대응물
