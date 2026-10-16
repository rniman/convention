# C++ 코드 포맷 규칙

[C++ 목차](index.md)

상태: 채택 · 적용 범위: 직접 작성하는 C++ 코드의 배치와 공백 · 예제: C++11 이상 · 개정일: 2026-10-16

블록·공백·줄바꿈을 일정하게 유지하는 개인 규칙이다.

## 핵심 규칙

| 항목 | 규칙 | 강도 |
| --- | --- | --- |
| 들여쓰기 | 단계마다 탭 문자 1개, 기본 표시 너비 4칸 | 필수 |
| 블록 중괄호 | 여는 중괄호와 닫는 중괄호를 각각 독립된 줄에 배치 | 필수 |
| 제어문 본문 | 한 문장이어도 중괄호 사용 | 필수 |
| 한 줄 길이 | 표시 너비 120열을 기준으로 줄바꿈 | 권장 |
| 포인터·참조 선언 | `int* value`, `const Player& player`처럼 타입에 붙임 | 필수 |
| 선언 | 한 선언에 변수 하나 | 필수 |
| 빈 줄 | 논리적 단계 사이에 한 줄 | 권장 |
| 줄 끝 | 불필요한 공백 제거, 파일 끝 개행 유지 | 필수 |
| 줄바꿈 형식 | LF (`\n`) | 필수 |
| 인코딩 | UTF-8, BOM 없음 | 필수 |

Tab 키는 탭 문자를 입력하도록 설정하고 줄 내부 구분에는 공백을 사용한다. 열 너비는 탭을 4칸으로 표시해 판단한다.

## 파일 인코딩과 줄바꿈

UTF-8·LF는 도구 간 파일 형식을 맞추기 위한 개인 선택이다.

- 같은 파일에 LF와 CRLF를 혼용하지 않는다.
- 줄 끝의 불필요한 공백·탭은 제거한다. 문자열 내용처럼 의미가 있는 공백은 보존한다.
- 비어 있지 않은 파일의 마지막 줄은 LF로 끝낸다. 마지막에 별도의 빈 줄을 추가하라는 뜻은 아니다.
- 외부 도구가 CRLF나 BOM을 명시적으로 요구하는 파일은 프로젝트별 예외로 기록한다. 컴파일러도 소스 파일을 UTF-8로 읽도록 프로젝트에서 설정한다.

EditorConfig 대응값은 `charset = utf-8`, `end_of_line = lf`, `insert_final_newline = true`다. 실제 설정은 별도 작업이다.

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

제어문 본문은 한 줄로 축약하지 않는다. 초기화의 `{}`는 블록과 달리 [초기화 규칙](initialization.md)에 따라 같은 줄에 쓸 수 있다.

## 공백과 선언

- `if (`·`for (`처럼 제어문 키워드 다음에는 공백 하나를 둔다. 함수 호출은 `GetHealth()`처럼 이름과 괄호를 붙인다.
- 괄호 안쪽에 불필요한 공백을 넣지 않는다. 쉼표 뒤에는 공백 하나를 둔다.
- 대입·산술·비교·논리 이항 연산자 양옆에는 공백 하나를 둔다. 단항 연산자는 `!isReady`, `++count`, `*value`처럼 피연산자에 붙인다.
- 선언의 `*`, `&`, `&&`는 타입에 붙인다. 주소 연산자 `&value` 등 표현식에는 이 선언 규칙을 적용하지 않는다.
- `int* first, second;`처럼 서로 다른 타입을 한 선언에 묶지 않는다.
- 여러 선언의 이름·`=`를 맞추는 세로 공백 정렬은 하지 않는다.

```cpp
int count = 0;
int* first = nullptr;
int* second = nullptr;
bool isReady = count > 0;
```

## 작업 경계와 빈 줄

- **권장:** 함수 정의 사이, 서로 다른 초기화·정리 단계 사이에는 빈 줄 하나를 둔다. 멤버 선언은 소유 자원·명령·동기화 등 역할별로 묶고 그룹 사이를 구분한다.
- **필수:** 서로 다른 부수 효과가 있는 작업을 하나의 조건식에 연결하여 실행하지 않는다. 초기화 호출 여러 개를 하나의 if에 ||로 연결하는 대신 작업마다 호출·실패 처리를 분리한다.
- 단일 작업의 호출과 실패 검사는 함께 유지할 수 있다. 입력 범위 검사나 자원 존재 확인처럼 하나의 판단에 필요한 논리 조건은 함께 쓴다.
- 실패 처리 블록 이후 다음 작업에는 빈 줄을 둔다. 같은 작업의 대입문마다 기계적으로 빈 줄을 넣지 않는다.

## 긴 줄과 함수 인자

**권장:** 120열과 가독성으로 줄바꿈을 판단한다. 짧고 명확하면 한 줄을 유지하며 인자·템플릿 타입의 개수로 결정하지 않는다.

**권장:** 폭 안에서도 중첩 호출·긴 식·인자별 주석 때문에 읽기 어려우면 줄바꿈하거나 변수로 추출한다. 인자 자체의 의미는 [함수 규칙](functions.md)에 따라 드러낸다.

