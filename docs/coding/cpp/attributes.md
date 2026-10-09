# C++ attribute 사용

[C++ 목차](index.md)

상태: 초안 · 적용 범위: 직접 작성하는 C++의 표준 attribute와 컴파일러 확장 구분 · 작성일: 2026-10-09

attribute는 API의 사용 의도, 진단, 제어 흐름과 최적화에 필요한 정보를 표현한다. **각 attribute의 동작과 붙일 대상을 확인한 뒤 필요한 곳에 사용**하는 방식을 제안한다. 모든 attribute를 단순한 경고 억제나 주석의 대체로 취급하지 않는다.

이 문서의 필수·권장·선택은 **채택 시의 제안 강도**다. `[[nodiscard]]`의 기존 권장 기준과 의도적 결과 무시의 채택 규칙은 [함수 반환값 규칙](functions.md#반환값-무시와-nodiscard)에서 관리한다. 이 문서 추가가 다른 attribute의 채택이나 기존 코드 일괄 변경을 뜻하지 않는다. C 규칙은 별도로 정한다.

## 목적과 최소 언어 버전

`[[...]]` 문법은 C++11부터 사용하지만 모든 attribute가 C++11 기능인 것은 아니다. 아래 버전은 표준 도입 기준이며 실제 지원은 프로젝트 컴파일러와 표준 모드에서 확인한다.

| attribute | 최소 버전 | 사용 제안 | 의미·주의 |
| --- | --- | --- | --- |
| `[[nodiscard]]` | C++17 | 결과 무시가 잘못된 사용인 API — 기존 권장 | 미사용 결과에 진단 유도. 결과 처리 자체를 강제하지 않음 |
| `[[nodiscard("이유")]]` | C++20 | 무시하면 안 되는 이유가 이름만으로 불분명할 때 — 선택 | 호출자가 해야 할 일을 짧게 설명 |
| `[[maybe_unused]]` | C++17 | 조건부 빌드·디버그 전용 값·고정 시그니처의 의도적 미사용 — 선택 | 불필요한 코드를 남기거나 결과 검사를 우회할 목적은 피함 |
| `[[fallthrough]]` | C++17 | 의도적으로 다음 case 본문을 실행 — 권장 | 다음 case/default로 이어지는 위치의 null statement에 `[[fallthrough]];` 사용 |
| `[[deprecated("대체 API와 이유")]]` | C++14 | 기존 API를 유지하며 새 사용을 중단하도록 안내 — 권장 | 대체 방법·지원 범위는 API 문서에 기록. 삭제를 대신하지 않음 |
| `[[noreturn]]` | C++11 | 정상적으로 호출자에게 돌아오지 않는 함수 — 선택 | 종료·항상 예외를 던지는 함수 등. 정상 반환하면 정의되지 않은 동작 |
| `[[likely]]`·`[[unlikely]]` | C++20 | 근거가 있는 실행 경로 힌트 — 선택 | 성능 개선 보장이 아님. 실제 워크로드·빌드 조건으로 검증 |
| `[[no_unique_address]]` | C++20 | 객체 배치 최적화가 필요한 비정적 데이터 멤버 — 선택 | 배치·주소·ABI의 영향과 컴파일러 지원 확인. 크기 감소 보장 없음 |
| `[[assume(expression)]]` | C++23 | 조건이 항상 성립함을 입증한 제한된 최적화 — 선택 | 런타임 검사가 아님. 조건이 거짓이면 정의되지 않은 동작 |

`noexcept`, `override`, `final`, `constexpr`는 `[[...]]` attribute가 아니다. 이 문서에서 사용 범위를 함께 확정하지 않는다. 특히 `noexcept`를 단순한 성능 힌트로 해석하지 않는다.

## nodiscard의 적용 범위와 진단

판단 기준은 [함수 반환값 규칙](functions.md#반환값-무시와-nodiscard)을 따른다. **권장:** 호출자가 보는 선언에 표시한다. 헤더에 선언한 API라면 그 선언에 두고, 헤더 없이 정의만 있는 함수는 해당 정의에 둔다. 구현 파일에만 표시하여 호출부의 진단에 의존하지 않는다.

```cpp
[[nodiscard]] bool Initialize();

// C++20: 후속 동작의 전제를 설명한다.
[[nodiscard("Check completion before reusing resources")]] bool WaitForCompletion();
```

**선택:** 특정 함수의 결과만 중요하면 함수에 표시한다. 타입의 값 자체를 버리는 것이 일관되게 잘못된 사용이라면 구조체·클래스·열거형 선언에 적용할 수 있다.

```cpp
struct [[nodiscard]] OperationResult
{
	bool succeeded;
	int errorCode;
};

OperationResult PerformOperation();
```

타입에 붙이면 그 타입을 **값으로 반환**하는 함수 호출의 결과 폐기에도 진단이 권고된다. 그 타입의 포인터·참조를 반환하는 함수까지 자동으로 적용되지 않는다. 필요한 경우 해당 함수에도 표시한다. 타입에 적용할 때는 다른 생산자와 소비자에서도 같은 계약이 성립하는지 확인한다.

MSVC는 무시한 결과에 C4834를 발생시킨다. 표준은 진단을 권고하며, 경고를 오류로 다룰지는 빌드 정책이다. 변수에 저장하거나 명시적으로 void 변환하는 것만으로 실제 결과 확인을 보장하지 않는다. 구체적인 호출부 예외와 표기 선택은 [의도적인 반환값 무시](functions.md#의도적인-반환값-무시)에 둔다.

## 의도와 계약을 정확하게 표시한다

**필수:** 적용 대상과 문법 위치가 맞는지 확인한다. 함수에 적용하려는 attribute를 반환형이나 포인터 타입에 붙이는 식으로 잘못 배치하지 않는다. 한 줄·여러 줄 배치는 기존 선언 포맷을 따르되 대상을 분명하게 한다.

`[[maybe_unused]]`는 사용하지 않을 수도 있는 선언에 붙인다. 예를 들어 Debug의 `assert`에서만 사용하는 값을 Release에서도 선언해야 할 때 사용할 수 있다. 불필요한 변수는 제거하고, 실패 결과를 저장한 뒤 이 attribute로 미사용 경고를 숨기지 않는다.

`[[fallthrough]]`는 `break`를 빠뜨린 실수를 의도적인 동작으로 바꾸지 않는다. 다음 case에서 수행할 동작이 실제로 필요한지 확인한다.

```cpp
enum class OutputMode
{
	Verbose,
	Normal
};

void WriteDetails();
void WriteSummary();

void WriteOutput(OutputMode mode)
{
	switch (mode)
	{
	case OutputMode::Verbose:
		WriteDetails();
		[[fallthrough]];
	case OutputMode::Normal:
		WriteSummary();
		break;
	}
}
```

`[[noreturn]]`는 반환형 `void`와 다르다. 조건에 따라 정상 반환하는 오류 보고 함수에는 붙이지 않는다. `[[assume]]`는 `assert`나 입력 검증을 대신하지 않으며 외부 입력의 유효성을 추정하는 데 사용하지 않는다.

## 성능 관련 attribute와 컴파일러 확장

**필수:** 성능을 근거로 선택한다면 워크로드·최적화 옵션·컴파일러·측정 결과를 기록한다. `[[likely]]`를 정상 경로마다, `[[unlikely]]`를 모든 오류 분기마다 기계적으로 추가하지 않는다. 힌트의 효과는 구현과 빌드 조건에 따라 달라진다.

**권장:** 지원하는 표준 attribute로 같은 목적을 표현할 수 있으면 우선 검토한다. `__declspec`·`__attribute__`·공급업체 네임스페이스의 attribute가 필요한 경우 대상 플랫폼·컴파일러·이유를 프로젝트에 기록한다. DLL import/export 같은 플랫폼 계약을 이름이 비슷한 표준 attribute로 대체하지 않는다.

**필수:** 알 수 없는 attribute가 무시될 수 있다는 사실을 필수 동작의 구현 근거로 삼지 않는다. 지원 여부는 필요한 경우 `__has_cpp_attribute`와 실제 빌드로 확인한다. 진단 표시용 attribute의 미지원과 ABI·동작에 필요한 확장의 미지원은 구분한다. 공통 호환 매크로·경고 억제 설정은 여기서 도입하지 않는다.

## 관련 문서

- [함수 매개변수·반환 규칙](functions.md)
- [타입 변환과 범위 검사 (초안)](conversions.md)
- [주석 작성 규칙](comments.md)
- [소유권·수명 규칙](ownership.md)
- [RnimanEngine 확인 사례](../../projects/rniman-engine.md#반환값과-attribute-확인)

## 근거와 출처

기존 [함수 규칙](functions.md)의 `[[nodiscard]]` 권장과 사용자 제시 판단 기준을 유지한다. [과거 개인 자료](../../../ref/CodingConvention.md)의 반환값·오류 처리와 `noexcept` 설명은 비교 근거이며 attribute 전체의 채택 근거는 아니다. 다른 attribute의 적용 강도·배치·성능 검증 기준은 이 저장소의 제안이다. 외부 명세는 언어 동작을 설명하며 개인 규칙을 자동 채택하지 않는다.

확인일: **2026-10-09**. C++11·14·17·20·23의 도입 범위를 구분했다. 아래 C++ 작업 초안은 계속 갱신되는 문서이므로 C++26 이후의 확장까지 이전 버전에 적용하지 않는다. Microsoft 문서는 Visual Studio 문서 뷰 `msvc-170`이며 프로젝트의 실제 도구 버전을 고정하지 않는다.

- [C++ 작업 초안 — dcl.attr.grammar](https://eel.is/c++draft/dcl.attr.grammar): attribute 문법·적용 대상과 알 수 없는 attribute 처리.
- [C++ 작업 초안 — cpp.cond](https://eel.is/c++draft/cpp.cond): `__has_cpp_attribute`의 지원 확인과 표준 attribute 버전 값. [WG21 P1301R4 — Wording](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1301r4.html#wording)은 이유 문자열의 추가 근거다.
- [dcl.attr.nodiscard](https://eel.is/c++draft/dcl.attr.nodiscard): 함수·타입 적용과 결과 폐기 진단, void 변환 예외.
- [dcl.attr.unused](https://eel.is/c++draft/dcl.attr.unused) · [dcl.attr.fallthrough](https://eel.is/c++draft/dcl.attr.fallthrough) · [dcl.attr.deprecated](https://eel.is/c++draft/dcl.attr.deprecated): 의도적인 미사용·case 연결·사용 중단 안내.
- [dcl.attr.noreturn](https://eel.is/c++draft/dcl.attr.noreturn) · [dcl.attr.assume](https://eel.is/c++draft/dcl.attr.assume): 정상 반환·거짓 전제에 따른 정의되지 않은 동작.
- [dcl.attr.likelihood](https://eel.is/c++draft/dcl.attr.likelihood) · [dcl.attr.nouniqueaddr](https://eel.is/c++draft/dcl.attr.nouniqueaddr): 실행 경로 힌트와 객체 배치 특성.
- [Microsoft — attribute·nodiscard](https://learn.microsoft.com/ko-kr/cpp/cpp/attributes?view=msvc-170#nodiscard) · [C4834](https://learn.microsoft.com/en-us/cpp/error-messages/compiler-warnings/c4834?view=msvc-170#remarks): MSVC 지원·진단과 표준/공급업체 확장 구분. C4834 문서의 `std::ignore` 우선 권고와 개인 채택 규칙의 차이는 함수 문서에 기록했다.

## 미결정 사항과 변경 기록

- attribute별 제안의 공통 채택은 미결정이다. 기존 `[[nodiscard]]` 권장의 강도는 유지한다.
- C++ 최소 버전 상향, 이유 문자열의 필수 여부·언어, 확장 호환 매크로·컴파일러 진단 설정은 미결정이다. 보류·폐기로 확정한 항목은 없다.
- 2026-10-09: 표준 attribute의 목적·언어 버전·적용 조건·진단의 한계와 컴파일러 확장 구분을 정리한 초안을 추가했다. 함수 문서의 채택 규칙과 프로젝트 확인 기록으로 연결했다.
