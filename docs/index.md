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

각 페이지의 `필수`, `권장`, `선택`을 구분해 적용하며, 프로젝트에서 합의한 별도 규칙이 있으면 해당 합의를 우선합니다.

## 전체 목차

- [코딩](coding/index.md): C++ 명명, 포맷, 언어 사용과 소유권·수명
- [Git·협업](git/index.md): 커밋 메시지와 브랜치 명명

다음 분류는 **목차만 준비된 후속 정리 항목**입니다.

- [설계](design/index.md): 디자인 패턴, 책임 분리, 모듈·계층과 의존성
- [프로젝트 구성·빌드](build/index.md): 폴더 배치, 빌드 타깃, 의존성과 개발 도구
- [테스트·품질](quality/index.md): 테스트 범위, 회귀 검증과 품질 판단
- [문서화](documentation/index.md): README, 사용 안내와 설계 결정 기록
- [프로젝트별 규칙](projects/index.md): 특정 프로젝트·엔진·플랫폼의 선택과 예외

## 참고 자료 안내

외부 가이드의 권고와 개인적으로 채택한 규칙은 각 페이지에서 구분합니다. 과거 개인 자료인 `ref/`는 로컬에만 보관하며 사이트에 포함하지 않습니다. 사이트에서 “로컬 참고 자료”로 표시된 출처는 공개 링크가 아닙니다.
