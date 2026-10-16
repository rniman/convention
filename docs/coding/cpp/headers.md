# C++ 헤더·include 규칙

[C++ 목차](index.md)

상태: 채택 · 적용 범위: 일반 C++ 헤더와 구현 파일의 의존성 · 예제: C++11 이상 · 개정일: 2026-10-16

숨은 include 의존성 없이 사용할 수 있는 헤더를 작성한다. 파일 이름은 [프로젝트 구조·파일 배치](project-structure.md#폴더파일-이름)를 따른다.

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

`#pragma once`는 라이선스 고지 뒤·다른 지시문 앞에 둔다. 미지원 도구·이식성 요구에는 고유 include guard를 사용하고 두 방식을 병용하지 않는다. `#pragma once`는 비표준 확장이며 빌드 속도 우위를 보장하지 않는다.

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

다른 헤더·PCH의 선행 include 없이 사용할 수 있어야 한다. 빌드의 플랫폼·기능 매크로는 전제할 수 있다.

헤더 보호는 번역 단위 내 중복 포함만 막는다. 비인라인 함수·외부 연결 변수의 중복 정의를 막지는 않으므로 일반 구현은 `.cpp`, 필요한 템플릿·인라인 정의는 헤더에 둔다.

## 직접 include와 순서

전체 정의·외부 함수가 필요하면 헤더와 `.cpp`에서 직접 include한다. 자기 헤더의 간접 include에도 의존하지 않는다. 자기 클래스 선언은 자기 헤더로 충족하며 선언만 필요한 타입은 아래 전방 선언 조건을 따른다. 순서는 다음과 같다.

1. 대응하는 자기 헤더 (`.cpp`만).
2. 같은 모듈 헤더.
3. 다른 프로젝트 모듈 헤더.
4. 서드파티·플랫폼 헤더.
5. 표준 라이브러리 헤더.

그룹 사이는 빈 줄 하나로 구분하고, 각 그룹 안에서는 include 경로의 알파벳 순서로 정렬한다. 빈 그룹은 생략한다. 순서 의존성이 있는 외부 헤더는 요구 순서를 지키고 이유를 주석으로 남긴다.

```cpp
// Player.cpp: 자기 헤더 뒤에 직접 사용하는 표준 헤더를 포함한다.
#include "Game/Player.h"

#include <string>
```

프로젝트 헤더는 `"Game/Player.h"`처럼 빌드에서 지정한 include 기준 디렉터리로부터의 경로를 사용한다. 절대 경로와 `../` 연쇄 경로를 피한다. 표준·플랫폼 헤더에는 `<...>`를 사용하고 서드파티 헤더는 라이브러리의 사용 지침을 따른다. 경로의 대소문자는 실제 파일과 일치시키고 구분자는 `/`로 작성한다.

## 전방 선언과 전체 정의

전방 선언은 직접 관리하는 클래스·구조체의 실제 네임스페이스에 작성한다. 외부·`std` 타입은 임의로 선언하지 않는다.

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

포함한 파일의 이름 탐색을 바꾸지 않도록 헤더 전역·네임스페이스 범위의 `using namespace`를 금지하고 이름을 한정한다. 공개 API 별칭과 `.cpp`의 using 정책은 별도 판단이다.

PCH 선행 include가 빌드 요구일 때만 `.cpp`의 자기 헤더 앞에 둔다. 공개 헤더에는 PCH를 넣지 않으며 PCH·부모 클래스의 간접 include로 직접 의존성을 대신하지 않는다. 독립성은 PCH·강제 include를 끄고 검증한다.

## 검증과 범위

- 실제 코드 적용 시 각 헤더만 include하는 최소 `.cpp`가 해당 프로젝트 설정에서 컴파일되는지 확인한다.
- 위의 include 순서와 PCH 예외를 지킨다. 순환 include가 있으면 공통 타입이나 인터페이스의 분리를 검토한다.
- 예제는 파일별 조각이며 include 경로에 맞는 파일 배치가 필요하다.
- 모듈, 헤더 유닛, 플랫폼 매크로 정책과 구체적인 PCH 설정은 후속 주제로 둔다.

## 관련 문서

- [코드 포맷 규칙](formatting.md)
- [주석 작성 규칙](comments.md)

## 근거와 출처

[기존 정리본](../../../ref/DevRnimanConvention/CodingConvention.md)의 보호·순서는 유지하되 전방 선언은 자체 타입의 선언에 한정했다. [과거 자료](../../../ref/CodingConvention.md)의 간접 include·범위 없는 using 허용은 독립성·이름 탐색을 위해 제한했다.

Google의 헤더 독립성과 직접 include 원칙을 참고했다. Google은 include guard, 표준·외부 헤더 우선 순서, 전방 선언 최소화를 사용한다. 이 문서의 `#pragma once`, 프로젝트 헤더 우선 순서, 제한적 전방 선언은 기존 개인 스타일을 반영한 차이다.

- [Google — Header Files](https://google.github.io/styleguide/cppguide.html#Header_Files)
- [Google — Names and Order of Includes](https://google.github.io/styleguide/cppguide.html#Names_and_Order_of_Includes)
- [Google — Namespaces](https://google.github.io/styleguide/cppguide.html#Namespaces)
- [Microsoft — once pragma](https://learn.microsoft.com/en-us/cpp/preprocessor/once?view=msvc-170)

출처 확인일: 2026-09-12.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.

## 변경 기록

- 2026-10-16: 반복 설명·중복 예시·배경을 줄여 핵심 규칙과 예시 중심으로 정리했다. 규칙 강도·예외·버전과 채택·초안·미결정 상태는 유지했다.
