# Unity 오브젝트·에셋 이름과 폴더 구조

[Unity 목차](index.md)

상태: 초안 · 작성일: 2026-09-30 · 적용 범위: 직접 관리하는 Unity GameObject, Prefab, Scene, 일반 에셋과 Assets 내부 폴더

이름에서 대상과 차이를 읽고 자료를 찾을 위치를 예측할 수 있도록 정리한다. 아래 `필수`·`권장`·`선택`은 채택 시의 제안 강도다. 대화에서 논의한 후보이며 아직 개인 채택 규칙이 아니다. Unity·C# 버전과 렌더 파이프라인은 프로젝트에서 정한다. C# 식별자·코드 포맷은 이번 범위에서 제외한다.

## 명명 규칙

### 공통 표기

직접 이름을 정하거나 의미를 바꿀 때 적용한다. GameObject·에셋·폴더에 같은 기준을 사용하며, 자동 복제 이름은 아래 중복·번호 기준을 따른다.

- **권장:** 의미 있는 영문 단어를 PascalCase로 연결한다. 위치·재질·외형·동작도 이름에 포함하며 공백을 `_`로 바꾸지 않는다. 예: `MainCamera`, `WallNorth`, `WallStoneDamaged`, `PlayerRun`.
- **필수:** 같은 계열에서는 단어 순서를 유지한다. `WallStone`과 `StoneWall` 중 프로젝트에서 선택한 방식을 일관되게 사용한다.
- **권장:** 폴더·그룹이 같은 종류의 모음이면 `Scenes`, `Prefabs`, `Walls`처럼 복수형을 쓴다. 개체·기능은 `Player`처럼 해당 명칭을 쓴다.
- **권장:** 필요한 정보만 이름에 담고, 직접 지정할 때 의미 없는 `New`, `Copy`, `FinalFinal`을 피한다.
- **필수:** 대소문자만 다른 파일·폴더로 구분하지 않는다. 예: `Wall.png`와 `wall.png`.

예약 이름·외부 도구가 요구하는 표기와 아래 `_Project` 루트 폴더는 예외다. 이 규칙은 Unity 콘텐츠용이며 UI 문구·번역 문자열에는 적용하지 않는다. 위키의 Markdown 경로는 기존 영문 소문자 `kebab-case`를 유지한다.

### 중복 이름과 번호

| 상황 | 강도 | 처리 |
| --- | --- | --- |
| 개별 식별이 필요 없는 반복 배치 | 선택 | 같은 부모 아래에서도 여러 `Wall` 허용 |
| 서로 다른 부모 아래의 같은 역할 | 선택 | 각 부모 아래에 `Visual`, `Collider` 등 동명 허용 |
| 자동 복제 이름 | 선택 | `Wall (1)`, `WallStone_02 (1)` 등을 그대로 유지. 공백·괄호 제거, 번호 삭제·변환·자릿수 통일 불필요 |
| 개별 식별이 필요한 대상 | 권장 | `WallNorth`처럼 의미를 우선하고, 직접 순번을 관리할 때 `SpawnPoint_01` 사용 |
| 서로 다른 폴더의 에셋 | 선택 | 동명 허용. 검색 시 혼동되면 이름을 구체화하는 것을 권장 |
| 이름으로 검색·참조하는 대상 | 필수 | 해당 검색 범위에서 대상을 하나로 구분. 번호가 붙었다는 사실만으로 유일성을 가정하지 않음 |

프로젝트 전체에서 이름을 유일하게 만들거나 단순 복제 이름을 일괄 정리할 필요는 없다. 직접 번호를 관리할 때는 다음 기준을 적용한다.

- **권장:** `이름_번호` 형태로 `_01`부터 최소 두 자리를 사용한다. 큰 집합은 `_001`부터 시작할 수 있으며 자릿수는 최대 개수 제한이 아니다.
- **필수:** 같은 계열에서 번호의 의미를 유지한다. 에셋 외형 번호와 배치 순번을 혼용하지 않는다. 자동 복제 번호에는 이 의미를 부여하지 않는다.
- **권장:** 삭제로 빈 번호가 생겨도 다시 매기지 않는다. 번호는 개수·현재 정렬 위치를 보장하지 않는다.
- **필수:** 이름이나 번호를 저장 데이터의 영구 ID로 가정하지 않는다.

