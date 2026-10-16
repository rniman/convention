# C++ auto 사용 규칙

[C++ 목차](index.md)

상태: 채택 · 채택일: 2026-10-15 · 적용 범위: C++11 이상(C 제외). 버전별 기능과 필수·권장·선택을 구분한다 · 개정일: 2026-10-16

**명시적 타입을 기본으로 하고, 타입의 의미가 명확하면서 중복을 줄이거나 직접 적기 어려운 타입을 다룰 때 `auto`를 사용한다.**

## 사용 기준

| 상황 | 기준 | 강도 |
| --- | --- | --- |
| 단순 숫자·불리언, 단위·부호·폭이 중요한 값 | `int count = 0;`처럼 타입 명시 | 권장 |
| 반환 타입이 불명확한 함수, API 상태 코드·핸들·외부 데이터 계약 | 실제 계약을 확인하고 타입 명시 | 권장 |
| 컨테이너 반복자·람다 객체 | `auto` 사용 | 권장 |
| 생성 타입이 드러나는 식, 범위 기반 for | 타입·소유 형태와 값·참조 의도가 명확하면 사용 | 선택 |
| 복잡한 템플릿·범위 어댑터 결과 | 역할과 수명·평가 방식을 확인할 수 있으면 사용 | 선택 |

**필수:** 가까운 선언·초기화 식에서 타입 의미를 판단할 수 있어야 한다. 길이·IDE 조회만으로 생략하지 않는다. 애매하면 명시하되 의도하지 않은 변환을 확인한다.

```cpp
int count = 0;
float deltaTime = GetDeltaTime(); // 실제 반환 타입이 float인 경우

auto it = values.begin(); // 가까운 선언에서 컨테이너 확인 가능
// C++14 이상, <memory>와 프로젝트의 Texture 정의 필요
auto texture = std::make_unique<Texture>();

// 피할 예: 반환 타입과 의미를 알기 어려운 호출
// auto result = Calculate();
```

## 값·참조와 주의사항

**필수:** 값 선언의 참조·최상위 `const` 제거와 lvalue 복사를 고려해 선택한다. 범위 기반 for에도 같은 기준을 적용한다.

| 표기 | 의도 |
| --- | --- |
| `auto value = source;` | 별도 값 보관 |
| `auto& value = source;` | 원본 참조, 비상수 원본 수정 가능 |
| `const auto& value = source;` | 참조를 통한 읽기 전용 접근 |
| `auto* value = pointer;` | 원시 포인터임을 표시 — 권장 |

- **필수:** 참조·포인터·뷰의 수명은 별도로 보장한다. `std::vector<bool>` 원소 같은 프록시의 값 선언은 독립 복사가 아닐 수 있으므로 불리언 복사본은 `bool`로 받는다.
- **필수:** `auto`는 정수 나눗셈·부호 혼합·오버플로를 해결하지 않는다. 예를 들어 `auto ratio = 1 / 2;`는 `int` 값 `0`이다.
- **권장:** 공개·비템플릿 함수의 반환 타입은 명시한다. `auto GetSize() -> Size;`는 반환 타입을 명시한 표기다.
- **선택:** C++17 구조적 바인딩은 요소의 의미가 명확할 때 사용하고 값·참조를 구분한다. `auto&&`, C++14의 `decltype(auto)`·반환 타입 추론·일반화 람다는 필요한 제네릭·보조 코드에 한정한다. C++20 함수 매개변수의 `auto`는 함수 템플릿을 만든다.

`=` 초기화를 유지하고 `auto`를 위한 불필요한 캐스트는 넣지 않는다. 관련 기준: [초기화](initialization.md) · [const](const.md) · [소유권](ownership.md) · [함수 반환](functions.md) · [변환 초안](conversions.md).

## 근거와 출처

[기존](../../../ref/CodingConvention.md)·[확장 컨벤션](../../../ref/DevRnimanConvention/CodingConvention.md)의 명확한 타입 원칙과 Core Guidelines의 중복 제거를 참고했다. 명시적 타입 기본은 사용자 선택이다.

출처 확인일: 2026-10-15. 언어 기준: C++11·14·17·20. 명세 링크는 현행 작업 초안이며 가이드는 2026-06-14 표시본이다.

- [C++ Core Guidelines ES.11](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-auto)
- [C++ 작업 초안 — placeholder type specifiers](https://eel.is/c++draft/dcl.spec.auto)
- [C++ 작업 초안 — placeholder type deduction](https://eel.is/c++draft/dcl.type.auto.deduct)

## 변경 기록과 적용 범위

- 2026-10-16: 반복 설명·중복 예시·배경을 줄여 핵심 규칙과 예시 중심으로 정리했다. 규칙 강도·예외·버전과 채택·초안·미결정 상태는 유지했다.

- 2026-10-15: 사용 조건·값과 참조·주의사항을 사용자 선택으로 채택했다.
- 적용: 개인 C++ 코드에 공통 기준으로 사용한다. 프로젝트별 예외와 반영 상태는 [컨벤션 적용 기준](../../baseline.md)을 따른다. 기존 코드 일괄 치환·자동 검사 설정은 제외한다.
