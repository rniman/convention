# RnimanEngine 프로젝트 기준

[프로젝트별 목차](index.md)

상태: 참조 초안(항목별 채택·시험 적용·확인 기록·제안 구분) · 정리일: 2026-10-16

적용 범위: Windows·MSVC·C++20·x64의 Sandbox와 관련 Smoke 테스트. 컨벤션 적용 상태·전용 규칙·예외를 정리하며 기능·실행·설계·검증 상세는 프로젝트 원본에 둔다.

## 대조 기준과 원본

확인일: 2026-10-16 · 대상: 조회 시점 원격 `main`의 최신 커밋 [087570c](https://github.com/rniman/RnimanEngine/commit/087570c7378c0d43ab3a0ad2d9c77942f6805067). 코드·설정·문서와 로컬 위키의 채택 규칙을 정적으로 대조했다.

| 원본 | 판단 근거 |
| --- | --- |
| [개발 설정과 검증](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#컨벤션) | 위키 확인·적용·예외·도구 설정 |
| [엔진 설계](https://github.com/rniman/RnimanEngine/blob/main/docs/design.md) | 소유권·수명·좌표축·렌더 데이터 계약 |
| [프로젝트 구조](https://github.com/rniman/RnimanEngine/blob/main/docs/project-structure.md) | 원본·생성물의 추적 범위와 배치 |
| [087570c의 적용 기록](https://github.com/rniman/RnimanEngine/blob/087570c7378c0d43ab3a0ad2d9c77942f6805067/docs/development.md#컨벤션) | 10월 15·16일 사용자 선택·적용·검증 |

[v0.1.0의 과거 근거](#milestone-v0-1-0)와 [검증 범위](#기존-검증-기록과-이번-확인의-구분)는 별도로 구분한다.

## 컨벤션 적용 상태

공통 기준은 [현재 채택 규칙](../baseline.md)과 [적용·근거 검토 절차](../baseline.md#위키의-적용과-프로젝트-근거-검토)를 따른다. 아래는 2026-10-16 대조 결과다.

| 기준 | 적용 상태 |
| --- | --- |
| C++ 채택 규칙 | 10월 15·16일 공개 baseline 조회 실패로 로컬 관련 문서를 임시 참고. 16일에는 명명·초기화·auto·프로젝트 구조의 채택 상태 확인 |
| 타입·명명 | [타입 명시 범위와 렌더 데이터 이름](#타입-명시와-렌더-데이터-명명)을 실제 반영 |
| 소스 배치·네임스페이스 | [평면 배치는 허용 범위](#소스-배치와-탐색-구조의-검토). 재배치는 초안, 제품 루트는 미반영·후속 결정 |
| 프로젝트 한정 채택 | 초기 구현·프레임 동기화·타입 명시·공용 PNG 원본 경로. 원본의 사용자 선택을 근거로 반영 |
| 좌표축·행렬 | [현재 코드와 공통 규약의 일치](#좌표축과-행렬-전달의-확인) 확인. CPU/GPU·FXC 패킹 검증은 v0.1.0의 과거 근거 |
| 공통 초안 | 자료형·변환·attribute·HLSL·검증·원본과 생성물은 초안 유지. WIC·sRGB·Phong 등도 공통 채택으로 확대하지 않음 |

이번 갱신은 공통 채택 범위를 늘리거나 엔진 전체 재검증을 완료한 기록이 아니다. 과거의 “미적용 항목 없음”도 당시 확인 범위의 판단이며 네임스페이스·`nodiscard` 후속 후보의 적용 완료를 뜻하지 않는다.

## 프로젝트 제약과 전용 기준

아래는 현재 프로젝트 설정과 예외의 확인 기록이다. 도구 버전·명령·출력 경로의 상세는 [개발 설정](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#프로젝트-설정)에서 관리한다.

| 대상 | 현재 기준·제약 | 이유·예외 |
| --- | --- | --- |
| 환경·출력 | Windows·MSVC·C++20·x64, 프로젝트·빌드 구성별 출력 분리 | 현재 D3D12 실행 환경과 산출물 구분에 맞춤 |
| PCH·헤더 | Sandbox 구현 파일은 PCH를 먼저 포함하며 두 Smoke는 PCH 없이 구현을 컴파일 | 프로젝트의 PCH 요구에 따른 첫 include 예외. [헤더 독립성·직접 include](../coding/cpp/headers.md)는 유지 |
| 파일 형식 | C++ 소스는 [UTF-8·LF](../coding/cpp/formatting.md), Windows 명령 스크립트는 CRLF | 스크립트의 Windows 도구 사용을 위한 파일 형식 예외 |

## 소스 배치와 탐색 구조의 검토

상태: **확인 기록과 재배치 초안** · 최초 확인일: 2026-10-14 · 재확인일: 2026-10-16

`087570c`의 [구조 문서](https://github.com/rniman/RnimanEngine/blob/main/docs/project-structure.md#현재-프로젝트와-코드)·[빌드 입력](https://github.com/rniman/RnimanEngine/blob/main/Sandbox/Sandbox.vcxproj)·[필터](https://github.com/rniman/RnimanEngine/blob/main/Sandbox/Sandbox.vcxproj.filters)에서 `Sandbox/`의 평면 배치와 기능별 `Filter` 부재를 확인했다. [공통 배치 규칙](../coding/cpp/project-structure.md#프로젝트-내부-파일-배치)은 작은 프로젝트의 평면 배치를 허용한다. 아래 재배치는 후보이며 즉시 적용 의무는 없다.

[RendererSmoke](https://github.com/rniman/RnimanEngine/blob/main/Tests/RendererSmoke.vcxproj)는 `D3D12Renderer.cpp`·`AssetLoader.cpp`, [WindowSmoke](https://github.com/rniman/RnimanEngine/blob/main/Tests/WindowSmoke.vcxproj)는 `Win32Window.cpp`를 직접 빌드한다. 두 테스트의 include 기준은 `Sandbox/`이며 PCH 없이 컴파일한다. Sandbox의 PCH 사용과 구분해 경로 변경 영향을 확인해야 한다.

주요 타입은 전역 범위에 있다. [공통 네임스페이스 권장](../coding/cpp/naming.md#네임스페이스)의 실제 제품 루트·대상 범위·도입 시점은 프로젝트별 후속 결정이다.

### 기능별 배치 후보

상태: **프로젝트 전용 초안** · 개정일: 2026-10-16. [공통 배치 규칙](../coding/cpp/project-structure.md)을 구체화한 후보이며 폴더 이름·경로·책임 경계는 미결정이다. 헤더·구현을 함께 두고 필터에도 같은 기능 분류를 표시한다.

| 후보 위치 | 대상 | 분류 이유·재검토 조건 |
| --- | --- | --- |
| `Sandbox/Main.cpp` | 기존 `Main.cpp` | 실행 진입점의 현재 위치 유지 |
| `Sandbox/App/` | `SandboxApp.h/.cpp`, `SandboxCamera.h`, `SandboxLighting.h` | 데모 실행·입력 해석·카메라·조명 상태. 범용 엔진 기능으로 바뀌면 다시 분류 |
| `Sandbox/Platform/` | `Win32Window.h/.cpp` | Win32 창·메시지·입력 수집 |
| `Sandbox/Assets/` | `AssetLoader.h/.cpp`, `ImageData.h` | CPU 이미지 로딩·표현. 저장소 루트의 원본 에셋 `Assets/`와 코드 폴더를 경로로 구분 |
| `Sandbox/Rendering/` | `D3D12Renderer.h/.cpp`, `RenderData.h` | GPU 렌더링과 렌더 입력 계약. D3D12 외 구현을 도입하면 API 전용 하위 분류 검토 |
| `Sandbox/Math/` | `Transform.h` | 변환 수학. 렌더링 전용 계약인지 공용 수학인지 실제 사용 범위로 재검토 |
| 기존 `Sandbox/` | `pch.h/.cpp`, `CubeShaders.props`, `SourcePaths.props`, 프로젝트·필터 파일 | 우선 현재 PCH·빌드 설정 위치 유지. 공통 최종 위치 규칙으로 확정하지 않음 |

적용 시 include 기준과 PCH 위치는 기존 `Sandbox/`로 유지하는 방향을 검토한다. 소스·테스트의 참조 경로와 셰이더·원본 경로 공유 설정을 맞추고 세 프로젝트의 x64 Debug·Release 빌드·Smoke·Sandbox 실행을 확인해야 한다. `src/`는 별도 코드 루트가 필요할 때 검토한다.

원본의 [Engine 라이브러리 분리 목표](https://github.com/rniman/RnimanEngine/blob/main/docs/project-structure.md#향후-확장-구조)와 이 재배치 후보는 별개다. 현재 앱·테스트의 공유만으로 공용 API나 기능별 `.vcxproj` 분리를 확정하지 않는다.

### 솔루션 전체의 확장 검토

상태: **계획 대조와 초안** · 확인일: 2026-10-15. 원본의 [확장 구조](https://github.com/rniman/RnimanEngine/blob/main/docs/project-structure.md#향후-확장-구조)와 [외부 의존성 후보](https://github.com/rniman/RnimanEngine/blob/main/docs/dependencies.md#외부-라이브러리와-도구)는 계획이며 도입 목록이 아니다.

현재 Sandbox·두 Smoke의 경로를 유지하고 필요할 때 솔루션 폴더로 묶을 수 있다. 실제 Engine·Samples·Tools·ThirdParty가 생기면 [역할별 분류](../coding/cpp/project-structure.md#솔루션의-프로젝트-구성)와 [써드파티 관리 기준](../coding/cpp/project-structure.md#써드파티-원본과-연동-코드)을 적용한다. 구체적인 분리·설치·재배치는 미확정이다.

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

상태: 2026-10-06 사용자 요청에 따른 **적용 기록**. `Win32Window`가 창 수명·메시지·입력 수집·콜백 상태를 소유하고 복사·이동을 금지한다. 앱은 읽기 전용 창 상태와 프레임별 입력 복사본을 사용한다. 키 눌림은 유지하고 마우스 누적량·시간 초기화 요청만 소비한다.

창 하나·UI 스레드의 계약이다. 다중 창·범용 Input 도입 시 소유자·전달 범위를 재검토하며 상세는 [창·입력 원본](https://github.com/rniman/RnimanEngine/blob/main/docs/design.md#창입력)을 따른다.

### 앱 실행부 분리의 프로젝트 적용

상태: **적용 기록**. 실행 수명·입력 해석은 앱, CPU 이미지 디코딩은 `AssetLoader`, GPU 업로드·동기화는 렌더러에 둔다. 앱·테스트는 `BuildObjectTransformConstants`로 변환 상수 계산을 공유한다.

창을 먼저 선언하여 역순 파괴에서 GPU 자원을 HWND보다 먼저 정리한다. `Run`은 한 번만 호출하며 부분 실패는 RAII로 정리한다. 현재 단일 앱의 계약이며 새 실행 주체·범용 Application·Scene 도입 시 재검토한다. 상세는 [앱 실행 원본](https://github.com/rniman/RnimanEngine/blob/main/docs/design.md#앱-실행)을 따른다.

### 타입 명시와 렌더 데이터 명명

상태: 2026-10-15 사용자 선택에 따른 **타입 명시의 프로젝트 한정 채택과 명명 적용 기록**. 실패 계약과 값의 의미를 드러내기 위해 Sandbox와 영향받는 RendererSmoke·LightingChecks·RendererReadback에 적용했다.

| 대상 | 적용 내용 |
| --- | --- |
| 타입 명시 | 실패 가능한 `std::optional`·이름 있는 결과 구조체, DirectX 행렬·벡터·저장 타입, 경로·입력/창 상태·D3D12 descriptor |
| auto 유지 | 범위 반복·기존 요소 참조·캐스트로 타입이 드러나는 포인터·chrono 시각·람다 |
| 제외 범위 | WindowSmoke의 선언. 이후 변경 시 검토하며 일괄 치환 의무는 아님 |
| 명명 변경 | `RenderObject` → `ObjectTransformConstants`, `CreateRenderObject` → `BuildObjectTransformConstants`, `AssetDirectoryResult` → `ExecutableDirectoryResult` |

명명 변경은 변환 상수 계산과 EXE 경로 반환의 역할을 구분하기 위한 적용이다. 앱·렌더러·테스트·설계 문서에 함께 반영했으며 행렬 계산·실패 계약·192바이트 레이아웃은 유지한다. 새 경로 선언도 타입을 명시했다.

공통 [auto 규칙](../coding/cpp/auto.md)을 따르며 [자료형 선택](../coding/cpp/type-selection.md)은 초안을 유지한다. 결정·검증 근거는 [087570c의 적용 기록](https://github.com/rniman/RnimanEngine/blob/087570c7378c0d43ab3a0ad2d9c77942f6805067/docs/development.md#타입-명시와-렌더-데이터-명명-적용-2026-10-15)에 둔다.

### 실행 에셋과 추적 범위

상태: **현재 적용 기록**, 2026-10-16 사용자 선택에 따른 **공용 PNG 원본 경로의 프로젝트 한정 채택**. 개발 실행의 중복 PNG 복사를 없애기 위한 기준이다.

| 대상 | 현재 계약 |
| --- | --- |
| Sandbox PNG | 루트 `Assets/` 원본 직접 읽기. 폴더 전체 Git 제외·BaseColor 별도 준비 유지 |
| RendererSmoke PNG | 추적하는 `Tests/Assets/TextureTest.png` 직접 읽기. 손상 PNG 생성·삭제는 테스트 출력에서만 수행 |
| 원본 경로 | 두 프로젝트가 `Sandbox/SourcePaths.props`를 import. 확정된 `OutDir`·`EngineRoot`로 계산한 경로를 `RNIMAN_SOURCE_ROOT`로 전달 |
| 실행 의존성 | 작업 디렉터리에 의존하지 않으며 C++에 개발자별 절대 경로·상위 폴더 개수를 고정하지 않음 |
| 복사·실패 | Debug·Release별 PNG 복사 제거. 원본 누락 시 빌드·실행에서 진단하고 EXE 옆 과거 복사본으로 대체하지 않음 |
| CSO | EXE 옆 `Shaders/`에서 읽기 유지 |

원본은 읽기 전용으로 소비한다. 기본 출력 구조를 유지한 저장소 전체 이동은 가능하지만 EXE·Shaders만 옮기는 독립 실행은 지원하지 않는다. 출력 경로 변경 시 다시 빌드하며 독립 배포·런타임 에셋 루트 선택·DDS 캐시는 후속 구현 범위다.

경로·제약은 [087570c의 공용 에셋 경로](https://github.com/rniman/RnimanEngine/blob/087570c7378c0d43ab3a0ad2d9c77942f6805067/docs/project-structure.md#개발-실행의-공용-에셋-경로), 준비는 [엔진 실행 안내](https://github.com/rniman/RnimanEngine/blob/main/README.md#빌드와-실행)를 따른다. 공통 [원본과 생성물](../git/artifacts.md)은 초안이며 모든 에셋의 Git 제외를 일반화하지 않는다.

## Sandbox의 시험 적용

아래 선택은 **시험 적용**이며 프로젝트 한정 채택과 구분한다. 현재 적용 조건과 이유를 유지하되 범용 엔진 정책으로 확대하지 않는다.

### 자원과 실패 진단

ComPtr·렌더러 소유 Event로 자원을 관리하고 bool/API/HRESULT로 실패를 보고한다. 실패 후 진행을 중단하고 발생 위치·원인을 확인하기 위한 선택이다. 소멸 시에도 미완료 GPU 작업의 완료를 시도하지만 대기 실패 경로의 안전성을 모두 검증한 것은 아니다. 통일 오류 정책은 미결정이다.

Debug 레이어 필수, VSync·두 백 버퍼도 시험 적용이다. Debug 앱과 RendererSmoke의 진단 전제·실행 조건은 [엔진 README](https://github.com/rniman/RnimanEngine/blob/main/README.md#빌드와-실행)를 따른다.

### 큐브 출력의 시험 적용

행렬 전달·축은 [확인 기록](#좌표축과-행렬-전달의-확인)을 따른다. 시계 방향 앞면·전체 창 Viewport·현재 종횡비 Projection을 사용하며 단일 Direct Queue의 D32 버퍼는 매 프레임 지우고 전체 GPU 대기 후 재생성한다.

Upload Heap에서 직접 읽는 방식은 작은 고정 큐브 메시의 초기 구현 선택이다. 범용 메시 로딩 도입 시 Default Heap 업로드를 검토한다.

### 카메라 입력과 여러 Transform의 시험 적용

앱이 카메라·부모 없는 Transform을 소유하며 S*R*T로 World를 계산한다. 포커스 해제·최소화·모달 조작 후 입력·시간 누적으로 이동하지 않도록 입력과 이동 시간을 초기화하고 긴 프레임의 이동 시간을 제한한다.

렌더러는 `Render(std::span<const ObjectTransformConstants>, const FrameLighting&)`의 입력을 호출 중 복사하고 참조를 보관하지 않는다. 슬롯 Fence 완료 후 첫 256바이트에 프레임 조명(PS b1), 이후 오브젝트별 256바이트에 행렬(VS b0)을 기록한다. `FrameLighting`의 64바이트 크기·필드 offset도 static_assert로 확인한다. 빈 목록도 프레임 값을 기록하고 화면 지우기·Present를 수행한다. 호출자 데이터 수명과 GPU 사용 수명을 구분하기 위한 선택이며 Transform 계층·장면 수집 도입 시 경계를 재검토한다.

### PNG·텍스처·색 공간의 시험 적용

상태: **2026-10-12 구현의 시험 적용**, 2026-10-13 코드 대조. 적용 범위는 Sandbox의 단일 BaseColor PNG와 RendererSmoke의 기준 PNG다.

- 파일 파싱과 GPU 업로드를 분리하기 위해 `LoadPngImage`는 WIC로 단일 프레임 PNG를 행 패딩 없는 CPU RGBA8로 반환한다. STA 초기화 성공 횟수만 RAII로 정리하며 기존 MTA에서는 실패한다. 오류는 이름 있는 결과 구조체의 HRESULT·API로 전달하고 호출자가 경로와 함께 진단한다.
- 렌더러는 Default Heap 텍스처에 RowPitch를 반영해 업로드하고 첫 사용 전 GPU 완료를 기다린다. 대기 실패 시 업로드 자원을 멤버에 보존해 소멸자의 완료 시도까지 수명을 유지한다. 고정 메시의 Upload Heap 직접 읽기와 구분한다.
- BaseColor를 sRGB로 간주하고 sRGB SRV에서 읽은 선형 색상으로 조명을 계산한 뒤 sRGB RTV로 출력한다. 단일 밉·선형 Clamp·공유 텍스처·불투명 alpha가 현재 선택이며 ICC 변환·EXIF 회전·텍스처 교체·HDR는 지원하지 않는다. 범용 재질·다른 데이터 텍스처 도입 시 색 공간과 업로드 계약을 다시 정한다.

상세 범위·실패 조건은 [텍스처·sRGB 계약](https://github.com/rniman/RnimanEngine/blob/main/docs/design.md#텍스처srgb)을 따른다. 외부 API의 일반 권고나 새 공통 채택 규칙이 아니라 실제 구현 선택의 기록이다.

### 조명과 렌더 데이터의 시험 적용

상태: **2026-10-12 구현의 시험 적용**, 2026-10-13 코드 대조. 현재 단일 방향광에 적용한다. `SandboxLighting`은 각도·강도를 보호하는 값 클래스이며 입력 수집·GPU 자원을 소유하지 않는다. 앱이 입력과 카메라 위치를 해석해 공개 데이터인 `FrameLighting`을 만든다.

렌더 데이터에는 좌표 공간·방향의 의미·유효 범위를 명시하고 CPU와 셰이더가 같은 계약을 사용한다. 현재 `direction`은 빛이 진행하는 월드 단위 방향이다. 조명 값의 유한성·범위를 검사하고 잘못된 입력은 실패로 보고한다. 현재 데모의 의미·실패 경계를 고정하기 위한 선택이며 다중 광원·재질·PBR 정책으로 확대하지 않는다. 상세 수식·범위는 [기본 Phong 조명 계약](https://github.com/rniman/RnimanEngine/blob/main/docs/design.md#기본-phong-조명)에 둔다.

### 겹침 픽셀 검증의 시험 적용

테스트 전용 friend 어댑터가 같은 draw 경로를 Present 없이 실행하고 GPU 완료 후 픽셀을 읽는다. flip-discard 이후 내용에 의존하지 않기 위한 선택이며 앱의 Present는 유지한다. 테스트 자원은 GPU 완료 후 렌더러보다 먼저 정리한다. 적용 범위는 현재 불투명 큐브의 가림 검증이며 일반 캡처 API 도입 시 별도 계약을 정한다. 비교 방법·한계는 [픽셀 검증 문서](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#겹치는-오브젝트의-픽셀-검증-2026-10-05)에 둔다.

### HLSL 컨벤션 적용 상태

[HLSL 규칙](../coding/hlsl.md)은 **공통 초안**이다. 현재 Cube 셰이더는 단계별 파일·`Main` 진입점, FXC·SM5.0, EXE 기준 CSO 로딩을 사용하며 Sandbox·RendererSmoke가 빌드 설정을 공유한다. CubeVS의 월드 위치·법선은 `positionWS`·`normalWS`로 공간을 표시하며, 행렬 전달은 [별도 확인 기록](#좌표축과-행렬-전달의-확인)을 따른다. CubePS는 t0·s0의 BaseColor와 b1의 프레임 조명을 사용한다. PNG와 CSO의 실행 경로는 [현재 에셋 계약](#실행-에셋과-추적-범위)을 따른다. 공유 HLSLI·변형별 출력은 필요 시 검토하고 SM6 도입 시 DXC 전환을 검토한다.

### 자료형과 변환 초안의 확인 상태

2026-10-06 [자료형 선택과 별칭](../coding/cpp/type-selection.md)·[타입 변환과 범위 검사](../coding/cpp/conversions.md)를 Sandbox·RendererSmoke에 제한적으로 시험 적용했다. CPU 데이터 크기와 전용 API 계약을 구분하기 위한 선택이다.

- CPU 복사 크기·span 인덱스는 `std::size_t`, D3D12·Win32 경계는 `UINT`·`UINT64`·`SIZE_T` 등 API 타입을 유지한다. 상수 영역 크기 계산에는 곱셈 전 범위 검사를 둔다.
- 자체 타입 별칭·변환 도우미는 미도입이다. 실제 반복 사용처가 생기면 검토하며 GPU 자원·뷰·CPU 크기의 범위와 장치 제한은 각각 확인한다.

## 공통 규칙의 대조 근거

아래는 이 프로젝트의 기존 적용·확인 기록이다. 공통 규칙 전문이나 별도의 엔진 전용 규칙을 추가하지 않는다.

### 좌표축과 행렬 전달의 확인

상태: **공통 채택 규약과 구현의 일치 확인** · 최초 확인일: 2026-10-13 · 코드 재확인일: 2026-10-16. `087570c`를 [좌표축과 행렬 규약](../coding/coordinates-and-matrices.md)과 대조했다.

| 대상 | 확인한 구현·범위 |
| --- | --- |
| 월드·카메라 축 | 카메라 상하는 월드 `+Y`, yaw·pitch가 0일 때 전방은 `+Z`·오른쪽은 `+X`. 현재 카메라 전방은 회전된 벡터이며 월드 `+Z`와 구분 |
| View·Projection | `XMMatrixLookToLH`·`XMMatrixPerspectiveFovLH`의 왼손 규약 사용 |
| World·WVP | 부모 없는 Transform의 `S * R * T`, `World * View * Projection` |
| CPU 저장·업로드 | `BuildObjectTransformConstants`에서 `XMStoreFloat4x4`로 저장하고 렌더러가 구조체를 그대로 복사 |
| HLSL 선언·연산 | CubeVS의 WVP·World·법선 행렬 모두 명시적 `row_major`. 위치·법선은 벡터를 첫 인자로 `mul` 호출 |
| 법선 | World 역전치를 계산한 뒤 행 우선 저장. 법선용 역전치와 패킹을 맞추기 위한 전치를 구분 |
| Constant Buffer | `ObjectTransformConstants`의 192바이트 크기와 World·법선 필드의 64·128바이트 offset을 CPU에서 static_assert. 오브젝트별 영역은 256바이트 stride |
| 빌드 선언 | Windows SDK 10.0.26100.0·FXC·SM5.0·`Main`. 공유 `CubeShaders.props`에는 별도 기본 행렬 패킹 지정이 없고 소스의 각 선언으로 명시 |

거리 단위·외부 에셋의 규격은 이번 카메라·행렬 대조의 확인 범위 밖이다. 모델 가져오기·부모 Transform·다른 수학 라이브러리 도입 시 경계 규약을 재검토한다. 법선용 World는 현재 유한한 아핀 행렬·양수 행렬식·유한한 역행렬을 요구하며 반전 Transform의 컬링 보정은 제공하지 않는다.

법선의 3×3은 셰이더 내부 변환이며 Constant Buffer에는 4×4로 전달한다. 기존 패킹 검증은 [v0.1.0의 과거 근거](#milestone-v0-1-0)를 따른다.

### 코드 가독성 적용

2026-10-06 Sandbox·RendererSmoke의 지역 상수·빈 함수 본문·직접 include·API 계약 주석을 채택 규칙에 맞췄다. 초기 120열 시험 적용 이후의 기준은 [현재 포맷 규칙](../coding/cpp/formatting.md#긴-줄과-함수-인자)이다. 2026-10-10 정리에서는 당시 C++ 14개 파일의 UTF-8·BOM 없음·LF·마지막 개행·탭 들여쓰기·후행 공백을 확인했다.

### 반환값과 attribute 확인

2026-10-09의 확인 기록에 더해 2026-10-16 최신 코드에서 주요 실패·종료·입력 소비 API의 `[[nodiscard]]` 및 호출부 결과 처리를 확인했다. 판단 기준은 [함수 반환값 규칙](../coding/cpp/functions.md#반환값-무시와-nodiscard)이다.

| 대상 | 확인한 상태·남은 범위 |
| --- | --- |
| `Initialize`·`Render`·`Resize`·`WaitForGpu` | 적용됨. 정상 실행·재사용의 실패 결과를 검사 |
| `PumpMessages`·`ConsumeInput` | 적용됨. 종료 코드·소비한 입력을 호출부에서 사용 |
| `GetExecutableDirectory`·`LoadPngImage`·`BuildObjectTransformConstants` | 적용됨. 이름 있는 경로·이미지 결과와 optional 렌더 데이터의 실패를 호출부에서 검사 |
| `GetWorld`·`GetView`·테스트의 `Capture` | 미적용 후보. 현재 호출부는 결과를 사용·검사하며 추가 적용은 후속 검토 |
| `GetHandle`·`GetState` | 미적용. 일반 Getter의 경고 실익은 개별 판단 |

`D3D12Renderer` 소멸자의 `(void)WaitForGpu();`와 Fence Event 닫기 실패의 명시적 결과 무시는 종료 정리의 예외다. 실패는 호출한 함수 내부에서 보고하며 캐스트 자체가 GPU 완료를 보장하지 않는다. `InputState`는 이름 있는 구조체 반환의 실제 사례다. [의도적인 반환값 무시](../coding/cpp/functions.md#의도적인-반환값-무시)·[복합 결과 선택](../coding/cpp/functions.md#구조체와-pairtuple의-선택)을 따르며 [attribute 문서](../coding/cpp/attributes.md)의 공통 초안 상태는 유지한다.

<span id="클래스구조체-초안의-근거"></span>

### 클래스·구조체 규칙의 근거

2026-10-09의 코드 확인에 더해 2026-10-16 최신 코드에서 다음 사례는 [클래스·구조체 규칙](../coding/cpp/classes.md)과 부합했다.

- `Transform`·`State`·`InputState`·`ObjectTransformConstants`·`FrameLighting`은 공개 데이터 묶음이며 Transform에는 계산 함수를 함께 둔다. `ImageLoadResult`·`ExecutableDirectoryResult`는 이름 있는 복합 결과다.
- `SandboxLighting`은 값의 범위를 보호하고 특수 멤버 선언 없이 Rule of Zero를 따른다. `ComApartment`는 삭제된 복사 연산과 사용자 선언 소멸자로 복사·암시적 이동을 막아 COM 초기화 횟수의 중복 정리를 방지한다.
- `Win32Window`·`SandboxApp`은 단일 인자 생성자에 `explicit`을 사용하고 복사·이동을 금지한다. 창의 콜백 주소와 앱의 자원 수명을 유지하기 위한 선택이다.
- `D3D12Renderer`는 기본 생성자 `= default`, 사용자 선언 소멸자, 삭제된 복사 연산으로 암시적 이동도 생성되지 않는다. 현재 선언 조합을 확인한 기록이며 이동 정책을 새로 채택한 것은 아니다.
- 공개 API 뒤에 비공개 보조 함수·데이터를 배치하고 멤버 선언 순서에는 창·렌더러의 수명 의존성을 반영한다.

상속·`override`·`final`의 적용·검증 사례는 이번 근거에 없다. 생성 실패·소멸 진단·noexcept, 다형적 복제·복잡한 상속은 공통 미결정 정책이다.

### 삼각형 출력의 시험 적용

2026-09-18의 고정 삼각형·정사각형 Viewport는 2026-09-24 큐브·전체 창 Viewport로 대체했다. 당시 검증을 현재 큐브의 오류 경로 검증으로 간주하지 않는다.

### 공통 초안의 근거

[검증 결과 기록](../quality/verification.md)과 [원본과 생성물 관리](../git/artifacts.md)는 **공통 초안**이다. 이 프로젝트의 검증 구분·자원 관리 사례를 근거로 삼으며 로그·파일별 정책은 원본 저장소에 둔다.

## 미결정과 후속 검토

| 구분 | 남은 내용 |
| --- | --- |
| 미결정 | ECS 저장 방식·Unity 데이터 규격·통일 오류 정책·DPI 정책·최소 창 크기 |
| 프로젝트별 결정 | 네임스페이스의 제품 루트·대상·도입 시점. 기능별 재배치는 초안이며 현재 평면 배치 허용 |
| 경계 확장 시 검토 | 로컬 정면·거리 단위·외부 에셋 변환, 비정방 행렬·행렬 배열의 패킹 검증 |
| 후속 후보 | 자체 타입 별칭·변환 도우미, Transform·입력·렌더 데이터·업로드 공통화. 실제 소비자·반복 요구가 생길 때 검토 |
| 후속 구현 | 독립 배포·런타임 에셋 루트 선택·DDS 캐시 |
| 남은 검증 | 실제 화면·장치 입력·F5, 장치 손실·전체 실패 경로·전체 live-object 검사·성능 측정 |

원본 누락·과거 복사본 대체 금지·출력 경로 변경은 [087570c에서 검증한 범위](https://github.com/rniman/RnimanEngine/blob/087570c7378c0d43ab3a0ad2d9c77942f6805067/docs/development.md#공용-원본-경로-적용-2026-10-16)다. 위 후속 항목을 완료된 적용으로 취급하지 않으며 보류·폐기로 새로 확정한 항목은 없다.

## 확인한 범위와 원본

2026-10-16 원격 `087570c`의 개발·설계·구조 문서, C++ 15개 파일·CubeVS·빌드 프로젝트·필터·경로 설정을 로컬 위키와 대조했다. 엔진 로컬 HEAD·미커밋 변경·Visual Studio 표시·실행 상태는 확인하지 않았다. 과거 `ref/gameConvention/[DX12] coding convention(25.10.04).md`는 비교 근거로 보존하고 현재 채택 규칙을 우선한다.

<span id="milestone-v0-1-0"></span>

### v0.1.0의 과거 대조 근거

확인일: 2026-10-13 · 대상: [v0.1.0](https://github.com/rniman/RnimanEngine/tree/v0.1.0), 커밋 [14c957c](https://github.com/rniman/RnimanEngine/commit/14c957c381e53e1995ae6488b5562cdc4dc687e4). 다음은 당시 기록이며 현재 상태로 소급하지 않는다.

- 원격 `main`·로컬 HEAD·태그가 일치하고 미커밋 변경은 없었다. 코드 대조 기준 `cee7605`에서 태그까지는 문서만 변경됐다.
- C++ 확인 범위는 10월 12일의 채택 문서 9개였다. 공개 위키·로컬 Git 접근 실패로 로컬 문서를 임시 참고했다.
- 당시 이름은 `RenderObject`·`CreateRenderObject`·`AssetDirectoryResult`였으며 PNG를 EXE 옆으로 복사·배치했다.
- Debug·Release CubeVS의 FXC dumpbin에서 `row_major`·offset 0/64/128·각 행렬 64바이트를 CPU 구조체와 대조했다. 상세는 [태그의 컨벤션 확인 기록](https://github.com/rniman/RnimanEngine/blob/v0.1.0/docs/milestones/v0.1.0-sandbox.md#컨벤션-확인-기록-2026-10-13)에 둔다.

### 기존 검증 기록과 이번 확인의 구분

| 근거 | 검증 범위 |
| --- | --- |
| [v0.1.0 원본](https://github.com/rniman/RnimanEngine/blob/v0.1.0/docs/milestones/v0.1.0-sandbox.md) | 당시 빌드·실행·CPU/GPU·패킹 검증과 제약 |
| [087570c 개발 기록](https://github.com/rniman/RnimanEngine/blob/087570c7378c0d43ab3a0ad2d9c77942f6805067/docs/development.md#컨벤션) | 최신 변경의 빌드·Smoke·숨김 창 실행·경로 실패 검증 |
| 이번 위키 정비 | 정적 대조와 문서·링크 확인. 엔진 빌드·실행·컴파일·dumpbin 재실행 없음 |

상세 결과는 원본에 두며 엔진 코드·설정·검증 기록은 변경하지 않았다.

## 관련 문서

- [컨벤션 적용 기준](../baseline.md)

## 변경 기록

### 2026-10-16

- `087570c`의 타입 명시·공용 PNG 원본 경로 채택과 최신 명명·실행 제약을 반영했다. v0.1.0은 당시 이름·PNG 복사·검증 근거로 보존했다.
- 재배치 후보를 `Sandbox/` 바로 아래 주제별 폴더로 정리하고 `src/`는 선택으로 유지했다. 평면 배치 허용·네임스페이스 후속 결정과 채택·시험 적용·공통 초안·미결정을 구분했다.
- 반복 설명과 변경 기록을 줄이고 공통 좌표축·행렬 확인을 대조 근거 절로 옮겼다. 기존 절 주소·상태·적용 범위는 유지하며 실제 엔진 재배치·설정 변경·실행 검증은 수행하지 않았다.

### 2026-10-15

- 원격 `main`의 프로젝트 확장 구조와 외부 의존성 후보의 상태를 대조하고, 솔루션 역할별 분류·써드파티 연동 관리의 공통 초안을 연결했다. 기존 계획을 실제 적용·도입으로 바꾸지 않았으며 코드·설정·패키지는 변경하지 않았다.

### 2026-10-14

- 원격 `main`의 구조·Sandbox 프로젝트·필터·두 Smoke 빌드 입력을 대조하여 실제 평면 배치와 원본 구현의 직접 참조를 기록했다. 기능별 실제 폴더·헤더와 구현의 동시 배치 후보를 초안으로 추가하고 공통 소스 배치 초안과 연결했다. 파일 이동·프로젝트 설정 변경·엔진 빌드·실행은 수행하지 않았다.

### 2026-10-13

- v0.1.0(`14c957c`)을 컨벤션 대조 시점으로 기록하고 좌표축·행렬 채택 규약과 기존 구현의 일치·패킹 검증 근거를 반영했다.
- PNG·sRGB·조명 데이터·자원 수명·에셋 추적 및 C++ 적용 사례를 정리했다. 프로젝트 한정 채택·시험 적용·미결정 상태와 공통 채택 범위는 유지했다.
- 사용자 요청에 따라 프로젝트 소개·마일스톤 성과·로드맵·상세 실행 결과를 원본 링크로 대체하고 컨벤션 적용·예외·판단 근거 중심으로 축약했다. 엔진 코드·설정은 변경하지 않았다.

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
