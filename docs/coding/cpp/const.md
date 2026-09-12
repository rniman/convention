# C++ const 사용 규칙

[C++ 목차](index.md) · 관련: [명명 규칙](naming.md), [초기화 규칙](initialization.md)

상태: 채택 · 적용 범위: C++의 읽기 전용 의도 표현 · 예제: C++11 이상

`const`는 변경하면 안 되는 값을 명시하기 위해 사용한다. 현재 코드에서 재대입하지 않는다는 사실만으로 지역 변수에 일괄 적용하지 않는다.

## 핵심 규칙

| 대상 | 적용 기준 | 강도 |
| --- | --- | --- |
| 지역 변수 | 의미상 읽기 전용임이 명확할 때 적용 | 필수 |
| 계산용 작업 변수 | 갱신·누적할 값은 일반 변수로 선언 | 권장 |
| 참조·포인터 입력 | 대상 변경이 필요 없으면 `const T&`·`const T*` | 권장 |
| 값으로 받는 매개변수 | 함수 선언에 최상위 `const`를 붙이지 않음 | 권장 |
| 조회 멤버 함수 | 객체의 논리적 상태를 변경하지 않으면 후행 `const` | 권장 |
| 컴파일 시점의 고정값 | 상수 표현식으로 사용할 값은 `constexpr` | 권장 |

## 지역 변수: 읽기 전용 의도가 명확할 때

고정된 기준값이나 보존해야 할 스냅샷처럼, 해당 범위에서 변경하면 의미가 훼손되는 값에 `const`를 사용한다. 미래의 요구사항을 예측하는 대신 현재 설계에서 변경을 허용할 값인지 판단한다.

```cpp
int ApplyDamageAndGetLoss(
	int& health,
	int damage)
{
	// 비교 기준으로 보존해야 하는 이전 상태의 복사본
	const int originalHealth = health;
	health -= damage;
	return originalHealth - health;
}
```

계산 과정에서 값을 보정·누적하는 작업 변수는 일반 변수로 작성한다. 지금은 한 번만 사용하더라도 읽기 전용 의도가 없다면 `const`를 강제하지 않는다.

```cpp
int CalculateDamage(
	int baseDamage,
	int bonusDamage)
{
	int damage = baseDamage;
	damage += bonusDamage;
	return damage;
}
```

`const`를 유지하려고 불필요한 변수를 추가하거나 로직을 복잡하게 나누지 않는다. 요구사항이 바뀌어 갱신이 필요해지면 `const`를 제거할 수 있다. 기존 값을 계속 보존해야 한다면 새 작업 변수를 사용한다.

## 매개변수와 멤버 함수

값·참조 중 어떤 형태로 받을지는 [함수 매개변수·반환 규칙](functions.md)을 따른다. 이 절은 선택한 전달 형태에 `const`를 적용하는 의미를 다룬다.

```cpp
#include <string>

bool HasName(const std::string& name)
{
	return !name.empty();
}

void SetHealth(int health); // 값 전달: 선언에 const를 붙이지 않는다.
```

값 매개변수의 최상위 `const`는 호출자의 값을 보호하는 계약이 아니다. 정의 내부에서 값을 보존해야 할 명확한 이유가 있을 때만 지역 변수 원칙에 따라 적용한다.

```cpp
class Player
{
public:
	int GetHealth() const
	{
		return mHealth;
	}

private:
	int mHealth = 100;
};
```

조회 함수의 후행 `const`는 지역 변수의 선택적 적용과 구분한다. 반환한 포인터·참조를 통해 객체 상태를 변경하게 하는 함수도 단순 조회로 취급하지 않는다. `const`만으로 스레드 안전성이나 깊은 불변성이 보장되는 것은 아니다.

## 포인터의 대상과 포인터 자체

| 표기 | 해당 포인터를 통한 대상 변경 | 포인터 재지정 |
| --- | --- | --- |
| `const int* value` | 불가 | 가능 |
| `int* const value` | 가능 | 불가 |
| `const int* const value` | 불가 | 불가 |

기본 표기는 `const T`로 통일한다. `const T&`는 그 참조를 통한 대상 수정을 제한한다. 다른 경로에서 원본이 바뀔 수 있으므로 참조 자체를 “상태가 고정된 스냅샷”으로 간주하지 않는다.

## const와 constexpr

`const`는 초기화 이후의 수정을 제한하며 실행 중 구한 값에도 사용할 수 있다. `constexpr` 변수는 컴파일 시점에 평가할 수 있는 초기값이 필요하다.

```cpp
constexpr int MAX_RETRY_COUNT = 3;
```

컴파일 시점에 정하는 고정값에는 `constexpr`를 권장한다. 이름은 [상수 명명 규칙](naming.md#상수-명명)을 따른다.

## 예외와 주의사항

- 이동해서 전달하거나 반환할 객체에는 기계적으로 `const`를 붙이지 않는다. 일반적인 이동 생성은 비상수 객체를 요구하므로 복사가 발생하거나 컴파일되지 않을 수 있다.
- `const` 멤버 변수를 모든 클래스에 일괄 도입하지 않는다. 복사·이동 대입 가능성 등 타입 설계에 영향을 주므로 별도로 판단한다.
- 필요한 갱신을 허용하려고 `const_cast`로 제한을 우회하지 않는다. 선언 또는 인터페이스의 의도를 먼저 바로잡는다.
- 외부 API의 지정된 시그니처는 유지한다. 스마트 포인터 전달은 [소유권·수명 규칙](ownership.md#전달할-때-소유-의도를-표현한다)을 따른다. 캐시를 위한 `mutable` 사용은 후속 설계 주제로 다룬다.

## 근거와 출처

[기존 컨벤션](../../../ref/CodingConvention.md)의 읽기 전용 매개변수·멤버 함수 원칙을 참고했다. `const T&`는 모든 입력 타입의 기본값으로 확대하지 않고 값 전달과 구분했다.

Google은 지역 변수의 `const` 사용에 중립적이다. C++ Core Guidelines는 변경하지 않는 객체에 `const`를 권장한다. 이 문서는 2026-09-12 사용자 선택에 따라 **의미상 읽기 전용임이 명확한 지역 변수에만 적용**하는 원칙을 채택했다. 재대입이 없다는 사실만으로 적용하는 방식은 채택하지 않았다.

- [Google C++ Style Guide — Use of const](https://google.github.io/styleguide/cppguide.html#Use_of_const)
- [C++ Core Guidelines — Con.1과 이동 관련 예외](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconst-immutable)
- [C++ Core Guidelines — Con.4](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconst-const)

출처 확인일: 2026-09-12.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.
