# 나의 컨벤션 위키

C++ 코드와 Git 작업에서 반복되는 선택을 일관되게 하기 위한 개인 개발 기준입니다.

현재 **C++ 코딩 8개, Git 2개** 문서를 채택했습니다. 적용 범위와 변경 기록은 [컨벤션 적용 기준](baseline.md)에서 확인하세요.

## 빠르게 찾아보기

| 지금 하려는 작업 | 찾아볼 규칙 |
| --- | --- |
| 이름을 짓고 코드를 정리하기 | [명명](coding/cpp/naming.md) · [포맷](coding/cpp/formatting.md) |
| 변수와 객체 만들기 | [초기화](coding/cpp/initialization.md) · [const](coding/cpp/const.md) |
| 함수와 헤더 작성하기 | [함수 매개변수·반환](coding/cpp/functions.md) · [헤더·include](coding/cpp/headers.md) |
| 코드의 의도 설명하기 | [주석](coding/cpp/comments.md) |
| 자원의 소유자와 수명 정하기 | [소유권·수명](coding/cpp/ownership.md) |
| 변경을 기록하고 작업 시작하기 | [커밋 메시지](git/commit-messages.md) · [브랜치 명명](git/branches.md) |

## 처음 읽는 순서

1. [컨벤션 적용 기준](baseline.md)에서 적용 범위와 규칙 강도를 확인합니다.
2. [C++ 목차](coding/cpp/index.md)에서 포맷·명명을 시작으로 관련 규칙을 읽습니다.
3. [소유권·수명](coding/cpp/ownership.md)에서 자원 관리 규칙을, [Git·협업](git/index.md)에서 작업 기록 방식을 확인합니다.

각 페이지의 `필수`, `권장`, `선택`을 구분해 적용합니다. 프로젝트의 별도 합의는 적용 기준에 따라 범위와 이유를 명시한 예외로 관리합니다.

## 전체 목차

- [코딩](coding/index.md): C++ 명명, 포맷, 언어 사용과 소유권·수명 · HLSL 셰이더 초안
- [Git·협업](git/index.md): 커밋 메시지와 브랜치 명명

다음 분류에는 **아직 채택하지 않은 초안과 후속 항목**이 있습니다.

- [테스트·품질](quality/index.md): 테스트 범위, 회귀 검증과 품질 판단
- [문서화](documentation/index.md): README, 사용 안내와 설계 결정 기록
- [프로젝트별 규칙](projects/index.md): 프로젝트별 설계, 구성·빌드와 공통 규칙의 예외

## 적용 절차와 검토 중인 문서

- [RnimanEngine 프로젝트 기준](projects/rniman-engine.md): 컨벤션 적용·핵심 제약과 주요 원본 링크
- [위키와 프로젝트의 상호 반영](baseline.md#위키와-프로젝트의-상호-반영): 위키 우선 적용과 새 결정의 위키 반영 절차 (채택)
- [HLSL 셰이더 규칙](coding/hlsl.md): 단계별 파일과 `Main`, 명명·좌표 공간·공유 include (초안)
- [HTML 기본 컨벤션](coding/html.md): 문서 골격·포맷·의미 있는 요소·입력·JSX 차이 (초안)
- [Material Forge 참고 기록](projects/material-forge.md): HTML 초안의 로컬 근거와 프로젝트 적용 상태
- [변경 검증과 결과 기록](quality/verification.md): 빌드·실행·화면·성능 확인
- [원본과 생성물 관리](git/artifacts.md): 에셋·산출물·캐시 구분

새 초안은 기존 채택 문서 10개에 포함하지 않습니다. 프로젝트별 정보와 원본 접근 안내는 해당 프로젝트 문서에서 확인합니다.

## 참고 자료 안내

외부 가이드의 권고와 개인적으로 채택한 규칙은 각 페이지에서 구분합니다. 과거 개인 자료인 `ref/`는 로컬에만 보관하며 사이트에 포함하지 않습니다. 사이트에서 “로컬 참고 자료”로 표시된 출처는 공개 링크가 아닙니다.