예를 들어 `WallStone_02`의 `02`는 외형 번호다. 외형과 배치 번호를 모두 직접 표현해야 한다면 `WallStoneVariant02_01`을 사용할 수 있다(**선택**). `WallStone_02_01`처럼 의미가 드러나지 않는 숫자 연결은 피한다(**권장**).

동명 허용은 원본 파일의 불필요한 복제를 권장하는 뜻이 아니다. 내용과 용도가 같은 원본 복사본은 사용처를 확인한 뒤 통합한다(**권장**).

### 대상별 예시와 추가 조건

다음은 공통 표기의 적용 예시다. 대상에만 필요한 추가 조건을 함께 적는다.

| 대상 | 이름 예시 | 추가 조건 |
| --- | --- | --- |
| GameObject | `MainCamera`, `WallNorth` | 중복·자동 번호는 위 기준 적용 |
| Prefab | `EnemyGoblin.prefab` | 원본 루트 이름을 `EnemyGoblin`으로 맞추는 것을 권장 |
| Prefab Variant | `EnemyGoblinElite.prefab` | 이름과 별도로 실제 Variant 관계 확인 필수 |
| Scene | `Bootstrap.unity`, `MainMenu.unity`, `StageForest.unity` | 빌드 순서 번호는 기본으로 붙이지 않음. 콘텐츠 순서인 스테이지 번호는 선택 |
| Material | `WallStone.mat` | — |
| Texture | `WallStoneBaseColor.png`, `WallStoneNormal.png` | 맵 이름은 실제 셰이더·제작 파이프라인 요구를 우선 |
| Animation Clip | `PlayerIdle.anim`, `PlayerRun.anim` | — |

이름이 텍스처 Import 설정이나 Scene 빌드·로딩 순서를 결정하지 않으므로 실제 설정을 확인한다(**필수**).

`PF_`, `MAT_`, `TEX_` 같은 종류 접두어의 공통 도입과 텍스처 맵 접미어 전체 목록은 **미결정**이다. 위 예시가 접두어 금지를 뜻하지는 않는다. 프로젝트에서 접두어를 선택하면 대상 종류·약어를 기록하고 같은 계열에 일관되게 적용한다.

## 빈 GameObject로 묶음 관리

