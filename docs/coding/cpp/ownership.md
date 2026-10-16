# C++ 소유권·수명 규칙

[C++ 목차](index.md)

상태: 채택 · 적용 범위: C++ 객체와 자원의 소유·대여·해제 · 예제: C++14 이상 · 개정일: 2026-10-16

소유자·해제 책임과 빌려 쓰는 동안의 유효성을 구분한다. 예제의 `std::make_unique`는 C++14이며 프로젝트 표준 버전은 별도 결정한다.

## 선택 기준

| 필요한 관계 | 기본 표현 | 의미 |
| --- | --- | --- |
| 범위나 다른 객체에 종속된 소유 | 값·멤버·컨테이너 | 불필요한 동적 할당 없이 수명 관리 |
| 동적 객체의 단독 소유 | `std::unique_ptr<T>` | 소유자 하나, 필요하면 이동 |
| 독립된 여러 주체의 공동 소유 | `std::shared_ptr<T>` | 마지막 소유자가 놓을 때 객체 해제 |
| 소유권 없이 반드시 존재하는 객체 사용 | `T&` | 사용하는 동안 대상의 유효성 필요 |
| 소유권 없이 부재도 허용하는 객체 사용 | `T*` | null 의미와 처리 방법 명시 |
| 공동 소유 객체를 수명 연장 없이 관찰 | `std::weak_ptr<T>` | 사용 시 `lock()`으로 소유권 확보 시도 |

표는 **권장**이며 아래 해제·유효성 규칙은 필수다. [const](const.md)의 읽기 전용 여부와 소유권은 별개다.

## 값과 자동 자원 관리 우선

**권장:** 지역 값, 멤버 객체, 표준 컨테이너로 충분하면 동적 할당을 추가하지 않는다. 동적 객체를 소유해야 할 때는 단독 소유를 기본으로 한다.

**필수:** 자원은 즉시 RAII 객체에 맡겨 조기 반환·예외에도 정리한다. 파일·잠금·핸들도 맞는 관리 객체를 사용한다.

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

**필수:** 일반 `T*`·`T&`는 비소유 계약이며 받는 쪽에서 해제·새 소유자로 감싸지 않는다. 언어의 강제가 아니며 외부 API의 소유권 반환은 해당 계약을 따른다.

- 빌려 받은 참조만으로 대상의 수명이 보장되지는 않는다. 임시 객체의 수명 연장에는 별도의 언어 조건이 있으며 참조를 전달·저장한다고 연장이 이어지지 않는다.
- 호출 동안만 쓰는 입력은 기본적으로 저장하지 않는다. 저장한다면 호출 이후 필요한 수명 조건을 API 주석에 명시한다.
- `get()` 주소는 대상을 유지하는 소유자가 있는 동안만 사용한다. 이전·공동 소유가 가능하므로 원래 핸들의 존재만으로 판단하지 않는다.
- `nullptr` 검사로 이미 해제된 객체의 주소를 판별할 수는 없다.

관찰자보다 긴 소유자 수명과 대상 유지가 보장되면 관찰 포인터 멤버를 허용한다. 보장할 수 없으면 소유 구조·핸들을 재설계한다.

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

- 단독 소유는 값으로 인수하며 보관하지 않으면 매개변수 소멸 시 해제된다. `unique_ptr<T>&&`를 추가 기본형으로 두지 않는다.
- 공동 소유 값 전달은 lvalue의 소유권 복사·rvalue의 이전이며 객체 복사가 아니다. 항상 보관하면 값으로 받아 멤버에 이동 저장한다.
- 핸들 교체용 `&`는 객체 내용 수정만을 위해 사용하지 않는다. 조건부 공동 소유 `const&`는 보관 분기에서 복사한다.
- 객체 관찰에는 `const unique_ptr<T>&` 대신 null 허용 여부에 따라 `T*`·`T&`를 쓴다. weak_ptr는 보관 시 값, 검사만 할 때 const&이며 참조 핸들을 호출 뒤까지 저장하지 않는다.

