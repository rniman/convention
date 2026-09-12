# C++ 소유권·수명 규칙

[C++ 목차](index.md) · 관련: [const 사용 규칙](const.md), [헤더·include 규칙](headers.md)

상태: 채택 · 적용 범위: C++ 객체와 자원의 소유·대여·해제 · 예제: C++14 이상

소유권은 자원을 관리하고 해제를 책임지는 관계다. 다른 코드에서 객체를 사용한다고 소유권을 함께 가져야 하는 것은 아니다. 먼저 누가 소유하는지 정하고, 사용하는 동안 객체가 유효하게 남는지 확인한다. 예제의 `std::make_unique`는 C++14부터 제공되며 프로젝트 전체의 표준 버전은 별도로 정한다.

## 선택 기준

| 필요한 관계 | 기본 표현 | 의미 |
| --- | --- | --- |
| 범위나 다른 객체에 종속된 소유 | 값·멤버·컨테이너 | 불필요한 동적 할당 없이 수명 관리 |
| 동적 객체의 단독 소유 | `std::unique_ptr<T>` | 소유자 하나, 필요하면 이동 |
| 독립된 여러 주체의 공동 소유 | `std::shared_ptr<T>` | 마지막 소유자가 놓을 때 객체 해제 |
| 소유권 없이 반드시 존재하는 객체 사용 | `T&` | 사용하는 동안 대상의 유효성 필요 |
| 소유권 없이 부재도 허용하는 객체 사용 | `T*` | null 의미와 처리 방법 명시 |
| 공동 소유 객체를 수명 연장 없이 관찰 | `std::weak_ptr<T>` | 사용 시 `lock()`으로 소유권 확보 시도 |

위 표는 **권장 선택 기준**이다. 아래의 해제 책임·유효성 규칙은 이 규칙을 적용할 때 필수다. 읽기 전용 여부는 [const 사용 규칙](const.md)에서 판단한다. `const`와 소유권은 서로 다른 기준이다.

## 값과 자동 자원 관리 우선

**권장:** 지역 값, 멤버 객체, 표준 컨테이너로 충분하면 동적 할당을 추가하지 않는다. 동적 객체를 소유해야 할 때는 단독 소유를 기본으로 한다.

**필수:** 획득한 자원은 해제를 담당하는 객체에 즉시 맡긴다. 소멸 시 자원을 정리하는 RAII 방식으로 조기 반환이나 예외 경로에서도 해제 책임이 유지되게 한다. 파일·잠금·외부 핸들도 해당 자원에 맞는 관리 객체를 사용한다.

```cpp
#include <memory>

struct Texture
{
	int width = 0;
};

std::unique_ptr<Texture> CreateTexture(int width)
{
	auto texture = std::make_unique<Texture>();
	texture->width = width;
	return texture;
}
```

새 코드에서는 관리되지 않는 `new`·`delete`를 일반 로직에 흩어 놓지 않는다. 외부 API나 사용자 정의 할당자가 필요하면 전용 래퍼 또는 올바른 deleter를 사용한다. 외부 자원에 기본 `delete`를 임의로 적용하지 않는다.

## 빌려 쓰는 참조와 포인터

**필수:** 이 컨벤션에서 일반 `T*`와 `T&`는 비소유로 취급한다. 받는 쪽은 임의로 해제하거나 새 소유 스마트 포인터로 감싸지 않는다. 이는 언어가 강제하는 성질이 아니라 새 코드의 계약이다. 외부 API의 소유권 반환은 API 문서에 따라 별도로 처리한다.

- 빌려 받은 참조만으로 대상의 수명이 보장되지는 않는다. 임시 객체의 수명 연장에는 별도의 언어 조건이 있으며 참조를 전달·저장한다고 연장이 이어지지 않는다.
- 호출 동안만 쓰는 입력은 기본적으로 저장하지 않는다. 저장한다면 호출 이후 필요한 수명 조건을 API 주석에 명시한다.
- `get()`으로 얻은 포인터는 빌린 주소다. 사용하는 동안 대상을 유지하는 소유자가 있어야 하며 대상이 파괴되거나 주소가 무효화된 뒤에는 사용하지 않는다. 소유권 이전이나 다른 공동 소유자가 있을 수 있으므로 원래 핸들의 존재만으로 판단하지 않는다.
- `nullptr` 검사로 이미 해제된 객체의 주소를 판별할 수는 없다.

관찰용 포인터 멤버 자체를 금지하지 않는다. 소유자가 관찰자보다 오래 살고 관찰 중 대상이 제거되지 않는 관계라면 사용할 수 있다. 이 보장이 없으면 소유 구조나 핸들 방식을 다시 설계한다.

## 전달할 때 소유 의도를 표현한다

아래는 직접 설계하는 표준 스마트 포인터 API의 전달 기준이다. 외부 API와 COM의 `ComPtr` 시그니처에는 그대로 강제하지 않는다.

