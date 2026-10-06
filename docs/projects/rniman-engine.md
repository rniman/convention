# RnimanEngine 프로젝트 기준

[프로젝트별 목차](index.md) · [컨벤션 적용 기준](../baseline.md)

상태: 참조 초안(초기 구현·프레임 동기화만 프로젝트 한정 채택하며 나머지는 시험 적용·확인 기록) · 정리일: 2026-10-06

D3D12 미니 게임 엔진의 전용 기준과 적용 상태를 요약한다. 구현·실행·검증 상세는 비공개 프로젝트 저장소에서 관리한다.

## 주요 문서

| 원본 | 내용 |
| --- | --- |
| [README](https://github.com/rniman/RnimanEngine/blob/main/README.md) | 현재 기능·빌드·실행 |
| [개발 설정과 검증](https://github.com/rniman/RnimanEngine/blob/main/docs/development.md) | 컨벤션 적용·검증 결과·남은 제약 |
| [엔진 설계](https://github.com/rniman/RnimanEngine/blob/main/docs/design.md) | 책임·수명·데이터 경계 |
| [프로젝트 구조](https://github.com/rniman/RnimanEngine/blob/main/docs/project-structure.md) | 출력·에셋·셰이더 배치 |

## 컨벤션 적용 상태

공통 기준은 [현재 채택 규칙](../baseline.md)이며 새 결정은 [상호 반영 절차](../baseline.md#위키와-프로젝트의-상호-반영)를 따른다. 아래 Sandbox 선택을 다른 프로젝트의 공통 규칙으로 확대하지 않는다. 원격 최신 상태·푸시·배포는 미확인이다.

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

## 큐브 출력의 시험 적용

앱은 행 벡터의 WVP를 전달하고 셰이더는 `row_major`·`mul(position, matrix)`로 읽는다. 왼손 View·Projection, 시계 방향 앞면, 전체 창 Viewport·종횡비 Projection을 사용한다. 작은 고정 메시는 Upload Heap에서 읽고, 단일 Direct Queue의 D32 버퍼는 매 프레임 지우며 전체 GPU 대기 후 재생성한다.

## 카메라 입력과 여러 Transform의 시험 적용

앱이 입력·카메라·부모 없는 Transform을 소유하며 S*R*T로 World를 계산한다. 포커스 해제·최소화·모달 조작 시 입력과 이동 시간을 초기화하고 긴 프레임의 이동 시간을 제한한다. 렌더러는 WVP 목록을 보관하지 않고 슬롯 Fence 완료 후 오브젝트별 256바이트 상수 영역을 확장·복사한다. 빈 목록은 화면 지우기·Present만 수행한다.

## 겹침 픽셀 검증의 시험 적용

테스트 전용 friend 어댑터가 같은 draw 경로를 Present 없이 실행하고 GPU 완료 후 픽셀을 읽는다. flip-discard 이후 내용에 의존하지 않으며 앱의 Present는 유지한다. 앞/뒤 단독 이미지와 정순·역순 결과를 비교하고 실제 겹침·색 차이·뒤쪽 가시 영역을 검사한다. 테스트 자원은 GPU 완료 후 렌더러보다 먼저 정리한다. 일반 캡처 API나 공통 friend 규칙으로 확대하지 않는다.

## HLSL 컨벤션 적용 상태

[HLSL 규칙](../coding/hlsl.md)은 **공통 초안**이다. 단계별 파일명·`Main` 진입점과 FXC·SM5.0·EXE 기준 CSO 로딩을 확인했다. 현재 Cube 셰이더 빌드 설정은 Sandbox·RendererSmoke가 공유한다. 공유 HLSLI·공간 접미어·변형별 출력은 필요 시 검토하며 SM6 도입 시 DXC 전환을 검토한다. 초안의 채택·엔진 전체 적용 완료를 뜻하지 않는다.

## 자료형과 변환 초안의 확인 상태

2026-10-06 자료형 선택·변환 통합 초안을 로컬 코드와 대조했으며 **규칙 채택·코드 변경은 하지 않았다**. 현재 초안은 [자료형 선택과 별칭](../coding/cpp/type-selection.md)과 [타입 변환과 범위 검사](../coding/cpp/conversions.md)로 분리했으며, 아래 확인 범위와 미적용 상태를 유지한다. 분리 후 엔진 코드를 다시 검증한 기록은 아니다.

- D3D12 전용 구현의 `UINT`·`UINT64`·`SIZE_T`는 API 타입 유지 후보이며 공통 엔진 타입으로 확대하지 않는다.
- `RenderInternal`의 span 순회·CPU 복사 크기는 `std::size_t` 정리 후보다. 곱셈 전 범위 검사는 유지하고 관련 코드 수정 또는 초안 채택 시 적용·검증한다.
- 자체 타입 별칭·변환 도우미는 추가하지 않았다. 실제 반복 사용처가 생기면 검토하며 GPU 자원·뷰·CPU 크기의 범위와 장치 제한은 각각 확인한다.

확인 당시의 근거는 로컬 Convention HEAD `a39c47b`와 미커밋 초안, `ref/DevRnimanConvention/CodingConvention.md`다. 당시 공개 위키는 접근 실패로 확인하지 못했다. 상세 적용 상태는 엔진 개발 문서에서 관리한다.

## 코드 가독성 적용

Sandbox·RendererSmoke에 작업별 빈 줄과 인자 배치를 적용했다. 초기 120열 시험 적용 이후의 기준은 [현재 포맷 규칙](../coding/cpp/formatting.md#긴-줄과-함수-인자)이며 과거 수치를 고정 기준으로 사용하지 않는다.

## 삼각형 출력의 시험 적용

2026-09-18의 고정 삼각형·정사각형 Viewport는 2026-09-24 큐브·전체 창 Viewport로 대체했다. 당시 검증을 현재 큐브의 오류 경로 검증으로 간주하지 않는다.

## 공통 초안의 근거

[검증 결과 기록](../quality/verification.md)과 [원본과 생성물 관리](../git/artifacts.md)는 **초안**이다. 프로젝트의 검증 구분·자원 관리 사례를 근거로 삼으며 로그·파일별 정책은 원본 저장소에 둔다. HRESULT 오류 정보·GPU 데이터 수명·Transform 공통화는 다른 실제 소비자가 생길 때 검토한다.

## 확인한 범위와 원본

최초 원격 조사 근거는 [2026-09-15 커밋 2845efb](https://github.com/rniman/RnimanEngine/tree/2845efb4db318fbe9b1df2cdb14ed1cb01849726)이며 이후 기록은 로컬 구현을 기준으로 한다. 프로젝트 확인 기록은 엔진 빌드·실행이나 원격 최신 상태·푸시·배포 완료를 뜻하지 않는다.

## 변경 기록

- 2026-10-06: 중복 설명과 작업 이력을 줄이고 프로젝트 한정 채택·시험 적용·미적용 조건을 유지했다. 자료형 선택·변환 초안과 로컬 코드의 확인 범위를 기록하고, 문서 분리에 맞춰 두 초안으로 연결했다. 엔진 코드 수정이나 빌드·실행 검증은 수행하지 않았다.
