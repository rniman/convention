# C++ 함수 매개변수·반환 규칙

[C++ 목차](index.md) · 관련: [const 사용 규칙](const.md), [소유권·수명 규칙](ownership.md), [주석 작성 규칙](comments.md)

상태: 채택 · 적용 범위: 일반 함수의 입력·입출력·결과 전달 · 예제: C++11 이상

호출부에서 어떤 데이터를 읽고, 무엇을 변경하고, 어떤 결과를 만드는지 드러나도록 인터페이스를 작성한다. 스마트 포인터 전달은 [확정된 소유권 규칙](ownership.md#전달할-때-소유-의도를-표현한다)을 우선한다.

## 기본 선택

| 목적 | 기본 방식 | 강도 |
| --- | --- | --- |
| 복사 비용이 작은 입력 | `T` 값 전달 | 권장 |
| 복사 비용이 큰 객체를 읽기만 함 | `const T&` | 권장 |
| 기존 객체를 읽고 수정 | `T&` | 권장 |
| 부재가 유효한 비소유 입력 | `const T*` 또는 `T*` | 권장 |
| 새 결과 하나 생성 | `T` 값 반환 | 권장 |
| 의미상 묶인 결과 여러 개 | 이름 있는 구조체 반환 | 권장 |
| 호출자 버퍼 재사용·외부 API | 계약을 명시한 출력 인자 허용 | 선택 |

## 입력과 입출력

`int`, `bool`, 열거형처럼 복사 비용이 작은 타입은 값으로 받는다. 문자열·컨테이너처럼 복사할 데이터가 많은 객체를 잠시 읽을 때는 `const T&`를 고려한다. 바이트 크기 하나로 모든 타입의 전달 방식을 결정하지 않는다.

```cpp
#include <string>

bool HasPrefix(
	const std::string& text,
	char prefix)
{
	return !text.empty() && text.front() == prefix;
}

void AddBonus(
	int& damage,
	int bonusDamage)
{
	damage += bonusDamage;
}
```

`T&`는 호출자의 기존 객체를 수정할 수 있다는 의미로 사용한다. 참조가 있다고 항상 출력 전용이라고 해석하지 않는다. 부재를 허용해야 할 때는 포인터와 null의 의미를 명시하며, 수명 조건은 [소유권·수명 규칙](ownership.md)을 따른다.

**필수:** 입력 참조를 함수 호출 이후까지 저장하려면 별도의 수명 계약이 있어야 한다. 문자열·컨테이너를 자체적으로 보관할 함수는 잠깐 읽는 함수와 구분한다. 복사·이동 가능한 값을 항상 보관한다면 값 전달 후 이동 저장을 기본안으로 사용할 수 있다.

```cpp
#include <string>
#include <utility>

class Player
{
public:
	void SetName(std::string name)
	{
		mName = std::move(name);
	}

private:
	std::string mName;
};
```

조건부 저장, 버퍼 재사용, 비용이 큰 타입은 실제 호출 패턴에 따라 별도로 검토한다. 단순 입력에 관성적으로 `T&&`를 사용하지 않는다. 전달 템플릿의 `T&&`·`std::forward`는 별도 주제로 둔다.

## 반환값으로 결과를 표현한다

새로 만든 결과는 값으로 반환한다. 큰 객체라는 이유만으로 출력 참조로 바꾸지 않는다. 반환 비용은 복사 생략·이동과 호출 패턴을 함께 고려한다.

```cpp
#include <vector>

std::vector<int> CreateScores(int count)
{
	std::vector<int> scores(count, 0);
	return scores;
}
```

이 예제는 `count >= 0`을 전제로 한다. 일반 지역 결과는 `return result;`로 반환하고 `return std::move(result);`를 기계적으로 추가하지 않는다. 값 반환 타입에 최상위 `const`를 붙이지 않는다. 참조로 반환하는 `const T&`와는 다른 규칙이다.

관련된 결과 여러 개는 필드 이름이 의미를 설명하는 구조체로 반환한다.

```cpp
struct Size
{
	int width;
	int height;
};

Size GetDefaultSize()
{
	return {1280, 720};
}
```

단순히 결과 개수가 둘이라는 이유로 항상 `std::pair`를 사용하지 않는다. 이미 표준 API가 정한 반환형이나 범용 템플릿은 예외로 둔다.

## 출력 인자를 허용하는 경우

외부 API의 지정된 시그니처, 호출자가 마련한 버퍼의 재사용, 측정으로 확인된 비용 절감이 필요한 경우 출력 인자를 허용한다. 새 객체 하나를 반환할 수 있는 일반 함수의 기본형으로 삼지는 않는다.

**필수:** 입력과 출력이 섞이면 무엇을 읽고 무엇을 쓰는지 설명한다. 실패 시 출력 유지·초기화·부분 변경 중 어떤 동작인지 명시하고 구현과 일치시킨다.

```cpp
#include <string>

/// @brief 경로에 해당하는 이름을 읽어 output에 기록한다.
/// @return 성공 시 true. 실패 시 false이며 output은 변경하지 않는다.
bool TryReadName(
	const std::string& path,
	std::string& output);
```

위 예제는 출력 계약의 선언 예시다. 실제 파일 읽기 구현은 포함하지 않는다. 출력 인자는 입력 인자 뒤에 두는 것을 권장하되 외부 API의 순서는 유지한다.

## 결과 없음과 실패

- 반환할 데이터가 없는 명령은 `void`, 참·거짓 질의나 성공 여부만 필요한 연산은 `bool`을 사용할 수 있다.
- 데이터가 없을 수 있는 결과에는 C++17 이상에서 `std::optional<T>`를 고려한다. 오류 원인까지 담는 형식은 아니다.
- 오류 원인이 필요한 연산은 결과 타입·오류 코드·예외 정책을 별도로 정한다. `std::expected`를 사용한다면 C++23 및 도구 지원을 확인한다.
- `0`, `-1`, 빈 문자열을 보편적인 실패값으로 삼지 않는다. 정상 결과와 구분되는지 먼저 확인한다.
- 결과 무시가 잘못된 사용이 되는 API에는 C++17 이상에서 `[[nodiscard]]`를 권장한다. 모든 Getter에 일괄 적용하지 않는다.

이 절은 반환형 선택의 경계만 다룬다. 프로젝트 전체의 예외 허용 범위나 오류 처리 방식은 아직 확정하지 않는다.

## 관련 규칙과 예외

- 함수명은 [명명 규칙](naming.md), 여러 줄 매개변수와 닫는 괄호 배치는 [포맷 규칙](formatting.md)을 따른다.
- 매개변수의 `const` 위치와 지역 변수 적용 기준은 [const 사용 규칙](const.md)에 둔다.
- 포인터·참조·뷰 반환의 유효 기간과 비동기 저장은 [소유권·수명 규칙](ownership.md)에 둔다.
- 매개변수가 많거나 비슷한 `bool`·정수 인자가 반복되면 이름 있는 옵션 타입이나 열거형을 검토한다. 단순히 인자 개수를 줄이기 위한 무관한 값의 묶음은 피한다.
- 오버라이드·콜백·C ABI 등 외부에서 지정한 함수 형태는 해당 계약을 우선한다.

## 근거와 출처

[기존 자료](../../../ref/CodingConvention.md)의 읽기 전용 입력·반환값 원칙과 기존 COM 출력 인자 사례를 참고했다. 읽기 전용 입력을 무조건 `const T&`로 받는 해석은 피하고 비용과 의도로 구분한다. 외부 API의 출력 방식은 일반 함수 전체의 기본값으로 확대하지 않는다.

C++ Core Guidelines의 입력·입출력 구분과 값·구조체 반환 권고를 참고했다. 값 전달 후 저장, 출력 인자 배치와 실패 계약의 구체화는 이 저장소의 선택이다.

- [F.16 — 입력 매개변수](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-in)
- [F.17 — 입출력 매개변수](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-inout)
- [F.20 — 반환값 우선](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-out)
- [F.21 — 여러 결과의 구조체 반환](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-out-multi)

출처 확인일: 2026-09-12.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.
