# C++ 명명 규칙

[C++ 목차](index.md)

상태: 채택 · 적용 범위: 직접 작성하는 C++ 식별자 · 예제: C++11 이상 · 개정일: 2026-10-16

## 기본 규칙

아래 표기는 **필수**이며 상수는 [상수 명명](#상수-명명)을 우선한다.

| 대상 | 표기 | 예시 |
| --- | --- | --- |
| 클래스·구조체·열거형 타입 | `PascalCase` | `Player`, `ResourceState` |
| 일반 함수·멤버 함수 | `PascalCase` | `LoadTexture`, `GetHealth` |
| 지역 변수·매개변수 | `camelCase` | `frameIndex`, `damageAmount` |
| 클래스의 비정적 멤버 변수 | `m` + `PascalCase` | `mHealth` |
| 클래스의 정적 멤버 변수 | `s` + `PascalCase` | `sPlayerCount` |
| 전역 변수 | `g` + `PascalCase` | `gFrameCount` |
| 구조체의 비정적 데이터 멤버 | `camelCase` | `positionX` |
| `enum class`의 열거자 | `PascalCase` | `ResourceState::Ready` |

`PascalCase`는 모든 단어, `camelCase`는 첫 단어를 제외한 단어의 첫 글자를 대문자로 쓴다. `m`·`s`·`g`는 범위를 구별하는 개인 접두어다.

## 상수 명명

`const`·`constexpr`나 초기값의 계산 시점이 아닌 **선언 범위**로 정한다. 아래 표기는 **필수**다.

| 선언 범위 | 표기 | 예시 |
| --- | --- | --- |
| 함수·블록 내부 — 지역 `static` 포함 | `camelCase` | `retryLimit`, `remainingCount` |
| 전역·네임스페이스, 클래스·구조체의 정적 상수 | `UPPER_SNAKE_CASE` | `MAX_FRAME_COUNT`, `WORKER_COUNT` |
| 비정적 `const` 데이터 멤버 | 기본 멤버 규칙 | 클래스 `mPlayerId`, 구조체 `playerId` |

- **필수:** 대문자 상수에 `m`·`s`·`g`·`k` 접두어를 붙이지 않는다.
- 변수 자체가 `const`인 경우에 적용한다(`constexpr`, `T* const` 포함). 대상만 읽기 전용인 `const T*`·`const T&`는 기본 변수 규칙을 따른다.
- `constexpr` 함수는 기본 함수 규칙을 따른다. 키워드 선택은 [const 사용 규칙](const.md)에서 다룬다.

```cpp
constexpr int MAX_FRAME_COUNT = 3;

int GetRemainingCount(int frameCount)
{
	static constexpr int retryLimit = 3;
	const int remainingCount = frameCount - retryLimit;
	return remainingCount > 0 ? remainingCount : 0;
}
```

## 의미가 드러나는 이름

| 대상 | 규칙·예시 | 강도 |
| --- | --- | --- |
| 동작 함수 | `Load`·`Create`·`Get` 등 동사로 시작. 성공 여부를 반환해도 `LoadTexture` 사용 | 필수 |
| 상태 질의 `bool` 함수 | `Is`·`Has`·`Can`·`Should` 사용. `IsAlive`, `HasTexture` | 필수 |
| 열거자 | 타입 이름을 반복하지 않음. `ResourceState::Ready` | 필수 |
| 일반 이름 | 역할을 드러냄. 피해량은 `damageAmount` | 권장 |

<span id="네임스페이스-초안"></span>

## 네임스페이스

적용 범위: 직접 작성하는 엔진 코드 · 채택일: 2026-10-16

| 항목 | 규칙·예시 | 강도·예외 |
| --- | --- | --- |
| 루트 | 엔진 공통 제품 루트 사용: `example::Logger` | 권장. `example`은 설명용 이름 |
| 큰 모듈 | 충돌·API 구분·독립 책임이 필요할 때 하위 구분 추가: `example::graphics::Renderer` | 선택 |
| 표기 | 소문자 `snake_case`: `example`, `asset_loading` | 권장 |
| 폴더·프로젝트 대응 | 일대일 대응을 강제하지 않고 논리적 소속이 같으면 유지 | 권장. 폴더 추가·이동이나 프로젝트 분리만으로 이름을 바꾸지 않음 |
| 별도 제품·외부 코드 | 독립 제품은 자체 루트 선택 가능. 외부·생성 코드는 원래 표기 유지 | 선택·예외. 솔루션 전체에 엔진 루트를 강제하지 않음 |

예를 들어 `Engine/Core/Memory/Allocator.h`는 `example::Allocator`, `Engine/Graphics/Renderer.h`는 `example::Renderer`로 시작할 수 있다. `Core`·`Memory` 폴더가 있다는 이유로 하위 네임스페이스를 추가하지 않는다. 예시는 타입의 전체 이름이며 특정 네임스페이스 선언 문법을 요구하지 않는다.

### 프로젝트별 결정 사항

공통 규칙의 미결정 항목이 아니다. 필요한 시점에 선택·이유·적용 범위·예외를 프로젝트에 기록한다.

| 항목 | 결정할 내용 |
| --- | --- |
| 실제 루트 | 제품 식별 이름과 적용 코드 범위 |
| 큰 모듈 | 하위 이름·대상 API·타입·추가 시점 |
| 별도 제품 | 독립 앱·도구·라이브러리의 자체 루트와 엔진 루트의 경계 |

<span id="네임스페이스-초안의-근거"></span>

### 네임스페이스 규칙의 근거

[Google — Namespace Names](https://google.github.io/styleguide/cppguide.html#Namespace_Names)의 `snake_case`와 제품·팀을 식별하는 루트를 참고했다. 사용자 선택으로 공통 루트·조건부 모듈 구분을 채택하며 폴더 대응은 강제하지 않는다. 확인일: 2026-10-16.

## 예외와 미결정 사항

- 생성자·소멸자·연산자, 외부 재정의·`begin`·`end` 등 계약상 정해진 이름은 유지한다. 외부·생성 코드에 자체 규칙을 강제하지 않는다.
- 외부 매크로와 충돌하면 소속 기능이 드러나는 구체적인 이름을 사용한다.
- **미결정:** 매크로, 상수가 아닌 구조체 정적 멤버, 일반 약어의 대소문자 표기. 채택 범위에서 제외한다.

## 관련 문서

- [const 사용 규칙](const.md)
- [코드 폴더·파일 이름](project-structure.md#폴더파일-이름)

## 근거와 출처

이 문서는 개인 스타일이다. Google의 변수 `snake_case`·멤버 후행 `_`·상수 `k` 접두어와 달리 범위 접두어와 선언 범위별 상수 표기를 사용한다. Google은 정적 저장 기간 상수에 상수 표기를 요구하고 자동 지역 상수는 일반 변수 표기도 허용한다.

- Google: [Type Names](https://google.github.io/styleguide/cppguide.html#Type_Names) · [Variable Names](https://google.github.io/styleguide/cppguide.html#Variable_Names) · [Function Names](https://google.github.io/styleguide/cppguide.html#Function_Names) · [Enumerator Names](https://google.github.io/styleguide/cppguide.html#Enumerator_Names) · [Constant Names](https://google.github.io/styleguide/cppguide.html#Constant_Names)
- 확인일: 일반 명명 2026-09-07, 상수 2026-10-06. Google 가이드는 고정 버전 없는 C++20 대상 웹 문서이며 프로젝트의 표준 버전을 고정하지 않는다.
- 채택일: 기본 규칙 2026-09-12, 상수 개정 2026-10-06, 네임스페이스 2026-10-16.

## 변경 기록

- 2026-10-16: 네임스페이스를 공통 채택하고 실제 루트·모듈 구분은 프로젝트별 결정으로 정리했다. `example` 예시를 사용하고 후속 요청으로 반복 설명·예시·근거를 압축했다. 기존 규칙 강도·예외·미결정 범위와 절 주소는 유지했다.
- 2026-10-06: 상수 명명을 선언 범위 기준으로 개정했다.
