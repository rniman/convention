# RnimanEngine 프로젝트 기준

[프로젝트별 목차](index.md)

상태: 참조 초안(초기 구현·프레임 동기화만 프로젝트 한정 채택하며 나머지는 시험 적용·확인 기록) · 정리일: 2026-10-13

D3D12 미니 게임 엔진의 전용 기준·제약과 적용 상태를 요약한다. 대상은 Windows·MSVC·C++20·x64의 현재 Sandbox와 관련 Smoke 테스트다. 구현·빌드·실행·검증 상세는 비공개 프로젝트 저장소에서 관리한다.

## 주요 문서

| 원본 | 내용 |
| --- | --- |
| [README](https://github.com/rniman/RnimanEngine/blob/main/README.md) | 현재 기능·빌드·실행 |
| [개발 설정과 검증](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md) | 컨벤션 적용·검증 결과·남은 제약 |
| [엔진 설계](https://github.com/rniman/RnimanEngine/blob/main/docs/design.md) | 책임·수명·데이터 경계 |
| [프로젝트 구조](https://github.com/rniman/RnimanEngine/blob/main/docs/project-structure.md) | 출력·에셋·셰이더 배치 |

## 컨벤션 적용 상태

공통 기준은 [현재 채택 규칙](../baseline.md)이며 프로젝트 작업과 위키 정비는 [위키의 적용과 프로젝트 근거 검토](../baseline.md#위키의-적용과-프로젝트-근거-검토)를 따른다. 공통 규칙의 상세 정의는 해당 문서에 둔다.

2026-10-10 대조에서 아래 전용 기준은 현재 Sandbox의 책임·수명·빌드 구조와 부합했다. 작은 고정 메시·단일 Queue·창 하나를 전제로 한 시험 적용은 그 범위에서 유지하며, 새 소비자나 기능을 도입할 때 재검토한다. 이 적합성 확인으로 규칙을 추가 채택하거나 엔진 전체 적용·검증을 완료한 것으로 기록하지 않는다.

## 프로젝트 제약과 전용 기준

아래는 현재 프로젝트 설정과 예외의 확인 기록이다. 도구 버전·명령·출력 경로의 상세는 [개발 설정](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#프로젝트-설정)에서 관리한다.

| 대상 | 현재 기준·제약 | 이유·예외 |
| --- | --- | --- |
| 환경·출력 | Windows·MSVC·C++20·x64, 프로젝트·빌드 구성별 출력 분리 | 현재 D3D12 실행 환경과 산출물 구분에 맞춤 |
| PCH·헤더 | Sandbox 구현 파일은 PCH를 먼저 포함하며 두 Smoke는 PCH 없이 구현을 컴파일 | 프로젝트의 PCH 요구에 따른 첫 include 예외. [헤더 독립성·직접 include](../coding/cpp/headers.md)는 유지 |
| 파일 형식 | C++ 소스는 [UTF-8·LF](../coding/cpp/formatting.md), Windows 명령 스크립트는 CRLF | 스크립트의 Windows 도구 사용을 위한 파일 형식 예외 |

## 소스 배치와 탐색 구조의 검토

상태: **확인 기록과 재배치 초안** · 확인일: 2026-10-14 · 대상: 원격 `main`의 구조 문서·Sandbox 프로젝트·필터·두 Smoke 프로젝트. 코드를 실행하거나 로컬 Visual Studio 표시를 확인한 것은 아니다.

[구조 문서](https://github.com/rniman/RnimanEngine/blob/main/docs/project-structure.md#현재-프로젝트와-코드)와 [Sandbox 빌드 입력](https://github.com/rniman/RnimanEngine/blob/main/Sandbox/Sandbox.vcxproj)을 대조했다. 앱·창·렌더러·자원 로딩·변환의 소스와 헤더가 `Sandbox/` 바로 아래에 있으며, [필터 파일](https://github.com/rniman/RnimanEngine/blob/main/Sandbox/Sandbox.vcxproj.filters)은 파일 항목만 나열하고 기능별 `Filter`를 정의하지 않는다. 단일 프로젝트라는 점과 실제 파일·표시가 평면 배치라는 점을 구분한다.

[RendererSmoke](https://github.com/rniman/RnimanEngine/blob/main/Tests/RendererSmoke.vcxproj)는 Sandbox의 `D3D12Renderer.cpp`·`AssetLoader.cpp`를, [WindowSmoke](https://github.com/rniman/RnimanEngine/blob/main/Tests/WindowSmoke.vcxproj)는 `Win32Window.cpp`를 직접 빌드한다. 두 테스트의 include 기준도 현재 `Sandbox/`다. 폴더 이동만으로도 이 참조 경로를 함께 갱신해야 한다. Sandbox는 PCH 생성·사용 설정을 유지하며 테스트는 PCH 없이 컴파일하는 현재 차이를 보존해야 한다.

### 기능별 배치 후보

후보 개정일: 2026-10-16. 아래는 [공통 프로젝트 구조·파일 배치 규칙](../coding/cpp/project-structure.md)의 프로젝트 바로 아래 주제별 배치를 구체화한 **프로젝트 전용 후보**다. 실제 재배치 결과가 아니며 개별 기능 폴더의 이름·경로·책임 경계는 미결정이다. 헤더와 대응 구현 파일을 함께 두고 필터에도 같은 기능 분류를 표시하는 방향을 제안한다.

| 후보 위치 | 대상 | 분류 이유·재검토 조건 |
| --- | --- | --- |
| `Sandbox/Main.cpp` | 기존 `Main.cpp` | 실행 진입점의 현재 위치 유지 |
| `Sandbox/App/` | `SandboxApp.h/.cpp`, `SandboxCamera.h`, `SandboxLighting.h` | 데모 실행·입력 해석·카메라·조명 상태. 범용 엔진 기능으로 바뀌면 다시 분류 |
| `Sandbox/Platform/` | `Win32Window.h/.cpp` | Win32 창·메시지·입력 수집 |
| `Sandbox/Assets/` | `AssetLoader.h/.cpp`, `ImageData.h` | CPU 이미지 로딩·표현. 저장소 루트의 원본 에셋 `Assets/`와 코드 폴더를 경로로 구분 |
| `Sandbox/Rendering/` | `D3D12Renderer.h/.cpp`, `RenderData.h` | GPU 렌더링과 렌더 입력 계약. D3D12 외 구현을 도입하면 API 전용 하위 분류 검토 |
| `Sandbox/Math/` | `Transform.h` | 변환 수학. 렌더링 전용 계약인지 공용 수학인지 실제 사용 범위로 재검토 |
| 기존 `Sandbox/` | `pch.h/.cpp`, `CubeShaders.props`, 프로젝트·필터 파일 | 우선 현재 PCH·빌드 설정 위치 유지. 공통 최종 위치 규칙으로 확정하지 않음 |

이 후보에서는 include 기준을 기존 `Sandbox/`로 유지하는 방향을 검토하고 PCH의 현재 위치도 유지한다. 테스트의 원본 참조·include와 소스의 include 표기를 새 기능 경로에 맞춘다. 별도 코드 루트가 필요한 이유가 생기면 `src/` 도입을 검토한다. 셰이더 공유 설정, 에셋 복사와 EXE 기준 실행 경로는 이동 영향이 있는지 확인한다. 실제 적용 시 x64 Debug·Release에서 영향받는 세 프로젝트의 빌드와 Smoke 실행·Sandbox 실행을 확인해야 한다.

원본의 [향후 확장 구조](https://github.com/rniman/RnimanEngine/blob/main/docs/project-structure.md#향후-확장-구조)는 공용 기능이 필요할 때 Engine 라이브러리를 분리하는 목표다. 이 초안은 먼저 Sandbox 내부의 물리적 배치와 필터를 정리하는 후보이며 기능 폴더별 별도 `.vcxproj`·Engine 라이브러리 전환을 확정하지 않는다. 현재 확인한 앱과 테스트의 공유만으로 공용 API 범위가 확정되지는 않는다.

### 솔루션 전체의 확장 검토

상태: **계획 대조와 초안** · 확인일: 2026-10-15. 원격 `main`의 [향후 확장 구조](https://github.com/rniman/RnimanEngine/blob/main/docs/project-structure.md#향후-확장-구조)와 [외부 라이브러리·도구](https://github.com/rniman/RnimanEngine/blob/main/docs/dependencies.md#외부-라이브러리와-도구)를 확인했다. Engine·Samples·Tools·ThirdParty 분류는 기존 확장 방향이며 외부 라이브러리 후보 표는 실제 도입 목록이 아니다.

새 [솔루션 역할별 분류 기준](../coding/cpp/project-structure.md#솔루션의-프로젝트-구성)은 이 확장 방향과 함께 검토할 수 있다. 현재 루트의 Sandbox 경로·두 Smoke 배치를 유지하면서 필요할 때 솔루션 폴더로 앱·테스트를 묶을 수 있다. 실제 엔진 라이브러리·샘플·도구와 외부 빌드 타깃이 생기면 해당 역할에 연결한다. 써드파티 원본, 엔진·앱의 연동 코드와 직접 작성한 빌드 설정의 상세 기준은 [공통 규칙](../coding/cpp/project-structure.md#써드파티-원본과-연동-코드) 한곳에서 관리한다. 구체적인 분리·설치·재배치는 수행하거나 확정하지 않았다.

## 프로젝트 한정 채택과 적용

### D3D12 초기 구현 선택

상태: 2026-09-15 **Sandbox 한정 채택**. 아래는 현재 구현의 수명·실행 전제다.

| 기준 | 이유·적용 조건 |
| --- | --- |
| 앱이 창·렌더러를 각각 소유하고 렌더러를 먼저 정리 | GPU 자원을 사용하는 동안 HWND 수명을 유지 |
| 고성능 하드웨어 우선, WARP 자동 대체 없음 | 하드웨어 실행을 전제로 하며 지원 장치가 없으면 실패를 보고 |
| WM_SIZE는 크기를 기록하고 프레임 경계에서 리사이즈 | 메시지 처리와 GPU 자원 변경 시점을 분리. 최소화·0 크기에는 렌더링 중지 |

### 프레임 동기화 전환

상태: 2026-09-17 **프로젝트 한정 채택**. 초기 매 프레임 전체 대기를 슬롯별 Allocator·Fence 완료 후 재사용으로 대체했다. GPU 사용 중인 기록 메모리의 재사용을 막기 위한 기준이며 리사이즈·종료는 전체 GPU 대기를 유지한다. 제출 실패 시에도 정리를 시도한다.

두 슬롯·단일 Command List·공유 Fence/Event는 현재 Sandbox의 구현 선택이다. 다중 Queue·프레임 자원 확장 시 완료 조건을 다시 정하며 성능 향상은 측정 결과 없이 주장하지 않는다.

### 창·입력 분리의 프로젝트 적용

상태: 2026-10-06 사용자 요청에 따른 **현재 구현의 적용 기록**. `Win32Window`가 창 수명·Win32 메시지·입력 수집과 콜백 상태를 소유하고 복사·이동을 금지한다. 앱은 읽기 전용 창 상태와 프레임별 입력 복사본을 사용한다. 키 눌림은 유지하고 마우스 누적량·시간 초기화 요청만 소비한다.

창의 수집 책임과 앱의 입력 해석을 분리하기 위한 구조이며 창 하나·UI 스레드에 적용한다. 다중 창·범용 Input 계층을 도입할 때 소유자와 입력 전달 범위를 재검토한다. 상세 계약은 [창·입력 문서](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#창입력-추출-2026-10-06)를 따른다.

### 앱 실행부 분리의 프로젝트 적용

상태: 2026-10-06 사용자 요청에 따른 **현재 구현의 적용 기록**. `SandboxApp`이 초기화·메시지 루프·카메라/큐브 갱신·WVP 생성·렌더 호출을 담당하며 Main은 앱 생성·Run 호출·종료 코드 전달을 담당한다.

앱이 창·렌더러·카메라·큐브를 직접 소유한다. 창을 렌더러보다 먼저 선언하여 역순 파괴에서 GPU 자원을 HWND보다 먼저 정리하고 GPU 리사이즈는 프레임 경계에서 수행한다. Run은 한 번만 호출하며 종료 요청에서는 GPU 완료 확인 후 WM_QUIT 코드를 전달한다. 부분 실패는 RAII로 정리한다. 현재 데모 실행 수명을 한곳에 두기 위한 선택이며 범용 Application·Scene 도입 시 책임을 재검토한다. 상세는 [앱 실행부 문서](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#앱-실행부-추출-2026-10-06)를 따른다.

## Sandbox의 시험 적용

아래 선택은 **시험 적용**이며 프로젝트 한정 채택과 구분한다. 현재 적용 조건과 이유를 유지하되 범용 엔진 정책으로 확대하지 않는다.

### 자원과 실패 진단

ComPtr·렌더러 소유 Event로 자원을 관리하고 bool/API/HRESULT로 실패를 보고한다. 실패 후 진행을 중단하고 발생 위치·원인을 확인하기 위한 선택이다. 소멸 시에도 미완료 GPU 작업의 완료를 시도하지만 대기 실패 경로의 안전성을 모두 검증한 것은 아니다. 통일 오류 정책은 미결정이다.

Debug 레이어 필수, VSync·두 백 버퍼도 시험 적용이다. Debug 앱과 RendererSmoke의 진단 전제·실행 조건은 [엔진 README](https://github.com/rniman/RnimanEngine/blob/main/README.md#빌드와-실행)를 따른다.

### 큐브 출력의 시험 적용

행렬 전달·축은 아래 [확인 기록](#좌표축과-행렬-전달의-확인)을 따른다. 시계 방향 앞면·전체 창 Viewport·현재 종횡비 Projection을 사용하며 단일 Direct Queue의 D32 버퍼는 매 프레임 지우고 전체 GPU 대기 후 재생성한다.

Upload Heap에서 직접 읽는 방식은 작은 고정 큐브 메시의 초기 구현 선택이다. 범용 메시 로딩 도입 시 Default Heap 업로드를 검토한다.

### 좌표축과 행렬 전달의 확인

상태: **현재 Sandbox의 시험 적용·확인 기록** · 확인일: 2026-10-13. 공통 기준은 [좌표축과 행렬 규약](../coding/coordinates-and-matrices.md)을 따르며, 아래는 로컬 구현과 대조한 근거다.

| 대상 | 확인한 구현·범위 |
| --- | --- |
| 월드·카메라 축 | 카메라 상하는 월드 `+Y`, yaw·pitch가 0일 때 전방은 `+Z`·오른쪽은 `+X`. 현재 카메라 전방은 회전된 벡터이며 월드 `+Z`와 구분 |
| View·Projection | `XMMatrixLookToLH`·`XMMatrixPerspectiveFovLH`의 왼손 규약 사용 |
| World·WVP | 부모 없는 Transform의 `S * R * T`, `World * View * Projection` |
| CPU 저장·업로드 | `CreateRenderObject`에서 `XMStoreFloat4x4`로 저장하고 렌더러가 구조체를 그대로 복사 |
| HLSL 선언·연산 | CubeVS의 WVP·World·법선 행렬 모두 명시적 `row_major`. 위치·법선은 벡터를 첫 인자로 `mul` 호출 |
| 법선 | World 역전치를 계산한 뒤 행 우선 저장. 법선용 역전치와 패킹을 맞추기 위한 전치를 구분 |
| Constant Buffer | `RenderObject`의 192바이트 크기와 World·법선 필드의 64·128바이트 offset을 CPU에서 static_assert. 오브젝트별 영역은 256바이트 stride |
| 빌드 선언 | Windows SDK 10.0.26100.0·FXC·SM5.0·`Main`. 공유 `CubeShaders.props`에는 별도 기본 행렬 패킹 지정이 없고 소스의 각 선언으로 명시 |

거리 단위·외부 에셋의 규격은 이번 카메라·행렬 대조의 확인 범위 밖이다. 모델 가져오기·부모 Transform·다른 수학 라이브러리 도입 시 경계 규약을 재검토한다. 법선용 World는 현재 유한한 아핀 행렬·양수 행렬식·유한한 역행렬을 요구하며 반전 Transform의 컬링 보정은 제공하지 않는다.

이번 확인은 로컬 `D:/STUDY/DirectX12/RnimanEngine`의 HEAD [cee7605](https://github.com/rniman/RnimanEngine/commit/cee760528b33f0353d63580030fa21f839a74713)·미커밋 변경 없음 상태에서 수행했다. 엔진 코드·설정·적용 기록은 변경하지 않았고 원격 최신 상태·빌드·GPU 실행은 이번 확인 범위 밖이다. 위키의 채택과 프로젝트 적용 상태는 구분한다.

원본: [개발 문서 — 큐브 렌더링 계약](https://github.com/rniman/RnimanEngine/blob/cee760528b33f0353d63580030fa21f839a74713/docs/development.md#큐브-렌더링-계약) · [RenderData](https://github.com/rniman/RnimanEngine/blob/cee760528b33f0353d63580030fa21f839a74713/Sandbox/RenderData.h) · [Transform](https://github.com/rniman/RnimanEngine/blob/cee760528b33f0353d63580030fa21f839a74713/Sandbox/Transform.h) · [SandboxCamera](https://github.com/rniman/RnimanEngine/blob/cee760528b33f0353d63580030fa21f839a74713/Sandbox/SandboxCamera.h) · [CubeVS](https://github.com/rniman/RnimanEngine/blob/cee760528b33f0353d63580030fa21f839a74713/Shaders/Samples/Sandbox/CubeVS.hlsl) · [공유 셰이더 빌드](https://github.com/rniman/RnimanEngine/blob/cee760528b33f0353d63580030fa21f839a74713/Sandbox/CubeShaders.props).

### 카메라 입력과 여러 Transform의 시험 적용

앱이 카메라·부모 없는 Transform을 소유하며 S*R*T로 World를 계산한다. 포커스 해제·최소화·모달 조작 후 입력·시간 누적으로 이동하지 않도록 입력과 이동 시간을 초기화하고 긴 프레임의 이동 시간을 제한한다.

렌더러는 호출자의 WVP 목록을 보관하지 않는다. 슬롯 Fence 완료 후 오브젝트별 256바이트 상수 영역을 확장·복사하여 호출자 데이터 수명과 GPU 사용 수명을 구분한다. 빈 목록은 화면 지우기·Present만 수행한다. Transform 계층·장면 수집 도입 시 데이터 경계를 재검토한다.

### 겹침 픽셀 검증의 시험 적용

테스트 전용 friend 어댑터가 같은 draw 경로를 Present 없이 실행하고 GPU 완료 후 픽셀을 읽는다. flip-discard 이후 내용에 의존하지 않기 위한 선택이며 앱의 Present는 유지한다. 테스트 자원은 GPU 완료 후 렌더러보다 먼저 정리한다. 적용 범위는 현재 불투명 큐브의 가림 검증이며 일반 캡처 API 도입 시 별도 계약을 정한다. 비교 방법·한계는 [픽셀 검증 문서](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#겹치는-오브젝트의-픽셀-검증-2026-10-05)에 둔다.

### HLSL 컨벤션 적용 상태

[HLSL 규칙](../coding/hlsl.md)은 **공통 초안**이다. 현재 Cube 셰이더는 단계별 파일·`Main` 진입점, FXC·SM5.0, EXE 기준 CSO 로딩을 사용하며 Sandbox·RendererSmoke가 빌드 설정을 공유한다. 2026-10-13 확인에서 CubeVS의 월드 위치·법선은 `positionWS`·`normalWS`로 공간을 표시하며, 행렬 전달은 [별도 확인 기록](#좌표축과-행렬-전달의-확인)을 따른다. 작업 디렉터리에 의존하지 않도록 EXE 옆 셰이더를 함께 배포한다. 공유 HLSLI·변형별 출력은 필요 시 검토하고 SM6 도입 시 DXC 전환을 검토한다.

### 자료형과 변환 초안의 확인 상태

2026-10-06 [자료형 선택과 별칭](../coding/cpp/type-selection.md)·[타입 변환과 범위 검사](../coding/cpp/conversions.md)를 Sandbox·RendererSmoke에 제한적으로 시험 적용했다. CPU 데이터 크기와 전용 API 계약을 구분하기 위한 선택이다.

- CPU 복사 크기·span 인덱스는 `std::size_t`, D3D12·Win32 경계는 `UINT`·`UINT64`·`SIZE_T` 등 API 타입을 유지한다. 상수 영역 크기 계산에는 곱셈 전 범위 검사를 둔다.
- 자체 타입 별칭·변환 도우미는 미도입이다. 실제 반복 사용처가 생기면 검토하며 GPU 자원·뷰·CPU 크기의 범위와 장치 제한은 각각 확인한다.

## 공통 규칙의 대조 근거

아래는 이 프로젝트의 기존 적용·확인 기록이다. 공통 규칙 전문이나 별도의 엔진 전용 규칙을 추가하지 않는다.

### 코드 가독성 적용

2026-10-06 Sandbox·RendererSmoke의 지역 상수·빈 함수 본문·직접 include·API 계약 주석을 채택 규칙에 맞췄다. 초기 120열 시험 적용 이후의 기준은 [현재 포맷 규칙](../coding/cpp/formatting.md#긴-줄과-함수-인자)이다. 이번 정리에서는 C++ 14개 파일의 UTF-8·BOM 없음·LF·마지막 개행·탭 들여쓰기·후행 공백을 확인했다.

### 반환값과 attribute 확인

2026-10-09의 확인 기록과 이번 대조에서 주요 실패·종료·입력 소비 API의 `[[nodiscard]]` 및 호출부 결과 처리를 확인했다. 판단 기준은 [함수 반환값 규칙](../coding/cpp/functions.md#반환값-무시와-nodiscard)이다.

| 대상 | 확인한 상태·남은 범위 |
| --- | --- |
| `Initialize`·`Render`·`Resize`·`WaitForGpu` | 적용됨. 정상 실행·재사용의 실패 결과를 검사 |
| `PumpMessages`·`ConsumeInput` | 적용됨. 종료 코드·소비한 입력을 호출부에서 사용 |
| `GetWorld`·`GetView`·테스트의 `Capture` | 미적용 후보. 현재 호출부는 결과를 사용·검사하며 추가 적용은 후속 검토 |
| `GetHandle`·`GetState` | 미적용. 일반 Getter의 경고 실익은 개별 판단 |

`D3D12Renderer` 소멸자의 `(void)WaitForGpu();`와 Fence Event 닫기 실패의 명시적 결과 무시는 종료 정리의 예외다. 실패는 호출한 함수 내부에서 보고하며 캐스트 자체가 GPU 완료를 보장하지 않는다. `InputState`는 이름 있는 구조체 반환의 실제 사례다. [의도적인 반환값 무시](../coding/cpp/functions.md#의도적인-반환값-무시)·[복합 결과 선택](../coding/cpp/functions.md#구조체와-pairtuple의-선택)을 따르며 [attribute 문서](../coding/cpp/attributes.md)의 공통 초안 상태는 유지한다.

<span id="클래스구조체-초안의-근거"></span>

### 클래스·구조체 규칙의 근거

2026-10-09의 코드 확인과 이번 대조에서 다음 사례는 [클래스·구조체 규칙](../coding/cpp/classes.md)과 부합했다.

- `Transform`·`State`·`InputState`는 공개 데이터 묶음이며 Transform에는 계산 함수를 함께 둔다.
- `Win32Window`·`SandboxApp`은 단일 인자 생성자에 `explicit`을 사용하고 복사·이동을 금지한다. 창의 콜백 주소와 앱의 자원 수명을 유지하기 위한 선택이다.
- `D3D12Renderer`는 기본 생성자 `= default`, 사용자 선언 소멸자, 삭제된 복사 연산으로 암시적 이동도 생성되지 않는다. 현재 선언 조합을 확인한 기록이며 이동 정책을 새로 채택한 것은 아니다.
- 공개 API 뒤에 비공개 보조 함수·데이터를 배치하고 멤버 선언 순서에는 창·렌더러의 수명 의존성을 반영한다.

상속·`override`·`final`의 적용·검증 사례는 이번 근거에 없다. 생성 실패·소멸 진단·noexcept, 다형적 복제·복잡한 상속은 공통 미결정 정책이다.

### 삼각형 출력의 시험 적용

2026-09-18의 고정 삼각형·정사각형 Viewport는 2026-09-24 큐브·전체 창 Viewport로 대체했다. 당시 검증을 현재 큐브의 오류 경로 검증으로 간주하지 않는다.

### 공통 초안의 근거

[검증 결과 기록](../quality/verification.md)과 [원본과 생성물 관리](../git/artifacts.md)는 **공통 초안**이다. 이 프로젝트의 검증 구분·자원 관리 사례를 근거로 삼으며 로그·파일별 정책은 원본 저장소에 둔다.

## 미결정과 후속 검토

- **미결정:** ECS 저장 방식·Unity 데이터 규격·통일 오류 정책·DPI 정책·최소 창 크기.
- **후속 후보:** 자체 타입 별칭·변환 도우미, Transform·입력·렌더 데이터·업로드의 공통화. 실제 소비자와 반복 요구가 생길 때 검토한다.
- **남은 검증:** 실제 화면·장치 입력, 강제 실패·장치 손실, 전체 live-object 검사와 성능 측정. 상세 범위는 [엔진의 남은 검증과 제약](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#남은-검증과-제약)을 따른다.

위 미결정·후속 항목을 채택 규칙이나 완료된 적용으로 취급하지 않는다. 보류·폐기로 확정한 새 항목은 없다.

## 확인한 범위와 원본

2026-10-10 원격 `main`과 로컬 HEAD는 [c4cab22](https://github.com/rniman/RnimanEngine/commit/c4cab2274865afd8246e28c95d1703e08b2ed1f8)로 일치하며 로컬 미커밋 변경은 없었다. 로컬 Convention `30cfc1d`의 현재 기준과 코드·설정·문서를 대조했다. 엔진이 마지막 위키 확인으로 기록한 시점은 2026-10-07 `56c63fe`이며 이번 위키 정리가 엔진의 확인·적용 기록을 변경하지 않는다.

최초 원격 조사 근거는 [2026-09-15 커밋 2845efb](https://github.com/rniman/RnimanEngine/tree/2845efb4db318fbe9b1df2cdb14ed1cb01849726)다. 이번에는 엔진 코드·설정을 수정하거나 빌드·실행을 반복하지 않았다. 기존 실행 결과는 [최신 검증 기록](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#최신-검증-결과)을 따르며 원격 코드 조회를 배포 확인으로 간주하지 않는다.

## 관련 문서

- [컨벤션 적용 기준](../baseline.md)

## 변경 기록

### 2026-10-16

- 사용자 요청에 맞춰 재배치 후보를 `Sandbox/` 바로 아래의 주제별 폴더로 수정했다. `Main.cpp`·PCH의 현재 위치와 기존 include 기준을 유지하는 방향으로 예시를 맞추고 `src/`는 선택으로 남겼다. 공통 소스 배치 규칙의 채택을 반영하되 구체적인 기능 분류·API·분리 시점은 프로젝트별 결정으로 남긴다. 이는 문서의 후보 개정이며 실제 엔진 파일·설정·빌드·실행의 적용 결과가 아니다.

### 2026-10-15

- 원격 `main`의 프로젝트 확장 구조와 외부 의존성 후보의 상태를 대조하고, 솔루션 역할별 분류·써드파티 연동 관리의 공통 초안을 연결했다. 기존 계획을 실제 적용·도입으로 바꾸지 않았으며 코드·설정·패키지는 변경하지 않았다.

### 2026-10-14

- 원격 `main`의 구조·Sandbox 프로젝트·필터·두 Smoke 빌드 입력을 대조하여 실제 평면 배치와 원본 구현의 직접 참조를 기록했다. 기능별 실제 폴더·헤더와 구현의 동시 배치 후보를 초안으로 추가하고 공통 소스 배치 초안과 연결했다. 파일 이동·프로젝트 설정 변경·엔진 빌드·실행은 수행하지 않았다.

### 2026-10-13

- 로컬 좌표축·World/WVP·법선 역전치·CPU 저장·CubeVS 선언과 빌드 설정을 대조하고 [공통 채택 규칙](../coding/coordinates-and-matrices.md)으로 연결했다. 기존 시험 적용·확인 범위는 유지한다.
- 반복 설명과 같은 날의 변경 기록을 통합했다. 엔진 코드·설정·적용·실행 검증 기록은 변경하지 않았다.

### 2026-10-10

- 원격·로컬 엔진과 현재 위키를 대조하고 전용 기준의 이유·범위·재검토 조건을 정리했다.
- 공통 규칙 대조 근거를 축약하고 변경 기록을 날짜별로 묶었다. 기존 절 링크·규칙 강도와 채택·시험 적용·미결정 상태는 유지했으며 엔진 코드·설정·적용 기록은 수정하지 않았다.

### 2026-10-09

- Sandbox의 반환값·attribute·종료 정리와 클래스·구조체·복사·이동 선언을 확인하고 관련 공통 규칙·초안으로 연결했다.
- 클래스 기본 규칙의 공통 채택과 엔진 적용 상태를 구분하고 `GetWorld`·`GetView`를 nodiscard 미적용 후보로 기록했다. 엔진 코드·설정은 변경하지 않았다.

### 2026-10-06

- `Win32Window`의 창·입력 수집과 `SandboxApp`의 앱 실행·데모 갱신 분리를 반영했다. Main의 진입점 역할, 입력 소비와 창·렌더러의 소유·수명 경계를 기록했다.
- Sandbox·RendererSmoke의 채택 규칙 적용과 자료형·변환 초안의 제한된 시험 적용 범위를 정리하고 해당 초안·엔진 검증 문서로 연결했다.
- 중복 설명·작업 이력을 줄이면서 프로젝트 한정 채택·시험 적용·미적용 조건과 공통 채택 상태를 유지했다. 문서 정리 자체에서는 엔진 코드 수정이나 빌드·실행 검증을 수행하지 않았다.
