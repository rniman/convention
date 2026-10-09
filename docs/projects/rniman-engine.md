# RnimanEngine 프로젝트 기준

[프로젝트별 목차](index.md)

상태: 참조 초안(초기 구현·프레임 동기화만 프로젝트 한정 채택하며 나머지는 시험 적용·확인 기록) · 정리일: 2026-10-09

D3D12 미니 게임 엔진의 전용 기준과 적용 상태를 요약한다. 구현·실행·검증 상세는 비공개 프로젝트 저장소에서 관리한다.

## 주요 문서

| 원본 | 내용 |
| --- | --- |
| [README](https://github.com/rniman/RnimanEngine/blob/main/README.md) | 현재 기능·빌드·실행 |
| [개발 설정과 검증](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md) | 컨벤션 적용·검증 결과·남은 제약 |
| [엔진 설계](https://github.com/rniman/RnimanEngine/blob/main/docs/design.md) | 책임·수명·데이터 경계 |
| [프로젝트 구조](https://github.com/rniman/RnimanEngine/blob/main/docs/project-structure.md) | 출력·에셋·셰이더 배치 |

## 컨벤션 적용 상태

공통 기준은 [현재 채택 규칙](../baseline.md)이며 프로젝트 작업과 위키 정비는 [위키의 적용과 프로젝트 근거 검토](../baseline.md#위키의-적용과-프로젝트-근거-검토)를 따른다. 아래 Sandbox 선택을 다른 프로젝트의 공통 규칙으로 확대하지 않는다. 원격 최신 상태·푸시·배포는 미확인이다.

## 프로젝트 제약과 전용 기준

- Windows·C++20·MSVC·x64를 대상으로 하며 출력은 프로젝트·빌드 구성별로 분리한다.
- Sandbox 구현 파일은 PCH를 먼저 포함한다. [헤더 독립성·직접 include](../coding/cpp/headers.md)는 유지한다.
- Windows 명령 스크립트는 CRLF, C++ 소스는 [UTF-8·LF](../coding/cpp/formatting.md)를 사용한다.
- ECS 저장 방식·Unity 데이터 규격·통일 오류 정책은 미결정이다.

## D3D12 초기 구현 선택

2026-09-15 Sandbox 한정 채택: 앱이 창·렌더러를 각각 소유하고 렌더러를 먼저 정리한다. 고성능 하드웨어를 우선하며 WARP로 자동 대체하지 않는다. WM_SIZE는 크기를 기록하고 프레임 경계에서 리사이즈하며 최소화·0 크기에는 렌더링을 중지한다.

ComPtr·렌더러 소유 Event, bool/API/HRESULT 실패 보고, Debug 레이어 필수, VSync·두 백 버퍼는 진단과 수명 관리를 위한 **시험 적용**이다.

## 프레임 동기화 전환

2026-09-17 **프로젝트 한정 채택**: 초기 매 프레임 전체 대기를 슬롯별 Allocator·Fence 완료 후 재사용으로 대체했다. 리사이즈·종료는 전체 GPU 대기를 유지하며 제출 실패 시에도 정리를 시도한다. 두 슬롯·단일 Command List·공유 Fence/Event는 Sandbox 구현 선택이며 다중 Queue 정책은 아니다.

## 창·입력 분리의 프로젝트 적용

2026-10-06 사용자 요청으로 Main의 창 수명·Win32 메시지·입력 수집을 `Win32Window`로 추출했다. 창이 콜백 상태를 소유하고 복사·이동을 금지한다. 앱은 읽기 전용 창 상태와 프레임별 입력 복사본을 사용하며, 키 눌림은 유지하고 마우스 누적량·시간 초기화 요청만 소비한다. GPU 리사이즈는 프레임 경계에서 앱이 수행하고, 렌더러를 창보다 먼저 정리한다.

현재 Sandbox의 창 하나·UI 스레드에 적용한다. 입력 의미·카메라·큐브 갱신은 아래 SandboxApp에 두며 범용 Input·Scene·공용 Engine의 정책으로 확대하지 않는다. 관련 헤더·함수·소유권의 기존 채택 규칙을 적용했고, 검증과 남은 제약은 [엔진 개발 문서](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#창입력-추출-2026-10-06)에서 관리한다.

## 앱 실행부 분리의 프로젝트 적용

2026-10-06 사용자 요청으로 Main의 초기화·메시지 루프·카메라/큐브 갱신·WVP 생성과 렌더 호출을 `SandboxApp`으로 추출했다. Main은 앱 생성·Run 호출·종료 코드 전달을 담당한다. 앱이 창·렌더러·카메라·큐브를 직접 소유하고, 창을 렌더러보다 먼저 선언하여 역순 파괴에서 GPU 자원을 HWND보다 먼저 정리한다.

Run은 한 번만 호출하며 종료 요청에서는 GPU 완료 확인 후 WM_QUIT 코드를 전달한다. 실패 시 부분 자원은 기존 RAII 정책으로 정리한다. Sandbox 한정 구현이며 범용 Application·Scene·Engine 계층을 추가한 것은 아니다. 헤더·초기화·소유권의 기존 채택 규칙을 적용했고 상세 흐름·검증·제약은 [엔진 개발 문서](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#앱-실행부-추출-2026-10-06)에서 관리한다.

## 큐브 출력의 시험 적용

앱은 행 벡터의 WVP를 전달하고 셰이더는 `row_major`·`mul(position, matrix)`로 읽는다. 왼손 View·Projection, 시계 방향 앞면, 전체 창 Viewport·종횡비 Projection을 사용한다. 작은 고정 메시는 Upload Heap에서 읽고, 단일 Direct Queue의 D32 버퍼는 매 프레임 지우며 전체 GPU 대기 후 재생성한다.

## 카메라 입력과 여러 Transform의 시험 적용

앱이 입력·카메라·부모 없는 Transform을 소유하며 S*R*T로 World를 계산한다. 포커스 해제·최소화·모달 조작 시 입력과 이동 시간을 초기화하고 긴 프레임의 이동 시간을 제한한다. 렌더러는 WVP 목록을 보관하지 않고 슬롯 Fence 완료 후 오브젝트별 256바이트 상수 영역을 확장·복사한다. 빈 목록은 화면 지우기·Present만 수행한다.

## 겹침 픽셀 검증의 시험 적용

테스트 전용 friend 어댑터가 같은 draw 경로를 Present 없이 실행하고 GPU 완료 후 픽셀을 읽는다. flip-discard 이후 내용에 의존하지 않으며 앱의 Present는 유지한다. 앞/뒤 단독 이미지와 정순·역순 결과를 비교하고 실제 겹침·색 차이·뒤쪽 가시 영역을 검사한다. 테스트 자원은 GPU 완료 후 렌더러보다 먼저 정리한다. 일반 캡처 API나 공통 friend 규칙으로 확대하지 않는다.

## HLSL 컨벤션 적용 상태

[HLSL 규칙](../coding/hlsl.md)은 **공통 초안**이다. 단계별 파일명·`Main` 진입점과 FXC·SM5.0·EXE 기준 CSO 로딩을 확인했다. 현재 Cube 셰이더 빌드 설정은 Sandbox·RendererSmoke가 공유한다. 공유 HLSLI·공간 접미어·변형별 출력은 필요 시 검토하며 SM6 도입 시 DXC 전환을 검토한다. 초안의 채택·엔진 전체 적용 완료를 뜻하지 않는다.

## 자료형과 변환 초안의 확인 상태

2026-10-06 공개 C++ 위키와 로컬 Convention HEAD `33e96f6`를 코드와 대조하고 [자료형 선택과 별칭](../coding/cpp/type-selection.md)·[타입 변환과 범위 검사](../coding/cpp/conversions.md)의 다음 범위를 Sandbox·RendererSmoke에 **시험 적용**했다. 공통 초안의 전체 채택을 뜻하지 않는다.

- `RenderInternal`의 상수 간격·CPU 복사 크기·span 순회 인덱스를 `std::size_t`로 정리했다. 곱셈 전 범위 검사를 유지했다.
- D3D12 전용 구현의 `UINT`·`UINT64`, API 출력 인자의 `SIZE_T`와 디스크립터 주소 계산은 API 계약에 맞춰 유지했다. 전체 범위가 보존되는 전달에 캐스트를 일괄 추가하지 않았다.
- 자체 타입 별칭·변환 도우미는 추가하지 않았다. 실제 반복 사용처가 생기면 검토하며 GPU 자원·뷰·CPU 크기의 범위와 장치 제한은 각각 확인한다.

코드 적용과 빌드·실행 검증 결과, 시각 확인·입력 검증의 남은 범위는 [엔진 개발 문서](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md#최신-검증-결과)에서 관리한다.

## 코드 가독성 적용

Sandbox·RendererSmoke에 작업별 빈 줄과 인자 배치를 적용했다. 2026-10-06 현재 채택 규칙에 맞춰 지역 상수를 camelCase로 변경하고 빈 함수 본문·직접 include·API 계약 주석을 정리했다. 초기 120열 시험 적용 이후의 기준은 [현재 포맷 규칙](../coding/cpp/formatting.md#긴-줄과-함수-인자)이며 과거 수치를 고정 기준으로 사용하지 않는다.

## 반환값과 attribute 확인

2026-10-09 로컬 `D:/STUDY/DirectX12/RnimanEngine`의 Sandbox 헤더와 호출부를 확인했다. 아래는 기존 구현의 확인 기록이며 공통 규칙의 추가 채택이나 이번 작업의 코드 적용 결과는 아니다. 공통 판단 기준은 [함수 반환값 규칙](../coding/cpp/functions.md#반환값-무시와-nodiscard)에 둔다.

| 대상 | 현재 로컬 코드 | 확인 이유·남은 범위 |
| --- | --- | --- |
| `Initialize`·`Render`·`Resize` | `[[nodiscard]]` 적용 | 실패를 후속 실행 중단에 사용 |
| `WaitForGpu` | `[[nodiscard]]` 적용 | 정상 종료·리사이즈에서 GPU 완료 결과를 검사 |
| `PumpMessages` | `[[nodiscard]] std::optional<int>` | 종료 요청 유무와 종료 코드를 반환하며 앱이 처리 |
| `ConsumeInput` | `[[nodiscard]] InputState` | 입력 복사 후 마우스 누적량·시간 초기화 요청을 비우므로 결과 폐기 시 해당 입력이 유실 |
| `GetWorld`·`GetView` | 미적용 | 계산 결과의 사용을 호출 목적으로 보는 적용 후보. 이번 확인에서 추가하지 않음 |
| `GetHandle`·`GetState` | 미적용 | 일반 Getter는 결과 폐기의 문제와 경고 실익을 개별 판단 |

`D3D12Renderer` 소멸자는 미완료 작업이 있을 때 `(void)WaitForGpu();`를 사용하고, Fence Event 닫기 실패의 `CheckResult` 반환값도 명시적으로 버린다. 실패 진단은 호출한 함수 내부에서 보고한다. 정상 경로의 검사와 종료 정리의 예외를 구분하는 사례이며 이 캐스트가 GPU 완료·모든 실패 경로의 안전성을 보장하지 않는다.

`InputState`는 이름 있는 구조체로 여러 입력 필드를 전달하는 기존 사례다. 엔진의 tuple 사용 사례나 구조체 대비 성능 측정은 이번 확인 근거에 없다. 현재 공통 기준은 [구조체와 pair·tuple의 선택](../coding/cpp/functions.md#구조체와-pairtuple의-선택)과 [의도적인 반환값 무시](../coding/cpp/functions.md#의도적인-반환값-무시)를 따른다. [attribute 초안](../coding/cpp/attributes.md)은 공통 미채택 상태를 유지한다. 엔진 코드·빌드 설정은 수정하지 않았으며 빌드·실행 검증도 수행하지 않았다.

<span id="클래스구조체-초안의-근거"></span>

## 클래스·구조체 규칙의 근거

2026-10-09 로컬 Sandbox의 `Transform.h`, `Win32Window.h`, `SandboxApp.h`, `D3D12Renderer.h`를 확인했다. [클래스·구조체 규칙](../coding/cpp/classes.md)을 작성하기 위한 기존 코드 대조이며 이번 작업의 코드 반영 결과가 아니다.

- `Transform`은 공개 필드와 `GetWorld() const`를 함께 갖는 구조체다. `Win32Window::State`·`InputState`도 공개 데이터 묶음이다. 구조체에 멤버 함수를 둘 수 있는 실제 사례이며 모든 구조체의 선택 기준을 자동으로 확정하지 않는다.
- `Win32Window`·`SandboxApp`은 단일 인자 생성자에 `explicit`을 사용하고 복사·이동 네 연산을 삭제한다. 창의 주소·콜백 상태와 앱의 자원 수명 제약은 기존 프로젝트 기록을 따른다.
- `D3D12Renderer`는 기본 생성자 `= default`, 사용자 선언 소멸자, 삭제된 복사 연산을 갖는다. 이동 연산을 명시하지 않았으며 이 선언 조합에서는 암시적 이동 연산이 생성되지 않는다. 모든 타입에 이동 `= default`를 추가하는 근거로 삼지 않는다.
- 클래스는 공개 API 뒤에 비공개 보조 함수·데이터를 배치한다. `SandboxApp`의 창·렌더러 선언 순서는 역순 정리의 수명 의존성을 반영한다.

이번 대조에는 `override`·`final` 적용 사례나 상속 정책 검증을 포함하지 않았다. 같은 날 사용자 선택으로 공통 기본 규칙을 채택했지만 엔진 전체 적용·검증 완료를 뜻하지 않는다. 생성 실패·소멸 진단·noexcept, 다형적 복제·복잡한 상속은 공통 채택에서 제외했다. 엔진 코드·설정은 수정하지 않았고 빌드·실행 검증도 수행하지 않았다. 전용 수명·오류 처리 계약은 프로젝트에서 관리한다.

## 삼각형 출력의 시험 적용

2026-09-18의 고정 삼각형·정사각형 Viewport는 2026-09-24 큐브·전체 창 Viewport로 대체했다. 당시 검증을 현재 큐브의 오류 경로 검증으로 간주하지 않는다.

## 공통 초안의 근거

[검증 결과 기록](../quality/verification.md)과 [원본과 생성물 관리](../git/artifacts.md)는 **초안**이다. 프로젝트의 검증 구분·자원 관리 사례를 근거로 삼으며 로그·파일별 정책은 원본 저장소에 둔다. HRESULT 오류 정보·GPU 데이터 수명·Transform 공통화는 다른 실제 소비자가 생길 때 검토한다.

## 확인한 범위와 원본

최초 원격 조사 근거는 [2026-09-15 커밋 2845efb](https://github.com/rniman/RnimanEngine/tree/2845efb4db318fbe9b1df2cdb14ed1cb01849726)이며 이후 기록은 로컬 구현을 기준으로 한다. 프로젝트 확인 기록은 엔진 빌드·실행이나 원격 최신 상태·푸시·배포 완료를 뜻하지 않는다.

## 관련 문서

- [컨벤션 적용 기준](../baseline.md)

## 변경 기록

- 2026-10-09: Sandbox의 반환값·attribute·종료 정리와 클래스·구조체·복사·이동 선언을 확인하고 관련 공통 규칙·초안으로 연결했다. 클래스 기본 규칙의 공통 채택과 엔진 적용 상태를 구분했다. GetWorld·GetView는 nodiscard 미적용 후보로 기록했으며 엔진 코드·설정은 변경하지 않았다.
- 2026-10-06: 앱 실행·데모 갱신을 SandboxApp으로 분리하고 Main의 진입점 역할과 창·렌더러 소유 순서를 기록했다. 공통 채택 규칙은 유지했다.
- 2026-10-06: 창·입력 수집을 Win32Window로 분리하고 창 소유 상태·입력 소비·앱과 렌더러의 수명 경계를 기록했다. 기존 공통 채택 규칙은 유지했다.
- 2026-10-06: Sandbox·RendererSmoke의 채택 규칙 적용과 자료형 초안의 제한된 시험 적용 결과를 반영했다. 검증 상세는 엔진 문서로 연결하며 공통 규칙의 채택 상태는 유지했다.
- 2026-10-06: 중복 설명과 작업 이력을 줄이고 프로젝트 한정 채택·시험 적용·미적용 조건을 유지했다. 자료형 선택·변환 초안과 로컬 코드의 확인 범위를 기록하고, 문서 분리에 맞춰 두 초안으로 연결했다. 엔진 코드 수정이나 빌드·실행 검증은 수행하지 않았다.