| 함수의 목적 | 표현 예시 |
| --- | --- |
| 객체를 잠시 읽음 | `void Draw(const Texture& texture);` |
| 없는 객체도 허용하며 잠시 사용 | `void DrawIfPresent(const Texture* texture);` |
| 단독 소유권을 넘겨받음 | `void SetTexture(std::unique_ptr<Texture> texture);` |
| 공동 소유권을 넘겨받아 보관하거나 수명을 유지 | `void KeepTexture(std::shared_ptr<Texture> texture);` |
| 호출자의 단독 소유 포인터를 교체·재설정 | `void ReplaceTexture(std::unique_ptr<Texture>& texture);` |
| 호출자의 공동 소유 포인터를 교체·재설정 | `void ReplaceSharedTexture(std::shared_ptr<Texture>& texture);` |
| 특정 조건에서만 공동 소유권을 복사하여 보관 | `void CacheIfNeeded(const std::shared_ptr<Texture>& texture);` |
| 약한 참조를 넘겨받아 보관 | `void WatchTexture(std::weak_ptr<Texture> texture);` |
| 약한 참조를 보관하지 않고 lock 시도 | `void CheckTexture(const std::weak_ptr<Texture>& texture);` |

**필수:** 스마트 포인터 매개변수는 소유권 또는 수명 관리가 함수의 역할일 때 사용한다. 객체만 잠시 사용한다면 참조·포인터를 전달한다. 단순히 복사를 피하려고 모든 스마트 포인터를 `const&`로 받지 않는다.

### 값 전달과 참조 전달

- **단독 소유권 인수:** `unique_ptr<T>` 값 전달을 기본으로 한다. 호출 경계에서 소유권이 이동하며, 함수가 보관하지 않으면 매개변수 소멸 시 해제된다. 일반적인 인수 API에 `unique_ptr<T>&&`를 별도 기본형으로 추가하지 않는다.
- **공동 소유권 인수:** `shared_ptr<T>` 값 전달 후 멤버에는 `std::move`로 저장한다. 호출자가 lvalue를 넘기면 소유권을 복사하고, 더 이상 필요 없는 핸들을 이동해서 넘기면 그 핸들의 소유권을 이전한다. 대상 객체 자체를 복사하는 것은 아니다.
- **핸들 교체:** `unique_ptr<T>&`·`shared_ptr<T>&`는 호출자의 핸들을 실제로 교체하거나 재설정할 수 있는 API에서만 사용한다. 객체 내용을 수정한다는 이유만으로 선택하지 않는다.
- **조건부 공동 소유:** `const shared_ptr<T>&`는 일부 경로에서만 소유권을 복사하여 보관할 때 허용한다. 보관하는 분기에서 값으로 복사한다. 항상 보관하는 API는 값 전달을 사용한다.
- **단순 관찰:** `const unique_ptr<T>&`를 객체 접근용 기본형으로 사용하지 않는다. null을 허용하면 `T*`, 반드시 존재하면 `T&`를 사용하고 읽기 전용 여부에 따라 대상에 `const`를 붙인다.
- **약한 참조:** `weak_ptr<T>`도 보관하면 값 전달, 보관하지 않고 검사하면 `const&`를 기본으로 한다. 참조로 받은 핸들 자체를 호출 이후까지 보관하지 않는다.

핸들 자체를 검사하는 범용 도구나 전달 템플릿처럼 소유자 타입이 필요한 경우는 예외로 허용하되, 단순 관찰 함수에 관성적으로 적용하지 않는다.

### 수명과 const의 주의점

`const shared_ptr<T>&`는 새로운 공동 소유자를 만들지 않는다. 다른 별칭이나 콜백이 원본 핸들을 재설정할 수 있다면 먼저 로컬 `shared_ptr` 복사본을 확보하거나 값 전달로 바꾼다. 같은 핸들에 대한 동시 접근의 동기화는 별도로 필요하다.

`const shared_ptr<T>&`의 `const`는 이 참조를 통한 핸들 변경을 제한하며 대상 `T`를 읽기 전용으로 만들지 않는다. 공동 소유하면서 읽기 전용 접근을 표현하려면 `shared_ptr<const T>`를 사용한다. 타입의 `const` 위치에 대한 일반 설명은 [const 사용 규칙](const.md)을 따른다.

### 소유권 저장 예시

```cpp
#include <memory>
#include <utility>

// Texture의 정의가 있는 상황의 예시
class Renderer
{
public:
	void SetTexture(std::unique_ptr<Texture> texture)
	{
		mTexture = std::move(texture);
	}

private:
	std::unique_ptr<Texture> mTexture;
};

class TextureCache
{
public:
	void KeepTexture(std::shared_ptr<Texture> texture)
	{
		mTexture = std::move(texture);
	}

	void CacheIfNeeded(const std::shared_ptr<Texture>& texture)
	{
		if (!mTexture)
		{
			mTexture = texture;
		}
	}

private:
	std::shared_ptr<Texture> mTexture;
};
```

호출자가 보유한 `unique_ptr`를 넘길 때는 `SetTexture(std::move(texture))`처럼 이전을 드러낸다. 이전된 원래 `unique_ptr`는 비어 있으므로 다시 대상을 역참조하지 않는다. 이 성질을 모든 타입의 이동 후 상태에 일반화하지 않는다.

