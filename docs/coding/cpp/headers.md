# C++ 헤더·include 규칙

[C++ 목차](index.md) · 관련: [코드 포맷 규칙](formatting.md), [주석 작성 규칙](comments.md)

상태: 채택 · 적용 범위: 일반 C++ 헤더와 구현 파일의 의존성 · 예제: C++11 이상

헤더를 사용하는 쪽에서 include 순서를 맞추거나 숨은 의존성을 추측하지 않아도 되도록 작성한다. 예제의 파일 이름은 설명용이며 파일 명명 규칙 전체를 확정하지 않는다.

## 핵심 규칙

| 항목 | 기준 | 강도 |
| --- | --- | --- |
| 헤더 보호 | 지원 환경에서는 `#pragma once` 사용 | 권장 |
| 헤더 독립성 | 필요한 선언과 정의를 헤더 스스로 확보 | 필수 |
| 직접 사용한 의존성 | 필요한 헤더를 직접 include하되, 아래 조건의 전방 선언 허용 | 필수 |
| 구현 파일의 첫 include | 대응하는 자기 헤더, PCH 요구 시 예외 | 필수 |
| 전방 선언 | 직접 관리하는 타입의 선언만 필요한 경우에 제한하여 사용 | 권장 |
| 헤더의 using | 네임스페이스 범위의 `using namespace` 금지 | 필수 |
| 구현 분리 | 구현에서만 필요한 헤더는 `.cpp`에 배치 | 권장 |

## 헤더 보호와 독립성

기존 `#pragma once` 선호를 유지한다. 라이선스 고지가 있다면 그 뒤, 다른 전처리 지시문과 선언보다 앞에 배치한다. 지원하지 않는 도구나 이식성 요구가 있는 프로젝트에서는 고유한 include guard를 사용한다. 두 방식을 함께 쓰지는 않는다.

`#pragma once`는 표준 C++의 필수 기능이 아니며 include guard가 낡거나 잘못된 방식인 것도 아니다. 이 선택만으로 더 빠른 빌드를 보장하지 않는다.

```cpp
// Player.h
#pragma once

#include <string>

class Player
{
public:
	const std::string& GetName() const;

private:
	std::string mName;
};
```

`Player.h`를 먼저 읽기 위해 다른 헤더나 `pch.h`를 미리 include할 필요가 없어야 한다. 단, 빌드에서 명시한 플랫폼·기능 매크로 등 프로젝트 설정은 전제할 수 있다.

헤더 보호는 한 번의 번역 단위 안에서 중복 포함을 막는다. 여러 `.cpp`에서 포함되는 일반 비인라인 함수 정의나 외부 연결 변수 정의의 중복 문제까지 해결하지는 않는다. 일반 구현은 `.cpp`에 두고, 템플릿·인라인 정의처럼 헤더에 필요한 구현은 별도로 유지한다.

## 직접 include와 순서

다른 헤더가 우연히 가져오는 선언에 의존하지 않는다. 타입의 전체 정의나 외부 함수 선언이 필요하면 해당 헤더를 직접 include한다. `.cpp`에서도 자기 헤더의 간접 include에 의존하지 않는다. 단, 선언만 필요한 타입은 아래 전방 선언 조건을 적용할 수 있다. 자기 헤더에 선언된 자신의 클래스 등을 사용한다는 이유로 별도 헤더를 추가하라는 뜻은 아니다.

기존 자료의 프로젝트 헤더 우선 순서를 기본안으로 유지한다.

1. 대응하는 자기 헤더 (`.cpp`만).
2. 같은 모듈 헤더.
3. 다른 프로젝트 모듈 헤더.
4. 서드파티·플랫폼 헤더.
5. 표준 라이브러리 헤더.

그룹 사이는 빈 줄 하나로 구분하고, 각 그룹 안에서는 include 경로의 알파벳 순서로 정렬한다. 빈 그룹은 생략한다. 순서 의존성이 있는 외부 헤더는 요구 순서를 지키고 이유를 주석으로 남긴다.

```cpp
// Player.cpp
#include "Game/Player.h"

#include <string>

const std::string& Player::GetName() const
{
	return mName;
}
```

프로젝트 헤더는 `"Game/Player.h"`처럼 빌드에서 지정한 include 기준 디렉터리로부터의 경로를 사용한다. 절대 경로와 `../` 연쇄 경로를 피한다. 표준·플랫폼 헤더에는 `<...>`를 사용하고 서드파티 헤더는 라이브러리의 사용 지침을 따른다. 경로의 대소문자는 실제 파일과 일치시키고 구분자는 `/`로 작성한다.

