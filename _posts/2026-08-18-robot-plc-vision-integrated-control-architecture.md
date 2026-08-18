---
layout: post
title: "Robot + PLC + Vision 통합제어 아키텍처 — 산업 자동화 설계 실무"
date: 2026-08-18 11:12:00 +0900
author: 아진네트웍스 기술팀
categories:
- 제어SW
description: "산업용 Robot, PLC, 2D·3D Vision을 하나의 자동화 셀로 통합할 때 필요한 제어 책임경계, Handshake, 좌표변환, State Machine, 인터록, 장애복구와 FAT 설계 방법을 설명합니다."
keywords:
- Robot PLC Vision 통합제어
- 로봇 PLC 연동
- 머신비전 로봇 연동
- 자동화 제어 시스템
- PLC 인터록
- 로봇 비전 시스템
tags:
- RobotPLC
- 통합제어
- 머신비전
- PLC제어
- 로봇자동화
image: /assets/images/hero/plc-hmi-scada.svg
---

Robot + PLC + Vision 통합제어에서 가장 흔한 문제는 통신 프로토콜이 아니라 **누가 공정 상태의 최종 권한을 갖는지 불명확한 것**입니다. PLC, Robot Controller, Vision Controller가 각각 정상 동작해도 책임경계와 Handshake가 잘못 설계되면 간헐정지와 복구 불능 문제가 발생합니다.

<!--more-->

## 1. 기본 책임경계

일반적인 자동화 셀에서는 PLC가 전체 공정 State, 주변장치 Interlock, 생산 Sequence를 관리하고 Robot Controller는 Motion과 Tool 동작을 담당합니다. Vision은 영상 취득, Feature/Defect 검출, 좌표 또는 판정값 생성을 담당합니다. 다만 설비 특성에 따라 책임은 달라질 수 있으므로 프로젝트 시작 시 Control Philosophy를 문서화해야 합니다.

## 2. Handshake는 신호 목록이 아니라 상태계약이다

예를 들어 Vision Guidance는 `PLC Trigger Request → Camera Ready → Trigger → Processing → Result Valid → Robot Coordinate Receive → Ack → Result Clear`처럼 상태 전이를 정의해야 합니다. 단순히 Trigger와 OK 신호만 연결하면 이전 Cycle 데이터가 다음 Cycle에 사용되는 Race Condition이 발생할 수 있습니다.

Robot 역시 Start, Busy, Complete, Fault, Home, Area Clear, Tool State를 명확히 구분해야 합니다. 각 Bit의 Set/Reset 주체와 Timeout 조건을 Signal Matrix에 기록하는 것이 좋습니다.

## 3. State Machine 설계

설비 Sequence를 Step Number만으로 작성하면 개조가 반복될수록 유지보수가 어려워집니다. Idle, Ready, Running, Hold, Fault, Recovery, Manual과 같은 상위 State와 세부 Step을 분리하면 Alarm Recovery와 재기동 조건을 명확하게 만들 수 있습니다.

특히 Fault 발생 시 `처음부터 재시작`이 아니라 현재 제품 위치와 Tool 상태를 확인한 뒤 안전한 Recovery Point로 이동하도록 설계해야 제품 이중투입과 충돌을 줄일 수 있습니다.

## 4. Vision–Robot 좌표변환

2D Guidance는 Camera Pixel Coordinate를 Robot Coordinate로 변환하기 위한 Calibration이 필요합니다. 3D Vision은 X·Y뿐 아니라 Z와 자세정보가 추가되므로 Camera Coordinate, World Coordinate, Robot Base, Tool Center Point 사이의 Transformation 관리가 더 중요합니다.

카메라 고정형(Eye-to-Hand)과 로봇 장착형(Eye-in-Hand)은 Calibration 방식과 오차요인이 다릅니다. 렌즈, 작업거리, Fixture 반복정밀도, Robot 반복정밀도까지 Error Budget으로 관리해야 합니다.

## 5. 통신 방식 선정

Discrete I/O는 단순하고 진단이 쉽지만 대량 데이터 전송에는 부적합합니다. Industrial Ethernet은 상태와 데이터 교환에 유리하지만 제조사별 구현 차이를 확인해야 합니다. OPC UA나 MQTT는 상위 데이터 수집에 유용하지만 Hard Real-time Motion Interlock을 대체하는 용도로 단순 적용해서는 안 됩니다.

프로토콜 선정 기준은 데이터량, Cycle 요구, 진단성, 기존 표준, 유지보수 인력, Cybersecurity 정책입니다.

## 6. Alarm과 장애복구

좋은 Alarm은 `Vision Error`가 아니라 `ST30 Vision Result Timeout — Camera Ready 확인`처럼 공정 위치와 원인을 보여줍니다. HMI에는 현재 State, Step, Robot Status, Vision Result, Interlock Missing Condition을 동시에 표시하면 현장 복구성이 높아집니다.

통신 단절, Robot Fault, Vision NG, Tool Grip Fail, Sensor 불일치, 제품 유실 각각에 대해 자동재시도 가능 여부와 작업자 개입 조건을 정의해야 합니다.

## 7. FAT 검증 시나리오

정상 Cycle만 반복해서는 통합제어 품질을 검증할 수 없습니다. FAT에는 다음 Fault Injection이 포함되어야 합니다.

- Vision 응답 Timeout 및 NG
- Robot Busy 중 Start 중복 입력
- Grip Sensor 불일치
- PLC–Robot 통신 단절
- Cycle 중 Emergency Stop과 재가동
- 제품 유무 상태와 PLC 내부 State 불일치
- Manual 동작 후 Auto 복귀

## 8. 유지보수를 위한 표준화

Tag Naming, I/O List, Signal Matrix, Alarm Code, Robot Program Number, Vision Job Number, Recipe ID를 서로 연결하면 문제 추적이 쉬워집니다. 변경 이력과 Backup 기준도 설비 인수 문서에 포함해야 합니다.

## 관련 기술 Cluster

- [SCADA·HMI 아키텍처 실무]({% post_url 2026-08-18-SCADAHMI-아키텍처-완전-정복-아진네트웍스-기술팀-해설 %})
- [레거시 PLC 마이그레이션 가이드]({% post_url 2026-08-18-레거시-PLC-마이그레이션-가이드-아진네트웍스-해설 %})

## 기술검토·RFQ 요청

통합제어 RFQ에는 **I/O List, Robot 모델, Vision 구성, Network 구성도, Sequence, Alarm List, 목표 Cycle, Safety 범위, 기존 Source 접근 여부**를 포함하면 인터페이스와 책임경계를 빠르게 정의할 수 있습니다.

## 결론

Robot + PLC + Vision 통합의 핵심은 장비를 연결하는 것이 아니라 **공정 State와 데이터의 소유권, 신호 수명주기, 좌표계, Fault Recovery를 하나의 제어 아키텍처로 설계하는 것**입니다. 아진네트웍스는 기구·전장·PLC·Robot·Vision을 분리 발주 관점이 아닌 통합 Cell 관점에서 검토합니다.