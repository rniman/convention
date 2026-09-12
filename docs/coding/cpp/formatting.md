# C++ 코드 포맷 규칙

[C++ 목차](index.md) · 관련: [명명 규칙](naming.md), [초기화 규칙](initialization.md)

상태: 채택 · 적용 범위: 직접 작성하는 C++ 코드의 배치와 공백 · 예제: C++11 이상

블록 경계와 문장의 구조를 일정하게 표현한다. 기존 자료에서 명시한 중괄호 사용·포인터 표기·인자 줄바꿈을 유지하고, 예제에서 사용하던 배치를 기본안으로 정리한다.

## 핵심 규칙

| 항목 | 규칙 | 강도 |
| --- | --- | --- |
| 들여쓰기 | 단계마다 탭 문자 1개, 기본 표시 너비 4칸 | 필수 |
| 블록 중괄호 | 여는 중괄호와 닫는 중괄호를 각각 독립된 줄에 배치 | 필수 |
| 제어문 본문 | 한 문장이어도 중괄호 사용 | 필수 |
| 한 줄 길이 | 표시 너비 100열을 기준으로 줄바꿈 | 권장 |
| 포인터·참조 선언 | `int* value`, `const Player& player`처럼 타입에 붙임 | 필수 |
| 선언 | 한 선언에 변수 하나 | 필수 |
| 빈 줄 | 논리적 단계 사이에 한 줄 | 권장 |
| 줄 끝 | 불필요한 공백 제거, 파일 끝 개행 유지 | 필수 |
| 줄바꿈 형식 | LF (`\n`) | 필수 |
| 인코딩 | UTF-8, BOM 없음 | 필수 |

편집기는 Tab 키를 공백으로 변환하지 않도록 설정한다. 줄 내부의 단어·연산자 구분에는 공백을 사용한다. 줄 길이는 탭을 4칸으로 표시한 열 너비를 기준으로 판단한다.

## 파일 인코딩과 줄바꿈

핵심 규칙의 UTF-8·LF는 여러 운영체제와 문서·웹 도구에서 같은 파일 형식을 유지하기 위한 선택이다. 모든 C++ 프로젝트가 따르는 유일한 표준이라는 뜻은 아니다.

- 같은 파일에 LF와 CRLF를 혼용하지 않는다.
- 줄 끝의 불필요한 공백·탭은 제거한다. 문자열 내용처럼 의미가 있는 공백은 보존한다.
- 비어 있지 않은 파일의 마지막 줄은 LF로 끝낸다. 마지막에 별도의 빈 줄을 추가하라는 뜻은 아니다.
- 외부 도구가 CRLF나 BOM을 명시적으로 요구하는 파일은 프로젝트별 예외로 기록한다. 컴파일러도 소스 파일을 UTF-8로 읽도록 프로젝트에서 설정한다.

EditorConfig로 적용할 때 대응하는 값은 `charset = utf-8`, `end_of_line = lf`, `insert_final_newline = true`다. 이 문서에서는 규칙을 정의하며 실제 도구 설정은 별도 작업으로 다룬다.

## 중괄호와 들여쓰기

함수·클래스·구조체·네임스페이스 및 제어문 블록에 같은 배치를 적용한다. 접근 지정자는 클래스와 같은 들여쓰기 수준에 두고 멤버는 한 단계 들여쓴다.

```cpp
class Player
{
public:
	void ApplyDamage(int damageAmount)
	{
		if (damageAmount <= 0)
		{
			return;
		}

		mHealth -= damageAmount;
	}

private:
	int mHealth = 100;
};
```

`else`는 앞 블록의 닫는 중괄호 다음 줄에 배치한다. `else if`는 같은 줄에 쓴다. `for`·`while`·`do`의 본문에도 중괄호를 사용한다. `do`의 마지막 `while`은 닫는 중괄호 다음 줄에 둔다.

```cpp
int GetDirection(bool movesForward)
{
	if (movesForward)
	{
		return 1;
	}
	else
	{
		return -1;
	}
}
```

`if (movesForward) return 1;`은 문법적으로 유효하지만 이 문서의 스타일 위반이다. 초기화 목록의 `{}`는 블록이 아니므로 [초기화 규칙](initialization.md)의 예제처럼 같은 줄에 쓸 수 있다.

## 공백과 선언

