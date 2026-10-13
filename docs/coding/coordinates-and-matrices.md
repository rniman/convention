# 좌표축과 행렬 규약

[코딩 목차](index.md)

상태: 채택 · 작성·채택일: 2026-10-13 · 적용 범위: 직접 작성하는 코드의 좌표축 선택·기록과 DirectXMath↔HLSL Constant Buffer 행렬 전달

좌표축·좌·우수성·벡터 곱셈 방향·저장 순서를 구분하고 CPU와 셰이더가 같은 행렬을 해석하도록 계약을 맞춘다. 좌표축 선택, 행렬 전달의 기본 규칙과 예외를 각각 아래 절에서 정의한다.

언어·API 특성과 개인 규칙을 구분한다. 기본 규칙과 [좌표축의 프로젝트별 기준](#좌표축의-프로젝트별-기준)의 필수·권장·선택은 채택 강도다. 기본 배열 설명은 C11·C++20 기준, C++ 예제는 C++11 이상·DirectXMath, HLSL 예제는 FXC·Shader Model 5.0 기준이다. 다른 버전·플랫폼·버퍼 형식은 해당 계약을 확인한다.

## 구분해서 정할 항목

| 항목 | 의미 | 정할 내용 |
| --- | --- | --- |
| 좌표 공간·축 | 값이 속한 공간과 축의 의미 | 로컬·월드·뷰·클립·화면, 위쪽·정면 방향 |
| 좌·우수성 | 세 축이 이루는 방향 관계 | 왼손 또는 오른손, View·Projection의 일치 |
| 벡터 연산 | 벡터를 행렬의 어느 쪽에 놓는가 | 행 벡터 `p * M` 또는 열 벡터 `M * p` |
| 저장 순서 | 논리적 행렬을 메모리에 나열하는 순서 | 행 우선 `row-major` 또는 열 우선 `column-major` |
| 전달 형식 | CPU와 셰이더가 같은 바이트를 어떻게 해석하는가 | 필드 순서·offset·stride·패킹·전치 위치 |

**필수:** 위 항목을 프로젝트의 좌표·렌더 데이터 계약에 따로 기록한다. `row_major`가 왼손 좌표계나 행 벡터를 강제한다고 해석하지 않는다. 공간 접미어의 상세 정의는 [HLSL 좌표 공간](hlsl.md#좌표-공간)을 따른다.

## 언어와 API의 기본 동작

### C·C++의 배열

**언어 특성:** 기본 다차원 배열 `float values[2][3]`은 배열의 배열이며 마지막 첨자가 가장 빠르게 변하는 행 우선 배치다. 첫 첨자를 행, 둘째를 열로 해석하면 다음과 같다. 이는 선택 가능한 컴파일러 기본값이 아니라 기본 배열의 저장 규칙이다.

```text
논리적 행렬:       행 우선 저장: 1, 2, 3, 4, 5, 6
1 2 3             열 우선 저장: 1, 4, 2, 5, 3, 6
4 5 6
```

이 설명을 모든 C·C++ 행렬 타입으로 확대하지 않는다. `float* rows[2]`는 포인터 배열이고 각 행이 연속한다는 보장이 없다. 사용자 정의 타입·수학 라이브러리는 자체 저장 순서와 접근 규약을 가질 수 있다. `values[row][column]`처럼 인덱스 의미도 확인한다.

### DirectXMath와 HLSL

| 대상 | 기본·고정 동작 | 주의점 |
| --- | --- | --- |
| DirectXMath | 행 우선 행렬, 행 벡터, `p * M` | 좌·우수성은 `LH`·`RH` 함수 선택과 구분 |
| `XMStoreFloat4x4` | `XMFLOAT4X4`에 행 우선 저장 | 저장 함수가 자동으로 전치하지 않음 |
| HLSL uniform 행렬 | 별도 지정이 없으면 열 우선 패킹 | 선언·pragma·컴파일 옵션으로 변경 가능 |
| HLSL `mul(p, M)` | 첫 번째 벡터를 행 벡터로 해석 | `row_major` 여부와 독립 |
| HLSL `mul(M, p)` | 두 번째 벡터를 열 벡터로 해석 | 동일한 논리적 행렬에서 인자만 바꾸면 일반적으로 다른 변환 |
| HLSL 행렬 생성·접근 | 생성자 값은 행 순서, `M[row][column]` | `column_major`도 생성자·인덱스 의미를 뒤집지 않음 |

HLSL의 행·열 우선은 여기서 **Constant Buffer에 전달되는 행렬의 패킹**을 뜻한다. 셰이더 지역 행렬의 물리적 레지스터 배치나 모든 GPU 메모리 형식을 일괄 지정하는 규칙으로 해석하지 않는다.

<span id="directxmathhlsl의-기본안"></span>

## DirectXMath↔HLSL의 기본 규칙

적용 범위: DirectXMath로 계산·저장한 행렬을 HLSL Constant Buffer에 전달하는 개인 코드. 기존 프로젝트는 변경 범위부터 적용하며 외부 계약·성능 예외는 아래 기준을 따른다.

| 대상 | 규칙 | 강도·이유 |
| --- | --- | --- |
| CPU 계산 | DirectXMath의 행 벡터 규약 유지 | 권장. 라이브러리의 기존 계약과 일치 |
| CPU 저장 | `XMStoreFloat4x4`로 행 우선 저장 | 권장. 계산 타입과 전달 타입을 구분 |
| HLSL 경계 선언 | 전달받는 행렬마다 `row_major` 명시 | 필수. 소스에서 CPU↔셰이더 계약을 확인 가능 |
| 위치 변환 | `mul(position, matrix)` | 필수. 기본 규칙의 행 벡터 규약과 일치 |
| 합성 | World = `S * R * T`, WVP = `World * View * Projection` | 필수. 크기 → 회전 → 이동, 월드 → 뷰 → 클립 순서 |
| 전달 | 패킹을 맞추기 위한 추가 전치 없이 복사 | 필수. CPU·HLSL이 동일한 논리적 행렬을 읽음 |
| 레이아웃 확인 | 크기·필드 offset·행렬/배열 stride 확인 | 필수. 행 우선 선언만으로 전체 구조체 호환성이 보장되지는 않음 |

`S * R * T`는 위 순서의 Transform을 구성할 때의 규칙이며 다른 변환 순서를 금지하지 않는다. 부모 계층·피벗·추가 변환이 있으면 합성 순서를 별도로 명시한다. C에서 다른 수학 구현을 사용할 때는 이 C++ API 표기를 그대로 적용하지 않고 동일한 계약 여부를 확인한다.

### 대응 예제

CPU는 다음과 같이 WVP를 계산·저장한다. 예제는 WVP 하나의 전달 형식만 보여준다.

```cpp
#include <DirectXMath.h>

struct ObjectConstants
{
	DirectX::XMFLOAT4X4 worldViewProjection;
};

static_assert(sizeof(ObjectConstants) == 64, "WVP payload must occupy 64 bytes");

ObjectConstants CreateObjectConstants(
	const DirectX::XMMATRIX& world,
	const DirectX::XMMATRIX& view,
	const DirectX::XMMATRIX& projection)
{
	ObjectConstants constants{};
	const auto worldViewProjection = world * view * projection;
	DirectX::XMStoreFloat4x4(&constants.worldViewProjection, worldViewProjection);
	return constants;
}
```

대응하는 VS는 아래처럼 선언한다. CPU 데이터는 위 구조체의 바이트 표현으로 업로드한다. 업로드·바인딩·D3D12 CBV 정렬과 자원 수명은 프로젝트의 별도 계약이다. 행렬의 64바이트 크기와 D3D12 상수 영역의 256바이트 정렬을 같은 기준으로 취급하지 않는다.

```hlsl
cbuffer ObjectConstants : register(b0)
{
	row_major float4x4 worldViewProjection;
};

float4 Main(float3 position : POSITION) : SV_Position
{
	return mul(float4(position, 1.0f), worldViewProjection);
}
```

행 벡터의 이동 행렬은 이동량을 마지막 **행**에 둔다. 이는 벡터 연산 규약에 따른 것이며 메모리 저장 순서만으로 정해지지 않는다.

```text
T = 1  0  0  0
    0  1  0  0
    0  0  1  0
    5  6  7  1

[1, 2, 3, 1] * T = [6, 8, 10, 1]
```

### 전치의 목적과 예외

**필수:** 저장 순서를 맞추는 전치와 변환 자체에 필요한 전치를 구분한다. 비균일 Scale의 법선 변환에서 사용하는 World 역전치는 수학적 변환이다. 역전치로 계산한 법선 행렬도 행 우선으로 저장·선언하며, 전달용 전치를 추가하지 않는다. 특이 행렬·반전 Transform 등의 허용 범위는 프로젝트에서 정한다.

| CPU에 준비한 데이터 | HLSL 선언 | 셰이더 연산 | 행 벡터 기본 규칙과의 관계 |
| --- | --- | --- | --- |
| `M`의 행 우선 데이터 | `row_major` | `mul(p, M)` | 기본 규칙. 추가 전치 없음 |
| `M`을 전치한 뒤 행 우선 저장 | `column_major` | `mul(p, M)` | 동일한 논리적 `M`을 전달하는 대안 |
| `M`의 행 우선 데이터 | 기본 `column_major` | `mul(p, M)` | 4×4에서는 셰이더가 `M`의 전치를 읽어 일반적으로 잘못된 결과 |
| `M`을 전치한 뒤 행 우선 저장 | `row_major` | `mul(p, M)` | 불필요한 전치로 일반적으로 잘못된 결과 |

**선택:** 외부 셰이더·라이브러리가 열 우선 전달이나 열 벡터 연산을 요구하면 그 계약을 유지한다. 변환 위치·책임·적용 대상을 경계에 기록하고 검증한다. 위 표의 전치 대안은 4×4 패킹 예시이며 비정방 행렬·다른 버퍼 형식에 동일한 복사 방식을 가정하지 않는다. 곱셈 인자 순서만 바꿔 저장 불일치를 보정하는 방식을 기본으로 쓰지 않는다.

`#pragma pack_matrix(row_major)`나 FXC `/Zpr`로 전체 기본값을 바꾸는 방식은 프로젝트가 선택·문서화한 경우의 대안이다. 외부 include와 다른 빌드 구성에 미치는 영향을 확인하는 것은 **권장**이다. 도구 설정 변경과 기존 선언의 일괄 변경은 요청된 프로젝트 작업 범위에서 수행한다.

### 성능 문제가 관측된 경우

**선택:** 행렬 전달·셰이더 연산에 관련된 성능 문제가 실제로 관측되면 `column_major` 전달로 전환할 수 있다. 대상 GPU·컴파일러·프로파일·실제 부하에서 두 방식을 비교하고 CPU의 전달용 전치·업로드 비용과 GPU 연산 비용을 함께 확인한다. 개선과 변환 결과의 정확성을 검증한 뒤 대상·이유·측정 조건·전달 규약을 프로젝트 예외로 기록한다. 행 우선이 열 우선보다 항상 빠르거나 GPU 연산량이 반드시 감소한다고 가정하지 않는다.

**필수:** 열 우선 저장으로 전환할 때 CPU의 전달 형식과 HLSL 선언을 함께 맞춘다. 저장 순서 변경만으로 행 벡터 연산까지 변경할 필요는 없다. 4×4에서는 위 표처럼 CPU에서 전달용 전치를 하고 `column_major`·`mul(position, matrix)`를 유지할 수 있다. 셰이더 선언만 바꾸거나 기존 전치와 새 전치를 중복 적용하지 않는다. 비정방 행렬·배열의 stride와 법선용 역전치도 각각 확인한다.

## 좌표축의 프로젝트별 기준

적용 범위: 이 위키를 사용하는 프로젝트의 좌표축 선택·기록.

**권장:** 해당 공간을 정의하는 엔진·API의 문서화된 기본 규약을 따른다. 월드·로컬 공간은 사용 중인 엔진의 기본 축·좌·우수성을 우선하고, 뷰·클립·화면 공간은 엔진 규약과 API의 필수 입출력 조건을 함께 맞춘다. 두 규약이 다르면 경계에서 명시적으로 변환한다. 모든 엔진에 하나의 월드 축을 강제하지 않는다.

**필수:** 월드의 위쪽 축, 로컬 오브젝트의 정면 축, 뷰의 앞쪽 방향과 View·Projection의 좌·우수성을 기록한다. 월드 `+Z`와 현재 카메라의 전방 벡터를 같은 값으로 취급하지 않는다. 카메라 회전은 월드 축을 바꾸지 않는다.

**권장:** View·Projection에 같은 좌·우수 규약을 사용하고 값이 속한 공간과 변환 결과를 확인한다. 축·좌·우수성 변환과 행렬 패킹용 전치는 별개다. 앞면 winding·컬링·UV·깊이 범위도 필요한 인터페이스에서 확인하며 `row_major`나 `LH`라는 이름으로 추정하지 않는다.

**필수:** 기본 규약이 없거나 선택 가능한 경우 프로젝트에서 정하고 기록한다. 현대 Direct3D는 왼손 좌표계를 강제하지 않고 DirectXMath도 `LH`·`RH`를 제공하므로, 이 API들만으로 월드의 위쪽·로컬 정면·좌·우수성이 하나로 정해진다고 가정하지 않는다. 자체 엔진은 기존 규약이 있으면 유지하고, 없는 부분만 프로젝트에서 정한다. RnimanEngine의 구체적인 확인 범위는 [프로젝트 기록](../projects/rniman-engine.md#좌표축과-행렬-전달의-확인)에 둔다.

**선택:** 엔진 기본 규약과 다른 축이 필요하면 프로젝트 제약·이유·변환 경계를 예외로 기록한다.

### 거리 단위와 외부 에셋 변환의 관리 범위

거리 단위와 외부 에셋 변환의 상세 규약은 **프로젝트·에셋별로 관리**하고 공용 컨벤션에서 고정하지 않는다. 표현이 다를 수 있으므로 단위·크기, 로컬 정면·축의 대응, 변환 방식·수행 위치는 해당 프로젝트와 에셋의 계약을 따른다. 이는 사용자 선택으로 확정한 관리 범위이며 공통 미결정·후속 채택 항목이 아니다.

## 검증 기준

- **필수:** 비대칭 행렬이나 이동 변환으로 CPU·셰이더의 대응을 확인한다. 항등행렬·대칭 행렬만으로는 전치 오류를 구분할 수 없다. 위 이동 예제는 `[6, 8, 10, 1]`이 나와야 한다.
- **필수:** HLSL을 대상 프로파일로 컴파일하고 reflection 또는 어셈블리 출력으로 행렬의 패킹·필드 offset·크기를 확인한다. CPU의 `sizeof`·`offsetof` 확인과 셰이더 확인은 서로 대체하지 않는다.
- **권장:** 실제 렌더 경로에서 이동·회전·비균일 Scale과 법선 결과를 확인한다. CPU 계산·셰이더 컴파일만 통과했다면 GPU 전달·화면 확인까지 완료했다고 기록하지 않는다.
- **필수:** `float3x3`·비정방 행렬·배열은 패딩·stride를 별도로 확인한다. 기본 배열의 촘촘한 저장과 HLSL Constant Buffer 패킹은 같지 않을 수 있다.

초안 작성 시 검증(2026-10-13): 위 C++ 예제를 MSVC x64·C++20·`/W4 /WX`로 컴파일·실행하여 이동 결과 `[6, 8, 10, 1]`, 크기 적용 후 이동 결과 `[7, 12, 19, 1]`과 마지막 행의 이동량 저장을 확인했다. HLSL 예제는 Windows SDK 10.0.26100.0의 FXC·`vs_5_0`·`/WX`로 컴파일하고 출력에서 `row_major`·offset 0·64바이트를 확인했다. 사이트 strict 빌드도 통과했다. 예제의 실제 GPU 업로드·실행 결과는 이번 검증 범위에 포함하지 않는다.

<span id="상태와-미결정-사항"></span>
<span id="상태와-후속-범위"></span>

## 후속 범위

DXC·SM6·SPIR-V와 StructuredBuffer·ByteAddressBuffer의 상세 레이아웃은 **후속 범위**다. 현재 FXC·SM5.0 Constant Buffer의 검토 결과를 자동 적용하지 않는다. 보류·폐기로 결정한 안은 없다.

## 근거와 출처

`ref/`의 [과거 컨벤션](../../ref/CodingConvention.md), [정리본](../../ref/DevRnimanConvention/CodingConvention.md), [별도 정리본](../../ref/DevRnimanConvention/Code_Convention_Kor.md), [DX12 자료](../../ref/gameConvention/%5BDX12%5D%20coding%20convention%2825.10.04%29.md)를 확인했다. 행렬·좌표 예시는 있지만 저장·곱셈·축을 통일한 기존 채택 근거는 확인하지 못했다. 이번 사용자 선택과 [RnimanEngine의 현재 구현](../projects/rniman-engine.md#좌표축과-행렬-전달의-확인)을 채택 근거로 사용한다.

행렬 규칙의 채택 이유는 CPU↔HLSL 해석을 맞추고 전달용 전치 위치의 혼동을 줄이기 위해서다. 좌표축은 엔진·API의 기존 규약과 호환되도록 선택하고, 표현이 다양한 거리 단위·외부 에셋 변환은 프로젝트·에셋별 계약으로 관리한다.

공식 자료 확인일: **2026-10-13**. 언어 기준은 C11 위원회 초안 N1570·C++20 초안 N4861, API 검토 범위는 DirectXMath·Windows SDK 10.0.26100.0과 FXC·SM5.0이다. HLSL 언어 버전의 별도 고정은 하지 않는다. 공식 문서는 동작·호환 조건을 설명하며, 선언별 `row_major`를 개인 기본안으로 강제하는 스타일 가이드는 아니다.

- [C11 N1570 — §6.5.2.1 Array subscripting](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf#page=98): 마지막 첨자가 가장 빠르게 변하는 행 우선 배열.
- [C++20 N4861 — 배열 선언 [dcl.array]](https://timsong-cpp.github.io/cppwp/n4861/dcl.array#6): 연속된 배열 요소와 다차원 배열의 배열 구조. C++ 표준 초안의 해당 절 열람본.
- [DirectXMath — Matrix convention](https://learn.microsoft.com/en-us/windows/win32/dxmath/pg-xnamath-getting-started#matrix-convention): 행 우선·행 벡터와 `LH`·`RH` 선택.
- [XMStoreFloat4x4 — Remarks](https://learn.microsoft.com/en-us/windows/win32/api/directxmath/nf-directxmath-xmstorefloat4x4#remarks): 행 우선 저장과 열 우선 전달용 전치.
- [HLSL — Matrix Ordering](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-per-component-math#matrix-ordering): 기본 열 우선 패킹, 생성자·접근·연산과의 구분.
- [HLSL mul — Parameters](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-mul#parameters): 벡터의 인자 위치에 따른 행·열 벡터 해석.
- [pack_matrix — Parameters](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-appendix-pre-pragma-pack-matrix#parameters) · [FXC — /Zpc·/Zpr](https://learn.microsoft.com/en-us/windows/win32/direct3dtools/dx-graphics-tools-fxc-syntax#zpr): 소스·컴파일 옵션으로 기본 패킹 지정.
- [HLSL Constant Buffer packing](https://learn.microsoft.com/en-us/windows/win32/direct3dhlsl/dx-graphics-hlsl-packing-rules): 필드·배열 패킹과 16바이트 경계.

## 관련 문서

- [HLSL 셰이더 규칙](hlsl.md)
- [RnimanEngine 프로젝트 기준](../projects/rniman-engine.md)
- [변경 검증과 결과 기록](../quality/verification.md)

## 변경 기록

### 2026-10-13

- 좌표축 선택과 DirectXMath ↔ HLSL 행렬 전달 규칙을 작성하고 사용자 선택으로 채택했다. 측정·정확성 검증을 거친 성능 예외와 프로젝트·에셋별 관리 범위를 구분했다.
- 기본 배열·패킹·전치의 설명과 대응 예제를 보완하고 CPU 실행·HLSL 컴파일·레이아웃 확인 결과를 기록했다. DXC·SM6·다른 버퍼 형식은 후속 범위로 남겼다.
- 반복된 채택 상태·범위 설명과 같은 날의 변경 기록을 정리했다. 규칙 강도·예외·기존 절 주소와 예제 코드는 유지했다.
