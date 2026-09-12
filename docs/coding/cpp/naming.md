# C++ 명명 규칙

[C++ 목차](index.md) · 관련: [const 사용 규칙](const.md)

상태: 채택 · 적용 범위: 직접 작성하는 C++ 식별자 · 예제: C++11 이상

이름의 표기를 통일해 코드에서 대상과 역할을 쉽게 구별한다. 기존 컨벤션의 명명 스타일을 기본안으로 정리했다. 프로젝트의 C++ 표준 버전은 이 문서에서 결정하지 않는다.

## 기본 규칙

아래 표는 이 규칙을 적용하는 코드에서 지킬 필수 표기다. 매크로, 네임스페이스와 파일 이름은 이번 범위에 포함하지 않는다. 상수에 해당하면 아래의 상수 규칙을 일반 변수 규칙보다 우선 적용한다.

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
| `constexpr` 변수 | `UPPER_SNAKE_CASE` | `MAX_FRAME_COUNT` |
| 고정된 정책값을 선언한 `const` 상수 | `UPPER_SNAKE_CASE` | `DEFAULT_WIDTH` |

`PascalCase`는 모든 단어의 첫 글자를 대문자로, `camelCase`는 첫 단어만 소문자로 시작한다. `m`, `s`, `g`는 기존 스타일을 유지하면서 변수의 범위를 구별하기 위한 개인 규칙이다. 전역 변수의 표기를 정의하는 것이 전역 변수 사용을 권장한다는 뜻은 아니다.

## 상수 명명

기존 전역 `constexpr`의 대문자 표기를 유지하고, 다른 범위와 `const`의 이름을 다음과 같이 구분한다.

- **필수:** `constexpr` 변수는 범위에 관계없이 `UPPER_SNAKE_CASE`로 작성한다. 단어는 대문자로 쓰고 `_`로 구분한다.
- **필수:** `const`로 선언한 값이 호출이나 객체마다 달라지는 입력·계산 결과라면 일반 변수 규칙을 따른다. `const`가 붙었다는 이유만으로 대문자로 바꾸지 않는다.
- **필수:** `const`로 선언한 고정 정책값·기본값은 `UPPER_SNAKE_CASE`로 작성한다. 예: `const int DEFAULT_WIDTH = 1280;`. 여기서 고정값은 소스에서 정책으로 지정한 값이다. 실행 중 설정 파일이나 계산으로 정해지는 값은 이후 변경되지 않더라도 일반 변수 규칙을 따른다.
- **필수:** 대문자 상수에는 `m`, `s`, `g`, `k` 접두어를 중복해서 붙이지 않는다. 클래스·구조체의 `static constexpr`도 `MAX_FRAME_COUNT`로 작성한다.

이 절은 이미 선언한 상수의 이름을 정한다. `const`를 붙일지와 `constexpr`를 선택할지는 [const 사용 규칙](const.md)에서 판단한다.

| 선언 상황 | 표기 예시 |
| --- | --- |
| 전역·네임스페이스의 `constexpr` | `MAX_FRAME_COUNT` |
| 함수 내부의 `constexpr` | `RETRY_LIMIT` |
| 클래스·구조체의 `static constexpr` | `MAX_PLAYER_COUNT` |
| 클래스의 `static const` 고정 정책값 | `DEFAULT_WIDTH` |
| 실행 중 계산한 지역 `const` | `remainingCount` |
| 생성자 입력으로 정해지는 클래스의 비정적 `const` 멤버 | `mPlayerId` |
| 실행 중 정해지는 클래스의 `static const` 설정값 | `sWorkerCount` |

```cpp
constexpr int MAX_FRAME_COUNT = 3;

class FrameSettings
{
public:
	static constexpr int DEFAULT_FRAME_COUNT = 3;
	static const int MAX_FRAME_COUNT = 8;
};
```

예시는 명명을 설명하는 선언이다. C++11·14에서 정적 멤버 상수의 주소를 취하는 등 별도 정의가 필요한 사용 방식은 여기서 다루지 않는다.

`constexpr` 함수의 이름은 일반 함수 규칙을 따른다. 포인터·참조가 가리키는 대상을 `const`로 제한했다는 이유만으로 상수 이름을 사용하지 않는다. `enum class`의 열거자는 기존 `PascalCase`를 유지한다.

헤더 배치와 매크로 정책은 별도 주제로 다룬다. 외부 매크로와 이름이 충돌하면 소속 기능이 드러나는 더 구체적인 이름으로 바꾼다.