## 전방 선언과 전체 정의

직접 관리하는 클래스·구조체를 포인터나 참조의 선언에서만 사용할 때 전방 선언을 고려한다. 반드시 실제 타입이 선언된 네임스페이스에 작성한다. 외부 라이브러리나 `std`의 타입을 임의로 전방 선언하지 않는다.

```cpp
// Renderer.h
#pragma once

class Scene;

class Renderer
{
public:
	void Draw(const Scene& scene);
};
```

`Draw`의 정의에서 `Scene` 멤버에 접근한다면 그 `.cpp`에는 `Scene`의 정의 헤더를 include한다.

| 상황 | 처리 |
| --- | --- |
| 직접 관리하는 타입의 포인터·참조를 선언만 함 | 전방 선언 가능 |
| 객체를 값 멤버로 보유하거나 해당 타입을 상속 | 전체 정의 include |
| `sizeof` 또는 멤버 접근이 필요한 구현 | 전체 정의 include |
| 표준 라이브러리 타입 사용 | 해당 표준 헤더 include |
| 불완전 타입을 지원하는 템플릿 사용 | 해당 템플릿과 사용 연산의 요구사항 확인 |

스마트 포인터도 전방 선언만으로 모든 연산이 가능한 것은 아니다. 예를 들어 불완전 타입을 소유하는 `std::unique_ptr<T>`는 소멸 지점의 요구사항을 확인해야 한다. 의존성을 줄이려고 값 멤버를 불필요한 포인터로 바꾸지는 않는다.

## 헤더의 네임스페이스와 PCH

헤더의 전역 또는 네임스페이스 범위에는 `using namespace std;` 같은 지시문을 두지 않는다. 포함한 파일의 이름 탐색에 영향을 주기 때문이다. 필요한 이름은 `std::string`처럼 한정한다. 공개 API로 의도한 타입 별칭은 별도로 판단한다. 이 규칙은 `.cpp`의 using 정책 전체를 정하는 것은 아니다.

PCH는 프로젝트별 빌드 최적화다. 빌드 도구가 `pch.h`의 선행 include를 요구할 때만 `.cpp`에서 자기 헤더 앞에 둔다. 일반 공개 헤더에는 PCH를 include하지 않는다.

PCH에 포함되어 있다는 이유로 직접 필요한 include를 생략하지 않는다. 헤더 독립성을 검증할 때는 PCH와 강제 include를 끈 별도 컴파일 환경을 사용한다. 부모 클래스에서 가져오는 간접 include도 자동 예외로 삼지 않는다.

## 검증과 범위

- 실제 코드 적용 시 각 헤더만 include하는 최소 `.cpp`가 해당 프로젝트 설정에서 컴파일되는지 확인한다.
- 위의 include 순서와 PCH 예외를 지킨다. 순환 include가 있으면 공통 타입이나 인터페이스의 분리를 검토한다.
- 예제는 파일별 조각이며 include 경로에 맞는 파일 배치가 필요하다.
- 모듈, 헤더 유닛, 플랫폼 매크로 정책과 구체적인 PCH 설정은 후속 주제로 둔다.

## 근거와 출처

[기존 정리본](../../../ref/DevRnimanConvention/CodingConvention.md)의 헤더 보호·include 순서를 유지했다. “전방 선언 우선”은 직접 관리하며 선언만 필요한 타입으로 범위를 좁혔다. PCH·부모 클래스의 간접 의존성 허용과 [기존 자료](../../../ref/CodingConvention.md)의 범위 없는 `using namespace std` 허용은 헤더 독립성과 이름 탐색을 위해 이번 정리에서 제한했다.

Google의 헤더 독립성과 직접 include 원칙을 참고했다. Google은 include guard, 표준·외부 헤더 우선 순서, 전방 선언 최소화를 사용한다. 이 문서의 `#pragma once`, 프로젝트 헤더 우선 순서, 제한적 전방 선언은 기존 개인 스타일을 반영한 차이다.

- [Google — Header Files](https://google.github.io/styleguide/cppguide.html#Header_Files)
- [Google — Names and Order of Includes](https://google.github.io/styleguide/cppguide.html#Names_and_Order_of_Includes)
- [Google — Namespaces](https://google.github.io/styleguide/cppguide.html#Namespaces)
- [Microsoft — once pragma](https://learn.microsoft.com/en-us/cpp/preprocessor/once?view=msvc-170)

출처 확인일: 2026-09-12.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.
