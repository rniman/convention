# C++ attribute 사용

[C++ 목차](index.md)

상태: 초안 · 적용 범위: 직접 작성하는 C++의 표준 attribute와 컴파일러 확장 구분 · 작성일: 2026-10-09 · 개정일: 2026-10-16

attribute는 **동작·적용 대상을 확인해 필요한 곳에 사용**한다. 경고 억제·주석 대체로 일괄 취급하지 않는다.

필수·권장·선택은 **채택 시의 제안 강도**다. 기존 nodiscard·결과 무시 채택 기준은 [함수 규칙](functions.md#반환값-무시와-nodiscard)에 두며 다른 attribute의 채택·일괄 변경·C 규칙을 포함하지 않는다.

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

**권장:** 헤더 선언 또는 선언 없는 함수의 정의처럼 호출자가 보는 곳에 표시한다. 구현에만 표시해 호출부 진단을 기대하지 않는다.

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

타입 적용은 **값 반환**의 폐기 진단에 해당하며 포인터·참조 반환에는 자동 적용되지 않는다. 필요하면 함수에도 표시하고 다른 생산자·소비자의 계약을 확인한다.

표준은 진단을 권고하고 MSVC는 C4834를 사용한다. 경고의 오류 취급은 빌드 정책이며 저장·void 변환이 실제 검사를 보장하지 않는다. 예외 표기는 [의도적 결과 무시](functions.md#의도적인-반환값-무시)를 따른다.

## 의도와 계약을 정확하게 표시한다

**필수:** 선언 포맷 안에서 적용 대상을 분명히 한다. 함수용 attribute를 반환형·포인터 타입에 잘못 붙이지 않는다.

`[[maybe_unused]]`는 Debug assert 전용 값 등 의도적 미사용 선언에 둔다. 불필요한 변수·실패 결과 검사를 숨기지 않는다.

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

**필수:** 성능 사용 시 워크로드·옵션·컴파일러·측정을 기록한다. likely·unlikely를 정상·오류 분기에 기계적으로 붙이지 않는다. 효과는 구현·빌드에 따라 다르다.

**권장:** 지원하는 표준 attribute로 같은 목적을 표현할 수 있으면 우선 검토한다. `__declspec`·`__attribute__`·공급업체 네임스페이스의 attribute가 필요한 경우 대상 플랫폼·컴파일러·이유를 프로젝트에 기록한다. DLL import/export 같은 플랫폼 계약을 이름이 비슷한 표준 attribute로 대체하지 않는다.

**필수:** 미지 attribute 무시를 필수 동작의 근거로 삼지 않는다. 필요하면 `__has_cpp_attribute`·실제 빌드로 확인하고 진단용과 ABI·동작 필수 확장의 미지원을 구분한다. 호환 매크로·경고 설정은 도입하지 않는다.

## 관련 문서

- [함수 매개변수·반환 규칙](functions.md)
- [타입 변환과 범위 검사 (초안)](conversions.md)
- [주석 작성 규칙](comments.md)
- [소유권·수명 규칙](ownership.md)
- [RnimanEngine 확인 사례](../../projects/rniman-engine.md#반환값과-attribute-확인)

## 근거와 출처

[함수](functions.md)의 nodiscard 권장은 유지하며 나머지는 제안이다. [과거 자료](../../../ref/CodingConvention.md)의 오류·noexcept와 외부 명세는 비교·언어 근거이며 전체 채택 근거가 아니다.

확인일: **2026-10-09**. 갱신되는 작업 초안의 후속 기능을 표의 C++11~23에 확대하지 않는다. Microsoft 뷰 `msvc-170`은 프로젝트 도구 버전 고정이 아니다.

- [C++ 작업 초안 — dcl.attr.grammar](https://eel.is/c++draft/dcl.attr.grammar): attribute 문법·적용 대상과 알 수 없는 attribute 처리.
- [C++ 작업 초안 — cpp.cond](https://eel.is/c++draft/cpp.cond): `__has_cpp_attribute`의 지원 확인과 표준 attribute 버전 값. [WG21 P1301R4 — Wording](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1301r4.html#wording)은 이유 문자열의 추가 근거다.
- [dcl.attr.nodiscard](https://eel.is/c++draft/dcl.attr.nodiscard): 함수·타입 적용과 결과 폐기 진단, void 변환 예외.
- [dcl.attr.unused](https://eel.is/c++draft/dcl.attr.unused) · [dcl.attr.fallthrough](https://eel.is/c++draft/dcl.attr.fallthrough) · [dcl.attr.deprecated](https://eel.is/c++draft/dcl.attr.deprecated): 의도적인 미사용·case 연결·사용 중단 안내.
- [dcl.attr.noreturn](https://eel.is/c++draft/dcl.attr.noreturn) · [dcl.attr.assume](https://eel.is/c++draft/dcl.attr.assume): 정상 반환·거짓 전제에 따른 정의되지 않은 동작.
- [dcl.attr.likelihood](https://eel.is/c++draft/dcl.attr.likelihood) · [dcl.attr.nouniqueaddr](https://eel.is/c++draft/dcl.attr.nouniqueaddr): 실행 경로 힌트와 객체 배치 특성.
- [Microsoft — attribute·nodiscard](https://learn.microsoft.com/ko-kr/cpp/cpp/attributes?view=msvc-170#nodiscard) · [C4834](https://learn.microsoft.com/en-us/cpp/error-messages/compiler-warnings/c4834?view=msvc-170#remarks): MSVC 지원·진단과 표준/공급업체 확장 구분. C4834 문서의 `std::ignore` 우선 권고와 개인 채택 규칙의 차이는 함수 문서에 기록했다.

## 미결정 사항과 변경 기록

- 2026-10-16: 반복 설명·중복 예시·배경을 줄여 핵심 규칙과 예시 중심으로 정리했다. 규칙 강도·예외·버전과 채택·초안·미결정 상태는 유지했다.

- attribute별 제안의 공통 채택은 미결정이다. 기존 `[[nodiscard]]` 권장의 강도는 유지한다.
- C++ 최소 버전 상향, 이유 문자열의 필수 여부·언어, 확장 호환 매크로·컴파일러 진단 설정은 미결정이다. 보류·폐기로 확정한 항목은 없다.
- 2026-10-09: 표준 attribute의 목적·언어 버전·적용 조건·진단의 한계와 컴파일러 확장 구분을 정리한 초안을 추가했다. 함수 문서의 채택 규칙과 프로젝트 확인 기록으로 연결했다.
