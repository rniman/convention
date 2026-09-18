# HLSL 셰이더 규칙

[코딩 목차](index.md) · 관련: [C++ 명명](cpp/naming.md), [RnimanEngine 적용 상태](../projects/rniman-engine.md#hlsl-컨벤션-적용-상태)

상태: 초안 · 작성일: 2026-09-18 · 적용 범위: 직접 작성하는 HLSL의 명명·파일 구성·컴파일 입출력 식별

단계별 파일에서 역할을 구분하고 진입점 이름을 단순하게 유지한다. 아래 `필수`·`권장`·`선택`은 채택 시의 제안 강도다. C·C++ 규칙을 HLSL에 일괄 적용하지 않으며, 컴파일러·Shader Model·HLSL 언어 버전과 지원 플랫폼은 프로젝트에서 정한다. 기본 검토 범위는 FXC·Shader Model 5.0의 전통적인 셰이더 단계이며, DXC·SM6 전용 기능은 별도 검토한다.

## 파일과 진입점

| 대상 | 강도 | 규칙 | 예시 |
| --- | --- | --- | --- |
| 컴파일 대상 파일 | 필수 | `PascalCase` 기능명 + 대문자 단계 약어 + `.hlsl` | `TriangleVS.hlsl`, `ShadowDepthPS.hlsl` |
| 진입점 | 필수 | 단계별 파일당 컴파일 진입점 하나를 `Main`으로 지정 | `PixelInput Main(VertexInput input)` |
| 공유 include 파일 | 필수 | 역할을 나타내는 `PascalCase` 이름 + `.hlsli` | `Lighting.hlsli`, `VertexTypes.hlsli` |
| 파일 분리 | 권장 | 단계별 `.hlsl` 분리를 기본으로 유지 | VS와 PS를 각각 컴파일 |

단계 약어는 `VS` = Vertex Shader, `PS` = Pixel Shader, `CS` = Compute Shader, `GS` = Geometry Shader, `HS` = Hull Shader, `DS` = Domain Shader다. 실제 사용 가능 여부는 대상 프로파일에 따른다.

`Main`은 컴파일 진입점의 이름이며 일반 함수의 동사 명명 규칙에서 제외한다. 보조 함수나 HS의 patch constant 함수까지 파일당 하나로 제한한다는 뜻은 아니다. 이름만으로 단계가 결정되지는 않으므로 빌드의 진입점·단계·프로파일을 소스와 일치시키는 것은 **필수**다.

## 식별자

| 대상 | 강도 | 표기 | 예시 |
| --- | --- | --- | --- |
| 구조체 | 필수 | `PascalCase` | `VertexInput`, `PixelInput` |
| 일반 함수 | 필수 | `PascalCase`, 동사로 동작 표현 | `ComputeLighting`, `TransformPosition` |
| 구조체 필드·매개변수·지역 변수 | 필수 | `camelCase` | `position`, `baseColor`, `input` |
| 고정 정책값·한계값 상수 | 필수 | `UPPER_SNAKE_CASE` | `MAX_LIGHT_COUNT` |
| 혼동 가능한 위치·방향·법선 | 권장 | 변수명 뒤에 좌표 공간 약어 표시 | `positionWS`, `normalVS`, `positionCS` |

상수 이름은 `static const uint MAX_LIGHT_COUNT = 16;`처럼 소스에서 고정한 값에 사용한다. 입력·계산 결과는 `const`여도 일반 변수 표기를 유지하며, CPU가 전달하는 constant buffer 값은 고정 상수로 간주하지 않는다. C++의 `constexpr` 사용 규칙은 가져오지 않는다.

기본 타입·내장 함수·시맨틱은 일반 식별자 표기 규칙의 대상이 아니다. `float4`, `mul`, `SV_Position`, `SV_Target` 등을 사용자 함수처럼 바꾸지 않는다. 사용자 정의 시맨틱도 단계 간 연결과 CPU 입력 레이아웃의 계약을 유지해야 한다.

## 좌표 공간

| 접미어 | 의미 | 예시 |
| --- | --- | --- |
| `WS` | World Space, 월드 공간 | `positionWS` |
| `VS` | View Space, 뷰 공간 | `normalVS` |
| `CS` | Clip Space, 원근 나눗셈 전 클립 공간 | `positionCS` |

파일명의 `VS`·`CS`는 셰이더 단계이고 변수명의 접미어는 좌표 공간이다. 다른 공간 약어는 필요한 시점에 정의하며, 약어만으로 행렬 저장 방식·곱셈 방향·좌표계의 handedness를 결정하지 않는다.

공간을 표시했다면 실제 값과 일치시키는 것은 **필수**다. 특히 VS 출력의 `SV_Position`은 클립 위치지만 PS 입력의 `SV_Position`은 래스터화 후 화면 좌표를 나타낸다. 두 인터페이스에서 같은 필드 이름을 공유한다는 이유로 PS 입력까지 `positionCS`로 부르지 않는다. 공유 구조체에서는 중립적인 `position`과 단계별 의미 설명을 사용하거나, 의미가 다르면 입출력 선언을 분리한다.

## 공유 선언과 빌드 산출물

- **권장:** 실제로 공유하는 선언·함수만 `.hlsli`로 추출한다. 공유 수요가 없는 단계 전용 코드를 미리 분리하지 않는다.
- **필수:** `.hlsli`는 include 용도로 사용하고 독립 컴파일 대상으로 등록하지 않는다. 공통 파일에 단계 진입점을 두지 않는다.
- **권장:** CSO의 기본 이름은 원본 파일명을 따른다. 예: `TriangleVS.hlsl` → `TriangleVS.cso`.
- **필수:** 폴더별 동명 파일, 매크로 변형, 프로파일 또는 빌드 구성이 공존하면 출력 경로·이름으로 구분한다. 서로 다른 컴파일 결과가 덮어써지지 않도록 하고 로딩 경로도 함께 맞춘다.

`.hlsli` 확장자와 출력 이름은 개인 파일 구성 규칙이다. 확장자만으로 빌드 등록 여부가 자동 결정된다고 가정하지 않는다. 이 문서는 폴더 구조나 도구 설정을 변경하라는 지시가 아니다.

## 예외와 미결정 사항

- **선택:** 프로젝트가 한 파일에 여러 단계를 묶어야 한다면 `Triangle.hlsl` 안의 `VSMain`·`PSMain` 방식을 예외로 사용할 수 있다. 이유·대상 파일·각 컴파일의 진입점과 프로파일을 프로젝트에 기록한다. 기본안과 임의로 혼용하지 않는다.
- 외부·생성 코드 및 이름을 지정하는 외부 인터페이스는 원래 계약을 유지한다.
- 전역 리소스·sampler·constant buffer의 명명과 접두어, 레지스터 배치, 매크로·include guard 정책, 행렬 규약·메모리 배치, HLSL 포맷은 미결정이다. C++의 `g`·`m`·`s` 접두어를 자동 도입하지 않는다.
- Mesh·Amplification 및 Raytracing 셰이더 라이브러리의 파일명·진입점은 후속 범위다. 여러 export를 갖는 라이브러리에 단일 `Main` 규칙을 강제하지 않는다.
- 이번 범위에 보류·폐기로 결정한 안은 없다. 위 다중 진입점 방식은 조건부 예외이며 폐기안이 아니다.

## 근거와 출처

사용자가 제시한 단계별 파일·`Main`·명명 제안을 초안으로 정리했다. 기존 [C++ 명명](cpp/naming.md)과 그 근거인 [과거 컨벤션](../../ref/CodingConvention.md), [정리본](../../ref/DevRnimanConvention/CodingConvention.md)의 타입·함수·필드 표기를 이어가되 HLSL 범위를 별도로 정의했다. 기존 자료는 C++ 대상이며 HLSL 채택 근거로 확대하지 않는다.

Microsoft 문서는 진입점·프로파일을 빌드에서 지정하는 방법과 시맨틱의 의미를 설명한다. `Main`, `PascalCase`, 단계별 파일 분리나 `.hlsli` 명명을 의무화하는 스타일 가이드는 아니다. 이 초안의 선택 이유는 파일에서 단계를 식별하고 기존 개인 명명 스타일을 유지하기 위해서다.

공식 자료 확인일: 2026-09-18. 참조 범위: Visual Studio 2022 문서 뷰(`msvc-170`)의 FXC 속성, Direct3D 10 이상 시맨틱 중 SM5.0 적용 범위. HLSL 언어 버전은 이 문서에서 고정하지 않는다.

- [HLSL 속성 — Entrypoint Name](https://learn.microsoft.com/en-us/cpp/build/reference/hlsl-property-pages?view=msvc-170#entrypoint-name): 컴파일 진입점 지정.
- [HLSL 속성 — Shader Type](https://learn.microsoft.com/en-us/cpp/build/reference/hlsl-property-pages?view=msvc-170#shader-type) · [Shader Model](https://learn.microsoft.com/en-us/cpp/build/reference/hlsl-property-pages?view=msvc-170#shader-model) · [Object File Name](https://learn.microsoft.com/en-us/cpp/build/reference/hlsl-property-pages?view=msvc-170#object-file-name): 단계·모델·출력 지정.
- [함수 선언 — Parameters](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-function-syntax#parameters): 함수 이름과 시맨틱 구분.
- [시맨틱 — Direct3D 9 VPOS and Direct3D 10 SV_Position](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-semantics#direct3d-9-vpos-and-direct3d-10-sv_position): PS 입력 위치의 의미.

## 변경 기록

- 2026-09-18: 사용자 제안을 바탕으로 명명·단계별 파일·진입점·공유 include·CSO 구분 초안을 추가했다. 좌표 공간과 PS 입력 의미, 상수의 범위 및 예외를 보완했다. 공통 채택과 엔진 코드 변경은 수행하지 않았다.