## 의미가 드러나는 이름

- **필수:** 일반 함수는 `Load`, `Create`, `Get` 등 동사로 시작해 수행하는 동작을 표현한다.
- **필수:** 상태를 질의하는 `bool` 함수는 의미에 맞는 `Is`, `Has`, `Can`, `Should` 등을 사용한다. 예: `IsAlive`, `HasTexture`, `CanMove`.
- **필수:** `enum class`의 열거자에는 타입 이름을 반복하지 않는다. `ResourceState::Ready`로 쓰고 `ResourceState::ResourceStateReady`로 쓰지 않는다.
- **권장:** 이름만으로 역할을 알 수 있도록 작성한다. 예를 들어 피해량은 `damageAmount`로 표현한다.

기존의 “bool 반환 함수” 규칙은 상태 질의 함수로 범위를 구체화했다. 성공 여부를 반환하는 동작 함수는 `LoadTexture`처럼 실제 동작을 이름으로 표현한다.

## 예시

```cpp
class Player
{
public:
	void ApplyDamage(int damageAmount)
	{
		mHealth -= damageAmount;
	}

	bool IsAlive() const
	{
		return mHealth > 0;
	}

private:
	int mHealth = 100;
};

enum class ResourceState
{
	Ready,
	Loading
};
```

아래 이름들은 문법 오류가 아니라 이 문서의 스타일 위반이다.

| 피할 표기 | 적용할 표기 | 이유 |
| --- | --- | --- |
| `class player` | `class Player` | 타입 표기 통일 |
| `int damage_amount` | `int damageAmount` | 지역 변수·매개변수 표기 통일 |
| `int health_` (클래스 멤버) | `int mHealth` | 개인 멤버 접두어 적용 |
| `bool Alive() const` | `bool IsAlive() const` | 상태 질의임을 명시 |

## 예외와 미결정 사항

- 생성자·소멸자·연산자는 C++에서 정하는 이름 형식을 따른다. 일반 함수의 동사 접두어 규칙을 적용하지 않는다.
- 외부 인터페이스를 재정의하거나 `begin`·`end`처럼 정해진 이름을 요구하는 인터페이스를 구현할 때는 해당 이름을 유지한다. 외부 라이브러리와 생성된 코드에도 이 규칙을 강제로 적용하지 않는다.
- 구조체의 정적 멤버 중 상수 규칙에 해당하지 않는 변수와 약어의 대소문자 표기는 후속 정리 대상이다.

## 근거와 출처

기존 [DevMiniEngine 컨벤션](../../../ref/CodingConvention.md)과 [정리본](../../../ref/DevRnimanConvention/CodingConvention.md)의 네이밍 규칙을 바탕으로 작성했다. 기존 변수 접두어와 열거자 표기를 유지하고, 매개변수·구조체 타입의 표기 및 함수 이름의 예외를 명시했다. 추가로 명시한 규칙을 포함하여 개인 기준으로 채택했다.

Google은 변수에 `snake_case`, 클래스 멤버에 후행 `_`를 사용한다. 이 문서는 기존 개인 스타일인 `camelCase`와 `m`·`s` 접두어를 유지한다. 또한 Google의 열거자 `k` 접두어를 도입하지 않는다. 이는 언어 표준의 요구사항이 아닌 스타일 선택이다.

상수는 기존 자료의 “전역 `constexpr`는 ALL_CAPS”를 유지하고 지역·정적 멤버 상수로 확장한 규칙이다. Google의 `k` + 혼합 대소문자 방식과 다르다. Google이 지역 상수에 일반 변수 표기도 허용하는 것과 달리, 이 문서는 지역 `constexpr`도 대문자로 통일한다. `const` 입력·계산 결과와 고정 정책값의 구분은 이 저장소의 선택이다.

- [Google C++ Style Guide — Type Names](https://google.github.io/styleguide/cppguide.html#Type_Names)
- [Google C++ Style Guide — Variable Names](https://google.github.io/styleguide/cppguide.html#Variable_Names)
- [Google C++ Style Guide — Function Names](https://google.github.io/styleguide/cppguide.html#Function_Names)
- [Google C++ Style Guide — Enumerator Names](https://google.github.io/styleguide/cppguide.html#Enumerator_Names)
- [Google C++ Style Guide — Constant Names](https://google.github.io/styleguide/cppguide.html#Constant_Names)

명명 출처 확인일: 2026-09-07. 상수 출처 확인일: 2026-09-08.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.
