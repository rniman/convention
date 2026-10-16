# C++ 타입 변환과 범위 검사

[C++ 목차](index.md)

상태: 초안 · 적용 범위: 직접 작성하는 C++의 명시적 변환·숫자 범위 검사·산술의 안전 조건 · 작성일: 2026-10-06 · 개정일: 2026-10-16

목적별 캐스트와 값의 범위·정밀도·객체 수명을 함께 확인한다.

어떤 자료형과 별칭을 사용할지는 [자료형 선택과 별칭](type-selection.md), 초기화 표기와 컴파일 시 축소 변환 진단은 [초기화](initialization.md#축소-변환을-숨기지-않는다)를 따른다. 외부 데이터의 표현 계약은 [자료형 선택 문서](type-selection.md#외부-데이터와-공개-계약)에 둔다.

필수·권장·선택은 **채택 시의 제안 강도**이며 기존 초기화 규칙과 구분한다. C·언어 버전·오류 정책은 별도 결정한다. 캐스트는 C++11, `std::optional`은 C++17, `std::in_range`·`std::cmp_*`·`std::bit_cast`는 C++20 이상이다.

## 명시적 변환의 선택

**권장:** 변환 없는 설계·표준 변환을 먼저 검토하고 필요하면 목적별 캐스트를 쓴다. 새 코드의 `(T)value`·기본 타입 `T(value)`는 피한다. 객체 생성·변환 생성자·`(void)` 결과 무시는 별개다.

결과를 버려도 되는 조건과 void 캐스트 표기의 채택 규칙은 [함수 반환값 문서](functions.md#의도적인-반환값-무시)에서 관리한다.

| 표기 | 사용 목적 | 조건·제약 |
| --- | --- | --- |
| `static_cast<T>` | 의도적인 숫자 변환, 알려진 `void*`의 원래 객체 타입 복원, 계약이 확인된 변환 | 범위·정밀도·실제 객체 타입을 검사하지 않음 |
| `dynamic_cast<T>` | 다형적 객체의 실행 중 타입 확인이 필요한 downcast·cross-cast | RTTI 지원 확인. 검사 실패 시 포인터는 null, 참조는 `std::bad_cast`; 실패를 처리 |
| `const_cast<T>` | const 등 cv 한정자의 명시적 변경 | 기존 API 적응의 제한된 예외. 변경 가능성과 API의 쓰기 여부를 확인 |
| `reinterpret_cast<T>` | 외부 ABI·저수준 표현이 요구하는 포인터·정수 등의 변환 | 크기뿐 아니라 정렬·객체 수명·접근 타입·플랫폼 계약이 필요 |
| `std::bit_cast<T>` | 값의 비트 표현을 다른 값으로 복사 | C++20, `<bit>`. 동일 크기·trivially copyable 조건과 유효한 대상 표현 필요 |

**필수:** 오류 제거용 `static_cast`를 피한다. downcast의 실제 타입을 보장하지 않으므로 실행 중 검사가 필요하면 `dynamic_cast`·타입 구분을 사용한다. RTTI·계층 정책은 별도 결정한다.

**필수:** 원래 const인 객체를 수정하지 않는다. 쓰지 않는다고 보장된 기존 API 적응에만 근거를 남겨 const를 제거한다. 쓰기가 필요하면 수정 가능한 객체·복사본·인터페이스를 검토한다.

**필수:** `reinterpret_cast`는 객체를 생성하거나 수명을 시작하거나 바이트를 파싱하지 않는다. 파일 버퍼를 구조체 포인터로 바꿔 읽는 것, 잘못된 API 출력 포인터를 억지로 맞추는 것에 사용하지 않는다. 다른 타입으로 접근할 수 있는지, 정렬·버퍼 범위·실제 객체 수명이 유효한지 확인한다.

`void*`의 알려진 원래 타입 복원에는 `static_cast`를 사용할 수 있으나 수명·쓰기 범위는 별도 조건이다. 바이트 복사의 `std::memcpy`도 복사 가능성·표현·수명을 확인한다.

`std::bit_cast`는 숫자 변환·엔디언·파일 형식 해결책이 아니다. 포인터·패딩·유효하지 않은 표현을 포함한 임의 구조체 변환에 일괄 사용하지 않는다.

## 외부 API와의 변환

**필수:** API 출력 포인터·참조는 요구 타입으로 선언한다. 같은 크기만으로 다른 기본 타입의 포인터를 캐스팅하지 않으며 동일 타입 별칭이면 캐스트가 불필요하다. 값 변환과 메모리 접근 타입 변경은 구분한다.

동일 타입·전체 범위 보존 변환에 캐스트를 일괄 추가하지 않는다. 손실·정책을 드러낼 때 명시하며 타입보다 좁은 API·장치 제한도 검사한다.

외부 API 타입을 유지하는 구현 범위는 [자료형 선택 문서](type-selection.md#외부-api의-자료형을-유지하는-범위)에 둔다.

## 숫자 변환과 산술 범위를 확인한다

**필수:** 정수 축소, 부호 변경, 정수와 실수 사이의 변환에는 보존해야 할 범위·정밀도와 손실 허용 정책을 정한다. 전체 범위가 보존되지 않더라도 상수·이전 검증·API 계약으로 값의 범위가 증명되면 검사를 반복하지 않아도 된다. 증명 근거가 호출자 가정이라면 함수 계약에 남긴다. 파일·사용자 입력의 실패를 Debug에서만 동작하는 `assert`로 처리하지 않는다.

`sizeof`가 같다는 이유로 안전하다고 판단하지 않는다. 정수의 부호·값 범위가 다를 수 있고, 정수에서 실수로의 변환은 실수가 더 커도 정확한 값을 잃을 수 있다. `{}`의 컴파일 시 축소 변환 진단과 실행 중 검사, 산술 오버플로 검사는 [초기화 규칙](initialization.md#축소-변환을-숨기지-않는다)의 구분을 유지한다.

### 정수 범위와 부호

**권장:** C++20의 지원 정수 타입에는 `<utility>`의 `std::in_range<T>`와 `std::cmp_*`를 사용해 signed·unsigned 혼합 검사를 명확히 한다. 이 함수들은 실수·열거형·`bool`·`char`·`wchar_t` 등 문자 전용 타입의 일반 변환 검사기가 아니다. `std::in_range`는 대상 타입의 표현 범위만 확인하며 유효한 개수·GPU 제한 등은 별도다.

```cpp
#include <cstddef>
#include <cstdint>
#include <optional>
#include <utility>

std::optional<std::uint32_t> ToStoredCount(std::size_t count)
{
	if (!std::in_range<std::uint32_t>(count))
	{
		return std::nullopt;
	}

	return static_cast<std::uint32_t>(count);
}

bool IsValidIndex(int index, std::size_t count)
{
	return index >= 0 && std::cmp_less(index, count);
}
```

`optional`은 예시이며 공통 오류 반환형이 아니다. 호출자는 실패를 보고·처리한다. C++20 전에는 부호를 먼저 처리하고 양쪽을 표현할 수 있는 타입으로 비교한다. 대상 최대값을 원본 타입으로 무조건 캐스트하면 그 값부터 잘릴 수 있다.

### 계산하기 전에 오버플로를 검사한다

**필수:** 크기 곱셈·덧셈·정렬 계산은 연산 전에 범위를 확인한다. 결과를 큰 타입으로 캐스트해도 이미 발생한 오버플로를 복구하지 못한다. 더 넓은 타입에서 계산하려면 피연산자를 연산 전에 그 타입으로 옮기고 그 타입의 범위도 확인한다.

unsigned 결과의 wraparound도 크기 계산의 성공을 뜻하지 않는다.

```cpp
#include <cstddef>
#include <limits>
#include <optional>

std::optional<std::size_t> CalculateByteCount(std::size_t count, std::size_t stride)
{
	if (stride != 0 && count > std::numeric_limits<std::size_t>::max() / stride)
	{
		return std::nullopt;
	}

	return count * stride;
}
```

예제는 0바이트를 허용하며 API가 금지하면 추가 검사한다. 덧셈은 `offset <= max` 전제에서 `bytes > max - offset`을 먼저 검사한다. 타입 범위 외에도 실제 버퍼·메모리·API 제한을 확인한다.

### 실수와 정수

**필수:** 실수에서 정수로 옮길 때 NaN·무한대, 대상 범위, 소수부 처리 정책을 확인한다. `static_cast<int>(value)`는 소수부를 0 방향으로 버리며, 버린 결과가 대상 범위를 벗어나면 정의되지 않은 동작이다. 반올림·내림·절삭 중 필요한 정책을 먼저 적용하고 그 결과를 검사한다.

큰 정수 최대값을 `float`나 `double`로 바꿔 경계로 쓰면 경계 자체가 반올림될 수 있다. 특히 `int64_t`의 최대값을 `double`로 옮겨 단순히 `<=`로 비교하는 방법을 안전한 공통 검사로 쓰지 않는다. 변환 조합에 맞는 경계·정밀도 검증을 사용한다. `std::in_range`는 실수 검사에 사용할 수 없다.

정수에서 실수, `double`에서 `float`로 옮길 때도 유효 범위뿐 아니라 정밀도 손실을 확인한다. 좌표 계산에서 허용하는 근사와 ID·카운터의 정확한 보존을 같은 정책으로 처리하지 않는다. 불필요한 정수→실수→정수 왕복 변환을 피한다.

## 적용과 후속 검토

- 기존 코드에는 관련 변경 범위부터 적용한다. 공개 인터페이스 변경은 별도 작업으로 다룬다.
- 반복되는 범위 검사·변환 실패 보고는 실제 소비자가 생기면 공통화를 검토한다. 사용할 곳이 없는 범용 변환 라이브러리를 먼저 추가하지 않는다.
- 초안 채택 여부와 공통 변환 오류 반환 방식은 미결정이다. 도구 설정·RTTI·예외 정책은 이 문서에서 결정하지 않는다.
- 검증할 때는 0·최대 허용값·초과값·음수·곱셈 오버플로를 포함한다. 실수 변환은 경계·NaN·무한대·정밀도 손실을, 포인터 변환은 실제 객체·정렬·수명·쓰기 계약을 확인한다.

## 관련 문서

- [자료형 선택과 별칭 (초안)](type-selection.md)
- [초기화 규칙](initialization.md)
- [const 사용 규칙](const.md)
- [함수 매개변수·반환 규칙](functions.md)
- [소유권·수명 규칙](ownership.md)

## 근거와 출처

[과거 자료](../../../ref/DevRnimanConvention/CodingConvention.md)의 호출별 캐스트 대신 변환 필요성·값 범위·객체 계약을 먼저 검토한다. 원본은 보존하며 타입 선택은 [자료형 근거](type-selection.md#근거와-출처)를 참조한다.

확인일: **2026-10-06**. 아래는 언어·API 근거이며 개인 규칙의 자동 채택 근거가 아니다. 갱신되는 작업 초안의 후속 기능을 앞서 명시한 C++11·17·20에 확대하지 않는다.

- [C++ Core Guidelines ES.46·ES.48·ES.49 — 축소 변환·캐스트·목적별 표기](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-narrowing): 손실을 드러내는 원칙을 참고한다. GSL 도입이나 전체 가이드 채택을 요구하지 않는다. 확인한 문서 표기: 2026-06-14, 현대 C++20 중심.
- [C++ 작업 초안 utility.intcmp — 정수 비교·범위 검사](https://eel.is/c++draft/utility.intcmp): `std::cmp_*`·`std::in_range`의 정수 타입 범위를 확인한다.
- [C++ 작업 초안 expr.arith.conv — 산술 변환](https://eel.is/c++draft/expr.arith.conv) · [conv.integral — 정수 변환](https://eel.is/c++draft/conv.integral): 부호 혼합과 범위 손실을 구분한다.
- [C++ 작업 초안 conv.fpint — 실수·정수 변환](https://eel.is/c++draft/conv.fpint): 절삭과 표현 범위를 확인한다.
- [static_cast](https://eel.is/c++draft/expr.static.cast) · [dynamic_cast](https://eel.is/c++draft/expr.dynamic.cast) · [const_cast](https://eel.is/c++draft/expr.const.cast) · [reinterpret_cast](https://eel.is/c++draft/expr.reinterpret.cast): 각 변환의 보장과 제한을 구분한다.
- [C++ 작업 초안 basic.lval — 객체 접근 타입](https://eel.is/c++draft/basic.lval) · [bit.cast — 비트 표현 복사](https://eel.is/c++draft/bit.cast): 같은 크기만으로 임의의 객체 접근을 허용하지 않는다.

## 변경 기록

- 2026-10-16: 반복 설명·중복 예시·배경을 줄여 핵심 규칙과 예시 중심으로 정리했다. 규칙 강도·예외·버전과 채택·초안·미결정 상태는 유지했다.

- 2026-10-09: 의도적 결과 무시의 채택 규칙을 함수 문서로 연결했다. 이 문서의 초안 상태는 유지했다.
- 2026-10-06: 자료형 선택·변환 통합 초안에서 목적별 캐스트·API 출력 인자·정수 범위·산술 오버플로·실수 변환을 분리했다. 자료형 선택과 외부 데이터 계약은 별도 초안으로 연결하며 기존 초기화 규칙과 프로젝트 코드는 변경하지 않았다.
