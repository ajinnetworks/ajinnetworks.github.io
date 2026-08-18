---
layout: post
title: "2D·3D 머신비전 검사 선정 기준 — 카메라·조명·렌즈·정밀도 실무 가이드"
date: 2026-08-18 11:13:00 +0900
author: 아진네트웍스 기술팀
categories:
- 딥러닝비전
description: "2D와 3D 머신비전 중 어떤 방식을 선택해야 하는지 검사목적, 결함 크기, FOV, 해상도, 조명, 렌즈, 높이정보, Cycle Time과 PoC 기준으로 설명합니다."
keywords:
- 2D 3D 비전검사 선정
- 머신비전 카메라 선정
- 비전검사 시스템
- 3D 비전검사
- 산업용 카메라
- 머신비전 조명
tags:
- 머신비전
- 2D비전
- 3D비전
- 비전검사
- 자동화검사
image: /assets/images/hero/ai-vision.svg
---

비전검사에서 2D와 3D의 선택은 최신 기술 여부가 아니라 **검출해야 할 결함이 어떤 물리량으로 표현되는가**로 결정해야 합니다. 색상, 명암, 윤곽, 인쇄 상태처럼 영상 평면에서 구분 가능한 특징은 2D가 효율적일 수 있고, 높이·단차·체적·변형처럼 Z 정보가 필요한 문제는 3D가 필요할 수 있습니다.

<!--more-->

## 1. 먼저 Defect Specification을 만든다

카메라 모델을 고르기 전에 검사 대상과 판정 기준을 수치화해야 합니다. 최소 결함 크기, 검사영역(FOV), 허용 위치편차, 표면 재질, 색상, 반사 특성, 제품 이동속도, 검사시간, 양품 변동범위를 정리합니다.

`스크래치 검사`처럼 모호한 요구사항 대신 `검출해야 할 최소 폭과 길이, 위치, 대비 특성`을 정의해야 광학계를 설계할 수 있습니다.

## 2. 2D Vision이 적합한 경우

2D는 X-Y 영상에서 특징을 추출합니다. 유무, 방향, 치수, 인쇄, OCR/OCV, 색상, 윤곽, 표면 결함 등은 2D 후보가 됩니다. 단, 광택 금속이나 투명체는 대상 자체보다 조명 설계가 성능을 좌우하는 경우가 많습니다.

Area Camera와 Line Scan Camera의 선택도 제품 크기와 이동 방식에 따라 달라집니다. 연속 웹이나 넓은 표면은 Line Scan이 유리할 수 있지만 Encoder 동기와 이송 안정성이 중요합니다.

## 3. 3D Vision이 필요한 경우

높이, 단차, 휨, 체적, 조립 깊이, 무작위 적재물의 자세처럼 Z 데이터가 판정의 핵심이면 3D를 검토합니다. Laser Profiling, Structured Light, Stereo/ToF 등 방식마다 정밀도, 작업거리, 재질 민감도, Cycle 특성이 다릅니다.

3D라는 이유만으로 모든 검사가 쉬워지는 것은 아닙니다. 검은색·고광택·투명 표면, Occlusion, 진동, 이동속도는 3D 데이터 품질을 떨어뜨릴 수 있으므로 실제 Sample 검증이 필요합니다.

## 4. 해상도와 FOV 계산의 기본

검사영역이 커질수록 같은 카메라 Pixel 수에서 물체측 해상도는 낮아집니다. 따라서 최소 결함을 안정적으로 검출하기 위해 필요한 Pixel 수를 먼저 정하고 FOV와 Sensor Resolution을 역산해야 합니다.

단순히 고화소 카메라를 선택하면 Exposure와 Data Transfer, Processing Time이 증가할 수 있으므로 Cycle과 함께 최적화해야 합니다.

## 5. Lens와 Working Distance

렌즈는 FOV, Sensor Size, Working Distance, 왜곡 허용치에 따라 선정합니다. 정밀 치수검사는 원근 오차를 줄이기 위해 Telecentric Lens를 검토할 수 있지만 비용과 설치공간이 증가합니다. 일반 검출에서는 고정초점 Lens가 더 합리적일 수 있습니다.

DOF가 부족하면 제품 높이 편차에 따라 Focus가 변하므로 Fixture 정밀도 또는 광학 조건을 함께 검토해야 합니다.

## 6. 조명이 검사 성능을 결정한다

Ring, Bar, Dome, Coaxial, Backlight, Dark-field 등 조명 방식은 결함을 카메라가 보기 쉬운 대비로 바꾸는 역할을 합니다. 광택 표면에서는 편광, 확산, 입사각 제어가 필요할 수 있습니다.

AI 알고리즘을 적용하더라도 광학적으로 결함이 보이지 않는 영상을 소프트웨어만으로 안정적으로 해결하기는 어렵습니다. 따라서 PoC는 알고리즘보다 광학 Sample Test부터 시작하는 것이 효율적입니다.

## 7. Rule-based와 Deep Learning 선택

치수, 위치, 명확한 Threshold처럼 규칙을 정의할 수 있는 문제는 Rule-based가 설명성과 검증성에서 유리합니다. 정상 변동이 크거나 비정형 결함처럼 규칙 정의가 어려운 경우 Deep Learning을 검토할 수 있습니다. 두 방식을 Hybrid로 구성하는 것도 가능합니다.

성능평가는 단순 Accuracy 하나보다 결함별 Recall, False Reject, False Accept와 실제 생산 분포를 함께 확인해야 합니다.

## 8. PLC·Robot·MES 연동

비전은 독립 장비가 아니라 생산설비의 일부입니다. Trigger 조건, Result Valid, Result Code, 좌표값, Recipe, Timeout, Retry, Reject Tracking을 PLC와 정의해야 합니다. Robot Guidance라면 Calibration과 좌표변환이 추가되고, MES 연동이라면 Image 저장정책과 Traceability ID가 필요합니다.

## 9. PoC 승인 기준

PoC에는 양품과 불량 Sample 수량, 결함별 구성, 조명 조건, 생산속도, 위치변동 범위를 사전에 정의합니다. 테스트 결과는 Detection Rate뿐 아니라 오검·미검 사례와 원인을 남겨야 합니다. Sample이 부족하면 양산 성능을 확정적으로 주장하지 않는 것이 기술적으로 정직합니다.

## 결론

2D/3D 머신비전 선정의 출발점은 카메라 브랜드가 아니라 **Defect Specification → 광학계 → 해상도/FOV → 알고리즘 → Cycle → PLC/Robot 연동 → PoC**입니다. 아진네트웍스는 실제 Sample을 기준으로 광학 테스트와 자동화 인터페이스를 함께 검토합니다.