**필수:** 여러 줄 인자는 첫 인자부터 새 줄·탭 한 단계로 배치하고 `)`는 마지막 인자 뒤에 붙인다. 한 줄에 인자 하나가 기본이며, API 순서·의미가 분명한 행렬 행·좌표 쌍·범위는 묶을 수 있다. 폭만 맞추기 위한 임의 묶음은 피한다.

선언·정의·호출에 같은 배치 기준을 적용하되 줄바꿈 여부는 각각 판단한다.

```cpp
// 인자가 4개여도 짧고 명확하면 한 줄을 유지한다.
void SetViewport(int positionX, int positionY, int width, int height);
SetViewport(x, y, width, height);

// API가 행 단위 순서로 받는 3×3 행렬은 구조를 드러낸다.
transform.SetMatrix(
	m00, m01, m02,
	m10, m11, m12,
	m20, m21, m22);

// 별도 의미 묶음이 없는 긴 인자는 하나씩 배치한다.
CreateBuffer(
	device.Get(),
	bufferSize,
	D3D12_RESOURCE_FLAG_NONE,
	D3D12_RESOURCE_STATE_COPY_DEST);
```

`const`·`noexcept`·후행 반환 타입은 `)` 뒤에 이어 쓰고 다음 줄에 `{`를 둔다. 생성자는 [멤버 초기화 목록](initialization.md#멤버의-기본값과-생성자-입력을-구분한다) 뒤에 `{`를 둔다. `)` 단독 줄이나 본문 직전 빈 줄은 추가하지 않는다.

```cpp
void CopyTexture(
	const TextureResource& source,
	TextureResource& destination,
	const TextureCopyRegion& region)
{
	// 복사 구현 생략
}

CopyTexture(source, destination, region);
```

URL, 분리하면 의미가 변하는 문자열, 긴 include 경로는 120열 기준의 예외로 둔다. 문자열 내용 자체를 포맷을 위해 바꾸지 않는다.

## 적용 범위와 미결정 사항

- 외부 라이브러리·자동 생성 코드는 원래 포맷을 유지한다.
- 기존 프로젝트를 수정할 때는 프로젝트의 명시적 포맷 규칙을 우선한다. 이 문서 추가만으로 기존 소스 전체를 재포맷하지 않는다.
- `switch` 레이블, 짧은 람다, 복잡한 템플릿 배치는 후속 정리 대상이다.
- `.clang-format` 설정은 도구 버전과 설정 작업 범위를 정할 때 추가한다.

## 관련 문서

- [명명 규칙](naming.md)
- [초기화 규칙](initialization.md)

## 근거와 출처

기존 [DevMiniEngine 컨벤션](../../../ref/CodingConvention.md)의 코드 스타일 및 [정리본](../../../ref/DevRnimanConvention/CodingConvention.md)의 함수 인자 정렬을 참고했다. 포인터 표기는 유지하고 참조에도 일관되게 확장했다. 공백·빈 줄·한 선언당 변수 하나는 이 문서에서 명시한 규칙이다.

Google의 공백 2칸·80자·같은 줄 중괄호와 달리 탭·표시 너비 4칸·120열 권장·다음 줄 중괄호를 채택했다.

Function Calls의 의미별 묶음을 참고하되 첫 인자 새 줄·마지막 인자 뒤 `)`는 개인 스타일이다. 긴 타입 이름과 불필요한 세로 확장을 고려해 120열·개수 제한 없는 기준을 선택했다.

- [Google C++ Style Guide — Formatting](https://google.github.io/styleguide/cppguide.html#Formatting)
- [Google C++ Style Guide — Spaces vs. Tabs](https://google.github.io/styleguide/cppguide.html#Spaces_vs._Tabs)
- [Google C++ Style Guide — Function Calls](https://google.github.io/styleguide/cppguide.html#Function_Calls)
- [EditorConfig — 인코딩·줄바꿈·파일 끝 개행 속성](https://editorconfig.org/#supported-properties)

출처 확인일: 2026-09-09.

Function Calls 절 재확인일: 2026-09-15. 문서 버전: 별도 명세 버전이 없는 온라인 가이드의 확인일 기준 내용.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.

## 변경 기록

- 2026-10-16: 반복 설명·중복 예시·배경을 줄여 핵심 규칙과 예시 중심으로 정리했다. 규칙 강도·예외·버전과 채택·초안·미결정 상태는 유지했다.

- 2026-09-15: 작업별 실패 처리 분리, 논리적 경계의 빈 줄과 여러 줄 인자의 의미 단위 묶음을 구체화했다. 이후 사용자 선택으로 줄 길이 권장을 100열에서 120열로 개정하고 인자·템플릿 타입 개수 기준을 제거했다. 행렬·좌표·범위의 의미 단위 배치, 선언·정의·호출별 판단과 예제를 보완했으며 기존 탭·괄호 스타일은 유지했다. 개정 전 다른 폭의 시험 적용은 프로젝트 기록과 구분한다.
