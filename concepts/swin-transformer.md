---
title: "Swin Transformer"
created: "2026-10-22"
updated: "2026-10-22"
type: "concept"
tags: ["pretraining"]
sources: ["raw/papers/2021-08-swin-transformer-hierarchical-vision-transformer-using-shifted-windows.md"]
confidence: "medium"
contested: false
contradictions: []
---
# Swin Transformer

계층적 특징 맵을 만들고 이동 윈도우(shifted window) 안에서만 self-attention을 계산해, 이미지 크기에
선형인 계산 복잡도를 갖는 범용 비전 Transformer 백본이다.^[raw/papers/2021-08-swin-transformer-hierarchical-vision-transformer-using-shifted-windows.md]

## 해결하려는 문제

[[vision-transformer]] 계열은 낮은 해상도의 단일 특징 맵을 만들고 self-attention을 전역으로
계산해, 계산량이 이미지 크기의 제곱에 비례한다. 고해상도 이미지나 detection·segmentation
같은 dense prediction에는 이것이 큰 부담이다. 논문은 언어와 비전 사이의 규모와 해상도
차이를 이유로 든다.^[raw/papers/2021-08-swin-transformer-hierarchical-vision-transformer-using-shifted-windows.md]

## 구조

- 작은 패치에서 시작해 깊은 층으로 갈수록 이웃 패치를 합쳐 계층 표현을 만든다. patch merging
  층은 2×2 이웃 패치의 특징을 이어 붙인 뒤 선형 층을 적용해 토큰 수를 4분의 1로 줄인다.
- self-attention은 이미지를 나누는 겹치지 않는 윈도우 안에서만 계산한다. 윈도우당 패치 수가
  고정이라 복잡도가 이미지 크기에 선형이 된다. 연속한 두 블록에서 윈도우 분할을 이동시켜
  윈도우 사이의 연결도 얻는다.
- 각 head의 attention에 상대 위치 편향을 더한다. 절대 위치 임베딩을 입력에 더하면 성능이
  약간 떨어져 쓰지 않았다.
- 기본 설정은 윈도우 크기 M=7, head당 query 차원 32, MLP 확장 비율 4다. Swin-T와 Swin-S는
  ResNet-50(DeiT-S)과 ResNet-101과 비슷한 모델 크기·계산량이다.^[raw/papers/2021-08-swin-transformer-hierarchical-vision-transformer-using-shifted-windows.md]

## 결과

ImageNet-22K(1,420만 장)로 사전학습한 뒤 fine-tuning해 ImageNet-1K top-1 87.3%, COCO test-dev
box AP 58.7과 mask AP 51.1, ADE20K val mIoU 53.5를 냈다. 이전 최고 성능 대비
COCO box AP +2.7, mask AP +2.6, ADE20K +3.2 mIoU 향상이다.^[raw/papers/2021-08-swin-transformer-hierarchical-vision-transformer-using-shifted-windows.md]

## 근거 수준

Swin 논문 한 편에 근거하므로 `confidence: medium`이다.

## 관련 개념

- [[vision-transformer]] — Swin이 개선한 전역 attention 기반 이미지 분류 모델
- [[transformer]] — 윈도우 단위로 재구성한 원래 attention 구조
- [[language-model-scaling]] — 사전학습 규모를 키워 성능을 올리는 같은 흐름
