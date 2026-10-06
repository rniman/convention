# C++ 명명 규칙

[C++ 목차](index.md)

상태: 채택 · 적용 범위: 직접 작성하는 C++ 식별자 · 예제: C++11 이상

이름의 표기를 통일해 대상과 역할을 구별한다.

## 기본 규칙

아래 표기는 **필수**다. 상수는 [상수 명명](#상수-명명)을 우선 적용한다.

| 대상 | 표기 | 예시 |
| --- | --- | --- |
| 클래스·구조체·열거형 타입 | `PascalCase` | `Player`, `SpawnPoint`, `ResourceState` |
| 일반 함수·멤버 함수 | `PascalCase` | `LoadTexture`, `GetHealth` |
| 지역 변수·매개변수 | `camelCase` | `frameIndex`, `damageAmount` |
| 클래스의 비정적 멤버 변수 | `m` + `PascalCase` | `mHealth` |
| 클래스의 정적 멤버 변수 | `s` + `PascalCase` | `sPlayerCount` |
| 전역 변수 | `g` + `PascalCase` | `gFrameCount` |
| 구조체의 비정적 데이터 멤버 | `camelCase` | `positionX` |
| `enum class`의 열거자 | `PascalCase` | `ResourceState::Ready` |

`PascalCase`는 각 단어의 첫 글자를 대문자로, `camelCase`는 첫 단어만 소문자로 시작한다. `m`·`s`·`g`는 범위를 구별하는 개인 규칙이다.

## 상수 명명

`const`·`constexpr`는 구분하지 않고 **선언 범위**를 기준으로 정한다. 아래 표기는 **필수**다. 초기값이 고정 정책값인지 실행 중 입력·계산 결과인지는 명명에 영향을 주지 않는다.

| 선언 범위 | 표기 | 예시 |
| --- | --- | --- |
| 함수·블록 내부 — 지역 `static` 포함 | `camelCase` | `retryLimit`, `remainingCount` |
| 전역·네임스페이스 상수, 클래스·구조체의 정적 상수 | `UPPER_SNAKE_CASE` | `MAX_FRAME_COUNT`, `WORKER_COUNT` |
| 비정적 `const` 데이터 멤버 | 기본 멤버 규칙 | 클래스 `mPlayerId`, 구조체 `playerId` |

- **필수:** 대문자 상수에는 `m`·`s`·`g`·`k` 접두어를 붙이지 않는다.
- 상수는 변수 자체가 `const`인 경우(`constexpr` 포함)를 뜻한다. `T* const`는 이 표를 따르고, 대상만 읽기 전용인 `const T*`와 `const T&` 참조는 기본 변수 규칙을 따른다.
- `const`·`constexpr`의 선택은 [const 사용 규칙](const.md)을 따른다. `constexpr` 함수에는 기본 함수 규칙을 적용한다.

```cpp
constexpr int MAX_FRAME_COUNT = 3;

int GetRemainingCount(int frameCount)
{
	constexpr int retryLimit = 3;
	const int remainingCount = frameCount - retryLimit;
	static constexpr int minimumCount = 0;
	return remainingCount > minimumCount ? remainingCount : minimumCount;
}
```

지역 상수는 주변 변수와 표기를 맞추고, 넓은 범위의 상수는 대문자로 구별한다. 선언 키워드를 바꿔도 같은 범위에서는 이름을 유지한다.

## 의미가 드러나는 이름

- **필수:** 일반 함수는 `Load`·`Create`·`Get` 등 동사로 시작해 동작을 표현한다. 성공 여부를 반환하는 동작 함수도 `LoadTexture`처럼 작성한다.
- **필수:** 상태를 질의하는 `bool` 함수는 `Is`·`Has`·`Can`·`Should` 등을 사용한다. 예: `IsAlive`, `HasTexture`, `CanMove`.
- **필수:** `enum class`의 열거자에는 타입 이름을 반복하지 않는다. `ResourceState::Ready`로 작성한다.
- **권장:** 이름만으로 역할을 알 수 있도록 작성한다. 예: 피해량 `damageAmount`.

## 예외와 미결정 사항

- 생성자·소멸자·연산자는 언어에서 정한 이름을 따른다. 일반 함수의 동사 접두어 규칙을 적용하지 않는다.
- 외부 인터페이스 재정의와 `begin`·`end` 등 정해진 이름을 요구하는 인터페이스는 해당 이름을 유지한다. 외부 라이브러리·생성 코드에는 이 규칙을 강제하지 않는다.
- 외부 매크로와 충돌하면 소속 기능이 드러나는 더 구체적인 이름을 사용한다.
- **미결정:** 매크로·네임스페이스·파일 이름, 상수가 아닌 구조체 정적 멤버, 약어의 대소문자 표기. 헤더 배치·매크로 정책은 별도 주제다.

## 관련 문서

- [const 사용 규칙](const.md)

## 근거와 출처

기존 [DevMiniEngine 컨벤션](../../../ref/CodingConvention.md)과 [정리본](../../../ref/DevRnimanConvention/CodingConvention.md)의 명명 스타일을 유지했다. 기존 전역 `constexpr`의 ALL_CAPS를 바탕으로, 상수의 범위 기준은 2026-10-06 사용자 선택으로 개정했다.

Google은 일반 변수에 `snake_case`, 클래스 멤버에 후행 `_`, 프로그램 실행 동안 값이 고정되는 상수와 열거자에 `k` + 혼합 대소문자를 사용한다. 정적 저장 기간을 갖는 상수에는 상수 표기를 요구하고 자동 지역 상수에는 일반 변수 표기도 허용한다. 이 문서는 기존 개인 스타일을 유지하며, 지역 `static`도 선언 범위에 따라 표기한다. 언어 표준의 요구사항이 아닌 개인 스타일 선택이다.

- Google C++ Style Guide: [Type Names](https://google.github.io/styleguide/cppguide.html#Type_Names) · [Variable Names](https://google.github.io/styleguide/cppguide.html#Variable_Names) · [Function Names](https://google.github.io/styleguide/cppguide.html#Function_Names) · [Enumerator Names](https://google.github.io/styleguide/cppguide.html#Enumerator_Names) · [Constant Names](https://google.github.io/styleguide/cppguide.html#Constant_Names)

명명 출처 확인일: 2026-09-07 · 상수 출처 확인일: 2026-10-06. Google 가이드는 고정 버전 번호 없는 웹 문서이며 확인 시점의 대상 언어 버전은 C++20이다.

채택일: 2026-09-12. 미결정 사항은 채택 범위에서 제외한다.

## 변경 기록

- 2026-10-06: 사용자 선택으로 상수 명명을 선언 범위 기준으로 개정하고 관련 예제·출처 비교를 갱신했다. 이후 요청에 따라 상수 정의를 한 표로 모으고 반복 설명·예제·위반 표를 줄여 핵심 규칙·예외·근거 중심으로 정리했다. 채택된 규칙과 미결정 범위는 유지했다.