- `if (`·`for (`처럼 제어문 키워드 다음에는 공백 하나를 둔다. 함수 호출은 `GetHealth()`처럼 이름과 괄호를 붙인다.
- 괄호 안쪽에 불필요한 공백을 넣지 않는다. 쉼표 뒤에는 공백 하나를 둔다.
- 대입·산술·비교·논리 이항 연산자 양옆에는 공백 하나를 둔다. 단항 연산자는 `!isReady`, `++count`, `*value`처럼 피연산자에 붙인다.
- 선언의 `*`, `&`, `&&`는 타입에 붙인다. 주소 연산자 `&value` 등 표현식에는 이 선언 규칙을 적용하지 않는다.
- 변수마다 선언을 분리한다. `int* first, second;`처럼 두 변수가 같은 타입으로 오해될 수 있는 표기를 피한다.
- 여러 선언의 이름이나 `=`를 세로로 맞추기 위해 공백을 추가하지 않는다. 한 이름을 바꿀 때 주변 줄까지 수정되는 일을 줄인다.

```cpp
int count = 0;
int* first = nullptr;
int* second = nullptr;
bool isReady = count > 0;
```

## 긴 줄과 함수 인자

인자가 4개 이상이거나, 한 줄이 100열을 넘거나, 복잡한 템플릿 타입이 둘 이상 포함되면 줄바꿈을 권장한다. 짧고 의미가 명확한 한 줄은 유지할 수 있다.

**필수:** 인자 목록을 여러 줄로 나누기로 했다면 모든 인자를 새 줄에 하나씩 배치하고 탭 한 단계 들여쓴다. 닫는 소괄호 `)`는 마지막 인자 바로 뒤에 붙인다. 함수 선언·정의의 매개변수 목록에도 같은 규칙을 적용한다.

```cpp
void SetViewport(
	int positionX,
	int positionY,
	int width,
	int height);
```

함수 정의도 마지막 매개변수 뒤에 `)`를 붙인다. 뒤에 필요한 `const`, `noexcept`, 후행 반환 타입 등은 이어서 작성하고, 함수 선언부가 끝난 다음 줄에 여는 중괄호를 둔다. 생성자는 [멤버 초기화 목록](initialization.md#멤버의-기본값과-생성자-입력을-구분한다)을 작성한 뒤 여는 중괄호를 둔다. `)`만을 위한 줄이나 본문 직전의 빈 줄을 추가하지 않는다.

```cpp
int AddValues(
	int first,
	int second)
{
	return first + second;
}

int result = AddValues(
	1,
	2);
```

URL, 분리하면 의미가 변하는 문자열, 긴 include 경로는 100열 기준의 예외로 둔다. 문자열 내용 자체를 포맷을 위해 바꾸지 않는다.

## 적용 범위와 미결정 사항

- 외부 라이브러리·자동 생성 코드는 원래 포맷을 유지한다.
- 기존 프로젝트를 수정할 때는 프로젝트의 명시적 포맷 규칙을 우선한다. 이 문서 추가만으로 기존 소스 전체를 재포맷하지 않는다.
- `switch` 레이블, 짧은 람다, 복잡한 템플릿 배치는 후속 정리 대상이다.
- `.clang-format` 설정은 도구 버전과 설정 작업 범위를 정할 때 추가한다.

## 근거와 출처

기존 [DevMiniEngine 컨벤션](../../../ref/CodingConvention.md)의 코드 스타일 및 [정리본](../../../ref/DevRnimanConvention/CodingConvention.md)의 함수 인자 정렬을 참고했다. 포인터 표기는 유지하고 참조에도 일관되게 확장했다. 공백·빈 줄·한 선언당 변수 하나는 이 문서에서 명시한 규칙이다.

Google의 포맷 규칙을 비교 자료로 참고했다. Google은 공백 2칸·80자·같은 줄 여는 중괄호를 사용한다. 이 문서는 사용자 선택인 탭 문자·표시 너비 4칸과 함께 100열 권장·다음 줄 중괄호를 사용한다. 인자를 새 줄에 하나씩 쓰는 기존 방식은 유지하되, 닫는 소괄호는 사용자 선택에 따라 마지막 인자 뒤에 붙이도록 변경했다. 특정 회사의 포맷이 C++의 필수 문법이라는 뜻은 아니다.

- [Google C++ Style Guide — Formatting](https://google.github.io/styleguide/cppguide.html#Formatting)
- [Google C++ Style Guide — Spaces vs. Tabs](https://google.github.io/styleguide/cppguide.html#Spaces_vs._Tabs)
- [Google C++ Style Guide — Function Calls](https://google.github.io/styleguide/cppguide.html#Function_Calls)
- [EditorConfig — 인코딩·줄바꿈·파일 끝 개행 속성](https://editorconfig.org/#supported-properties)

출처 확인일: 2026-09-09.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.