소유자 타입을 검사하는 범용 도구·전달 템플릿은 예외로 허용한다.

### 수명과 const의 주의점

`const shared_ptr<T>&`는 소유자를 추가하지 않는다. 별칭·콜백의 핸들 재설정이 가능하면 로컬 복사본·값 전달로 수명을 확보한다. 같은 핸들의 동시 접근은 별도 동기화한다.

핸들의 `const`는 대상의 읽기 전용과 다르다. 읽기 전용 공동 소유는 `shared_ptr<const T>`로 표현한다([const 규칙](const.md)).

### 소유권 저장 예시

```cpp
#include <memory>
#include <utility>

// 앞 예제의 Texture가 정의된 상황
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

`SetTexture(std::move(texture))`처럼 단독 소유권 이전을 드러낸다. 이전된 `unique_ptr`는 비지만 이 상태를 모든 이동 타입에 일반화하지 않는다.

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

예시는 부재·양수가 아닌 너비에 false를 반환하는 질의다. 너비 반환 API의 부재를 0으로 대신하지 않으며 [반환 규칙](functions.md)을 따른다. 수명 유지는 대상의 동시 읽기·쓰기를 보장하지 않는다.

## 수명이 끝나는 경계

- 지역 객체나 임시 객체를 가리키는 포인터·참조·뷰를 유효 기간 밖으로 반환하거나 저장하지 않는다.
- 컨테이너 재할당·삭제가 참조·포인터·이터레이터를 무효화하는 조건을 확인한다. 컨테이너마다 무효화 규칙은 다르다.
- `std::string_view`(C++17), `std::span`(C++20)은 비소유다. 원본의 수명과 유효한 저장 공간을 별도로 보장한다.
- 비동기 작업과 저장되는 콜백은 호출 범위를 넘어 실행될 수 있다. 지역 참조와 `this`를 캡처하기 전에 완료 시점까지의 수명을 보장한다.
- 소유권 이전, null 허용, 반환한 참조의 유효 기간은 [API 주석](comments.md)에 기록한다.
- 불완전 타입과 스마트 포인터 소멸 지점은 [헤더·include 규칙](headers.md)을 함께 확인한다.

## 프로젝트별 예외

COM·DX12의 `ComPtr`, 메모리 풀, ECS 핸들, GPU 자원 해제 시점은 해당 환경의 수명 규약을 따른다. 범용 스마트 포인터 규칙만으로 외부 참조 계수나 비동기 사용 완료를 대신하지 않는다. 구체적인 조작 방법은 프로젝트별 문서에서 다룬다.

## 관련 문서

- [const 사용 규칙](const.md)
- [헤더·include 규칙](headers.md)

## 근거와 출처

[기존 자료](../../../ref/DevRnimanConvention/CodingConvention.md)의 소유 구분을 유지하며 일괄 const& 전달·raw pointer 저장 기피 대신 소유 의도·수명 보장으로 판단한다. COM은 프로젝트별 규칙이다.

Core Guidelines의 RAII·비소유·단독 소유·전달 원칙을 참고하며 동적 할당·raw pointer 자체를 금지하지 않는다.

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

R.36은 미완성 표시가 있어 조건부 보관을 참고하되 허용 조건은 개인 정책으로 정했다. weak_ptr 전달·unique_ptr&&를 기본으로 두지 않는 것도 개인 선택이다.

출처 확인일: 2026-09-12.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.

## 변경 기록

- 2026-10-16: 반복 설명·중복 예시·배경을 줄여 핵심 규칙과 예시 중심으로 정리했다. 규칙 강도·예외·버전과 채택·초안·미결정 상태는 유지했다.

- 2026-09-12: C++ 언어 사용 규칙을 한곳에서 찾도록 설계에서 코딩 → C++로 이동했다. 규칙과 예제, 채택 상태는 유지했다.
