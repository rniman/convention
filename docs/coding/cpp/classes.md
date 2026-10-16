# C++ 클래스·구조체 규칙

[C++ 목차](index.md)

상태: 채택(미결정 정책 제외) · 채택일: 2026-10-09 · 적용 범위: C++ 사용자 정의 타입의 설계·생성·복사·이동·기본 상속 · 예제: C++11 이상 · 개정일: 2026-10-16

타입 설계와 생성·복사·이동·상속을 다룬다. **필수·권장·선택을 구분**하며 [미결정 정책](#미결정-정책)은 채택에서 제외한다. C 구조체는 별도 기준이다.

## 기존 규칙과의 경계

상세 정의는 다음 문서를 따르며 여기서는 타입 설계만 다룬다.

| 내용 | 상세 기준 |
| --- | --- |
| 타입·클래스 멤버·구조체 필드 이름 | [명명](naming.md) |
| 접근 지정자 들여쓰기·괄호·빈 줄 | [포맷](formatting.md) |
| `=`·`()`·`{}` 선택, 멤버 기본값·초기화 목록 | [초기화](initialization.md#멤버의-기본값과-생성자-입력을-구분한다) |
| 조회 함수의 후행 `const`, const 멤버의 주의점 | [const](const.md) |
| RAII·스마트 포인터·대여와 수명 경계 | [소유권·수명](ownership.md) |
| 매개변수·반환형, 구조체·pair·tuple 선택, nodiscard | [함수](functions.md) |
| 공개 선언·include·전방 선언 | [헤더·include](headers.md) |

## class와 struct의 선택

C++에서 둘은 같은 클래스 기능을 사용할 수 있다. 차이는 **멤버 접근과 기반 클래스 상속 접근의 기본값**이다.

| 선언 | 멤버의 기본 접근 | 기반 클래스의 기본 상속 접근 |
| --- | --- | --- |
| `struct` | `public` | `public` |
| `class` | `private` | `private` |

`struct`도 생성·소멸·함수·상속·가상 함수를 지원한다. 집합체·단순 복사·C 호환 배치를 보장하지 않으므로 API·파일·GPU 계약과 언어 버전을 확인한다.

**권장:** 필드를 직접 수정해도 의미가 유지되는 데이터는 `struct`, 유효 조건·자원·상태를 API로 보호하면 `class`를 쓴다. 크기·함수 유무로 선택하지 않는다.

```cpp
struct Position2D
{
	float x = 0.0f;
	float y = 0.0f;

	float LengthSquared() const
	{
		return x * x + y * y;
	}
};
```

비공개 구현·상태 검증이 필요하면 class 전환을 검토한다. 외부·생성·ABI 표기는 예외로 기록하며 복합 반환은 [함수 규칙](functions.md#구조체와-pairtuple의-선택)을 따른다.

## 책임과 공개 인터페이스

**권장:** 타입의 상태·책임·불변식을 정하고 공개 연산이 보존하게 한다. 함께 바뀌는 포인터·길이 등을 독립 공개하기 전에 호출자 책임을 검토한다.

- **권장:** 클래스의 구현 데이터는 `private`에 두고, 필요한 연산만 공개한다. 모든 필드에 Getter·Setter를 기계적으로 추가하지 않는다. 검증·동기화가 필요한 변경은 그 목적을 드러내는 연산으로 제공한다.
- **권장:** 파생 클래스에 필요한 확장 지점은 `protected` 함수로 제공한다. `protected` 데이터는 여러 파생 클래스가 상태 조건을 직접 관리하게 하므로 공개 범위를 줄이는 방향으로 검토한다.
- **선택:** 밀접하게 협력하는 타입이나 테스트 어댑터에 `friend`를 사용할 수 있다. 필요한 접근과 수명 조건을 설명하고 일반 호출자의 API를 대신하는 관행으로 확대하지 않는다.

멤버를 반환하는 참조·포인터의 변경 가능성과 유효 기간은 기존 [const](const.md#매개변수와-멤버-함수)·[소유권](ownership.md#빌려-쓰는-참조와-포인터)·[API 주석](comments.md) 규칙을 따른다.

## 선언 구성과 멤버 순서

**권장:** `public → protected → private` 순서로 필요한 구역만 명시한다. 공개 데이터 구조체의 `public:`은 생략 가능하다. 구역은 모으되 가독성·도구상 필요하면 반복한다. 아래 순서보다 수명 의존성을 우선한다.

| 구역 | 권장 구성 순서 |
| --- | --- |
| `public` | 공개 중첩 타입·별칭 → 생성자·소멸자·복사·이동 → 필요한 정적 생성 함수 → 주요 API → 관련 조회·변경 함수·연산자 |
| `protected` | 파생 클래스에 제공하는 타입·확장 함수 |
| `private` | 내부 타입·보조 함수 → 멤버 데이터 |

알파벳순보다 호출 흐름·기능 묶음을 우선하고 형식용 API를 추가하지 않는다. 구조체는 데이터 의미 순서 뒤에 관련 함수를 묶는다.

**필수:** 선언 순서에 따른 초기화·역순 파괴와 의존성을 확인한다. **권장:** 수명을 만족시킨 뒤 역할별로 묶는다. 크기순 정렬은 기본이 아니며 배치 변경 시 ABI·외부 계약·측정을 확인한다.

## 생성자와 explicit

**필수:** 생성 후 유효 상태·허용 연산을 정의한다. 유효 상태를 못 만들면 기본 생성을 생략할 수 있다. 표기는 [멤버 초기화](initialization.md#멤버의-기본값과-생성자-입력을-구분한다)를 따른다.

**권장:** 기본 인자 포함 한 인자로 호출 가능한 생성자는 `explicit`으로 둔다. 의도적 암시 변환 계약은 예외이며 복사·이동 생성자에 일괄 적용하지 않는다.

```cpp
class PlayerId
{
public:
	explicit PlayerId(unsigned value)
		: mValue{value}
	{
	}

	unsigned GetValue() const
	{
		return mValue;
	}

private:
	unsigned mValue;
};

PlayerId playerId{7u};
// PlayerId implicitId = 7u; // explicit 생성자는 이 암시적 변환을 허용하지 않는다.
```

`explicit`은 입력 검증이나 축소 변환 검사를 대신하지 않는다. **권장:** 변환 연산자를 제공할 때도 암시적 변환의 필요성을 검토한다. `explicit operator bool()`은 조건식에서 사용하는 대표적인 선택이며 임의의 숫자·포인터 변환을 일괄 제공하지 않는다. 조건부 `explicit(...)`은 C++20 기능으로, 제네릭 변환 정책이 필요할 때 별도로 검토한다.

## 특수 멤버 함수와 default·delete

### 기본은 Rule of Zero

**권장:** 값 타입과 RAII 멤버로 필요한 수명 관리를 표현할 수 있으면 복사 생성자·복사 대입·이동 생성자·이동 대입·소멸자를 직접 선언하지 않는다. 이를 Rule of Zero라고 한다. 일반 생성자나 일반 멤버 함수를 작성하지 말라는 뜻은 아니다.

### 정책이 필요할 때 명시한다

| 선택 | 사용 기준 |
| --- | --- |
| 선언 생략 | 멤버가 제공하는 기본 동작이 타입의 의미에 맞으면 우선 — 권장 |
| `= default` | 기본 동작을 명시적으로 제공해야 할 때 — 권장 |
| `= delete` | 호출을 허용하지 않는 연산의 의도를 공개 선언에서 표현 — 권장 |
| 직접 구현 | 자원 이전·외부 등록 갱신 등 기본 동작으로 해결되지 않는 처리 — 선택 |

**필수:** 복사·이동·소멸 중 하나에 개입하면 다섯 연산의 생성·의미를 함께 검토한다(Rule of Five). 필요한 선언만 작성하며 모든 타입에 다섯 선언을 강제하지 않는다.

사용자 선언 소멸자·복사 연산(`default`·`delete` 포함)은 암시적 이동을 막을 수 있다. 이동이 없어도 우측값을 복사할 수 있으므로 선언 부재를 정책으로 간주하지 않는다.

**권장:** 값으로 복제하는 타입은 복사를 허용하고, 자원 소유자나 객체 주소에 의존하는 콜백 대상은 복사·이동 각각의 타당성을 검토한다. 다음은 주소가 유지되어야 하는 타입의 정책 선언 예시다.

```cpp
class CallbackTarget
{
public:
	CallbackTarget() = default;

	CallbackTarget(const CallbackTarget&) = delete;
	CallbackTarget& operator=(const CallbackTarget&) = delete;
	CallbackTarget(CallbackTarget&&) = delete;
	CallbackTarget& operator=(CallbackTarget&&) = delete;
};
```

**필수:** `= default`가 해당 연산의 사용 가능성이나 올바른 자원 이전을 보장한다고 가정하지 않는다. 멤버 조건 때문에 기본 연산이 삭제될 수 있다. 소유하는 원시 핸들의 기본 이동은 값을 복사하여 중복 정리를 만들 수 있으므로, RAII 래퍼를 사용하거나 이전·원본 무효화를 직접 구현한다.

이동을 제공한다면 이동 후 원본의 파괴·재대입과 추가 허용 연산을 정의한다. `const` 멤버의 영향은 [const 주의사항](const.md#예외와-주의사항)을 함께 확인한다. 참조 멤버가 있으면 기본 복사·이동 대입이 삭제되므로 필요한 대입 정책을 이 타입에서 검토한다.

## 상속과 가상 함수

### 상속이 필요한 관계인지 확인한다

**권장:** 기능을 보유·조합하는 관계에는 멤버 구성을 먼저 검토한다. 기반 타입을 요구하는 코드에서 파생 타입을 같은 계약으로 사용할 수 있거나 런타임 다형성이 필요한 경우 공개 상속을 사용한다. 코드 재사용만을 위해 가상 계층을 만들지 않는다.

**권장:** `class Derived : public Base`처럼 상속 접근을 명시한다.

### virtual·override·final의 목적을 구분한다

`override`·`final`은 C++11의 특별한 의미를 갖는 식별자이며 `[[...]]` attribute가 아니다.

| 상황 | 표기·강도 |
| --- | --- |
| 기반 클래스에서 새 가상 함수를 선언 | `virtual` — 필수 |
| 기존 가상 함수를 재정의 | `override`로 재정의 의도를 검사 — 권장. 함수 `final`로 표시한 경우는 아래 기준 적용 |
| 특정 가상 함수의 추가 재정의를 차단하려는 경우 | 함수 뒤 `final` — 권장 |
| 타입의 추가 상속을 차단하려는 경우 | 클래스 이름 뒤 `final` — 권장 |

**권장:** 재정의는 `override`, 추가 재정의 금지는 `final`을 쓰고 `virtual`을 반복하지 않는다. 하나가 기본이며 `override final` 병기도 허용한다. 함수 final은 가상 함수에 사용한다. override는 이름·인자·const 불일치를 검사하며 생략해도 재정의가 성립할 수 있다.

```cpp
class UpdateTarget
{
public:
	virtual ~UpdateTarget() = default;
	virtual void Update(float deltaSeconds) = 0;
};

class FixedUpdateTarget final : public UpdateTarget
{
public:
	void Update(float deltaSeconds) override;
};
```

**권장:** final은 확장 금지 계약일 때만 적용한다. 성능을 위해 사용하면 컴파일러·빌드·호출 경로에서 측정한다.

### 기반 타입을 통한 파괴와 복사

**필수:** 일반적인 `delete Base*` 또는 `std::unique_ptr<Base>`의 기본 삭제 경로로 파생 객체를 정리하도록 허용하는 기반 클래스는 공개 가상 소멸자를 제공한다. 기반 타입을 통한 삭제를 금지하는 설계는 `protected` 비가상 소멸자를 사용할 수 있다. 전용 삭제자·외부 수명 관리가 필요한 API는 정리 계약을 별도로 명시한다. 상속하지 않는 일반 값 타입에 가상 소멸자를 일괄 추가하지 않는다.

**권장:** 다형적 객체를 기반 타입의 값으로 복사하여 파생 상태가 잘리는 객체 슬라이싱을 피한다. 기반 참조·포인터로 사용하고, 공개 복사·이동 제공 여부를 검토한다.

## 근거와 출처

기존 [DevMiniEngine 자료](../../../ref/CodingConvention.md), [DevRniman 자료](../../../ref/DevRnimanConvention/CodingConvention.md), [DX12 자료](../../../ref/gameConvention/%5BDX12%5D%20coding%20convention%2825.10.04%29.md)의 공개 API 우선 배치와 기능별 묶음을 유지했다. 자료의 복사 금지·이동 기본 제공 템플릿과 크기순 멤버 정렬은 타입별 수명·주소 의존성을 먼저 판단하도록 수정했다. 사용자 선택에 따라 선언 순서는 권장으로 두고 접근 구역의 필요한 반복을 허용한다. 자료 원본은 보존한다.

[RnimanEngine 확인](../../projects/rniman-engine.md#클래스구조체-규칙의-근거)은 사례이며 전체 적용 결과가 아니다. 채택 근거는 2026-10-09 사용자 선택이다.

외부 가이드는 설계 권고이고 표준은 언어 동작의 근거다. 적용 강도·선언 순서·예외 범위는 사용자가 선택한 개인 규칙이다. **확인일: 2026-10-09.** Core Guidelines는 2026-06-14 표기본, Google 가이드는 확인일의 온라인 본문을 참고했다. C++ 작업 초안은 계속 갱신되므로 이 문서는 C++11의 기본 기능을 대상으로 하며 조건부 `explicit`만 C++20으로 구분한다. 최신 초안의 이후 버전 기능까지 도입하는 의미는 아니다.

- C++ Core Guidelines [C.2](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-struct), [C.20](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-zero), [C.21](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-five), [C.46](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-explicit), [C.128](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-override): 타입 선택·특수 멤버·명시적 변환·가상 함수 표기를 참고했다. C.21의 다섯 연산 명시 권고는 연산별 정책 검토로 완화했다. 반복 선언보다 필요한 정책을 드러내기 위한 선택이다. C.128의 한 표기 권장을 기본으로 두되 병기도 허용한다.
- [Google — Copyable and Movable Types](https://google.github.io/styleguide/cppguide.html#Copyable_Movable_Types): 복사·이동 허용을 타입의 의미와 함께 판단하는 비교 근거다. Google은 공개 인터페이스에서 복사·이동 정책을 대체로 명시하도록 권고한다. 이 문서는 멤버의 기본 동작으로 의미가 충분한 경우 Rule of Zero를 우선한다.
- C++ 작업 초안 [class.access.general](https://eel.is/c++draft/class.access.general), [class.access.base](https://eel.is/c++draft/class.access.base): 멤버·상속 접근의 기본값. [class.prop](https://eel.is/c++draft/class.prop)·[dcl.init.aggr](https://eel.is/c++draft/dcl.init.aggr)는 레이아웃·단순 복사·집합체의 별도 조건이다.
- [class.conv.ctor](https://eel.is/c++draft/class.conv.ctor), [class.conv.fct](https://eel.is/c++draft/class.conv.fct), [dcl.fct.spec](https://eel.is/c++draft/dcl.fct.spec): 생성자·변환 연산자와 `explicit`.
- [dcl.fct.def.default](https://eel.is/c++draft/dcl.fct.def.default), [dcl.fct.def.delete](https://eel.is/c++draft/dcl.fct.def.delete), [class.copy.ctor](https://eel.is/c++draft/class.copy.ctor), [class.copy.assign](https://eel.is/c++draft/class.copy.assign): 기본·삭제 정의와 복사·이동 생성 조건.
- [class.base.init](https://eel.is/c++draft/class.base.init), [class.virtual](https://eel.is/c++draft/class.virtual), [lex.name](https://eel.is/c++draft/lex.name), [expr.delete](https://eel.is/c++draft/expr.delete): 초기화·파괴 순서, 가상 재정의·특별한 의미를 갖는 식별자와 기반 타입 삭제 조건.

## 미결정 정책

상태: 초안 · 아래 두 묶음은 채택 제외다. 검토 제안이며 보류·폐기 결정은 없다.

### 생성 실패·소멸 진단·noexcept

생성 실패를 예외·팩터리 결과·별도 초기화로 전달하는 방식, 소멸 중의 실패 보고·예외 처리, `noexcept`의 적용 정책은 미결정이다.

검토 제안: 외부 API·오류 처리 때문에 생성과 `Initialize`를 나누는 경우에는 미초기화·초기화 성공·실패 후 상태, 재시도 여부, 허용 연산과 정리 책임을 명시한다. 이동에 `noexcept`를 명시할 때는 멤버·기반 클래스와 직접 구현의 비예외 계약을 확인한다. 이 제안을 공통 채택 규칙이나 확정된 프로젝트별 결정 절차로 적용하지 않는다.

### 다형적 복제·복잡한 상속

`Clone`의 필요·반환 소유권·복제 범위와 다중·비공개·가상 상속은 미정이다. 사용처·수명·인터페이스 관계를 검토하며 복제 기본형·복잡한 상속의 일괄 허용·금지는 정하지 않는다.

`auto`와 일반 함수의 언어 지정자는 해당 주제에서 따로 다룬다.

## 관련 문서

- [컨벤션 적용 기준](../../baseline.md)
- [자료형 선택과 별칭 (초안)](type-selection.md)
- [attribute 사용 (초안)](attributes.md)
- [프로젝트별 규칙](../../projects/index.md)

## 변경 기록

- 2026-10-16: 반복 설명·중복 예시·배경을 줄여 핵심 규칙과 예시 중심으로 정리했다. 규칙 강도·예외·버전과 채택·초안·미결정 상태는 유지했다.

- 2026-10-09: 사용자 선택으로 클래스·구조체의 기본 규칙을 채택했다. override·조건부 final은 권장, 병기는 허용하며 선언 순서·접근 구역 반복과 기존 문서 유지·필요한 지점의 링크 원칙을 정했다. 생성 실패·소멸 진단·noexcept, 다형적 복제·복잡한 상속은 별도 초안 절에 두고 채택에서 제외했다.
