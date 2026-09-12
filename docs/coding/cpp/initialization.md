# C++ 초기화 규칙

[C++ 목차](index.md) · 관련: [const 사용 규칙](const.md), [코드 포맷 규칙](formatting.md)

상태: 채택 · 적용 범위: 지역 변수와 비정적 멤버의 초기화 · 예제: C++11 이상

초기값과 생성 의도가 선언에서 드러나도록 작성한다. 기존 자료의 `=` 기본 스타일을 유지하되, 생성자 선택과 값 손실에 영향을 주는 경우는 별도로 구분한다.

이 문서는 초기값을 지정하는 방법을 다룬다. 읽기 전용 여부는 [const 사용 규칙](const.md), 괄호의 줄 배치는 [코드 포맷 규칙](formatting.md)을 따른다.

## 핵심 규칙

| 상황 | 기본 표기 | 강도 |
| --- | --- | --- |
| 타입이 일치하는 단일 값 | `int count = 0;` | 권장 |
| 함수 결과의 타입을 그대로 사용 | `auto result = Calculate();` | 권장 |
| 컨테이너의 원소 목록 | `std::vector<int> values = {1, 2, 3};` | 권장 |
| 개수 생성자가 있는 컨테이너의 크기·반복값 지정 | `std::vector<int> values(3, 10);` | 필수 |
| 집합 초기화·빈 값 초기화 | `Position position{0.0f, 0.0f};`, `Position origin{};` | 권장 |
| 공통 멤버 기본값 | `int mFrameIndex = 0;` | 권장 |
| 생성자 인자에 따라 달라지는 멤버 | 생성자 초기화 목록 | 필수 |

## 선언할 때 유효한 상태를 만든다

**필수:** 지역 스칼라와 포인터를 미초기화 상태로 두지 않는다. 실제 초기값을 구할 수 있는 위치에서 선언하고, 의미 없는 임시값을 넣은 뒤 곧바로 덮어쓰는 패턴을 피한다.

```cpp
int count = 0;
bool isReady = false;
int* currentValue = nullptr;
```

기본 생성자가 유효한 상태를 만드는 타입은 그 생성자를 사용할 수 있다. 모든 객체를 숫자 `0`이나 원시 메모리 초기화로 처리한다는 뜻은 아니다.

## 원소 목록과 생성자 인자를 구분한다

```cpp
#include <vector>

std::vector<int> values = {3, 10}; // 원소 3과 10: 총 2개
std::vector<int> repeatedValues(3, 10); // 값 10인 원소: 총 3개
std::vector<int> zeroValues(3); // 값 0인 원소: 총 3개
```

**필수:** `()`와 `{}`를 단순한 포맷 변경으로 치환하지 않는다. 원소 목록을 받는 생성자가 있는 타입은 의미가 달라질 수 있다.

**권장:** 집합의 멤버를 순서대로 지정하거나 `explicit` 생성자를 직접 호출할 때는 `T value{args};`를 사용한다. 단, 위와 같이 크기 등을 지정하는 생성자가 목적이면 `()`를 사용한다. `explicit`이라는 이유만으로 중괄호가 필수인 것은 아니다.

```cpp
struct Position
{
	float x;
	float y;
};

Position position{1.0f, 2.0f};
Position origin{}; // 이 구조체의 두 float 멤버는 0으로 초기화된다.
```

## 축소 변환을 숨기지 않는다

**필수:** 초기화 과정에서 값의 범위나 정밀도를 잃는 암시적 변환을 피한다. 원본 타입을 유지하거나, 변환 대상 타입에 값이 들어가는지 확인한다. 축소 변환을 금지하려는 초기화에는 `{}`를 사용하여 언어 규칙에 따른 컴파일 시점 진단을 받는다.

`{}`는 실행 중 값의 범위를 검사하지 않는다. 실제 값이 대상 타입에 들어가더라도 언어에서 축소 변환으로 분류하면 거부하며, 초기화 표현식 안의 산술 오버플로도 방지하지 않는다.

```cpp
double distance = 3.5;
double copiedDistance = distance; // 타입 유지

// 아래는 피해야 할 예시이며 주석을 해제하면 마지막 줄은 컴파일 오류다.
// int truncatedDistance = distance; // 문법상 가능하지만 소수부 손실
// int rejectedDistance{distance}; // 축소 변환으로 컴파일 오류
```

의도적인 변환도 범위와 반올림·절삭 정책을 먼저 결정한다. 오류를 없애기 위한 캐스트만 추가하지 않는다. 컴파일러 경고는 보조 수단이며 중괄호 초기화의 축소 변환 진단을 대체하지 않는다.

## 멤버의 기본값과 생성자 입력을 구분한다

공통 기본값은 멤버 선언에 작성한다. 생성자 입력이 필요한 멤버는 초기화 목록에 작성하고, 목록 순서는 멤버 선언 순서에 맞춘다.

```cpp
class Player
{
public:
	explicit Player(int playerId)
		: mPlayerId{playerId}
	{
	}

private:
	int mPlayerId;
	int mHealth = 100;
};
```

초기화를 대신하려고 생성자 본문에서 멤버에 대입하지 않는다. 유효하게 초기화한 뒤 생성 과정에 필요한 상태를 갱신하는 것까지 금지하지는 않는다. 생성자를 추가할 때도 모든 멤버가 유효하게 초기화되는지 확인한다. 실제 초기화 순서는 초기화 목록의 나열 순서가 아니라 멤버 선언 순서다.

## 적용 범위와 예외

- `auto`로 단일 결과를 받을 때는 `auto value = expression;`을 사용한다. `auto value = {1};`은 정수 하나가 아닌 초기화 목록을 추론하므로 대체 표기로 사용하지 않는다.
- 외부 API의 출력 인자를 새로 선언할 때도 먼저 유효한 기본 상태를 만들고, 성공 여부를 확인한 뒤 결과를 사용한다. 이미 유효한 객체나 버퍼를 호출마다 초기값으로 되돌리라는 뜻은 아니다.
- 성능 때문에 버퍼 초기화를 생략하려면 측정 근거와 모든 읽기 전 쓰기가 보장되는 경로를 프로젝트별 예외로 문서화한다.
- 동적 자원 생성, 전역 초기화 순서, 상수의 헤더 정의 방식은 별도 주제로 다룬다.

## 근거와 출처

기존 [DevMiniEngine 컨벤션](../../../ref/CodingConvention.md)의 초기화 항목에서 `=` 기본 표기와 원소 목록 표기를 유지했다. 기존의 “explicit 생성자 예외”는 괄호 선택의 의미를 기준으로 구체화했다. “경고로 narrowing 방지”는 보장되지 않으므로 이 문서에서는 변환 검토와 중괄호 진단을 함께 사용한다.

C++ Core Guidelines의 초기화·멤버 기본값 원칙을 참고했다. 해당 가이드의 `{}` 우선 권고와 달리, 이 문서는 타입이 일치하는 단일 값에 기존 `=` 스타일을 유지한다. 이는 개인 스타일 선택이며 C++ 언어의 의무가 아니다.

- [ES.20 — 객체 초기화](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-always)
- [ES.23 — 중괄호 초기화와 컨테이너 예외](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-list)
- [C.48 — 멤버 기본 초기화](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-in-class-initializer)

출처 확인일: 2026-09-08.

기술 설명 보완 확인일: 2026-09-12. C++ 작업 초안의 [목록 초기화](https://eel.is/c++draft/dcl.init.list)와 [기반 클래스·멤버 초기화](https://eel.is/c++draft/class.base.init)를 확인했다.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.
