---
layout: post
title: "자동화 설비 투자비·ROI 산정 방법 — 견적 전 반드시 계산할 항목"
date: 2026-08-18 11:14:00 +0900
author: 아진네트웍스 기술팀
categories:
- 스마트팩토리
description: "로봇·비전·물류·포장 자동화 설비의 투자비를 기구, 로봇, 전장, 제어, 설치, 시운전으로 분해하고 인건비·생산성·불량·다운타임을 반영해 ROI를 검증하는 방법을 정리합니다."
keywords:
- 자동화 설비 ROI
- 자동화 설비 견적
- 로봇 자동화 비용
- 스마트팩토리 투자비
- 자동화 투자 회수기간
- 자동화 설비 제작 비용
tags:
- 자동화ROI
- 설비견적
- 투자비
- 생산성
- 스마트팩토리
image: /assets/images/hero/oee-smart-factory.svg
---

자동화 투자 검토에서 가장 위험한 방식은 `로봇을 넣으면 몇 명이 줄어드는가`만으로 ROI를 계산하는 것입니다. 실제 투자비에는 로봇 외에도 EOAT, 기구, 전장, PLC, Vision, Safety, 설치와 시운전이 포함되고, 효과 측에도 생산량, 불량, 재작업, 다운타임, Changeover가 영향을 줍니다.

<!--more-->

## 1. CAPEX를 Work Breakdown Structure로 분해한다

초기 견적은 최소한 다음 범위로 분리해야 합니다.

- Robot/Servo/Actuator 등 구동계
- EOAT, Jig, Conveyor, Frame, Guard 등 기구부
- PLC, HMI, Panel, Sensor, Safety 등 전장부
- Vision Camera, Lens, Light, Controller
- Robot Teaching, PLC/HMI, Vision Software
- 설계 Engineering
- 조립, 배선, Debugging
- FAT, 포장·운송, 현장 설치, SAT
- 교육, 문서, Spare Part

이 구조를 사용하면 견적 비교 시 단순 총액이 아니라 Scope 차이를 확인할 수 있습니다.

## 2. 인건비 절감은 실제 투입시간으로 계산한다

현재 작업자 수 전체를 자동화 절감인원으로 잡아서는 안 됩니다. 자동화 후에도 Loading, 자재공급, 검사, 복구, Changeover 인력이 남을 수 있기 때문입니다.

현재 공정의 작업자별 순수 작업시간과 대기시간을 관찰하고, 자동화 후 제거되는 작업시간만 분리하는 방식이 보수적입니다.

## 3. 생산성 효과

생산성은 설비 최고속도가 아니라 병목공정의 Effective Cycle로 평가해야 합니다. 자동화 후 Cycle이 빨라져도 전후공정이 따라오지 못하면 전체 생산량은 증가하지 않습니다.

따라서 Current CT, Target CT, Bottleneck CT, Changeover Time, Planned/Unplanned Downtime을 함께 기록해야 합니다.

## 4. 품질비용을 포함한다

자동화가 수동 편차를 줄이는 공정이라면 불량, 재작업, 폐기, 고객 Claim 비용 감소가 투자효과가 될 수 있습니다. 그러나 개선률을 임의로 가정하지 말고 기존 품질실적과 PoC/FAT 결과를 기준으로 Scenario를 작성해야 합니다.

## 5. 다운타임 리스크

복잡한 자동화는 생산성을 높이는 동시에 고장 시 영향범위를 키울 수 있습니다. MTBF, MTTR 데이터가 없다면 최소한 주요 고장모드, Spare 확보시간, Manual Bypass 가능 여부, 원격지원 범위를 검토해야 합니다.

Brownfield 개조는 설치 중 생산중단 비용도 투자판단에 포함해야 합니다.

## 6. ROI 계산 구조

연간 편익은 `직접 인건비 절감 + 추가 생산 기여 + 품질비용 절감 + 기타 검증 가능한 절감`으로 구성하고, 여기서 자동화로 증가하는 유지보수비와 운영비를 차감합니다. 단순 회수기간은 총 투자비를 연간 순편익으로 나누어 비교할 수 있습니다.

다만 생산 증가분을 금액으로 환산할 때는 매출액 전체가 아니라 실제 공헌이익 또는 회사가 승인한 재무 기준을 사용하는 것이 적절합니다.

## 7. 세 가지 Scenario로 검토한다

한 개의 ROI 숫자보다 Conservative, Base, Upside 세 Scenario가 의사결정에 유용합니다. Conservative에는 낮은 생산량, 잔존인력, 초기 Ramp-up, 예상 유지비를 반영합니다. Base는 합의된 목표값, Upside는 추가 증산 가능성을 반영하되 각각의 Assumption을 공개해야 합니다.

## 8. 견적 요청 전에 고객이 준비하면 좋은 데이터

- 제품 종류, 도면, 중량과 연간 생산량
- 현재 공정 Layout과 작업인원
- 공정별 Cycle Time
- 교대수와 연간 가동일
- 불량·재작업 실적
- 목표 CAPA와 자동화 범위
- 기존 PLC/Robot/Vision 사양
- 설치공간과 Utility
- 목표 납기와 허용 생산중단 기간

이 정보가 충분할수록 예비견적의 불확실성이 낮아집니다.

## 9. PoC와 단계투자

제품 거동이나 검사성능이 불확실한 공정은 처음부터 전체 양산라인을 발주하기보다 핵심 메커니즘을 PoC로 검증하는 편이 안전합니다. PoC 비용은 추가비용처럼 보일 수 있지만 대규모 설비의 기술 리스크를 앞단에서 제거하는 Engineering 비용으로 볼 수 있습니다.

## 결론

자동화 ROI의 핵심은 낙관적인 절감률을 만드는 것이 아니라 **투자 Scope와 현재 공정 데이터를 같은 기준으로 구조화하는 것**입니다. 아진네트웍스는 현장조사, Cycle 분석, Concept 설계, Preliminary BOM, PoC 범위를 기반으로 기술성과 경제성을 함께 검토합니다.