**권장:** 반복 오브젝트를 한 단위로 찾아보고 선택·접기 쉽도록, 의미 있는 묶음은 빈 GameObject 아래에 배치한다. 그룹 이름은 [공통 표기](#공통-표기)를 따른다.

```text
Environment
├── Walls
│   ├── Wall
│   ├── Wall (1)
│   └── Wall (2)
└── Props
    ├── Barrel
    └── Barrel (1)
SpawnPoints
├── SpawnPoint_01
└── SpawnPoint_02
```

예시는 [중복 이름과 번호](#중복-이름과-번호)의 자동 복제 이름과 직접 관리 번호를 각각 적용한 구조다.

- **권장:** 용도·구역·함께 편집할 단위를 기준으로 묶는다. 기존 부모가 이미 역할을 충분히 표현하면 중간 그룹을 추가하지 않는다. 빈 그룹이나 의미 없는 중첩을 미리 만들지 않는다.
- **권장:** 단순 정리용 그룹은 자식을 넣기 전에 로컬 Position·Rotation을 `(0, 0, 0)`, Scale을 `(1, 1, 1)`로 두는 것을 기본으로 한다. 구역의 기준점이나 회전축 역할을 하는 부모는 목적에 맞는 Transform을 사용할 수 있다.
- **필수:** 빈 GameObject도 Transform을 가진 실제 부모다. 기존 오브젝트를 묶거나 부모 Transform을 바꾼 뒤에는 자식의 월드 위치·회전·크기와 기존 동작이 유지되는지 확인한다. 자식을 넣은 뒤 부모를 무조건 Reset하지 않는다.
- **필수:** 부모 경로나 부모·자식 관계에 의존하는 검색·스크립트·Prefab 구조가 있다면 재배치의 영향을 확인한다. 그룹을 만들어도 전역 이름 검색의 중복이 자동으로 해결되지는 않는다.

이 구조는 Hierarchy 탐색과 편집을 위한 개인 제안이다. Unity의 부모 Transform 동작을 근거로 주의사항을 정했으며, 특정 계층 구조나 성능 향상을 보장하는 규칙은 아니다.

## 기본 폴더 구조

**권장:** 작은 프로젝트는 종류별 폴더로 시작하고 직접 만든 콘텐츠를 `Assets/_Project/`에 모은다. `_Project`의 선행 `_`는 자체 콘텐츠 루트를 눈에 띄게 구분하기 위한 폴더 한정 예외다. 다른 폴더·에셋에 선행 `_`를 확장하지 않는다. 이 이름은 개인 구성 제안이며 Unity 예약 이름이 아니다. 프로젝트명을 루트 이름으로 사용해야 한다면 이유를 기록하고 일관되게 사용할 수 있다(**선택**).

```text
Assets/
├── _Project/
│   ├── Scenes/
│   ├── Scripts/
│   ├── Prefabs/
│   ├── Art/
│   │   ├── Materials/
│   │   ├── Textures/
│   │   ├── Models/
│   │   └── Animations/
│   ├── Audio/
│   ├── UI/
│   ├── Settings/
│   └── Sandbox/
└── ThirdParty/
```

필요한 폴더만 만드는 예시다. 빈 폴더를 미리 전부 만들지 않는다(**권장**). `Scripts`는 위치만 안내하며 C# 내부 구조를 결정하지 않는다. `Settings`는 직접 만든 설정 에셋의 위치이며 프로젝트 루트의 `ProjectSettings`를 옮기는 곳이 아니다.

- **권장:** UI 전용 Prefab·이미지 등은 `UI/` 아래에, 여러 영역이 공유하는 시각 자료는 `Art/`에 둔다.
- **권장:** 실험용 Scene·자료는 `Sandbox/`로 구분하고 제작용 콘텐츠가 의존하지 않게 관리한다. 폴더 이름만으로 빌드에서 제외되지는 않는다.
- **권장:** 외부 자료는 직접 만든 자료와 분리한다. 이동 가능한 외부 에셋은 `ThirdParty/<공급자 또는 패키지명>/`에 둘 수 있다. 고정 경로를 요구하는 도구·패키지는 공급자의 배치를 유지한다.
- **필수:** Package Manager 패키지를 이 구조에 맞추려고 `Assets/ThirdParty/`로 이동하지 않는다. 패키지의 관리 방식을 유지한다.
- **선택:** 함께 수정할 파일이 여러 폴더에 흩어져 관리가 어려우면 `Assets/_Project/Characters/Player/`처럼 기능·개체별 구조로 전환한다. 필요하면 그 아래에 `Prefabs/`, `Models/`, `Animations/`를 둔다. 전용 자료와 공용 자료의 위치를 프로젝트에 기록한다.

기능별 구조와 종류별 구조에 같은 원본을 중복 보관하지 않는다(**필수**). 구체적인 프로젝트 트리와 전환 이유는 [프로젝트별 문서](../projects/index.md)에 기록한다.

### Unity 예약 폴더와 예외

**필수:** `Editor`, `Resources`, `Plugins`, `StreamingAssets` 등은 Unity 동작에 영향을 주는 이름으로 취급한다. 필요할 때만 해당 프로젝트의 Unity 버전·플랫폼 문서를 확인하고 생성한다. 기본 트리에 이 폴더들을 자동 추가하지 않는다.

Unity 6.0 문서에서 `StreamingAssets`는 `Assets` 바로 아래 위치를 요구한다. `Editor Default Resources`처럼 공백을 포함한 예약 이름도 있다. 이런 계약은 `_Project` 내부 배치나 공백 없는 이름 제안보다 우선한다. `Editor` 코드의 구체적인 분리와 assembly definition 구성은 이번 초안에서 결정하지 않는다.

## 이름 변경·이동과 참조 보존

- **권장:** 에셋과 폴더의 이동·재명명은 Unity Project 창에서 수행한다.
- **필수:** 외부 도구로 이동·재명명할 때는 대응하는 `.meta`도 함께 처리해 기존 GUID를 보존한다. `.meta`를 지워 이름을 정리하지 않는다.
- **필수:** 버전 관리 대상 에셋의 `.meta`도 함께 관리한다. 자동 생성된 파일이라는 이유만으로 제외하지 않는다.
- **필수:** 변경 후 관련 Scene·Prefab의 참조와 이름·경로 문자열을 사용하는 로딩·도구를 확인한다. GUID 보존만으로 문자열 참조까지 갱신되었다고 가정하지 않는다.

이번 문서 작성은 기존 프로젝트의 일괄 이동·재명명을 지시하지 않는다. 실제 적용은 변경 범위와 프로젝트 제약을 기록하고 진행한다.

## 미결정·후속 범위

- 초안 전체의 채택 여부. 종류 접두어·맵 접미어는 [대상별 예시와 추가 조건](#대상별-예시와-추가-조건)의 미결정 범위를 따른다.
- Tag·Layer·Sorting Layer, Addressables 주소·그룹, ScriptableObject 종류별 명명.
- C# 명명·포맷·수명 관리, assembly definition, 자동 검사·폴더 생성 도구.
- 이번 범위에서 보류·폐기로 확정한 안은 없다. 기능별 폴더는 조건부 선택이며 폐기안이 아니다.

## 관련 문서

- [컨벤션 적용 기준](../baseline.md)
- [원본과 생성물 관리 (초안)](../git/artifacts.md)
- [프로젝트별 규칙](../projects/index.md)

## 근거와 출처

사용자가 요청한 오브젝트·에셋 이름, 기본 폴더, `Wall_1` 같은 반복 이름과 공백·`_` 논의를 바탕으로 작성했다. [기존 C++ 명명](../coding/cpp/naming.md)과 [과거 컨벤션](../../ref/CodingConvention.md), [정리본](../../ref/DevRnimanConvention/CodingConvention.md)의 PascalCase·의미가 드러나는 이름을 참고했지만 C++의 `m`·`s`·`g` 접두어를 Unity 오브젝트에 확대하지 않았다.

Unity 공식 가이드는 일관된 이름, 공백 없는 파일·폴더, 자체 자료와 외부 자료의 분리를 권고하며 단일 정답 구조를 정하지 않는다. 이 초안의 PascalCase, 번호 앞 `_`, 두 자리 번호, `_Project`와 구체적인 트리는 개인 제안이다. 검색과 식별을 쉽게 하고 초기 분류를 단순하게 하려는 이유로 제안했다. 자동 복제 이름 허용은 반복적인 수동 정리 비용에 대한 사용자 피드백을 반영한 개인 제안이며 공식 명명 규칙으로 간주하지 않는다. 공식 가이드의 일괄 재명명 권고와 달리 기존 프로젝트에는 영향 범위를 확인해 점진적으로 적용한다.

공식 자료 확인일: 2026-09-30. 프로젝트 구성 가이드는 별도 명세 버전이 없는 온라인 문서다. 엔진 동작의 확인 자료는 Unity 6.0(6000.0) Manual이며, 이는 프로젝트 버전 채택을 뜻하지 않는다. 다른 버전에서 예약 경로·도구 동작이 달라지면 해당 버전 자료를 확인하고 프로젝트 예외를 기록한다.

- [Unity 프로젝트 구성 가이드 — Folder structure / Naming standards](https://unity.com/how-to/organizing-your-project): 명명·분류 권고와 자체·외부 자료 구분.
- [Unity Manual — Asset IDs](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html#asset-ids) · [Meta files / Moving and renaming assets](https://docs.unity3d.com/6000.0/Documentation/Manual/AssetMetadata.html#meta-files): 에셋 식별과 이동 시 메타데이터 보존.
- [Unity Manual — Reserved folder name reference](https://docs.unity3d.com/6000.0/Documentation/Manual/SpecialFolders.html): 예약 폴더 이름·위치·용도.
- [Unity Manual — Transforms, Properties / Parenting](https://docs.unity3d.com/6000.0/Documentation/Manual/class-Transform.html): 부모 기준 Transform과 계층 관계.

## 변경 기록

- 2026-09-30: Unity 명명·Hierarchy 묶음 관리·폴더 구조·참조 보존 초안을 작성했다. 명명은 PascalCase를 기본으로 직접 관리하는 번호에 `_`를 사용하며, 동명 배치와 자동 복제 이름을 허용한다. 공통 규칙과 대상별 예시를 통합하고 빈 GameObject 그룹의 적용 기준을 정리했다. Unity 버전은 공통 고정하지 않으며 종류 접두어·C# 규칙은 미결정으로 남겼다.