`release()`는 삭제 없이 관리 책임을 내려놓으므로 소유권을 넘겨받는 API가 명확한 경우에만 사용한다. 같은 raw pointer로 서로 독립된 소유 스마트 포인터를 만들지 않는다.

## 공동 소유와 순환 관계

`shared_ptr`는 여러 곳에서 접근한다는 이유만으로 선택하지 않는다. 각 주체가 독립적으로 대상의 수명을 유지해야 하는지 먼저 확인한다.

**필수:** 공동 소유 관계에 순환이 생기지 않게 한다. 부모를 참조하는 자식이나 콜백이 소유자를 다시 가리키는 관계에서는 비소유 관계 또는 `weak_ptr`를 검토한다. 사용 시에는 `expired()` 확인과 접근을 분리하기보다 `lock()` 결과를 보관한다.

```cpp
// Texture가 정의되고 <memory>가 포함된 상황의 예시
bool HasPositiveWidth(const std::weak_ptr<Texture>& texture)
{
	auto lockedTexture = texture.lock();
	if (!lockedTexture)
	{
		return false;
	}

	return lockedTexture->width > 0;
}
```

이 예제는 “대상이 존재하고 너비가 양수인가”를 질의한다. 대상이 없거나 너비가 양수가 아니면 false다. 실제 너비를 조회하는 API에서 부재를 정상 너비인 0으로 대신하지 않으며, 실패 표현은 [함수 반환 규칙](functions.md)을 따른다. `shared_ptr`로 수명을 유지해도 대상 객체에 대한 동시 읽기·쓰기까지 안전해지는 것은 아니다.

## 수명이 끝나는 경계

- 지역 객체나 임시 객체를 가리키는 포인터·참조·뷰를 유효 기간 밖으로 반환하거나 저장하지 않는다.
- 컨테이너 재할당·삭제가 참조·포인터·이터레이터를 무효화하는 조건을 확인한다. 컨테이너마다 무효화 규칙은 다르다.
- `std::string_view`(C++17), `std::span`(C++20)은 비소유다. 원본의 수명과 유효한 저장 공간을 별도로 보장한다.
- 비동기 작업과 저장되는 콜백은 호출 범위를 넘어 실행될 수 있다. 지역 참조와 `this`를 캡처하기 전에 완료 시점까지의 수명을 보장한다.
- 소유권 이전, null 허용, 반환한 참조의 유효 기간은 [API 주석](comments.md)에 기록한다.
- 불완전 타입과 스마트 포인터 소멸 지점은 [헤더·include 규칙](headers.md)을 함께 확인한다.

## 프로젝트별 예외

COM·DX12의 `ComPtr`, 메모리 풀, ECS 핸들, GPU 자원 해제 시점은 해당 환경의 수명 규약을 따른다. 범용 스마트 포인터 규칙만으로 외부 참조 계수나 비동기 사용 완료를 대신하지 않는다. 구체적인 조작 방법은 프로젝트별 문서에서 다룬다.

## 근거와 출처

[기존 자료](../../../ref/DevRnimanConvention/CodingConvention.md)의 단독·공동 소유 구분을 유지했다. “스마트 포인터는 const& 전달”은 함수의 소유 의도에 따라 구분하고, “raw pointer 저장은 위험”은 수명 보장 여부로 판단하도록 구체화했다. COM 세부 규칙은 이 범용 문서에서 분리했다.

C++ Core Guidelines의 자동 자원 관리, 비소유 포인터, 단독 소유 우선, 스마트 포인터 매개변수 원칙을 참고했다. 모든 동적 할당이나 raw pointer를 금지하는 규칙은 아니다.

- [R.1 — RAII](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii)
- [R.3 — 비소유 포인터](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-ptr)
- [R.21 — 단독 소유 우선](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-unique)
- [R.24 — weak_ptr와 순환 관계](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-weak_ptr)
- [R.30 — 스마트 포인터 매개변수](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-smartptrparam)
- [R.32 — unique_ptr 값 전달](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-uniqueptrparam)
- [R.33 — unique_ptr 핸들 교체](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-reseat)
- [R.34 — shared_ptr 값 전달](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-sharedptrparam-owner)
- [R.35 — shared_ptr 핸들 교체](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-sharedptrparam)
- [R.36 — 조건부 공동 소유](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-sharedptrparam-const)

R.36 원문에는 미완성 표시가 남아 있다. 조건부 보관의 의미를 참고하되 위 허용 조건은 이 저장소의 확정 정책으로 명시했다. `weak_ptr` 전달 기준과 `unique_ptr&&`를 기본형으로 두지 않는 선택도 개인 컨벤션이다.

출처 확인일: 2026-09-12.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.

## 변경 기록

- 2026-09-12: C++ 언어 사용 규칙을 한곳에서 찾도록 설계에서 코딩 → C++로 이동했다. 규칙과 예제, 채택 상태는 유지했다.
